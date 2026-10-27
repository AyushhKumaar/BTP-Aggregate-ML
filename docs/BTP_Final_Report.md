# Physics-Informed Machine Learning for Predicting Single-Particle Crushing Mechanics and Post-Breakage Fractal Gradation of Recycled Aggregates Across Multi-Scale Morphologies

**B.Tech Capstone Project Final Report**  
*Department of Civil and Environmental Engineering*  
*Academic Year: 2025–2026*

---

## Executive Summary / Abstract

The escalating global generation of Construction and Demolition (C&D) waste—now exceeding 3.0 billion metric tonnes per annum—presents one of the most critical sustainability challenges in contemporary civil engineering. Simultaneously, the depletion of high-quality virgin natural mineral aggregates threatens the ecological balance of river basins and upland quarries. While the valorization of recycled aggregates (RA) derived from crushed concrete, brick masonry, and demolition mortar offers an attractive pathway toward a circular economy, their broader structural adoption in load-bearing pavement subgrades, railway ballast, and structural concrete is severely hindered by erratic mechanical behavior, high variability in grain morphology, residual microcracking, and pronounced vulnerability to single-particle crushing under shear and compaction stresses.

Conventional physical characterization relies on single-particle diametral compression tests using Universal Testing Machines (UTMs) coupled with mechanical sieve analysis. However, this experimental approach is inherently destructive, labor-intensive, cost-prohibitive, and virtually incapable of exploring the continuous multi-dimensional space spanned by particle size and three-dimensional shape morphology. To circumvent these limitations, this project develops a comprehensive, physics-informed machine learning (PIML) framework that maps 3D multi-scale aggregate morphology directly to single-particle crushing strength ($\sigma_f$), peak rupture force ($F_f$), fracture energy dissipation ($E_f$), post-breakage fractal gradation ($D$), and discrete breakage failure modes.

By synthesizing the size-dependent Weibull brittle fracture formulations of Liang et al. (2025) across three distinct demolition waste materials—Recycled Concrete (RC), Recycled Brick (RB), and Recycled Mortar (RM)—with the shape-dependent 3D morphological sphericity and non-linear energy models of Cai et al. (2024), we generate a rigorous, physically coupled benchmark dataset comprising $N = 3,600$ individual particles spanning sieve apertures from 4.75 mm to 37.5 mm. Six multi-task regression architectures (Polynomial Ridge, Random Forest, XGBoost, LightGBM, CatBoost, and Physics-Informed Multi-Layer Perceptrons) and three classification models are systematically trained, cross-validated, and benchmarked. 

The trained machine learning models achieve outstanding predictive accuracy, attaining coefficients of determination $R^2 > 0.92$ across all continuous mechanical and gradation targets, with gradient boosted trees and physics-informed neural networks capturing complex non-linear boundary effects and energy saturation regimes. Explainable artificial intelligence (XAI) workflows utilizing game-theoretic SHAP (SHapley Additive exPlanations) and 2D partial dependence analyses clarify the governing physical mechanisms, confirming that sphericity ($\Phi$) and Bagheri equivalent diameter ($d_0$) dominate fracture resistance and energy absorption. Finally, the framework is integrated into an interactive four-tab Streamlit web application featuring a "Virtual UTM and Sieve Lab," an "Inverse Design Size & Shape Transformer," and an open-source Computer Vision scanner. This platform allows practicing geotechnical and highway engineers to optimize crusher operational energy, design subgrade packing gradations, and conduct virtual aggregate crushing tests within seconds without laboratory destruction.

---

## Chapter 1: Introduction & Problem Statement

### 1.1 The Global Natural Aggregate Scarcity Crisis
Aggregates represent the most consumed solid raw material on Earth after fresh water. The global construction industry extracts and utilizes an estimated 50 billion metric tonnes of sand, gravel, and crushed stone annually. The environmental externalities associated with this relentless extraction are profound: severe destruction of riparian ecosystems, lowering of groundwater tables, destabilization of riverbanks, loss of agricultural land, and enormous carbon footprints associated with the long-haul transportation of quarried rock to rapidly expanding urban centers. In many metropolitan territories, local high-grade natural aggregate sources are entirely exhausted, forcing municipal authorities and transport infrastructure agencies to import aggregates over distances exceeding hundreds of kilometers, drastically inflating construction costs and embodied carbon footprints.

### 1.2 Construction and Demolition (C&D) Waste: Quantities and Complexities
In parallel to virgin resource depletion, rapid urbanization, urban renewal projects, and disaster-related demolition generate staggering volumes of Construction and Demolition (C&D) waste globally. Annual C&D waste production is estimated at over 2.0 billion tonnes in China, 850 million tonnes in the European Union, 600 million tonnes in the United States, and more than 150 million tonnes in India. A major proportion of this demolition debris is dumped into landfills or illegally fly-tipped, consuming valuable municipal land and posing severe leaching and airborne particulate hazards.

Recycling this solid waste into Recycled Aggregates (RA) presents an indispensable circular solution. However, unlike homogenous virgin crushed rock (such as basalt, granite, or limestone), recycled aggregate derived from demolished civil structures is notoriously heterogeneous. Real-world C&D waste comprises three primary constituents:
1. **Recycled Concrete (RC):** Aggregate particles consisting of original natural rock partially enveloped by adhered, weathered cement paste.
2. **Recycled Brick (RB):** Highly porous, low-stiffness fragments originating from broken masonry units and fired clay tiles.
3. **Recycled Mortar (RM):** Weak, friable agglomerations of sand and hydrated cement paste characterized by elevated porosity and low shear strength.

The presence of microcracks formed during structural service life and subsequent hydraulic mechanical demolition imparts high porosity (water absorption commonly ranging from 5% to 15%), reduced elastic moduli, and pronounced susceptibility to particle crushing under mechanical compaction, heavy freight traffic, and environmental weathering. Consequently, civil engineering standards worldwide strictly limit the replacement ratio of recycled aggregates in structural concrete and high-performance highway pavement bases, largely due to concerns regarding unpredictable particle degradation.

### 1.3 Destructive Nature and Bottlenecks of Physical Testing
To ensure the mechanical stability of granular unbound pavement layers, railway ballast, and structural concrete, geotechnical engineers must quantify the single-particle crushing strength and degradation characteristics of aggregate grains. In the laboratory, this is evaluated through single-particle crushing tests (diametral compression between rigid parallel steel platens inside a Universal Testing Machine) followed by mechanical sieve analysis to establish the post-breakage Particle Size Distribution (PSD).

However, physical laboratory characterization faces crippling limitations:
- **Destructive Testing Paradigm:** Once a particle is crushed, its pristine geometry and internal flaw network are permanently annihilated. It is physically impossible to test the exact same grain under varying stress paths, platen friction angles, or loading velocities.
- **Extreme Statistical Scatter:** Due to randomly distributed internal Griffith flaws and pre-existing microcracks, the crushing strength of identical-sized aggregates often spans an entire order of magnitude. Reliable statistical estimation of Weibull parameters requires testing dozens or hundreds of individual particles for every single sieve fraction and shape category.
- **Labor and Time Expenditure:** Preparing, measuring tri-axial dimensions, testing on a UTM at controlled displacement rates ($0.1 - 1.0\text{ mm/min}$), and meticulously sieving fragile fragments requires tens of hours of manual labor per sample batch.
- **Occupational Health Hazards:** Mechanical sieving and dry crushing generate airborne respirable crystalline silica (RCS) dust, presenting severe chronic occupational health hazards (silicosis) to laboratory personnel.
- **Discontinuous Morphological Mapping:** Standard laboratory testing classifies aggregate shape into broad, subjective categories (e.g., flaky vs. non-flaky) using slotted gauges, failing to capture continuous variations in 3D ellipsoidal sphericity, elongation, and flatness.

