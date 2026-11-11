"""
build_iitj_ppt.py
Generates the official IIT Jodhpur B.Tech Project Evaluation PowerPoint Presentation (.pptx).
Aligned 1:1 with docs/BTP_IITJ_Final_Report.pdf.
Candidate: Ayush Kumar | Roll No.: B23CI1009
Supervisor: Dr. Tekcham Gishan Singh, Assistant Professor
Department of Civil and Infrastructure Engineering, IIT Jodhpur
"""

from pathlib import Path
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

PROJECT_ROOT = Path(r"c:\Users\Ayush\Documents\BTP_Aggregate_ML")
DOCS_DIR = PROJECT_ROOT / "docs"
FIGURES_DIR = DOCS_DIR / "figures"
PPTX_OUT = DOCS_DIR / "BTP_IITJ_Presentation.pptx"
ARTIFACT_DIR = Path(r"C:\Users\Ayush\.gemini\antigravity\brain\aae4c91f-8ef8-4fa8-b316-d7101184cc0e")
PPTX_ARTIFACT = ARTIFACT_DIR / "BTP_IITJ_Presentation.pptx"

# Color Palette (IIT Jodhpur Academic Theme)
NAVY = RGBColor(30, 58, 138)       # #1E3A8A Primary IIT Navy
DARK_NAVY = RGBColor(15, 23, 42)   # #0F172A Slate Dark
TEAL = RGBColor(15, 118, 110)      # #0F766E Engineering Accent
AMBER = RGBColor(180, 83, 9)       # #B45309 Highlight Accent
LIGHT_BG = RGBColor(248, 250, 252) # #F8FAFC Card Fill
CARD_ALT = RGBColor(239, 246, 255) # #EFF6FF Soft Blue Fill
BORDER = RGBColor(203, 213, 225)   # #CBD5E1 Subtle Border
TEXT_DARK = RGBColor(30, 41, 59)   # #1E293B Body Text
TEXT_MUTED = RGBColor(100, 116, 139) # #64748B Captions/Footer
WHITE = RGBColor(255, 255, 255)

FONT_HEAD = "Calibri"
FONT_BODY = "Calibri"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

TOTAL_SLIDES = 14

def set_notes(slide, text):
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = text

def add_slide_chrome(slide, title_text, section_tag, slide_num):
    # Top navy header bar
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.95))
    bar.fill.solid()
    bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background()

    # Gold/Teal thin accent stripe below header
    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0.95), Inches(13.333), Inches(0.05))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = TEAL
    stripe.line.fill.background()

    # Section tag + Slide Title
    tb = slide.shapes.add_textbox(Inches(0.55), Inches(0.12), Inches(10.5), Inches(0.75))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

    p0 = tf.paragraphs[0]
    r0 = p0.add_run()
    r0.text = section_tag.upper()
    r0.font.name = FONT_HEAD
    r0.font.size = Pt(10)
    r0.font.bold = True
    r0.font.color.rgb = RGBColor(147, 197, 253)

    p1 = tf.add_paragraph()
    r1 = p1.add_run()
    r1.text = title_text
    r1.font.name = FONT_HEAD
    r1.font.size = Pt(22)
    r1.font.bold = True
    r1.font.color.rgb = WHITE

    # Right small IITJ label in header
    rb = slide.shapes.add_textbox(Inches(10.8), Inches(0.28), Inches(2.1), Inches(0.4))
    rtf = rb.text_frame
    rp = rtf.paragraphs[0]
    rp.alignment = PP_ALIGN.RIGHT
    rr = rp.add_run()
    rr.text = "IIT Jodhpur | BTP 2026"
    rr.font.name = FONT_HEAD
    rr.font.size = Pt(11)
    rr.font.bold = True
    rr.font.color.rgb = RGBColor(226, 232, 240)

    # Bottom footer line + metadata
    fline = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.55), Inches(7.05), Inches(12.23), Inches(0.015))
    fline.fill.solid()
    fline.fill.fore_color.rgb = BORDER
    fline.line.fill.background()

    fb_left = slide.shapes.add_textbox(Inches(0.55), Inches(7.1), Inches(9.5), Inches(0.3))
    fp_l = fb_left.text_frame.paragraphs[0]
    fr_l = fp_l.add_run()
    fr_l.text = "Ayush Kumar (B23CI1009)  |  Dept. of Civil & Infrastructure Engineering  |  Supervisor: Dr. Tekcham Gishan Singh"
    fr_l.font.name = FONT_BODY
    fr_l.font.size = Pt(9.5)
    fr_l.font.color.rgb = TEXT_MUTED

    fb_right = slide.shapes.add_textbox(Inches(11.0), Inches(7.1), Inches(1.78), Inches(0.3))
    fp_r = fb_right.text_frame.paragraphs[0]
    fp_r.alignment = PP_ALIGN.RIGHT
    fr_r = fp_r.add_run()
    fr_r.text = f"Slide {slide_num} / {TOTAL_SLIDES}"
    fr_r.font.name = FONT_BODY
    fr_r.font.size = Pt(9.5)
    fr_r.font.bold = True
    fr_r.font.color.rgb = NAVY

def add_card(slide, left, top, width, height, fill_rgb=LIGHT_BG, border_rgb=BORDER, header_text=None, header_color=NAVY):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.adjustments[0] = 0.02
    card.fill.solid()
    card.fill.fore_color.rgb = fill_rgb
    card.line.color.rgb = border_rgb
    card.line.width = Pt(1)

    if header_text:
        hbar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(0.42))
        hbar.fill.solid()
        hbar.fill.fore_color.rgb = header_color
        hbar.line.fill.background()

        htb = slide.shapes.add_textbox(Inches(left + 0.15), Inches(top + 0.06), Inches(width - 0.3), Inches(0.32))
        htf = htb.text_frame
        htf.margin_top = htf.margin_bottom = 0
        hp = htf.paragraphs[0]
        hr = hp.add_run()
        hr.text = header_text
        hr.font.name = FONT_HEAD
        hr.font.size = Pt(13)
        hr.font.bold = True
        hr.font.color.rgb = WHITE
    return card

def add_bullets(slide, left, top, width, height, items, font_size=13, space_after=8):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

    for idx, (lead, body) in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.space_after = Pt(space_after)
        p.line_spacing = 1.15
        if lead:
            r_lead = p.add_run()
            r_lead.text = f"▪  {lead}: " if body else f"▪  {lead}"
            r_lead.font.name = FONT_BODY
            r_lead.font.size = Pt(font_size)
            r_lead.font.bold = True
            r_lead.font.color.rgb = NAVY
        if body:
            r_body = p.add_run()
            r_body.text = body
            r_body.font.name = FONT_BODY
            r_body.font.size = Pt(font_size)
            r_body.font.color.rgb = TEXT_DARK
    return tb

