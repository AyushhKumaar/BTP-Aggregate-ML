"""
sync_page_numbers.py
Synchronizes exact chapter page numbers across build_iitj_report_v2.py and render_iitj_pdf_v2.py.
"""

from pathlib import Path

# 1. Update build_iitj_report_v2.py
docx_script = Path(r"c:\Users\Ayush\Documents\BTP_Aggregate_ML\scratch\build_iitj_report_v2.py")
text = docx_script.read_text(encoding="utf-8")

# Replace page numbers in toc_items
toc_replacements = [
    ('("1. INTRODUCTION", "1")', '("1. INTRODUCTION", "1")'),
    ('("    1.1 Infrastructure Demand and Construction Waste Crisis", "1")', '("    1.1 Infrastructure Demand and Construction Waste Crisis", "1")'),
    ('("    1.2 Geotechnical Limitations of Recycled Aggregates", "2")', '("    1.2 Geotechnical Limitations of Recycled Aggregates", "1")'),
    ('("    1.3 Machine Learning and Computational Granular Mechanics", "2")', '("    1.3 Machine Learning and Computational Granular Mechanics", "2")'),
    ('("2. LITERATURE SURVEY", "3")', '("2. LITERATURE SURVEY", "2")'),
    ('("    2.1 Single-Particle Rock Mechanics vs. Bulk Standard Tests (IS 2386 / ASTM C131)", "3")', '("    2.1 Single-Particle Rock Mechanics vs. Bulk Standard Tests (IS 2386 / ASTM C131)", "2")'),
    ('("    2.2 Microstructure and Interfacial Transition Zone (ITZ) in C&D Aggregates", "4")', '("    2.2 Microstructure and Interfacial Transition Zone (ITZ) in C&D Aggregates", "3")'),
    ('("    2.3 3D Morphological Characterization & Zingg Classification", "4")', '("    2.3 3D Morphological Characterization & Zingg Classification", "3")'),
    ('("    2.4 Weibull Weakest-Link Size Scaling & Fractal Fragmentation", "5")', '("    2.4 Weibull Weakest-Link Size Scaling & Fractal Fragmentation", "3")'),
    ('("    2.5 Machine Learning & Explainable AI in Granular Geomechanics", "6")', '("    2.5 Machine Learning & Explainable AI in Granular Geomechanics", "4")'),
    ('("3. PROBLEM DEFINITION & OBJECTIVES", "7")', '("3. PROBLEM DEFINITION & OBJECTIVES", "4")'),
    ('("    3.1 Problem Definition", "7")', '("    3.1 Problem Definition", "4")'),
    ('("    3.2 Research Objectives", "7")', '("    3.2 Research Objectives", "4")'),
    ('("    3.3 Scope and Technical Boundaries", "8")', '("    3.3 Scope and Technical Boundaries", "4")'),
    ('("4. METHODOLOGY", "9")', '("4. METHODOLOGY", "5")'),
    ('("    4.1 Physics-Coupled Benchmark Dataset Generation", "9")', '("    4.1 Physics-Coupled Benchmark Dataset Generation", "5")'),
    ('("        4.1.1 Material Properties and Morphological Characterization", "9")', '("        4.1.1 Material Properties and Morphological Characterization", "5")'),
    ('("        4.1.2 Governing Fracture Formulations (Hiramatsu-Oka & Bagheri)", "10")', '("        4.1.2 Governing Fracture Formulations (Hiramatsu-Oka & Bagheri)", "6")'),
    ('("        4.1.3 Weibull Size-Scaling and Shape Power Laws", "11")', '("        4.1.3 Weibull Size-Scaling and Shape Power Laws", "6")'),
    ('("        4.1.4 Scale-Invariant Fractal Gradation", "11")', '("        4.1.4 Scale-Invariant Fractal Gradation", "7")'),
    ('("    4.2 Machine Learning Architecture and Training Pipeline", "12")', '("    4.2 Machine Learning Architecture and Training Pipeline", "8")'),
    ('("        4.2.1 16-Dimensional Feature Space and Stratified Data Partitioning", "12")', '("        4.2.1 16-Dimensional Feature Space and Stratified Data Partitioning", "8")'),
    ('("        4.2.2 Machine Learning Regressors & Hyperparameter Optimization", "13")', '("        4.2.2 Machine Learning Regressors & Hyperparameter Optimization", "8")'),
    ('("        4.2.3 Model Evaluation Metrics", "13")', '("        4.2.3 Model Evaluation Metrics", "8")'),
    ('("5. NUMERICAL & MACHINE LEARNING FINDINGS", "14")', '("5. NUMERICAL & MACHINE LEARNING FINDINGS", "9")'),
    ('("    5.1 Model Performance Benchmarks across Target Variables", "14")', '("    5.1 Model Performance Benchmarks across Target Variables", "9")'),
    ('("    5.2 Actual vs. Predicted Parity Analysis", "15")', '("    5.2 Actual vs. Predicted Parity Analysis", "10")'),
    ('("    5.3 Explainable AI (SHAP) Feature Attribution", "16")', '("    5.3 Explainable AI (SHAP) Feature Attribution", "11")'),
    ('("    5.4 Residual Error Distribution & Heteroscedasticity Analysis", "17")', '("    5.4 Residual Error Distribution & Heteroscedasticity Analysis", "12")'),
    ('("    5.5 2D Partial Dependence Analysis", "18")', '("    5.5 2D Partial Dependence Analysis", "12")'),
    ('("    5.6 Weibull Size-Scaling and Sphericity Effects on Failure Modes", "19")', '("    5.6 Weibull Size-Scaling and Sphericity Effects on Failure Modes", "13")'),
    ('("6. INTERACTIVE VIRTUAL TESTING SUITE & DESIGN APPLICATION", "20")', '("6. INTERACTIVE VIRTUAL TESTING SUITE & DESIGN APPLICATION", "13")'),
    ('("    6.1 System Architecture and Technical Stack", "20")', '("    6.1 System Architecture and Technical Stack", "13")'),
    ('("    6.2 Virtual Universal Testing Machine & Sieve Gradation (Tab 1)", "20")', '("    6.2 Virtual Universal Testing Machine & Sieve Gradation (Tab 1)", "13")'),
    ('("    6.3 Multiscale Size-Scaling Simulator (Tab 2)", "21")', '("    6.3 Multiscale Size-Scaling Simulator (Tab 2)", "14")'),
    ('("    6.4 Auxiliary Computer Vision Particle Sizing (Tab 3)", "22")', '("    6.4 Auxiliary Computer Vision Particle Sizing (Tab 3)", "15")'),
    ('("    6.5 Baseline Recycled Concrete Case Study", "22")', '("    6.5 Baseline Recycled Concrete Case Study", "15")'),
    ('("    6.6 Practical Pavement Base Course Design under IRC:37-2018", "23")', '("    6.6 Practical Pavement Base Course Design under IRC:37-2018", "15")'),
    ('("    6.7 Validation against Published Experimental Benchmark Datasets", "24")', '("    6.7 Validation against Published Experimental Benchmark Datasets", "16")'),
    ('("7. SUMMARY AND FUTURE PLAN OF WORK", "25")', '("7. SUMMARY AND FUTURE PLAN OF WORK", "16")'),
    ('("    7.1 Summary of Research Achievements", "25")', '("    7.1 Summary of Research Achievements", "16")'),
    ('("    7.2 Future Plan of Work", "25")', '("    7.2 Future Plan of Work", "16")'),
    ('("8. REFERENCES", "26")', '("8. REFERENCES", "17")'),
]

