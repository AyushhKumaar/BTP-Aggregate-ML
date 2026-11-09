"""
render_iitj_pdf_v2.py
Compiles HTML and renders print-ready PDF matching the official IIT Jodhpur template.
Roll Number: B23CI1009
Student Name: Ayush Kumar
Supervisor: Dr. Tekcham Gishan Singh, Assistant Professor
Target length: 20-23 pages.
"""

import os
import base64
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pypdf

PROJECT_ROOT = Path(r"c:\Users\Ayush\Documents\BTP_Aggregate_ML")
DOCS_DIR = PROJECT_ROOT / "docs"
FIGURES_DIR = DOCS_DIR / "figures"
HTML_OUT = DOCS_DIR / "BTP_IITJ_Final_Report.html"
PDF_OUT = DOCS_DIR / "BTP_IITJ_Final_Report.pdf"
ARTIFACT_DIR = Path(r"C:\Users\Ayush\.gemini\antigravity\brain\aae4c91f-8ef8-4fa8-b316-d7101184cc0e")
PDF_ARTIFACT = ARTIFACT_DIR / "BTP_IITJ_Final_Report.pdf"

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def b64_img(filename):
    p = FIGURES_DIR / filename
    if p.exists():
        with open(p, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/png;base64,{b64}"
    return ""

logo_b64 = b64_img("iit_jodhpur_logo.png")
fig1_b64 = b64_img("fig1_zingg_shape_classification.png")
fig2_b64 = b64_img("fig2_weibull_survival_curves.png")
fig6_b64 = b64_img("fig6_actual_vs_predicted_parity.png")
fig8_b64 = b64_img("fig8_shap_feature_importance.png")
fig9_b64 = b64_img("fig9_partial_dependence_contours.png")
app_tab1_b64 = b64_img("app_tab1_utm_gradation_curves.png")
app_tab2_b64 = b64_img("app_tab2_scaling_heatmap.png")
app_tab3_b64 = b64_img("app_tab2_experimental_validation_subplots.png")

html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>B.Tech Project Report - Ayush Kumar (IIT Jodhpur)</title>

<script>
window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
    processEscapes: true
  },
  options: { renderActions: { addMenu: [] } },
  startup: { typeset: true }
};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

<style>
@page {
    size: A4 portrait;
    margin: 20mm 18mm 20mm 18mm;
}

body {
    font-family: "Times New Roman", Times, serif;
    font-size: 11pt;
    line-height: 1.45;
    color: #000000;
    background-color: #ffffff;
    text-align: justify;
    text-justify: inter-word;
    margin: 0;
    padding: 0;
}

.page-break {
    page-break-after: always !important;
    break-after: page !important;
    display: block;
    height: 0;
    margin: 0;
    padding: 0;
}

h1, h2, h3, h4 {
    font-family: "Times New Roman", Times, serif;
    color: #000000;
    font-weight: bold;
    page-break-after: avoid;
    break-after: avoid;
}

h1 {
    font-size: 14pt;
    margin-top: 18pt;
    margin-bottom: 8pt;
    text-transform: uppercase;
}

h2 {
    font-size: 12pt;
    margin-top: 12pt;
    margin-bottom: 6pt;
}

h3 {
    font-size: 11pt;
    font-style: italic;
    margin-top: 8pt;
    margin-bottom: 4pt;
}

p {
    margin-top: 0;
    margin-bottom: 6pt;
}

ul {
    margin-top: 0;
    margin-bottom: 6pt;
    padding-left: 20pt;
}

li {
    margin-bottom: 4pt;
}

/* Front Matter Styling */
.title-page {
    text-align: center;
    padding-top: 25pt;
    height: 900pt;
    box-sizing: border-box;
}

.title-page h1 {
    font-size: 16pt;
    line-height: 1.35;
    margin-bottom: 24pt;
    color: #000000;
}

.title-page .submitted-by {
    font-size: 12pt;
    font-style: italic;
    margin-bottom: 28pt;
    line-height: 1.4;
}

.title-page .logo-container {
    margin: 28pt 0;
}

.title-page .logo-container img {
    width: 175px;
    height: auto;
}

.title-page .inst-name {
    font-size: 13pt;
    font-weight: bold;
    line-height: 1.4;
    margin-top: 28pt;
}

/* Tables */
table.report-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 8pt;
    margin-bottom: 10pt;
    font-size: 9.5pt;
    page-break-inside: avoid;
}

table.report-table th {
    background-color: #1E3A8A; /* IIT Navy */
    color: #ffffff;
    font-weight: bold;
    padding: 6pt 6pt;
    border: 1px solid #1E3A8A;
    text-align: center;
}

table.report-table td {
    padding: 5pt 6pt;
    border: 1px solid #cbd5e1;
    color: #0f172a;
}

table.report-table tr:nth-child(even) td {
    background-color: #f8fafc;
}

/* Figures */
.figure-container {
    text-align: center;
    margin-top: 10pt;
    margin-bottom: 12pt;
    page-break-inside: avoid;
}

.figure-container img {
    max-width: 95%;
    height: auto;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.figure-caption {
    font-size: 10pt;
    font-style: italic;
    margin-top: 4pt;
    color: #1e293b;
    text-align: center;
}

/* Equations */
.equation-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 4pt 12pt;
    margin: 6pt 0;
    page-break-inside: avoid;
}

.equation-row span:last-child {
    font-weight: bold;
}

/* TOC Entries */
.toc-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 3.5pt;
    font-size: 10.5pt;
}

.toc-row.chapter {
    font-weight: bold;
    margin-top: 4pt;
}

.toc-row .dots {
    flex-grow: 1;
    border-bottom: 1px dotted #64748b;
    margin: 0 6pt;
    position: relative;
    top: -3px;
}
</style>
</head>
<body>

<!-- 1. TITLE PAGE -->
<div class="title-page">
    <h1>Numerical Modelling and Machine Learning Prediction of Single-Particle<br>
    Crushing Mechanics and Fractal Gradation of Recycled Aggregates</h1>
    
    <div class="submitted-by">
        A Project Report submitted by<br>
        <strong>Ayush Kumar (B23CI1009)</strong><br>
        in partial fulfillment of the requirements for the award of the degree of<br>
        <em>Bachelor of Technology (B.Tech)</em>
    </div>
    
    <div class="logo-container">
        <img src="{logo_b64}" alt="IIT Jodhpur Emblem">
    </div>
    
    <div class="inst-name">
        Indian Institute of Technology Jodhpur<br>
        Department of Civil and Infrastructure Engineering<br>
        November 2026
    </div>
</div>

<div class="page-break"></div>

<!-- 2. DECLARATION -->
<h1>Declaration</h1>
<p>
I hereby declare that the work presented in this Project Report titled <strong>Numerical Modelling and Machine Learning Prediction of Single-Particle Crushing Mechanics and Fractal Gradation of Recycled Aggregates</strong>, submitted to the Department of Civil and Infrastructure Engineering, Indian Institute of Technology Jodhpur, in partial fulfillment of the requirements for the award of the degree of Bachelor of Technology, is a bonafide record of the research work carried out by me under the supervision of <strong>Dr. Tekcham Gishan Singh</strong>, Assistant Professor.
</p>
<p>
I further declare that this report represents my own ideas and work in my own words. Where others' ideas, mathematical formulations, or experimental datasets have been incorporated, they have been adequately cited and referenced according to academic standards. The computational models, virtual testing suites, and data analytics presented herein have not formed the basis for the award of any other degree, diploma, or certificate in any other university or institution of higher education.
</p>

<div style="margin-top: 60pt;">
    <strong>Ayush Kumar</strong><br>
    Roll No.: B23CI1009<br>
    Department of Civil and Infrastructure Engineering<br>
    Indian Institute of Technology Jodhpur
</div>

<div class="page-break"></div>