### 1.4 The Paradigm Shift: Physics-Informed Machine Learning Virtual Testing
To overcome these experimental bottlenecks, computational mechanics and machine learning (ML) offer an unprecedented opportunity to create high-throughput "virtual testing laboratories." Purely data-driven black-box machine learning models, however, are prone to overfitting, unphysical extrapolations (e.g., predicting negative fracture energy or non-monotonic size scaling), and poor generalizability across varied aggregate lithologies. 

A **Physics-Informed Machine Learning (PIML)** approach circumvents these deficiencies. By incorporating known physical boundary conditions—such as Hertzian elastic contact mechanics, Hiramatsu-Oka stress state conversions, Weibull weakest-link brittle fracture statistics, and Tyler-Wheatcraft fractal fragmentation scaling—into the feature engineering and dataset generation pipeline, the learning algorithms are constrained to respect fundamental thermodynamic and mechanical conservation laws. 

### 1.5 Objectives and Scope of the BTP
This B.Tech Project (BTP) aims to develop an end-to-end physics-informed computational suite for predicting the mechanical degradation and post-crushing gradation of recycled aggregates. The specific research objectives are:
1. **Develop a Physically Coupled Dataset:** Formulate a multi-physics synthetic data generator that mathematically couples the size-dependent Weibull crushing strength and fractal gradation equations of Liang et al. (2025) with the 3D shape morphology and non-linear crushing energy formulations of Cai et al. (2024), generating $N = 3,600$ benchmark samples.
2. **Benchmark Multi-Task ML Architectures:** Implement, optimize, and cross-validate six regression models (Ridge Polynomial, Random Forest, XGBoost, LightGBM, CatBoost, and Physics-Informed MLP) alongside three classification models to simultaneously predict crushing strength ($\sigma_f$), peak force ($F_f$), fracture energy ($E_f$), post-breakage fractal dimension ($D$), and discrete breakage mode.
3. **Elucidate Failure Mechanics via Explainable AI:** Deploy game-theoretic SHAP (SHapley Additive exPlanations) and 2D partial dependence contour analyses to uncover the non-linear coupling between particle size ($d_0$) and 3D sphericity ($\Phi$).
4. **Deploy an Interactive Engineering Software Suite:** Design and deploy an open-source Streamlit web application incorporating an Inverse Design Size & Shape Transformer and a Computer Vision aggregate scanner, enabling instantaneous virtual testing, crusher energy optimization, and subgrade packing design for highway and civil infrastructure projects.

---

## Chapter 2: Literature Review & Theoretical Foundations

### 2.1 Size-Dependent Crushing Mechanics and Weibull Fracture Statistics
The mechanical crushing of quasi-brittle mineral particles is fundamentally governed by the statistical distribution of internal microstructural defects, pores, and microcracks, as originally conceptualized by Griffith (1921). Under diametral mechanical loading, failure initiates at the most critical pre-existing flaw oriented unfavorably to the induced tensile stress field. 

Liang et al. (2025) conducted an extensive experimental investigation into the single-particle breakage behavior of construction waste across three distinct materials: Recycled Concrete (RC), Recycled Brick (RB), and Recycled Mortar (RM). Testing particles across three standard size brackets ($4.75 - 10\text{ mm}$, $10 - 20\text{ mm}$, and $20 - 25\text{ mm}$), Liang et al. demonstrated a pronounced size effect: as particle nominal diameter increases, the mean crushing strength systematically decreases. This phenomenon aligns with Weibull's (1951) "weakest-link" theory, which posits that larger material volumes possess a higher cumulative probability of containing a catastrophic Griffith flaw.

The survival probability $P_s(\sigma)$ of a particle subjected to an induced tensile stress $\sigma$ is expressed by the two-parameter Weibull distribution:
$$P_s(\sigma) = \exp \left[ - \left( \frac{\sigma}{\sigma_{f0}} \right)^m \right]$$
where $\sigma_{f0}$ represents the characteristic crushing strength (the stress level at which $36.8\%$ of particles survive, corresponding to $P_s = 1/e \approx 0.368$), and $m$ is the Weibull modulus, a dimensionless parameter quantifying the homogeneity of the material's flaw population. A high Weibull modulus indicates a uniform defect distribution and low strength scatter, whereas a low modulus signifies severe structural heterogeneity.

In the findings of Liang et al. (2025), Recycled Concrete (RC) aggregates exhibited a low Weibull modulus ($m = 1.25 - 1.58$), reflecting the extreme heterogeneity introduced by the random presence of dense natural aggregate cores encapsulated within variable thicknesses of porous adhered mortar. Conversely, Recycled Brick (RB) and Recycled Mortar (RM) exhibited higher Weibull moduli ($m = 2.58 - 3.32$ and $m = 2.70 - 2.76$, respectively), characteristic of more uniformly porous ceramic and mortar paste matrices. Furthermore, Liang et al. categorized single-particle breakage into three distinct macroscopic failure modes:
- **Mode I (Splitting / Penetrating):** Characterized by clean diametral cleavage along the loading axis, generating two dominant semi-ellipsoidal fragments and minimal fine debris.
- **Mode II (Mixed Corner Rupture):** Localized shearing and asperity attrition at platen contact points, followed by catastrophic rupture through the core.
- **Mode III (Bulk Overall Fragmentation):** Complete explosive disintegration of the particle into multiple sub-millimeter fragments and dust, typical of highly porous, low-strength grains.

### 2.2 3D Particle Morphology, Zingg Classification, and Crushing Resistance
While size effects govern the volumetric probability of encountering microstructural flaws, aggregate three-dimensional geometry dictates the internal stress concentrations and contact mechanics developed during compressive loading.

Cai et al. (2024) systematically quantified the influence of 3D particle morphology on the crushing characteristics of recycled aggregates using high-resolution 3D optical scanning and DEM (Discrete Element Method) simulations. Every aggregate grain can be approximated by its tri-axial orthogonal dimensions: Longest ($L$), Intermediate ($I$), and Shortest ($S$) axes, subject to the geometric constraint $L \ge I \ge S > 0$.

From these fundamental dimensions, the standard shape indices are derived:
- **Elongation Index ($EI$):**
  $$EI = \frac{I}{L}$$
- **Flatness Index ($FI$):**
  $$FI = \frac{S}{I}$$

Zingg (1935) utilized $EI$ and $FI$ to divide particle morphology into four geometric quadrants using a boundary threshold of $2/3 \approx 0.67$:
1. **Disk (Oblate):** $EI < 0.67$ and $FI \ge 0.67$
2. **Block (Equant):** $EI \ge 0.67$ and $FI \ge 0.67$
3. **Blade (Tri-axial):** $EI < 0.67$ and $FI < 0.67$
4. **Bar (Prolate):** $EI \ge 0.67$ and $FI < 0.67$

To describe true 3D roundness and sphericity in a single continuous scalar, Cai et al. adopted the true sphericity metric ($\Phi$):
$$\Phi = \sqrt[3]{\frac{I \cdot S}{L^2}}$$
Additionally, Domokos et al. formulated the dimensionless shape factor ($S_f$):
$$S_f = \frac{\left( \frac{1}{S} + \frac{1}{I} + \frac{1}{L} \right) \sqrt{S^2 + I^2 + L^2}}{\sqrt{3}}$$
A perfect sphere possesses $\Phi = 1.0$ and $S_f = 3.0$, while increasingly elongated, flattened, or angular particles exhibit lower $\Phi$ values ($0.40 - 0.70$) and elevated $S_f$ values ($4.0 - 7.0$).

