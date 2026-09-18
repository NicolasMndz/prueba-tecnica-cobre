# run_backtest_simulation.py
# Motor de Simulacion y Backtesting Comparativo de Politicas de Rebalanceo
# Technical Lead, Data Science - Cobre

import pandas as pd
import numpy as np

# Cargar datos limpios
balances = pd.read_csv('account_balances_daily_CLEAN.csv')
balances['date'] = pd.to_datetime(balances['date'])

THRESHOLDS = {
    'ACC-001': 1_000_000_000, # 1,000M COP
    'ACC-002': 100_000,       # 100k USD
    'ACC-004': 40_000_000,    # 40M MXN
}

RESERVE_FLOORS = {
    'ACC-003': 1_000_000_000, # 1,000M COP
    'ACC-006': 50_000,        # 50k USD
    'ACC-005': 30_000_000,    # 30M MXN
}

PARTNERS = {
    'ACC-001': 'ACC-003',
    'ACC-002': 'ACC-006',
    'ACC-004': 'ACC-005'
}

LEAD_TIMES = {
    ('ACC-003', 'ACC-001'): 1,
    ('ACC-006', 'ACC-002'): 1,
    ('ACC-005', 'ACC-004'): 0
}

FEES = {
    'ACC-001': 50000.0,
    'ACC-002': 25.0,
    'ACC-004': 20.0
}

# ==============================================================================
# PARAMETRIZACION ESTOCASTICA Y REGLAS DE DECISION DINAMICAS (OPERATIONS RESEARCH)
# ==============================================================================
Z_ALPHA = 2.326               # Confianza 99% -> P(Deficit) <= 1% (Requisito Cobre)
HORIZON_AUTONOMY_DAYS = 14    # Horizonte de autonomia operacional (Ciclo quincenal)

def calculate_dynamic_safety_stock(threshold: float, sigma_outflow: float, lead_time: int, z_alpha: float = Z_ALPHA) -> float:
    """
    SENSOR DE ALERTA: Calcula el Safety Stock Dinamico a horizonte de liquidacion bancaria L.
    Formula: SS_i = Threshold_i + Z_alpha * sigma_i * sqrt(L_i)
    """
    return threshold + z_alpha * sigma_outflow * np.sqrt(max(1, lead_time))

def calculate_dynamic_target_balance(threshold: float, expected_burn_horizon: float, sigma_outflow: float, 
                                     horizon_days: int = HORIZON_AUTONOMY_DAYS, z_alpha: float = Z_ALPHA) -> float:
    """
    AMORTIGUADOR DE FONDEO (SIZING): Calcula el Target Balance Dinamico a horizonte H dias.
    Formula: Target_i = Threshold_i + Burn_H + Z_alpha * sigma_i * sqrt(H)
    Cero heuristicas fijas (ej. 130% arbitrario): cada peso se justifica en volatilidad y consumo esperado.
    """
    burn_allowance = max(0.0, -expected_burn_horizon)
    diffusion_buffer = z_alpha * sigma_outflow * np.sqrt(horizon_days)
    return threshold + burn_allowance + diffusion_buffer

cutover = '2025-07-20'
test_dates = balances[balances.date >= cutover]['date'].sort_values().unique()

# Precalcular estadisticas historicas previas al cutover (para no tener data leakage)
hist = balances[balances.date < cutover]
outflow_std = hist.groupby('account_id')['outflow'].std().to_dict()
dow_netflow_mean = hist.groupby(['account_id', 'day_of_week_num'])['net_flow'].mean().to_dict()