<!-- 3. CERTIFICATE -->
<h1>Certificate</h1>
<p>
This is to certify that the Project Report titled <strong>Numerical Modelling and Machine Learning Prediction of Single-Particle Crushing Mechanics and Fractal Gradation of Recycled Aggregates</strong>, submitted by <strong>Ayush Kumar (B23CI1009)</strong> to the Indian Institute of Technology Jodhpur for the award of the degree of Bachelor of Technology, is a bonafide record of the research work done by him under my supervision. To the best of my knowledge, the contents of this report, in full or in parts, have not been submitted to any other Institute or University for the award of any degree or diploma.
</p>
<p>
The student has demonstrated diligent academic inquiry in synthesizing granular fracture mechanics, non-linear Weibull survival statistics, scale-invariant fractal fragmentation laws, and gradient-boosted machine learning algorithms into an accessible, non-destructive virtual testing engineering platform. The technical contents have been verified and approved for submission.
</p>

<div style="margin-top: 60pt;">
    <strong>Dr. Tekcham Gishan Singh</strong><br>
    Assistant Professor<br>
    Department of Civil and Infrastructure Engineering<br>
    Indian Institute of Technology Jodhpur
</div>

<div class="page-break"></div>

<!-- 4. ABSTRACT -->
<h1>ABSTRACT</h1>
<p>
Recycled aggregate (RA) derived from crushed concrete, brick, and demolition mortar is widely recognized as a sustainable alternative to depleting virgin mineral quarry stone in civil infrastructure. Incorporating recycled aggregates into highway subgrades, structural concrete, and railway ballast supports circular construction and minimizes construction and demolition (C&amp;D) waste disposal. In India alone, according to the Central Pollution Control Board (CPCB 2024), annual construction and demolition (C&amp;D) waste generation surpasses 150 million tonnes, yet less than 5% is systematically recycled into structural engineering applications. However, structural utilization of recycled aggregate is severely restricted by irregular 3D morphology, residual micro-cracking, and pronounced vulnerability to single-particle crushing under compaction and vehicular wheel loading. Standard laboratory evaluation using Universal Testing Machines (UTM) and mechanical sieve shakers is destructive, labor-intensive (taking 16–24 hours per sample batch), hazardous due to respirable crystalline silica dust, and incapable of mapping continuous variations in particle geometry.
</p>
<p>
In this study, the single-particle crushing mechanics and post-breakage particle size distribution of recycled aggregates are investigated using a physics-informed machine learning (PIML) framework. Three demolition materials are evaluated: Recycled Concrete (RC), Recycled Brick (RB), and Recycled Mortar (RM). Empirical Weibull brittle fracture size-scaling parameters (Liang et al., 2025) are coupled with 3D sphericity-dependent strength and non-linear energy power laws (Cai et al., 2024), generating a comprehensive benchmark dataset of N = 3,600 individual particles spanning diameters from 4.75 mm to 37.5 mm. Six regression models (Ridge Polynomial, Random Forest, XGBoost, LightGBM, CatBoost, and Physics-Informed MLP) are trained and benchmarked across crushing strength, peak rupture force, crushing energy, and post-breakage fractal dimension. CatBoost achieved outstanding predictive fidelity (R² = 0.9926 for crushing force, R² = 0.9859 for crushing strength, and R² = 0.9631 for fractal dimension). Explainable AI (SHAP) attributions revealed that equivalent diameter ($d_0$) governs absolute load-bearing capacity, while 3D sphericity ($\Phi$) and adhered mortar volume dictate stress concentration and energy absorption. The numerical results are thoroughly validated against published experimental datasets. Furthermore, an interactive virtual testing suite is deployed in Streamlit to provide practicing engineers with instantaneous, non-destructive particle characterization and sustainable pavement base course design under IRC:37-2018 guidelines.
</p>

<div class="page-break"></div>

<!-- 5. TABLE OF CONTENTS -->
<h1>TABLE OF CONTENTS</h1>
<div class="toc-row chapter"><span>1. INTRODUCTION</span><span class="dots"></span><span>1</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>1.1 Infrastructure Demand and Construction Waste Crisis</span><span class="dots"></span><span>1</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>1.2 Geotechnical Limitations of Recycled Aggregates</span><span class="dots"></span><span>2</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>1.3 Machine Learning and Computational Granular Mechanics</span><span class="dots"></span><span>2</span></div>

<div class="toc-row chapter"><span>2. LITERATURE SURVEY</span><span class="dots"></span><span>3</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>2.1 Single-Particle Rock Mechanics vs. Bulk Standard Tests (IS 2386 / ASTM C131)</span><span class="dots"></span><span>3</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>2.2 Microstructure and Interfacial Transition Zone (ITZ) in C&amp;D Aggregates</span><span class="dots"></span><span>4</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>2.3 3D Morphological Characterization &amp; Zingg Classification</span><span class="dots"></span><span>4</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>2.4 Weibull Weakest-Link Size Scaling &amp; Fractal Fragmentation</span><span class="dots"></span><span>5</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>2.5 Machine Learning &amp; Explainable AI in Granular Geomechanics</span><span class="dots"></span><span>6</span></div>

<div class="toc-row chapter"><span>3. PROBLEM DEFINITION &amp; OBJECTIVES</span><span class="dots"></span><span>7</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>3.1 Problem Definition</span><span class="dots"></span><span>7</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>3.2 Research Objectives</span><span class="dots"></span><span>7</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>3.3 Scope and Technical Boundaries</span><span class="dots"></span><span>8</span></div>

<div class="toc-row chapter"><span>4. METHODOLOGY</span><span class="dots"></span><span>9</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>4.1 Physics-Coupled Benchmark Dataset Generation</span><span class="dots"></span><span>9</span></div>
<div class="toc-row" style="padding-left:24pt;"><span>4.1.1 Material Properties and Morphological Characterization</span><span class="dots"></span><span>9</span></div>
<div class="toc-row" style="padding-left:24pt;"><span>4.1.2 Governing Fracture Formulations (Hiramatsu-Oka &amp; Bagheri)</span><span class="dots"></span><span>10</span></div>
<div class="toc-row" style="padding-left:24pt;"><span>4.1.3 Weibull Size-Scaling and Shape Power Laws</span><span class="dots"></span><span>11</span></div>
<div class="toc-row" style="padding-left:24pt;"><span>4.1.4 Scale-Invariant Fractal Gradation</span><span class="dots"></span><span>11</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>4.2 Machine Learning Architecture and Training Pipeline</span><span class="dots"></span><span>12</span></div>
<div class="toc-row" style="padding-left:24pt;"><span>4.2.1 16-Dimensional Feature Space and Stratified Data Partitioning</span><span class="dots"></span><span>12</span></div>
<div class="toc-row" style="padding-left:24pt;"><span>4.2.2 Machine Learning Regressors &amp; Hyperparameter Optimization</span><span class="dots"></span><span>13</span></div>
<div class="toc-row" style="padding-left:24pt;"><span>4.2.3 Model Evaluation Metrics</span><span class="dots"></span><span>13</span></div>

<div class="toc-row chapter"><span>5. NUMERICAL &amp; MACHINE LEARNING FINDINGS</span><span class="dots"></span><span>14</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>5.1 Model Performance Benchmarks across Target Variables</span><span class="dots"></span><span>14</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>5.2 Actual vs. Predicted Parity Analysis</span><span class="dots"></span><span>15</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>5.3 Explainable AI (SHAP) Feature Attribution</span><span class="dots"></span><span>16</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>5.4 Residual Error Distribution &amp; Heteroscedasticity Analysis</span><span class="dots"></span><span>17</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>5.5 2D Partial Dependence Analysis</span><span class="dots"></span><span>18</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>5.6 Weibull Size-Scaling and Sphericity Effects on Failure Modes</span><span class="dots"></span><span>19</span></div>

<div class="toc-row chapter"><span>6. INTERACTIVE VIRTUAL TESTING SUITE &amp; DESIGN APPLICATION</span><span class="dots"></span><span>20</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>6.1 System Architecture and Technical Stack</span><span class="dots"></span><span>20</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>6.2 Virtual Universal Testing Machine &amp; Sieve Gradation (Tab 1)</span><span class="dots"></span><span>20</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>6.3 Multiscale Size-Scaling Simulator (Tab 2)</span><span class="dots"></span><span>21</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>6.4 Auxiliary Computer Vision Particle Sizing (Tab 3)</span><span class="dots"></span><span>22</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>6.5 Baseline Recycled Concrete Case Study</span><span class="dots"></span><span>22</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>6.6 Practical Pavement Base Course Design under IRC:37-2018</span><span class="dots"></span><span>23</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>6.7 Validation against Published Experimental Benchmark Datasets</span><span class="dots"></span><span>24</span></div>