for old, new in toc_replacements:
    text = text.replace(old, new)

# Update figures list in docx
fig_replacements = [
    ('("Fig. 4.1", "Zingg 3D particle shape classification and aspect ratio domains (Flat, Equant, Blade, Elongated)", "10")',
     '("Fig. 4.1", "Zingg 3D particle shape classification and aspect ratio domains (Flat, Equant, Blade, Elongated)", "5")'),
    ('("Fig. 4.2", "Weibull survival probability distributions across particle size fractions (4.75–9.5 mm, 9.5–19.0 mm, 19.0–37.5 mm)", "11")',
     '("Fig. 4.2", "Weibull survival probability distributions across particle size fractions (4.75–9.5 mm, 9.5–19.0 mm, 19.0–37.5 mm)", "6")'),
    ('("Fig. 5.1", "Actual vs. predicted parity plots across mechanical targets on test set (R² >= 0.96 across all targets)", "15")',
     '("Fig. 5.1", "Actual vs. predicted parity plots across mechanical targets on test set (R² >= 0.96 across all targets)", "10")'),
    ('("Fig. 5.2", "SHAP global feature importance rankings across failure force, crushing strength, and crushing energy", "16")',
     '("Fig. 5.2", "SHAP global feature importance rankings across failure force, crushing strength, and crushing energy", "11")'),
    ('("Fig. 5.3", "2D Partial Dependence contour heatmaps for mechanical targets over size d₀ and sphericity Φ", "18")',
     '("Fig. 5.3", "2D Partial Dependence contour heatmaps for mechanical targets over size d₀ and sphericity Φ", "12")'),
    ('("Fig. 6.1", "Program screenshot from Tab 1: Virtual Universal Testing Machine and post-breakage sieve gradation curve", "20")',
     '("Fig. 6.1", "Program screenshot from Tab 1: Virtual Universal Testing Machine and post-breakage sieve gradation curve", "13")'),
    ('("Fig. 6.2", "Program screenshot from Tab 2: Multiscale size-scaling contour heatmaps across d₀ and Φ", "21")',
     '("Fig. 6.2", "Program screenshot from Tab 2: Multiscale size-scaling contour heatmaps across d₀ and Φ", "14")'),
    ('("Fig. 6.3", "Program screenshot from Tab 2: Model size-scaling predictions benchmarked against published experimental data", "21")',
     '("Fig. 6.3", "Program screenshot from Tab 2: Model size-scaling predictions benchmarked against published experimental data", "14")'),
]
for old, new in fig_replacements:
    text = text.replace(old, new)

