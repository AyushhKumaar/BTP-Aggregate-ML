"""
Inverse Design / Size & Shape Transformer Module.

Calibrated against and validated with peer-reviewed laboratory literature:
  - Liang et al. (2025): Single-particle crushing Weibull characteristics and fractal gradation
    (Case Studies in Construction Materials 23, e05603; DOI: 10.1016/j.cscm.2025.e05603)
  - Cai et al. (2024): Shape-dependent crushing strength & energy of recycled aggregates
    (Construction and Building Materials 439, 137363; DOI: 10.1016/j.conbuildmat.2024.137363)
  - Li et al. (2021): Size effect & fractal fragmentation under static/impact loading
    (Advances in Materials Science and Engineering 2021, 6097897; DOI: 10.1155/2021/6097897)

Takes measured aggregate dimensions (L, I, S in mm) and projects mechanical crushing properties
(strength, peak force, estimated energy, fractal dimension D, and sieve passing curve) across
continuous size scales and Zingg shape morphologies.
"""

import numpy as np
import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

try:
    from src.data_generator import (
        MATERIAL_PROPS, SHAPE_STRENGTH_PARAMS, ENERGY_POWER_PARAMS,
        ENERGY_SATURATING_PARAMS, WEIBULL_PARAMS, FRACTAL_SIZE, FRACTAL_SHAPE,
        SIEVE_SIZES, compute_shape_indices, compute_gradation_curve,
        map_sieve_to_weibull_bracket
    )
except ImportError:
    from data_generator import (
        MATERIAL_PROPS, SHAPE_STRENGTH_PARAMS, ENERGY_POWER_PARAMS,
        ENERGY_SATURATING_PARAMS, WEIBULL_PARAMS, FRACTAL_SIZE, FRACTAL_SHAPE,
        SIEVE_SIZES, compute_shape_indices, compute_gradation_curve,
        map_sieve_to_weibull_bracket
    )

# ==============================================================================
# PUBLISHED EXPERIMENTAL BENCHMARKS (For Direct Quantitative Validation)
# ==============================================================================

EXPERIMENTAL_BENCHMARKS = {
    'Liang2025_Table2': {
        'RC': [
            {'size_bracket': '4.75–10 mm', 'd_nom_mid': 7.375, 'd0_bagheri': 6.54, 'sigma_f0_exp': 6.51, 'm_exp': 1.58, 'D_exp': 1.66},
            {'size_bracket': '10–20 mm', 'd_nom_mid': 15.00, 'd0_bagheri': 13.31, 'sigma_f0_exp': 6.28, 'm_exp': 1.30, 'D_exp': 1.78},
            {'size_bracket': '20–25 mm', 'd_nom_mid': 22.50, 'd0_bagheri': 19.96, 'sigma_f0_exp': 6.07, 'm_exp': 1.25, 'D_exp': 1.87},
        ],
        'RB': [
            {'size_bracket': '4.75–10 mm', 'd_nom_mid': 7.375, 'd0_bagheri': 6.54, 'sigma_f0_exp': 6.35, 'm_exp': 2.58, 'D_exp': 1.68},
            {'size_bracket': '10–20 mm', 'd_nom_mid': 15.00, 'd0_bagheri': 13.31, 'sigma_f0_exp': 6.21, 'm_exp': 2.61, 'D_exp': 1.82},
            {'size_bracket': '20–25 mm', 'd_nom_mid': 22.50, 'd0_bagheri': 19.96, 'sigma_f0_exp': 4.92, 'm_exp': 3.32, 'D_exp': 2.01},
        ],
        'RM': [
            {'size_bracket': '4.75–10 mm', 'd_nom_mid': 7.375, 'd0_bagheri': 6.54, 'sigma_f0_exp': 3.03, 'm_exp': 2.70, 'D_exp': 1.77},
            {'size_bracket': '10–20 mm', 'd_nom_mid': 15.00, 'd0_bagheri': 13.31, 'sigma_f0_exp': 2.97, 'm_exp': 2.73, 'D_exp': 1.91},
            {'size_bracket': '20–25 mm', 'd_nom_mid': 22.50, 'd0_bagheri': 19.96, 'sigma_f0_exp': 2.91, 'm_exp': 2.76, 'D_exp': 2.11},
        ]
    },
    'Cai2024_Fig11_ShapeStrength': {
        'RC': [
            {'Phi': 0.551, 'sigma_f_exp': 2.74, 'd_range': '19–37.5 mm'},
            {'Phi': 0.837, 'sigma_f_exp': 6.47, 'd_range': '19–37.5 mm'},
        ],
        'RB': [
            {'Phi': 0.531, 'sigma_f_exp': 1.17, 'd_range': '19–37.5 mm'},
            {'Phi': 0.856, 'sigma_f_exp': 2.88, 'd_range': '19–37.5 mm'},
        ],
        'RM': [
            {'Phi': 0.542, 'sigma_f_exp': 1.12, 'd_range': '19–37.5 mm'},
            {'Phi': 0.847, 'sigma_f_exp': 3.20, 'd_range': '19–37.5 mm'},
        ]
    },
    'Cai2024_Fig14_Energy': {
        'RC': [
            {'Phi_range': '0.4–0.6 (mean 0.50)', 'Phi_eval': 0.50, 'E_f_exp_mean': 912.42, 'd_range': '19–37.5 mm'},
            {'Phi_range': '0.8–1.0 (mean 0.90)', 'Phi_eval': 0.90, 'E_f_exp_mean': 1598.63, 'd_range': '19–37.5 mm'},
        ],
        'RB': [
            {'Phi_range': '0.4–0.6 (mean 0.50)', 'Phi_eval': 0.50, 'E_f_exp_mean': 349.05, 'd_range': '19–37.5 mm'},
            {'Phi_range': '0.8–1.0 (mean 0.90)', 'Phi_eval': 0.90, 'E_f_exp_mean': 1288.89, 'd_range': '19–37.5 mm'},
        ],
        'RM': [
            {'Phi_range': '0.4–0.6 (mean 0.50)', 'Phi_eval': 0.50, 'E_f_exp_mean': 316.62, 'd_range': '19–37.5 mm'},
            {'Phi_range': '0.8–1.0 (mean 0.90)', 'Phi_eval': 0.90, 'E_f_exp_mean': 1381.18, 'd_range': '19–37.5 mm'},
        ]
    },
    'Li2021_Benchmarks': {
        'D_min_optimal': 1.887,
        'D_max_optimal': 2.631,
        'source': 'Li et al. (2021), AMSE, DOI: 10.1155/2021/6097897'
    }
}


