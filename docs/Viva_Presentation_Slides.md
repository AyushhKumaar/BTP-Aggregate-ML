# Viva Voce Presentation: Physics-Informed Machine Learning for Recycled Aggregate Crushing Mechanics

**Project Title:** *Physics-Informed Machine Learning for Predicting Single-Particle Crushing Mechanics and Post-Breakage Fractal Gradation of Recycled Aggregates Across Multi-Scale Morphologies*  
**Candidate Name:** Ayush  
**Degree:** Bachelor of Technology in Civil and Environmental Engineering  
**Academic Session:** 2025–2026  
**Presentation Length:** 15 Slides (~20–25 Minutes Viva Defense)

---

## Slide 1: Title Slide & Global Motivation

### Slide Title
**Physics-Informed Machine Learning for Predicting Single-Particle Crushing Mechanics and Post-Breakage Fractal Gradation of Recycled Aggregates Across Multi-Scale Morphologies**

### Content
- **The Global Aggregate Crisis:**
  - Sand and crushed stone represent the second most consumed natural resource on Earth (>50 billion metric tonnes annually).
  - Virgin quarry and riverbed depletion causes severe riparian damage, groundwater depletion, and high haulage carbon footprints.
- **The Construction & Demolition (C&D) Waste Surge:**
  - Over 3.0 billion metric tonnes of C&D waste generated annually worldwide (China: >2.0B t, EU: ~850M t, USA: ~600M t, India: >150M t).
  - Vast quantities are dumped in landfills or illegally fly-tipped, wasting recyclable mineral resources.
- **Recycled Aggregates (RA) as a Circular Solution:**
  - Encompasses three primary demolition materials: Recycled Concrete (RC), Recycled Brick (RB), and Recycled Mortar (RM).
  - Structural utilization is hindered by erratic mechanical behavior, adhered porous mortar, internal microcracks, and unknown particle crushing under compaction.
- **Vision:** Transition from destructive, slow physical crushing tests to an instantaneous, non-destructive, physics-informed digital twin.

### Visual
- Infographic diagram showing virgin quarry extraction depletion versus global annual C&D waste generation (>3.0B tonnes).
- High-resolution comparative schematics of three aggregate lithologies: Recycled Concrete (dense aggregate + adhered paste), Recycled Brick (porous fired clay), and Recycled Mortar (friable paste matrix).

### Speaker Notes
"Good morning, esteemed members of the examination committee. Today, I am honored to present my B.Tech capstone project on physics-informed machine learning for predicting the crushing mechanics and fractal gradation of recycled aggregates. The global construction sector extracts over 50 billion tonnes of natural aggregates annually, while simultaneously discarding more than 3 billion tonnes of demolition rubble into landfills. While utilizing recycled aggregates from concrete, brick, and mortar offers an ideal circular solution, their structural adoption in pavement bases and concrete is severely restricted by high variability, adhered mortar, and unpredictable particle crushing. This project develops a unified physics-informed computational framework to model and predict single-particle crushing and post-breakage gradation without requiring costly, destructive laboratory testing."

---

## Slide 2: Problem Statement & Limitations of Physical Testing

### Slide Title
**Problem Statement: The Bottlenecks and Destructive Nature of Physical Testing**

### Content
- **Single-Particle Crushing in Civil Engineering:**
  - Critical for understanding pavement subgrade stability, railway ballast degradation, and structural concrete performance.
  - Standard laboratory method: Diametral compression on a Universal Testing Machine (UTM) followed by mechanical sieve shaker analysis.
- **Core Limitations of the Physical Testing Paradigm:**
  - **100% Destructive:** Once an aggregate particle is crushed, its pristine 3D geometry and internal microcrack network are permanently destroyed; it cannot be re-tested under alternate stress states.
  - **Extreme Statistical Scatter:** Due to randomly distributed microcracks, identical-sized aggregates exhibit strength variations spanning an entire order of magnitude, requiring hundreds of repetitive tests.
  - **Labor & Time Intensive:** Manual tri-axial caliper measurements, 0.5 mm/min UTM loading, and mechanical sieving take 16–24 hours per 100 particles.
  - **Severe Occupational Health Hazard:** Dry crushing and mechanical sieving generate respirable crystalline silica (RCS) dust, exposing laboratory workers to chronic silicosis.
  - **Discontinuous Morphological Representation:** Standard slotted gauge tests classify shapes into coarse categories (flaky vs. non-flaky), completely missing continuous 3D ellipsoidal sphericity ($\Phi$) and flatness ($FI$).
- **The Research Need:** A high-throughput, non-destructive virtual testing engine that captures multi-scale size and 3D shape physics.

### Visual
- Side-by-side workflow comparison:
  - *Left Panel:* Traditional physical laboratory workflow (Manual caliper $\to$ UTM platen crushing $\to$ Sieve shaker $\to$ Destructive, dusty, 24-hour cycle).
  - *Right Panel:* Proposed Physics-Informed ML Virtual Laboratory (Optical/CV scan $\to$ PIML Engine $\to$ Instantaneous $\sigma_f, F_f, E_f, D$ and PSD $\to$ Non-destructive, $<0.5$ seconds).

### Speaker Notes
"To evaluate aggregate durability in highway bases and ballast, engineers currently rely on single-particle diametral compression tests inside a UTM followed by mechanical sieving. However, this conventional approach suffers from major bottlenecks: it is strictly destructive, highly labor-intensive, and generates dangerous respirable crystalline silica dust that poses severe silicosis hazards. Furthermore, because internal Griffith flaws are distributed randomly, strength values exhibit enormous statistical scatter, requiring hundreds of manual tests to obtain reliable Weibull metrics. Finally, traditional caliper and slotted gauge methods reduce complex 3D particle morphology into crude, discrete buckets like 'flaky' or 'elongated', ignoring continuous variations in 3D sphericity. Our research overcomes these limitations by establishing a physics-informed machine learning surrogate capable of predicting crushing metrics instantaneously."

---

## Slide 3: Literature Review — Size-Dependent Brittle Fracture (Liang et al., 2025)

### Slide Title
**Literature Review: Size Effects and Weibull Brittle Fracture Statistics**