def add_image_fit(slide, filename, box_left, box_top, box_w, box_h, caption=None):
    img_path = FIGURES_DIR / filename
    if not img_path.exists():
        return
    with Image.open(img_path) as im:
        iw, ih = im.size
    img_ratio = iw / ih

    cap_reserve = 0.28 if caption else 0.0
    avail_h = box_h - cap_reserve
    box_ratio = box_w / avail_h

    if img_ratio > box_ratio:
        draw_w = box_w
        draw_h = box_w / img_ratio
    else:
        draw_h = avail_h
        draw_w = avail_h * img_ratio

    draw_x = box_left + (box_w - draw_w) / 2.0
    draw_y = box_top + (avail_h - draw_h) / 2.0

    slide.shapes.add_picture(str(img_path), Inches(draw_x), Inches(draw_y), width=Inches(draw_w), height=Inches(draw_h))

    if caption:
        ctb = slide.shapes.add_textbox(Inches(box_left), Inches(draw_y + draw_h + 0.04), Inches(box_w), Inches(0.26))
        ctf = ctb.text_frame
        ctf.word_wrap = True
        ctf.margin_top = ctf.margin_bottom = 0
        cp = ctf.paragraphs[0]
        cp.alignment = PP_ALIGN.CENTER
        cr = cp.add_run()
        cr.text = caption
        cr.font.name = FONT_BODY
        cr.font.size = Pt(9.5)
        cr.font.italic = True
        cr.font.color.rgb = TEXT_MUTED

def add_styled_table(slide, left, top, width, height, headers, rows, col_widths=None, font_size=10.5):
    shape = slide.shapes.add_table(len(rows) + 1, len(headers), Inches(left), Inches(top), Inches(width), Inches(height))
    table = shape.table
    if col_widths:
        for i, w in enumerate(col_widths):
            table.columns[i].width = Inches(w)

    # Header
    for c_idx, h in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = h
        r.font.name = FONT_HEAD
        r.font.size = Pt(font_size)
        r.font.bold = True
        r.font.color.rgb = WHITE

    # Data rows
    for r_idx, row_vals in enumerate(rows):
        bg = WHITE if r_idx % 2 == 0 else LIGHT_BG
        for c_idx, val in enumerate(row_vals):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if c_idx == 0 else PP_ALIGN.CENTER
            r = p.add_run()
            r.text = str(val)
            r.font.name = FONT_BODY
            r.font.size = Pt(font_size - 0.5)
            r.font.color.rgb = TEXT_DARK
            if r_idx == 0 and c_idx >= 2 and len(rows) > 5:
                r.font.bold = True
    return table

print("Building IIT Jodhpur BTP PowerPoint Presentation (14 Slides)...")

# ==============================================================================
# SLIDE 1: TITLE SLIDE
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = LIGHT_BG
bg1.line.fill.background()

# Left Navy Accent Panel
panel = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.45), Inches(7.5))
panel.fill.solid()
panel.fill.fore_color.rgb = NAVY
panel.line.fill.background()

panel2 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.45), Inches(0), Inches(0.10), Inches(7.5))
panel2.fill.solid()
panel2.fill.fore_color.rgb = TEAL
panel2.line.fill.background()

# IITJ Logo Top Right/Center
add_image_fit(s1, "iit_jodhpur_logo.png", 5.85, 0.55, 1.65, 1.65)

# Department header
tb_dept = s1.shapes.add_textbox(Inches(1.1), Inches(2.25), Inches(11.1), Inches(0.45))
p_dept = tb_dept.text_frame.paragraphs[0]
p_dept.alignment = PP_ALIGN.CENTER
r_dept = p_dept.add_run()
r_dept.text = "INDIAN INSTITUTE OF TECHNOLOGY JODHPUR  |  B.TECH PROJECT EVALUATION (2026)"
r_dept.font.name = FONT_HEAD
r_dept.font.size = Pt(12)
r_dept.font.bold = True
r_dept.font.color.rgb = TEAL

# Main Title
tb_t = s1.shapes.add_textbox(Inches(1.0), Inches(2.75), Inches(11.3), Inches(1.5))
tf_t = tb_t.text_frame
tf_t.word_wrap = True
p_t = tf_t.paragraphs[0]
p_t.alignment = PP_ALIGN.CENTER
p_t.line_spacing = 1.2
r_t = p_t.add_run()
r_t.text = "Numerical Modelling and Machine Learning Prediction of Single-Particle Crushing Mechanics and Fractal Gradation of Recycled Aggregates"
r_t.font.name = FONT_HEAD
r_t.font.size = Pt(25)
r_t.font.bold = True
r_t.font.color.rgb = DARK_NAVY

# Metadata Card at Bottom
add_card(s1, 2.1, 4.55, 9.1, 2.05, fill_rgb=WHITE, border_rgb=NAVY)
tb_meta = s1.shapes.add_textbox(Inches(2.35), Inches(4.7), Inches(8.6), Inches(1.75))
tf_m = tb_meta.text_frame
tf_m.word_wrap = True
meta_lines = [
    ("Presented by: ", "Ayush Kumar  (Roll No.: B23CI1009)", 16, True),
    ("Supervisor: ", "Dr. Tekcham Gishan Singh, Assistant Professor", 15, False),
    ("Department: ", "Department of Civil and Infrastructure Engineering, IIT Jodhpur", 14, False),
    ("Date: ", "November 2026", 13, False),
]
for idx, (k, v, sz, is_b) in enumerate(meta_lines):
    pm = tf_m.paragraphs[0] if idx == 0 else tf_m.add_paragraph()
    pm.alignment = PP_ALIGN.CENTER
    pm.space_after = Pt(6)
    rk = pm.add_run()
    rk.text = k
    rk.font.name = FONT_BODY
    rk.font.size = Pt(sz)
    rk.font.bold = True
    rk.font.color.rgb = NAVY
    rv = pm.add_run()
    rv.text = v
    rv.font.name = FONT_BODY
    rv.font.size = Pt(sz)
    rv.font.bold = is_b
    rv.font.color.rgb = TEXT_DARK

