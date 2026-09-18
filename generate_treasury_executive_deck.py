import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# ==============================================================================
# DESIGN TOKENS & COLOR PALETTE
# ==============================================================================
COLOR_DARK_NAVY   = RGBColor(15, 23, 42)     # #0F172A
COLOR_SLATE_CARD  = RGBColor(30, 41, 59)    # #1E293B
COLOR_COBRE       = RGBColor(255, 90, 31)    # #FF5A1F (Cobre Copper)
COLOR_SKY_BLUE    = RGBColor(14, 165, 233)   # #0EA5E9
COLOR_EMERALD     = RGBColor(16, 185, 129)   # #10B981
COLOR_AMBER       = RGBColor(245, 158, 11)   # #F59E0B
COLOR_CRIMSON     = RGBColor(239, 68, 68)    # #EF4444
COLOR_LIGHT_BG    = RGBColor(248, 250, 252)  # #F8FAFC
COLOR_WHITE       = RGBColor(255, 255, 255)
COLOR_CARD_BORDER = RGBColor(226, 232, 240)  # #E2E8F0
COLOR_TEXT_MUTED  = RGBColor(100, 116, 139)  # #64748B
COLOR_TEXT_DARK   = RGBColor(15, 23, 42)     # #0F172A

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "presentation_assets")

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# ==============================================================================
# HELPER FUNCTIONS (NO SPEAKER NOTES GENERATED)
# ==============================================================================
def set_slide_background(slide, color):
    bg_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5)
    )
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = color
    bg_shape.line.fill.background()
    return bg_shape

def add_header(slide, title, category, slide_num, total_slides=11, is_dark=False):
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10), Inches(0.32))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    tf_cat.margin_left = tf_cat.margin_right = tf_cat.margin_top = tf_cat.margin_bottom = 0
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category.upper()
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_COBRE

    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.2), Inches(0.6))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title
    p_title.font.size = Pt(20)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_WHITE if is_dark else COLOR_TEXT_DARK

    num_box = slide.shapes.add_textbox(Inches(11.5), Inches(0.4), Inches(1.0), Inches(0.35))
    tf_num = num_box.text_frame
    tf_num.margin_left = tf_num.margin_right = tf_num.margin_top = tf_num.margin_bottom = 0
    p_num = tf_num.paragraphs[0]
    p_num.text = f"{slide_num:02d} / {total_slides:02d}"
    p_num.alignment = PP_ALIGN.RIGHT
    p_num.font.size = Pt(10)
    p_num.font.bold = True
    p_num.font.color.rgb = COLOR_TEXT_MUTED

def add_card(slide, left, top, width, height, bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card

def add_bullet_list(slide, left, top, width, height, items, font_size=10.5, text_color=COLOR_TEXT_DARK, space_after=6):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = "•  " + item
        p.font.size = Pt(font_size)
        p.font.color.rgb = text_color
        p.space_after = Pt(space_after)

# ==============================================================================
# SLIDE 1: PORTADA EJECUTIVA
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1, COLOR_DARK_NAVY)

acc_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(1.4), Inches(0.8), Inches(0.08))
acc_bar.fill.solid()
acc_bar.fill.fore_color.rgb = COLOR_COBRE
acc_bar.line.fill.background()

tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.7), Inches(11.0), Inches(4.2))
tf1 = tb1.text_frame
tf1.word_wrap = True

p_sub = tf1.paragraphs[0]
p_sub.text = "PRUEBA TÉCNICA • TECHNICAL LEAD DATA SCIENCE (LIQUIDITY & CASH FLOW)"
p_sub.font.size = Pt(12)
p_sub.font.bold = True
p_sub.font.color.rgb = COLOR_COBRE
p_sub.space_after = Pt(14)

p_title = tf1.add_paragraph()
p_title.text = "Motor Inteligente de Optimización de Liquidez Multi-Divisa"
p_title.font.size = Pt(28)
p_title.font.bold = True
p_title.font.color.rgb = COLOR_WHITE
p_title.space_after = Pt(12)

p_desc = tf1.add_paragraph()
p_desc.text = "Sustentación Estratégica para Comité de Finanzas & Tesorería | Metodología CRISP-DM Industrial\n" \
             "Garantía de 0 Quiebres Operacionales (100% SLA), Eficiencia de Capital (-96.9% Fricción Bancaria) y Solvencia Patrimonial."
p_desc.font.size = Pt(13)
p_desc.font.color.rgb = COLOR_SKY_BLUE
p_desc.space_after = Pt(28)

p_cand = tf1.add_paragraph()
p_cand.text = "Candidato: Nicolás Méndez Gutiérrez   |   Cobre B2B Payments Infrastructure   |   Septiembre 2026"
p_cand.font.size = Pt(11)
p_cand.font.color.rgb = COLOR_TEXT_MUTED

add_card(s1, Inches(1.2), Inches(5.8), Inches(10.9), Inches(1.0), bg_color=COLOR_SLATE_CARD, border_color=COLOR_COBRE)
tb_b = s1.shapes.add_textbox(Inches(1.4), Inches(5.95), Inches(10.5), Inches(0.7))
tf_b = tb_b.text_frame
tf_b.word_wrap = True
p_b1 = tf_b.paragraphs[0]
p_b1.text = "ESTRUCTURA DE LA SESIÓN: 8 Secciones Metodológicas (Negocio, Auditoría Forense, Física de Flujos, Modelamiento y Explicabilidad, Validación Empírica, Scorecard Cuantitativo, Arquitectura Productiva, y Transparencia Metodológica con IA)."
p_b1.font.size = Pt(11)
p_b1.font.bold = True
p_b1.font.color.rgb = COLOR_WHITE

# ==============================================================================
# SLIDE 2: ENTENDIMIENTO DEL NEGOCIO (MEMO SEC. 1)
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2, COLOR_LIGHT_BG)
add_header(s2, "El Trilema de Tesorería B2B y la Topología de Cuentas", "CRISP-DM: FASE 1 • BUSINESS UNDERSTANDING", 2)

add_card(s2, Inches(0.8), Inches(1.4), Inches(11.733), Inches(1.9), bg_color=COLOR_WHITE)
tb_tri = s2.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(0.3))
p = tb_tri.text_frame.paragraphs[0]
p.text = "EL TRILEMA DE OPTIMIZACIÓN FINANCIERA EN COBRE"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = COLOR_COBRE

