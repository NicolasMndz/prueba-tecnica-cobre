# Motor Inteligente de Optimización de Liquidez Multi-Banco y Flujo de Caja

> **Prueba Técnica:** Technical Lead Data Science (Liquidity & Cash Flow)  
> **Compañía:** Cobre — B2B Payments & Liquidity Infrastructure  
> **Candidato:** Nicolás Méndez Gutiérrez  
> **Marco Metodológico:** CRISP-DM Industrial | **Período de Evaluación:** 70 días fuera de muestra (*Out-of-Sample*)  

---

## 1. Mapeo Maestro: Partes de la Prueba Técnica vs. Archivos Entregables

A continuación se detalla cómo se da cumplimiento riguroso a cada requerimiento de la prueba oficial de Cobre (`Candidate Test - Technical Lead DS (Liquidity) EN.pdf`) y con qué archivos específicos se responde cada parte:

| Parte de la Prueba Técnica | Descripción del Requerimiento Oficial | Archivo(s) de Respuesta | Enfoque y Cómo se Cumple |
| :--- | :--- | :--- | :--- |
| **Parte 1: Diagnosticar y Corregir (Hands-on Fix)** | Revisar el código inicial del squad, diagnosticar qué falló en los datos y el modelado, reconstruir el pipeline de curaduría y explicar el impacto en lenguaje de negocio. | • [`clean_data_pipeline.py`](clean_data_pipeline.py)<br>• [`test_data_integrity.py`](test_data_integrity.py)<br>• [`TECHNICAL_MEMO_DATA_SCIENCE.md`](TECHNICAL_MEMO_DATA_SCIENCE.md) (Sec. 2 y 3) | • **Auditoría Forense:** Detección de las 5 fallas críticas: descarte del 18.3% de datos por fechas multiformato (`YYYY-MM-DD`, `DD/MM/YYYY`, `MM-DD-YYYY`), 4 inversiones de signo (débitos como créditos), 3 errores de escala decimal 10x ($400M vs $40M MXN), ceguera de divisa al transferir y modelado de stock en vez de flujo.<br>• **Reconciliación Contable:** Pipeline determinístico que restaura la identidad física contable ($B_t = B_{t-1} + I_t - O_t$) con residuo mediano exactamente igual a `0.0000`, preservando el 100% de los registros (270 días continuos $\times$ 6 cuentas = 1,620 filas).<br>• **Suite de Calidad:** 6 pruebas automatizadas en `pytest` que certifican continuidad temporal, completitud sin nulos y límites físicos. |
| **Parte 2: Diseñar una Mejor Solución (Forecasting & Sizing)** | Proponer un método sólido y explicable para predecir flujos y decidir cuándo y cuánto mover capital, minimizando riesgo de déficit y costos de fricción bancaria. | • [`run_backtest_simulation.py`](run_backtest_simulation.py)<br>• [`TECHNICAL_MEMO_DATA_SCIENCE.md`](TECHNICAL_MEMO_DATA_SCIENCE.md) (Sec. 4 y 5) | • **Física de Tanque vs. Caudal:** Transición del modelado de saldos integrados $I(1)$ al pronóstico de flujos netos diarios estacionarios $I(0)$ mediante regresión regularizada Ridge L2 ($\alpha=10.0$) con factores de calendario B2B (estacionalidad semanal, quincenas y fin de mes).<br>• **Motor Desacoplado en Dos Capas:** Separación del **Sensor Predictivo** (evalúa riesgo al lead time $T+L$ con 99% de confianza, $Z_\alpha=2.326$) del **Amortiguador de Fondeo** (dimensiona el target para garantizar 14 días de autonomía quincenal, $H=14$).<br>• **Regla de Solvencia Inviolable:** Blindaje del piso de reserva de la cuenta matriz (`ACC-001`) para erradicar su descapitalización. |
| **Parte 3: Explicar a Dos Públicos Objetivo (Dual Audience)** | Entregar dos explicaciones de la solución adaptadas a sus audiencias:<br>1. Técnica para el Data Scientist del squad.<br>2. De negocio para el Comité de Tesorería / Finanzas (CFO). | • **Audiencia Técnica:** [`TECHNICAL_MEMO_DATA_SCIENCE.md`](TECHNICAL_MEMO_DATA_SCIENCE.md)<br>• **Audiencia Tesorería:** [`presentacion_ejecutiva_tesoreria.pptx`](presentacion_ejecutiva_tesoreria.pptx) | • **Para Data Science:** Documento técnico formal de 300+ líneas con rigor econométrico, supuestos de estacionariedad, formulación analítica de pérdidas, cuantificación de riesgo de cola, intervalos de confianza y protocolo MLOps.<br>• **Para Tesorería:** Presentación ejecutiva en PowerPoint (11 diapositivas panorámicas 16:9), sin fórmulas complejas, con analogías intuitivas (tanque vs. caudal), scorecard financiero comparativo de los 3 modelos (Inacción, Squad, Propuesto) y cero notas al orador (diseñada para lectura y decisión ejecutiva inmediata). |
| **Parte 4: Formas de Trabajo con IA (Ways of Working)** | Transparentar dónde sí se usaron herramientas de IA (agentes, asistentes) y dónde deliberadamente NO se utilizaron, destacando el criterio del liderazgo humano. | • [`TECHNICAL_MEMO_DATA_SCIENCE.md`](TECHNICAL_MEMO_DATA_SCIENCE.md) (Sec. 7)<br>• [`presentacion_ejecutiva_tesoreria.pptx`](presentacion_ejecutiva_tesoreria.pptx) (Slide 10) | • **Dónde SÍ IA (~60% de ahorro de tiempo):** Scaffolding acelerado de pruebas unitarias en `pytest`, regex complejas para normalización multiformato de fechas, linters de código (PEP-8) y benchmarking de literatura sobre modelos $(s, S)$ de control de inventarios.<br>• **Dónde NO IA (Criterio Humano Irreemplazable):** Diagnóstico forense contable (la IA sugería imputar con la media o suavizar, lo que ocultaba el error 10x), causalidad temporal $T+L$ sin filtración de futuro (*zero lookahead bias*), desacoplamiento sensor vs. amortiguador y diseño de los 4 Circuit Breakers automáticos. |
| **Parte 5: Blueprint de Puesta en Producción** | Describir arquitectura de producción: pipeline de datos, orquestación, monitoreo continuo y salvaguardas (circuit breakers). | • [`TECHNICAL_MEMO_DATA_SCIENCE.md`](TECHNICAL_MEMO_DATA_SCIENCE.md) (Sec. 6)<br>• [`presentacion_ejecutiva_tesoreria.pptx`](presentacion_ejecutiva_tesoreria.pptx) (Slide 09) | • **Pipeline & Calidad:** Ingesta Snowflake $\rightarrow$ Compuertas contables en `dbt` / Great Expectations $\rightarrow$ Microservicio de inferencia.<br>• **Orquestación:** DAG diario en Apache Airflow a las 06:00 UTC (antes de la apertura de rieles ACH 07:00 COT y SPEI 06:00 CDMX).<br>• **Monitoreo MLOps:** Pruebas Kolmogorov-Smirnov y Population Stability Index ($\text{PSI} < 0.10$) para detección de deriva de datos (*data drift*), y seguimiento de MAE diario frente a bandas de volatilidad.<br>• **4 Circuit Breakers en Código:** Integridad Contable Cero-Tolerancia, Solvencia Inviolable del Donante, Techo Diario del 15% de Activos Líquidos y Aislamiento Cambiario Estricto. |