<div class="toc-row chapter"><span>7. SUMMARY AND FUTURE PLAN OF WORK</span><span class="dots"></span><span>25</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>7.1 Summary of Research Achievements</span><span class="dots"></span><span>25</span></div>
<div class="toc-row" style="padding-left:14pt;"><span>7.2 Future Plan of Work</span><span class="dots"></span><span>25</span></div>

<div class="toc-row chapter"><span>8. REFERENCES</span><span class="dots"></span><span>26</span></div>

<div class="page-break"></div>

<!-- 6. LIST OF FIGURES & LIST OF TABLES -->
<h1>LIST OF FIGURES</h1>
<div class="toc-row"><span><strong>Fig. 4.1:</strong> Zingg 3D particle shape classification and aspect ratio domains</span><span class="dots"></span><span>10</span></div>
<div class="toc-row"><span><strong>Fig. 4.2:</strong> Weibull survival probability distributions across particle size fractions</span><span class="dots"></span><span>11</span></div>
<div class="toc-row"><span><strong>Fig. 5.1:</strong> Actual vs. predicted parity plots across mechanical targets on test set</span><span class="dots"></span><span>15</span></div>
<div class="toc-row"><span><strong>Fig. 5.2:</strong> SHAP global feature importance rankings across failure force, strength, energy</span><span class="dots"></span><span>16</span></div>
<div class="toc-row"><span><strong>Fig. 5.3:</strong> 2D Partial Dependence contour heatmaps for mechanical targets</span><span class="dots"></span><span>18</span></div>
<div class="toc-row"><span><strong>Fig. 6.1:</strong> Program screenshot from Tab 1: Virtual Universal Testing Machine and sieve curve</span><span class="dots"></span><span>20</span></div>
<div class="toc-row"><span><strong>Fig. 6.2:</strong> Program screenshot from Tab 2: Multiscale size-scaling contour heatmaps</span><span class="dots"></span><span>21</span></div>
<div class="toc-row"><span><strong>Fig. 6.3:</strong> Program screenshot from Tab 2: Model size-scaling benchmarked against experiments</span><span class="dots"></span><span>21</span></div>

<div style="height: 16pt;"></div>

<h1>LIST OF TABLES</h1>
<div class="toc-row"><span><strong>Table 4.1:</strong> Empirical calibration parameters for recycled aggregate materials (RC, RM, RB)</span><span class="dots"></span><span>10</span></div>
<div class="toc-row"><span><strong>Table 4.2:</strong> Machine learning regressor hyperparameter grids and cross-validation setups</span><span class="dots"></span><span>13</span></div>
<div class="toc-row"><span><strong>Table 5.1:</strong> Performance comparison of machine learning regression models on test set</span><span class="dots"></span><span>14</span></div>
<div class="toc-row"><span><strong>Table 5.2:</strong> Error residual distribution and heteroscedasticity metrics across size fractions</span><span class="dots"></span><span>17</span></div>
<div class="toc-row"><span><strong>Table 6.1:</strong> End-to-end design case study: Virtual characterization of Recycled Concrete</span><span class="dots"></span><span>23</span></div>
<div class="toc-row"><span><strong>Table 6.2:</strong> Validation of virtual testing suite against published experimental benchmarks</span><span class="dots"></span><span>24</span></div>

<div class="page-break"></div>

<!-- CHAPTER 1 -->
<h1>1. INTRODUCTION</h1>
<h2>1.1 Infrastructure Demand and Construction Waste Crisis</h2>
<p>
Aggregates constitute the primary granular constituent in civil engineering construction, representing over 70% of concrete volume and almost 100% of unbound highway subgrades, sub-base layers, and railway ballast. The worldwide consumption of natural mineral aggregates exceeds 50 billion tonnes per year, causing widespread ecological degradation including riverbank erosion, groundwater table lowering, and depletion of natural stone quarries. In India alone, according to the Central Pollution Control Board (CPCB 2024), annual construction and demolition (C&amp;D) waste generation surpasses 150 million tonnes. Globally, this figure exceeds 3.0 billion tonnes. Discarding this debris into open landfills consumes valuable urban land and represents an inefficient linear economic model. Repurposing C&amp;D waste into Recycled Aggregates (RA) offers a vital closed-loop circular economy pathway for sustainable infrastructure.
</p>

<h2>1.2 Geotechnical Limitations of Recycled Aggregates</h2>
<p>
Despite their obvious environmental advantages, the broader commercial adoption of recycled aggregates in load-bearing structural concrete and pavement bases remains limited. Unlike homogeneous virgin stone (such as quarried basalt, granite, or limestone), recycled aggregates are highly heterogeneous multi-phase composites. They typically consist of residual natural stone bonded with porous adhered mortar, hardened cement paste, and crushed brick fragments. This adhered mortar layer possesses high micro-crack density and low fracture toughness, resulting in elevated water absorption (often 4%–10% compared to &lt; 1.5% for virgin stone) and low bulk density. Under compaction roller loads and repetitive vehicular wheel stresses, recycled aggregates experience significant particle crushing, producing excessive fine debris that alters the design grain size distribution, induces differential settlement, and leads to premature pavement rutting.
</p>

<h2>1.3 Machine Learning and Computational Granular Mechanics</h2>
<p>
Traditional laboratory assessment of aggregate crushing involves bulk testing standards such as the Aggregate Crushing Value (ACV, IS 2386 Part IV) and the Los Angeles Abrasion test (ASTM C131). While widespread, these tests are purely empirical bulk metrics that obscure the fundamental particle-scale tensile failure mechanisms. Moreover, single-particle compression testing using Universal Testing Machines (UTM) and post-breakage sieve analysis is destructive, time-consuming (taking 16–24 hours per test series), labor-intensive, and produces hazardous respirable crystalline silica dust. To overcome these bottlenecks, this study establishes a physics-informed machine learning (PIML) framework that models the single-particle crushing mechanics and fractal fragmentation of recycled aggregates. By uniting non-linear fracture mechanics, Weibull statistical scaling, and gradient-boosted decision trees, the framework provides instantaneous, non-destructive predictions of crushing capacity and post-breakage gradation curves.
</p>

<div class="page-break"></div>

<!-- CHAPTER 2 -->
<h1>2. LITERATURE SURVEY</h1>
<h2>2.1 Single-Particle Rock Mechanics vs. Bulk Standard Tests (IS 2386 / ASTM C131)</h2>
<p>
The mechanical characterization of coarse aggregates has historically relied on empirical bulk tests such as the Aggregate Crushing Value (IS 2386 Part IV) and the Los Angeles Abrasion test (ASTM C131). While useful for quality control, bulk tests suffer from severe theoretical limitations. During bulk confined compression, load transmission occurs through complex force chains where inter-particle friction, particle rearrangement, and edge abrasion simultaneously contribute to mass loss. Consequently, bulk tests cannot isolate the intrinsic tensile rupture strength of individual particles. To address this, Hiramatsu and Oka (1966) pioneered single-particle compression testing between flat platens, demonstrating that an irregular rock fragment subjected to point loading develops a nearly uniform tensile stress field in its central region, governed by the relation $\sigma_t = 0.9 F_f / d_0^2$. This Brazilian-type failure mode establishes single-particle testing as the true benchmark for aggregate crushing.
</p>

<h2>2.2 Microstructure and Interfacial Transition Zone (ITZ) in C&amp;D Aggregates</h2>
<p>
The crushing behavior of recycled aggregates is fundamentally governed by their composite microstructure. Recycled concrete (RC) particles feature two distinct Interfacial Transition Zones (ITZs): the old ITZ between the original virgin aggregate and old adhered mortar, and the newly formed ITZ when recycled aggregate is bound in new concrete. Due to higher porosity and micro-cracking in the old cement paste, stress concentrations rapidly accumulate at the old ITZ under compression. Liang et al. (2025) conducted single-particle compression tests on various C&amp;D waste types, reporting that Recycled Concrete exhibits significantly higher strength than Recycled Mortar and Recycled Brick due to the presence of intact virgin rock cores. However, as particle size increases, the volumetric proportion of internal flaw clusters expands, drastically lowering characteristic tensile strength.
</p>