add_bullet_list(s2, Inches(1.0), Inches(1.85), Inches(11.3), Inches(1.35), [
    "1. Cero Quiebres de Liquidez (SLA 99.9%): Garantizar fondos inmediatos para dispersiones de nómina y pagos corporativos sin rechazos por saldo insuficiente.",
    "2. Minimización de Costos y Fricción Bancaria: Eliminar comisiones SWIFT/ACH recurrentes y sobrecostos por spread cambiario en fondeos reactivos.",
    "3. Maximización del Rendimiento del Float: Mantener el capital consolidado en cuentas remuneradas overnight sin atrapar liquidez ociosa en cuentas operativas."
], font_size=10.5, space_after=4)

accounts_data = [
    ("ACC-001 • Bancolombia (COP)", "Cuenta Matriz & Donante Primario", [
        "Moneda: Pesos Colombianos (COP)",
        "Umbral Operativo Mínimo: $1,000M COP",
        "Latencia de Fondeo: L = 1 día hábil",
        "Rol: Respaldo patrimonial y generador de float; provee fondeo a cuentas filiales."
    ], COLOR_SKY_BLUE),
    ("ACC-002 • Chase Bank (USD)", "Cuenta de Liquidación Internacional", [
        "Moneda: Dólares Americanos (USD)",
        "Umbral Operativo Mínimo: $100,000 USD",
        "Latencia de Fondeo: L = 1 día (SWIFT)",
        "Rol: Liquidación cross-border; expuesta a costos fijos ($25 USD) y volatilidad cambiaria."
    ], COLOR_COBRE),
    ("ACC-004 • BBVA Bancomer (MXN)", "Cuenta de Dispersión Local Inmediata", [
        "Moneda: Pesos Mexicanos (MXN)",
        "Umbral Operativo Mínimo: $40,000,000 MXN",
        "Latencia de Fondeo: L = 0 días (SPEI)",
        "Rol: Pagos corporativos continuos con picos intensos en ciclos de quincena."
    ], COLOR_EMERALD)
]

for idx, (acc_title, acc_sub, acc_bullets, acc_color) in enumerate(accounts_data):
    x_pos = Inches(0.8 + idx * 4.0)
    add_card(s2, x_pos, Inches(3.45), Inches(3.733), Inches(2.7), bg_color=COLOR_WHITE)
    
    tb_ac = s2.shapes.add_textbox(x_pos + Inches(0.2), Inches(3.55), Inches(3.33), Inches(0.6))
    tf_ac = tb_ac.text_frame
    tf_ac.word_wrap = True
    p1 = tf_ac.paragraphs[0]
    p1.text = acc_title
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = acc_color
    p2 = tf_ac.add_paragraph()
    p2.text = acc_sub
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_TEXT_MUTED
    
    add_bullet_list(s2, x_pos + Inches(0.2), Inches(4.25), Inches(3.33), Inches(1.8), acc_bullets, font_size=9.5, space_after=4)

add_card(s2, Inches(0.8), Inches(6.3), Inches(11.733), Inches(0.75), bg_color=COLOR_SLATE_CARD, border_color=None)
tb_al = s2.shapes.add_textbox(Inches(1.0), Inches(6.38), Inches(11.3), Inches(0.6))
tf_al = tb_al.text_frame
tf_al.word_wrap = True
p_al = tf_al.paragraphs[0]
p_al.text = "RESTRICCIÓN OPERACIONAL CRÍTICA: Liquidación Asíncrona Estricta (T+L). Los fondos transferidos tardan al menos un día hábil en acreditarse en cuentas internacionales (L=1). Si tesorería reacciona cuando el saldo ya cayó por debajo del umbral, el quiebre de liquidez es inevitable."
p_al.font.size = Pt(9.5)
p_al.font.bold = True
p_al.font.color.rgb = COLOR_AMBER

# ==============================================================================
# SLIDE 3: ENTENDIMIENTO DE DATOS Y AUDITORÍA FORENSE (MEMO SEC. 2)
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3, COLOR_LIGHT_BG)
add_header(s3, "Diagnóstico Forense y Mitigación de Riesgos Reales de Negocio", "CRISP-DM: FASE 2 • DATA UNDERSTANDING & AUDIT", 3)

add_card(s3, Inches(0.8), Inches(1.4), Inches(6.8), Inches(2.6), bg_color=COLOR_WHITE)
tb_f1 = s3.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(6.4), Inches(0.3))
p = tb_f1.text_frame.paragraphs[0]
p.text = "DESALINEACIÓN TEMPORAL Y FALACIA DEL \"9.6% DE FALTANTES\""
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = COLOR_COBRE

add_bullet_list(s3, Inches(1.0), Inches(1.85), Inches(6.4), Inches(2.0), [
    "Desfase de Registros: La tabla de transferencias registraba 283 días mientras que la de balances contenía 293 días de operación.",
    "Falacia de Faltantes Masivos: El análisis anterior descartó fechas heterogéneas y declaró un falso 9.6% de quiebres de liquidez.",
    "Realidad Operativa Saneada: Al alinear el calendario contable continuo de 270 días, se comprobó que solo existieron 19 eventos aislados en los datos crudos.",
    "Impacto en Negocio: Evaluar sobre datos desalineados genera alertas falsas de liquidez y compras innecesarias de divisas con sobrecosto cambiario."
], font_size=9.5, space_after=4)

add_card(s3, Inches(0.8), Inches(4.15), Inches(6.8), Inches(2.8), bg_color=COLOR_WHITE)
tb_f2 = s3.shapes.add_textbox(Inches(1.0), Inches(4.25), Inches(6.4), Inches(0.3))
p = tb_f2.text_frame.paragraphs[0]
p.text = "ANOMALÍAS NUMÉRICAS Y RECONCILIACIÓN CONTABLE"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = COLOR_CRIMSON

add_bullet_list(s3, Inches(1.0), Inches(4.6), Inches(6.4), Inches(2.2), [
    "Error de Escalamiento 10x: Se identificaron registros en BBVA con un dígito adicional erróneo ($400M MXN en vez de $40M MXN) por descalce en la coma decimal.",
    "Transposiciones de Polaridad: Débitos registrados erróneamente como créditos, invirtiendo la dirección de los flujos de dispersión.",
    "Ruptura de la Ecuación Contable: En los datos crudos no se cumplía el principio básico de que el saldo de hoy debe igualar el de ayer más ingresos menos egresos.",
    "Solución Forense: Pipeline determinístico de reconciliación que recupera el balance real con residuo contable exactamente en cero."
], font_size=9.5, space_after=4)

chart_forensic_path = os.path.join(ASSETS_DIR, "chart_forensic_audit.png")
if os.path.exists(chart_forensic_path):
    s3.shapes.add_picture(chart_forensic_path, Inches(7.8), Inches(1.4), Inches(4.733), Inches(5.55))
