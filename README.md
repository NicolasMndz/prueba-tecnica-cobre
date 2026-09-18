# Motor Inteligente de Optimización de Liquidez Multi-Banco y Flujo de Caja

> **Prueba Técnica:** Technical Lead Data Science (Liquidity & Cash Flow)  
> **Compañía:** Cobre — B2B Payments & Liquidity Infrastructure  
> **Candidato:** Nicolás Méndez Gutiérrez  
> **Marco Metodológico:** CRISP-DM Industrial | **Período de Evaluación:** 70 días fuera de muestra (*Out-of-Sample*)  

---

## 1. Resumen Ejecutivo y Resultados de Negocio

Este repositorio contiene la resolución técnica integral de la prueba para el rol de **Technical Lead Data Science** en Cobre. El objetivo es transformar una gestión de liquidez reactiva en un **motor predictivo y estocástico de optimización de transferencias multi-banco y multi-divisa (COP, USD, MXN)**.

### Resultados Cuantitativos Clave (Evaluación en 70 Días Out-of-Sample):
* **Cero Quiebres Operacionales (100.0% Cumplimiento de SLA):** Se eliminaron por completo los eventos de déficit de saldo en todas las cuentas operativas de dispersión (frente a 109 días de quiebre en inacción y 2 días en el modelo del squad).
* **Reducción del 96.9% en Fricción Bancaria:** Se pasó de 97 transferencias caóticas y desordenadas (1.4 órdenes diarias del squad) a **únicamente 3 fondeos estratégicos amortiguados** (1 cada 23 días).
* **Costo Transaccional Marginal:** El gasto total en comisiones bancarias durante todo el trimestre fue de solo **$50 USD** (2 transferencias internacionales SWIFT de $25 USD) y **$20 MXN** (1 transferencia local SPEI), erradicando el sangrado de tarifas y sobrecostos cambiarios.
* **Solvencia Patrimonial Intacta:** La cuenta matriz donante (`ACC-001` Bancolombia en COP) mantuvo un saldo mínimo de **$1,942.0M COP (+94.2% sobre su piso de seguridad)** y generó **+$12.97M COP adicionales** en saldo promedio remunerado (*float*) frente al modelo previo.

---

## 2. Mapeo Maestro: Partes de la Prueba Técnica vs. Archivos Entregables

A continuación se detalla con precisión quirúrgica qué archivo da respuesta a cada parte del examen oficial de Cobre (`Candidate Test - Technical Lead DS (Liquidity) EN.pdf`):