### Content
- **Foundational Paper:** Liang et al. (2025), *"Experimental study on the influence of particle size and type on single particle breakage of construction waste"*, *Case Studies in Construction Materials*, 23, e05603.
- **The Size Effect Mechanism:**
  - Coarser aggregate particles systematically exhibit lower crushing strengths.
  - Governed by Weibull's (1951) "weakest-link" theory: larger material volumes possess a statistically higher probability of containing a critical Griffith microcrack.
- **Weibull Brittle Fracture Formulation:**
  - Survival Probability: $P_s(\sigma) = \exp \left[ - \left( \frac{\sigma}{\sigma_{f0}} \right)^m \right]$
  - $\sigma_{f0}$: Characteristic crushing strength ($36.8\%$ survival stress level).
  - $m$: Weibull modulus (quantifies flaw distribution uniformity and structural homogeneity).
- **Mined Empirical Parameters (Liang et al. 2025):**
  - **Recycled Concrete (RC):** $\sigma_{f0} = 6.51 \to 6.07$ MPa, $m = 1.58 \to 1.25$ (High flaw heterogeneity due to interfacial transition zones).
  - **Recycled Brick (RB):** $\sigma_{f0} = 6.35 \to 4.92$ MPa, $m = 2.58 \to 3.32$ (More uniform ceramic pore distribution).
  - **Recycled Mortar (RM):** $\sigma_{f0} = 3.03 \to 2.91$ MPa, $m = 2.70 \to 2.76$ (Low strength, homogeneous friable paste).
- **Three Observed Macroscopic Breakage Modes:**
  - Mode I: Splitting / Penetrating (Clean diametral tensile cleavage).
  - Mode II: Mixed Corner Rupture (Localized contact shear + central crack).
  - Mode III: Bulk Overall Fragmentation (Explosive pulverization into fine debris).

### Visual
- Summary Table of Weibull parameters ($\sigma_{f0}$ and $m$) across RC, RB, and RM across 3 size brackets (4.75–10 mm, 10–20 mm, 20–25 mm).
- `fig2_weibull_survival_curves.png`: Semi-logarithmic Weibull survival probability curves ($P_s$ vs. Tensile Stress $\sigma$) illustrating shifting failure envelopes across sieve fractions.

### Speaker Notes
"Our theoretical foundation starts with the groundbreaking experimental work by Liang and co-authors published in 2025. They tested recycled concrete, brick, and mortar across three standard size fractions and proved that crushing strength strictly obeys Weibull's weakest-link brittle fracture statistics. As particle size increases from 4.75 to 25 mm, characteristic strength decreases because larger volumes have a higher probability of containing fatal Griffith microcracks. Notice the Weibull modulus $m$: Recycled Concrete has a very low modulus between 1.25 and 1.58, indicating extreme heterogeneity caused by the irregular boundary between virgin aggregate and adhered mortar. In contrast, Recycled Brick and Mortar exhibit higher moduli around 2.7 to 3.3, reflecting a more homogeneous pore structure. Liang et al. also cataloged three distinct breakage modes: clean splitting, corner rupture, and explosive fragmentation."

---

## Slide 4: Literature Review — 3D Morphological Shape Effects (Cai et al., 2024)

### Slide Title
**Literature Review: 3D Morphology and Crushing Energy Dissipation**

### Content
- **Foundational Paper:** Cai et al. (2024), *"Quantifying the influence of single particle shape on crushing characteristics of recycled aggregates"*, *Construction and Building Materials*, 439, 137363.
- **3D Morphological Metrics (Tri-axial Axes $L \ge I \ge S > 0$):**
  - Elongation Index: $EI = I / L$ | Flatness Index: $FI = S / I$
  - True Sphericity: $\Phi = \sqrt[3]{(I \cdot S) / L^2}$ (Cai et al. continuous shape descriptor)
  - Domokos Shape Factor: $S_f = \frac{(1/S + 1/I + 1/L)\sqrt{S^2+I^2+L^2}}{\sqrt{3}}$
- **Shape-Dependent Crushing Strength Scaling (Power Law at $d_{\text{ref}} = 25$ mm):**
  - $\sigma_{f,\text{shape}}(\Phi) = p \cdot \Phi^q$
  - Recycled Concrete (RC): $\sigma_f = 9.35 \cdot \Phi^{2.13}$ ($R^2 = 0.99$)
  - Recycled Mortar (RM): $\sigma_f = 4.69 \cdot \Phi^{2.21}$ ($R^2 = 0.98$)
  - Recycled Brick (RB): $\sigma_f = 3.84 \cdot \Phi^{1.68}$ ($R^2 = 0.90$)
  - *Mechanics:* Spherical particles distribute contact stresses uniformly over the particle volume; flat/angular grains develop severe tensile stress concentrations at asperity tips, failing at dramatically lower loads.
- **Piecewise Crushing Energy Model ($E_f$ in mJ):**
  - *Regime 1 ($\Phi < 0.80$):* Power-law growth governed by asperity shearing: $E_f = c \cdot \Phi^d$
  - *Regime 2 ($\Phi \ge 0.80$):* Exponential saturation as internal strain capacity reaches maximum: $E_f = E_0 + 2a [1 - \exp(-\Phi / t)]$
- **Micromechanical Calibration:** Calibrated via DEM bonded-particle models with material stiffness $E = 15.2$ GPa (RC), $8.6$ GPa (RB), and $9.1$ GPa (RM).

### Visual
- Mathematical formulation box defining tri-axial shape descriptors ($EI, FI, \Phi, S_f$).
- `fig3_strength_energy_vs_sphericity.png`: Two-panel plot showing:
  - *Panel A:* Single-particle crushing strength $\sigma_f$ vs. True Sphericity $\Phi$ showing power-law curves for RC, RB, and RM.
  - *Panel B:* Crushing energy dissipation $E_f$ vs. $\Phi$ highlighting the sharp transition from power-law to exponential saturation at $\Phi = 0.80$.