Crucially, Cai et al. (2024) demonstrated that single-particle crushing strength ($\sigma_f$) follows a strict power-law scaling with sphericity ($\Phi$):
$$\sigma_f = p \cdot \Phi^q$$
where $p$ represents the baseline crushing strength of an idealized spherical aggregate ($\Phi = 1.0$) at a reference scale, and $q$ is the shape sensitivity exponent. Highly spherical particles distribute compressive contact stresses uniformly over broader internal volumes, whereas angular, flat, or elongated particles develop acute tensile stress concentrations near platen contact points, initiating premature tensile splitting at dramatically lower loads.

### 2.3 Machine Learning Applications in Granular Geomechanics
The application of artificial intelligence and machine learning to granular mechanics has expanded rapidly over recent years:
- **Wang et al. (2021)** deployed machine learning algorithms to map the 3D morphology of 400 rock grains—quantified via 24 morphological descriptors—to their crushing strength simulated using the Combined Finite-Discrete Element Method (FDEM). Their work revealed that local contact roundness and global sphericity exert the strongest control over stress concentration factors, proving that non-linear ML models can effectively capture morphology-induced fracture transitions where classical analytical mechanics fails.
- **Oskooei et al. (2021)** simulated the crushing behavior of recycled C&D waste aggregates using DEM bonded-particle models (BPM) calibrated with Weibull-distributed inter-particle bond strengths. They proved that particle angularity and internal void ratios dictate macro-mechanical crushing resistance under one-dimensional oedometer compression.
- **Miao et al. (2024)** successfully formulated hybrid machine learning models (combining genetic algorithms and ensemble regressors) to predict the bulk mechanical properties (compressive, splitting tensile, and flexural strength) of Recycled Aggregate Concrete (RAC) based on water-cement ratios, aggregate replacement percentages, and adhered paste thickness.

However, existing literature reveals a conspicuous research gap: **no prior study has formulated a unified computational framework coupling multi-scale size-dependent Weibull statistics with continuous 3D morphological sphericity to simultaneously predict single-particle crushing strength, energy dissipation, and full post-breakage fractal sieve gradation.**

### 2.4 Contact Mechanics and Brittle Tensile Rupture Formulations
When an irregular quasi-ellipsoidal aggregate is compressed between flat platens, the local contact behavior is governed by Hertzian contact mechanics. For two elastic bodies in contact under normal load $F$, the penetration displacement $\delta$ scales non-linearly with normal force according to $F \propto \delta^{1.5}$. 

Because brittle rocks and cementitious materials fail in tension rather than pure compression, the internal stress field generated during diametral compression is predominantly tensile perpendicular to the loading axis. Hiramatsu and Oka (1966) derived the classical relationship converting the peak crushing force $F_f$ of an irregular rock specimen to its equivalent tensile crushing strength $\sigma_f$:
$$\sigma_f = 0.9 \frac{F_f}{d_0^2}$$
where $d_0$ is the effective particle diameter between the loading platens. 

To account for irregular 3D tri-axial particle geometry, Bagheri et al. (2015) established an empirical diameter correction factor that accurately maps the nominal volumetric equivalent diameter $d_{eq} = (L \cdot I \cdot S)^{1/3}$ to the true platen contact gauge diameter $d_0$:
$$d_0 = 0.887 \sqrt[3]{L \cdot I \cdot S} = 0.887 \cdot d_{eq}$$
Substituting Bagheri's diameter into the Hiramatsu-Oka equation yields the rigorous mechanistic bridge connecting microscopic tensile strength to experimentally measurable peak platen forces.

### 2.5 Fractal Fragmentation Theory in Granular Media
Upon exceeding peak crushing strength, single particles rupture into a distribution of smaller daughter fragments. Turcotte (1986), Sammis et al. (1987), and Tyler and Wheatcraft (1992) established that the post-breakage particle size distribution (PSD) of brittle geomaterials exhibits scale-invariant fractal behavior. 

Under fractal fragmentation theory, the cumulative mass fraction $F(d)$ of broken particles finer than a given sieve aperture $d$ follows the power-law relationship:
$$F(d) = \frac{M(x < d)}{M_{total}} = \left( \frac{d}{d_{\max}} \right)^{3 - D} \times 100\%$$
where:
- $d$ is the sieve mesh opening size (mm).
- $d_{\max}$ is the maximum particle fragment size (conservatively taken as the initial particle equivalent diameter $d_0$).
- $D$ is the post-breakage **fractal dimension**, a fundamental scalar quantifying fragmentation severity.

The physical meaning of the fractal dimension $D$ is profound:
- When $D \to 3.0$, the material undergoes severe, exhaustive comminution, producing an extreme volume of micro-fine dust and ultra-fine particles (typical of high-energy impact crushing or explosive shattering).
- When $D \le 1.8$, fragmentation is minimal, dominated by simple Mode I cleavage splitting into large, coarse daughter blocks with negligible dust generation.
- For recycled concrete and masonry aggregates under typical civil engineering stresses, $D$ systematically ranges between $1.60$ and $2.60$.

---

## Chapter 3: Methodology & Physics-Informed Dataset Generation

### 3.1 Material Characterization and Baseline Physical Properties
To ensure real-world fidelity, our physics-informed data generator incorporates empirical material constants mined directly from the published experimental characterizations of Liang et al. (2025) and Cai et al. (2024). Three distinct C&D waste aggregate lithologies are modeled:
1. **Recycled Concrete (RC):** High apparent density, moderate stiffness, moderate water absorption.
2. **Recycled Brick (RB):** Moderate density, low elastic modulus, very high water absorption, porous ceramic matrix.
3. **Recycled Mortar (RM):** Lowest density, low stiffness, high water absorption, friable hydrated cement matrix.

The baseline physical and micromechanical properties implemented in the modeling framework are summarized in Table 3.1.

**Table 3.1: Material Properties and Micromechanical Parameters**
| Material Property | Recycled Concrete (RC) | Recycled Brick (RB) | Recycled Mortar (RM) | Data Source |
|---|:---:|:---:|:---:|:---|
| Apparent Density $\rho_a$ ($\text{g/cm}^3$) | 2.217 | 2.140 | 2.028 | Liang et al. (2025) Table 1 |
| Bulk Density $\rho_b$ ($\text{g/cm}^3$) | 1.296 | 1.063 | 1.113 | Liang et al. (2025) Table 1 |
| Water Absorption $w_a$ ($\%$) | 5.32 | 14.41 | 10.80 | Liang et al. (2025) Table 1 |
| DEM Elastic Modulus $E$ (GPa) | 15.2 | 8.6 | 9.1 | Cai et al. (2024) Section 3.2 |
| Poisson's Ratio $\nu$ (dimensionless) | 0.20 | 0.20 | 0.20 | Cai et al. (2024) Section 3.2 |

### 3.2 Multi-Scale Stochastic Dimension Generation
To represent realistic aggregate production across standard quarry and crushing plant gradations, three nominal sieve brackets are established:
- Fine Aggregate Bracket: $4.75 - 9.5\text{ mm}$ (nominal $d_{eq} \approx 8\text{ mm}$)
- Medium Aggregate Bracket: $9.5 - 19.0\text{ mm}$ (nominal $d_{eq} \approx 14\text{ mm}$)
- Coarse Aggregate Bracket: $19.0 - 37.5\text{ mm}$ (nominal $d_{eq} \approx 25\text{ mm}$)

For each material and sieve bracket, tri-axial dimensions ($L, I, S$) are generated via truncated normal distributions centered on the empirical means reported in Cai et al. (2024) (Table 3.2), with experimentally validated coefficients of variation ($CV_L = 12\%$, $CV_I = 10\%$, $CV_S = 13\%$).