| Parte de la Prueba Técnica | Descripción del Requerimiento | Archivo(s) de Respuesta | Enfoque y Contenido Entregado |
| :--- | :--- | :--- | :--- |
| **Parte 1: Diagnosticar y Corregir (Hands-on)** | Revisar el notebook inicial del squad, identificar fallas de datos y modelado, reconstruir el pipeline y explicar en lenguaje de negocio su impacto. | • [`clean_data_pipeline.py`](clean_data_pipeline.py)<br>• [`test_data_integrity.py`](test_data_integrity.py)<br>• [`flawed_model_squad_draft.ipynb`](flawed_model_squad_draft.ipynb)<br>• [`solution_notebook.ipynb`](solution_notebook.ipynb) (Sec. 1-2) | • **Auditoría Forense:** Descubrimiento del descarte del 18% de datos por fechas multiformato, error de escala decimal 10x ($400M vs $40M MXN) y 4 inversiones de signo.<br>• **Reconciliación Contable:** Pipeline determinístico que restaura la identidad contable física con residuo cero (`0.00`).<br>• **Suite de Calidad:** 6 pruebas automatizadas en `pytest` para certificar la integridad de datos antes de modelar. |
| **Parte 2: Diseñar una Mejor Solución (Forecasting & Sizing)** | Diseñar un método sólido y explicable para decidir cuándo y cuánto mover capital, minimizando riesgo de déficit y costos de fricción bancaria. | • [`solution_notebook.ipynb`](solution_notebook.ipynb) (Sec. 3-5)<br>• [`run_backtest_simulation.py`](run_backtest_simulation.py)<br>• [`TECHNICAL_MEMO_DATA_SCIENCE.md`](TECHNICAL_MEMO_DATA_SCIENCE.md) (Sec. 4) | • **Física de Tanque vs. Caudal:** Abandono del pronóstico de saldos acumulativos $I(1)$ y adopción de Flujos Netos Diarios $I(0)$ con Ridge L2 y features de calendario B2B (quincenas, fines de mes, estacionalidad semanal).<br>• **Arquitectura en Dos Capas:** Separación del sensor predictivo (anticipa al lead time $T+L$ con 99% confianza) del amortiguador de fondeo (colchón de absorción para 14 días).<br>• **Regla de Solvencia:** Blindaje inviolable de la cuenta matriz (`ACC-001`) para evitar su descapitalización. |
| **Parte 3: Explicar a Dos Públicos Objetivo** | Escribir dos explicaciones de la solución:<br>1. Técnica para el Data Scientist del Squad.<br>2. De negocio para el Comité de Tesorería / Finanzas (CFO). | • **Técnico:** [`TECHNICAL_MEMO_DATA_SCIENCE.md`](TECHNICAL_MEMO_DATA_SCIENCE.md)<br>• **Tesorería:** [`presentacion_ejecutiva_tesoreria.pptx`](presentacion_ejecutiva_tesoreria.pptx) | • **Para Data Science:** Documento técnico formal de 300+ líneas con rigor matemático, supuestos de estacionariedad, formulación de pérdidas, análisis de riesgo de cola y protocolo MLOps.<br>• **Para Tesorería:** Presentación ejecutiva en PowerPoint (11 slides widescreen 16:9), sin fórmulas complejas, con analogías intuitivas, tabla financiera maestra de 3 modelos y cero notas al orador (lista para lectura ejecutiva). |
| **Parte 4: Formas de Trabajo con IA (Ways of Working)** | Transparentar dónde sí se usaron herramientas de IA (agentes, copilotos) y dónde deliberadamente NO se utilizaron. | • [`TECHNICAL_MEMO_DATA_SCIENCE.md`](TECHNICAL_MEMO_DATA_SCIENCE.md) (Sec. 7)<br>• [`presentacion_ejecutiva_tesoreria.pptx`](presentacion_ejecutiva_tesoreria.pptx) (Slide 10)<br>• [`solution_notebook.ipynb`](solution_notebook.ipynb) (Sec. 7) | • **Dónde SÍ IA (~60% ahorro en tiempo):** Scaffolding de tests en `pytest`, regex complejas de fechas, linters estáticos (PEP-8) y benchmarking de modelos $(s, S)$.<br>• **Dónde NO IA (Criterio Humano Irreemplazable):** Diagnóstico contable (la IA sugería imputar o descartar el 10x), causalidad temporal $T+L$, analogía tanque vs. caudal y diseño de los 4 Circuit Breakers. |
| **Parte 5: Blueprint de Puesta en Producción** | Describir arquitectura de producción: pipeline de datos, orquestación, monitoreo y salvaguardas (circuit breakers). | • [`TECHNICAL_MEMO_DATA_SCIENCE.md`](TECHNICAL_MEMO_DATA_SCIENCE.md) (Sec. 6)<br>• [`presentacion_ejecutiva_tesoreria.pptx`](presentacion_ejecutiva_tesoreria.pptx) (Slide 09)<br>• [`solution_notebook.ipynb`](solution_notebook.ipynb) (Sec. 8) | • **Pipeline:** Extracción Snowflake $ightarrow$ Calidad `dbt` $ightarrow$ Endpoint Vertex AI.<br>• **Orquestación:** DAG diario en Apache Airflow a las 06:00 UTC (antes de apertura de rieles ACH 07:00 COT y SPEI 06:00 CDMX).<br>• **Monitoreo MLOps:** Tests de Kolmogorov-Smirnov y Population Stability Index (PSI < 0.10) para deriva de datos.<br>• **Salvaguardas:** 4 Circuit Breakers automáticos en código (Integridad Contable, Solvencia del Donante, Techo Diario de 15% y Aislamiento Cambiario). |