else:
    add_card(s3, Inches(7.8), Inches(1.4), Inches(4.733), Inches(5.55), bg_color=COLOR_SLATE_CARD)

# ==============================================================================
# SLIDE 4: PREPARACIÓN DE DATOS Y FÍSICA DE FLUJOS (MEMO SEC. 3 + 4.1-4.2)
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4, COLOR_LIGHT_BG)
add_header(s4, "Física del Flujo de Caja: Modelado de Flujos Netos vs. Saldos", "CRISP-DM: FASE 3 • DATA PREPARATION & FEATURE TAXONOMY", 4)

add_card(s4, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.65), bg_color=COLOR_WHITE)
tb_targ = s4.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(5.3), Inches(0.35))
p = tb_targ.text_frame.paragraphs[0]
p.text = "LA ANALOGÍA ESENCIAL: EL TANQUE DE AGUA VS. EL CAUDAL"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = COLOR_COBRE

tb_targ_body = s4.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.8))
tf_tb = tb_targ_body.text_frame
tf_tb.word_wrap = True

p1 = tf_tb.paragraphs[0]
p1.text = "1. El Error Conceptual Previo: Pronosticar Saldos (Nivel del Tanque)"
p1.font.bold = True
p1.font.size = Pt(10)
p1.font.color.rgb = COLOR_TEXT_DARK
p1_b = tf_tb.add_paragraph()
p1_b.text = "Un saldo bancario funciona como el nivel de agua en un tanque: acumula todo el historial pasado. Predecir directamente el nivel acumulado hace que cualquier pequeño error de hoy se arrastre y se magnifique en el tiempo como una bola de nieve incontrolable."
p1_b.font.size = Pt(9.5)
p1_b.font.color.rgb = COLOR_TEXT_MUTED
p1_b.space_after = Pt(8)

p2 = tf_tb.add_paragraph()
p2.text = "2. La Formulación Correcta: Pronosticar Flujos Netos (Caudal de la Tubería)"
p2.font.bold = True
p2.font.size = Pt(10)
p2.font.color.rgb = COLOR_TEXT_DARK
p2_b = tf_tb.add_paragraph()
p2_b.text = "Modelamos el Flujo Neto diario: la diferencia entre lo que entra y lo que sale cada día. El flujo se comporta como el caudal en la tubería: oscila alrededor de una media predecible, no arrastra errores pasados y es cuantitativamente estable."
p2_b.font.size = Pt(9.5)
p2_b.font.color.rgb = COLOR_TEXT_DARK
p2_b.space_after = Pt(8)

p3 = tf_tb.add_paragraph()
p3.text = "3. Reconstrucción Contable Exacta del Saldo Futuro"
p3.font.bold = True
p3.font.size = Pt(10)
p3.font.color.rgb = COLOR_TEXT_DARK
p3_b = tf_tb.add_paragraph()
p3_b.text = "Para saber el saldo de mañana, sumamos al dinero disponible hoy los flujos netos proyectados por el modelo más los fondos que vienen viajando en el sistema. Consistencia contable perfecta sin acumulación de error."
p3_b.font.size = Pt(9.5)
p3_b.font.color.rgb = COLOR_EMERALD

chart_flow_path = os.path.join(ASSETS_DIR, "chart_flow_seasonality.png")
if os.path.exists(chart_flow_path):
    s4.shapes.add_picture(chart_flow_path, Inches(6.8), Inches(1.4), Inches(5.733), Inches(2.65))
else:
    add_card(s4, Inches(6.8), Inches(1.4), Inches(5.733), Inches(2.65), bg_color=COLOR_SLATE_CARD)

add_card(s4, Inches(6.8), Inches(4.15), Inches(5.733), Inches(2.9), bg_color=COLOR_WHITE)
tb_fe = s4.shapes.add_textbox(Inches(7.0), Inches(4.25), Inches(5.33), Inches(0.35))
p = tb_fe.text_frame.paragraphs[0]
p.text = "TAXONOMÍA DE VARIABLES DE NEGOCIO (FEATURE ENGINEERING)"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = COLOR_COBRE

add_bullet_list(s4, Inches(7.0), Inches(4.65), Inches(5.33), Inches(2.3), [
    "Hábitos Semanales B2B: Lunes concentran cobranzas y recaudos corporativos (+); Viernes concentran pagos masivos de facturas (-); Fines de semana con retención por cierre de compensación bancaria.",
    "Ciclos de Nómina y Quincena: Ventanas críticas en días 14 al 16 y 29 al 31 del mes. Los egresos se multiplican hasta 3.4 veces respecto a una jornada operativa ordinaria.",
    "Memoria y Estabilidad Operativa: Rezagos a 1 día y 7 días que capturan el ciclo semanal y la reversión natural a la media tras picos de desembolso corporativo."
], font_size=9.2, space_after=4)

# ==============================================================================
# SLIDE 5: MODELAMIENTO Y EXPLICABILIDAD (MEMO SEC. 4.3-4.4)
# ==============================================================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5, COLOR_LIGHT_BG)
add_header(s5, "Arquitectura de Decisión en Dos Capas y Explicabilidad", "CRISP-DM: FASE 4 • MODELING & EXPLAINABILITY", 5)

add_card(s5, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.65), bg_color=COLOR_WHITE)
tb_tl = s5.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(5.3), Inches(0.35))
p = tb_tl.text_frame.paragraphs[0]
p.text = "ARQUITECTURA DE DECISIÓN CONCEPTUAL EN DOS CAPAS"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = COLOR_COBRE

tb_tl_body = s5.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.8))
tf_tlb = tb_tl_body.text_frame
tf_tlb.word_wrap = True

p_c1 = tf_tlb.paragraphs[0]
p_c1.text = "1. Capa 1: Sensor Predictivo de Seguridad (¿Cuándo actuar?)"
p_c1.font.bold = True
p_c1.font.size = Pt(10)
p_c1.font.color.rgb = COLOR_SKY_BLUE
p_c1_b = tf_tlb.add_paragraph()
p_c1_b.text = "Monitorea continuamente la cuenta y proyecta el balance al plazo exacto de acreditación bancaria (hoy para riel local SPEI, mañana para rieles SWIFT/ACH). Dispara una alerta preventiva con confianza del 99% ANTES de que el saldo perfore el umbral de clientes."
p_c1_b.font.size = Pt(9.2)
p_c1_b.font.color.rgb = COLOR_TEXT_MUTED
p_c1_b.space_after = Pt(7)