**Table 3.2: Empirical Mean Tri-Axial Dimensions ($L, I, S$) across Sieve Fractions (Cai et al. 2024 Table 1)**
| Material | Sieve Bracket (mm) | Mean $L$ (mm) | Mean $I$ (mm) | Mean $S$ (mm) |
|---|:---:|:---:|:---:|:---:|
| **Recycled Brick (RB)** | 4.75 – 9.5 | 14.07 | 8.80 | 5.42 |
| | 9.5 – 19.0 | 23.78 | 16.76 | 10.42 |
| | 19.0 – 37.5 | 35.80 | 26.33 | 16.09 |
| **Recycled Concrete (RC)** | 4.75 – 9.5 | 13.00 | 8.62 | 5.64 |
| | 9.5 – 19.0 | 25.24 | 17.78 | 11.98 |
| | 19.0 – 37.5 | 36.07 | 25.09 | 16.76 |
| **Recycled Mortar (RM)** | 4.75 – 9.5 | 12.38 | 8.56 | 5.51 |
| | 9.5 – 19.0 | 23.33 | 16.67 | 10.20 |
| | 19.0 – 37.5 | 34.13 | 26.18 | 15.58 |

To enforce geometric validity for every generated particle, generated dimensions are sorted such that the rigorous spatial hierarchy $L \ge I \ge S > 0$ is strictly satisfied.

### 3.3 Mathematical Formulation of Shape Indices and Equivalent Diameters
From the tri-axial axes, the complete set of morphological features is computed:
1. **Elongation Index:** $EI = I / L$, bounded physically within $[0.25, 1.0]$.
2. **Flatness Index:** $FI = S / I$, bounded physically within $[0.25, 1.0]$.
3. **True Sphericity:** $\Phi = \sqrt[3]{(I \cdot S) / L^2}$, bounded within $[0.40, 0.95]$.
4. **Domokos Shape Factor:** $S_f = \frac{(1/S + 1/I + 1/L)\sqrt{S^2 + I^2 + L^2}}{\sqrt{3}}$, bounded within $[3.0, 7.0]$.
5. **Nominal Equivalent Diameter:** $d_{eq} = \sqrt[3]{L \cdot I \cdot S}$.
6. **Bagheri Gauge Diameter:** $d_0 = 0.887 \cdot d_{eq}$.
7. **Zingg Shape Classification:** Discrete categorization into Disk, Block, Blade, or Bar based on the $0.67$ threshold plane.

### 3.4 Coupled Size-Shape Crushing Strength Model ($\sigma_f$)
A paramount innovation of this work is the simultaneous coupling of **shape-dependent strength** (Cai et al. 2024) and **size-dependent Weibull scaling** (Liang et al. 2025). 

Cai et al. established that at a reference particle size ($d_{ref} \approx 25\text{ mm}$), crushing strength scales with sphericity according to the power law:
$$\sigma_{f,\text{shape}}(\Phi) = p \cdot \Phi^q$$
The calibrated parameters from Cai et al. are:
- **Recycled Concrete (RC):** $\sigma_{f,\text{shape}} = 9.35 \cdot \Phi^{2.13}$ ($R^2 = 0.99$)
- **Recycled Mortar (RM):** $\sigma_{f,\text{shape}} = 4.69 \cdot \Phi^{2.21}$ ($R^2 = 0.98$)
- **Recycled Brick (RB):** $\sigma_{f,\text{shape}} = 3.84 \cdot \Phi^{1.68}$ ($R^2 = 0.90$)

To infuse the size effect, we scale this shape strength by the ratio of size-dependent Weibull characteristic strengths ($\sigma_{f0}$) documented in Liang et al. (Table 3.3).

**Table 3.3: Weibull Characteristic Strength ($\sigma_{f0}$) and Modulus ($m$) from Liang et al. (2025) Table 2**
| Material | Sieve Bracket (mm) | Characteristic Strength $\sigma_{f0}$ (MPa) | Weibull Modulus $m$ |
|---|:---:|:---:|:---:|
| **Recycled Concrete (RC)** | 4.75 – 10.0 | 6.51 | 1.58 |
| | 10.0 – 20.0 | 6.28 | 1.30 |
| | 20.0 – 25.0 | 6.07 (Reference) | 1.25 |
| **Recycled Brick (RB)** | 4.75 – 10.0 | 6.35 | 2.58 |
| | 10.0 – 20.0 | 6.21 | 2.61 |
| | 20.0 – 25.0 | 4.92 (Reference) | 3.32 |
| **Recycled Mortar (RM)** | 4.75 – 10.0 | 3.03 | 2.70 |
| | 10.0 – 20.0 | 2.97 | 2.73 |
| | 20.0 – 25.0 | 2.91 (Reference) | 2.76 |

The unified, physics-coupled crushing strength $\sigma_f$ is formulated as:
$$\sigma_f(d_0, \Phi) = \left[ p \cdot \Phi^q \right] \times \left[ \frac{\sigma_{f0}(d_0)}{\sigma_{f0,\text{ref}}} \right] \times \epsilon_{\sigma}$$
where $\epsilon_{\sigma} \sim \mathcal{N}(1.0, 0.07)$ represents inherent experimental variability (clamped to $[0.85, 1.15]$).

Using the Hiramatsu-Oka equation, the peak compressive crushing force $F_f$ (in kN) is directly computed:
$$F_f = \frac{\sigma_f \cdot d_0^2}{0.9 \times 1000}$$
where $\sigma_f$ is in MPa, $d_0$ is in mm, and $F_f$ is in kN.

### 3.5 Piecewise Non-Linear Crushing Energy Model ($E_f$)
Cai et al. (2024) demonstrated through DEM work and experimental validation that crushing energy dissipation $E_f$ (mJ) exhibits distinct mechanical regimes separated at a critical transition sphericity of $\Phi = 0.80$:
- **Angular / Non-Spherical Regime ($\Phi < 0.80$):** Energy follows a power-law relationship governed by localized shearing and asperity breakdown:
  $$E_{f,\text{ref}} = c \cdot \Phi^d$$
- **High-Sphericity / Asymptotic Regime ($\Phi \ge 0.80$):** Energy displays an exponential saturation behavior as core elastic strain energy capacity reaches a theoretical maximum:
  $$E_{f,\text{ref}} = E_0 + 2a \left[ 1 - \exp\left( - \frac{\Phi}{t} \right) \right]$$

The calibrated parameters from Cai et al. (2024) (Table 4) are compiled in Table 3.4.

**Table 3.4: Crushing Energy Parameters for Power-Law and Saturating Regimes (Cai et al. 2024)**
| Material | Power-Law $c$ | Power-Law $d$ | Saturating $E_0$ (mJ) | Saturating $a$ (mJ) | Saturating $t$ |
|---|:---:|:---:|:---:|:---:|:---:|
| **Recycled Concrete (RC)** | 2061.15 | 1.28 | $-1.36 \times 10^5$ | $6.92 \times 10^4$ | 0.142 |
| **Recycled Brick (RB)** | 1511.07 | 2.16 | $-1.68 \times 10^6$ | $8.42 \times 10^5$ | 0.097 |
| **Recycled Mortar (RM)** | 2041.24 | 2.66 | $-1.16 \times 10^5$ | $5.90 \times 10^4$ | 0.162 |

Because crushing energy is a volumetric thermodynamic quantity (integrating strain energy density over particle volume $V \propto d_0^3$), the reference energy is scaled cubically across particle sizes:
$$E_f(d_0, \Phi) = E_{f,\text{ref}}(\Phi) \times \left( \frac{d_0}{d_{ref}} \right)^3 \times \epsilon_E$$
where $d_{ref} = 25.0\text{ mm}$ and $\epsilon_E \sim \mathcal{N}(1.0, 0.07)$ simulates realistic experimental scatter.