---

## 3. Estructura del Repositorio

El repositorio ha sido curado para contener estrictamente los archivos esenciales requeridos para la evaluación técnica y financiera:

```
.
├── README.md                                  # Guía Maestra de Navegación y Mapeo contra la Prueba
├── TECHNICAL_MEMO_DATA_SCIENCE.md             # Documento Técnico Formal (Partes 1 a 5 para DS y C-Level)
├── presentacion_ejecutiva_tesoreria.pptx      # Presentación Ejecutiva a Tesorería (11 slides, sin fórmulas)
├── solution_notebook.ipynb                    # Notebook Jupyter Ejecutable de Solución Completa
│
├── accounts.csv                               # Catálogo maestro de cuentas y umbrales (Original Cobre)
├── account_balances_daily_RAW.csv             # Datos crudos de saldos diarios (Original Cobre)
├── transfers_log_RAW.csv                      # Libro crudo de transferencias (Original Cobre)
├── account_balances_daily_CLEAN.csv           # Dataset saneado y reconciliado con residuo contable cero
├── transfers_log_CLEAN.csv                    # Transferencias estandarizadas en formato ISO-8601
│
├── clean_data_pipeline.py                     # Parte 1: Pipeline de saneamiento forense y reconciliación
├── test_data_integrity.py                     # Parte 1: Suite pytest de aserción contable y contratos
├── run_backtest_simulation.py                 # Parte 2 y 3: Simulación OOS de los 3 protocolos
├── generate_treasury_executive_deck.py        # Generador automatizado de la presentación PowerPoint
│
├── flawed_model_squad_draft.ipynb             # Notebook inicial del squad entregado por Cobre
├── requirements.txt                           # Dependencias de Python reproducibles
├── Candidate Test - Technical Lead DS (Liquidity) EN.pdf # Enunciado oficial de la prueba técnica
│
└── presentation_assets/                       # Gráficos vectoriales de alta resolución (300 DPI)
    ├── chart_forensic_audit.png               # Auditoría forense y reconciliación contable
    ├── chart_flow_seasonality.png             # Estacionalidad semanal y picos de nómina
    ├── chart_feature_importance.png           # Explicabilidad económica de variables Ridge
    ├── chart_backtest_trajectories.png        # Trayectorias de saldo fuera de muestra (70 días)
    ├── chart_kpi_comparison.png               # Comparativa visual de métricas de gestión
    └── chart_production_pipeline.png          # Arquitectura productiva y 4 circuit breakers
```

---

## 4. Guía de Ejecución Rápida y Reproducibilidad (Quickstart)

Todo el proyecto está diseñado para ejecutarse y verificarse en menos de un minuto:

### Paso 1: Clonar el repositorio e instalar dependencias
```bash
git clone <URL_DEL_REPOSITORIO>
cd pruebatcnicacobretechnicalleaddatascience
pip install -r requirements.txt
```

### Paso 2: Ejecutar el pipeline de curaduría forense de datos (Parte 1)
```bash
python clean_data_pipeline.py
```
*Salida esperada:* 100% de fechas recuperadas (293 días), deduplicación a 270 días continuos para las 6 cuentas, corrección del error 10x y residuo contable promedio de `0.00`.

### Paso 3: Validar la suite de pruebas unitarias y contratos de datos (`pytest`)
```bash
pytest test_data_integrity.py
```
*Salida esperada:* `6 passed in ~0.7s` (continuidad temporal, completitud sin nulos, no negatividad, consistencia de catálogo y cuadre contable).