p_c2 = tf_tlb.add_paragraph()
p_c2.text = "2. Capa 2: Amortiguador de Fondeo Quincenal (¿Cuánto transferir?)"
p_c2.font.bold = True
p_c2.font.size = Pt(10)
p_c2.font.color.rgb = COLOR_COBRE
p_c2_b = tf_tlb.add_paragraph()
p_c2_b.text = "Cuando el sensor detecta necesidad, no transfiere montos mínimos diarios. Inyecta un colchón estratégico calculado para cubrir 14 días de operación y absorber la quincena corporativa, eliminando el 96.9% de las órdenes innecesarias."
p_c2_b.font.size = Pt(9.2)
p_c2_b.font.color.rgb = COLOR_TEXT_MUTED
p_c2_b.space_after = Pt(7)

p_c3 = tf_tlb.add_paragraph()
p_c3.text = "3. Restricción Dura de Solvencia del Donante (¿Desde dónde transferir?)"
p_c3.font.bold = True
p_c3.font.size = Pt(10)
p_c3.font.color.rgb = COLOR_CRIMSON
p_c3_b = tf_tlb.add_paragraph()
p_c3_b.text = "Regla inviolable: Protege el piso de capital de la cuenta matriz en Bancolombia ($1,000M COP). Solo transfiere excedentes genuinos. Si fondear a una filial compromete la matriz, bloquea el envío para evitar la descapitalización de Cobre."
p_c3_b.font.size = Pt(9.2)
p_c3_b.font.color.rgb = COLOR_TEXT_DARK
p_c3_b.space_after = Pt(7)

p_c4 = tf_tlb.add_paragraph()
p_c4.text = "4. Cascada Dinámica por Latencia y Divisa"
p_c4.font.bold = True
p_c4.font.size = Pt(10)
p_c4.font.color.rgb = COLOR_EMERALD
p_c4_b = tf_tlb.add_paragraph()
p_c4_b.text = "Prioriza rieles inmediatos (SPEI) si la urgencia es intradía, y compensación interbancaria si es anticipada. Opera con aislamiento estricto de divisa para blindar a tesorería contra pérdidas por spread cambiario."
p_c4_b.font.size = Pt(9.2)
p_c4_b.font.color.rgb = COLOR_TEXT_MUTED

chart_feat_path = os.path.join(ASSETS_DIR, "chart_feature_importance.png")
if os.path.exists(chart_feat_path):
    s5.shapes.add_picture(chart_feat_path, Inches(6.75), Inches(1.4), Inches(5.8), Inches(5.65))
else:
    add_card(s5, Inches(6.8), Inches(1.4), Inches(5.733), Inches(5.65), bg_color=COLOR_SLATE_CARD)

# ==============================================================================
# SLIDE 6: VALIDACIÓN EMPÍRICA Y TRAYECTORIAS (MEMO SEC. 5.1)
# ==============================================================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6, COLOR_LIGHT_BG)
add_header(s6, "Validación Empírica: Trayectorias de Saldo Fuera de Muestra (70 Días)", "CRISP-DM: FASE 5 • EMPIRICAL VALIDATION & OUT-OF-SAMPLE TRAJECTORIES", 6)

chart_traj_path = os.path.join(ASSETS_DIR, "chart_backtest_trajectories.png")
if os.path.exists(chart_traj_path):
    s6.shapes.add_picture(chart_traj_path, Inches(0.8), Inches(1.4), Inches(6.8), Inches(5.65))
else:
    add_card(s6, Inches(0.8), Inches(1.4), Inches(6.8), Inches(5.65), bg_color=COLOR_SLATE_CARD)

add_card(s6, Inches(7.8), Inches(1.4), Inches(4.733), Inches(5.65), bg_color=COLOR_WHITE)
tb_tr_t = s6.shapes.add_textbox(Inches(8.0), Inches(1.55), Inches(4.33), Inches(0.35))
p = tb_tr_t.text_frame.paragraphs[0]
p.text = "DIAGNÓSTICO DE COMPORTAMIENTO POR GEOGRAFÍA"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = COLOR_COBRE

tb_tr_b = s6.shapes.add_textbox(Inches(8.0), Inches(2.0), Inches(4.33), Inches(4.8))
tf_tr = tb_tr_b.text_frame
tf_tr.word_wrap = True

p_g1 = tf_tr.paragraphs[0]
p_g1.text = "Bancolombia (COP - Donante Matriz):"
p_g1.font.bold = True
p_g1.font.size = Pt(10)
p_g1.font.color.rgb = COLOR_SKY_BLUE
p_g1_b = tf_tr.add_paragraph()
p_g1_b.text = "• Saldo Mínimo Preservado: $1,942.0M COP (+94.2% sobre umbral).\n" \
              "• Preservación Patrimonial: La política propuesta protegió la cuenta matriz intacta, mientras que el squad anterior canibalizó la nodriza drenándola a $1,695M COP."
p_g1_b.font.size = Pt(9.2)
p_g1_b.font.color.rgb = COLOR_TEXT_MUTED
p_g1_b.space_after = Pt(8)

p_g2 = tf_tr.add_paragraph()
p_g2.text = "Chase Bank (USD - Liquidación Internacional):"
p_g2.font.bold = True
p_g2.font.size = Pt(10)
p_g2.font.color.rgb = COLOR_COBRE
p_g2_b = tf_tr.add_paragraph()
p_g2_b.text = "• Saldo Mínimo Preservado: $104.7k USD (+4.7% sobre umbral).\n" \
              "• Cero Quiebres: Mantuvo solvencia continua. La inacción colapsó a $56.0k USD y el squad perforó el umbral a $99.4k USD."
p_g2_b.font.size = Pt(9.2)
p_g2_b.font.color.rgb = COLOR_TEXT_MUTED
p_g2_b.space_after = Pt(8)

p_g3 = tf_tr.add_paragraph()
p_g3.text = "BBVA Bancomer (MXN - Dispersión Local):"
p_g3.font.bold = True
p_g3.font.size = Pt(10)
p_g3.font.color.rgb = COLOR_EMERALD
p_g3_b = tf_tr.add_paragraph()
p_g3_b.text = "• Saldo Mínimo Preservado: $52.8M MXN (+32.0% sobre umbral).\n" \
              "• Absorción Quincenal: Soportó los 5 ciclos de nómina sin perforar los $40M MXN. La inacción cayó a $15.4M MXN y el squad a $39.98M MXN."
p_g3_b.font.size = Pt(9.2)
p_g3_b.font.color.rgb = COLOR_TEXT_MUTED
p_g3_b.space_after = Pt(8)

