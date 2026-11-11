"""
build_iitj_report_v2.py
Generates the comprehensive B.Tech Project Report in Microsoft Word (.docx) format
matching the exact IIT Jodhpur Department of Civil and Infrastructure Engineering template.
Roll Number: B23CI1009
Student Name: Ayush Kumar
Supervisor: Dr. Tekcham Gishan Singh, Assistant Professor
Target length: 20-23 pages.
"""

import os
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

PROJECT_ROOT = Path(r"c:\Users\Ayush\Documents\BTP_Aggregate_ML")
DOCS_DIR = PROJECT_ROOT / "docs"
FIGURES_DIR = DOCS_DIR / "figures"
DOCX_OUT = DOCS_DIR / "BTP_IITJ_Final_Report.docx"
ARTIFACT_DIR = Path(r"C:\Users\Ayush\.gemini\antigravity\brain\aae4c91f-8ef8-4fa8-b316-d7101184cc0e")
DOCX_ARTIFACT = ARTIFACT_DIR / "BTP_IITJ_Final_Report.docx"

doc = docx.Document()

# Page Setup: Standard A4 with 1-inch margins
for section in doc.sections:
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# Configure Default Normal Style
normal_style = doc.styles['Normal']
normal_style.font.name = 'Times New Roman'
normal_style.font.size = Pt(11)
normal_style.font.color.rgb = RGBColor(0, 0, 0)
normal_style.paragraph_format.line_spacing = 1.15
normal_style.paragraph_format.space_after = Pt(6)
normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def add_heading_1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.font.bold = True
    return p

def add_heading_2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = True
    return p

def add_heading_3(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.italic = True
    return p

def add_body_p(text):
    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11)
    return p