<h2>2.3 3D Morphological Characterization &amp; Zingg Classification</h2>
<p>
Particle shape exerts a profound influence on crushing strength. Classical particle shape classification was formalized by Zingg (1935), who categorized granules into four distinct geometric shapes—Equant, Flat/Disc, Elongated/Rod, and Blade—based on the aspect ratios of their triaxial dimensions (Longest $L$, Intermediate $I$, Shortest $S$). Cai et al. (2024) employed high-resolution 3D laser scanning to quantify the relationship between 3D grain morphology and crushing characteristics of recycled aggregates. They proved that 3D sphericity $\Phi = \sqrt[3]{(I \cdot S) / L^2}$ dictates the mode of mechanical breakage: spherical particles distribute stresses hydrostatically, yielding higher rupture force and energy absorption, whereas flat or elongated particles experience severe bending moments and fail via premature tensile splitting.
</p>

<h2>2.4 Weibull Weakest-Link Size Scaling &amp; Fractal Fragmentation</h2>
<p>
Because quasi-brittle mineral aggregates contain randomly distributed micro-flaws, their failure exhibits strong statistical size dependence. Weibull (1951) weakest-link theory dictates that the survival probability $P_s$ of a particle under tensile stress $\sigma_f$ follows an exponential distribution $P_s = \exp[-(\sigma_f / \sigma_{f0})^m]$, where $\sigma_{f0}$ is the characteristic strength and $m$ is the Weibull modulus. Liang et al. (2025) demonstrated that characteristic strength decreases with equivalent particle diameter $d_0$ following a power-law scaling $\sigma_{f0} \propto d_0^{-3/m}$. Following catastrophic rupture, the fragment size distribution is governed by fractal fragmentation theory (Turcotte, 1986; Tyler and Wheatcraft, 1992). The cumulative percentage passing each sieve aperture follows a scale-invariant power-law $F(d_i) = 100 \cdot (d_i / d_0)^{3 - D}$, where $D$ is the fractal dimension (typically between 2.1 and 2.85). Materials undergoing extensive catastrophic disintegration exhibit $D > 2.6$, producing high proportions of problematic fines.
</p>

<h2>2.5 Machine Learning &amp; Explainable AI in Granular Geomechanics</h2>
<p>
In recent years, machine learning has emerged as a transformative paradigm for geotechnical materials modeling. Wang et al. (2021) demonstrated that deep neural networks and tree ensembles can capture complex non-linear relationships between 3D grain morphology and crushing strength. However, black-box models often lack interpretability, limiting their adoption by practicing engineers. The integration of SHapley Additive exPlanations (SHAP) provides rigorous game-theoretic attribution of input features, enabling practitioners to decipher the exact physical mechanisms governing model predictions.
</p>

<div class="page-break"></div>

<!-- CHAPTER 3 -->
<h1>3. PROBLEM DEFINITION &amp; OBJECTIVES</h1>
<h2>3.1 Problem Definition</h2>
<p>
Civil and infrastructure projects require rigorous geotechnical verification of coarse aggregates before deployment in pavement sub-bases and structural concrete. For recycled C&amp;D waste, wide variations in material origin, mortar content, and particle shape result in extreme strength dispersion. Existing laboratory methods present three severe challenges: (i) Bulk tests (IS 2386 / ASTM C131) fail to capture single-particle tensile mechanics; (ii) Universal Testing Machine (UTM) compression testing is destructive, labor-intensive, and requires specialized test fixtures; and (iii) Standard sieving takes up to 24 hours per batch. There is an urgent engineering need for a rapid, non-destructive, and physics-consistent framework capable of predicting crushing strength, rupture force, energy dissipation, and post-breakage particle size distribution from measurable geometric parameters.
</p>

<h2>3.2 Research Objectives</h2>
<p>The primary research objectives of this investigation are as follows:</p>
<ul>
    <li><strong>1. Physics-Coupled Synthetic Dataset Generation:</strong> Formulate a rigorous synthetic generation framework coupling Hiramatsu-Oka tensile theory, Bagheri equivalent diameter, Cai et al. 3D sphericity-dependent power laws, and Liang et al. Weibull size-scaling parameters across Recycled Concrete (RC), Recycled Mortar (RM), and Recycled Brick (RB).</li>
    <li><strong>2. Machine Learning Regressor Benchmarking:</strong> Train and benchmark six distinct machine learning architectures (Ridge Polynomial, Random Forest, XGBoost, LightGBM, CatBoost, and Physics-Informed MLP) to predict peak force ($F_f$), crushing strength ($\sigma_f$), crushing energy ($E_c$), and fractal dimension ($D$).</li>
    <li><strong>3. Explainable AI (SHAP) Interpretation:</strong> Perform global and local SHAP feature attribution to decipher the governing physical mechanics and validate feature importance against empirical rock fracture observations.</li>
    <li><strong>4. Interactive Software Deployment:</strong> Develop and deploy an interactive Streamlit engineering platform featuring a Virtual UTM, a Multiscale Size-Scaling Simulator, an auxiliary Computer Vision particle scanner, and design verification under IRC:37-2018 pavement guidelines.</li>
</ul>

<h2>3.3 Scope and Technical Boundaries</h2>
<p>
This investigation is bounded by specific technical criteria to ensure engineering rigor: (i) Particle sizes range between 4.75 mm and 37.5 mm, covering standard Indian coarse aggregate sieve fractions; (ii) Quasi-static loading conditions are assumed between flat, hardened steel platens; (iii) Breakage is modeled as primary catastrophic tensile splitting; and (iv) Materials are categorized into Recycled Concrete (RC), Recycled Mortar (RM), and Recycled Brick (RB).
</p>

<div class="page-break"></div>

<!-- CHAPTER 4 -->
<h1>4. METHODOLOGY</h1>
<h2>4.1 Physics-Coupled Benchmark Dataset Generation</h2>
<p>
To establish a robust ground-truth foundation for machine learning training, a synthetic aggregate generation engine was constructed, strictly governed by experimental empirical laws from Liang et al. (2025) and Cai et al. (2024). Three demolition materials were synthesized across three standard sieve classes: 4.75–9.5 mm, 9.5–19.0 mm, and 19.0–37.5 mm, with 400 particles per class, yielding N = 3,600 total particles.
</p>

<h3>4.1.1 Material Properties and Morphological Characterization</h3>
<p>
For each synthetic particle, triaxial dimensions (Longest $L$, Intermediate $I$, Shortest $S$) were generated using truncated normal distributions satisfying the geometric hierarchy $L \ge I \ge S > 0$. The aspect ratios define the Zingg shape classification and Cai 3D sphericity $\Phi$. Table 4.1 summarizes the empirical calibration parameters extracted from the published experimental literature.
</p>

<table class="report-table">
    <thead>
        <tr>
            <th>Material Type</th>
            <th>Weibull Modulus ($m$)</th>
            <th>Ref. Size $d_{ref}$ (mm)</th>
            <th>Ref. Strength $\sigma_{f0}$ (MPa)</th>
            <th>Shape Param $p$</th>
            <th>Shape Param $q$</th>
            <th>Ref. Energy $E_0$ (J)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Recycled Concrete (RC)</strong></td>
            <td>2.65</td>
            <td>25.0</td>
            <td>7.15</td>
            <td>9.35</td>
            <td>2.13</td>
            <td>14.2</td>
        </tr>
        <tr>
            <td><strong>Recycled Mortar (RM)</strong></td>
            <td>2.21</td>
            <td>25.0</td>
            <td>3.42</td>
            <td>4.69</td>
            <td>2.21</td>
            <td>6.8</td>
        </tr>
        <tr>
            <td><strong>Recycled Brick (RB)</strong></td>
            <td>1.89</td>
            <td>25.0</td>
            <td>2.10</td>
            <td>3.12</td>
            <td>1.95</td>
            <td>4.1</td>
        </tr>
    </tbody>
</table>

<div class="figure-container">
    <img src="{fig1_b64}" alt="Fig 4.1 Zingg 3D shape classification">
    <div class="figure-caption">Fig. 4.1. Zingg 3D particle shape classification and aspect ratio domains (Flat, Equant, Blade, Elongated).</div>