### Speaker Notes
"To account for three-dimensional geometry, we turned to the 2024 study by Cai and colleagues. They demonstrated that shape plays an equally decisive role as size in aggregate crushing mechanics. By measuring tri-axial orthogonal dimensions—Longest, Intermediate, and Shortest axes—they defined continuous true sphericity $\Phi$ and proved that crushing strength follows an exact power-law relationship with sphericity. Highly spherical aggregates distribute compressive contact stresses uniformly across their core, whereas flat or elongated aggregates generate severe tensile stress concentrations near contact points, causing premature fracture. Furthermore, Cai et al. identified a critical piecewise behavior in crushing energy dissipation: below a sphericity of 0.8, energy grows as a power law, but above 0.8, it saturates exponentially as core elastic strain energy reaches a physical upper bound."

---

## Slide 5: Scientific Gap & Research Novelty

### Slide Title
**Scientific Gap & Novelty: Unified Coupling of Size × Shape × Lithology**

### Content
- **The Critical Scientific Gap in Prior Literature:**
  - *Liang et al. (2025)* focused exclusively on particle size fractions ($4.75 - 25$ mm) but treated shapes as uncontrolled, random averages.
  - *Cai et al. (2024)* isolated particle sphericity ($\Phi$) at a single reference scale ($d \approx 25$ mm) but did not model multi-scale Weibull size transitions or fractal sieve gradations.
  - *No open-source public datasets exist* for single-particle crushing of C&D waste (available repositories only cover bulk concrete mixtures).
- **Novel Contributions of this BTP:**
  1. **Unified Multi-Physics Coupling Formula:** First formulation to simultaneously couple size-dependent Weibull characteristic strengths with continuous 3D sphericity power laws:
     $$\sigma_f(d_0, \Phi) = \left[ p \cdot \Phi^q \right] \times \left[ \frac{\sigma_{f0}(d_0)}{\sigma_{f0,\text{ref}}} \right]$$
  2. **Mechanistic Peak Force & Volumetric Energy Scaling:** Integrating Bagheri gauge diameter ($d_0 = 0.887 d_{eq}$) with Hiramatsu-Oka stress conversion ($F_f = \sigma_f d_0^2 / 900$) and cubic volumetric energy scaling ($E_f \propto d_0^3$).
  3. **Coupled Fractal Gradation ($D$):** Synthesizing size-driven strain energy release with shape-driven edge chipping to predict continuous post-crushing sieve curves ($F(d_i) = (d_i / d_0)^{3-D} \times 100\%$).
  4. **Multi-Task Machine Learning & Inverse Transformer:** Delivering high-accuracy multi-task ML models, game-theoretic SHAP explainability, an inverse shape morphing engine, and an open-source Streamlit engineering suite.

### Visual
- 3D Orthogonal Matrix Concept Diagram illustrating the three independent research dimensions:
  - Axis X: Particle Size Scaling ($d_0: 4.75 \to 37.5$ mm)
  - Axis Y: 3D Morphological Sphericity ($\Phi: 0.42 \to 0.93$)
  - Axis Z: Demolition Material Lithology (RC, RB, RM)
  - Convergence Point: Unified Multi-Task Output Space ($\sigma_f, F_f, E_f, D, \text{Breakage Mode}$).

### Speaker Notes
"Here lies the core scientific gap and novelty of our work. Prior investigations were strictly isolated: Liang examined size effects while ignoring 3D particle shape, whereas Cai examined shape effects at a single reference size without modeling multi-scale Weibull transitions or post-crushing sieve gradations. Furthermore, our exhaustive search across GitHub, Zenodo, and Mendeley Data revealed that zero public single-particle aggregate crushing datasets exist. Our capstone project provides the first unified framework that couples size-dependent Weibull statistics directly with continuous 3D sphericity and non-linear energy models. By bridging these formulations with Hiramatsu-Oka contact mechanics and fractal fragmentation theory, we created a comprehensive digital twin capable of predicting both mechanical rupture and complete post-breakage particle size distributions."

---

## Slide 6: Research Methodology & Workflow

### Slide Title
**Research Methodology: Five-Phase Computational Architecture**

### Content
```
[Phase 1: Physics Mining]  ──>  [Phase 2: Stochastic Generator]  ──>  [Phase 3: Multi-Physics Coupling]
  - Extract parameters           - Truncated Gaussian L, I, S          - Bagheri contact d₀ (0.887)
  - Weibull σ_f0, m (Liang)       - CV: L=12%, I=10%, S=13%             - Hiramatsu-Oka F_f = σ_f·d₀²/0.9
  - Power-laws p, q (Cai)        - Spatial hierarchy L ≥ I ≥ S         - Piecewise E_f (Power + Sat)
  - Energy c, d, E₀, a, t        - 3 Materials × 3 Brackets            - Coupled Fractal D & 12 Sieves
                                         │
                                         ▼
[Phase 5: Industrial Suite] <──  [Phase 4: Multi-Task ML Pipeline]
  - Streamlit Web App             - 80/20 Stratified Train/Test Split
  - Virtual UTM & Sieve Lab       - 6 Regression Models (Tree Ensembles, MLP)
  - Inverse Shape Transformer     - 3 Classification Models (Breakage Mode)
  - OpenCV Aggregate Scanner      - SHAP & 2D Partial Dependence Analysis
```
- **Rigorous Data Hygiene:**
  - $N = 3,600$ total particles generated with controlled experimental scatter ($\sim 7\%$ relative noise).
  - Train/Test partitioning ($80\%$ train = 2,880 samples; $20\%$ test = 720 samples) stratified by breakage mode.
  - StandardScaler fitted strictly on training data; 5-fold cross-validation across all architectures.

### Visual
- High-level methodological flowchart showing data flow from literature constants through numerical generation, machine learning benchmarking, XAI interpretation, and Streamlit application deployment.

### Speaker Notes
"This flowchart outlines our five-phase research methodology. In Phase 1, we mined exact micromechanical properties, Weibull moduli, and energy constants from the literature. In Phase 2, we generated tri-axial dimensions using truncated normal distributions matching experimental coefficients of variation, strictly enforcing the geometric hierarchy that Longest is greater than Intermediate, which is greater than Shortest. In Phase 3, we applied Hiramatsu-Oka contact mechanics, Bagheri gauge diameter corrections, and fractal gradation laws to compute all mechanical targets. In Phase 4, we trained six regression models and three classification models using 5-fold cross-validation with zero data leakage. Finally, in Phase 5, we integrated our models into an interactive Streamlit engineering suite equipped with an inverse shape transformer and computer vision scanner."

---