# ==========================================
# SIMULADOR DE POLITICAS DE REBALANCEO
# ==========================================
def run_simulation(policy_name):
    # Estado inicial: saldos en el dia inmediatamente anterior al cutover
    prev_date = balances[balances.date < cutover]['date'].max()
    curr_b = balances[balances.date == prev_date].set_index('account_id')['balance'].to_dict()
    
    pending_transfers = [] # lista de dicts: {'arrive_date': d, 'to_acc': acc, 'amount': amt}
    
    shortfall_events = {acc: 0 for acc in THRESHOLDS}
    shortfall_volume = {acc: 0.0 for acc in THRESHOLDS}
    transfers_count = 0
    total_fees = {'COP': 0.0, 'USD': 0.0, 'MXN': 0.0}
    
    for dt in test_dates:
        dt = pd.to_datetime(dt)
        dow = dt.dayofweek
        
        # 1. Aplicar transferencias que llegan hoy
        ready = [t for t in pending_transfers if t['arrive_date'] == dt]
        pending_transfers = [t for t in pending_transfers if t['arrive_date'] > dt]
        for t in ready:
            curr_b[t['to_acc']] += t['amount']
            
        # 2. Obtener flujos comerciales reales del dia
        flows_today = balances[balances.date == dt].set_index('account_id')[['inflow', 'outflow']].to_dict(orient='index')
        
        # 3. Decision de rebalanceo segun la politica
        if policy_name == 'squad':
            # Politica squad: si trailing 14d mean < threshold, transferir desde idxmax crudo
            for acc, th in THRESHOLDS.items():
                past_14 = balances[(balances.account_id == acc) & (balances.date <= dt) & (balances.date > dt - pd.Timedelta(days=14))]
                fc = past_14['balance'].mean()
                if fc < th:
                    donor = pd.Series(curr_b).drop(index=acc).idxmax()
                    shortfall = th - fc
                    if curr_b[donor] >= shortfall:
                        curr_b[donor] -= shortfall
                        curr_b[acc] += shortfall
                        transfers_count += 1
                        
        elif policy_name == 'proposed':
            # Politica propuesta por Technical Lead:
            # Desacoplamiento estricto: Sensor a Lead Time L vs Amortiguador Dinamico a Horizonte H
            for acc, th in THRESHOLDS.items():
                donor = PARTNERS[acc]
                L = LEAD_TIMES.get((donor, acc), 1)
                
                # Proyeccion de flujo neto esperado en los proximos L dias (horizonte de liquidacion)
                expected_burn_L = sum(dow_netflow_mean.get((acc, (dow + step) % 7), 0.0) for step in range(1, L + 1))
                sigma = outflow_std.get(acc, 0.0)
                
                # 1. SENSOR: Safety Stock Dinamico
                safety_buffer = calculate_dynamic_safety_stock(th, sigma, L, z_alpha=Z_ALPHA)
                b_proj = curr_b[acc] + expected_burn_L
                
                # 2. GATILLO: Se activa si el saldo proyectado a la llegada rompe el buffer
                if b_proj < safety_buffer:
                    # 3. SIZING: Target Balance Dinamico a horizonte H=14 dias
                    expected_burn_H = sum(dow_netflow_mean.get((acc, (dow + step) % 7), 0.0) for step in range(1, HORIZON_AUTONOMY_DAYS + 1))
                    target_dynamic = calculate_dynamic_target_balance(th, expected_burn_H, sigma, horizon_days=HORIZON_AUTONOMY_DAYS, z_alpha=Z_ALPHA)
                    
                    deficit = target_dynamic - b_proj
                    donor_surplus = max(0.0, curr_b[donor] - RESERVE_FLOORS[donor])
                    amt = min(deficit, donor_surplus)
                    
                    if amt > 0.02 * th: # umbral de materialidad
                        curr_b[donor] -= amt
                        transfers_count += 1
                        curr_name = 'COP' if acc == 'ACC-001' else ('USD' if acc == 'ACC-002' else 'MXN')
                        total_fees[curr_name] += FEES[acc]
                        
                        arrive_dt = dt + pd.Timedelta(days=L)
                        if L == 0:
                            curr_b[acc] += amt
                        else:
                            pending_transfers.append({'arrive_date': arrive_dt, 'to_acc': acc, 'amount': amt})
                            
        # 4. Actualizar saldos finales del dia con los flujos comerciales
        for acc in curr_b:
            inf = flows_today[acc]['inflow']
            outf = flows_today[acc]['outflow']
            curr_b[acc] += (inf - outf)
            
        # 5. Medir shortfalls
        for acc, th in THRESHOLDS.items():
            if curr_b[acc] < th:
                shortfall_events[acc] += 1
                shortfall_volume[acc] += (th - curr_b[acc])
                
    return {
        'policy': policy_name,
        'shortfall_days': shortfall_events,
        'shortfall_volume': shortfall_volume,
        'transfers_count': transfers_count,
        'total_fees': total_fees
    }

print('=== RESULTADOS DEL BACKTESTING (70 DIAS FUERA DE MUESTRA) ===')
for pol in ['none', 'squad', 'proposed']:
    res = run_simulation(pol)
    print(f'\n--- POLITICA: {pol.upper()} ---')
    print('Dias en Shortfall por cuenta:', res['shortfall_days'])
    print('Total dias shortfall sumados:', sum(res['shortfall_days'].values()))
    print('Numero de transferencias:', res['transfers_count'])
    print('Comisiones pagadas:', res['total_fees'])