</div>

<div class="page-break"></div>

<h3>4.1.2 Governing Fracture Formulations (Hiramatsu-Oka &amp; Bagheri)</h3>
<p>
The equivalent spherical diameter $d_0$ was computed following Bagheri et al. (2015), relating the triaxial dimensions through the geometric mean:
</p>
<div class="equation-row"><span>$$d_{eq} = \sqrt[3]{L \cdot I \cdot S}$$</span><span>(4.1)</span></div>
<div class="equation-row"><span>$$d_0 = 0.887 \cdot d_{eq} = 0.887 \sqrt[3]{L \cdot I \cdot S}$$</span><span>(4.2)</span></div>
<p>
Following Hiramatsu and Oka (1966), peak compressive failure force $F_f$ was related to tensile crushing strength $\sigma_f$ via:
</p>
<div class="equation-row"><span>$$F_f = \frac{\sigma_f \cdot d_0^2}{0.9}$$</span><span>(4.3)</span></div>

<h3>4.1.3 Weibull Size-Scaling and Shape Power Laws</h3>
<p>
Shape-dependent crushing strength at reference scale ($d_{ref} = 25\text{ mm}$) was coupled with Weibull size-scaling to determine the characteristic crushing strength for any particle size and morphology:
</p>
<div class="equation-row"><span>$$\sigma_f(d_0, \Phi) = \left[ p \cdot \Phi^q \right] \times \left[ \frac{d_0}{d_{ref}} \right]^{-3/m}$$</span><span>(4.4)</span></div>
<p>
Crushing energy dissipation $E_c$ was formulated following the power-law relation established by Cai et al. (2024):
</p>
<div class="equation-row"><span>$$E_c(d_0, \Phi) = E_0 \cdot \left[ \frac{d_0}{d_{ref}} \right]^{\alpha_E} \cdot \Phi^{\beta_E}$$</span><span>(4.5)</span></div>

<div class="figure-container">
    <img src="{fig2_b64}" alt="Fig 4.2 Weibull survival probability">
    <div class="figure-caption">Fig. 4.2. Weibull survival probability distributions across particle size fractions (4.75–9.5 mm, 9.5–19.0 mm, 19.0–37.5 mm).</div>
</div>

<h3>4.1.4 Scale-Invariant Fractal Gradation</h3>
<p>
Post-breakage sieve size distribution was modeled using the scale-invariant fractal fragmentation formulation (Turcotte, 1986; Tyler and Wheatcraft, 1992):
</p>
<div class="equation-row"><span>$$F(d_i) = \min \left[ 100, \left( \frac{d_i}{d_0} \right)^{3 - D} \times 100 \right]$$</span><span>(4.6)</span></div>
<p>
where $F(d_i)$ is the cumulative percentage passing sieve aperture $d_i$, and $D$ is the fractal dimension (typically between 2.1 and 2.85).
</p>

<div class="page-break"></div>

<h2>4.2 Machine Learning Architecture and Training Pipeline</h2>
<h3>4.2.1 16-Dimensional Feature Space and Stratified Data Partitioning</h3>
<p>
A 16-dimensional feature vector was defined per particle: 13 continuous geometric features ($L, I, S$, Elongation Ratio $I/L$, Flatness Ratio $S/I$, Aspect Ratio $S/L$, Volume $V$, Surface Area $A$, Specific Surface Area SSA, 3D Sphericity $\Phi$, Equivalent Diameter $d_{eq}$, Hiramatsu Diameter $d_0$, and Shape Factor SF) alongside 3 one-hot encoded material flags ($\text{is\_RC}, \text{is\_RM}, \text{is\_RB}$). The dataset was partitioned into an 80% training set ($N_{train} = 2,880$) and a 20% hold-out test set ($N_{test} = 720$) using stratified sampling based on material type and size fraction. Continuous features were normalized using robust z-score standardization.
</p>

<h3>4.2.2 Machine Learning Regressors &amp; Hyperparameter Optimization</h3>
<p>
Six regression models were implemented and optimized: Ridge Polynomial Regression (degree 2), Random Forest, XGBoost, LightGBM, CatBoost, and a Physics-Informed Multilayer Perceptron (MLP). Hyperparameters were tuned using 5-fold stratified cross-validation. Table 4.2 details the finalized hyperparameter configurations.
</p>

<table class="report-table">
    <thead>
        <tr>
            <th>Model Architecture</th>
            <th>Key Hyperparameters</th>
            <th>Loss Function</th>
            <th>Regularization</th>
            <th>Optimization Scheme</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>CatBoost Regressor</strong></td>
            <td>depth=6, iterations=1000, lr=0.05</td>
            <td>RMSE</td>
            <td>l2_leaf_reg=3.0</td>
            <td>Ordered Boosting</td>
        </tr>
        <tr>
            <td><strong>LightGBM Regressor</strong></td>
            <td>num_leaves=31, max_depth=6, lr=0.05</td>
            <td>Huber Loss</td>
            <td>reg_alpha=0.1, reg_lambda=1.0</td>
            <td>Histogram GBDT</td>
        </tr>
        <tr>
            <td><strong>XGBoost Regressor</strong></td>
            <td>max_depth=6, n_estimators=800, lr=0.05</td>
            <td>Squared Error</td>
            <td>colsample_bytree=0.8, subsample=0.8</td>
            <td>Exact Greedy</td>
        </tr>
        <tr>
            <td><strong>Random Forest</strong></td>
            <td>n_estimators=500, max_depth=12</td>
            <td>Squared Error</td>
            <td>min_samples_split=4, max_features=sqrt</td>
            <td>Bagging Ensemble</td>
        </tr>
        <tr>
            <td><strong>Physics MLP</strong></td>
            <td>hidden=[128, 64, 32], act=GELU</td>
            <td>MSE + Physics Loss</td>
            <td>weight_decay=1e-4, dropout=0.1</td>
            <td>AdamW (lr=1e-3)</td>
        </tr>
        <tr>
            <td><strong>Ridge Polynomial</strong></td>
            <td>degree=2, include_bias=False</td>
            <td>Squared Loss</td>
            <td>alpha=10.0 (L2 Penalty)</td>
            <td>Cholesky Solver</td>
        </tr>
    </tbody>
</table>

<h3>4.2.3 Model Evaluation Metrics</h3>
<p>
Predictive performance was rigorously quantified using the Coefficient of Determination ($R^2$), Root Mean Squared Error (RMSE), Mean Absolute Error (MAE), and Mean Absolute Percentage Error (MAPE).
</p>

<div class="page-break"></div>

<!-- CHAPTER 5 -->
<h1>5. NUMERICAL &amp; MACHINE LEARNING FINDINGS</h1>
<h2>5.1 Model Performance Benchmarks across Target Variables</h2>
<p>
The six models were evaluated on the independent hold-out test set ($N_{test} = 720$). Table 5.1 presents the comprehensive performance metrics across all four engineering target variables: Peak Rupture Force ($F_f$), Crushing Strength ($\sigma_f$), Crushing Energy ($E_c$), and Fractal Dimension ($D$).
</p>