def get_continuous_weibull_params(material: str, d0: float) -> tuple:
    """
    Interpolate Weibull characteristic strength sigma_f0 (MPa) and modulus m
    smoothly across sizes based on the exact laboratory measurements of Liang et al. (2025) Table 2.

    Parameters:
        material: 'RC', 'RB', or 'RM'
        d0: Bagheri equivalent diameter (mm)

    Returns:
        (sigma_f0, m)
    """
    # Liang et al. 2025 Table 2 empirical midpoints:
    # 4.75-10 mm -> d0 midpoint ~ 6.54 mm
    # 10-20 mm   -> d0 midpoint ~ 13.31 mm
    # 20-25 mm   -> d0 midpoint ~ 19.96 mm
    d0_pts = np.array([6.54, 13.31, 19.96])
    s0_pts = np.array([
        WEIBULL_PARAMS[material]['4.75-10'][0],
        WEIBULL_PARAMS[material]['10-20'][0],
        WEIBULL_PARAMS[material]['20-25'][0]
    ])
    m_pts = np.array([
        WEIBULL_PARAMS[material]['4.75-10'][1],
        WEIBULL_PARAMS[material]['10-20'][1],
        WEIBULL_PARAMS[material]['20-25'][1]
    ])

    log_d0 = np.log(d0_pts)
    log_s0 = np.log(s0_pts)
    slope, intercept = np.polyfit(log_d0, log_s0, 1)

    if d0 <= d0_pts[0]:
        s0 = float(np.exp(slope * np.log(max(d0, 1.0)) + intercept))
        m = float(m_pts[0])
    elif d0 >= d0_pts[-1]:
        s0 = float(np.exp(slope * np.log(d0) + intercept))
        m = float(m_pts[-1])
    else:
        s0 = float(np.interp(d0, d0_pts, s0_pts))
        m = float(np.interp(d0, d0_pts, m_pts))

    return s0, m


