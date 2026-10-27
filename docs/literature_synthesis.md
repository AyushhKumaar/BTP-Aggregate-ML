# Literature Synthesis for Physics-Informed ML Aggregate Crushing

*Cross-paper data mining for physical constants, boundary conditions, and validation benchmarks*

---

## Primary Reference Papers

### Paper 1: Liang et al. (2025)
**"Experimental study on the influence of particle size and type on single particle breakage of construction waste"**
*Case Studies in Construction Materials* 23, e05603.

**Key Contributions:**
- Systematic study of size-dependent crushing behavior across 4.75–25 mm
- Three material types: Recycled Concrete (RC), Recycled Brick (RB), Recycled Mortar (RM)
- Weibull survival analysis with characteristic strengths (σ_f0) and moduli (m)
- Post-breakage fractal gradation analysis (D values 1.66–2.34)
- Three breakage modes identified: Splitting, Corner Rupture, Bulk Fragmentation

**Key Parameters (Table 1 - Material Properties):**
| Property | RC | RB | RM |
|---|---|---|---|
| Apparent Density (g/cm³) | 2.217 | 2.140 | 2.028 |
| Bulk Density (g/cm³) | 1.296 | 1.063 | 1.113 |
| Water Absorption (%) | 5.32 | 14.41 | 10.80 |

**Key Parameters (Table 2 - Weibull Analysis):**
| Material | Size (mm) | σ_f0 (MPa) | Weibull m |
|---|---|---|---|
| RM | 4.75-10 | 3.03 | 2.70 |
| RM | 10-20 | 2.97 | 2.73 |
| RM | 20-25 | 2.91 | 2.76 |
| RB | 4.75-10 | 6.35 | 2.58 |
| RB | 10-20 | 6.21 | 2.61 |
| RB | 20-25 | 4.92 | 3.32 |
| RC | 4.75-10 | 6.51 | 1.58 |
| RC | 10-20 | 6.28 | 1.30 |
| RC | 20-25 | 6.07 | 1.25 |

**Key Parameters (Fig. 4 - Fractal Dimensions):**
| Material | 4.75-10 mm | 10-20 mm | 20-25 mm | Composite |
|---|---|---|---|---|
| RM | 1.77 | 1.91 | 2.11 | 2.34 |
| RB | 1.68 | 1.82 | 2.01 | 2.26 |
| RC | 1.66 | 1.78 | 1.87 | 2.12 |

---

### Paper 2: Cai et al. (2024)
**"Quantifying the influence of single particle shape on crushing characteristics of recycled aggregates"**
*Construction and Building Materials* 439, 137363.

**Key Contributions:**
- Detailed 3D morphological characterization (L, I, S axes, EI, FI, Sphericity, Domokos Sf)
- Zingg/Sneed-Folk shape classification (Disk, Block, Blade, Bar)
- Shape-dependent crushing strength: σ_f = p·Φ^q (power law)
- Piecewise crushing energy model (Eq. 10, 11)
- DEM simulation validation (E = 15.2, 8.6, 9.1 GPa; ν = 0.20)

**Key Parameters (Table 1 - Tri-axial Dimensions):**
| Material | Sieve (mm) | L (mm) | I (mm) | S (mm) |
|---|---|---|---|---|
| RB | 4.75-9.5 | 14.07 | 8.80 | 5.42 |
| RB | 9.5-19 | 23.78 | 16.76 | 10.42 |
| RB | 19-37.5 | 35.80 | 26.33 | 16.09 |
| RC | 4.75-9.5 | 13.0 | 8.62 | 5.64 |
| RC | 9.5-19 | 25.24 | 17.78 | 11.98 |
| RC | 19-37.5 | 36.07 | 25.09 | 16.76 |
| RM | 4.75-9.5 | 12.38 | 8.56 | 5.51 |
| RM | 9.5-19 | 23.33 | 16.67 | 10.20 |
| RM | 19-37.5 | 34.13 | 26.18 | 15.58 |

**Shape-Strength Power Laws (Eq. 8):**
| Material | p | q | R² |
|---|---|---|---|
| RC | 9.35 | 2.13 | 0.99 |
| RM | 4.69 | 2.21 | 0.98 |
| RB | 3.84 | 1.68 | 0.90 |

**Crushing Energy - Power Law (Φ < 0.8, Eq. 10):**
| Material | c | d |
|---|---|---|
| RC | 2061.15 | 1.28 |
| RM | 2041.24 | 2.66 |
| RB | 1511.07 | 2.16 |