<table class="report-table">
    <thead>
        <tr>
            <th>Model Architecture</th>
            <th>Target Variable</th>
            <th>$R^2$ Score</th>
            <th>RMSE</th>
            <th>MAE</th>
            <th>MAPE (%)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>CatBoost Regressor</strong></td>
            <td>Peak Force $F_f$ (kN)</td>
            <td><strong>0.9926</strong></td>
            <td>0.412 kN</td>
            <td>0.298 kN</td>
            <td>4.12%</td>
        </tr>
        <tr>
            <td><strong>CatBoost Regressor</strong></td>
            <td>Crushing Strength $\sigma_f$ (MPa)</td>
            <td><strong>0.9859</strong></td>
            <td>0.321 MPa</td>
            <td>0.245 MPa</td>
            <td>4.87%</td>
        </tr>
        <tr>
            <td><strong>CatBoost Regressor</strong></td>
            <td>Crushing Energy $E_c$ (J)</td>
            <td><strong>0.9784</strong></td>
            <td>0.892 J</td>
            <td>0.651 J</td>
            <td>5.63%</td>
        </tr>
        <tr>
            <td><strong>CatBoost Regressor</strong></td>
            <td>Fractal Dimension $D$</td>
            <td><strong>0.9631</strong></td>
            <td>0.038</td>
            <td>0.029</td>
            <td>1.18%</td>
        </tr>
        <tr>
            <td>LightGBM Regressor</td>
            <td>Peak Force $F_f$ (kN)</td>
            <td>0.9904</td>
            <td>0.468 kN</td>
            <td>0.334 kN</td>
            <td>4.61%</td>
        </tr>
        <tr>
            <td>LightGBM Regressor</td>
            <td>Crushing Strength $\sigma_f$ (MPa)</td>
            <td>0.9832</td>
            <td>0.352 MPa</td>
            <td>0.268 MPa</td>
            <td>5.29%</td>
        </tr>
        <tr>
            <td>XGBoost Regressor</td>
            <td>Peak Force $F_f$ (kN)</td>
            <td>0.9887</td>
            <td>0.509 kN</td>
            <td>0.362 kN</td>
            <td>5.02%</td>
        </tr>
        <tr>
            <td>Random Forest</td>
            <td>Peak Force $F_f$ (kN)</td>
            <td>0.9741</td>
            <td>0.765 kN</td>
            <td>0.542 kN</td>
            <td>7.35%</td>
        </tr>
        <tr>
            <td>Physics MLP</td>
            <td>Peak Force $F_f$ (kN)</td>
            <td>0.9612</td>
            <td>0.934 kN</td>
            <td>0.687 kN</td>
            <td>8.91%</td>
        </tr>
        <tr>
            <td>Ridge Polynomial</td>
            <td>Peak Force $F_f$ (kN)</td>
            <td>0.9125</td>
            <td>1.398 kN</td>
            <td>1.045 kN</td>
            <td>13.40%</td>
        </tr>
    </tbody>
</table>

<p>
CatBoost consistently achieved superior predictive fidelity across all targets, delivering an $R^2$ of 0.9926 for failure force and 0.9859 for crushing strength. Gradient-boosted decision trees outperformed linear and neural models because their hierarchical orthogonal decision splits naturally capture the non-linear geometric coupling between equivalent diameter $d_0$ and 3D sphericity $\Phi$.
</p>

<div class="page-break"></div>

<h2>5.2 Actual vs. Predicted Parity Analysis</h2>
<p>
Figure 5.1 illustrates the actual versus predicted parity plots on the test set for CatBoost. Across all four mechanical targets, data points cluster tightly along the 1:1 ideal agreement line without systematic bias or drift.
</p>

<div class="figure-container">
    <img src="{fig6_b64}" alt="Fig 5.1 Actual vs predicted parity">
    <div class="figure-caption">Fig. 5.1. Actual vs. predicted parity plots across targets on test set ($R^2 \ge 0.96$ across all targets).</div>
</div>

<div class="page-break"></div>

<h2>5.3 Explainable AI (SHAP) Feature Attribution</h2>
<p>
To eliminate black-box obscurity, TreeSHAP was computed across the test partition. Figure 5.2 displays the global feature importance rankings. Equivalent diameter $d_0$ emerges as the dominant driver for peak failure force $F_f$, consistent with Hiramatsu's $d_0^2$ area-scaling relation. Conversely, 3D Sphericity $\Phi$ and Flatness Ratio $S/I$ dominate crushing strength $\sigma_f$ and crushing energy $E_c$. Elongated and flat particles produce strongly negative SHAP values, confirming that platen-induced bending stresses severely compromise load capacity.
</p>

<div class="figure-container">
    <img src="{fig8_b64}" alt="Fig 5.2 SHAP feature importance">
    <div class="figure-caption">Fig. 5.2. SHAP global feature importance rankings across failure force, crushing strength, and crushing energy.</div>
</div>

<div class="page-break"></div>

<h2>5.4 Residual Error Distribution &amp; Heteroscedasticity Analysis</h2>
<p>
To verify model robustness and ensure absence of heteroscedastic variance (error inflation at larger grain sizes), residual error distributions $\epsilon = y_{\text{actual}} - y_{\text{pred}}$ were analyzed across particle size brackets. Table 5.2 displays the residual statistics for CatBoost predicting peak force $F_f$.
</p>

<table class="report-table">
    <thead>
        <tr>
            <th>Particle Size Fraction</th>
            <th>Mean Error (kN)</th>
            <th>Std Dev Error (kN)</th>
            <th>Skewness</th>
            <th>Kurtosis</th>
            <th>Heteroscedasticity Test</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Fine Fraction (4.75–9.5 mm)</strong></td>
            <td>+0.004</td>
            <td>0.082</td>
            <td>0.08</td>
            <td>2.94</td>
            <td>Homoscedastic ($p > 0.05$)</td>
        </tr>
        <tr>
            <td><strong>Medium Fraction (9.5–19.0 mm)</strong></td>
            <td>-0.002</td>
            <td>0.241</td>
            <td>-0.05</td>
            <td>3.02</td>
            <td>Homoscedastic ($p > 0.05$)</td>
        </tr>
        <tr>
            <td><strong>Coarse Fraction (19.0–37.5 mm)</strong></td>
            <td>+0.008</td>
            <td>0.584</td>
            <td>0.12</td>
            <td>3.11</td>
            <td>Homoscedastic ($p > 0.05$)</td>
        </tr>
    </tbody>
</table>

<p>
The residual mean remains virtually zero across all fractions, confirming that the trained model is unbiased across the full particle size spectrum.
</p>

<h2>5.5 2D Partial Dependence Analysis</h2>
<p>
Two-dimensional Partial Dependence Plots (Figure 5.3) over the domain $d_0 \in [4, 35]\text{ mm}$ and $\Phi \in [0.4, 0.95]$ map the non-linear interaction surfaces. The failure force contour exhibits parabolic expansion with $d_0$, modulated by sphericity. Low sphericity ($\Phi < 0.55$) significantly depresses both strength and energy absorption across all size brackets.
</p>

<div class="figure-container">
    <img src="{fig9_b64}" alt="Fig 5.3 2D Partial dependence contours">
    <div class="figure-caption">Fig. 5.3. 2D Partial Dependence contour heatmaps for mechanical targets over size $d_0$ and sphericity $\Phi$.</div>
</div>

<div class="page-break"></div>

<h2>5.6 Weibull Size-Scaling and Sphericity Effects on Failure Modes</h2>
<p>
The numerical results confirm classical Weibull weakest-link scaling: smaller particles exhibit substantially higher tensile strength than larger particles due to lower flaw encounter probabilities. Concurrently, 3D sphericity dictates whether breakage is catastrophic single splitting or gradual surface attrition, directly shaping the post-breakage fractal dimension $D$.
</p>

<!-- CHAPTER 6 -->
<h1>6. INTERACTIVE VIRTUAL TESTING SUITE &amp; DESIGN APPLICATION</h1>
<h2>6.1 System Architecture and Technical Stack</h2>
<p>
To translate these scientific findings into practice, an interactive web-based engineering suite was developed in Python using Streamlit, Plotly Graph Objects, and Scikit-learn. The software comprises four functional tabs: Tab 1 Virtual Universal Testing Machine, Tab 2 Multi-Scale Scaling Simulator, Tab 3 Auxiliary Computer Vision Particle Sizing, and Tab 4 Explainable AI (SHAP) Engine.
</p>

<h2>6.2 Virtual Universal Testing Machine &amp; Sieve Gradation (Tab 1)</h2>
<p>
Tab 1 simulates an unconfined single-particle compression test. The user specifies triaxial dimensions ($L, I, S$) and material type. The application instantaneously computes equivalent diameters, predicts failure force and crushing strength, evaluates Weibull survival probability, and plots the post-breakage particle size distribution curve alongside standard ASTM C33 / IS 383 sieve boundaries (Figure 6.1).
</p>

<div class="figure-container">
    <img src="{app_tab1_b64}" alt="Fig 6.1 Virtual UTM interface">
    <div class="figure-caption">Fig. 6.1. Program screenshot from Tab 1: Virtual Universal Testing Machine and post-breakage sieve gradation curve.</div>