# Update tables list in docx
tbl_replacements = [
    ('("Table 4.1", "Empirical calibration parameters for recycled aggregate materials (RC, RM, RB)", "10")',
     '("Table 4.1", "Empirical calibration parameters for recycled aggregate materials (RC, RM, RB)", "5")'),
    ('("Table 4.2", "Machine learning regressor hyperparameter grids and 5-fold cross-validation configurations", "13")',
     '("Table 4.2", "Machine learning regressor hyperparameter grids and 5-fold cross-validation configurations", "8")'),
    ('("Table 5.1", "Performance comparison of machine learning regression models on hold-out test set", "14")',
     '("Table 5.1", "Performance comparison of machine learning regression models on hold-out test set", "9")'),
    ('("Table 5.2", "Error residual distribution and heteroscedasticity metrics across particle size fractions", "17")',
     '("Table 5.2", "Error residual distribution and heteroscedasticity metrics across particle size fractions", "12")'),
    ('("Table 6.1", "End-to-end design case study: Virtual characterization of Recycled Concrete aggregate", "23")',
     '("Table 6.1", "End-to-end design case study: Virtual characterization of Recycled Concrete aggregate", "15")'),
    ('("Table 6.2", "Validation of virtual testing suite against published experimental benchmark datasets", "24")',
     '("Table 6.2", "Validation of virtual testing suite against published experimental benchmark datasets", "16")'),
]
for old, new in tbl_replacements:
    text = text.replace(old, new)

docx_script.write_text(text, encoding="utf-8")
print("Updated build_iitj_report_v2.py successfully.")