def get_continuous_fractal_dimension(material: str, d0: float, Phi: float) -> float:
    """
    Compute continuous post-breakage fractal dimension D coupling:
      1. Size scaling from Liang et al. (2025) Fig. 4
      2. Shape modulation from Cai et al. (2024) Fig. 9
    """
    d0_pts = np.array([6.54, 13.31, 19.96, 25.0])
    D_size_pts = np.array([
        FRACTAL_SIZE[material]['4.75-10'],
        FRACTAL_SIZE[material]['10-20'],
        FRACTAL_SIZE[material]['20-25'],
        FRACTAL_SIZE[material].get('composite', 2.12)
    ])
    D_size = float(np.interp(d0, d0_pts, D_size_pts))

    D_shape_vals = FRACTAL_SHAPE[material]
    D_shape = float(np.interp(Phi, [0.4, 0.7, 1.0], list(D_shape_vals)))
    D_shape_mean = float(np.mean(D_shape_vals))
    D = D_size * (1.0 + 0.3 * (D_shape - D_shape_mean) / D_shape_mean)
    return float(np.clip(D, 1.5, 2.7))


def transform_particle(L: float, I: float, S: float, material: str,
                        scale_factors: np.ndarray = None,
                        morph_targets: list = None,
                        continuous_scaling: bool = True) -> pd.DataFrame:
    """
    Transform a single particle across size scales and shape morphologies.

    Parameters:
        L, I, S: Measured tri-axial dimensions (mm), must be > 0.
        material: 'RC', 'RB', or 'RM'
        scale_factors: Array of size scaling factors (e.g., [0.3, 0.5, 1.0, 2.0])
        morph_targets: List of (EI_target, FI_target, Morph_Name) shape morph endpoints
        continuous_scaling: If True, uses smooth empirical interpolation across sizes.

    Returns:
        DataFrame with predicted crushing properties for each transformation.
    """
    if L <= 0 or I <= 0 or S <= 0:
        raise ValueError("Particle dimensions L, I, S must be strictly positive (> 0 mm).")

    # Enforce standard triaxial convention: L >= I >= S
    dims = sorted([float(L), float(I), float(S)], reverse=True)
    L, I, S = dims

    if scale_factors is None:
        scale_factors = np.array([0.3, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5])

    if morph_targets is None:
        # Default: morph across key Zingg diagram zones
        morph_targets = [
            (0.45, 0.80, 'Disk (Oblate)'),
            (0.80, 0.80, 'Block (Equant)'),
            (0.45, 0.45, 'Blade (Triaxial)'),
            (0.80, 0.45, 'Bar (Prolate)'),
            (0.67, 0.67, 'Equant Boundary'),
        ]

    records = []
    params = SHAPE_STRENGTH_PARAMS[material]
    d_ref = 25.0
    sigma_f0_ref, _ = WEIBULL_PARAMS[material]['20-25']

    # 1. Size Scaling transformations (preserving shape)
    for sf in scale_factors:
        L_s, I_s, S_s = L * sf, I * sf, S * sf
        dims_s = sorted([L_s, I_s, S_s], reverse=True)
        L_s, I_s, S_s = dims_s

        shape = compute_shape_indices(
            np.array([L_s]), np.array([I_s]), np.array([S_s])
        )

        Phi = shape['Phi'][0]
        d_eq = shape['d_eq'][0]
        d0 = shape['d_bagheri'][0]

        # Shape strength at reference size
        sigma_shape = params['p'] * (Phi ** params['q'])

        if continuous_scaling:
            sigma_f0, m = get_continuous_weibull_params(material, d0)
            D = get_continuous_fractal_dimension(material, d0, Phi)
        else:
            bracket = map_sieve_to_weibull_bracket(d0)
            sigma_f0, m = WEIBULL_PARAMS[material][bracket]
            D_size = FRACTAL_SIZE[material][bracket]
            D_shape_vals = FRACTAL_SHAPE[material]
            D_shape = np.interp(Phi, [0.4, 0.7, 1.0], list(D_shape_vals))
            D_shape_mean = np.mean(D_shape_vals)
            D = D_size * (1.0 + 0.3 * (D_shape - D_shape_mean) / D_shape_mean)
            D = float(np.clip(D, 1.5, 2.7))

        # Size-coupled crushing strength
        sigma_f = sigma_shape * (sigma_f0 / sigma_f0_ref)

        # Peak force via Hiramatsu & Oka (1966)
        F_f_N = sigma_f * (d0 ** 2) / 0.9
        F_f_kN = F_f_N / 1000.0

        # Estimated crushing energy (Cai et al. 2024 with volumetric scaling)
        if Phi < 0.8:
            ep = ENERGY_POWER_PARAMS[material]
            E_f = ep['c'] * (Phi ** ep['d'])
        else:
            es = ENERGY_SATURATING_PARAMS[material]
            E_f = es['E0'] + 2 * es['a'] * (1.0 - np.exp(-Phi / es['t']))
        E_f *= (d0 / d_ref) ** 3

        # Gradation curve
        gradation = compute_gradation_curve(D, d0)

        # Weibull survival probability
        P_s = np.exp(-((sigma_f / sigma_f0) ** m))

        record = {
            'Scale_Factor': round(sf, 3),
            'Morph_Target': np.nan,
            'L_mm': round(L_s, 2),
            'I_mm': round(I_s, 2),
            'S_mm': round(S_s, 2),
            'd_eq_mm': round(d_eq, 2),
            'd_bagheri_mm': round(d0, 2),
            'EI': round(shape['EI'][0], 4),
            'FI': round(shape['FI'][0], 4),
            'Sphericity': round(Phi, 4),
            'Shape_Class': shape['Shape_Class'][0],
            'Sigma_f_MPa': round(sigma_f, 4),
            'F_f_kN': round(F_f_kN, 4),
            'E_f_mJ': round(max(E_f, 1.0), 2),
            'Fractal_Dim_D': round(D, 4),
            'Weibull_Ps': round(P_s, 4),
            'Weibull_m': round(m, 2),
        }
        record.update(gradation)
        records.append(record)

    # 2. Morphological transformations at original equivalent volume
    d_eq_orig = (L * I * S) ** (1.0 / 3.0)
    for (EI_t, FI_t, morph_name) in morph_targets:
        # Reconstruct L, I, S from target shape indices preserving constant volume
        # d_eq^3 = L * (EI*L) * (FI*EI*L) = EI^2 * FI * L^3
        # L = d_eq / (EI^2 * FI)^(1/3)
        L_m = d_eq_orig / (EI_t ** 2 * FI_t) ** (1.0 / 3.0)
        I_m = EI_t * L_m
        S_m = FI_t * I_m

        dims_m = sorted([L_m, I_m, S_m], reverse=True)
        L_m, I_m, S_m = dims_m

        shape = compute_shape_indices(
            np.array([L_m]), np.array([I_m]), np.array([S_m])
        )

        Phi = shape['Phi'][0]
        d_eq = shape['d_eq'][0]
        d0 = shape['d_bagheri'][0]

        sigma_shape = params['p'] * (Phi ** params['q'])

        if continuous_scaling:
            sigma_f0, m = get_continuous_weibull_params(material, d0)
            D = get_continuous_fractal_dimension(material, d0, Phi)
        else:
            bracket = map_sieve_to_weibull_bracket(d0)
            sigma_f0, m = WEIBULL_PARAMS[material][bracket]
            D_size = FRACTAL_SIZE[material][bracket]
            D_shape_vals = FRACTAL_SHAPE[material]
            D_shape = np.interp(Phi, [0.4, 0.7, 1.0], list(D_shape_vals))
            D_shape_mean = np.mean(D_shape_vals)
            D = D_size * (1.0 + 0.3 * (D_shape - D_shape_mean) / D_shape_mean)
            D = float(np.clip(D, 1.5, 2.7))

        sigma_f = sigma_shape * (sigma_f0 / sigma_f0_ref)
        F_f_N = sigma_f * (d0 ** 2) / 0.9
        F_f_kN = F_f_N / 1000.0

        if Phi < 0.8:
            ep = ENERGY_POWER_PARAMS[material]
            E_f = ep['c'] * (Phi ** ep['d'])
        else:
            es = ENERGY_SATURATING_PARAMS[material]
            E_f = es['E0'] + 2 * es['a'] * (1.0 - np.exp(-Phi / es['t']))
        E_f *= (d0 / d_ref) ** 3

        gradation = compute_gradation_curve(D, d0)
        P_s = np.exp(-((sigma_f / sigma_f0) ** m))

        record = {
            'Scale_Factor': 1.0,
            'Morph_Target': morph_name,
            'L_mm': round(L_m, 2),
            'I_mm': round(I_m, 2),
            'S_mm': round(S_m, 2),
            'd_eq_mm': round(d_eq, 2),
            'd_bagheri_mm': round(d0, 2),
            'EI': round(shape['EI'][0], 4),
            'FI': round(shape['FI'][0], 4),
            'Sphericity': round(Phi, 4),
            'Shape_Class': shape['Shape_Class'][0],
            'Sigma_f_MPa': round(sigma_f, 4),
            'F_f_kN': round(F_f_kN, 4),
            'E_f_mJ': round(max(E_f, 1.0), 2),
            'Fractal_Dim_D': round(D, 4),
            'Weibull_Ps': round(P_s, 4),
            'Weibull_m': round(m, 2),
        }
        record.update(gradation)
        records.append(record)

    return pd.DataFrame(records)