---

## 2. Estructura del Repositorio

El repositorio contiene estrictamente los archivos necesarios para la auditoría, reproducción y evaluación de la solución técnica:

```
.
├── README.md                                  # Guía Maestra de Navegación y Mapeo contra la Prueba
├── TECHNICAL_MEMO_DATA_SCIENCE.md             # Documento Técnico Formal (Partes 1 a 5 para DS y C-Level)
├── presentacion_ejecutiva_tesoreria.pptx      # Presentación Ejecutiva a Tesorería (11 slides, sin fórmulas)
│
├── accounts.csv                               # Catálogo maestro de cuentas y umbrales (Original Cobre)
├── account_balances_daily_RAW.csv             # Datos crudos de saldos diarios (Original Cobre)
├── transfers_log_RAW.csv                      # Libro crudo de transferencias (Original Cobre)
├── account_balances_daily_CLEAN.csv           # Dataset saneado y reconciliado con residuo contable cero
├── transfers_log_CLEAN.csv                    # Transferencias estandarizadas en formato ISO-8601
│
├── clean_data_pipeline.py                     # Parte 1: Pipeline de saneamiento forense y reconciliación
├── test_data_integrity.py                     # Parte 1: Suite pytest de aserción contable y contratos
├── run_backtest_simulation.py                 # Parte 2 y 5: Simulación causal OOS de los 3 protocolos
│
├── requirements.txt                           # Dependencias de Python reproducibles
├── Candidate Test - Technical Lead DS (Liquidity) EN.pdf # Enunciado oficial de la prueba técnica
│
└── presentation_assets/                       # Gráficos de soporte en alta resolución (300 DPI)
    ├── chart_forensic_audit.png               # Auditoría forense y reconciliación contable
    ├── chart_flow_seasonality.png             # Estacionalidad semanal y picos de nómina
    ├── chart_feature_importance.png           # Explicabilidad económica de variables Ridge
    ├── chart_backtest_trajectories.png        # Trayectorias de saldo fuera de muestra (70 días)
    ├── chart_kpi_comparison.png               # Comparativa visual de métricas de gestión
    └── chart_production_pipeline.png          # Arquitectura productiva y 4 circuit breakers
```

---

## 3. Guía de Ejecución Rápida y Reproducibilidad (Quickstart)

Todo el proyecto está diseñado para ejecutarse y verificarse de forma 100% reproducible mediante scripts `.py`:

### Paso 1: Clonar el repositorio e instalar dependencias
```bash
git clone https://github.com/NicolasMndz/prueba-tecnica-cobre.git
cd prueba-tecnica-cobre
pip install -r requirements.txt
```

### Paso 2: Ejecutar el pipeline de curaduría forense de datos (Parte 1)
```bash
python clean_data_pipeline.py
```
*Salida esperada:* Recuperación del 100% de las fechas (293 días crudos), deduplicación y alineación a 270 días continuos para las 6 cuentas (1,620 registros), corrección de los 4 signos invertidos y los 3 errores de escala decimal 10x, y verificación de residuo contable promedio de `0.00`.

### Paso 3: Validar la suite de pruebas unitarias y contratos contables (`pytest`)
```bash
pytest test_data_integrity.py
```
*Salida esperada:* `6 passed in ~0.7s` (continuidad temporal sin huecos, completitud sin nulos, no negatividad, integridad referencial y cuadre contable exacto).

### Paso 4: Ejecutar la simulación de backtesting fuera de muestra (Partes 2 y 5)
```bash
python run_backtest_simulation.py
```
*Salida esperada:*
* **Protocolo Inacción:** 109 días en déficit | 0 transferencias | $0.00 comisiones.
* **Protocolo Squad:** 2 días en déficit | 97 transferencias | Drenaje caótico multimoneda.
* **Protocolo Propuesto (Lead DS):** **0 días en déficit (100.0% SLA) | 3 transferencias | $50 USD + $20 MXN ($0 COP)**.