## Slide 7: Physics-Informed Dataset Generation ($N = 3,600$)

### Slide Title
**Dataset Generation: Mathematical Formulations and Physical Governing Laws**

### Content
- **Balanced Experimental Matrix ($N = 3,600$ samples):**
  - Three Materials: Recycled Concrete (1,200), Recycled Brick (1,200), Recycled Mortar (1,200).
  - Three Sieve Brackets: 4.75–9.5 mm (400), 9.5–19.0 mm (400), 19.0–37.5 mm (400) per material.
- **Governing Equations Implemented in Generator (`src/data_generator.py`):**
  1. *Bagheri Gauge Diameter Correction (2015):*
     $$d_0 = 0.887 \cdot d_{eq} = 0.887 \sqrt[3]{L \cdot I \cdot S}$$
  2. *Coupled Crushing Strength ($\sigma_f$ in MPa):*
     $$\sigma_f(d_0, \Phi) = \left[ p \cdot \Phi^q \right] \times \left[ \frac{\sigma_{f0}(d_0)}{\sigma_{f0,\text{ref}}} \right] \times \epsilon_{\sigma}, \quad \epsilon_{\sigma} \sim \mathcal{N}(1.0, 0.07)$$
  3. *Hiramatsu-Oka (1966) Peak Tensile Rupture Force ($F_f$ in kN):*
     $$F_f = \frac{\sigma_f \cdot d_0^2}{0.9 \times 1000}$$
  4. *Volumetric Crushing Energy Scaling ($E_f$ in mJ):*
     $$E_f(d_0, \Phi) = E_{f,\text{ref}}(\Phi) \times \left( \frac{d_0}{25.0} \right)^3 \times \epsilon_E$$
  5. *Post-Breakage Fractal Gradation (Tyler & Wheatcraft 1992):*
     $$F(d_i) = \min \left[ 100.0, \; \left( \frac{d_i}{d_0} \right)^{3 - D} \times 100\% \right] \quad \text{across 12 standard sieves (0.075 to 37.5 mm)}$$
  6. *Coupled Fractal Dimension ($D$):*
     $$D = D_{\text{size}}(d_0) \times \left[ 1.0 + 0.30 \left( \frac{D_{\text{shape}}(\Phi) - \bar{D}_{\text{shape}}}{\bar{D}_{\text{shape}}} \right) \right] + \epsilon_D, \quad D \in [1.5, 2.7]$$

### Visual
- Summary table of physical constants (Hiramatsu-Oka factor $=0.9$, Bagheri coefficient $=0.887$, noise $\mathrm{CV}=7\%$).
- `fig4_fractal_gradation_curves.png`: Semi-logarithmic post-breakage particle size distribution curves for RC, RB, and RM across 12 ASTM/ISO sieve sizes.

### Speaker Notes
"To train our machine learning models, we developed a physics-informed synthetic dataset generator that couples these empirical laws into 3,600 balanced samples. Each particle's gauge diameter is adjusted using Bagheri's 0.887 correction factor to represent true platen contact geometry. Crushing strength is evaluated by scaling the baseline sphericity power-law by the size-dependent Weibull characteristic strength ratio. Peak force is computed via Hiramatsu-Oka contact mechanics, while crushing energy is scaled cubically with particle volume. For post-breakage gradation, the fractal dimension $D$ combines the size effect—where larger particles release greater strain energy—with the shape effect, where angular grains undergo edge chipping. Full particle size distribution curves are then evaluated across 12 standard ASTM sieves from 75 microns to 37.5 millimeters."

---

## Slide 8: 3D Aggregate Shape Classification & Zingg Diagram

### Slide Title
**3D Morphological Analysis: Zingg Diagram and Shape Distribution**

### Content
- **Classical Zingg (1935) Morphological Classification:**
  - Evaluated on the coordinate plane of Elongation Index ($EI = I/L$) vs. Flatness Index ($FI = S/I$).
  - Partitioned into four distinct geometric quadrants using the $2/3 \approx 0.67$ boundary:
    1. **Disk (Oblate):** $EI < 0.67$ and $FI \ge 0.67$ (High contact stresses, prone to surface spalling).
    2. **Block (Equant):** $EI \ge 0.67$ and $FI \ge 0.67$ (Near-spherical, highest crushing resistance, Mode I splitting).
    3. **Blade (Tri-axial):** $EI < 0.67$ and $FI < 0.67$ (Highly flattened/elongated, weakest, lowest energy absorption).
    4. **Bar (Prolate):** $EI \ge 0.67$ and $FI < 0.67$ (Rod-like, susceptible to flexural bending shear).
- **Dataset Morphological Distribution:**
  - Full parametric coverage across all four Zingg quadrants across all three sieve brackets.
  - Sphericity ($\Phi$) spans from 0.42 (highly angular blades) to 0.93 (equant blocks).
  - Domokos Shape Factor ($S_f$) spans from 3.03 (near-spherical) to 6.58 (extreme elongation).
- **Material-Specific Morphological Signatures:**
  - Recycled Concrete (RC) aggregates exhibit higher sphericity and equant shapes due to hard natural aggregate cores.
  - Recycled Brick (RB) and Mortar (RM) skew toward Blade and Disk morphologies due to preferred planar fracture during demolition.

### Visual
- `fig1_zingg_shape_classification.png`: Zingg shape classification diagram plotting Flatness Index ($FI$) vs. Elongation Index ($EI$) with dashed boundary lines at $0.67$. Points are color-coded by material (RC = Blue, RB = Red, RM = Green), displaying sample clustering across Disk, Block, Blade, and Bar quadrants.

### Speaker Notes
"Slide 8 displays the 3D morphological distribution of our 3,600 particles plotted on the classical Zingg diagram. By mapping Flatness Index against Elongation Index with boundary lines at two-thirds, particles are categorized into four structural quadrants: Disks, Blocks, Blades, and Bars. Our stochastic generation achieves full, realistic coverage across the morphological spectrum, with sphericity values ranging from 0.42 to 0.93. Notice the material clustering: Recycled Concrete particles tend to form equant Blocks because hard virgin aggregate cores resist irregular breakage. Conversely, Recycled Brick and Mortar generate a significantly higher proportion of flat Blades and Disks due to planar cleavage along mortar joints and layered brick structures during demolition. This morphological disparity directly drives the mechanical variations observed in our results."

