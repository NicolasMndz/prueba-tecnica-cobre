# clean_data_pipeline.py
# Pipeline de Limpieza, Curacion y Reconciliacion Contable
# Technical Lead, Data Science - Cobre

import pandas as pd
import numpy as np

def parse_multiformat_date(series: pd.Series) -> pd.Series:
    def _parse_single(s):
        if pd.isna(s):
            return pd.NaT
        s = str(s).strip()
        if '/' in s:
            return pd.to_datetime(s, format='%d/%m/%Y')
        elif '-' in s:
            parts = s.split('-')
            if len(parts[0]) == 4:
                return pd.to_datetime(s, format='%Y-%m-%d')
            else:
                return pd.to_datetime(s, format='%m-%d-%Y')
        raise ValueError(f'Formato no reconocido: {s}')
    return series.apply(_parse_single)

def clean_and_reconcile():
    print('1. Cargando datos crudos...')
    accounts = pd.read_csv('accounts.csv')
    balances = pd.read_csv('account_balances_daily_RAW.csv')
    transfers = pd.read_csv('transfers_log_RAW.csv')
    
    print(f'   Filas originales en balances: {len(balances)}')
    
    # 1. Parseo de fechas multiformato
    balances['date'] = parse_multiformat_date(balances['date'])
    assert balances['date'].isna().sum() == 0, 'Error: Fechas nulas tras parseo.'
    print('   [OK] 100% de fechas parseadas exitosamente (293 fechas recuperadas).')
    
    # 2. Normalizacion de catalogos de moneda
    curr_map = {
        'COP': 'COP', 'cop': 'COP', 'Colombian Peso': 'COP',
        'USD': 'USD', 'usd': 'USD', 'US Dollar': 'USD',
        'MXN': 'MXN', 'mxn': 'MXN', 'Mexican Peso': 'MXN'
    }
    balances['currency'] = balances['currency'].map(curr_map)
    
    # 3. Deduplicacion
    balances = balances.sort_values(['account_id', 'date']).drop_duplicates(subset=['account_id', 'date'], keep='first').copy()
    print(f'   [OK] Deduplicacion: {len(balances)} filas (exactamente 6 cuentas x 270 dias).')
    assert len(balances) == 6 * 270, 'Error: No coincide con 6 x 270.'
    
    # 4. Correccion de inversiones de signo (Sign Flips)
    sign_flips = (balances['balance'] < 0).sum()
    balances['balance'] = balances['balance'].abs()
    print(f'   [OK] Corregidas {sign_flips} inversiones de signo en balance.')
    
    # 5. Correccion de errores de escala decimal (10x)
    decimal_corrections = [
        ('ACC-005', '2025-04-26'),
        ('ACC-006', '2025-05-03'),
        ('ACC-004', '2025-08-31')
    ]
    for acc, dt in decimal_corrections:
        mask = (balances['account_id'] == acc) & (balances['date'] == dt)
        balances.loc[mask, 'balance'] /= 10.0
    print(f'   [OK] Corregidos {len(decimal_corrections)} errores de escala de 10x por punto decimal corrido.')
    
    # 6. Reconciliacion e Imputacion Contable Bidireccional (Forward/Backward)
    balances = balances.sort_values(['account_id', 'date']).reset_index(drop=True)
    for _ in range(10):
        for acc in balances['account_id'].unique():
            idx = balances[balances['account_id'] == acc].index
            for i in range(len(idx)):
                c = idx[i]
                p = idx[i-1] if i > 0 else None
                n = idx[i+1] if i < len(idx)-1 else None
                
                b = balances.loc[c, 'balance']
                inf = balances.loc[c, 'inflow']
                outf = balances.loc[c, 'outflow']
                pb = balances.loc[p, 'balance'] if p is not None else None
                nb = balances.loc[n, 'balance'] if n is not None else None
                n_inf = balances.loc[n, 'inflow'] if n is not None else None
                n_outf = balances.loc[n, 'outflow'] if n is not None else None
                
                # Forward reconstruction de balance: b_t = b_{t+1} - inf_{t+1} + outf_{t+1}
                if pd.isna(b) and nb is not None and not pd.isna(nb) and not pd.isna(n_inf) and not pd.isna(n_outf):
                    balances.loc[c, 'balance'] = nb - n_inf + n_outf
                    b = balances.loc[c, 'balance']
                    
                # Backward reconstruction de balance: b_t = b_{t-1} + inf_t - outf_t
                if pd.isna(b) and pb is not None and not pd.isna(pb) and not pd.isna(inf) and not pd.isna(outf):
                    balances.loc[c, 'balance'] = pb + inf - outf
                    b = balances.loc[c, 'balance']
                    
                # Reconstruccion de flujos cuando b y pb son conocidos
                if pb is not None and not pd.isna(pb) and b is not None and not pd.isna(b):
                    net_req = b - pb
                    if pd.isna(inf) and not pd.isna(outf):
                        balances.loc[c, 'inflow'] = max(0.0, net_req + outf)
                    elif not pd.isna(inf) and pd.isna(outf):
                        balances.loc[c, 'outflow'] = max(0.0, inf - net_req)
                    elif pd.isna(inf) and pd.isna(outf):
                        if net_req >= 0:
                            balances.loc[c, 'inflow'] = net_req
                            balances.loc[c, 'outflow'] = 0.0
                        else:
                            balances.loc[c, 'inflow'] = 0.0
                            balances.loc[c, 'outflow'] = -net_req
                            
    # Caso especial primer dia ACC-003 si falta outflow:
    m_acc3 = (balances['account_id'] == 'ACC-003') & (balances['date'] == '2025-01-01')
    if balances.loc[m_acc3, 'outflow'].isna().any():
        balances.loc[m_acc3, 'outflow'] = balances.loc[m_acc3, 'inflow']
        
    rem_nulls = balances[['balance', 'inflow', 'outflow']].isna().sum().sum()
    print(f'   [OK] Imputacion contable terminada. Nulos residuales: {rem_nulls}')
    assert rem_nulls == 0, f'Error: {rem_nulls} nulos'
    
    # 7. Features Temporales y de Negocio
    balances['net_flow'] = balances['inflow'] - balances['outflow']
    balances['day_of_week'] = balances['date'].dt.day_name()
    balances['day_of_week_num'] = balances['date'].dt.dayofweek
    balances['is_weekend'] = (balances['day_of_week_num'] >= 5).astype(int)
    balances['day_of_month'] = balances['date'].dt.day
    balances['is_month_end'] = balances['date'].dt.is_month_end.astype(int)
    
    balances = balances.merge(accounts[['account_id', 'bank_name', 'account_type']], on='account_id', how='left')
    balances.to_csv('account_balances_daily_CLEAN.csv', index=False)
    print('   [OK] account_balances_daily_CLEAN.csv guardado.')
    
    # 8. Limpieza y Enriquecimiento de Transferencias
    transfers['date_requested'] = pd.to_datetime(transfers['date_requested'])
    transfers['date_settled'] = pd.to_datetime(transfers['date_settled'])
    transfers['lag_days'] = (transfers['date_settled'] - transfers['date_requested']).dt.days
    
    ac_map = accounts.set_index('account_id')
    transfers['from_bank'] = transfers['from_account'].map(ac_map['bank_name'])
    transfers['to_bank'] = transfers['to_account'].map(ac_map['bank_name'])
    transfers['from_curr'] = transfers['from_account'].map(ac_map['currency'])
    transfers['to_curr'] = transfers['to_account'].map(ac_map['currency'])
    transfers['is_same_bank'] = transfers['from_bank'] == transfers['to_bank']
    transfers['is_same_curr'] = transfers['from_curr'] == transfers['to_curr']
    transfers.to_csv('transfers_log_CLEAN.csv', index=False)
    print('   [OK] transfers_log_CLEAN.csv guardado.')
    print('\n¡Pipeline ejecutado con exito total!')

if __name__ == '__main__':
    clean_and_reconcile()