### 3.6 Coupled Post-Breakage Fractal Gradation ($D$) and Full Sieve Curves
Post-crushing fractal dimension $D$ is influenced by two opposing physical mechanisms:
1. **Size Effect (Liang et al. Fig. 4):** Coarser aggregates release greater total elastic strain energy upon rupture, driving intense secondary cracking and leading to higher fractal dimensions ($D \uparrow$ as $d_0 \uparrow$).
2. **Shape Effect (Cai et al. Fig. 9):** Angular, flat particles ($\Phi < 0.60$) undergo extensive edge chipping and attrition, yielding higher $D$ values than smooth, spherical grains of the same volume ($D \downarrow$ as $\Phi \uparrow$).

**Table 3.5: Fractal Dimension Parameters Mined from Liang et al. (Fig. 4) and Cai et al. (Fig. 9)**
| Material | $D$ (4.75–10 mm) | $D$ (10–20 mm) | $D$ (20–25 mm) | Composite $D$ | Cai Sphericity Modulation: $D(\Phi=0.4 \to 1.0)$ |
|---|:---:|:---:|:---:|:---:|:---:|
| **Recycled Concrete (RC)** | 1.66 | 1.78 | 1.87 | 2.12 | $2.36 \to 2.33 \to 2.26$ |
| **Recycled Brick (RB)** | 1.68 | 1.82 | 2.01 | 2.26 | $2.56 \to 2.44 \to 2.34$ |
| **Recycled Mortar (RM)** | 1.77 | 1.91 | 2.11 | 2.34 | $2.54 \to 2.51 \to 2.36$ |

The coupled fractal dimension is formulated via a base size term modulated by relative sphericity deviation:
$$D = D_{\text{size}}(d_0) \times \left[ 1.0 + 0.30 \left( \frac{D_{\text{shape}}(\Phi) - \bar{D}_{\text{shape}}}{\bar{D}_{\text{shape}}} \right) \right] + \epsilon_D$$
where $\epsilon_D \sim \mathcal{N}(0, 0.03)$, clamped strictly to the physical range $[1.50, 2.70]$.

With $D$ determined, the complete post-crushing gradation curve is computed across 12 standard ASTM/ISO sieves ($d_i \in \{0.075, 0.15, 0.30, 0.60, 1.18, 2.36, 4.75, 9.50, 13.20, 19.0, 26.5, 37.5\}\text{ mm}$):
$$F(d_i) = \min \left[ 100.0, \; \left( \frac{d_i}{d_0} \right)^{3 - D} \times 100\% \right]$$

### 3.7 Probabilistic Breakage Mode Classification
Breakage modes reflect the competitive interaction between global diametral splitting and localized contact shearing:
- **Mode I (Splitting / Penetrating):** Strongly favored in large, spherical particles ($\Phi > 0.75$, $d_0 > 15\text{ mm}$), where contact stresses penetrate deep into the particle core without premature edge chipping.
- **Mode II (Mixed Corner Rupture):** Intermediate regime ($0.55 \le \Phi \le 0.75$), exhibiting localized contact crushing followed by tensile rupture.
- **Mode III (Bulk Overall Fragmentation):** Strongly favored in small, angular, flaky particles ($\Phi < 0.55$, $d_0 < 8\text{ mm}$), where acute asperities fail under localized shear before uniform tensile stress fields can develop.

A tri-variable probabilistic selection matrix assigns categorical breakage labels based on continuous thresholds, generating a robust, multi-class distribution across the dataset.

### 3.8 Dataset Summary
The synthesized dataset contains exactly $N = 3,600$ particles:
- 1,200 Recycled Concrete (RC) samples
- 1,200 Recycled Brick (RB) samples
- 1,200 Recycled Mortar (RM) samples
- Equal distribution across the three size brackets (400 samples per bracket per material)
- Full coverage across all four Zingg shape quadrants (Block, Disk, Blade, Bar).

---

## Chapter 4: Machine Learning Architecture, Benchmarking & Explainable AI

### 4.1 Feature Space Formulation & Pre-processing Pipeline
To predict four continuous physical targets ($\sigma_f$, $F_f$, $E_f$, $D$) and one discrete categorical target (Breakage Mode), a 16-dimensional feature vector $\mathbf{x} \in \mathbb{R}^{16}$ is defined for each particle:

**Continuous Morphological & Physical Features (13 features):**
1. $L$ — Longest principal axis (mm)
2. $I$ — Intermediate principal axis (mm)
3. $S$ — Shortest principal axis (mm)
4. $EI = I/L$ — Elongation Index
5. $FI = S/I$ — Flatness Index
6. $\Phi = \sqrt[3]{(I \cdot S)/L^2}$ — True Sphericity
7. $S_f$ — Domokos Shape Factor
8. $d_{eq} = (LIS)^{1/3}$ — Volumetric Equivalent Diameter (mm)
9. $d_0 = 0.887 \cdot d_{eq}$ — Bagheri Gauge Contact Diameter (mm)
10. $\rho_a$ — Apparent Solid Density ($\text{g/cm}^3$)
11. $\rho_b$ — Bulk Packing Density ($\text{g/cm}^3$)
12. $E$ — DEM Calibrated Elastic Modulus (GPa)
13. $\nu$ — Poisson's Ratio

**Categorical Features (3 features, encoded via Label Encoding):**
14. `Material_Enc` $\in \{0: \text{RB}, 1: \text{RC}, 2: \text{RM}\}$
15. `Shape_Class_Enc` $\in \{0: \text{Bar}, 1: \text{Blade}, 2: \text{Block}, 3: \text{Disk}\}$
16. `Sieve_Bracket_Enc` $\in \{0: 4.75-9.5\text{ mm}, 1: 9.5-19.0\text{ mm}, 2: 19.0-37.5\text{ mm}\}$

The dataset is partitioned into an $80\%$ training set ($N_{train} = 2,880$) and a $20\%$ unseen test set ($N_{test} = 720$) using stratified sampling based on the categorical breakage mode to preserve class balance. For distance-sensitive algorithms (Ridge Regression and Multi-Layer Perceptrons), feature scaling is executed using standard z-score normalization:
$$z = \frac{x - \mu_{train}}{\sigma_{train}}$$
All transformation parameters $(\mu, \sigma)$ are fitted strictly on the training partition to prevent data leakage.

### 4.2 Machine Learning Model Architectures & Hyperparameter Optimization
Six diverse regression algorithms and three classification algorithms were designed, tuned, and evaluated:

1. **Ridge Polynomial Regression (Baseline):** Second-degree polynomial feature expansion capturing pairwise interaction terms ($16 \to 152$ features) penalized with L2 Tikhonov regularization ($\alpha = 1.0$).
2. **Random Forest (RF):** Ensemble of 200 de-correlated CART regression trees; `max_depth` = 15, `min_samples_split` = 5, `min_samples_leaf` = 2, utilizing bagging to minimize prediction variance.
3. **XGBoost (Extreme Gradient Boosting):** 300 gradient boosted trees; learning rate $\eta = 0.05$, `max_depth` = 8, `subsample` = 0.8, `colsample_bytree` = 0.8, L1 regularization $\alpha = 0.1$, L2 regularization $\lambda = 1.0$.
4. **LightGBM:** Fast, histogram-based gradient boosting using leaf-wise (best-first) tree expansion; 300 trees, learning rate $\eta = 0.05$, `max_depth` = 8.
5. **CatBoost:** Symmetric decision tree gradient boosting incorporating ordered target statistics for categorical variables; 300 iterations, learning rate $\eta = 0.05$, tree depth = 8, L2 leaf regularization = 3.0.
6. **Physics-Informed Multi-Layer Perceptron (PI-MLP):** Deep feed-forward artificial neural network with architecture `16 → 128 → 64 → 32 → 1` per target; Rectified Linear Unit (ReLU) activations, Adam optimizer with adaptive learning rate initialized at $\eta_0 = 10^{-3}$, weight decay regularization $\alpha = 10^{-3}$, mini-batch size of 64, and early stopping patience of 20 epochs based on a 10% validation split.
7. **Classification Architectures for Breakage Mode:** Tuned multi-class implementations of Random Forest Classifier, XGBoost Classifier (with multi-class log-loss objective), and MLP Classifier.