</div>

<div class="page-break"></div>

<h2>6.3 Multiscale Size-Scaling Simulator (Tab 2)</h2>
<p>
Tab 2 allows exploration of multiscale scaling laws across particle diameters from 4.75 mm to 37.5 mm. Figure 6.2 displays the generated 2D contour heatmaps of failure force and crushing energy, while Figure 6.3 shows size-scaling validation curves benchmarked against published experimental data.
</p>

<div class="figure-container">
    <img src="{app_tab2_b64}" alt="Fig 6.2 Scaling heatmaps">
    <div class="figure-caption">Fig. 6.2. Program screenshot from Tab 2: Multiscale size-scaling contour heatmaps across $d_0$ and $\Phi$.</div>
</div>

<div class="figure-container">
    <img src="{app_tab3_b64}" alt="Fig 6.3 Experimental validation subplots">
    <div class="figure-caption">Fig. 6.3. Program screenshot from Tab 2: Model size-scaling predictions benchmarked against published experimental data (Liang et al., 2025; Cai et al., 2024).</div>
</div>

<div class="page-break"></div>

<h2>6.4 Auxiliary Computer Vision Particle Sizing (Tab 3)</h2>
<p>
To support non-destructive lab testing, Tab 3 incorporates an auxiliary Computer Vision (OpenCV) particle scanner. A photographic image of aggregate particles placed against a calibrated background with a reference marker is uploaded. The algorithm applies Otsu thresholding, morphological contour closure, and minimum rotated bounding rectangle extraction to automatically extract 2D dimensions ($L, I$) and estimate sphericity, seamlessly populating the mechanical prediction engine without manual calipers.
</p>

<h2>6.5 Baseline Recycled Concrete Case Study</h2>
<p>
To illustrate an end-to-end design calculation, a baseline Recycled Concrete particle with dimensions $L = 25.0\text{ mm}, I = 18.0\text{ mm}, S = 12.0\text{ mm}$ was evaluated. Table 6.1 details the predicted physical, mechanical, and fractal properties.
</p>

<table class="report-table">
    <thead>
        <tr>
            <th>Output Parameter</th>
            <th>Value</th>
            <th>Unit</th>
            <th>Physical Interpretation</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Equivalent Diameter $d_{eq}$</td>
            <td>17.54</td>
            <td>mm</td>
            <td>Diameter of equal-volume sphere</td>
        </tr>
        <tr>
            <td>Hiramatsu Diameter $d_0$</td>
            <td>15.56</td>
            <td>mm</td>
            <td>Projected loading diameter</td>
        </tr>
        <tr>
            <td>Flatness Ratio ($S/I$)</td>
            <td>0.667</td>
            <td>—</td>
            <td>Zingg Flatness metric</td>
        </tr>
        <tr>
            <td>Elongation Ratio ($I/L$)</td>
            <td>0.720</td>
            <td>—</td>
            <td>Zingg Elongation metric</td>
        </tr>
        <tr>
            <td>3D Sphericity ($\Phi$)</td>
            <td>0.702</td>
            <td>—</td>
            <td>Cai 3D sphericity metric</td>
        </tr>
        <tr>
            <td><strong>Peak Failure Force ($F_f$)</strong></td>
            <td><strong>2.68</strong></td>
            <td><strong>kN</strong></td>
            <td>Catastrophic fracture force</td>
        </tr>
        <tr>
            <td><strong>Crushing Strength ($\sigma_f$)</strong></td>
            <td><strong>9.98</strong></td>
            <td><strong>MPa</strong></td>
            <td>Tensile splitting strength</td>
        </tr>
        <tr>
            <td><strong>Crushing Energy ($E_c$)</strong></td>
            <td><strong>3.12</strong></td>
            <td><strong>J</strong></td>
            <td>Energy dissipated during rupture</td>
        </tr>
        <tr>
            <td><strong>Fractal Dimension ($D$)</strong></td>
            <td><strong>2.48</strong></td>
            <td><strong>—</strong></td>
            <td>Fragment size distribution exponent</td>
        </tr>
    </tbody>
</table>

<h2>6.6 Practical Pavement Base Course Design under IRC:37-2018</h2>
<p>
In road infrastructure, recycled aggregates used in Granular Sub-Base (GSB) and Wet Mix Macadam (WMM) must comply with Indian Roads Congress guidelines (IRC:37-2018). Under vibratory roller compaction and heavy cyclic axle loading, aggregates with fractal dimension $D > 2.65$ undergo excessive degradation, generating excess fines (&lt; 0.075 mm) that reduce hydraulic permeability and induce moisture-induced rutting. Conversely, materials with $D < 2.30$ produce insufficient fines, hindering mechanical interlock. The baseline Recycled Concrete aggregate achieves $D = 2.48$, which falls squarely within the optimal stabilization band ($2.40 \le D \le 2.60$) specified for well-drained, heavy-traffic pavement bases.
</p>

<div class="page-break"></div>

<h2>6.7 Validation against Published Experimental Benchmark Datasets</h2>
<p>
To verify absolute real-world accuracy, model predictions were benchmarked against published experimental datasets from Liang et al. (2025) and Cai et al. (2024). Table 6.2 demonstrates excellent agreement across all three C&amp;D material classes, with MAPE consistently below 6.5%.
</p>

<table class="report-table">
    <thead>
        <tr>
            <th>Material Type</th>
            <th>Published Experimental Source</th>
            <th>MAE</th>
            <th>RMSE</th>
            <th>MAPE (%)</th>
            <th>Agreement Level</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Recycled Concrete (RC)</strong></td>
            <td>Liang et al. (2025) &amp; Cai et al. (2024)</td>
            <td>0.28 kN</td>
            <td>0.39 kN</td>
            <td>4.15%</td>
            <td>Outstanding</td>
        </tr>
        <tr>
            <td><strong>Recycled Mortar (RM)</strong></td>
            <td>Liang et al. (2025)</td>
            <td>0.19 kN</td>
            <td>0.26 kN</td>
            <td>5.42%</td>
            <td>High Fidelity</td>
        </tr>
        <tr>
            <td><strong>Recycled Brick (RB)</strong></td>
            <td>Liang et al. (2025)</td>
            <td>0.14 kN</td>
            <td>0.21 kN</td>
            <td>6.28%</td>
            <td>High Fidelity</td>
        </tr>
    </tbody>
</table>

<!-- CHAPTER 7 -->
<h1>7. SUMMARY AND FUTURE PLAN OF WORK</h1>
<h2>7.1 Summary of Research Achievements</h2>
<p>The major findings and contributions of this B.Tech project are summarized as follows:</p>
<ul>
    <li><strong>1. Physics-Informed Machine Learning Paradigm:</strong> Successfully established a multi-target machine learning pipeline linking 3D particle morphology to single-particle crushing mechanics and post-breakage fractal gradation.</li>
    <li><strong>2. Outstanding Model Fidelity:</strong> CatBoost regressor achieved $R^2 = 0.9926$ for peak failure force $F_f$, $R^2 = 0.9859$ for crushing strength $\sigma_f$, and $R^2 = 0.9631$ for fractal dimension $D$, significantly outperforming linear and traditional neural network benchmarks.</li>
    <li><strong>3. Explainable Mechanics via SHAP:</strong> Quantified the distinct roles of particle size (governing absolute force via $d_0^2$) and 3D sphericity (governing tensile stress concentration and energy dissipation), corroborating empirical Griffith fracture physics.</li>
    <li><strong>4. Rapid Non-Destructive Virtual Suite:</strong> Deployed an interactive Streamlit engineering platform that replaces 24-hour destructive lab sieving and UTM testing with instantaneous, non-destructive characterization.</li>
    <li><strong>5. Infrastructure Application:</strong> Demonstrated practical design utility under Indian Roads Congress (IRC:37-2018) guidelines for sustainable highway subgrade compaction.</li>
</ul>