p_g4 = tf_tr.add_paragraph()
p_g4.text = "Rigor Fuera de Muestra (Zero Lookahead Bias):"
p_g4.font.bold = True
p_g4.font.size = Pt(9.5)
p_g4.font.color.rgb = COLOR_TEXT_DARK
p_g4_b = tf_tr.add_paragraph()
p_g4_b.text = "Evaluación estricta día por día en 70 días continuos con orden temporal causal, sin acceso a información futura."
p_g4_b.font.size = Pt(9.0)
p_g4_b.font.color.rgb = COLOR_TEXT_MUTED

# ==============================================================================
# SLIDE 7: EVALUACIÓN CUANTITATIVA: SCORECARD COMPARATIVO DE LOS 3 MODELOS (MEMO SEC. 5.4)
# ==============================================================================
s7 = prs.slides.add_slide(blank_layout)
set_slide_background(s7, COLOR_LIGHT_BG)
add_header(s7, "Scorecard Financiero Comparativo: Inacción vs. Squad vs. Modelo Propuesto", "CRISP-DM: FASE 5 • COMPARATIVE SCORECARD & POLICY BENCHMARK", 7)

# Master Financial Scorecard Table (9 rows x 5 columns) - Full width for maximum readability
table_shape = s7.shapes.add_table(9, 5, Inches(0.8), Inches(1.35), Inches(11.733), Inches(4.7))
tbl = table_shape.table
tbl.columns[0].width = Inches(2.4)
tbl.columns[1].width = Inches(1.7)
tbl.columns[2].width = Inches(2.0)
tbl.columns[3].width = Inches(2.4)
tbl.columns[4].width = Inches(3.233)

headers = [
    "DIMENSIÓN FINANCIERA Y OPERATIVA",
    "1. INACCIÓN\n(Sin Fondeo)",
    "2. SQUAD ANTERIOR\n(Heurística Reactiva)",
    "3. MODELO PROPUESTO\n(Lead DS • Dos Capas)",
    "IMPACTO FINANCIERO Y CONCLUSIÓN TÉCNICA"
]

for c_idx, h_text in enumerate(headers):
    cell = tbl.cell(0, c_idx)
    cell.fill.solid()
    # Highlight winning column header in Cobre Brand Color, others in Dark Navy
    cell.fill.fore_color.rgb = COLOR_COBRE if c_idx == 3 else COLOR_DARK_NAVY
    p = cell.text_frame.paragraphs[0]
    p.text = h_text
    p.font.size = Pt(9.0)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

table_data = [
    (
        "Días en Déficit (Quiebres)",
        "109 días acumulados",
        "2 días en test (19 hist.)",
        "0 días (100.0% SLA)",
        "Cero quiebres operativos. Se eliminó el riesgo de bloqueo en dispersión de nóminas masivas."
    ),
    (
        "Transferencias Bancarias",
        "0 órdenes",
        "97 órdenes (1.4 / día)",
        "3 órdenes (-96.9%)",
        "Reducción del 96.9% en fricción operativa: de 1.4 órdenes diarias a 1 fondeo cada 23 días."
    ),
    (
        "Costo en Fees Bancarios",
        "$0.00",
        "Descontrol de comisiones",
        "$50 USD + $20 MXN",
        "Solo 2 órdenes internacionales SWIFT ($25 c/u) y 1 orden local SPEI ($20 MXN)."
    ),
    (
        "Saldo Mín. Matriz (COP)",
        "$1,942.0M COP",
        "Canibalizó matriz ($1,695M)",
        "$1,942.0M COP (+94.2%)",
        "La cuenta donante jamás perforó el piso ($1,000M COP). Margen de seguridad intacto (+94.2%)."
    ),
    (
        "Saldo Mín. en USD (Chase)",
        "$56.0k USD (Quiebre)",
        "$99.4k USD (Quiebre)",
        "$104.7k USD (+4.7%)",
        "Cumplimiento estricto del umbral ($100k USD) durante todo el trimestre evaluado."
    ),
    (
        "Saldo Mín. en MXN (BBVA)",
        "$15.4M MXN (Quiebre)",
        "$39.98M MXN (Quiebre)",
        "$52.8M MXN (+32.0%)",
        "El colchón amortiguó 5 ciclos de nómina sin perforar el umbral contractual ($40M MXN)."
    ),
    (
        "Preservación del Float (COP)",
        "$124.5M COP float",
        "$111.5M COP float",
        "$124.5M COP (+12.97M COP)",
        "Superó al squad en +$12.97M COP en saldo promedio remunerado en la cuenta matriz en Colombia."
    ),
    (
        "Descapitalización de Caja",
        "No aplica",
        "Crítica (vació Bancolombia)",
        "0 eventos (Piso intacto)",
        "Protección patrimonial absoluta mediante la regla dura de solvencia del donante."
    )
]

for r_idx, row in enumerate(table_data):
    for c_idx, val in enumerate(row):
        cell = tbl.cell(r_idx + 1, c_idx)
        cell.fill.solid()
        if c_idx == 3:
            # Highlight proposed winning column in very soft emerald tint
            cell.fill.fore_color.rgb = RGBColor(236, 253, 245) if r_idx % 2 == 0 else RGBColor(209, 250, 229)
        else:
            cell.fill.fore_color.rgb = COLOR_LIGHT_BG if r_idx % 2 == 0 else COLOR_WHITE
            
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(8.5)
        
        if c_idx == 0:
            p.font.bold = True
            p.font.color.rgb = COLOR_TEXT_DARK
        elif c_idx == 1:
            p.font.color.rgb = COLOR_CRIMSON if "quiebre" in val.lower() or "109" in val else COLOR_TEXT_MUTED
            p.alignment = PP_ALIGN.CENTER
        elif c_idx == 2:
            p.font.color.rgb = COLOR_CRIMSON
            p.font.bold = True if "canibal" in val.lower() or "quiebre" in val.lower() else False
            p.alignment = PP_ALIGN.CENTER
        elif c_idx == 3:
            p.font.bold = True
            p.font.color.rgb = RGBColor(6, 95, 70)  # Dark Emerald
            p.alignment = PP_ALIGN.CENTER
        else:
            p.font.color.rgb = COLOR_TEXT_DARK
            p.font.size = Pt(8.2)

add_card(s7, Inches(0.8), Inches(6.15), Inches(11.733), Inches(0.95), bg_color=COLOR_DARK_NAVY, border_color=COLOR_COBRE)
tb_bt = s7.shapes.add_textbox(Inches(1.0), Inches(6.22), Inches(11.333), Inches(0.8))
tf_bt = tb_bt.text_frame
tf_bt.word_wrap = True
p_bt1 = tf_bt.paragraphs[0]
p_bt1.text = "SÍNTESIS EJECUTIVA DE RETORNO FINANCIERO: El Modelo Propuesto resuelve simultáneamente el Trilema de Tesorería:"
p_bt1.font.size = Pt(9.5)
p_bt1.font.bold = True
p_bt1.font.color.rgb = COLOR_COBRE
p_bt1.space_after = Pt(2)