set_notes(s1, "Good morning/afternoon respected panel members. I am Ayush Kumar, Roll No. B23CI1009, presenting my B.Tech Project supervised by Dr. Tekcham Gishan Singh. My project develops a Physics-Informed Machine Learning framework and Virtual Testing Suite to instantaneously predict single-particle crushing strength, failure force, energy, and post-breakage particle size distribution of recycled construction aggregates.")

# ==============================================================================
# SLIDE 2: BACKGROUND & MOTIVATION
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
add_slide_chrome(s2, "Background & Engineering Motivation", "1. Introduction", 2)

add_card(s2, 0.55, 1.3, 5.95, 4.3, fill_rgb=WHITE, border_rgb=BORDER, header_text="The Construction & Demolition (C&D) Waste Crisis", header_color=NAVY)
add_bullets(s2, 0.75, 1.9, 5.55, 3.5, [
    ("Global Aggregate Demand", "Over 50 billion tonnes/year of virgin stone & sand mined globally, depleting quarries and riverbeds."),
    ("C&D Waste Generation", "Exceeds 3.0 billion tonnes/year worldwide; India generates >150 million tonnes/year (CPCB 2024), yet <5% is reused structurally."),
    ("Circular Economy Materials", "Recycled Concrete (RC), Recycled Mortar (RM), and Recycled Brick (RB) offer sustainable substitutes for highway subgrades & concrete.")
], font_size=13.5, space_after=12)

add_card(s2, 6.8, 1.3, 5.95, 4.3, fill_rgb=WHITE, border_rgb=BORDER, header_text="Why Recycled Aggregates Crush Prematurely", header_color=TEAL)
add_bullets(s2, 7.0, 1.9, 5.55, 3.5, [
    ("Multi-Phase Heterogeneity", "Unlike virgin basalt/granite, recycled aggregate retains porous adhered mortar & two weak Interfacial Transition Zones (ITZs)."),
    ("Flaw & Water Vulnerability", "High micro-crack density gives 4–10% water absorption (vs. <1.5% virgin rock) and wide strength scatter."),
    ("Compaction Degradation", "Under vibratory rollers & traffic loads, grains crush into excess fines (<0.075 mm), causing drainage blockages & rutting.")
], font_size=13.5, space_after=12)

add_card(s2, 0.55, 5.85, 12.2, 0.95, fill_rgb=CARD_ALT, border_rgb=NAVY)
tb_bot2 = s2.shapes.add_textbox(Inches(0.8), Inches(6.02), Inches(11.7), Inches(0.6))
tf_bot2 = tb_bot2.text_frame
tf_bot2.word_wrap = True
p_b2 = tf_bot2.paragraphs[0]
r_b2a = p_b2.add_run()
r_b2a.text = "Core Goal: "
r_b2a.font.name = FONT_HEAD
r_b2a.font.size = Pt(14)
r_b2a.font.bold = True
r_b2a.font.color.rgb = NAVY
r_b2b = p_b2.add_run()
r_b2b.text = "Screen and predict single-particle crushing mechanics & post-breakage gradation non-destructively in <0.1 seconds before road/concrete placement."
r_b2b.font.name = FONT_BODY
r_b2b.font.size = Pt(13.5)
r_b2b.font.color.rgb = TEXT_DARK

set_notes(s2, "In India, CPCB reports over 150 million tonnes of C&D waste per year, mostly dumped in landfills. Using crushed concrete, mortar, and brick in road subbases saves virgin stone, but engineers avoid them because old adhered mortar makes them crush unpredictably under road rollers. If they crush too much, fine dust clogs road drainage and causes rutting.")

# ==============================================================================
# SLIDE 3: PROBLEM STATEMENT & OBJECTIVES
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
add_slide_chrome(s3, "Problem Definition & Research Objectives", "2–3. Literature & Problem Scope", 3)

headers_s3 = ["Evaluation Aspect", "Traditional Lab Testing (UTM + Sieving / IS 2386)", "Proposed Physics-Informed ML Suite"]
rows_s3 = [
    ["Test Nature", "100% Destructive — specimen lost after single crush", "Non-Destructive — zero sample destruction"],
    ["Testing Speed", "16–24 hours per batch (calipers, UTM, mechanical sieving)", "< 0.1 seconds per particle (real-time inference)"],
    ["Occupational Safety", "Generates hazardous respirable crystalline silica dust", "Completely digital & dust-free screening"],
    ["Shape Sensitivity", "Coarse bulk indices (ACV/LAA) hide 3D shape effects", "Captures continuous 3D Sphericity (Φ) & L, I, S axes"],
    ["Output Completeness", "Single aggregate strength or isolated sieve value", "Simultaneous Force, Strength, Energy & Fractal Curve"]
]
add_styled_table(s3, 0.55, 1.22, 12.2, 2.45, headers_s3, rows_s3, col_widths=[2.2, 5.0, 5.0], font_size=11.5)

add_card(s3, 0.55, 3.92, 12.2, 2.95, fill_rgb=WHITE, border_rgb=BORDER, header_text="Four Core Project Objectives (Within 4.75–37.5 mm Quasi-Static Scope)", header_color=TEAL)
add_bullets(s3, 0.75, 4.46, 11.8, 2.3, [
    ("1. Physics-Coupled Benchmark Dataset", "Synthesize N = 3,600 calibrated particles (RC, RM, RB) uniting Hiramatsu-Oka, Bagheri, Cai et al. (2024), and Liang et al. (2025) fracture laws."),
    ("2. Multi-Target ML Benchmarking", "Compare 6 regressors (CatBoost, LightGBM, XGBoost, Random Forest, MLP Neural Network, Ridge) across Force, Strength, Energy & Fractal Dimension."),
    ("3. Explainable AI (TreeSHAP) Verification", "Quantify physical feature importance on XGBoost models to confirm they obey brittle fracture physics rather than overfitting noise."),
    ("4. Interactive Streamlit Engineering Suite", "Deploy a 4-tab tool (Virtual UTM, Scaling Simulator, Auxiliary CV Photo Scanner, AI & Benchmarks) for non-destructive aggregate screening.")
], font_size=12, space_after=5)

set_notes(s3, "Standard laboratory tests like ACV and LAA (IS 2386 / ASTM C131) crush aggregates in bulk, hiding how individual grain size and 3D shape trigger failure. Single-particle UTM testing solves this scientifically, but takes up to 24 hours per batch and creates silica dust. Our four objectives build a fast, explainable virtual twin.")

# ==============================================================================
# SLIDE 4: GOVERNING PHYSICS & ZINGG MORPHOLOGY
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
add_slide_chrome(s4, "Governing Fracture Physics & 3D Morphology", "4.1 Methodology — Mechanics", 4)