def generate_scaling_grid(L: float, I: float, S: float, material: str,
                           size_range: tuple = (4.75, 37.5),
                           n_sizes: int = 20,
                           n_shapes: int = 15,
                           continuous_scaling: bool = True) -> pd.DataFrame:
    """
    Generate a 2D scaling grid of (size d0, shape Phi) variations for heatmap visualization.

    Parameters:
        L, I, S: Measured tri-axial dimensions (mm)
        material: 'RC', 'RB', or 'RM'
        size_range: (min_d0, max_d0) in mm
        n_sizes: number of discrete size steps
        n_shapes: number of discrete sphericity steps
        continuous_scaling: whether to use smooth Weibull interpolation

    Returns:
        DataFrame with grid points and predicted crushing targets.
    """
    if L <= 0 or I <= 0 or S <= 0:
        raise ValueError("Particle dimensions L, I, S must be strictly positive (> 0 mm).")

    d_eq_orig = (float(L) * float(I) * float(S)) ** (1.0 / 3.0)
    d0_orig = 0.887 * d_eq_orig

    # Sieve diameter range
    d0_range = np.linspace(size_range[0] * 0.887, size_range[1] * 0.887, n_sizes)
    phi_range = np.linspace(0.42, 0.93, n_shapes)

    records = []
    params = SHAPE_STRENGTH_PARAMS[material]
    d_ref = 25.0
    sigma_f0_ref, _ = WEIBULL_PARAMS[material]['20-25']

    for d0 in d0_range:
        if continuous_scaling:
            sigma_f0, m = get_continuous_weibull_params(material, d0)
        else:
            bracket = map_sieve_to_weibull_bracket(d0)
            sigma_f0, m = WEIBULL_PARAMS[material][bracket]

        for phi_target in phi_range:
            sigma_shape = params['p'] * (phi_target ** params['q'])
            sigma_f = sigma_shape * (sigma_f0 / sigma_f0_ref)

            F_f_N = sigma_f * (d0 ** 2) / 0.9
            F_f_kN = F_f_N / 1000.0

            if phi_target < 0.8:
                ep = ENERGY_POWER_PARAMS[material]
                E_f = ep['c'] * (phi_target ** ep['d'])
            else:
                es = ENERGY_SATURATING_PARAMS[material]
                E_f = es['E0'] + 2 * es['a'] * (1.0 - np.exp(-phi_target / es['t']))
            E_f *= (d0 / d_ref) ** 3

            if continuous_scaling:
                D = get_continuous_fractal_dimension(material, d0, phi_target)
            else:
                bracket = map_sieve_to_weibull_bracket(d0)
                D_size = FRACTAL_SIZE[material][bracket]
                D_shape_vals = FRACTAL_SHAPE[material]
                D_shape = np.interp(phi_target, [0.4, 0.7, 1.0], list(D_shape_vals))
                D_shape_mean = np.mean(D_shape_vals)
                D = D_size * (1.0 + 0.3 * (D_shape - D_shape_mean) / D_shape_mean)
                D = float(np.clip(D, 1.5, 2.7))

            P_s = np.exp(-((sigma_f / sigma_f0) ** m))

            records.append({
                'd_bagheri_mm': round(d0, 2),
                'Sphericity': round(phi_target, 4),
                'Sigma_f_MPa': round(sigma_f, 4),
                'F_f_kN': round(F_f_kN, 4),
                'E_f_mJ': round(max(E_f, 1.0), 2),
                'Fractal_Dim_D': round(D, 4),
                'Weibull_Ps': round(P_s, 4),
                'Weibull_m': round(m, 2),
            })

    return pd.DataFrame(records)