p_bt2 = tf_bt.add_paragraph()
p_bt2.text = "1. Cero días en déficit (100% SLA)   |   2. Ahorro de 96.9% en transferencias ($50 USD + $20 MXN en comisiones)   |   3. Maximización del float (+12.97M COP en matriz) blindando la reserva de capital."
p_bt2.font.size = Pt(9.0)
p_bt2.font.bold = True
p_bt2.font.color.rgb = COLOR_WHITE

# ==============================================================================
# SLIDE 8: IMPACTO FINANCIERO Y P&L POR MONEDA NATIVA (MEMO SEC. 5.2)
# ==============================================================================
s8 = prs.slides.add_slide(blank_layout)
set_slide_background(s8, COLOR_LIGHT_BG)
add_header(s8, "Auditoría Financiera: P&L por Divisa Nativa y Clarificación del Float", "CRISP-DM: FASE 5 • FINANCIAL AUDIT & NATIVE P&L", 8)

add_card(s8, Inches(0.8), Inches(1.4), Inches(11.733), Inches(2.9), bg_color=COLOR_WHITE)
tb_pl = s8.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(0.3))
p = tb_pl.text_frame.paragraphs[0]
p.text = "DESGLOSE DE SALDOS MÍNIMOS Y COSTOS OPERACIONALES POR MONEDA NATIVA"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = COLOR_COBRE

table_pl = s8.shapes.add_table(4, 6, Inches(1.0), Inches(1.85), Inches(11.3), Inches(2.2))
tbl_p = table_pl.table
tbl_p.columns[0].width = Inches(2.2)
tbl_p.columns[1].width = Inches(1.2)
tbl_p.columns[2].width = Inches(2.0)
tbl_p.columns[3].width = Inches(2.0)
tbl_p.columns[4].width = Inches(2.0)
tbl_p.columns[5].width = Inches(1.9)