add_card(s4, 0.55, 1.2, 5.95, 2.1, fill_rgb=CARD_ALT, border_rgb=NAVY, header_text="Geometry & Tensile Rupture (Bagheri & Hiramatsu-Oka)", header_color=NAVY)
add_bullets(s4, 0.72, 1.72, 5.6, 1.5, [
    ("Triaxial Dimensions", "Longest (L), Intermediate (I), Shortest (S) axes; 3D Sphericity Φ = ∛[(I·S)/L²]"),
    ("Effective Diameter (Eq. 4.2)", "d₀ = 0.887 · ∛(L · I · S)  [Bagheri et al., 2015]"),
    ("Peak Force–Strength (Eq. 4.3)", "Ff = (σf · d₀²) / 0.9  [Hiramatsu & Oka, 1966]")
], font_size=12, space_after=5)

add_card(s4, 6.8, 1.2, 5.95, 2.1, fill_rgb=CARD_ALT, border_rgb=TEAL, header_text="Weibull Scaling & Fractal Gradation (Liang / Cai / Turcotte)", header_color=TEAL)
add_bullets(s4, 6.98, 1.72, 5.6, 1.5, [
    ("Strength Scaling (Eq. 4.4)", "σf(d₀, Φ) = [p · Φ^q] × [σf₀(d₀) / σf₀(d_ref)]  (Liang Table 2)"),
    ("Crushing Energy (Eq. 4.5)", "Ef = c·Φ^d·(d₀/25)³ (Φ<0.8)  |  Sat. Law (Φ≥0.8) [mJ]"),
    ("Fractal Gradation (Eq. 4.6)", "F(d_i) = min[100, (d_i / d₀)^(3 - D) × 100]")
], font_size=12, space_after=5)

# Panoramic Zingg Figure across bottom
add_card(s4, 0.55, 3.45, 12.2, 3.45, fill_rgb=WHITE, border_rgb=BORDER)
add_image_fit(s4, "fig1_zingg_shape_classification.png", 0.7, 3.52, 11.9, 3.3, caption="Fig. 4.1: Zingg 3D particle shape classification across Disk, Block, Blade, and Bar morphological domains (0.67 cutoffs; N=3,600).")

set_notes(s4, "Here are the exact physics laws driving our model. First, we convert L, I, S into Hiramatsu loading diameter d0 and Cai's 3D sphericity Phi. Larger particles are weaker because they contain more internal flaws—captured by Weibull's exponent (-3/m). Flatter or elongated particles fail early due to bending. After fracture, fragment sizes follow Turcotte's fractal dimension D.")

# ==============================================================================
# SLIDE 5: CALIBRATION DATASET & WEIBULL SCALING
# ==============================================================================
s5 = prs.slides.add_slide(blank_layout)
add_slide_chrome(s5, "Physics-Coupled Calibration Dataset (N = 3,600)", "4.1 Methodology — Dataset", 5)

headers_s5 = ["Material Type", "σf₀ (MPa) [3 brk]", "m [3 brackets]", "p , q", "c (mJ), d", "D_size [3 brk]"]
rows_s5 = [
    ["Recycled Concrete (RC)", "6.51 / 6.28 / 6.07", "1.58 / 1.30 / 1.25", "9.35, 2.13", "2061, 1.28", "1.66–1.87"],
    ["Recycled Mortar (RM)", "3.03 / 2.97 / 2.91", "2.70 / 2.73 / 2.76", "4.69, 2.21", "2041, 2.66", "1.77–2.11"],
    ["Recycled Brick (RB)", "6.35 / 6.21 / 4.92", "2.58 / 2.61 / 3.32", "3.84, 1.68", "1511, 2.16", "1.68–2.01"]
]
add_styled_table(s5, 0.55, 1.25, 6.2, 1.9, headers_s5, rows_s5, col_widths=[1.65, 1.15, 1.1, 0.75, 0.80, 0.75], font_size=9.8)

add_card(s5, 0.55, 3.35, 6.2, 3.45, fill_rgb=WHITE, border_rgb=BORDER, header_text="Benchmark Dataset Architecture (Table 4.1)", header_color=NAVY)
add_bullets(s5, 0.75, 3.92, 5.8, 2.75, [
    ("Total Samples", "N = 3,600 synthetic particles calibrated strictly to Liang et al. (2025) & Cai et al. (2024) tables."),
    ("Three Sieve Brackets", "400 particles per bracket × 3 materials across 4.75–9.5 mm, 9.5–19.0 mm, and 19.0–37.5 mm."),
    ("Material Ranking", "RC has highest shape strength (p = 9.35 MPa, dataset mean 4.30 MPa); porous RB (mean 2.31 MPa) & RM (2.11 MPa) are weaker."),
    ("Experimental Noise", "Realistic ~7% measurement noise injected across targets matching laboratory UTM dispersion.")
], font_size=12, space_after=8)

add_card(s5, 6.95, 1.25, 5.8, 5.55, fill_rgb=WHITE, border_rgb=BORDER)
add_image_fit(s5, "fig2_weibull_survival_curves.png", 7.1, 1.4, 5.5, 5.25, caption="Fig. 4.2: Weibull survival distributions and log-linear plots across 3 materials and sieve brackets.")

set_notes(s5, "Using published parameters from Liang et al. 2025 and Cai et al. 2024 (Table 4.1), we synthesized 3,600 particles across Concrete, Brick, and Mortar. In Fig 4.2, porous Brick shows strong coarse weakening (19-37.5 mm shifts left because sigma_f0 drops from 6.35 to 4.92 MPa), whereas in Concrete and Mortar the larger particles from Cai Table 1 are slightly more spherical, offsetting the gentle size drop.")

# ==============================================================================
# SLIDE 6: ML ARCHITECTURE & PIPELINE
# ==============================================================================
s6 = prs.slides.add_slide(blank_layout)
add_slide_chrome(s6, "Machine Learning Architecture & Training Pipeline", "4.2 Methodology — ML Pipeline", 6)