def compute_validation_error_metrics(material: str = 'RC') -> dict:
    """
    Compute quantitative error metrics (MAE, RMSE, MAPE) comparing model predictions
    against published laboratory measurements from Cai et al. (2024) and Liang et al. (2025).

    Returns:
        dict with detailed comparison rows and summary error metrics.
    """
    benchmarks_shape = EXPERIMENTAL_BENCHMARKS['Cai2024_Fig11_ShapeStrength'][material]
    benchmarks_size = EXPERIMENTAL_BENCHMARKS['Liang2025_Table2'][material]
    params = SHAPE_STRENGTH_PARAMS[material]
    sigma_f0_ref, _ = WEIBULL_PARAMS[material]['20-25']

    rows = []
    abs_errors_strength = []
    pct_errors_strength = []

    # 1. Shape-strength comparison (Cai et al. 2024)
    for b in benchmarks_shape:
        phi = b['Phi']
        exp_val = b['sigma_f_exp']
        pred_val = params['p'] * (phi ** params['q'])
        abs_err = abs(pred_val - exp_val)
        pct_err = ((pred_val - exp_val) / exp_val) * 100.0

        abs_errors_strength.append(abs_err)
        pct_errors_strength.append(abs(pct_err))

        rows.append({
            'Category': 'Shape Effect on Sigma_f',
            'Source': 'Cai et al. (2024)',
            'Condition / Range': f"Phi = {phi:.3f} (19-37.5 mm)",
            'Measured': round(exp_val, 2),
            'Predicted': round(pred_val, 2),
            'Units': 'MPa',
            'Abs Error': round(abs_err, 3),
            'Pct Error (%)': f"{pct_err:+.1f}%",
        })

    # 2. Size-scaling Weibull characteristic strength comparison (Liang et al. 2025)
    for b in benchmarks_size:
        d0 = b['d0_bagheri']
        exp_val = b['sigma_f0_exp']
        pred_s0, _ = get_continuous_weibull_params(material, d0)
        abs_err = abs(pred_s0 - exp_val)
        pct_err = ((pred_s0 - exp_val) / exp_val) * 100.0

        abs_errors_strength.append(abs_err)
        pct_errors_strength.append(abs(pct_err))

        rows.append({
            'Category': 'Size Effect on Sigma_f0',
            'Source': 'Liang et al. (2025)',
            'Condition / Range': f"{b['size_bracket']} (d0 ~ {d0:.1f} mm)",
            'Measured': round(exp_val, 2),
            'Predicted': round(pred_s0, 2),
            'Units': 'MPa',
            'Abs Error': round(abs_err, 3),
            'Pct Error (%)': f"{pct_err:+.1f}%",
        })

    # Summary metrics
    mae = float(np.mean(abs_errors_strength))
    rmse = float(np.sqrt(np.mean(np.array(abs_errors_strength) ** 2)))
    mape = float(np.mean(pct_errors_strength))

    return {
        'comparison_df': pd.DataFrame(rows),
        'MAE_MPa': round(mae, 3),
        'RMSE_MPa': round(rmse, 3),
        'MAPE_pct': round(mape, 2),
    }