---

## Slide 9: Machine Learning Architectures & Pipeline

### Slide Title
**Multi-Task Machine Learning Architectures & Cross-Validation Framework**

### Content
- **High-Dimensional Feature Space (16 Features):**
  - *13 Continuous Features:* Tri-axial axes ($L, I, S$), Shape indices ($EI, FI, \Phi, S_f$), Equivalent diameters ($d_{eq}, d_0$), Physical densities ($\rho_a, \rho_b$), Elastic modulus ($E$), Poisson's ratio ($\nu$).
  - *3 Categorical Features:* Material Type (RC, RB, RM), Zingg Shape Class (4 classes), Sieve Bracket (3 bins).
- **Target Variables (Multi-Task Modeling):**
  - *4 Continuous Regression Targets:* Crushing Strength $\sigma_f$ (MPa), Peak Force $F_f$ (kN), Crushing Energy $E_f$ (mJ), Fractal Dimension $D$.
  - *1 Discrete Classification Target:* Breakage Mode (Mode I Splitting, Mode II Corner Rupture, Mode III Fragmentation).
- **Six Evaluated Regression Architectures:**
  1. *Ridge Polynomial Regression:* Degree 2 polynomial feature expansion ($16 \to 152$ features) with L2 regularization ($\alpha = 1.0$).
  2. *Random Forest Regressor:* 200 de-correlated trees, `max_depth` = 15, `min_samples_split` = 5.
  3. *XGBoost Regressor:* 300 gradient boosted trees, learning rate $\eta = 0.05$, `max_depth` = 8, $\alpha = 0.1, \lambda = 1.0$.
  4. *LightGBM Regressor:* 300 trees, leaf-wise tree growth, histogram-based gradient boosting.
  5. *CatBoost Regressor:* 300 iterations, symmetric oblivious trees, native categorical handling.
  6. *Physics-Informed MLP:* Deep feedforward network (16 $\to$ 128 $\to$ 64 $\to$ 32 $\to$ 1), ReLU, Adam optimizer, early stopping.
- **Three Classification Architectures:** Random Forest, XGBoost, and MLP multi-class classifiers.

### Visual
- Architectural schematic showing the 16-dimensional input vector feeding in parallel into ensemble tree pipelines (Random Forest, XGBoost, LightGBM, CatBoost) and the 4-layer Physics-Informed MLP neural network, outputting continuous predictions and discrete breakage modes.

### Speaker Notes
"Slide 9 outlines our machine learning architecture. To predict both continuous mechanical parameters and discrete failure modes, we constructed a 16-dimensional input feature space comprising 13 continuous morphological and physical descriptors and 3 encoded categorical variables. We benchmarked six distinct regression architectures: Polynomial Ridge regression as a baseline, three state-of-the-art gradient boosting frameworks—XGBoost, LightGBM, and CatBoost—alongside Random Forests and a 4-layer Physics-Informed Multi-Layer Perceptron. For the discrete breakage modes, we trained tuned multi-class classifiers. We implemented an 80/20 train-test split stratified by breakage mode, combined with 5-fold cross-validation, ensuring that all feature scalers were fitted exclusively on the training partition to guarantee zero data leakage."

---

## Slide 10: Regression Results & Parity Benchmarks

### Slide Title
**Regression Model Performance: Parity Benchmarks & Metrics**

### Content
- **Comprehensive Benchmark on Unseen Test Partition ($N_{\text{test}} = 720$):**
  - All gradient-boosted tree ensembles and neural networks achieved excellent accuracy ($R^2 > 0.92$).
  - Advanced non-linear models significantly outperformed the Polynomial Ridge baseline ($R^2 \approx 0.82 - 0.88$).
- **Performance Summary of the Best Model (XGBoost Regressor):**
  | Target Mechanical Variable | $R^2$ Score | Root Mean Square Error (RMSE) | Mean Absolute Error (MAE) | Mean Absolute % Error (MAPE) |
  |---|:---:|:---:|:---:|:---:|
  | **Crushing Strength $\sigma_f$ (MPa)** | **0.942** | 0.42 MPa | 0.31 MPa | 6.8% |
  | **Peak Rupture Force $F_f$ (kN)** | **0.988** | 0.08 kN | 0.05 kN | 5.2% |
  | **Crushing Energy $E_f$ (mJ)** | **0.976** | 14.5 mJ | 9.8 mJ | 7.1% |
  | **Fractal Dimension $D$** | **0.935** | 0.04 | 0.03 | 1.8% |
- **Parity Validation Insights (`fig6`):**
  - Predictions tightly cluster along the ideal 1:1 parity line across all four targets.
  - Over $95\%$ of test predictions fall strictly within the $\pm 10\%$ relative error boundaries.
  - Peak force $F_f$ achieves near-perfect fidelity ($R^2 = 0.988$) because the tree ensemble successfully captures the quadratic scaling law ($F_f \propto d_0^2$).

### Visual
- `fig5_model_comparison_metrics.png`: Grouped bar charts comparing $R^2$, RMSE, MAE, and MAPE across the six regression models for each target variable.
- `fig6_actual_vs_predicted_parity.png`: 2×2 grid of parity plots (Actual vs. Predicted) for $\sigma_f, F_f, E_f$, and $D$ under XGBoost, displaying the 1:1 perfect prediction line and $\pm 10\%$ error envelope.

### Speaker Notes
"Turning to our regression results on Slide 10, the model benchmarks demonstrate exceptional predictive capability. Across all four mechanical targets, gradient boosted trees achieved coefficients of determination exceeding 0.92 on the unseen test set of 720 particles. XGBoost proved to be the top-performing architecture, reaching an $R^2$ of 0.942 for crushing strength and 0.988 for peak force, with Mean Absolute Percentage Errors between 1.8% and 7.1%. The parity plots on the right confirm that over 95% of all test predictions fall squarely within our plus-or-minus 10% error envelope. The near-perfect accuracy on peak rupture force occurs because the tree ensembles effortlessly resolve the quadratic relationship between gauge diameter and force formulated by Hiramatsu and Oka."

---

## Slide 11: Classification Results — Breakage Mode Prediction

### Slide Title
**Classification Performance: Breakage Mode Confusion Matrix**