# 2. Update HTML
html_file = Path(r"c:\Users\Ayush\Documents\BTP_Aggregate_ML\docs\BTP_IITJ_Final_Report.html")
html_text = html_file.read_text(encoding="utf-8")

# Update HTML TOC spans
html_replacements = [
    ('<span>1. INTRODUCTION</span><span class="dots"></span><span>1</span>', '<span>1. INTRODUCTION</span><span class="dots"></span><span>1</span>'),
    ('<span>1.1 Infrastructure Demand and Construction Waste Crisis</span><span class="dots"></span><span>1</span>', '<span>1.1 Infrastructure Demand and Construction Waste Crisis</span><span class="dots"></span><span>1</span>'),
    ('<span>1.2 Geotechnical Limitations of Recycled Aggregates</span><span class="dots"></span><span>2</span>', '<span>1.2 Geotechnical Limitations of Recycled Aggregates</span><span class="dots"></span><span>1</span>'),
    ('<span>1.3 Machine Learning and Computational Granular Mechanics</span><span class="dots"></span><span>2</span>', '<span>1.3 Machine Learning and Computational Granular Mechanics</span><span class="dots"></span><span>2</span>'),
    ('<span>2. LITERATURE SURVEY</span><span class="dots"></span><span>3</span>', '<span>2. LITERATURE SURVEY</span><span class="dots"></span><span>2</span>'),
    ('<span>2.1 Single-Particle Rock Mechanics vs. Bulk Standard Tests (IS 2386 / ASTM C131)</span><span class="dots"></span><span>3</span>', '<span>2.1 Single-Particle Rock Mechanics vs. Bulk Standard Tests (IS 2386 / ASTM C131)</span><span class="dots"></span><span>2</span>'),
    ('<span>2.2 Microstructure and Interfacial Transition Zone (ITZ) in C&amp;D Aggregates</span><span class="dots"></span><span>4</span>', '<span>2.2 Microstructure and Interfacial Transition Zone (ITZ) in C&amp;D Aggregates</span><span class="dots"></span><span>3</span>'),
    ('<span>2.3 3D Morphological Characterization &amp; Zingg Classification</span><span class="dots"></span><span>4</span>', '<span>2.3 3D Morphological Characterization &amp; Zingg Classification</span><span class="dots"></span><span>3</span>'),
    ('<span>2.4 Weibull Weakest-Link Size Scaling &amp; Fractal Fragmentation</span><span class="dots"></span><span>5</span>', '<span>2.4 Weibull Weakest-Link Size Scaling &amp; Fractal Fragmentation</span><span class="dots"></span><span>3</span>'),
    ('<span>2.5 Machine Learning &amp; Explainable AI in Granular Geomechanics</span><span class="dots"></span><span>6</span>', '<span>2.5 Machine Learning &amp; Explainable AI in Granular Geomechanics</span><span class="dots"></span><span>4</span>'),
    ('<span>3. PROBLEM DEFINITION &amp; OBJECTIVES</span><span class="dots"></span><span>7</span>', '<span>3. PROBLEM DEFINITION &amp; OBJECTIVES</span><span class="dots"></span><span>4</span>'),
    ('<span>3.1 Problem Definition</span><span class="dots"></span><span>7</span>', '<span>3.1 Problem Definition</span><span class="dots"></span><span>4</span>'),
    ('<span>3.2 Research Objectives</span><span class="dots"></span><span>7</span>', '<span>3.2 Research Objectives</span><span class="dots"></span><span>4</span>'),
    ('<span>3.3 Scope and Technical Boundaries</span><span class="dots"></span><span>8</span>', '<span>3.3 Scope and Technical Boundaries</span><span class="dots"></span><span>4</span>'),
    ('<span>4. METHODOLOGY</span><span class="dots"></span><span>9</span>', '<span>4. METHODOLOGY</span><span class="dots"></span><span>5</span>'),
    ('<span>4.1 Physics-Coupled Benchmark Dataset Generation</span><span class="dots"></span><span>9</span>', '<span>4.1 Physics-Coupled Benchmark Dataset Generation</span><span class="dots"></span><span>5</span>'),
    ('<span>4.1.1 Material Properties and Morphological Characterization</span><span class="dots"></span><span>9</span>', '<span>4.1.1 Material Properties and Morphological Characterization</span><span class="dots"></span><span>5</span>'),
    ('<span>4.1.2 Governing Fracture Formulations (Hiramatsu-Oka &amp; Bagheri)</span><span class="dots"></span><span>10</span>', '<span>4.1.2 Governing Fracture Formulations (Hiramatsu-Oka &amp; Bagheri)</span><span class="dots"></span><span>6</span>'),
    ('<span>4.1.3 Weibull Size-Scaling and Shape Power Laws</span><span class="dots"></span><span>11</span>', '<span>4.1.3 Weibull Size-Scaling and Shape Power Laws</span><span class="dots"></span><span>6</span>'),
    ('<span>4.1.4 Scale-Invariant Fractal Gradation</span><span class="dots"></span><span>11</span>', '<span>4.1.4 Scale-Invariant Fractal Gradation</span><span class="dots"></span><span>7</span>'),
    ('<span>4.2 Machine Learning Architecture and Training Pipeline</span><span class="dots"></span><span>12</span>', '<span>4.2 Machine Learning Architecture and Training Pipeline</span><span class="dots"></span><span>8</span>'),
    ('<span>4.2.1 16-Dimensional Feature Space and Stratified Data Partitioning</span><span class="dots"></span><span>12</span>', '<span>4.2.1 16-Dimensional Feature Space and Stratified Data Partitioning</span><span class="dots"></span><span>8</span>'),
    ('<span>4.2.2 Machine Learning Regressors &amp; Hyperparameter Optimization</span><span class="dots"></span><span>13</span>', '<span>4.2.2 Machine Learning Regressors &amp; Hyperparameter Optimization</span><span class="dots"></span><span>8</span>'),
    ('<span>4.2.3 Model Evaluation Metrics</span><span class="dots"></span><span>13</span>', '<span>4.2.3 Model Evaluation Metrics</span><span class="dots"></span><span>8</span>'),
    ('<span>5. NUMERICAL &amp; MACHINE LEARNING FINDINGS</span><span class="dots"></span><span>14</span>', '<span>5. NUMERICAL &amp; MACHINE LEARNING FINDINGS</span><span class="dots"></span><span>9</span>'),
    ('<span>5.1 Model Performance Benchmarks across Target Variables</span><span class="dots"></span><span>14</span>', '<span>5.1 Model Performance Benchmarks across Target Variables</span><span class="dots"></span><span>9</span>'),
    ('<span>5.2 Actual vs. Predicted Parity Analysis</span><span class="dots"></span><span>15</span>', '<span>5.2 Actual vs. Predicted Parity Analysis</span><span class="dots"></span><span>10</span>'),
    ('<span>5.3 Explainable AI (SHAP) Feature Attribution</span><span class="dots"></span><span>16</span>', '<span>5.3 Explainable AI (SHAP) Feature Attribution</span><span class="dots"></span><span>11</span>'),
    ('<span>5.4 Residual Error Distribution &amp; Heteroscedasticity Analysis</span><span class="dots"></span><span>17</span>', '<span>5.4 Residual Error Distribution &amp; Heteroscedasticity Analysis</span><span class="dots"></span><span>12</span>'),
    ('<span>5.5 2D Partial Dependence Analysis</span><span class="dots"></span><span>18</span>', '<span>5.5 2D Partial Dependence Analysis</span><span class="dots"></span><span>12</span>'),
    ('<span>5.6 Weibull Size-Scaling and Sphericity Effects on Failure Modes</span><span class="dots"></span><span>19</span>', '<span>5.6 Weibull Size-Scaling and Sphericity Effects on Failure Modes</span><span class="dots"></span><span>13</span>'),
    ('<span>6. INTERACTIVE VIRTUAL TESTING SUITE &amp; DESIGN APPLICATION</span><span class="dots"></span><span>20</span>', '<span>6. INTERACTIVE VIRTUAL TESTING SUITE &amp; DESIGN APPLICATION</span><span class="dots"></span><span>13</span>'),
    ('<span>6.1 System Architecture and Technical Stack</span><span class="dots"></span><span>20</span>', '<span>6.1 System Architecture and Technical Stack</span><span class="dots"></span><span>13</span>'),
    ('<span>6.2 Virtual Universal Testing Machine &amp; Sieve Gradation (Tab 1)</span><span class="dots"></span><span>20</span>', '<span>6.2 Virtual Universal Testing Machine &amp; Sieve Gradation (Tab 1)</span><span class="dots"></span><span>13</span>'),
    ('<span>6.3 Multiscale Size-Scaling Simulator (Tab 2)</span><span class="dots"></span><span>21</span>', '<span>6.3 Multiscale Size-Scaling Simulator (Tab 2)</span><span class="dots"></span><span>14</span>'),
    ('<span>6.4 Auxiliary Computer Vision Particle Sizing (Tab 3)</span><span class="dots"></span><span>22</span>', '<span>6.4 Auxiliary Computer Vision Particle Sizing (Tab 3)</span><span class="dots"></span><span>15</span>'),
    ('<span>6.5 Baseline Recycled Concrete Case Study</span><span class="dots"></span><span>22</span>', '<span>6.5 Baseline Recycled Concrete Case Study</span><span class="dots"></span><span>15</span>'),
    ('<span>6.6 Practical Pavement Base Course Design under IRC:37-2018</span><span class="dots"></span><span>23</span>', '<span>6.6 Practical Pavement Base Course Design under IRC:37-2018</span><span class="dots"></span><span>15</span>'),
    ('<span>6.7 Validation against Published Experimental Benchmark Datasets</span><span class="dots"></span><span>24</span>', '<span>6.7 Validation against Published Experimental Benchmark Datasets</span><span class="dots"></span><span>16</span>'),
    ('<span>7. SUMMARY AND FUTURE PLAN OF WORK</span><span class="dots"></span><span>25</span>', '<span>7. SUMMARY AND FUTURE PLAN OF WORK</span><span class="dots"></span><span>16</span>'),
    ('<span>7.1 Summary of Research Achievements</span><span class="dots"></span><span>25</span>', '<span>7.1 Summary of Research Achievements</span><span class="dots"></span><span>16</span>'),
    ('<span>7.2 Future Plan of Work</span><span class="dots"></span><span>25</span>', '<span>7.2 Future Plan of Work</span><span class="dots"></span><span>16</span>'),
    ('<span>8. REFERENCES</span><span class="dots"></span><span>26</span>', '<span>8. REFERENCES</span><span class="dots"></span><span>17</span>'),
]