# 4-Step Horizontal Flowchart using shapes
steps = [
    ("1. 16-D Feature Vector", "13 Continuous Inputs:\nL, I, S, EI, FI, Φ, Sf, d_eq, d₀,\nApp./Bulk Density, E, ν\n+ 3 Label Encoded Classes", NAVY),
    ("2. Stratified Partitioning", "80% Training (N = 2,880)\n20% Hold-out Test (N = 720)\nStandardScaler Z-Score +\nBreakage-Mode Stratification", TEAL),
    ("3. Six Trained Regressors", "CatBoost, LightGBM,\nXGBoost, Random Forest,\nMLP Neural Network,\n& Ridge Polynomial (deg=2)", NAVY),
    ("4. Four Target Outputs", "Crushing Strength σf (MPa)\nPeak Force Ff (kN)\nCrushing Energy Ef (mJ)\nFractal Dimension D", AMBER)
]
for i, (st_title, st_body, col) in enumerate(steps):
    x = 0.55 + i * 3.12
    add_card(s6, x, 1.25, 2.85, 2.45, fill_rgb=WHITE, border_rgb=col, header_text=st_title, header_color=col)
    tb = s6.shapes.add_textbox(Inches(x + 0.12), Inches(1.8), Inches(2.6), Inches(1.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.line_spacing = 1.25
    r = p.add_run()
    r.text = st_body
    r.font.name = FONT_BODY
    r.font.size = Pt(11.5)
    r.font.color.rgb = TEXT_DARK
    if i < 3:
        arr = s6.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x + 2.89), Inches(2.35), Inches(0.20), Inches(0.28))
        arr.fill.solid()
        arr.fill.fore_color.rgb = TEXT_MUTED
        arr.line.fill.background()

# Hyperparameter Table (Table 4.2)
headers_s6 = ["Model Architecture", "Key Hyperparameters", "Loss Function", "Regularization", "Optimization"]
rows_s6 = [
    ["CatBoost Regressor", "depth=8, iterations=300, lr=0.05", "RMSE", "l2_leaf_reg=3.0", "Ordered Boosting"],
    ["LightGBM Regressor", "max_depth=8, n_est=300, lr=0.05", "Squared Error", "reg_alpha=0.1, λ=1.0", "Histogram GBDT"],
    ["XGBoost Regressor", "max_depth=8, n_est=300, lr=0.05", "Squared Error", "colsample=0.8, sub=0.8", "Hist / Greedy Tree"],
    ["Random Forest", "n_estimators=200, max_depth=15", "Squared Error", "min_split=5, min_leaf=2", "Bagging Ensemble"],
    ["MLP Neural Network", "hidden=(128,64,32), ReLU", "MSE (Early Stop)", "alpha=0.001, batch=64", "Adam (lr=1e-3)"],
    ["Ridge Polynomial", "degree=2, include_bias=False", "Squared Loss", "alpha=1.0 (L2 Penalty)", "Closed-Form Ridge"]
]
add_styled_table(s6, 0.55, 3.95, 12.2, 2.85, headers_s6, rows_s6, col_widths=[2.1, 3.1, 2.0, 2.6, 2.4], font_size=10.5)

set_notes(s6, "Our ML pipeline converts 16 particle features into 4 simultaneous mechanical predictions. We split the 3,600 particles 80/20 stratified by breakage mode so there is zero data leakage, applied StandardScaler fitted only on the training fold, and benchmarked 6 regressors with fixed hyperparameters. CatBoost uses depth-8 symmetric trees with ordered boosting to prevent overfitting.")

# ==============================================================================
# SLIDE 7: MODEL PERFORMANCE BENCHMARKS
# ==============================================================================
s7 = prs.slides.add_slide(blank_layout)
add_slide_chrome(s7, "Model Performance Benchmarks on Hold-Out Test Set", "5.1 Numerical Findings", 7)

headers_s7 = ["Model Architecture", "Target Variable", "R² Score", "RMSE", "MAE", "MAPE (%)"]
rows_s7 = [
    ["CatBoost Regressor", "Peak Force Ff (kN)", "0.9871", "0.081 kN", "0.050 kN", "6.56%"],
    ["CatBoost Regressor", "Crushing Strength (MPa)", "0.9636", "0.235 MPa", "0.172 MPa", "5.81%"],
    ["CatBoost Regressor", "Crushing Energy Ef (mJ)", "0.9498", "82.53 mJ", "23.36 mJ", "9.13%"],
    ["CatBoost Regressor", "Fractal Dimension D", "0.9469", "0.032", "0.025", "1.37%"],
    ["LightGBM Regressor", "Peak Force Ff (kN)", "0.9852", "0.087 kN", "0.052 kN", "6.48%"],
    ["XGBoost Regressor", "Peak Force Ff (kN)", "0.9847", "0.089 kN", "0.054 kN", "6.67%"],
    ["Random Forest", "Peak Force Ff (kN)", "0.9840", "0.091 kN", "0.054 kN", "6.80%"],
    ["MLP Neural Network", "Peak Force Ff (kN)", "0.9866", "0.083 kN", "0.052 kN", "7.66%"],
    ["Ridge Polynomial", "Energy Ef (Piecewise Fail)", "0.8647", "135.44 mJ", "54.40 mJ", "65.08%"]
]
add_styled_table(s7, 0.55, 1.25, 6.75, 4.35, headers_s7, rows_s7, col_widths=[1.75, 1.75, 0.85, 0.85, 0.85, 0.70], font_size=10)

add_card(s7, 0.55, 5.75, 6.75, 1.1, fill_rgb=CARD_ALT, border_rgb=NAVY)
add_bullets(s7, 0.72, 5.86, 6.45, 0.9, [
    ("Why CatBoost Leads Overall", "CatBoost achieves top mean R² = 0.9619 (0.9871 Force, 0.9636 Strength). Ridge collapses on piecewise energy Ef (MAPE 65.1%), proving GBDT necessity.")
], font_size=11.5, space_after=2)

add_card(s7, 7.5, 1.25, 5.25, 5.6, fill_rgb=WHITE, border_rgb=BORDER)
add_image_fit(s7, "fig5_model_comparison_metrics.png", 7.62, 1.35, 5.0, 5.4, caption="Fig. 5.0: Comparative R², RMSE, MAE, and MAPE across the 6 regression architectures.")

set_notes(s7, "On the unseen hold-out test set of 720 particles, CatBoost achieved the best overall average R-squared of 0.9619: 0.9871 for peak force, 0.9636 for crushing strength, 0.9498 for energy, and 0.9469 for fractal dimension. Notice Ridge fails badly on crushing energy (65% MAPE) because energy switches piecewise at sphericity 0.80.")

# ==============================================================================
# SLIDE 8: PARITY PLOTS & RESIDUAL HOMOSCEDASTICITY
# ==============================================================================
s8 = prs.slides.add_slide(blank_layout)
add_slide_chrome(s8, "Actual vs. Predicted Parity & Residual Error Analysis", "5.2 & 5.4 Numerical Findings", 8)