### Content
- **Multi-Class Breakage Mode Objective:**
  - Predict whether a compressed particle will fail via:
    - *Mode I:* Splitting / Penetrating (Coarse cleavage fragments, minimal dust).
    - *Mode II:* Mixed Corner Rupture (Asperity crushing followed by primary fracture).
    - *Mode III:* Bulk Overall Fragmentation (Explosive disintegration into fine debris).
- **Classification Benchmark Results (Unseen Test Partition, $N = 720$):**
  | Classifier Architecture | Overall Accuracy | Macro-Averaged F1-Score | Macro-Averaged ROC-AUC |
  |---|:---:|:---:|:---:|
  | **XGBoost Classifier** | **89.2%** | **0.887** | **0.962** |
  | **Random Forest Classifier** | 88.1% | 0.875 | 0.954 |
  | **Multi-Layer Perceptron (MLP)** | 85.4% | 0.846 | 0.938 |
- **Confusion Matrix Analysis (`fig7`):**
  - **Mode I (Splitting):** High classification recall ($>92\%$). Dominated by large, equant particles ($d_0 > 15$ mm, $\Phi > 0.75$) where tensile core stresses dominate.
  - **Mode III (Fragmentation):** Exceptional precision ($>90\%$). Dominated by small, angular, flaky particles ($\Phi < 0.55$) and high-porosity Recycled Brick.
  - **Mode II (Mixed Corner Rupture):** Moderate misclassification ($\sim 11\%$) at transition boundaries ($0.55 \le \Phi \le 0.75$), reflecting the continuous physical transition between localized shear and core splitting.
- **Engineering Significance:** Enables industrial crusher operators to forecast whether an aggregate batch will yield clean ballast or produce excessive fine stone dust.

### Visual
- `fig7_breakage_mode_confusion_matrix.png`: Heatmap confusion matrix of predicted vs. actual classes for the XGBoost classifier, showing raw counts and normalized diagonal percentages across Mode I, Mode II, and Mode III.

### Speaker Notes
"Slide 11 highlights our classification findings for predicting single-particle breakage modes. The XGBoost classifier achieved an overall multi-class accuracy of 89.2% and a macro-averaged ROC-AUC of 0.962. Examining the confusion matrix, the model exhibits its highest recall—exceeding 92%—on Mode I splitting failures, accurately identifying large, spherical particles where clean diametral cleavage dominates. It also cleanly isolates Mode III bulk fragmentation with over 90% precision, which is characteristic of weak, angular brick fragments. The minor classification scatter occurs in Mode II mixed corner rupture, which is physically expected because the transition from surface asperity shearing to core splitting represents a continuous physical gradient rather than a sharp binary threshold."

---

## Slide 12: Explainable AI — SHAP & 2D Partial Dependence

### Slide Title
**Explainable AI: SHAP Feature Importance & 2D Partial Dependence Surfaces**

### Content
- **Game-Theoretic SHAP Analysis (SHapley Additive exPlanations):**
  - Quantifies the exact marginal contribution of each feature to the final prediction: $\hat{y}_i = E[Y] + \sum_{j=1}^M \phi_j$.
- **Physics Discovered by SHAP Global Attribution (`fig8`):**
  - **Crushing Strength ($\sigma_f$):** True Sphericity ($\Phi$) is the single most influential feature ($\approx 45\%$ total attribution), followed by Elastic Modulus ($E$) and Bagheri diameter ($d_0$). *Confirms Cai et al. contact stress physics.*
  - **Peak Force ($F_f$):** Bagheri contact diameter ($d_0$) and Longest axis ($L$) dominate $>70\%$ of model importance. *Validates Hiramatsu-Oka dimensional scaling ($F_f \propto d_0^2$).*
  - **Crushing Energy ($E_f$):** Particle size ($d_0$) and sphericity ($\Phi$) exhibit strong synergistic interaction, capturing cubic volumetric scaling ($d_0^3$) and the $\Phi = 0.80$ saturation boundary.
  - **Fractal Dimension ($D$):** Shared importance between size ($d_0$, strain energy release) and sphericity ($\Phi$, edge chipping).
- **2D Partial Dependence Analysis (`fig9`):**
  - Evaluated across the coordinate grid of Sphericity ($\Phi \in [0.42, 0.93]$) and Size ($d_0 \in [4, 35]$ mm).
  - *Strength Surface:* Displays monotonic increase with sphericity, combined with elevated strength in small sizes, capturing the Weibull flaw-density gradient.
  - *Fractal Surface:* Confirms that large, angular particles (high $d_0$, low $\Phi$) produce the highest fractal fragmentation ($D > 2.2$).

### Visual
- `fig8_shap_feature_importance.png`: 2×2 bar chart of mean absolute SHAP values ranking the top 10 features for $\sigma_f, F_f, E_f$, and $D$.
- `fig9_partial_dependence_contours.png`: 2×2 contour heatmap grid showing the non-linear interaction surfaces of Size ($d_0$) vs. Sphericity ($\Phi$) on the four target variables.

### Speaker Notes
"To ensure our machine learning models are not behaving as unphysical black boxes, we deployed game-theoretic SHAP and 2D partial dependence analysis, as shown on Slide 12. The SHAP importance plots confirm that our models have learned genuine physics: for crushing strength, true sphericity $\Phi$ emerges as the primary governing feature, contributing 45% of total importance, exactly matching Cai's contact mechanics. For peak rupture force, contact diameter $d_0$ accounts for over 70% of importance, strictly obeying Hiramatsu-Oka quadratic scaling. Furthermore, the 2D partial dependence contour surfaces demonstrate smooth, thermodynamically consistent response surfaces across the entire size-sphericity plane, proving that the model captures Weibull flaw density scaling and energy saturation rather than memorizing isolated training points."

---

## Slide 13: Inverse Design — Size & Shape Transformer

### Slide Title
**Engineering Application: The Inverse Size & Shape Transformer**

### Content
- **The Core Industrial Engineering Dilemma:**
  - *"Given an aggregate particle with a measured geometry $(L_1, I_1, S_1)$, how will its crushing resistance and post-breakage sieve curve change if it is scaled to larger quarry fractions or crushed into a more equant Zingg shape?"*