for old, new in html_replacements:
    html_text = html_text.replace(old, new)

# HTML figures list
html_fig_replacements = [
    ('<span><strong>Fig. 4.1:</strong> Zingg 3D particle shape classification and aspect ratio domains</span><span class="dots"></span><span>10</span>',
     '<span><strong>Fig. 4.1:</strong> Zingg 3D particle shape classification and aspect ratio domains</span><span class="dots"></span><span>5</span>'),
    ('<span><strong>Fig. 4.2:</strong> Weibull survival probability distributions across particle size fractions</span><span class="dots"></span><span>11</span>',
     '<span><strong>Fig. 4.2:</strong> Weibull survival probability distributions across particle size fractions</span><span class="dots"></span><span>6</span>'),
    ('<span><strong>Fig. 5.1:</strong> Actual vs. predicted parity plots across mechanical targets on test set</span><span class="dots"></span><span>15</span>',
     '<span><strong>Fig. 5.1:</strong> Actual vs. predicted parity plots across mechanical targets on test set</span><span class="dots"></span><span>10</span>'),
    ('<span><strong>Fig. 5.2:</strong> SHAP global feature importance rankings across failure force, strength, energy</span><span class="dots"></span><span>16</span>',
     '<span><strong>Fig. 5.2:</strong> SHAP global feature importance rankings across failure force, strength, energy</span><span class="dots"></span><span>11</span>'),
    ('<span><strong>Fig. 5.3:</strong> 2D Partial Dependence contour heatmaps for mechanical targets</span><span class="dots"></span><span>18</span>',
     '<span><strong>Fig. 5.3:</strong> 2D Partial Dependence contour heatmaps for mechanical targets</span><span class="dots"></span><span>12</span>'),
    ('<span><strong>Fig. 6.1:</strong> Program screenshot from Tab 1: Virtual Universal Testing Machine and sieve curve</span><span class="dots"></span><span>20</span>',
     '<span><strong>Fig. 6.1:</strong> Program screenshot from Tab 1: Virtual Universal Testing Machine and sieve curve</span><span class="dots"></span><span>13</span>'),
    ('<span><strong>Fig. 6.2:</strong> Program screenshot from Tab 2: Multiscale size-scaling contour heatmaps</span><span class="dots"></span><span>21</span>',
     '<span><strong>Fig. 6.2:</strong> Program screenshot from Tab 2: Multiscale size-scaling contour heatmaps</span><span class="dots"></span><span>14</span>'),
    ('<span><strong>Fig. 6.3:</strong> Program screenshot from Tab 2: Model size-scaling benchmarked against experiments</span><span class="dots"></span><span>21</span>',
     '<span><strong>Fig. 6.3:</strong> Program screenshot from Tab 2: Model size-scaling benchmarked against experiments</span><span class="dots"></span><span>14</span>'),
]
for old, new in html_fig_replacements:
    html_text = html_text.replace(old, new)