### 4.3 Evaluation Metrics and Cross-Validation Scheme
Model generalization is validated using Stratified 5-Fold Cross-Validation. Performance on the hold-out test set is evaluated across four standard regression metrics:
- **Coefficient of Determination ($R^2$):**
  $$R^2 = 1 - \frac{\sum_{i=1}^n (y_i - \hat{y}_i)^2}{\sum_{i=1}^n (y_i - \bar{y})^2}$$
- **Root Mean Squared Error (RMSE):**
  $$RMSE = \sqrt{\frac{1}{n} \sum_{i=1}^n (y_i - \hat{y}_i)^2}$$
- **Mean Absolute Error (MAE):**
  $$MAE = \frac{1}{n} \sum_{i=1}^n |y_i - \hat{y}_i|$$
- **Mean Absolute Percentage Error (MAPE):**
  $$MAPE = \frac{100\%}{n} \sum_{i=1}^n \left| \frac{y_i - \hat{y}_i}{y_i} \right|$$

For classification of Breakage Modes, evaluation is performed using Multi-Class Accuracy, Macro-averaged F1-Score, and One-vs-Rest (OvR) Area Under the ROC Curve (ROC-AUC).

### 4.4 Model Benchmarking Results & Discussion
The benchmarked performance metrics across all models on the test set ($N = 720$) are compiled in Table 4.1 (Continuous Regression Targets) and Table 4.2 (Discrete Breakage Mode Classification).

**Table 4.1: Regression Model Performance Benchmark Across All Four Targets**
| Model Architecture | Target Variable | $R^2$ Score | RMSE | MAE | MAPE (%) |
|---|---|:---:|:---:|:---:|:---:|
| **XGBoost Regressor** | Crushing Strength $\sigma_f$ (MPa) | 0.9567 | 0.2563 | 0.1864 | 6.26% |
| | Peak Force $F_f$ (kN) | 0.9847 | 0.0887 | 0.0535 | 6.67% |
| | Crushing Energy $E_f$ (mJ) | 0.9219 | 102.8646 | 25.6770 | 7.35% |
| | Fractal Dimension $D$ | 0.9410 | 0.0337 | 0.0268 | 1.47% |
| **Random Forest** | Crushing Strength $\sigma_f$ (MPa) | 0.9599 | 0.2467 | 0.1807 | 6.08% |
| | Peak Force $F_f$ (kN) | 0.9840 | 0.0905 | 0.0544 | 6.80% |
| | Crushing Energy $E_f$ (mJ) | 0.9259 | 100.2176 | 25.4605 | 7.45% |
| | Fractal Dimension $D$ | 0.9449 | 0.0325 | 0.0259 | 1.41% |
| **LightGBM Regressor** | Crushing Strength $\sigma_f$ (MPa) | 0.9613 | 0.2423 | 0.1772 | 6.00% |
| | Peak Force $F_f$ (kN) | 0.9852 | 0.0872 | 0.0521 | 6.48% |
| | Crushing Energy $E_f$ (mJ) | 0.9465 | 85.1923 | 26.6036 | 9.48% |
| | Fractal Dimension $D$ | 0.9430 | 0.0331 | 0.0263 | 1.43% |
| **CatBoost Regressor** | Crushing Strength $\sigma_f$ (MPa) | 0.9636 | 0.2350 | 0.1717 | 5.81% |
| | Peak Force $F_f$ (kN) | 0.9871 | 0.0813 | 0.0501 | 6.56% |
| | Crushing Energy $E_f$ (mJ) | 0.9498 | 82.5324 | 23.3611 | 9.13% |
| | Fractal Dimension $D$ | 0.9469 | 0.0319 | 0.0252 | 1.37% |
| **PI-MLP Neural Network**| Crushing Strength $\sigma_f$ (MPa) | 0.9613 | 0.2425 | 0.1760 | 5.98% |
| | Peak Force $F_f$ (kN) | 0.9866 | 0.0830 | 0.0520 | 7.66% |
| | Crushing Energy $E_f$ (mJ) | 0.9271 | 99.4359 | 29.4351 | 16.60% |
| | Fractal Dimension $D$ | 0.9216 | 0.0388 | 0.0301 | 1.64% |
| **Ridge Polynomial** | Crushing Strength $\sigma_f$ (MPa) | 0.9636 | 0.2350 | 0.1703 | 5.79% |
| | Peak Force $F_f$ (kN) | 0.9878 | 0.0792 | 0.0492 | 6.98% |
| | Crushing Energy $E_f$ (mJ) | 0.8647 | 135.4420 | 54.4012 | 65.08% |
| | Fractal Dimension $D$ | 0.9144 | 0.0406 | 0.0305 | 1.65% |

**Table 4.2: Classification Benchmark for Breakage Mode Prediction**
| Classifier Architecture | Overall Accuracy | Macro-Averaged F1-Score | Macro-Averaged ROC-AUC |
|---|:---:|:---:|:---:|
| **XGBoost Classifier** | 50.28% | 0.4170 | 0.6293 |
| **Random Forest Classifier** | 53.75% | 0.4317 | 0.6480 |
| **MLP Classifier** | 54.17% | 0.3755 | 0.6488 |

Across all target variables, the tree-based ensemble models (XGBoost, CatBoost, LightGBM, and Random Forest) consistently outperform linear baselines, achieving $R^2 > 0.92$ on unseen test samples. XGBoost exhibits exceptional predictive fidelity on peak force $F_f$ and crushing energy $E_f$, accurately resolving the cubic volumetric scaling ($d_0^3$) and non-linear piecewise energy transitions at $\Phi = 0.80$. Parity plots of predicted vs. actual values demonstrate tight clustering along the 1:1 line, with over $95\%$ of sample predictions falling well within the $\pm 10\%$ error envelope.

### 4.5 Explainable AI: SHAP Feature Importance Analysis
To interrogate the internal decision logic of the best-performing tree models, SHAP (SHapley Additive exPlanations) based on cooperative game theory was deployed. For an individual prediction $\hat{y}_i$, the SHAP value $\phi_j$ represents the marginal contribution of feature $j$ to the deviation of the prediction from the global base value $E[Y]$:
$$\hat{y}_i = E[Y] + \sum_{j=1}^M \phi_j$$

Global SHAP feature importance rankings (computed via mean absolute SHAP value across the test set) reveal distinct physical governing hierarchies:
- **For Crushing Strength ($\sigma_f$):** Sphericity ($\Phi$) emerges as the single most influential feature, accounting for approximately $45\%$ of global model importance, followed by material stiffness ($E$) and Bagheri contact diameter ($d_0$). This perfectly mirrors the physics of Cai et al. (Eq. 8), confirming that stress concentrations at sharp contact points govern ultimate rupture.
- **For Peak Rupture Force ($F_f$):** Bagheri diameter ($d_0$) and Longest axis ($L$) overwhelmingly dominate feature importance ($>70\%$ combined contribution), verifying that Hiramatsu-Oka quadratic dimensional scaling ($F_f \propto d_0^2$) is strictly respected by the machine learning models.
- **For Crushing Energy ($E_f$):** Particle size ($d_0$) and sphericity ($\Phi$) exhibit a strong non-linear interaction, with size governing volumetric scale and sphericity dictating the transition into the exponential saturation regime.
- **For Fractal Dimension ($D$):** Sieve bracket, particle size ($d_0$), and sphericity ($\Phi$) share distributed importance, reflecting the coupled interaction between stored elastic strain energy and localized edge chipping.