if __name__ == '__main__':
    print("=" * 70)
    print("INVERSE DESIGN / SIZE & SHAPE TRANSFORMER (AUDITED & VALIDATED)")
    print("=" * 70)

    # Baseline Particle: RC aggregate measured at 25 x 18 x 12 mm
    L, I, S = 25.0, 18.0, 12.0
    material = 'RC'
    print(f"\nBaseline Particle: L={L}, I={I}, S={S} mm ({material})")

    result = transform_particle(L, I, S, material)
    print(f"Generated {len(result)} transformed configurations.")

    scale_rows = result[result['Morph_Target'].isna()]
    print("\nSize Scaling Configurations:")
    print(scale_rows[['Scale_Factor', 'd_bagheri_mm', 'Sphericity', 'Sigma_f_MPa', 'F_f_kN', 'E_f_mJ', 'Fractal_Dim_D']].to_string(index=False))

    morph_rows = result[result['Morph_Target'].notna()]
    print("\nMorphological Target Configurations (Equal Volume):")
    print(morph_rows[['Morph_Target', 'EI', 'FI', 'Sphericity', 'Shape_Class', 'Sigma_f_MPa', 'E_f_mJ', 'Fractal_Dim_D']].to_string(index=False))

    print("\nQuantitative Validation Error Metrics vs. Published Data:")
    val_metrics = compute_validation_error_metrics(material)
    print(val_metrics['comparison_df'].to_string(index=False))
    print(f"\nSummary Metrics: MAE = {val_metrics['MAE_MPa']} MPa | RMSE = {val_metrics['RMSE_MPa']} MPa | MAPE = {val_metrics['MAPE_pct']}%")

    grid = generate_scaling_grid(L, I, S, material)
    output_dir = PROJECT_ROOT / 'data'
    grid.to_csv(output_dir / 'inverse_design_grid.csv', index=False)
    print(f"\nSaved updated scaling grid to {output_dir / 'inverse_design_grid.csv'}")