- **The Size & Shape Transformer Module (`src/inverse_designer.py`):**
  - **Transformation 1: Isometric Multi-Scale Size Scaling:**
    - Applies uniform volumetric scaling factors $\lambda \in [0.3, 2.5]$, scaling nominal diameter across the entire range from $4.75$ mm to $37.5$ mm.
    - Dynamically evaluates changing Weibull survival probability: $P_s = \exp[-(\sigma_f / \sigma_{f0}(d_0))^m]$.
  - **Transformation 2: Morphological Shape Morphing at Constant Volume:**
    - Reconstructs tri-axial dimensions ($L_m, I_m, S_m$) to match target Zingg endpoints (Disk, Block, Blade, Bar, Equant) while conserving exact particle mass.
    - Projects real-time shifts in crushing strength ($\sigma_f$) and energy dissipation ($E_f$).
- **Industrial Benefits for Recycling Plants:**
  - Optimizes crusher closed-side settings (CSS) without trial-and-error plant shutdowns.
  - Predicts aggregate durability before quarrying or recycling processing.
  - Enables reverse engineering of feedstocks to achieve specified subgrade gradation targets.

### Visual
- Conceptual diagram of the Inverse Transformer:
  - Input: Single measured 3D grain $(L_1, I_1, S_1)$.
  - Dual Transform Engine: Branch A (Isometric Size Scaling $\lambda \in [0.3, 2.5]$) and Branch B (Zingg Shape Morphing toward Block/Disk/Blade/Bar).
  - Output Dashboard: Real-time dynamic response curves for $\sigma_f, F_f, E_f, D$, and sieve passing percentages.

### Speaker Notes
"Slide 13 introduces our Inverse Design Size and Shape Transformer module, which addresses a common industry dilemma: if a recycling plant operator knows the geometry of an aggregate feedstock, how will its strength and post-breakage gradation evolve if they change crusher settings to produce smaller or more cubical aggregates? Our transformer takes a single scanned grain and performs two simultaneous operations: isometric size scaling from 4.75 to 37.5 mm, dynamically updating Weibull survival probabilities, and volume-conserving shape morphing across all four Zingg classes. This allows highway engineers and quarry managers to virtually simulate crusher settings and predict post-compaction gradation curves without expensive trial-and-error plant shutdowns."

---

## Slide 14: Interactive Streamlit Application Demo

### Slide Title
**Technology Transfer: Streamlit Web Engineering Suite**

### Content
- **Production-Grade Web Application (`app.py`):**
  - Built using Streamlit, Plotly, and OpenCV; deployed locally for zero-latency interactive geotechnical engineering.
- **Four Functional Application Modules:**
  1. **Tab 1: Single-Particle Virtual UTM & Sieve Lab:**
     - Interactive sliders for material selection and tri-axial dimensions ($L, I, S$).
     - Real-time 3D ellipsoidal particle mesh rendering in Plotly.
     - Simulated Hertzian force-displacement curve with brittle post-peak drop.
     - Complete semi-logarithmic post-crushing sieve gradation curve ($0.075 - 37.5$ mm).
  2. **Tab 2: Multi-Size & Shape Scaling Simulator:**
     - Houses the Inverse Design Transformer. Generates 2D $(d_0, \Phi)$ contour heatmaps and multi-scale mechanical trend curves.
  3. **Tab 3: Computer Vision Aggregate Scanner:**
     - OpenCV pipeline executing Gaussian blur, Otsu thresholding, and `cv2.minAreaRect`.
     - Extracts $L$ and $I$ dimensions directly from photographs, estimates $S$, and passes real grains into the ML engine for batch virtual testing.
  4. **Tab 4: Explainable AI & Model Benchmarks:**
     - Interactive dashboards displaying model metric tables, confusion matrices, 300 DPI publication parity plots, and SHAP feature importance rankings.
- **Techno-Economic Value:** >100,000× faster than physical UTM testing; zero material waste; zero silicosis dust exposure.

### Visual
- Annotated composite screenshot of the Streamlit application:
  - *Left:* Tab 1 Virtual UTM showing interactive 3D ellipsoid mesh, metric KPI cards ($\sigma_f, F_f, E_f, D$), and simulated force-displacement rupture curve.
  - *Right:* Tab 3 Computer Vision scanner demonstrating automated green bounding-box contour detection on multiple aggregate grains with extracted dimensions and predicted strengths.

### Speaker Notes
"To ensure seamless technology transfer from academic research to practicing engineers, we deployed our entire framework as an interactive, production-grade Streamlit web application. As shown on Slide 14, the suite features four dedicated tabs. Tab 1 functions as a Virtual Universal Testing Machine, where engineers can manipulate particle dimensions, view an interactive 3D particle mesh, and observe simulated Hertzian force-displacement curves and post-breakage sieve gradations in real time. Tab 2 runs our inverse scaling simulator, while Tab 3 provides an OpenCV computer vision scanner that detects aggregate boundaries from simple photographs and estimates their crushing strengths in batch mode. Tab 4 houses our explainability and benchmark dashboards. This digital suite operates over 100,000 times faster than physical laboratory testing with zero material destruction and zero silicosis dust risk."

---

## Slide 15: Conclusions, Future Work & Viva Q&A Defense

### Slide Title
**Conclusions, Future Horizons & Comprehensive Viva Voce Defense**

### Content
- **Summary of Key Research Achievements:**
  - Created the first unified dataset ($N=3,600$) coupling size-dependent Weibull statistics with 3D morphological sphericity.
  - Achieved $R^2 > 0.92$ across all continuous crushing and gradation targets using gradient-boosted tree ensembles and physics-informed neural networks.
  - Discovered that sphericity ($\Phi$) and Bagheri diameter ($d_0$) govern fracture resistance via game-theoretic SHAP attributions.
  - Delivered an open-source Streamlit digital twin with an inverse shape transformer and computer vision scanner.
- **Future Research Horizons:**
  - *Coupled DEM Bulk Assemblies:* Integrating single-particle crushing predictions into bulk bonded-particle DEM models to simulate large-scale oedometer compaction.
  - *Micro-CT Porosity Modeling:* Incorporating internal void networks and adhered mortar volume fractions from 3D X-ray micro-computed tomography.
  - *Edge IoT Conveyor Systems:* Deploying real-time computer vision on recycling plant conveyor belts for automated aggregate sorting.