add_card(s8, 0.55, 1.25, 5.75, 5.55, fill_rgb=WHITE, border_rgb=BORDER)
add_image_fit(s8, "fig6_actual_vs_predicted_parity.png", 0.68, 1.35, 5.5, 5.35, caption="Fig. 5.1: XGBoost test-set parity plots across σf, Ff, Ef, and D (±10% band).")

add_card(s8, 6.5, 1.25, 6.25, 2.35, fill_rgb=WHITE, border_rgb=BORDER, header_text="Parity Diagnostics (Fig. 5.1 — XGBoost R² = 0.922–0.985)", header_color=NAVY)
add_bullets(s8, 6.7, 1.8, 5.85, 1.7, [
    ("Tight ±10% Parity", "Most test points stay within the ±10% error band across all 3 materials (R² = 0.957 σf, 0.985 Ff, 0.922 Ef, 0.941 D)."),
    ("Clustered Fractal Tiers", "Fractal D plot reflects the 3 calibrated Liang et al. (2025) sieve brackets around 1.66–2.12.")
], font_size=12, space_after=8)

add_card(s8, 6.5, 3.8, 6.25, 3.0, fill_rgb=WHITE, border_rgb=BORDER, header_text="CatBoost Residual Stability across Sieve Brackets (Table 5.2)", header_color=TEAL)
headers_s8 = ["Size Bracket", "σf Mean / Std", "Ff Mean / Std", "Variance Check"]
rows_s8 = [
    ["Fine (4.75–9.5 mm)", "-0.013 / 0.230", "-0.001 / 0.018", "σf Homoscedastic"],
    ["Medium (9.5–19 mm)", "+0.002 / 0.245", "+0.001 / 0.067", "σf Levene p = 0.924"],
    ["Coarse (19–37.5 mm)", "+0.043 / 0.228", "+0.020 / 0.120", "Unbiased Mean ~0"]
]
add_styled_table(s8, 6.68, 4.35, 5.88, 1.65, headers_s8, rows_s8, col_widths=[1.65, 1.3, 1.3, 1.63], font_size=9.8)

tb_s8 = s8.shapes.add_textbox(Inches(6.7), Inches(6.15), Inches(5.85), Inches(0.5))
tf_s8 = tb_s8.text_frame
tf_s8.word_wrap = True
p_s8 = tf_s8.paragraphs[0]
r_s8 = p_s8.add_run()
r_s8.text = "Note: Crushing strength σf is strictly homoscedastic (p = 0.924); Ff std scales with d₀² while relative MAPE stays ~6.6%."
r_s8.font.name = FONT_BODY
r_s8.font.size = Pt(11)
r_s8.font.italic = True
r_s8.font.color.rgb = TEXT_DARK

set_notes(s8, "On the left, Fig 5.1 shows XGBoost actual vs predicted parity plots within plus-or-minus 10% bands. On the right, Table 5.2 checks CatBoost residuals across Fine, Medium, and Coarse fractions: crushing strength error variance is completely constant at 0.23 MPa (Levene p=0.924), while Peak Force std naturally scales with d0 squared.")

# ==============================================================================
# SLIDE 9: EXPLAINABLE AI (SHAP) FEATURE IMPORTANCE
# ==============================================================================
s9 = prs.slides.add_slide(blank_layout)
add_slide_chrome(s9, "Explainable AI: Physical Attribution via TreeSHAP", "5.3 Numerical Findings — SHAP", 9)

add_card(s9, 0.55, 1.25, 6.3, 5.55, fill_rgb=WHITE, border_rgb=BORDER)
add_image_fit(s9, "fig8_shap_feature_importance.png", 0.68, 1.35, 6.05, 5.35, caption="Fig. 5.2: XGBoost TreeSHAP Mean |SHAP| feature importance across all 4 targets.")

add_card(s9, 7.05, 1.25, 5.7, 5.55, fill_rgb=WHITE, border_rgb=BORDER, header_text="Deciphering the Physics Inside XGBoost (TreeSHAP)", header_color=NAVY)
add_bullets(s9, 7.25, 1.85, 5.3, 4.75, [
    ("1. Strength σf — Density & Sphericity Φ", "Apparent density (#1) separates strong RC (2.22 g/cm³) from RB/RM, while 3D Sphericity Φ (#2) captures platen stress distribution."),
    ("2. Force Ff & Energy Ef — Size Axes (S, d_eq)", "Shortest axis S (#1) and d_eq (#2) dominate Ff and Ef directly matching Ff ∝ d₀² area scaling and (d₀/25)³ volume scaling."),
    ("3. Fractal Dimension D — Size & Material", "d_eq (#1) and Apparent Density (#2) drive post-breakage D because larger fragments generate more secondary debris."),
    ("4. No Unphysical Shortcut Learning", "TreeSHAP confirms the ML splits strictly follow Hiramatsu-Oka, Cai, and Liang fracture mechanics.")
], font_size=12.5, space_after=12)

set_notes(s9, "Professors often ask how we know ML isn't a black box. We ran TreeSHAP on our XGBoost models (Fig 5.2). For Crushing Strength sigma_f, Apparent Density and Sphericity rank #1 and #2. For Peak Force and Energy, shortest axis S and nominal diameter d_eq rank #1 and #2 because area and volume drive total force and energy.")

# ==============================================================================
# SLIDE 10: 2D PARTIAL DEPENDENCE CONTOURS
# ==============================================================================
s10 = prs.slides.add_slide(blank_layout)
add_slide_chrome(s10, "2D Partial Dependence & Coupled Scaling Surfaces", "5.5–5.6 Numerical Findings", 10)

add_card(s10, 0.55, 1.25, 6.45, 5.55, fill_rgb=WHITE, border_rgb=BORDER)
add_image_fit(s10, "fig9_partial_dependence_contours.png", 0.68, 1.35, 6.2, 5.35, caption="Fig. 5.3: 2D Partial Dependence contour heatmaps over diameter d₀ and sphericity Φ.")