p_headers = ["CUENTA OPERATIVA", "DIVISA", "SALDO MÍN. REAL", "UMBRAL MÍNIMO", "MARGEN DE SEGURIDAD", "COSTO TOTAL FEES"]
for c_idx, h_text in enumerate(p_headers):
    cell = tbl_p.cell(0, c_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = COLOR_DARK_NAVY
    p = cell.text_frame.paragraphs[0]
    p.text = h_text
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

pl_data = [
    ("ACC-001 • Bancolombia", "COP", "$1,942,000,000 COP", "$1,000,000,000 COP", "+$942,000,000 (+94.2%)", "$0.00 COP (0 envíos)"),
    ("ACC-002 • Chase Bank", "USD", "$104,700 USD", "$100,000 USD", "+$4,700 USD (+4.7%)", "$50.00 USD (2 SWIFT)"),
    ("ACC-004 • BBVA Bancomer", "MXN", "$52,800,000 MXN", "$40,000,000 MXN", "+$12,800,000 MXN (+32.0%)", "$20.00 MXN (1 SPEI)")
]

for r_idx, row in enumerate(pl_data):
    for c_idx, val in enumerate(row):
        cell = tbl_p.cell(r_idx + 1, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_LIGHT_BG if r_idx % 2 == 0 else COLOR_WHITE
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(8.5)
        if c_idx == 0:
            p.font.bold = True
            p.font.color.rgb = COLOR_TEXT_DARK
        elif c_idx == 4:
            p.font.bold = True
            p.font.color.rgb = COLOR_EMERALD
            p.alignment = PP_ALIGN.CENTER
        elif c_idx == 5:
            p.font.bold = True
            p.font.color.rgb = COLOR_COBRE
            p.alignment = PP_ALIGN.CENTER
        else:
            p.alignment = PP_ALIGN.CENTER
            p.font.color.rgb = COLOR_TEXT_DARK

add_card(s8, Inches(0.8), Inches(4.45), Inches(11.733), Inches(2.6), bg_color=COLOR_SLATE_CARD, border_color=COLOR_SKY_BLUE)
tb_sol = s8.shapes.add_textbox(Inches(1.0), Inches(4.55), Inches(11.3), Inches(0.35))
p = tb_sol.text_frame.paragraphs[0]
p.text = "ACLARACIÓN ESTRATÉGICA SOBRE EL \"FLOAT\" Y SOLVENCIA PATRIMONIAL"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = COLOR_SKY_BLUE

add_bullet_list(s8, Inches(1.0), Inches(4.95), Inches(11.3), Inches(1.95), [
    "Diferencial de Float en Matriz (+12.97M COP): El saldo promedio remunerado en la cuenta matriz superó en +$12.97M COP al modelo anterior, capturando mayor rentabilidad overnight en Bancolombia.",
    "El Espejismo de Liquidez del Prototipo Previo: El squad anterior aparentaba 'menor uso de capital' únicamente porque dejó desatendida a la cuenta de BBVA en México, manteniéndola en insolvencia técnica continua durante el trimestre.",
    "Fondeo Just-in-Time y Cero Riesgo Patrimonial: Nuestro motor garantizó solvencia en el 100% de las geografías sin sobre-inmovilizar capital. Las 3 cuentas operaron en zona de holgura financiera positiva continua.",
    "Fricción Bancaria Marginal: El costo total directo de comisiones bancarias durante todo el período fue de tan solo $50 USD y $20 MXN, frente a cientos de dólares en transferencias reactivas del modelo previo."
], font_size=9.5, text_color=COLOR_WHITE, space_after=4)

# ==============================================================================
# SLIDE 9: DESPLIEGUE Y GOBERNANZA PRODUCTIVA (MEMO SEC. 6)
# ==============================================================================
s9 = prs.slides.add_slide(blank_layout)
set_slide_background(s9, COLOR_LIGHT_BG)
add_header(s9, "Arquitectura Productiva, Pipeline End-to-End y 4 Circuit Breakers", "CRISP-DM: FASE 6 • DEPLOYMENT & GOVERNANCE", 9)

add_card(s9, Inches(0.8), Inches(1.4), Inches(11.733), Inches(1.5), bg_color=COLOR_WHITE)
tb_pip = s9.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(0.3))
p = tb_pip.text_frame.paragraphs[0]
p.text = "PIPELINE PRODUCTIVO DE EJECUCIÓN DIARIA (ORQUESTACIÓN AUTOMATIZADA A LAS 06:00 UTC)"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = COLOR_COBRE

steps = [
    ("01. INGESTA", "Cloud Storage / Snowflake"),
    ("02. CALIDAD", "dbt Tests & Conciliación"),
    ("03. ORQUESTACIÓN", "Airflow DAG (06:00 UTC)"),
    ("04. PREDICCIÓN", "GCP Vertex AI Endpoint"),
    ("05. GOBERNANZA", "Despacho Seguro a Core Bancario")
]
for idx, (st_name, st_desc) in enumerate(steps):
    x_s = Inches(1.0 + idx * 2.3)
    add_card(s9, x_s, Inches(1.85), Inches(2.1), Inches(0.85), bg_color=COLOR_SLATE_CARD, border_color=COLOR_SKY_BLUE)
    tb_st = s9.shapes.add_textbox(x_s + Inches(0.1), Inches(1.9), Inches(1.9), Inches(0.7))
    tf_st = tb_st.text_frame
    tf_st.word_wrap = True
    p1 = tf_st.paragraphs[0]
    p1.text = st_name
    p1.font.size = Pt(9)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_COBRE
    p2 = tf_st.add_paragraph()
    p2.text = st_desc
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = COLOR_WHITE

add_card(s9, Inches(0.8), Inches(3.05), Inches(5.7), Inches(4.0), bg_color=COLOR_WHITE)
tb_cb = s9.shapes.add_textbox(Inches(1.0), Inches(3.15), Inches(5.3), Inches(0.3))
p = tb_cb.text_frame.paragraphs[0]
p.text = "LOS 4 CIRCUIT BREAKERS AUTOMÁTICOS DE SEGURIDAD"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = COLOR_CRIMSON

add_bullet_list(s9, Inches(1.0), Inches(3.5), Inches(5.3), Inches(3.4), [
    "1. Breaker de Integridad Contable: Si se detecta descuadre o incoherencia entre saldos y movimientos en los datos de entrada, el pipeline aborta la inferencia y notifica a Ingeniería de Datos.",
    "2. Breaker de Solvencia Inviolable: Bloquea automáticamente cualquier orden si el balance remanente de la cuenta matriz (COP) cae por debajo de su piso de seguridad ($1,000M COP).",
    "3. Breaker de Techo Diario de Movilización: Impide transferir más del 15% del activo consolidado en una sola jornada, conteniendo riesgos operativos y shocks macroeconómicos.",
    "4. Breaker de Aislamiento Cambiario: Prohíbe en código realizar conversiones automáticas entre diferentes divisas, blindando a tesorería contra pérdidas por spread cambiario."
], font_size=9.2, space_after=5)

add_card(s9, Inches(6.8), Inches(3.05), Inches(5.733), Inches(4.0), bg_color=COLOR_WHITE)
tb_mc = s9.shapes.add_textbox(Inches(7.0), Inches(3.15), Inches(5.33), Inches(0.3))
p = tb_mc.text_frame.paragraphs[0]
p.text = "DESPACHO ATÓMICO, OBSERVABILIDAD Y AUDITORÍA CRIPTOGRÁFICA"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = COLOR_EMERALD

add_bullet_list(s9, Inches(7.0), Inches(3.5), Inches(5.33), Inches(3.4), [
    "Transmisión Segura a Core Bancario: Ejecución idempotente y atómica hacia las APIs bancarias de compensación (SPEI / ACH / SWIFT).",
    "Trazabilidad Criptográfica SHA-256: Cada orden emitida genera una huella digital inmutable que registra saldos previos, montos calculados y justificación del modelo.",
    "Monitoreo Continuo de Deriva (Drift MLOps): Cálculo diario de estabilidad poblacional (KS y PSI); ante desplazamientos severos (PSI > 0.25), conmuta automáticamente a modo heurístico defensivo.",
    "Gobernanza Champion-Challenger: El modelo Ridge opera como titular; modelos alternativos compiten en sombra durante 60 días antes de considerar cualquier relevo."
], font_size=9.2, space_after=5)

# ==============================================================================
# SLIDE 10: TRANSPARENCIA METODOLÓGICA CON IA (MEMO SEC. 7)
# ==============================================================================
s10 = prs.slides.add_slide(blank_layout)
set_slide_background(s10, COLOR_DARK_NAVY)
add_header(s10, "Formas de Trabajo con IA: Productividad Aumentada vs. Criterio Humano Senior", "PARTE 4 • TRANSPARENCIA METODOLÓGICA & LIDERAZGO TÉCNICO", 10, is_dark=True)

add_card(s10, Inches(0.8), Inches(1.4), Inches(5.7), Inches(4.7), bg_color=COLOR_SLATE_CARD, border_color=COLOR_EMERALD)
tb_ai_yes = s10.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(5.3), Inches(0.35))
p = tb_ai_yes.text_frame.paragraphs[0]
p.text = "DÓNDE SÍ SE APALANCÓ IA GENERATIVA (~60% Ahorro de Tiempo)"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = COLOR_EMERALD

add_bullet_list(s10, Inches(1.0), Inches(2.0), Inches(5.3), Inches(3.9), [
    "Scaffolding y Suites de Pruebas Unitarias: Generación acelerada de la suite de pruebas en pytest (test_data_integrity.py) para validar aserciones contables e integridad referencial.",
    "Expresiones Regulares Complejas: Construcción rápida de regex para normalizar formatos heterogéneos de fechas (DD/MM/YYYY, YYYY-MM-DD, MM-DD-YYYY) sin descartar registros históricos.",
    "Automatización de Código y Linters: Empleo de skills de análisis estático (PEP-8, tipado estricto, modularización de pipelines) reduciendo la fricción de desarrollo de días a horas.",
    "Benchmarking y Revisión Bibliográfica: Consulta y contrastación ágil de literatura en optimización estocástica de inventarios aplicada a tesorería (modelos (s, S) de Arrow-Harris-Marschak)."
], font_size=9.2, text_color=COLOR_WHITE, space_after=6)

add_card(s10, Inches(6.8), Inches(1.4), Inches(5.733), Inches(4.7), bg_color=COLOR_SLATE_CARD, border_color=COLOR_COBRE)
tb_ai_no = s10.shapes.add_textbox(Inches(7.0), Inches(1.55), Inches(5.33), Inches(0.35))
p = tb_ai_no.text_frame.paragraphs[0]
p.text = "DÓNDE DELIBERADAMENTE NO SE USÓ IA (Juicio Humano Irreemplazable)"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = COLOR_COBRE