### Paso 4: Ejecutar la simulación de backtesting fuera de muestra (Partes 2 y 3)
```bash
python run_backtest_simulation.py
```
*Salida esperada:*
* Inacción: 109 días en déficit | 0 transferencias | $0 fees.
* Squad: 2 días en déficit | 97 transferencias | Descontrol operativo.
* Propuesto: **0 días en déficit (100% SLA) | 3 transferencias | $50 USD + $20 MXN**.

### Paso 5: Regenerar la Presentación Ejecutiva en PowerPoint
```bash
python generate_treasury_executive_deck.py
```
*Salida esperada:* Generación automática de `presentacion_ejecutiva_tesoreria.pptx` (11 diapositivas alineadas al memo, sin fórmulas complejas, sin Streamlit y con cero notas al orador).

---

## 5. Scorecard Financiero Comparativo (Tabla Maestra de la Diapositiva 07)

A continuación se presenta la tabla financiera que sintetiza los resultados de los tres modelos evaluados sobre los mismos 70 días de prueba fuera de muestra:

| Dimensión Financiera y Operativa | 1. Inacción (Sin Fondeo) | 2. Squad Anterior (Heurística) | 3. Modelo Propuesto (Lead DS) | Impacto Financiero y Conclusión Técnica |
| :--- | :---: | :---: | :---: | :--- |
| **Días en Déficit (Quiebres)** | 109 días acumulados | 2 días en test (19 hist.) | **0 días (100.0% SLA)** | **Cero quiebres operativos.** Se eliminó el riesgo de bloqueo en dispersión de nóminas corporativas. |
| **Transferencias Bancarias** | 0 órdenes | 97 órdenes (1.4 / día) | **3 órdenes (-96.9%)** | **Reducción del 96.9% en fricción bancaria:** de 1.4 órdenes diarias a solo un fondeo cada 23 días. |
| **Costo Total en Fees Bancarios** | $0.00 | Descontrol de comisiones | **$50 USD + $20 MXN** | Solo 2 órdenes internacionales SWIFT ($25 c/u) y 1 orden local SPEI ($20 MXN). |
| **Saldo Mín. Matriz (COP)** | $1,942.0M COP | Canibalizó ($1,695M COP) | **$1,942.0M COP (+94.2%)** | La cuenta nodriza jamás bajó de su piso ($1,000M). Margen de seguridad intacto (+94.2%). |
| **Saldo Mín. en USD (Chase)** | $56.0k USD (Quiebre) | $99.4k USD (Quiebre) | **$104.7k USD (+4.7%)** | Cumplimiento estricto del umbral ($100k USD) durante todo el trimestre evaluado. |
| **Saldo Mín. en MXN (BBVA)** | $15.4M MXN (Quiebre) | $39.98M MXN (Quiebre) | **$52.8M MXN (+32.0%)** | El colchón amortiguó 5 ciclos de nómina sin romper el umbral contractual ($40M MXN). |
| **Preservación del Float (COP)** | $124.5M COP float | $111.5M COP float | **$124.5M COP (+12.97M COP)** | Superó al squad en +$12.97M COP en saldo promedio remunerado en la cuenta matriz en Colombia. |
| **Descapitalización de Caja** | No aplica | Crítica (vació Bancolombia) | **0 eventos (Piso intacto)** | Protección patrimonial absoluta mediante la regla dura de solvencia del donante. |

---

## 6. Arquitectura Productiva y Gobernanza de Riesgos (Parte 5)