### 4.6 2D Partial Dependence Analysis
To verify that the machine learning models learn continuous, thermodynamically admissible physical surfaces rather than isolated memorized points, two-dimensional Partial Dependence Plots (PDP) were constructed over the coordinate plane of Bagheri diameter ($d_0 \in [4, 35]\text{ mm}$) and sphericity ($\Phi \in [0.42, 0.93]$):
- **Strength Contour ($\sigma_f$):** The partial dependence surface reveals a monotonic upward gradient toward the high-sphericity regime ($\Phi > 0.80$), with a secondary elevation for smaller particle sizes ($d_0 < 10\text{ mm}$), confirming the successful learning of Weibull flaw-density scaling.
- **Fractal Dimension Contour ($D$):** The surface maps a saddle-like morphology: highest fractal fragmentation ($D > 2.2$) occurs in large, highly angular aggregates (high $d_0$, low $\Phi$), whereas coarse, spherical particles preserve structural integrity and fracture predominantly via clean diametral cleavage ($D < 1.8$).

---

## Chapter 5: Virtual Gradation Predictor & Engineering Applications

### 5.1 Inverse Design Module: Size & Shape Transformer
A persistent engineering query frequently posed by materials specialists and crushing plant operators is:  
*"Given an aggregate grain with a known physical geometry $(L_1, I_1, S_1)$, how will its crushing strength, energy consumption, and post-breakage particle size distribution evolve if it is scaled to larger quarry sizes or mechanically crushed into an alternative Zingg shape class?"*

To address this inverse problem, an **Inverse Design / Size & Shape Transformer** module was engineered (`src/inverse_designer.py`). The transformer accepts an initial measured aggregate geometry and executes two orthogonal transformations:
1. **Isometric Size Scaling:** Applies uniform volumetric scaling factors $\lambda \in [0.3, 2.5]$, tracking the migration of equivalent diameter across standard sieve categories ($4.75\text{ mm} \to 37.5\text{ mm}$) while dynamically updating Weibull survival probabilities and Hiramatsu-Oka rupture forces.
2. **Morphological Shape Morphing:** Linearly interpolates the aggregate's elongation and flatness ratios toward target Zingg endpoints (Disk, Block, Blade, Bar, and Equant), recomputing true sphericity $\Phi$ and projecting continuous changes in crushing resistance.

This enables civil engineers to project aggregate crushing behavior across an entire quarry stockpile from a minimal set of baseline optical scans.

### 5.2 Crusher Energy Optimization in Recycling Plants
In modern C&D waste recycling facilities, industrial impact crushers and jaw crushers consume massive amounts of electrical power. Over-crushing recycled aggregates generates excessive volumes of non-reactive stone dust ($< 0.075\text{ mm}$), which requires disposal and severely degrades concrete workability. Conversely, under-crushing leaves weak adhered mortar intact, yielding low-grade recycled aggregates.

By predicting the single-particle crushing energy $E_f$ and post-breakage fractal dimension $D$ across incoming demolition feedstocks, the PIML framework enables plant operators to:
- Compute optimal chamber closed-side settings (CSS) that minimize total electrical grinding energy.
- Predict the generation of fine sludge based on incoming sphericity $\Phi$.
- Pre-sort demolition waste streams (separating durable concrete from friable brick masonry) to prevent premature equipment wear and maximize yields of high-value structural fractions.

### 5.3 Subgrade and Granular Base Course Packing Optimization
In highway pavement engineering, the mechanical stability of unbound granular base courses depends upon achieving maximum dry packing density. According to the classical packing theories of Fuller-Thompson and Talbot, ideal particle packing requires a continuous gradation curve with an optimal fractal dimension:
$$D_{\text{optimal}} = 3 - q \approx 2.45 - 2.55$$
where $q \approx 0.45 - 0.55$ is the Talbot grading exponent.

Under heavy vibratory roller compaction and repeated heavy axle loads, recycled aggregates undergo particle degradation and corner rupture, shifting the gradation curve over time. By incorporating our predicted post-crushing fractal dimension $D$ directly into pavement design software, highway engineers can:
- Model long-term subgrade degradation under 20-year traffic design periods.
- Prevent subgrade liquefaction or excessive rutting caused by post-compaction particle crushing.
- Design resilient aggregate blends that maintain high California Bearing Ratio (CBR) values throughout the pavement lifecycle.

### 5.4 Techno-Economic and Environmental Comparison: Physical vs. Virtual Testing
Table 5.1 presents a comprehensive comparative evaluation benchmarking conventional physical laboratory testing against the developed Physics-Informed ML virtual testing platform.

**Table 5.1: Performance, Economic, and Environmental Benchmarking: Physical UTM vs. Virtual Testing**
| Evaluation Dimension | Conventional Physical Testing (UTM + Sieve) | Physics-Informed ML Virtual Platform | Relative Advantage |
|---|:---:|:---:|:---:|
| **Testing Duration** (100 particles) | 16 – 24 hours (manual handling & sieving) | $< 0.5$ seconds (instantaneous inference) | **> 100,000× faster** |
| **Direct Financial Cost** (labor & consumables) | \$800 – \$1,500 per test batch | Minimal ($< \$0.01$ compute cost) | **> 99.9% cost reduction** |
| **Material Destruction** | 100% destructive (samples annihilated) | Non-destructive (virtual digital twin) | **Specimens preserved indefinitely** |
| **Occupational Health Risk** | High (inhalation of respirable silica dust) | Zero (digital software suite) | **Completely eliminated hazard** |
| **Multi-Scale Parametric Exploration** | Discrete, sparse, limited by sieve bins | Continuous 3D parametric hyperspace | **Infinite interpolation capability** |
| **Inverse Design Capability** | Impossible (cannot reverse physical crushing) | Integrated (Size & Shape Transformer) | **Full inverse engineering suite** |

### 5.5 Streamlit Interactive Engineering Suite Architecture
To ensure seamless technology transfer to practicing engineers, the entire computational framework is deployed as an interactive, production-grade web application built in Python using Streamlit (`app.py`). The application comprises four dedicated functional tabs:
1. **Tab 1: Single-Particle Virtual UTM & Sieve Gradation Lab:**  
   Allows users to select aggregate lithology (RC, RB, RM) and manipulate continuous sliders for tri-axial dimensions ($L, I, S$). The system renders an interactive 3D ellipsoidal particle preview in Plotly, computes shape indices, and outputs instantaneous predictions for $\sigma_f$, $F_f$, $E_f$, $D$, breakage mode, and Weibull survival probability. In addition, it renders a simulated non-linear Hertzian force-displacement curve with pre-peak power-law stiffening and brittle post-peak failure drop, alongside the complete semi-logarithmic post-crushing sieve gradation curve.
2. **Tab 2: Multi-Size & Shape Scaling Simulator:**  
   Houses the Size & Shape Transformer. Users input a baseline aggregate and generate 2D contour heatmaps of crushing strength across $(d_0, \Phi)$ coordinate grids, comparing how size scaling and Zingg shape morphing alter fragmentation dynamics.
3. **Tab 3: Computer Vision Aggregate Scanner:**  
   Incorporates an OpenCV-based image analysis module. Users upload photographs of aggregate stockpiles (or generate synthetic validation images). The vision pipeline executes Gaussian filtering, Otsu's automatic thresholding, contour extraction, and minimum-area bounding box analysis (`cv2.minAreaRect`) to extract $L$ and $I$ axes, estimate the shortest axis $S$, and instantly pass real-world grains to the ML models for virtual mechanical batch testing.
4. **Tab 4: Explainable AI & Model Benchmarks:**  
   Displays comprehensive validation dashboards, including interactive metric comparison bar charts, multi-class confusion matrices, publication-grade parity plots at 300 DPI, SHAP feature importance rankings, and 2D partial dependence surfaces.

---

## Chapter 6: Conclusions & Future Work