# HTML tables list
html_tbl_replacements = [
    ('<span><strong>Table 4.1:</strong> Empirical calibration parameters for recycled aggregate materials (RC, RM, RB)</span><span class="dots"></span><span>10</span>',
     '<span><strong>Table 4.1:</strong> Empirical calibration parameters for recycled aggregate materials (RC, RM, RB)</span><span class="dots"></span><span>5</span>'),
    ('<span><strong>Table 4.2:</strong> Machine learning regressor hyperparameter grids and cross-validation setups</span><span class="dots"></span><span>13</span>',
     '<span><strong>Table 4.2:</strong> Machine learning regressor hyperparameter grids and cross-validation setups</span><span class="dots"></span><span>8</span>'),
    ('<span><strong>Table 5.1:</strong> Performance comparison of machine learning regression models on test set</span><span class="dots"></span><span>14</span>',
     '<span><strong>Table 5.1:</strong> Performance comparison of machine learning regression models on test set</span><span class="dots"></span><span>9</span>'),
    ('<span><strong>Table 5.2:</strong> Error residual distribution and heteroscedasticity metrics across size fractions</span><span class="dots"></span><span>17</span>',
     '<span><strong>Table 5.2:</strong> Error residual distribution and heteroscedasticity metrics across size fractions</span><span class="dots"></span><span>12</span>'),
    ('<span><strong>Table 6.1:</strong> End-to-end design case study: Virtual characterization of Recycled Concrete</span><span class="dots"></span><span>23</span>',
     '<span><strong>Table 6.1:</strong> End-to-end design case study: Virtual characterization of Recycled Concrete</span><span class="dots"></span><span>15</span>'),
    ('<span><strong>Table 6.2:</strong> Validation of virtual testing suite against published experimental benchmarks</span><span class="dots"></span><span>24</span>',
     '<span><strong>Table 6.2:</strong> Validation of virtual testing suite against published experimental benchmarks</span><span class="dots"></span><span>16</span>'),
]
for old, new in html_tbl_replacements:
    html_text = html_text.replace(old, new)

html_file.write_text(html_text, encoding="utf-8")
print("Updated BTP_IITJ_Final_Report.html successfully.")