**Crushing Energy - Saturating (Φ ≥ 0.8, Eq. 11, Table 4):**
| Material | E₀ | a | t |
|---|---|---|---|
| RB | -1.68×10⁶ | 8.42×10⁵ | 0.097 |
| RC | -1.36×10⁵ | 6.92×10⁴ | 0.142 |
| RM | -1.16×10⁵ | 5.90×10⁴ | 0.162 |

---

## Cross-Referenced Literature

### Wang et al. (2021)
**"Machine learning reveals the influences of grain morphology on grain crushing strength"**
*Acta Geotechnica* 16, 3617–3630.

**Key Findings:**
- Dataset: 400 3D-scanned rock grains with 24 global shape descriptors
- 8 key descriptors selected via hierarchical clustering (avoiding multicollinearity)
- FDEM (Combined Finite-Discrete Element Method) used for crushing simulation
- ML models mapped non-linear grain morphology → crushing strength relationships
- Local roundness at contact points and global convexity/sphericity critically control stress concentrations
- Angular grains with sharp contacts have significantly lower crushing strength

**Relevance to BTP:** Validates our use of sphericity and shape indices as primary features for ML prediction. Confirms power-law relationships between morphology and strength.

---

### Oskooei et al. (2021)
**"Crushing behavior of recycled waste materials: Experimental analysis and DEM simulation"**
*Construction and Building Materials* 299, 124226.

**Key Findings:**
- DEM models with Weibull-distributed bond strengths for recycled CDW materials
- Particle shape/angularity significantly influences crushing resistance
- Angular recycled particles show distinct stress concentration patterns vs natural aggregates
- Weibull weakest-link theory: P_s = exp[-(σ/σ₀)^m] used for calibration
- Lower Weibull modulus m → higher heterogeneity (characteristic of recycled waste)
- Successfully validated DEM predictions against laboratory 1D compression tests

**Relevance to BTP:** Provides DEM-based validation for our Weibull parameter assumptions. Confirms that recycled aggregates exhibit wider strength variability than natural aggregates.

---

### Miao et al. (2024)
**"Intelligent prediction of comprehensive mechanical properties of recycled aggregate concrete"**
*Case Studies in Construction Materials* 21, e03708.

**Key Findings:**
- Hybrid ML algorithms for predicting compressive, flexural, and splitting tensile strengths of RAC
- Used ensemble methods to capture non-linear multi-variable interactions
- Demonstrated superior prediction accuracy vs traditional empirical formulas
- Incorporated SCM (supplementary cementitious materials) effects

**Relevance to BTP:** Validates the ML approach for predicting recycled aggregate properties. Our work extends from bulk RAC to single-particle mechanics.

---

## Public Dataset Search Results

**Searched repositories:**
- GitHub: "single particle crushing" / "recycled aggregate morphology"
- Zenodo: "grain crushing strength" / "aggregate fracture dataset"
- Figshare: "construction waste crushing" / "particle breakage"
- Mendeley Data: "recycled aggregate" / "single grain strength"

**Result:** No direct public CSV datasets found for single-particle crushing of recycled aggregates. Available datasets are primarily for bulk recycled aggregate concrete (RAC) mixture optimization. The closest relevant open data are supplementary tables within the cited journal papers themselves.

**Conclusion:** Our physics-informed synthetic dataset generation approach (coupling Liang et al. and Cai et al. empirical equations) is the most viable strategy, as no direct experimental CSV data is publicly accessible.

---

## Physical Constants & Boundary Conditions Summary

| Parameter | Value | Source |
|---|---|---|
| Hiramatsu-Oka coefficient | 0.9 | Standard contact mechanics |
| Bagheri diameter correction | 0.887 | Bagheri et al. (2015) |
| Zingg EI/FI threshold | 0.67 (2/3) | Zingg (1935) |
| Fractal gradation model | F(d) = (d/d_max)^(3-D) × 100 | Tyler & Wheatcraft (1992) |
| Weibull survival | P_s = exp[-(σ/σ₀)^m] | Weibull (1951) |
| Sphericity range | [0.42, 0.93] | Cai et al. (2024) |
| Domokos Sf range | [3.03, 6.58] | Cai et al. (2024) |
| DEM Poisson's ratio | 0.20 (all materials) | Cai et al. (2024) |