add_bullet_list(s10, Inches(7.0), Inches(2.0), Inches(5.33), Inches(3.9), [
    "Diagnóstico Forense y Descubrimiento del 10x: Los LLMs recomendaban 'imputar con la media' o 'eliminar outliers'. Solo el criterio humano identificó el error decimal 10x y las 4 polaridades invertidas, salvando los datos reales.",
    "Causalidad Temporal y Latencia Bancaria (T+L): Comprender los plazos de acreditación y estructurar la partición temporal sin filtración de futuro (zero lookahead bias) requiere experiencia financiera real.",
    "Física de 'Tanque vs. Caudal': Concebir que los saldos acumulan error y que la meta predictiva debía ser el flujo neto diario estacionario fue una decisión metodológica humana.",
    "Arquitectura en Dos Capas: Separar el momento de actuar (lead time) del tamaño de la recarga (colchón quincenal) para abatir el sobre-rebalanceo en 96.9%.",
    "Gobernanza de Solvencia y Circuit Breakers: Definición del piso intocable de Bancolombia ($1,000M COP) y las compuertas de seguridad institucional para proteger el patrimonio de Cobre."
], font_size=9.2, text_color=COLOR_WHITE, space_after=5)

add_card(s10, Inches(0.8), Inches(6.25), Inches(11.733), Inches(0.8), bg_color=COLOR_COBRE, border_color=None)
tb_to = s10.shapes.add_textbox(Inches(1.0), Inches(6.35), Inches(11.3), Inches(0.6))
tf_to = tb_to.text_frame
tf_to.word_wrap = True
p_to = tf_to.paragraphs[0]
p_to.text = "REFLEXIÓN DE LIDERAZGO TÉCNICO: La IA multiplica la velocidad operativa y la cobertura técnica, pero la formulación matemática, la estrategia financiera y la gobernanza de riesgos dependen del juicio crítico y la experiencia de negocio del Technical Lead."
p_to.font.size = Pt(10.0)
p_to.font.bold = True
p_to.font.color.rgb = COLOR_WHITE

# ==============================================================================
# SLIDE 11: CONCLUSIONES Y HOJA DE RUTA (MEMO SEC. 8)
# ==============================================================================
s11 = prs.slides.add_slide(blank_layout)
set_slide_background(s11, COLOR_LIGHT_BG)
add_header(s11, "Conclusiones del Technical Lead y Hoja de Ruta Tecnológica", "CONCLUSIONES ESTRATÉGICAS & HOJA DE RUTA", 11)

concl_pillars = [
    ("1. RIGOR METODOLÓGICO Y CONTABLE", [
        "Diagnóstico forense que desmitificó el supuesto 9.6% de quiebres y rescató el 100% de la historia.",
        "Variable objetivo formulada en flujos netos diarios estacionarios, eliminando la deriva de saldo.",
        "Modelo lineal Ridge L2 completamente explicable, auditable y transparente ante reguladores."
    ], COLOR_COBRE),
    ("2. IMPACTO FINANCIERO COMPROBADO", [
        "100% de cumplimiento en SLA: CERO días en déficit en los 70 días de prueba fuera de muestra.",
        "96.9% de reducción en transferencias bancarias: de 97 operaciones reactivas a solo 3 fondeos quincenales.",
        "Preservación del float en la matriz (+12.97M COP) y costo de comisiones marginal ($50 USD + $20 MXN)."
    ], COLOR_EMERALD),
    ("3. GOBERNANZA Y ESCALABILIDAD", [
        "4 Circuit Breakers automáticos que blindan la cuenta nodriza y contienen anomalías operativas.",
        "Pipeline productivo en Airflow a las 06:00 UTC con contratos de datos dbt y observabilidad MLOps (KS / PSI).",
        "Despacho seguro de órdenes con firma criptográfica y esquema de competencia Champion-Challenger."
    ], COLOR_SKY_BLUE)
]

for idx, (c_title, c_items, c_color) in enumerate(concl_pillars):
    x_pos = Inches(0.8 + idx * 4.0)
    add_card(s11, x_pos, Inches(1.4), Inches(3.733), Inches(3.1), bg_color=COLOR_WHITE)
    
    tb_c = s11.shapes.add_textbox(x_pos + Inches(0.15), Inches(1.5), Inches(3.43), Inches(0.35))
    p = tb_c.text_frame.paragraphs[0]
    p.text = c_title
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = c_color
    
    add_bullet_list(s11, x_pos + Inches(0.15), Inches(1.95), Inches(3.43), Inches(2.4), c_items, font_size=9.2, space_after=6)

add_card(s11, Inches(0.8), Inches(4.7), Inches(11.733), Inches(2.35), bg_color=COLOR_SLATE_CARD, border_color=COLOR_COBRE)
tb_rm = s11.shapes.add_textbox(Inches(1.0), Inches(4.8), Inches(11.3), Inches(0.35))
p = tb_rm.text_frame.paragraphs[0]
p.text = "HOJA DE RUTA TECNOLÓGICA (PRÓXIMAS FASES DE EVOLUCIÓN EN COBRE)"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = COLOR_COBRE

add_bullet_list(s11, Inches(1.0), Inches(5.2), Inches(11.3), Inches(1.7), [
    "Fase A (Data Cloud & Streaming): Integración nativa con Snowflake / BigQuery y validación contable sub-minutaria con dbt.",
    "Fase B (Rieles 24/7): Soporte especializado para sistemas de compensación instantánea continua (SPEI 24/7 en México, Pix en Brasil, Bre-B en Colombia).",
    "Fase C (Optimización de FX Dinámico): Incorporación de modelos de aprendizaje por refuerzo restringido para sincronizar conversiones de divisas con ventanas de mejor spread cambiario.",
    "Fase D (Escalado Panregional): Despliegue de tesorería multi-entidad consolidando operaciones a nivel panregional en toda América Latina."
], font_size=9.2, text_color=COLOR_WHITE, space_after=4)

# ==============================================================================
# SAVE PRESENTATION
# ==============================================================================
output_path = os.path.join(os.path.dirname(__file__), "presentacion_ejecutiva_tesoreria.pptx")
fallback_path = os.path.join(os.path.dirname(__file__), "presentacion_ejecutiva_tesoreria_actualizada.pptx")

try:
    prs.save(output_path)
    print(f"Presentation successfully saved to: {output_path}")
except PermissionError:
    prs.save(fallback_path)
    print(f"Nota: El archivo principal está abierto en PowerPoint. Se guardó copia actualizada en: {fallback_path}")

try:
    prs.save(fallback_path)
    print(f"Verified fallback copy also saved to: {fallback_path}")
except Exception as e:
    pass

print(f"Total slides generated: {len(prs.slides)}")