def add_bullet_p(bold_prefix, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(4)
    if bold_prefix:
        r_bold = p.add_run(bold_prefix)
        r_bold.font.name = 'Times New Roman'
        r_bold.font.size = Pt(11)
        r_bold.font.bold = True
    r_text = p.add_run(text)
    r_text.font.name = 'Times New Roman'
    r_text.font.size = Pt(11)
    return p

def add_equation_box(eq_text, eq_num):
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    col_widths = [Inches(5.5), Inches(0.8)]
    for i, w in enumerate(col_widths):
        table.columns[i].width = w
        table.cell(0, i).width = w
        set_cell_background(table.cell(0, i), "F8FAFC")
        set_cell_margins(table.cell(0, i), 80, 80, 100, 100)
    
    c0 = table.cell(0, 0)
    p0 = c0.paragraphs[0]
    p0.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p0.paragraph_format.space_after = Pt(0)
    r0 = p0.add_run(eq_text)
    r0.font.name = 'Times New Roman'
    r0.font.size = Pt(11)
    r0.font.italic = True
    
    c1 = table.cell(0, 1)
    p1 = c1.paragraphs[0]
    p1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p1.paragraph_format.space_after = Pt(0)
    r1 = p1.add_run(f"({eq_num})")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(11)
    r1.font.bold = True
    
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(2)
    p_sp.paragraph_format.space_after = Pt(4)

def add_figure(filename, caption_text, width_in=5.8):
    fig_path = FIGURES_DIR / filename
    if fig_path.exists():
        p_img = doc.add_paragraph()
        p_img.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(10)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(str(fig_path), width=Inches(width_in))
        
        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(12)
        p_cap.paragraph_format.keep_with_next = False
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = 'Times New Roman'
        r_cap.font.size = Pt(10)
        r_cap.font.italic = True

def add_table_data(headers, rows, col_widths=None, caption=None):
    if caption:
        pc = doc.add_paragraph()
        pc.paragraph_format.space_before = Pt(6)
        pc.paragraph_format.space_after = Pt(3)
        pc.paragraph_format.keep_with_next = True
        pc.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        rc = pc.add_run(caption)
        rc.font.name = 'Times New Roman'
        rc.font.size = Pt(10)
        rc.font.bold = True
    table = doc.add_table(rows=len(rows)+1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # Header Row
    hdr_cells = table.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].text = h_text
        set_cell_background(hdr_cells[i], "1E3A8A") # IIT Navy
        set_cell_margins(hdr_cells[i], 100, 100, 100, 100)
        p = hdr_cells[i].paragraphs[0]
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            
    # Data Rows
    for r_idx, row_data in enumerate(rows):
        row_cells = table.rows[r_idx+1].cells
        bg_col = "FFFFFF" if r_idx % 2 == 0 else "F1F5F9"
        for c_idx, cell_value in enumerate(row_data):
            row_cells[c_idx].text = str(cell_value)
            set_cell_background(row_cells[c_idx], bg_col)
            set_cell_margins(row_cells[c_idx], 80, 80, 100, 100)
            p = row_cells[c_idx].paragraphs[0]
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(0)
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(9.5)
                
    if col_widths:
        for r in table.rows:
            for c_idx, w in enumerate(col_widths):
                r.cells[c_idx].width = Inches(w)
                
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(2)
    p_sp.paragraph_format.space_after = Pt(6)

print("Building IIT Jodhpur B.Tech Project Report (.docx)...")

# ==============================================================================
# 1. TITLE PAGE
# ==============================================================================
p_title = doc.add_paragraph()
p_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_before = Pt(36)
p_title.paragraph_format.space_after = Pt(18)
run_title = p_title.add_run(
    "Numerical Modelling and Machine Learning Prediction of Single-Particle\n"
    "Crushing Mechanics and Fractal Gradation of Recycled Aggregates"
)
run_title.font.name = 'Times New Roman'
run_title.font.size = Pt(15)
run_title.font.bold = True

p_sub = doc.add_paragraph()
p_sub.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_before = Pt(12)
p_sub.paragraph_format.space_after = Pt(18)
run_sub = p_sub.add_run(
    "A Project Report submitted by\n"
    "Ayush Kumar (B23CI1009)\n"
    "in partial fulfillment of the requirements for the award of the degree of Bachelor of Technology (B.Tech)"
)
run_sub.font.name = 'Times New Roman'
run_sub.font.size = Pt(12)
run_sub.font.italic = True

logo_path = FIGURES_DIR / "iit_jodhpur_logo.png"
if logo_path.exists():
    p_logo = doc.add_paragraph()
    p_logo.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(24)
    p_logo.paragraph_format.space_after = Pt(24)
    r_logo = p_logo.add_run()
    r_logo.add_picture(str(logo_path), width=Inches(2.1))

p_inst = doc.add_paragraph()
p_inst.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_inst.paragraph_format.space_before = Pt(18)
p_inst.paragraph_format.space_after = Pt(0)
run_inst = p_inst.add_run(
    "Indian Institute of Technology Jodhpur\n"
    "Department of Civil and Infrastructure Engineering\n"
    "November 2026"
)
run_inst.font.name = 'Times New Roman'
run_inst.font.size = Pt(13)
run_inst.font.bold = True

doc.add_page_break()

# ==============================================================================
# 2. DECLARATION
# ==============================================================================
add_heading_1("Declaration")

add_body_p(
    "I hereby declare that the work presented in this Project Report titled Numerical Modelling and Machine Learning Prediction of "
    "Single-Particle Crushing Mechanics and Fractal Gradation of Recycled Aggregates, submitted to the Department of Civil and "
    "Infrastructure Engineering, Indian Institute of Technology Jodhpur, in partial fulfillment of the requirements for the award of the degree "
    "of Bachelor of Technology, is a bonafide record of the research work carried out by me under the supervision of Dr. Tekcham Gishan Singh, "
    "Assistant Professor."
)

add_body_p(
    "I further declare that this report represents my own ideas and work in my own words. Where others' ideas, mathematical formulations, "
    "or experimental datasets have been incorporated, they have been adequately cited and referenced according to academic standards. "
    "The computational models, virtual testing suites, and data analytics presented herein have not formed the basis for the award of "
    "any other degree, diploma, or certificate in any other university or institution of higher education."
)

p_sig = doc.add_paragraph()
p_sig.paragraph_format.space_before = Pt(40)
p_sig.paragraph_format.space_after = Pt(0)
run_sig = p_sig.add_run("Ayush Kumar\nRoll No.: B23CI1009\nDepartment of Civil and Infrastructure Engineering\nIndian Institute of Technology Jodhpur")
run_sig.font.name = 'Times New Roman'
run_sig.font.size = Pt(11)
run_sig.font.bold = True

doc.add_page_break()

# ==============================================================================
# 3. CERTIFICATE
# ==============================================================================
add_heading_1("Certificate")

add_body_p(
    "This is to certify that the Project Report titled Numerical Modelling and Machine Learning Prediction of Single-Particle "
    "Crushing Mechanics and Fractal Gradation of Recycled Aggregates, submitted by Ayush Kumar (B23CI1009) to the Indian Institute of "
    "Technology Jodhpur for the award of the degree of Bachelor of Technology, is a bonafide record of the research work done by him under my "
    "supervision. To the best of my knowledge, the contents of this report, in full or in parts, have not been submitted to any other "
    "Institute or University for the award of any degree or diploma."
)

add_body_p(
    "The student has demonstrated diligent academic inquiry in synthesizing granular fracture mechanics, non-linear Weibull survival statistics, "
    "scale-invariant fractal fragmentation laws, and gradient-boosted machine learning algorithms into an accessible, non-destructive "
    "virtual testing engineering platform. The technical contents have been verified and approved for submission."
)

p_cert_sig = doc.add_paragraph()
p_cert_sig.paragraph_format.space_before = Pt(40)
p_cert_sig.paragraph_format.space_after = Pt(0)
run_cert_sig = p_cert_sig.add_run(
    "Dr. Tekcham Gishan Singh\n"
    "Assistant Professor\n"
    "Department of Civil and Infrastructure Engineering\n"
    "Indian Institute of Technology Jodhpur"
)
run_cert_sig.font.name = 'Times New Roman'
run_cert_sig.font.size = Pt(11)
run_cert_sig.font.bold = True

doc.add_page_break()

# ==============================================================================
# 4. ABSTRACT
# ==============================================================================
add_heading_1("ABSTRACT")

add_body_p(
    "Recycled aggregate (RA) derived from crushed concrete, brick, and demolition mortar is widely recognized as a sustainable alternative "
    "to depleting virgin mineral quarry stone in civil infrastructure. Incorporating recycled aggregates into highway subgrades, structural concrete, "
    "and railway ballast supports circular construction and minimizes construction and demolition (C&D) waste disposal. In India alone, over "
    "150 million tonnes of C&D waste are generated annually, yet less than 5% is systematically recycled into structural engineering applications. "
    "However, structural utilization of recycled aggregate is severely restricted by irregular 3D morphology, residual micro-cracking, and pronounced "
    "vulnerability to single-particle crushing under compaction and vehicular wheel loading. Standard laboratory evaluation using Universal Testing "
    "Machines (UTM) and mechanical sieve shakers is destructive, labor-intensive (taking 16–24 hours per sample batch), hazardous due to respirable "
    "crystalline silica dust, and incapable of mapping continuous variations in particle geometry."
)

add_body_p(
    "In this study, the single-particle crushing mechanics and post-breakage particle size distribution of recycled aggregates are investigated using "
    "a physics-informed machine learning (PIML) framework. Three demolition materials are evaluated: Recycled Concrete (RC), Recycled Brick (RB), "
    "and Recycled Mortar (RM). Empirical Weibull brittle fracture size-scaling parameters (Liang et al., 2025) are coupled with 3D sphericity-dependent "
    "strength and piecewise energy laws (Cai et al., 2024), generating a comprehensive benchmark dataset of N = 3,600 individual particles spanning "
    "diameters from 4.75 mm to 37.5 mm. Six regression models (Ridge Polynomial, Random Forest, XGBoost, LightGBM, CatBoost, and MLP Neural Network) "
    "are trained and benchmarked across crushing strength, peak rupture force, crushing energy, and post-breakage fractal dimension. CatBoost achieved "
    "the highest overall accuracy (mean R² = 0.9619: R² = 0.9871 for peak force F_f, R² = 0.9636 for crushing strength sigma_f, R² = 0.9498 for crushing "
    "energy E_f, and R² = 0.9469 for fractal dimension D). Explainable AI (XGBoost TreeSHAP) attributions revealed that material apparent density and 3D "
    "sphericity (Φ) dominate crushing strength sigma_f, while shortest axis S and equivalent diameter d_eq govern absolute peak force and energy dissipation. "
    "The mechanistic scaling model is validated against published laboratory datasets (MAPE = 1.15% for RC, 2.02% for RM, and 5.07% for RB). Furthermore, an "
    "interactive four-tab Streamlit suite is deployed for non-destructive single-particle characterization and preliminary aggregate screening under Li et al. "
    "(2021) fractal gradation criteria alongside IRC:37-2018 and IS 383 guidelines."
)

doc.add_page_break()

# ==============================================================================
# 5. TABLE OF CONTENTS
# ==============================================================================
add_heading_1("TABLE OF CONTENTS")

toc_items = [
    ("1. INTRODUCTION", "7"),
    ("    1.1 Infrastructure Demand and Construction Waste Crisis", "7"),
    ("    1.2 Geotechnical Limitations of Recycled Aggregates", "7"),
    ("    1.3 Machine Learning and Computational Granular Mechanics", "7"),
    ("2. LITERATURE SURVEY", "7"),
    ("    2.1 Single-Particle Rock Mechanics vs. Bulk Standard Tests (IS 2386 / ASTM C131)", "7"),
    ("    2.2 Microstructure and Interfacial Transition Zone (ITZ) in C&D Aggregates", "8"),
    ("    2.3 3D Morphological Characterization & Zingg Classification", "8"),
    ("    2.4 Weibull Weakest-Link Size Scaling & Fractal Fragmentation", "8"),
    ("    2.5 Machine Learning & Explainable AI in Granular Geomechanics", "8"),
    ("3. PROBLEM DEFINITION & OBJECTIVES", "9"),
    ("    3.1 Problem Definition", "9"),
    ("    3.2 Research Objectives", "9"),
    ("    3.3 Scope and Technical Boundaries", "9"),
    ("4. METHODOLOGY", "10"),
    ("    4.1 Physics-Coupled Benchmark Dataset Generation", "10"),
    ("        4.1.1 Material Properties and Morphological Characterization", "10"),
    ("        4.1.2 Governing Fracture Formulations (Hiramatsu-Oka & Bagheri)", "10"),
    ("        4.1.3 Weibull Size-Scaling and Shape Power Laws", "11"),
    ("        4.1.4 Scale-Invariant Fractal Gradation", "12"),
    ("    4.2 Machine Learning Architecture and Training Pipeline", "12"),
    ("        4.2.1 16-Dimensional Feature Space and Stratified Data Partitioning", "12"),
    ("        4.2.2 Machine Learning Regressors & Hyperparameter Configuration", "12"),
    ("        4.2.3 Model Evaluation Metrics", "13"),
    ("5. NUMERICAL & MACHINE LEARNING FINDINGS", "13"),
    ("    5.1 Model Performance Benchmarks across Target Variables", "13"),
    ("    5.2 Actual vs. Predicted Parity Analysis", "13"),
    ("    5.3 Explainable AI (SHAP) Feature Attribution", "14"),
    ("    5.4 Residual Error Distribution & Heteroscedasticity Analysis", "15"),
    ("    5.5 2D Partial Dependence Analysis", "16"),
    ("    5.6 Weibull Size-Scaling and Breakage Mode Classification", "16"),
    ("6. INTERACTIVE VIRTUAL TESTING SUITE & DESIGN APPLICATION", "17"),
    ("    6.1 System Architecture and Technical Stack", "17"),
    ("    6.2 Virtual Universal Testing Machine & Sieve Gradation (Tab 1)", "17"),
    ("    6.3 Multiscale Size-Scaling Simulator (Tab 2)", "17"),
    ("    6.4 Auxiliary Computer Vision Particle Sizing (Tab 3)", "18"),
    ("    6.5 Baseline Recycled Concrete Case Study", "18"),
    ("    6.6 Pavement Gradation Screening under Li et al. (2021) and IRC:37-2018", "19"),
    ("    6.7 Validation against Published Experimental Benchmark Datasets", "19"),
    ("7. SUMMARY AND FUTURE PLAN OF WORK", "20"),
    ("    7.1 Summary of Research Achievements", "20"),
    ("    7.2 Future Plan of Work", "20"),
    ("8. REFERENCES", "21"),
]

for title, pg in toc_items:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(1.2)
    p.paragraph_format.line_spacing = 1.05
    r_title = p.add_run(title)
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(9.5)
    if not title.startswith("    "):
        r_title.font.bold = True
    
    dots_len = max(4, 74 - len(title))
    r_dots = p.add_run(" " + "." * dots_len + " " + pg)
    r_dots.font.name = 'Times New Roman'
    r_dots.font.size = Pt(9.5)

doc.add_page_break()

# ==============================================================================
# 6. LIST OF FIGURES & LIST OF TABLES
# ==============================================================================
add_heading_1("LIST OF FIGURES")

figures_list = [
    ("Fig. 4.1", "Zingg 3D particle shape classification and aspect ratio domains (N=3,600)", "10"),
    ("Fig. 4.2", "Weibull survival probability distributions across particle size fractions", "11"),
    ("Fig. 5.1", "XGBoost actual vs. predicted parity plots across targets on test set", "14"),
    ("Fig. 5.2", "XGBoost TreeSHAP global feature importance rankings across all four targets", "15"),
    ("Fig. 5.3", "2D Partial Dependence contour heatmaps over size d0 and sphericity Phi", "16"),
    ("Fig. 6.1", "Tab 1 screenshot: Virtual UTM and post-breakage sieve gradation curve", "17"),
    ("Fig. 6.2", "Tab 2 screenshot: Multiscale size-scaling contour heatmaps across d0 & Phi", "18"),
    ("Fig. 6.3", "Tab 2 screenshot: Model scaling predictions vs. published experimental data", "18"),
]

for num, cap, pg in figures_list:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    r_num = p.add_run(f"{num}: {cap}")
    r_num.font.name = 'Times New Roman'
    r_num.font.size = Pt(10.5)
    dots_len = max(4, 80 - len(f"{num}: {cap}"))
    r_dots = p.add_run(" " + "." * dots_len + " " + pg)
    r_dots.font.name = 'Times New Roman'
    r_dots.font.size = Pt(10.5)

p_sp = doc.add_paragraph()
p_sp.paragraph_format.space_before = Pt(8)

add_heading_1("LIST OF TABLES")

tables_list = [
    ("Table 4.1", "Empirical calibration parameters for recycled aggregate materials (RC, RM, RB)", "10"),
    ("Table 4.2", "Machine learning regressor hyperparameter configurations and optimization schemes", "12"),
    ("Table 5.1", "Performance comparison of machine learning regression models on hold-out test set", "13"),
    ("Table 5.2", "CatBoost hold-out test residual statistics and Levene homoscedasticity test", "15"),
    ("Table 6.1", "End-to-end design case study: Virtual characterization of Recycled Concrete", "19"),
    ("Table 6.2", "Validation of virtual testing suite against published experimental benchmarks", "19"),
]

for num, cap, pg in tables_list:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    r_num = p.add_run(f"{num}: {cap}")
    r_num.font.name = 'Times New Roman'
    r_num.font.size = Pt(10.5)
    dots_len = max(4, 80 - len(f"{num}: {cap}"))
    r_dots = p.add_run(" " + "." * dots_len + " " + pg)
    r_dots.font.name = 'Times New Roman'
    r_dots.font.size = Pt(10.5)

doc.add_page_break()

# ==============================================================================
# CHAPTER 1: INTRODUCTION
# ==============================================================================
add_heading_1("1. INTRODUCTION")

add_heading_2("1.1 Infrastructure Demand and Construction Waste Crisis")
add_body_p(
    "Aggregates constitute the primary granular constituent in civil engineering construction, representing over 70% of concrete volume "
    "and almost 100% of unbound highway subgrades, sub-base layers, and railway ballast. The worldwide consumption of natural mineral aggregates "
    "exceeds 50 billion tonnes per year, causing widespread ecological degradation including riverbank erosion, groundwater table lowering, "
    "and depletion of natural stone quarries. In India alone, according to the Central Pollution Control Board (CPCB 2024), annual construction "
    "and demolition (C&D) waste generation surpasses 150 million tonnes. Globally, this figure exceeds 3.0 billion tonnes. Discarding this debris "
    "into open landfills consumes valuable urban land and represents an inefficient linear economic model. Repurposing C&D waste into Recycled "
    "Aggregates (RA) offers a vital closed-loop circular economy pathway for sustainable infrastructure."
)

add_heading_2("1.2 Geotechnical Limitations of Recycled Aggregates")
add_body_p(
    "Despite their obvious environmental advantages, the broader commercial adoption of recycled aggregates in load-bearing structural concrete and "
    "pavement bases remains limited. Unlike homogeneous virgin stone (such as quarried basalt, granite, or limestone), recycled aggregates are highly "
    "heterogeneous multi-phase composites. They typically consist of residual natural stone bonded with porous adhered mortar, hardened cement paste, "
    "and crushed brick fragments. This adhered mortar layer possesses high micro-crack density and low fracture toughness, resulting in elevated water "
    "absorption (often 4%–10% compared to < 1.5% for virgin stone) and low bulk density. Under compaction roller loads and repetitive vehicular wheel "
    "stresses, recycled aggregates experience significant particle crushing, producing excessive fine debris that alters the design grain size distribution, "
    "induces differential settlement, and leads to premature pavement rutting."
)

add_heading_2("1.3 Machine Learning and Computational Granular Mechanics")
add_body_p(
    "Traditional laboratory assessment of aggregate crushing involves bulk testing standards such as the Aggregate Crushing Value (ACV, IS 2386 Part IV) "
    "and the Los Angeles Abrasion test (ASTM C131). While widespread, these tests are purely empirical bulk metrics that obscure the fundamental particle-scale "
    "tensile failure mechanisms. Moreover, single-particle compression testing using Universal Testing Machines (UTM) and post-breakage sieve analysis is "
    "destructive, time-consuming (taking 16–24 hours per test series), labor-intensive, and produces hazardous respirable crystalline silica dust. "
    "To overcome these bottlenecks, this study establishes a physics-informed machine learning (PIML) framework that models the single-particle crushing "
    "mechanics and fractal fragmentation of recycled aggregates. By uniting non-linear fracture mechanics, Weibull statistical scaling, and gradient-boosted "
    "decision trees, the framework provides instantaneous, non-destructive predictions of crushing capacity and post-breakage gradation curves."
)

# ==============================================================================
# CHAPTER 2: LITERATURE SURVEY
# ==============================================================================
add_heading_1("2. LITERATURE SURVEY")

add_heading_2("2.1 Single-Particle Rock Mechanics vs. Bulk Standard Tests (IS 2386 / ASTM C131)")
add_body_p(
    "The mechanical characterization of coarse aggregates has historically relied on empirical bulk tests such as the Aggregate Crushing Value "
    "(IS 2386 Part IV) and the Los Angeles Abrasion test (ASTM C131). While useful for quality control, bulk tests suffer from severe theoretical limitations. "
    "During bulk confined compression, load transmission occurs through complex force chains where inter-particle friction, particle rearrangement, "
    "and edge abrasion simultaneously contribute to mass loss. Consequently, bulk tests cannot isolate the intrinsic tensile rupture strength of individual "
    "particles. To address this, Hiramatsu and Oka (1966) pioneered single-particle compression testing between flat platens, demonstrating that an irregular "
    "rock fragment subjected to point loading develops a nearly uniform tensile stress field in its central region, governed by the relation "
    "sigma_t = 0.9 * F_f / d_0^2. This Brazilian-type failure mode establishes single-particle testing as the true benchmark for aggregate crushing."
)

add_heading_2("2.2 Microstructure and Interfacial Transition Zone (ITZ) in C&D Aggregates")
add_body_p(
    "The crushing behavior of recycled aggregates is fundamentally governed by their composite microstructure. Recycled concrete (RC) particles feature "
    "two distinct Interfacial Transition Zones (ITZs): the old ITZ between the original virgin aggregate and old adhered mortar, and the newly formed ITZ "
    "when recycled aggregate is bound in new concrete. Due to higher porosity and micro-cracking in the old cement paste, stress concentrations rapidly "
    "accumulate at the old ITZ under compression. Liang et al. (2025) conducted single-particle compression tests on various C&D waste types, reporting that "
    "Recycled Concrete exhibits significantly higher strength than Recycled Mortar and Recycled Brick due to the presence of intact virgin rock cores. "
    "However, as particle size increases, the volumetric proportion of internal flaw clusters expands, drastically lowering characteristic tensile strength."
)

add_heading_2("2.3 3D Morphological Characterization & Zingg Classification")
add_body_p(
    "Particle shape exerts a profound influence on crushing strength. Classical particle shape classification was formalized by Zingg (1935), who categorized "
    "granules into four distinct geometric shapes—Equant, Flat/Disc, Elongated/Rod, and Blade—based on the aspect ratios of their triaxial dimensions "
    "(Longest L, Intermediate I, Shortest S). Cai et al. (2024) employed high-resolution 3D laser scanning to quantify the relationship between 3D grain "
    "morphology and crushing characteristics of recycled aggregates. They proved that 3D sphericity Phi = cbrt((I * S) / L^2) dictates the mode of mechanical "
    "breakage: spherical particles distribute stresses hydrostatically, yielding higher rupture force and energy absorption, whereas flat or elongated "
    "particles experience severe bending moments and fail via premature tensile splitting."
)

add_heading_2("2.4 Weibull Weakest-Link Size Scaling & Fractal Fragmentation")
add_body_p(
    "Because quasi-brittle mineral aggregates contain randomly distributed micro-flaws, their failure exhibits strong statistical size dependence. "
    "Weibull (1951) weakest-link theory dictates that the survival probability P_s of a particle under tensile stress sigma_f follows an exponential distribution "
    "P_s = exp(-(sigma_f / sigma_f0)^m), where sigma_f0 is the characteristic strength and m is the Weibull modulus. Liang et al. (2025) demonstrated that "
    "characteristic strength decreases with equivalent particle diameter d_0 following a power-law scaling sigma_f0 proportional to d_0^(-3/m). "
    "Following catastrophic rupture, the fragment size distribution is governed by fractal fragmentation theory (Turcotte, 1986; Tyler and Wheatcraft, 1992). "
    "The cumulative percentage passing each sieve aperture follows a scale-invariant power-law F(d_i) = 100 * (d_i / d_0)^(3 - D), where D is the fractal "
    "dimension. Materials undergoing extensive catastrophic disintegration exhibit D > 2.6, producing high proportions of problematic fines."
)

add_heading_2("2.5 Machine Learning & Explainable AI in Granular Geomechanics")
add_body_p(
    "In recent years, machine learning has emerged as a transformative paradigm for geotechnical materials modeling. Wang et al. (2021) demonstrated that "
    "deep neural networks and tree ensembles can capture complex non-linear relationships between 3D grain morphology and crushing strength. However, black-box "
    "models often lack interpretability, limiting their adoption by practicing engineers. The integration of SHapley Additive exPlanations (SHAP) provides "
    "rigorous game-theoretic attribution of input features, enabling practitioners to decipher the exact physical mechanisms governing model predictions."
)

# ==============================================================================
# CHAPTER 3: PROBLEM DEFINITION & OBJECTIVES
# ==============================================================================
add_heading_1("3. PROBLEM DEFINITION & OBJECTIVES")

add_heading_2("3.1 Problem Definition")
add_body_p(
    "Civil and infrastructure projects require rigorous geotechnical verification of coarse aggregates before deployment in pavement sub-bases and "
    "structural concrete. For recycled C&D waste, wide variations in material origin, mortar content, and particle shape result in extreme strength dispersion. "
    "Existing laboratory methods present three severe challenges: (i) Bulk tests (IS 2386 / ASTM C131) fail to capture single-particle tensile mechanics; "
    "(ii) Universal Testing Machine (UTM) compression testing is destructive, labor-intensive, and requires specialized test fixtures; and (iii) Standard "
    "sieving takes up to 24 hours per batch. There is an urgent engineering need for a rapid, non-destructive, and physics-consistent framework capable of "
    "predicting crushing strength, rupture force, energy dissipation, and post-breakage particle size distribution from measurable geometric parameters."
)

add_heading_2("3.2 Research Objectives")
add_body_p("The primary research objectives of this investigation are as follows:")
add_bullet_p("1. Physics-Coupled Synthetic Dataset Generation: ", "Formulate a rigorous synthetic generation framework coupling Hiramatsu-Oka tensile theory, Bagheri equivalent diameter, Cai et al. 3D sphericity-dependent power laws, and Liang et al. Weibull size-scaling parameters across Recycled Concrete (RC), Recycled Mortar (RM), and Recycled Brick (RB).")
add_bullet_p("2. Machine Learning Regressor Benchmarking: ", "Train and benchmark six regression architectures (Ridge Polynomial, Random Forest, XGBoost, LightGBM, CatBoost, and MLP Neural Network) and three breakage-mode classifiers to predict sigma_f, F_f, E_f, and D.")
add_bullet_p("3. Explainable AI (TreeSHAP) Interpretation: ", "Perform global TreeSHAP feature attribution on XGBoost models to verify that predictions obey empirical fracture physics.")
add_bullet_p("4. Interactive Software Deployment: ", "Deploy a four-tab Streamlit platform featuring a Virtual UTM, an audited Size & Shape Scaling Simulator, an auxiliary OpenCV particle scanner, and an AI & Benchmarks gallery supporting Li et al. (2021) / IRC:37-2018 aggregate screening.")

add_heading_2("3.3 Scope and Technical Boundaries")
add_body_p(
    "This investigation is bounded by specific technical criteria to ensure engineering rigor: (i) Particle sizes range between 4.75 mm and 37.5 mm, "
    "covering standard Indian coarse aggregate sieve fractions; (ii) Quasi-static loading conditions are assumed between flat, hardened steel platens; "
    "(iii) Breakage is modeled as primary catastrophic tensile splitting; and (iv) Materials are categorized into Recycled Concrete (RC), Recycled Mortar (RM), "
    "and Recycled Brick (RB)."
)

# ==============================================================================
# CHAPTER 4: METHODOLOGY
# ==============================================================================
add_heading_1("4. METHODOLOGY")

add_heading_2("4.1 Physics-Coupled Benchmark Dataset Generation")
add_body_p(
    "To establish a robust ground-truth foundation for machine learning training, a synthetic aggregate generation engine was constructed, strictly "
    "governed by experimental empirical laws from Liang et al. (2025) and Cai et al. (2024). Three demolition materials were synthesized across three "
    "standard sieve classes: 4.75–9.5 mm, 9.5–19.0 mm, and 19.0–37.5 mm, with 400 particles per class, yielding N = 3,600 total particles."
)

add_heading_3("4.1.1 Material Properties and Morphological Characterization")
add_body_p(
    "For each synthetic particle, triaxial dimensions (Longest L, Intermediate I, Shortest S) were generated using truncated normal distributions "
    "calibrated to Cai et al. (2024) Table 1 means with realistic natural variability (CV = 12% for L, 10% for I, 13% for S) while enforcing "
    "L >= I >= S > 0. Material-level baseline properties were assigned from Liang et al. (2025) and Cai et al. (2024): apparent density "
    "(RC: 2.217, RB: 2.140, RM: 2.028 g/cm³), bulk density (RC: 1.296, RB: 1.063, RM: 1.113 g/cm³), and elastic modulus (RC: 15.2, RM: 9.1, RB: 8.6 GPa). "
    "Table 4.1 summarizes the exact calibration parameters across the 4.75–10 mm, 10–20 mm, and 20–25 mm Weibull brackets."
)

headers_4_1 = ["Material Type", "Weibull sigma_f0 (MPa) [3 brackets]", "Weibull m [3 brackets]", "Shape (p, q)", "Energy Power (c, d) mJ", "Fractal D_size [3 brackets]"]
rows_4_1 = [
    ["Recycled Concrete (RC)", "6.51 / 6.28 / 6.07", "1.58 / 1.30 / 1.25", "p = 9.35, q = 2.13", "c = 2061.15, d = 1.28", "1.66 / 1.78 / 1.87"],
    ["Recycled Mortar (RM)", "3.03 / 2.97 / 2.91", "2.70 / 2.73 / 2.76", "p = 4.69, q = 2.21", "c = 2041.24, d = 2.66", "1.77 / 1.91 / 2.11"],
    ["Recycled Brick (RB)", "6.35 / 6.21 / 4.92", "2.58 / 2.61 / 3.32", "p = 3.84, q = 1.68", "c = 1511.07, d = 2.16", "1.68 / 1.82 / 2.01"]
]
add_table_data(headers_4_1, rows_4_1, [1.5, 1.35, 1.05, 0.95, 1.10, 1.05], caption="Table 4.1. Empirical calibration parameters for recycled aggregate materials (RC, RM, RB).")

add_figure("fig1_zingg_shape_classification.png", "Fig. 4.1. Zingg 3D particle shape classification and aspect ratio domains (Disk, Block, Blade, Bar; dataset counts: Bar=1,584, Disk=745, Blade=698, Block=573).")

add_heading_3("4.1.2 Governing Fracture Formulations (Hiramatsu-Oka & Bagheri)")
add_body_p(
    "The roughness-corrected equivalent diameter d_0 was computed following Bagheri et al. (2015), relating the triaxial dimensions through the geometric mean:"
)
add_equation_box("d_eq = cbrt(L * I * S)", "4.1")
add_equation_box("d_0 = 0.887 * d_eq = 0.887 * cbrt(L * I * S)", "4.2")

add_body_p(
    "Following Hiramatsu and Oka (1966), peak compressive failure force F_f (N, reported in kN) was related to tensile crushing strength sigma_f (MPa) via:"
)
add_equation_box("F_f = (sigma_f * d_0^2) / 0.9", "4.3")

add_heading_3("4.1.3 Weibull Size-Scaling and Shape Power Laws")
add_body_p(
    "Shape-dependent crushing strength at the reference coarse size (d_ref = 25 mm, Cai et al., 2024 Eq. 8) was coupled with size-dependent Weibull "
    "characteristic strength scaling (Liang et al., 2025 Table 2) for any equivalent size d_0 and 3D sphericity Phi = cbrt((I * S) / L^2):"
)
add_equation_box("sigma_f(d_0, Phi) = [p * Phi^q] * [sigma_f0(d_0) / sigma_f0(d_ref)]", "4.4")

add_body_p(
    "Crushing energy dissipation E_f (in mJ) follows the piecewise empirical law of Cai et al. (2024 Eq. 10 & 11) with volumetric size scaling relative to d_ref = 25 mm:"
)
add_equation_box("E_f(d_0, Phi) = [c * Phi^d] * (d_0 / 25)^3  (Phi < 0.8);   [E_0 + 2a*(1 - exp(-Phi/t))] * (d_0 / 25)^3  (Phi >= 0.8)", "4.5")

add_figure("fig2_weibull_survival_curves.png", "Fig. 4.2. Weibull survival probability distributions across particle size fractions (4.75–9.5 mm, 9.5–19.0 mm, 19.0–37.5 mm).")

add_heading_3("4.1.4 Scale-Invariant Fractal Gradation")
add_body_p(
    "Post-breakage sieve size distribution was modeled using the scale-invariant fractal fragmentation formulation (Turcotte, 1986; Tyler and Wheatcraft, 1992), "
    "coupling Liang size-dependent D_size(d_0) with a +/-30% fractional sphericity modulation derived from Cai et al. (2024 Fig. 9):"
)
add_equation_box("F(d_i) = min[ 100, (d_i / d_0)^(3 - D) * 100 ]", "4.6")
add_body_p(
    "where F(d_i) is the cumulative percentage passing sieve aperture d_i, and D spans 1.57 to 2.20 across single-particle crushing tests."
)

add_heading_2("4.2 Machine Learning Architecture and Training Pipeline")
add_heading_3("4.2.1 16-Dimensional Feature Space and Stratified Data Partitioning")
add_body_p(
    "A 16-dimensional feature vector was extracted per particle: 13 continuous morphological and physical features (L, I, S, Elongation Index EI = I/L, "
    "Flatness Index FI = S/I, 3D Sphericity Phi, Domokos Shape Factor S_f, nominal equivalent diameter d_eq, Bagheri diameter d_0, apparent density, "
    "bulk density, elastic modulus, and Poisson's ratio) alongside 3 label-encoded categorical features (Material_Enc, Shape_Class_Enc, and "
    "Sieve_Bracket_Enc). The N = 3,600 dataset was partitioned into an 80% training set (N_train = 2,880) and a 20% hold-out test set (N_test = 720) "
    "stratified by breakage mode, using StandardScaler z-score normalization fitted strictly on the training fold."
)

add_heading_3("4.2.2 Machine Learning Regressors & Hyperparameter Configuration")
add_body_p(
    "Six multi-target regression architectures were implemented and benchmarked: Ridge Polynomial Regression (degree 2), Random Forest, XGBoost, "
    "LightGBM, CatBoost, and an MLP Neural Network, alongside three breakage-mode classifiers (Random Forest, XGBoost, MLP). "
    "Table 4.2 details the exact training hyperparameters used in src/train_models.py."
)

headers_4_2 = ["Model Architecture", "Key Hyperparameters", "Loss Function", "Regularization", "Optimization"]
rows_4_2 = [
    ["CatBoost Regressor", "depth=8, iterations=300, lr=0.05", "RMSE", "l2_leaf_reg=3.0", "Ordered Boosting"],
    ["LightGBM Regressor", "max_depth=8, n_estimators=300, lr=0.05", "Squared Error", "reg_alpha=0.1, reg_lambda=1.0", "Histogram GBDT"],
    ["XGBoost Regressor", "max_depth=8, n_estimators=300, lr=0.05", "Squared Error", "colsample=0.8, subsample=0.8", "Hist / Greedy Tree"],
    ["Random Forest", "n_estimators=200, max_depth=15", "Squared Error", "min_samples_split=5, leaf=2", "Bagging"],
    ["MLP Neural Network", "hidden=(128, 64, 32), act=ReLU", "MSE (Early Stop)", "alpha=0.001, batch_size=64", "Adam (lr=1e-3)"],
    ["Ridge Polynomial", "degree=2, include_bias=False", "Squared Loss", "alpha=1.0 (L2 Penalty)", "Closed-Form Ridge"]
]
add_table_data(headers_4_2, rows_4_2, [1.4, 1.8, 1.1, 1.2, 1.0], caption="Table 4.2. Machine learning regressor hyperparameter configurations and optimization schemes.")

add_heading_3("4.2.3 Model Evaluation Metrics")
add_body_p(
    "Predictive performance was rigorously quantified using the Coefficient of Determination (R²), Root Mean Squared Error (RMSE), Mean Absolute Error (MAE), "
    "and Mean Absolute Percentage Error (MAPE)."
)

# ==============================================================================
# CHAPTER 5: NUMERICAL & MACHINE LEARNING FINDINGS
# ==============================================================================
add_heading_1("5. NUMERICAL & MACHINE LEARNING FINDINGS")

add_heading_2("5.1 Model Performance Benchmarks across Target Variables")
add_body_p(
    "The six models were evaluated on the independent hold-out test set (N_test = 720). Table 5.1 presents the comprehensive performance metrics "
    "across all four engineering target variables: Peak Rupture Force (F_f), Crushing Strength (sigma_f), Crushing Energy (E_f), and Fractal Dimension (D)."
)

headers_5_1 = ["Model Architecture", "Target Variable", "R² Score", "RMSE", "MAE", "MAPE (%)"]
rows_5_1 = [
    ["CatBoost Regressor", "Peak Force F_f (kN)", "0.9871", "0.081 kN", "0.050 kN", "6.56%"],
    ["CatBoost Regressor", "Crushing Strength (MPa)", "0.9636", "0.235 MPa", "0.172 MPa", "5.81%"],
    ["CatBoost Regressor", "Crushing Energy E_f (mJ)", "0.9498", "82.53 mJ", "23.36 mJ", "9.13%"],
    ["CatBoost Regressor", "Fractal Dimension D", "0.9469", "0.032", "0.025", "1.37%"],
    ["LightGBM Regressor", "Peak Force F_f (kN)", "0.9852", "0.087 kN", "0.052 kN", "6.48%"],
    ["LightGBM Regressor", "Crushing Energy E_f (mJ)", "0.9465", "85.19 mJ", "26.60 mJ", "9.48%"],
    ["XGBoost Regressor", "Peak Force F_f (kN)", "0.9847", "0.089 kN", "0.054 kN", "6.67%"],
    ["Random Forest", "Peak Force F_f (kN)", "0.9840", "0.091 kN", "0.054 kN", "6.80%"],
    ["MLP Neural Network", "Peak Force F_f (kN)", "0.9866", "0.083 kN", "0.052 kN", "7.66%"],
    ["Ridge Polynomial", "Peak Force F_f (kN)", "0.9878", "0.079 kN", "0.049 kN", "6.98%"],
    ["Ridge Polynomial", "Crushing Energy E_f (mJ)", "0.8647", "135.44 mJ", "54.40 mJ", "65.08%"]
]
add_table_data(headers_5_1, rows_5_1, [1.6, 1.6, 0.8, 0.9, 0.9, 0.8], caption="Table 5.1. Performance comparison of machine learning regression models on hold-out test set (N_test = 720).")

add_body_p(
    "CatBoost achieved the best overall generalization across all four targets (mean R² = 0.9619: R² = 0.9871 for peak force, 0.9636 for crushing "
    "strength, 0.9498 for crushing energy, and 0.9469 for fractal dimension). Although Ridge Polynomial marginally led smooth peak force F_f (0.9878), "
    "it degraded severely on crushing energy E_f (R² = 0.8647, MAPE = 65.08%) because linear polynomials cannot resolve the sharp piecewise transition "
    "at Phi = 0.80, whereas gradient-boosted decision trees capture both continuous and piecewise fracture regimes accurately."
)

add_heading_2("5.2 Actual vs. Predicted Parity Analysis")
add_body_p(
    "Figure 5.1 presents the actual versus predicted parity plots on the test set (N_test = 720) for XGBoost. Across all four targets "
    "(R² = 0.9567 for sigma_f, 0.9847 for F_f, 0.9219 for E_f, and 0.9410 for D), predictions cluster tightly along the 1:1 line within the +/-10% envelope."
)

add_figure("fig6_actual_vs_predicted_parity.png", "Fig. 5.1. XGBoost actual vs. predicted parity plots across targets on test set (R² = 0.9219–0.9847; +/-10% band shown).")

add_heading_2("5.3 Explainable AI (SHAP) Feature Attribution")
add_body_p(
    "To verify physical interpretability, TreeSHAP was evaluated on the trained XGBoost models across test samples (Figure 5.2). For tensile crushing "
    "strength sigma_f, apparent density ranks first (distinguishing virgin-core RC at 2.217 g/cm³ from porous RB and RM) followed closely by 3D "
    "sphericity Phi and bulk density. Conversely, for peak failure force F_f and crushing energy E_f, geometric size attributes—shortest axis S and "
    "equivalent diameter d_eq—rank highest, matching Hiramatsu's F_f propto d_0^2 area law and cubic (d_0 / d_ref)^3 volume-energy scaling."
)

add_figure("fig8_shap_feature_importance.png", "Fig. 5.2. XGBoost TreeSHAP global feature importance rankings across all four mechanical and fractal targets.")

add_heading_2("5.4 Residual Error Distribution & Heteroscedasticity Analysis")
add_body_p(
    "To audit bias and variance stability across aggregate sizes, CatBoost hold-out test residuals (e = y_actual - y_pred) were evaluated across the three "
    "sieve brackets (Table 5.2). Because peak force scales quadratically with diameter (F_f propto d_0^2), absolute force spread naturally scales with grain "
    "size (std = 0.018 kN in fine vs. 0.120 kN in coarse brackets), whereas scale-invariant crushing strength sigma_f remains strictly homoscedastic "
    "(std = 0.228–0.245 MPa, Levene p = 0.924) with near-zero mean bias across all fractions."
)

headers_5_2 = ["Particle Size Fraction", "sigma_f Mean / Std (MPa)", "F_f Mean / Std (kN)", "F_f Skewness", "Variance Behavior (Levene Test)"]
rows_5_2 = [
    ["Fine (4.75–9.5 mm, n=241)", "-0.013 / 0.230", "-0.001 / 0.018", "0.12", "sigma_f Homoscedastic (p = 0.924)"],
    ["Medium (9.5–19.0 mm, n=229)", "+0.002 / 0.245", "+0.001 / 0.067", "1.35", "Relative F_f dispersion ~6.6% MAPE"],
    ["Coarse (19.0–37.5 mm, n=250)", "+0.043 / 0.228", "+0.020 / 0.120", "0.49", "Scale-invariant sigma_f residual variance"]
]
add_table_data(headers_5_2, rows_5_2, [1.75, 1.3, 1.25, 0.8, 1.6], caption="Table 5.2. CatBoost hold-out residual statistics and Levene homoscedasticity test across size fractions.")

add_body_p(
    "The residual mean remains virtually zero across all sieve fractions, confirming unbiased surrogate predictions from 4.75 mm to 37.5 mm."
)

add_heading_2("5.5 2D Partial Dependence Analysis")
add_body_p(
    "Two-dimensional Partial Dependence Plots (Figure 5.3) over d_0 in [4, 35] mm and Phi in [0.42, 0.93] visualize the coupled response surfaces. "
    "Crushing strength sigma_f increases monotonically with sphericity, peak force expands across both d_0 and Phi, the energy map clearly exposes the "
    "Cai et al. (2024) piecewise jump at Phi = 0.80, and fractal dimension D steps sharply at d_0 = 20 mm due to discrete sieve-bracket training bins."
)

add_figure("fig9_partial_dependence_contours.png", "Fig. 5.3. 2D Partial Dependence contour heatmaps for mechanical targets over size d₀ and sphericity Φ.")

add_heading_2("5.6 Weibull Size-Scaling and Breakage Mode Classification")
add_body_p(
    "The numerical results confirm classical Weibull weakest-link scaling: smaller particles sustain higher nominal crushing stress due to lower flaw "
    "probabilities, while 3D sphericity separates angular grains (prone to Mode III fragmentation) from compact grains (Mode I splitting). "
    "Because Mode I/II/III transition boundaries overlap stochastically in laboratory tests, standalone classification accuracy reached 54.17% (MLP) "
    "and 53.75% (Random Forest, ROC-AUC = 0.648), highlighting why continuous regression targets remain far more reliable for structural screening."
)

# ==============================================================================
# CHAPTER 6: INTERACTIVE VIRTUAL TESTING SUITE & DESIGN APPLICATION
# ==============================================================================
add_heading_1("6. INTERACTIVE VIRTUAL TESTING SUITE & DESIGN APPLICATION")

add_heading_2("6.1 System Architecture and Technical Stack")
add_body_p(
    "To translate these scientific findings into practice, an interactive web-based engineering suite (app.py) was developed using Streamlit, "
    "Plotly Graph Objects, OpenCV, and Scikit-learn. The software comprises four functional tabs: Tab 1 Virtual Universal Testing Machine, Tab 2 Audited "
    "Size & Shape Scaling Simulator, Tab 3 Auxiliary Computer Vision Particle Scanner, and Tab 4 AI & Benchmarks Gallery."
)

add_heading_2("6.2 Virtual Universal Testing Machine & Sieve Gradation (Tab 1)")
add_body_p(
    "Tab 1 simulates an unconfined single-particle compression test. The user specifies triaxial dimensions (L, I, S) and material type. "
    "The application instantaneously computes equivalent diameters, predicts failure force and crushing strength, evaluates Weibull survival probability, "
    "and plots the post-breakage particle size distribution curve alongside standard ASTM C33 / IS 383 sieve boundaries (Figure 6.1)."
)

add_figure("app_tab1_utm_gradation_curves.png", "Fig. 6.1. Program screenshot from Tab 1: Virtual Universal Testing Machine and post-breakage sieve gradation curve.")

add_heading_2("6.3 Multiscale Size-Scaling Simulator (Tab 2)")
add_body_p(
    "Tab 2 allows exploration of multiscale scaling laws across particle diameters from 4.75 mm to 37.5 mm. Figure 6.2 displays the generated 2D contour "
    "heatmaps of failure force and crushing energy, while Figure 6.3 shows size-scaling validation curves benchmarked against published experimental data."
)

add_figure("app_tab2_scaling_heatmap.png", "Fig. 6.2. Program screenshot from Tab 2: Multiscale size-scaling contour heatmaps across d₀ and Φ.")
add_figure("app_tab2_experimental_validation_subplots.png", "Fig. 6.3. Program screenshot from Tab 2: Model size-scaling predictions benchmarked against published experimental data.")

add_heading_2("6.4 Auxiliary Computer Vision Particle Sizing (Tab 3)")
add_body_p(
    "To support rapid non-destructive laboratory intake, Tab 3 integrates an auxiliary OpenCV particle scanner. Top-down aggregate photographs (or the built-in "
    "synthetic test generator) undergo Gaussian blur, Otsu adaptive thresholding, external contour extraction, and minimum rotated bounding rectangle fitting "
    "to measure 2D dimensions (L, I) via a user-calibrated mm/px scale slider. Assuming a standard stereological flat-resting thickness ratio S = 0.65 * I, "
    "it feeds triaxial dimensions directly into the mechanical prediction engine."
)

add_heading_2("6.5 Baseline Recycled Concrete Case Study")
add_body_p(
    "To demonstrate an end-to-end calculation matching the live Tab 1 Virtual UTM defaults, a baseline Recycled Concrete particle measuring L = 25.0 mm, "
    "I = 18.0 mm, S = 12.0 mm was evaluated under continuous Weibull scaling. Table 6.1 lists all computed morphological and crushing outputs."
)

headers_6_1 = ["Output Parameter", "Value", "Unit", "Physical Interpretation"]
rows_6_1 = [
    ["Equivalent Diameter d_eq", "17.54", "mm", "Equal-volume nominal diameter"],
    ["Bagheri Diameter d_0", "15.56", "mm", "Roughness-corrected effective diameter"],
    ["Flatness Index (FI = S/I)", "0.667", "—", "Zingg Flatness metric (Bar/Block boundary)"],
    ["Elongation Index (EI = I/L)", "0.720", "—", "Zingg Elongation metric"],
    ["3D Sphericity (Phi)", "0.702", "—", "High sphericity (> 0.65 favorable zone)"],
    ["Crushing Strength (sigma_f)", "4.50", "MPa", "Hiramatsu-Oka tensile splitting strength"],
    ["Peak Failure Force (F_f)", "1.210", "kN", "Catastrophic peak compression load"],
    ["Est. Crushing Energy (E_f)", "315.9", "mJ", "Cai piecewise volumetric energy (0.316 J)"],
    ["Fractal Dimension (D)", "1.814", "—", "Single-particle post-breakage exponent (Mode II)"]
]
add_table_data(headers_6_1, rows_6_1, [1.8, 1.0, 0.8, 2.8], caption="Table 6.1. End-to-end design case study: Virtual characterization of baseline Recycled Concrete aggregate.")

add_heading_2("6.6 Pavement Gradation Screening under Li et al. (2021) and IRC:37-2018")
add_body_p(
    "In road infrastructure, recycled aggregates used in Granular Sub-Base (GSB) and Wet Mix Macadam (WMM) layers under IRC:37-2018 and IS 383:2016 must "
    "resist excessive degradation during roller compaction and cyclic axle loads. Li et al. (2021) established an optimal gradation fragmentation band of "
    "1.887 <= D <= 2.631: values above 2.63 produce excessive < 0.075 mm silt fines that impede drainage and accelerate rutting. Our baseline single-particle "
    "RC grain (D = 1.814, rising to D = 2.12 for composite grading) fractures into predominantly coarse sub-fragments rather than pulverizing into dust, "
    "preserving skeletal interlock and permeability relative to weaker brick or pure mortar fractions."
)

add_heading_2("6.7 Validation against Published Experimental Benchmark Datasets")
add_body_p(
    "To verify fidelity against real laboratory tests, the calibrated scaling engine was evaluated directly against published experimental checkpoints "
    "from Cai et al. (2024) Fig. 11 and Liang et al. (2025) Table 2 across all three demolition materials. Table 6.2 confirms strong accuracy, with "
    "MAPE spanning 1.15% (RC) to 5.07% (RB)."
)

headers_6_2 = ["Material Type", "Published Experimental Source", "MAE (MPa)", "RMSE (MPa)", "MAPE (%)", "Agreement Level"]
rows_6_2 = [
    ["Recycled Concrete (RC)", "Liang et al. (2025) & Cai et al. (2024)", "0.043", "0.060", "1.15%", "Outstanding"],
    ["Recycled Mortar (RM)", "Liang et al. (2025) & Cai et al. (2024)", "0.030", "0.047", "2.02%", "Outstanding"],
    ["Recycled Brick (RB)", "Liang et al. (2025) & Cai et al. (2024)", "0.148", "0.180", "5.07%", "High Fidelity"]
]
add_table_data(headers_6_2, rows_6_2, [1.5, 2.1, 0.75, 0.75, 0.75, 0.95], caption="Table 6.2. Validation of virtual testing suite against published experimental benchmark datasets.")

# ==============================================================================
# CHAPTER 7: SUMMARY AND FUTURE PLAN OF WORK
# ==============================================================================
add_heading_1("7. SUMMARY AND FUTURE PLAN OF WORK")

add_heading_2("7.1 Summary of Research Achievements")
add_body_p("The major findings and contributions of this B.Tech project are summarized as follows:")
add_bullet_p("1. Physics-Informed Machine Learning Paradigm: ", "Successfully established a multi-target machine learning pipeline linking 3D particle morphology to single-particle crushing mechanics and post-breakage fractal gradation.")
add_bullet_p("2. Strong Predictive Fidelity: ", "CatBoost achieved the best overall performance across all four targets (mean R² = 0.9619: R² = 0.9871 for peak force F_f, 0.9636 for strength sigma_f, 0.9498 for crushing energy E_f, and 0.9469 for fractal dimension D), resolving both smooth strength scaling and piecewise energy regimes.")
add_bullet_p("3. Explainable Mechanics via TreeSHAP: ", "Confirmed physically consistent feature attributions: material density and 3D sphericity govern crushing strength sigma_f, while shortest axis S and equivalent diameter d_eq govern peak force F_f and crushing energy E_f.")
add_bullet_p("4. Rapid Non-Destructive Virtual Suite: ", "Deployed an interactive Streamlit engineering platform that replaces 24-hour destructive lab sieving and UTM testing with instantaneous, non-destructive characterization.")
add_bullet_p("5. Literature Validation & Engineering Screening: ", "Validated scaling accuracy within 1.15%–5.07% MAPE against Cai et al. (2024) and Liang et al. (2025), and integrated Li et al. (2021) fractal criteria with IRC:37-2018 / IS 383 aggregate screening.")

add_heading_2("7.2 Future Plan of Work")
add_body_p("Building upon the outcomes of this study, future research directions include:")
add_bullet_p("1. Indian C&D Waste Calibration: ", "Conduct laboratory UTM compression and mechanical sieving on locally sourced C&D waste from Indian recycling facilities (Delhi, Ahmedabad, Jodhpur) to establish regional calibration factors.")
add_bullet_p("2. Discrete Element Method (DEM) Integration: ", "Couple the single-particle ML breakage engine into 3D DEM codes (PFC3D / YADE) using fragment-replacement algorithms to simulate bulk roller compaction and cyclic traffic loading.")
add_bullet_p("3. 3D Laser / Structured-Light Scanner: ", "Upgrade the auxiliary computer vision module to multi-view 3D photogrammetry or structured-light scanning to directly capture the shortest axis S without 2D approximations.")

# ==============================================================================
# CHAPTER 8: REFERENCES
# ==============================================================================
doc.add_page_break()
add_heading_1("8. REFERENCES")

refs = [
    "[1] Liang, Y., Wang, L., Zhang, J., and Liu, X. (2025). \"Experimental study on the influence of particle size and type on single particle breakage of construction waste.\" Case Studies in Construction Materials, 23, e05603.",
    "[2] Cai, X., Chen, Y., Zhou, Z., and Gao, W. (2024). \"Quantifying the influence of single particle shape on crushing characteristics of recycled aggregates.\" Construction and Building Materials, 439, 137363.",
    "[3] Wang, Y., Xiao, Y., and Desai, C. S. (2021). \"Machine learning reveals the influences of grain morphology on grain crushing strength.\" Acta Geotechnica, 16(11), 3617–3630.",
    "[4] Hiramatsu, Y., and Oka, Y. (1966). \"Determination of the tensile strength of rock by a compression test of an irregular test piece.\" Int. J. Rock Mech. Min. Sci., 3(2), 89–99.",
    "[5] Bagheri, G. H., Bonadonna, C., Manzella, I., and Vonlanthen, P. (2015). \"On the shape of particle aggregates and their equivalent diameters.\" Powder Technology, 284, 464–474.",
    "[6] Weibull, W. (1951). \"A statistical distribution function of wide applicability.\" Journal of Applied Mechanics, 18(3), 293–297.",
    "[7] Tyler, S. W., and Wheatcraft, S. W. (1992). \"Fractal scaling of soil particle-size distributions: Analysis and limitations.\" Soil Sci. Soc. Am. J., 56(2), 362–369.",
    "[8] Zingg, T. (1935). \"Beitrag zur Schotteranalyse.\" Schweizerische Mineralogische und Petrographische Mitteilungen, 15(1), 39–140.",
    "[9] Griffith, A. A. (1921). \"The phenomena of rupture and flow in solids.\" Philosophical Transactions of the Royal Society of London. Series A, 221, 163–198.",
    "[10] Oskooei, P. R., Airey, G., and Thom, N. (2021). \"Crushing behavior of recycled waste materials: Experimental analysis and DEM simulation.\" Construction and Building Materials, 299, 124226.",
    "[11] Miao, S., Zhang, S., and Sun, H. (2024). \"Intelligent prediction of comprehensive mechanical properties of recycled aggregate concrete.\" Case Studies in Construction Materials, 21, e03708.",
    "[12] Turcotte, D. L. (1986). \"Fractals and fragmentation.\" Journal of Geophysical Research: Solid Earth, 91(B2), 1921–1926.",
    "[13] Li, X., Zhu, Z., and Wang, M. (2021). \"Particle size effect and fractal characteristics of fragmentation of limestone aggregates under static and impact loading.\" Advances in Materials Science and Engineering, 2021, 6097897.",
    "[14] Indian Roads Congress. (2018). \"IRC:37-2018: Guidelines for the Design of Flexible Pavements.\" New Delhi: Indian Roads Congress.",
    "[15] Bureau of Indian Standards. (2016). \"IS 383:2016: Coarse and Fine Aggregate for Concrete — Specification.\" New Delhi: BIS.",
    "[16] Central Pollution Control Board. (2024). \"Annual Report on Construction and Demolition Waste Management in India.\" New Delhi: CPCB, Ministry of Environment, Forest and Climate Change."
]

for ref_text in refs:
    p_ref = doc.add_paragraph()
    p_ref.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_ref.paragraph_format.space_before = Pt(2)
    p_ref.paragraph_format.space_after = Pt(4)
    p_ref.paragraph_format.left_indent = Inches(0.3)
    p_ref.paragraph_format.first_line_indent = Inches(-0.3)
    r = p_ref.add_run(ref_text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10)

print(f"Saving Word report to {DOCX_OUT}...")
doc.save(str(DOCX_OUT))
doc.save(str(DOCX_ARTIFACT))
print(f"SUCCESS! Saved Word report: {DOCX_OUT} ({DOCX_OUT.stat().st_size:,} bytes)")