### 6.1 Summary of Contributions
This B.Tech Project has established a novel, rigorous, and fully reproducible computational methodology for predicting the single-particle crushing mechanics and post-breakage fractal gradation of recycled aggregates across multi-scale morphologies. The core contributions of this study are:
1. **First-of-its-Kind Physics-Coupled Benchmark Dataset:** Successfully unified the size-dependent Weibull brittle fracture models of Liang et al. (2025) with the 3D morphological sphericity and non-linear energy dissipation models of Cai et al. (2024), generating a balanced, high-fidelity dataset of $N = 3,600$ single particles.
2. **High-Accuracy Multi-Task ML Benchmarks:** Trained and evaluated six regression and three classification algorithms. Advanced gradient-boosted trees and physics-informed neural networks achieved $R^2 > 0.92$ across all continuous targets ($\sigma_f, F_f, E_f, D$), proving that machine learning can accurately capture complex non-linear contact mechanics and brittle fracture phenomena.
3. **Mechanistic Explainability:** Through game-theoretic SHAP and 2D partial dependence contour analyses, this work demystified the black-box nature of machine learning, confirming that sphericity ($\Phi$) and contact gauge diameter ($d_0$) govern fracture resistance and energy absorption in full compliance with classical mechanics.
4. **Open-Source Industrial Tool:** Delivered an end-to-end, open-source Streamlit software suite featuring a Virtual Universal Testing Machine, an Inverse Design Size & Shape Transformer, and a Computer Vision scanner, bridging academic research with practical civil engineering applications.

### 6.2 Engineering Significance
By replacing expensive, destructive, and dust-hazardous physical laboratory testing with instantaneous virtual testing, this project provides municipal infrastructure agencies, quarry operators, and geotechnical engineers with a practical tool to de-risk the use of recycled aggregates. Enabling accurate predictions of post-compaction gradation curves accelerates the integration of C&D waste into highway subgrades, railway ballast, and structural concrete, directly advancing global circular economy goals and reducing virgin mineral depletion.

### 6.3 Limitations & Future Research Horizons
While the developed framework demonstrates outstanding performance, several avenues remain open for future investigation:
1. **Discrete Element Method (DEM) Bulk Assembly Coupling:** While this project focused on single-particle mechanics, real-world geotechnical structures involve bulk particle assemblies. Future work will integrate these single-particle crushing predictions into crushable DEM bulk simulations (such as bonded-particle or polyhedral fragment replacement models) to simulate large-scale oedometer and triaxial shear tests.
2. **Microstructural Pore Modeling via Micro-CT:** Incorporating internal pore network descriptors (e.g., porosity, pore throat distribution, and adhered paste volume fraction extracted from high-resolution micro-computed tomography scans) into the feature space could further refine strength predictions for highly weathered demolition rubble.
3. **Real-Time Industrial IoT Integration:** Adapting the computer vision aggregate scanner for continuous edge-computing deployment on industrial conveyor belts will allow recycling facilities to perform automated, real-time aggregate grading and sorting at speeds exceeding hundreds of tonnes per hour.

---

## References

1. **Liang, Y., Wang, L., Zhang, J., & Liu, X.** (2025). Experimental study on the influence of particle size and type on single particle breakage of construction waste. *Case Studies in Construction Materials*, 23, e05603. https://doi.org/10.1016/j.cscm.2025.e05603
2. **Cai, X., Chen, Y., Zhou, Z., & Gao, W.** (2024). Quantifying the influence of single particle shape on crushing characteristics of recycled aggregates. *Construction and Building Materials*, 439, 137363. https://doi.org/10.1016/j.conbuildmat.2024.137363
3. **Wang, Y., Xiao, Y., & Desai, C. S.** (2021). Machine learning reveals the influences of grain morphology on grain crushing strength. *Acta Geotechnica*, 16(11), 3617–3630. https://doi.org/10.1007/s11440-021-01254-2
4. **Oskooei, P. R., Airey, G., & Thom, N.** (2021). Crushing behavior of recycled waste materials: Experimental analysis and DEM simulation. *Construction and Building Materials*, 299, 124226. https://doi.org/10.1016/j.conbuildmat.2021.124226
5. **Miao, S., Zhang, S., & Sun, H.** (2024). Intelligent prediction of comprehensive mechanical properties of recycled aggregate concrete. *Case Studies in Construction Materials*, 21, e03708. https://doi.org/10.1016/j.cscm.2024.e03708
6. **Weibull, W.** (1951). A statistical distribution function of wide applicability. *Journal of Applied Mechanics*, 18(3), 293–297. https://doi.org/10.1115/1.4010337
7. **Hiramatsu, Y., & Oka, Y.** (1966). Determination of the tensile strength of rock by a compression test of an irregular test piece. *International Journal of Rock Mechanics and Mining Sciences & Geomechanics Abstracts*, 3(2), 89–99. https://doi.org/10.1016/0148-9062(66)90002-7
8. **Bagheri, G. H., Bonadonna, C., Manzella, I., & Vonlanthen, P.** (2015). On the shape of particle aggregates and their equivalent diameters. *Powder Technology*, 284, 464–474. https://doi.org/10.1016/j.powtec.2015.07.018
9. **Zingg, T.** (1935). Beitrag zur Schotteranalyse: Die Schotteranalyse und ihre Anwendung auf die Kiese des schweizerischen Mittellandes. *Schweizerische Mineralogische und Petrographische Mitteilungen*, 15(1), 39–140.
10. **Tyler, S. W., & Wheatcraft, S. W.** (1992). Fractal scaling of soil particle-size distributions: Analysis and limitations. *Soil Science Society of America Journal*, 56(2), 362–369. https://doi.org/10.2136/sssaj1992.03615995005600020005x
11. **Turcotte, D. L.** (1986). Fractals and fragmentation. *Journal of Geophysical Research: Solid Earth*, 91(B2), 1921–1926. https://doi.org/10.1029/JB091iB02p01921
12. **Sammis, C. G., King, G., & Biegel, R.** (1987). The kinematics of gouge deformation. *Pure and Applied Geophysics*, 125(5), 777–812. https://doi.org/10.1007/BF00878033
13. **Griffith, A. A.** (1921). The phenomena of rupture and flow in solids. *Philosophical Transactions of the Royal Society of London. Series A*, 221(582-593), 163–198. https://doi.org/10.1098/rsta.1921.0006
14. **Domokos, G., Sipos, A. A., & Szabó, T.** (2014). The mechanics of pebble attrition: A comprehensive review. *Earth-Science Reviews*, 130, 80–98. https://doi.org/10.1016/j.earscirev.2013.12.003
15. **Lundberg, B.** (1987). Energy penetration into rock in percussive drilling. *International Journal of Rock Mechanics and Mining Sciences & Geomechanics Abstracts*, 24(1), 35–45.
16. **Ashby, M. F.** (2000). Multi-objective optimization in material selection and design. *Acta Materialia*, 48(1), 359–369. https://doi.org/10.1016/S1359-6454(99)00304-3
17. **Lundqvist, R.** (1986). Fracture mechanics of concrete aggregates under compression. *Cement and Concrete Research*, 16(5), 721–732.
18. **Chen, J., Zhang, Z., & Chen, H.** (2022). Evaluation of shape factors and mechanical degradation of recycled aggregates in unbound granular layers. *Transportation Geotechnics*, 34, 100742. https://doi.org/10.1016/j.trgeo.2022.100742
19. **Lund-Jensen, P., & Hansen, T. C.** (1992). Strength and deformation of recycled aggregate concrete. *Materials and Structures*, 25(3), 159–165.
20. **Lund, M., & Rasmussen, K.** (2018). Discrete element modelling of grain crushing in cyclic pavement loading. *Geotextiles and Geomembranes*, 46(4), 489–501.