add_card(s10, 7.2, 1.25, 5.55, 5.55, fill_rgb=WHITE, border_rgb=BORDER, header_text="Engineering Design Insights from Contours", header_color=TEAL)
add_bullets(s10, 7.4, 1.85, 5.15, 4.75, [
    ("Coupled (Φ, d₀) Contours", "Strength σf rises steadily with Sphericity Φ (left to right), while Peak Force Ff peaks at upper-right where both size d₀ and Φ are high."),
    ("Piecewise Transition at Φ = 0.80", "Crushing energy Ef plot exposes the sharp Cai et al. (2024 Eq. 11) jump at Φ = 0.80 learned directly by the ML trees."),
    ("Step Boundary at d₀ = 20 mm", "Fractal D heatmap reveals the discrete sieve-bracket step at 20 mm in raw training bins—motivating smooth Tab 2 interpolation."),
    ("Quality Control Guideline", "Avoiding flaky particles (Φ < 0.55) prevents low strength and premature brittle failure.")
], font_size=12.5, space_after=12)

set_notes(s10, "Figure 5.3 maps the combined 2D partial dependence across size d0 (x-axis) and sphericity Phi (y-axis). Notice the critical boundary below sphericity 0.55 where strength and crushing energy plummet. Civil engineers can use these contour zones directly as quality-control acceptance thresholds.")

# ==============================================================================
# SLIDE 11: INTERACTIVE VIRTUAL TESTING SUITE (DEMO SCREENSHOTS)
# ==============================================================================
s11 = prs.slides.add_slide(blank_layout)
add_slide_chrome(s11, "Interactive Virtual Testing Suite (Streamlit Software Demo)", "6.1–6.4 Software Platform", 11)

add_card(s11, 0.55, 1.22, 6.1, 2.75, fill_rgb=WHITE, border_rgb=BORDER, header_text="Tab 1: Virtual UTM & Sieve Gradation Curve", header_color=NAVY)
add_image_fit(s11, "app_tab1_utm_gradation_curves.png", 0.68, 1.72, 5.84, 2.15, caption="Fig. 6.1: Live single-particle virtual compression & ASTM/IS post-breakage PSD.")

add_card(s11, 6.85, 1.22, 5.9, 2.75, fill_rgb=WHITE, border_rgb=BORDER, header_text="Tab 2: Multi-Scale Scaling Contour Simulator", header_color=TEAL)
add_image_fit(s11, "app_tab2_scaling_heatmap.png", 6.98, 1.72, 5.64, 2.15, caption="Fig. 6.2: Interactive 2D size-scaling response surfaces.")

add_card(s11, 0.55, 4.15, 6.1, 2.7, fill_rgb=WHITE, border_rgb=BORDER, header_text="Parametric Console & 3D Preview (Tab 1)", header_color=DARK_NAVY)
add_image_fit(s11, "sidebar_inputs.png", 0.68, 4.62, 5.84, 2.15, caption="Material selector, triaxial sliders (25 × 18 × 12 mm RC), and live 3D ellipsoid.")

add_card(s11, 6.85, 4.15, 5.9, 2.7, fill_rgb=CARD_ALT, border_rgb=NAVY, header_text="Four Integrated Engineering Modules", header_color=NAVY)
add_bullets(s11, 7.05, 4.70, 5.5, 2.05, [
    ("Tab 1 — Virtual UTM", "Instant σf, Ff, Ef, D, Weibull P_s survival metric, breakage mode, and sieve curve."),
    ("Tab 2 — Scaling Simulator", "Continuous vs. discrete size-scaling contours benchmarked against lab checkpoints."),
    ("Tab 3 — Auxiliary CV Scanner", "Optional OpenCV photo sizer estimating 2D L & I (assumes S = 0.65·I) as a convenience helper."),
    ("Tab 4 — AI & Benchmarks", "Interactive R² bar chart + test metrics tables + all 9 publication plots (SHAP, PDP, Parity).")
], font_size=11.5, space_after=5)

set_notes(s11, "We packaged the project into a 4-tab Streamlit dashboard. Tab 1 acts as a Virtual UTM showing a 3D grain, 4 metrics, breakage mode, and gradation curves. Tab 2 overlays model scaling against lab data from Liang and Cai. Tab 3 is an optional OpenCV photo helper assuming S equals 0.65 times I. Tab 4 displays all regression/classification metrics and publication SHAP/PDP figures.")

# ==============================================================================
# SLIDE 12: DESIGN CASE STUDY & IRC:37-2018 APPLICATION
# ==============================================================================
s12 = prs.slides.add_slide(blank_layout)
add_slide_chrome(s12, "Baseline RC Case Study & Pavement Gradation Screening", "6.5–6.6 Design Application", 12)

headers_s12 = ["Output Parameter", "Value", "Unit", "Physical Interpretation"]
rows_s12 = [
    ["Input Particle Size", "25 / 18 / 12", "mm", "Recycled Concrete (L / I / S axes)"],
    ["Equivalent Diameter d_eq", "17.54", "mm", "Equal-volume nominal diameter"],
    ["Bagheri Diameter d₀", "15.56", "mm", "Roughness-corrected diameter"],
    ["FI (S/I)  |  EI (I/L)", "0.667 | 0.720", "—", "Zingg Bar/Block boundary (0.67 cutoff)"],
    ["3D Sphericity (Φ)", "0.702", "—", "High sphericity (> 0.65 favorable zone)"],
    ["Crushing Strength (σf)", "4.50", "MPa", "Hiramatsu-Oka tensile splitting strength"],
    ["Peak Failure Force (Ff)", "1.210", "kN", "Catastrophic rupture load"],
    ["Est. Crushing Energy (Ef)", "315.9", "mJ", "Cai piecewise volumetric energy (0.316 J)"],
    ["Fractal Dimension (D)", "1.814", "—", "Single-particle exponent (Mode II rupture)"]
]
add_styled_table(s12, 0.55, 1.25, 6.55, 5.55, headers_s12, rows_s12, col_widths=[2.05, 1.05, 0.65, 2.8], font_size=10)

add_card(s12, 7.3, 1.25, 5.45, 5.55, fill_rgb=WHITE, border_rgb=TEAL, header_text="Gradation & Pavement Screening (Li 2021 & IRC:37-2018)", header_color=TEAL)
add_bullets(s12, 7.5, 1.85, 5.05, 4.75, [
    ("GSB / WMM Screening", "IRC:37-2018 & IS 383:2016 require roadbase aggregates to resist crushing into fine dust under roller compaction."),
    ("Over-Pulverization Risk (D > 2.63)", "Above Li et al. (2021) upper limit D = 2.631, crushing produces excess <0.075 mm fines, hurting permeability & causing rutting."),
    ("Baseline RC Verdict (D = 1.814)", "Single-particle D = 1.814 (composite RC = 2.12, inside Li 1.887–2.631) indicates coarse splitting with minimal fine silt generation."),
    ("Failure & Survival Check", "Mode II Mixed Corner Rupture with Weibull survival probability P_s = 0.516 (m = 1.28, σ_f0 = 6.21 MPa).")
], font_size=12.5, space_after=10)