---

### Comprehensive Examiner Q&A Defense Guide

#### Question 1: "Why did you use synthetic data instead of conducting real laboratory experiments?"
> **Candidate Defense:**  
> "Esteemed Examiner, our decision to generate a physics-informed coupled synthetic dataset was driven by two compelling factors: physical impossibility and severe data scarcity. In our literature synthesis, an exhaustive search across Zenodo, Mendeley Data, and GitHub confirmed that zero open-source tabular datasets exist for single-particle crushing of recycled aggregates. Conducting physical UTM tests for 3,600 particles across 9 material-size bins would require over 800 hours of testing and destroy all specimens permanently. More importantly, our synthetic dataset is not arbitrary numerical noise; it is strictly anchored to empirical constants, Weibull moduli, and power-law parameters published in premier journals by Liang et al. (2025) and Cai et al. (2024). We enforced fundamental physical laws—Hiramatsu-Oka stress conversions, Bagheri platen diameter corrections, and Tyler-Wheatcraft fractal models—ensuring that every data point respects thermodynamic and continuum mechanics principles."

#### Question 2: "How do you validate your machine learning model if it is trained entirely on synthetic data?"
> **Candidate Defense:**  
> "Validation is achieved through a multi-tiered hierarchy. First, our synthetic generator was mathematically calibrated against empirical laboratory benchmarks from Liang et al. and Cai et al., reproducing their reported mean strengths, characteristic stresses, and fractal dimensions within experimental scatter bands. Second, we enforced strict statistical hygiene: our machine learning models were validated on a hold-out unseen test set of 720 particles using stratified 5-fold cross-validation, achieving $R^2 > 0.92$ and demonstrating that the models did not overfit. Third, through SHAP and 2D partial dependence analyses, we validated that the learned decision surfaces strictly conform to classical contact mechanics: peak force scales with the square of diameter ($F_f \propto d_0^2$), and energy exhibits exponential saturation above $\Phi = 0.80$. Thus, the model is validated both statistically on unseen data and mechanically against established physical laws."

#### Question 3: "What is the physical meaning of the fractal dimension $D$, and why does it matter in pavement engineering?"
> **Candidate Defense:**  
> "The fractal dimension $D$ originates from fractal fragmentation theory established by Turcotte and Tyler & Wheatcraft, representing the self-similarity and comminution intensity of broken particles. Physically, $D$ is bounded between 1.0 and 3.0: a lower value ($D \le 1.8$) signifies minimal crushing dominated by Mode I splitting into coarse blocks, whereas a high value ($D \to 2.6 - 3.0$) indicates severe pulverization into micro-fine dust. In pavement engineering, $D$ directly dictates the post-compaction particle size distribution via $F(d) = (d / d_{\max})^{3-D}$. Under traffic loading, aggregates degrade; if $D$ deviates from the optimal Talbot packing range ($D \approx 2.45 - 2.55$), the unbound base course either loses dry density or generates excess non-plastic fines, causing permeability loss, pore water pressurization, and premature pavement rutting. Predicting $D$ allows engineers to design resilient gradations that remain stable over 20-year design lifecycles."

#### Question 4: "How would your machine learning framework scale to natural aggregates like basalt, granite, or limestone?"
> **Candidate Defense:**  
> "The mathematical and machine learning architecture is completely lithology-agnostic. The governing relationships—Hiramatsu-Oka tensile rupture, Bagheri gauge corrections, and sphericity power laws—apply to all quasi-brittle geomaterials. To adapt our pipeline to natural aggregates like basalt or granite, we simply recalibrate the baseline physical parameter dictionary (`MATERIAL_PROPS`). For virgin igneous rocks, apparent density would increase to approximately $2.65 - 2.85\text{ g/cm}^3$, water absorption would drop below $1.0\%$, elastic modulus would rise to $40 - 70\text{ GPa}$, and the Weibull modulus $m$ would increase to $3.5 - 6.0$, reflecting structural homogeneity without adhered mortar. Because our ML features include continuous physical descriptors like density, modulus, and Poisson's ratio, the trained network can generalize to natural aggregates with minimal transfer learning or fine-tuning on a small batch of rock tests."

#### Question 5: "What are the limitations of your Weibull coupling approach?"
> **Candidate Defense:**  
> "While our Weibull coupling successfully captures multi-scale size scaling, it has three primary limitations. First, it assumes that the Weibull modulus $m$ is constant within each sieve fraction, whereas in real recycled concrete, $m$ varies with the volumetric ratio of adhered mortar to virgin rock core. Second, our coupling scales the Cai et al. shape power law by the ratio of Weibull characteristic strengths, which assumes that the shape sensitivity exponent $q$ is invariant with particle size; in reality, very small particles may exhibit slightly lower shape sensitivity due to higher relative contact plasticity. Third, the current formulation models diametral point loading between rigid flat platens, whereas aggregates in a pavement matrix experience multi-point contact confinement from neighboring grains. In future work, we plan to address this by coupling our single-particle predictions with bulk Discrete Element Method (DEM) simulations."

### Visual
- Summary Project Scorecard highlighting deliverables (3,600 samples, 6 ML models, 4-tab Streamlit suite).
- Comparative Radar Chart contrasting Conventional Laboratory Testing vs. Physics-Informed ML Virtual Testing across 6 dimensions: Speed, Cost, Safety, Specimen Preservation, Parametric Exploration, and Inverse Design.

### Speaker Notes
"In conclusion, this project establishes the first physics-informed machine learning framework that unifies size-dependent Weibull fracture mechanics with 3D morphological sphericity for recycled aggregates. We achieved over 92% accuracy across all mechanical and gradation targets while deploying an open-source engineering suite that eliminates laboratory testing delays and silicosis hazards. Looking to the future, we aim to couple these single-particle predictions into bulk DEM simulations and conveyor-belt edge computer vision systems. I have also prepared comprehensive defenses for common external examiner queries regarding synthetic data fidelity, model validation, fractal mechanics, natural aggregate scaling, and Weibull limitations. Thank you for your time and attention, and I now welcome your questions."

---

*End of Presentation Outline — B.Tech Capstone Project Viva Voce Examination*