El diseño para producción trasciende el prototipo estático y contempla:
1. **Contratos de Datos (`dbt tests`):** Aserción determinística de balance $|B_t - (B_{t-1} + I_t - O_t)| < 0.01$ y filtros estadísticos 5-sigma para aislar anomalías de escala o signo antes de alimentar la inferencia.
2. **Orquestación en Airflow:** Ejecución diaria a las 06:00 UTC (01:00 AM COT / 00:00 AM CDMX), finalizando antes de la apertura de las cámaras de compensación (ACH 07:00 COT, SPEI 06:00 CDMX).
3. **Observabilidad y Detección de Drift (MLOps):** Monitoreo diario del Population Stability Index ($	ext{PSI} < 0.10$) y test de Kolmogorov-Smirnov. Si $	ext{PSI} > 0.25$, el sistema conmuta automáticamente a modo defensivo.
4. **4 Circuit Breakers Automáticos en Código:**
   * *CB-1 (Integridad Contable):* Aborta si hay descalce de balance.
   * *CB-2 (Solvencia Inviolable):* Bloquea la transferencia si la matriz (`ACC-001`) cae bajo $1,000M COP.
   * *CB-3 (Techo de Exposición Diario):* Límite de movilización máxima del 15% del activo consolidado por jornada.
   * *CB-4 (Aislamiento Cambiario):* Prohibición en código de fondeos cross-currency sin cobertura FX.
5. **Esquema Champion-Challenger:** El modelo Ridge regularizado L2 opera como titular; modelos alternativos (ej. LightGBM con restricciones monótonas o ARIMAX) corren en sombra (*shadow deployment*) durante 60 días antes de considerar cualquier reemplazo.

---

## 7. Formas de Trabajo con Inteligencia Artificial (Parte 4)

* **Dónde SÍ se apalancó IA (~60% de ahorro de tiempo):**
  * Generación acelerada de la suite de pruebas unitarias en `pytest` (`test_data_integrity.py`).
  * Construcción de expresiones regulares complejas para normalización multiformato de fechas (`DD/MM/YYYY`, `YYYY-MM-DD`, `MM-DD-YYYY`).
  * Scaffolding de código modular, tipado estricto y linters de análisis estático (PEP-8).
  * Benchmarking ágil de literatura especializada en optimización estocástica de inventarios aplicada a tesorería (modelos $(s, S)$ de Arrow-Harris-Marschak).
* **Dónde deliberadamente NO se utilizó IA (Juicio Humano Irreemplazable):**
  * *Diagnóstico Forense Contable:* Las herramientas de LLM sugerían "imputar con la media" o "suavizar con splines", lo que habría ocultado el error decimal 10x y las 4 inversiones de signo. Solo el criterio analítico humano auditó el libro contable y rescató el 100% de la historia.
  * *Causalidad Temporal y Latencia Bancaria ($T+L$):* Diseñar el orden temporal estricto sin filtración de futuro (*zero lookahead bias*) respetando los plazos de acreditación interbancarios.
  * *Física de Tanque vs. Caudal:* Identificar que los saldos acumulan error y que el modelo predictivo debía descansar sobre flujos netos diarios estacionarios $I(0)$.
  * *Arquitectura en Dos Capas:* Desacoplar la decisión de cuándo actuar (lead time) del tamaño de la recarga (amortiguador quincenal).
  * *Gobernanza de Solvencia:* Conceptualización del piso de seguridad de la cuenta nodriza y los 4 Circuit Breakers institucionales.

---

## 8. Conclusiones del Technical Lead

1. **Rigor Estadístico y Contable:** La transición desde el modelado ingenuo de saldo hacia la predicción de flujos netos estacionarios regularizados con Ridge L2 proporciona una base matemática sólida, auditable y libre de derivas acumulativas.
2. **Eficiencia Cuantificada:** La arquitectura de dos capas demostró en 70 días de backtesting fuera de muestra un desempeño impecable: **0 quiebres de liquidez (100% de SLA)** reduciendo en un **96.9% las transferencias bancarias** (de 97 a solo 3 órdenes) y preservando la rentabilidad de las reservas en COP.
3. **Preparación para Producción:** El diseño integra contratos de datos rigurosos en dbt, observabilidad continua de drift con métricas KS y PSI, seguimiento continuo de precisión MAE, 4 circuit breakers automatizados y un esquema Champion-Challenger que posiciona a Cobre a la vanguardia de la tesorería algorítmica institucional en América Latina.

---
*Para cualquier consulta técnica o financiera sobre la solución, contactar a Nicolás Méndez Gutiérrez.*
