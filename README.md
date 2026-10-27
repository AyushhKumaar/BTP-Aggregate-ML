# Physics-Informed Machine Learning for Predicting Single-Particle Crushing Mechanics and Post-Breakage Fractal Gradation of Recycled Aggregates Across Multi-Scale Morphologies

**B.Tech Capstone Project (BTP)**  
*Department of Civil and Environmental Engineering*

---

## 📌 Project Overview
Sustainable circular economy infrastructure relies on the effective reuse of Construction and Demolition (C&D) waste as Recycled Aggregates (RA). However, physical Universal Testing Machine (UTM) crushing and post-breakage sieve analyses are destructive, time-consuming, expensive, and present occupational silicosis hazards.

This project delivers a **Physics-Informed Machine Learning (PIML)** framework that couples:
1. **Size-dependent Weibull fracture mechanics** (Liang et al., 2025)
2. **3D morphological shape & sphericity scaling** (Cai et al., 2024)
3. **Hiramatsu-Oka stress conversions and Bagheri contact gauge diameters**
4. **Tyler-Wheatcraft post-breakage fractal sieve gradation curves**

---

## 🚀 Key Features & Deliverables

* **Coupled Dataset ($N = 3,600$):** 1,200 samples each for Recycled Concrete (`RC`), Recycled Brick (`RB`), and Recycled Mortar (`RM`) across 34 multi-scale geometric, mechanical, and fractal targets.
* **Benchmarked ML Architectures:** 6 regression models (Ridge Polynomial, Random Forest, XGBoost, LightGBM, CatBoost, Physics-Informed MLP) achieving **$R^2 > 0.92$** on unseen test data.
  * **Top Performer:** CatBoost Regressor ($\text{Mean } R^2 = 0.9618$)
    * Crushing Strength $\sigma_f$: $R^2 = 0.9636$, $\text{MAPE} = 5.81\%$
    * Peak Rupture Force $F_f$: $R^2 = 0.9871$, $\text{MAPE} = 6.56\%$
    * Dissipated Crushing Energy $E_f$: $R^2 = 0.9498$, $\text{MAPE} = 9.13\%$
    * Post-Breakage Fractal Dimension $D$: $R^2 = 0.9469$, $\text{MAPE} = 1.37\%$
* **Breakage Mode Classifier:** Categorizes failure into Mode I (Splitting), Mode II (Corner Rupture), and Mode III (Bulk Fragmentation).
* **Inverse Design / Size & Shape Transformer:** Virtual quarry simulator scaling any single aggregate $(L_1, I_1, S_1)$ across scale factors ($4.75 \to 37.5\text{ mm}$) and Zingg classes (`Disk`, `Block`, `Blade`, `Bar`).
* **Interactive Streamlit Engineering Suite (`app.py`):** 4-tab interactive web lab with 3D Plotly particle previews, live virtual UTM curves, computer vision aggregate scanning, and SHAP explainability.
* **Publication Figures (300 DPI):** 9 high-resolution publication figures replicating and extending experimental findings from literature.
* **Comprehensive Academic Documentation:** 
  * 7,975-word BTP Capstone Final Report (`docs/BTP_Final_Report.md`).
  * 15-slide Viva Presentation Deck with speaker notes and examiner defense answers (`docs/Viva_Presentation_Slides.md`).

---

## 📂 Repository Directory Structure

```text
BTP_Aggregate_ML/
├── data/
│   ├── coupled_aggregate_breakage_dataset.csv  # Unified N=3,600 dataset
│   └── inverse_design_grid.csv                 # 2D Size x Shape scaling grid
├── docs/
│   ├── BTP_Final_Report.md                     # 7,975-word academic project report
│   ├── Viva_Presentation_Slides.md            # 15-slide defense deck with notes
│   ├── extracted_papers_notes.md               # Text & table extraction from PDFs
│   └── literature_synthesis.md                 # Cross-literature benchmark synthesis
├── results/
│   ├── figures/                                # 9 publication-grade 300 DPI figures
│   │   ├── fig1_zingg_shape_classification.png
│   │   ├── fig2_weibull_survival_curves.png
│   │   ├── fig3_strength_energy_vs_sphericity.png
│   │   ├── fig4_fractal_gradation_curves.png
│   │   ├── fig5_model_comparison_metrics.png
│   │   ├── fig6_actual_vs_predicted_parity.png
│   │   ├── fig7_breakage_mode_confusion_matrix.png
│   │   ├── fig8_shap_feature_importance.png
│   │   └── fig9_partial_dependence_contours.png
│   ├── models/                                 # Serialized model weights & scalers
│   ├── regression_metrics.csv                  # Full test benchmarks across 6 models
│   ├── classification_metrics.csv              # Breakage mode classification scores
│   └── metrics_summary.json                    # Machine-readable evaluation summary
├── src/
│   ├── data_generator.py                       # Physics-informed dataset generation
│   ├── train_models.py                         # Multi-task training & 300 DPI plotting
│   ├── inverse_designer.py                     # Size & Shape Transformer engine
│   ├── pdf_extractor.py                        # Automated PyMuPDF literature parser
│   └── populate_report_metrics.py              # Automated report metric populator
├── app.py                                      # 4-tab Streamlit web application
├── requirements.txt                            # Python dependencies
└── pyproject.toml                              # uv package configuration
```

---

## ⚡ Quickstart Guide

### 1. Environment Setup
```powershell
# Using Python 3.11 with pip
pip install -r requirements.txt
```

### 2. Regenerate Dataset (Optional)
```powershell
python src/data_generator.py
```

### 3. Retrain Models & Regenerate 300 DPI Figures (Optional)
```powershell
python src/train_models.py
```

### 4. Launch Interactive Streamlit Engineering Suite
```powershell
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📜 References
1. **Liang et al. (2025):** Experimental study on the influence of particle size and type on single particle breakage of construction waste. *Case Studies in Construction Materials*, 23, e05603.
2. **Cai et al. (2024):** Quantifying the influence of single particle shape on crushing characteristics of recycled aggregates: Experimental and numerical insights. *Construction and Building Materials*, 439, 137363.
3. **Wang et al. (2021):** Machine learning reveals the influences of grain morphology on grain crushing strength. *Acta Geotechnica*, 16, 3617–3630.
4. **Oskooei et al. (2021):** Crushing behavior of recycled waste materials: Experimental analysis and DEM simulation. *Construction and Building Materials*, 299, 124226.
5. **Miao et al. (2024):** Intelligent prediction of comprehensive mechanical properties of recycled aggregate concrete... *Case Studies in Construction Materials*, 21, e03708.