set_notes(s12, "This table matches the exact default Tab 1 live screen for our baseline 25 by 18 by 12 mm Recycled Concrete particle: 4.50 MPa strength, 1.210 kN peak force, 315.9 mJ energy, and single-particle fractal dimension 1.814 (Mode II corner rupture). Low D confirms coarse splitting without excess <0.075 mm silt dust that blocks pavement drainage.")

# ==============================================================================
# SLIDE 13: EXPERIMENTAL LITERATURE VALIDATION
# ==============================================================================
s13 = prs.slides.add_slide(blank_layout)
add_slide_chrome(s13, "Validation Against Published Experimental Benchmarks", "6.7 Experimental Verification", 13)

headers_s13 = ["Material Type", "Published Experimental Source", "MAE (MPa)", "RMSE (MPa)", "MAPE (%)", "Agreement"]
rows_s13 = [
    ["Recycled Concrete (RC)", "Liang et al. (2025) & Cai et al. (2024)", "0.043", "0.060", "1.15%", "Outstanding"],
    ["Recycled Mortar (RM)", "Liang et al. (2025) & Cai et al. (2024)", "0.030", "0.047", "2.02%", "Outstanding"],
    ["Recycled Brick (RB)", "Liang et al. (2025) & Cai et al. (2024)", "0.148", "0.180", "5.07%", "High Fidelity"]
]
add_styled_table(s13, 0.55, 1.25, 12.2, 1.6, headers_s13, rows_s13, col_widths=[2.4, 3.6, 1.4, 1.4, 1.5, 1.9], font_size=11)

add_card(s13, 0.55, 3.05, 12.2, 3.85, fill_rgb=WHITE, border_rgb=BORDER)
add_image_fit(s13, "app_tab2_experimental_validation_subplots.png", 0.75, 3.12, 11.8, 3.7, caption="Fig. 6.3: Tab 2 size-scaling curves vs. experimental markers (Liang et al., 2025; Cai et al., 2024; Li et al., 2021).")

set_notes(s13, "To validate against published laboratory data, Table 6.2 reports exact error metrics computed in Tab 2 against Liang et al. (2025) and Cai et al. (2024): MAE is 0.043 MPa (1.15% MAPE) for RC, 0.030 MPa (2.02% MAPE) for RM, and 0.148 MPa (5.07% MAPE) for RB.")

# ==============================================================================
# SLIDE 14: SUMMARY & FUTURE PLAN OF WORK
# ==============================================================================
s14 = prs.slides.add_slide(blank_layout)
add_slide_chrome(s14, "Summary of Contributions & Future Work", "7. Conclusion", 14)

add_card(s14, 0.55, 1.25, 5.95, 4.35, fill_rgb=WHITE, border_rgb=NAVY, header_text="Key Project Contributions", header_color=NAVY)
add_bullets(s14, 0.75, 1.85, 5.55, 3.6, [
    ("Unified PIML Dataset", "Coupled Weibull size scaling, Hiramatsu-Oka tensile laws, Cai 3D sphericity, and Turcotte fractal gradation into N = 3,600 benchmark particles."),
    ("High-Accuracy CatBoost Surrogate", "Achieved best average R² = 0.9619 (0.9871 Force, 0.9636 Strength, 0.9498 Energy, 0.9469 D) & homoscedastic σf residuals."),
    ("Transparent Explainable AI", "Verified physics via XGBoost TreeSHAP (Density & Φ govern strength σf; S & d_eq govern Force & Energy)."),
    ("Deployable Engineering Suite", "Delivered a 4-tab Streamlit app (Tab 1 Virtual UTM: 1.210 kN / 4.50 MPa baseline) cutting test time to <0.1 s.")
], font_size=12.5, space_after=10)

add_card(s14, 6.8, 1.25, 5.95, 4.35, fill_rgb=WHITE, border_rgb=TEAL, header_text="Known Limitations & Future Work", header_color=TEAL)
add_bullets(s14, 7.0, 1.85, 5.55, 3.6, [
    ("Current Boundaries", "Quasi-static single-particle compression (4.75–37.5 mm); calibrated on literature data; CV assumes S = 0.65·I; mode clf ~54% acc."),
    ("Indian C&D Waste Lab Testing", "Perform physical UTM crushing on locally processed demolition samples (Delhi, Ahmedabad, Jodhpur) to validate locally."),
    ("Bulk DEM Simulation Coupling", "Integrate ML breakage criteria into 3D DEM codes (PFC3D / YADE) for full roller compaction & cyclic traffic simulations."),
    ("3D Depth Photogrammetry", "Upgrade optional CV helper with multi-view depth sensing to measure shortest axis S directly without assumptions.")
], font_size=12.5, space_after=10)

add_card(s14, 0.55, 5.8, 12.2, 1.0, fill_rgb=NAVY, border_rgb=NAVY)
tb_ty = s14.shapes.add_textbox(Inches(0.8), Inches(5.8), Inches(11.7), Inches(1.0))
tf_ty = tb_ty.text_frame
tf_ty.vertical_anchor = MSO_ANCHOR.MIDDLE
p_ty = tf_ty.paragraphs[0]
p_ty.alignment = PP_ALIGN.CENTER
r_ty = p_ty.add_run()
r_ty.text = "Thank You!  |  Open for Questions & Live Streamlit Virtual UTM Demonstration"
r_ty.font.name = FONT_HEAD
r_ty.font.size = Pt(18)
r_ty.font.bold = True
r_ty.font.color.rgb = WHITE

set_notes(s14, "In conclusion, we built a physics-informed ML framework achieving R-squared up to 0.9871 (mean 0.9619 for CatBoost), verified its physics with TreeSHAP, validated within 1.15% to 5.07% MAPE against Cai 2024 and Liang 2025, honestly documented limitations like quasi-static scope and stochastic breakage mode overlap, and deployed a 4-tab Streamlit app. Thank you!")

prs.save(str(PPTX_OUT))
prs.save(str(PPTX_ARTIFACT))
print(f"SUCCESS! Saved PowerPoint Presentation to:")
print(f"  - {PPTX_OUT} ({PPTX_OUT.stat().st_size:,} bytes)")
print(f"  - {PPTX_ARTIFACT} ({PPTX_ARTIFACT.stat().st_size:,} bytes)")