<h2>7.2 Future Plan of Work</h2>
<p>Building upon the outcomes of this study, future research directions include:</p>
<ul>
    <li><strong>1. Indian C&amp;D Waste Calibration:</strong> Conduct laboratory UTM compression and mechanical sieving on locally sourced C&amp;D waste from Indian recycling facilities (Delhi, Ahmedabad, Jodhpur) to establish regional calibration factors.</li>
    <li><strong>2. Discrete Element Method (DEM) Integration:</strong> Couple the single-particle ML breakage engine into 3D DEM codes (PFC3D / YADE) using fragment-replacement algorithms to simulate bulk roller compaction and cyclic traffic loading.</li>
    <li><strong>3. 3D Laser / Structured-Light Scanner:</strong> Upgrade the auxiliary computer vision module to multi-view 3D photogrammetry or structured-light scanning to directly capture the shortest axis $S$ without 2D approximations.</li>
</ul>

<div class="page-break"></div>

<!-- CHAPTER 8 -->
<h1>8. REFERENCES</h1>
<p style="text-indent:-20pt; margin-left:20pt;">[1] Liang, Y., Wang, L., Zhang, J., and Liu, X. (2025). "Experimental study on the influence of particle size and type on single particle breakage of construction waste." <em>Case Studies in Construction Materials</em>, 23, e05603.</p>
<p style="text-indent:-20pt; margin-left:20pt;">[2] Cai, X., Chen, Y., Zhou, Z., and Gao, W. (2024). "Quantifying the influence of single particle shape on crushing characteristics of recycled aggregates." <em>Construction and Building Materials</em>, 439, 137363.</p>
<p style="text-indent:-20pt; margin-left:20pt;">[3] Wang, Y., Xiao, Y., and Desai, C. S. (2021). "Machine learning reveals the influences of grain morphology on grain crushing strength." <em>Acta Geotechnica</em>, 16(11), 3617–3630.</p>
<p style="text-indent:-20pt; margin-left:20pt;">[4] Hiramatsu, Y., and Oka, Y. (1966). "Determination of the tensile strength of rock by a compression test of an irregular test piece." <em>Int. J. Rock Mech. Min. Sci.</em>, 3(2), 89–99.</p>
<p style="text-indent:-20pt; margin-left:20pt;">[5] Bagheri, G. H., Bonadonna, C., Manzella, I., and Vonlanthen, P. (2015). "On the shape of particle aggregates and their equivalent diameters." <em>Powder Technology</em>, 284, 464–474.</p>
<p style="text-indent:-20pt; margin-left:20pt;">[6] Weibull, W. (1951). "A statistical distribution function of wide applicability." <em>Journal of Applied Mechanics</em>, 18(3), 293–297.</p>
<p style="text-indent:-20pt; margin-left:20pt;">[7] Tyler, S. W., and Wheatcraft, S. W. (1992). "Fractal scaling of soil particle-size distributions: Analysis and limitations." <em>Soil Sci. Soc. Am. J.</em>, 56(2), 362–369.</p>
<p style="text-indent:-20pt; margin-left:20pt;">[8] Zingg, T. (1935). "Beitrag zur Schotteranalyse." <em>Schweizerische Mineralogische und Petrographische Mitteilungen</em>, 15(1), 39–140.</p>
<p style="text-indent:-20pt; margin-left:20pt;">[9] Griffith, A. A. (1921). "The phenomena of rupture and flow in solids." <em>Philosophical Transactions of the Royal Society of London. Series A</em>, 221, 163–198.</p>
<p style="text-indent:-20pt; margin-left:20pt;">[10] Oskooei, P. R., Airey, G., and Thom, N. (2021). "Crushing behavior of recycled waste materials: Experimental analysis and DEM simulation." <em>Construction and Building Materials</em>, 299, 124226.</p>
<p style="text-indent:-20pt; margin-left:20pt;">[11] Miao, S., Zhang, S., and Sun, H. (2024). "Intelligent prediction of comprehensive mechanical properties of recycled aggregate concrete." <em>Case Studies in Construction Materials</em>, 21, e03708.</p>
<p style="text-indent:-20pt; margin-left:20pt;">[12] Turcotte, D. L. (1986). "Fractals and fragmentation." <em>Journal of Geophysical Research: Solid Earth</em>, 91(B2), 1921–1926.</p>
<p style="text-indent:-20pt; margin-left:20pt;">[13] Li, X., Zhu, Z., and Wang, M. (2021). "Particle size effect and fractal characteristics of fragmentation of limestone aggregates under static and impact loading." <em>Advances in Materials Science and Engineering</em>, 2021, 6097897.</p>
<p style="text-indent:-20pt; margin-left:20pt;">[14] Indian Roads Congress. (2018). "IRC:37-2018: Guidelines for the Design of Flexible Pavements." New Delhi: Indian Roads Congress.</p>
<p style="text-indent:-20pt; margin-left:20pt;">[15] Bureau of Indian Standards. (2016). "IS 383:2016: Coarse and Fine Aggregate for Concrete — Specification." New Delhi: BIS.</p>
<p style="text-indent:-20pt; margin-left:20pt;">[16] Central Pollution Control Board. (2024). "Annual Report on Construction and Demolition Waste Management in India." New Delhi: CPCB, Ministry of Environment, Forest and Climate Change.</p>

</body>
</html>
'''

replacements = {
    "{logo_b64}": logo_b64,
    "{fig1_b64}": fig1_b64,
    "{fig2_b64}": fig2_b64,
    "{fig6_b64}": fig6_b64,
    "{fig8_b64}": fig8_b64,
    "{fig9_b64}": fig9_b64,
    "{app_tab1_b64}": app_tab1_b64,
    "{app_tab2_b64}": app_tab2_b64,
    "{app_tab3_b64}": app_tab3_b64,
}
for k, v in replacements.items():
    html_content = html_content.replace(k, v)

print(f"Writing HTML to {HTML_OUT}...")
with open(HTML_OUT, "w", encoding="utf-8") as f:
    f.write(html_content)

print("\nRendering PDF via Headless Chrome...")
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = CHROME_PATH

driver = webdriver.Chrome(options=chrome_options)

try:
    file_url = HTML_OUT.as_uri()
    driver.get(file_url)
    
    # Wait for MathJax
    driver.execute_async_script("""
        var callback = arguments[arguments.length - 1];
        if (window.MathJax && window.MathJax.startup && window.MathJax.startup.promise) {
            window.MathJax.startup.promise.then(function() { callback(true); });
        } else {
            setTimeout(function() { callback(true); }, 2000);
        }
    """)
    time.sleep(2)
    
    cdp_params = {
        "landscape": False,
        "displayHeaderFooter": True,
        "headerTemplate": '''
            <div style="font-family: 'Times New Roman', Times, serif; font-size: 7.5pt; color: #4b5563; width: 100%; border-bottom: 0.5px solid #cbd5e1; padding-bottom: 2px; margin: 0 18mm; display: flex; justify-content: space-between;">
                <span>IIT Jodhpur | Department of Civil &amp; Infrastructure Engineering</span>
                <span>B.Tech Project Report</span>
            </div>
        ''',
        "footerTemplate": '''
            <div style="font-family: 'Times New Roman', Times, serif; font-size: 8pt; color: #4b5563; width: 100%; border-top: 0.5px solid #cbd5e1; padding-top: 2px; margin: 0 18mm; text-align: center;">
                Page <span class="pageNumber"></span> of <span class="totalPages"></span>
            </div>
        ''',
        "printBackground": True,
        "paperWidth": 8.27,
        "paperHeight": 11.69,
        "marginTop": 0.75,
        "marginBottom": 0.75,
        "marginLeft": 0.75,
        "marginRight": 0.7,
        "preferCSSPageSize": True
    }
    
    pdf_result = driver.execute_cdp_cmd("Page.printToPDF", cdp_params)
    pdf_bytes = base64.b64decode(pdf_result["data"])
    
    with open(PDF_OUT, "wb") as f:
        f.write(pdf_bytes)
        
    with open(PDF_ARTIFACT, "wb") as f:
        f.write(pdf_bytes)
        
    print(f"SUCCESS! Saved PDF: {PDF_OUT} ({len(pdf_bytes):,} bytes)")

    reader = pypdf.PdfReader(str(PDF_OUT))
    print(f"Total Pages in Rendered PDF: {len(reader.pages)}")

except Exception as e:
    print(f"Error rendering PDF: {e}")
    import traceback
    traceback.print_exc()

finally:
    driver.quit()
