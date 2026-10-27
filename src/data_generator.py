"""
Physics-Informed Dataset Generator for Single-Particle Crushing Mechanics
of Recycled Aggregates Across Multi-Scale Morphologies.

Couples empirical frameworks from:
  - Liang et al. (2025): Size-dependent Weibull crushing strength & fractal gradation
  - Cai et al. (2024): Shape-dependent (sphericity) crushing strength & energy

Generates N=3,600 samples (1,200 each for RC, RB, RM) with full mechanistic targets.

Author: BTP Project - Physics-Informed ML for Recycled Aggregate Crushing
"""

import numpy as np
import pandas as pd
from pathlib import Path

# ==============================================================================
# 1. MATERIAL PROPERTIES (Liang et al. Table 1 & Cai et al. Section 3.2)
# ==============================================================================

MATERIAL_PROPS = {
    'RC': {
        'name': 'Recycled Concrete',
        'apparent_density': 2.217,  # g/cm3
        'bulk_density': 1.296,      # g/cm3
        'elastic_modulus': 15.2,    # GPa (DEM)
        'poisson_ratio': 0.20,
    },
    'RB': {
        'name': 'Recycled Brick',
        'apparent_density': 2.140,  # g/cm3
        'bulk_density': 1.063,      # g/cm3
        'elastic_modulus': 8.6,     # GPa (DEM)
        'poisson_ratio': 0.20,
    },
    'RM': {
        'name': 'Recycled Mortar',
        'apparent_density': 2.028,  # g/cm3
        'bulk_density': 1.113,      # g/cm3
        'elastic_modulus': 9.1,     # GPa (DEM)
        'poisson_ratio': 0.20,
    },
}

# ==============================================================================
# 2. MORPHOLOGICAL DISTRIBUTIONS (Cai et al. Table 1 - Means)
# ==============================================================================

# Tri-axial dimension means from Cai et al. Table 1
# Format: {material: {sieve_bracket: (L_mean, I_mean, S_mean)}}
DIMENSION_MEANS = {
    'RB': {
        '4.75-9.5':  (14.07, 8.80, 5.42),
        '9.5-19':    (23.78, 16.76, 10.42),
        '19-37.5':   (35.80, 26.33, 16.09),
    },
    'RC': {
        '4.75-9.5':  (13.0, 8.62, 5.64),
        '9.5-19':    (25.24, 17.78, 11.98),
        '19-37.5':   (36.07, 25.09, 16.76),
    },
    'RM': {
        '4.75-9.5':  (12.38, 8.56, 5.51),
        '9.5-19':    (23.33, 16.67, 10.20),
        '19-37.5':   (34.13, 26.18, 15.58),
    },
}

# Coefficient of variation (CV) for realistic scatter â€” derived from Cai et al.
# typical experimental CV for tri-axial measurements of crushed aggregates
DIMENSION_CV = {
    'L': 0.12,  # ~12% CV for longest axis
    'I': 0.10,  # ~10% CV for intermediate axis
    'S': 0.13,  # ~13% CV for shortest axis
}

# ==============================================================================
# 3. WEIBULL SIZE-SCALING PARAMETERS (Liang et al. Table 2)
# ==============================================================================

# Format: {material: {sieve_bracket: (sigma_f0_MPa, weibull_m)}}
WEIBULL_PARAMS = {
    'RM': {
        '4.75-10':  (3.03, 2.70),
        '10-20':    (2.97, 2.73),
        '20-25':    (2.91, 2.76),
    },
    'RB': {
        '4.75-10':  (6.35, 2.58),
        '10-20':    (6.21, 2.61),
        '20-25':    (4.92, 3.32),
    },
    'RC': {
        '4.75-10':  (6.51, 1.58),
        '10-20':    (6.28, 1.30),
        '20-25':    (6.07, 1.25),
    },
}

# ==============================================================================
# 4. SHAPE-DEPENDENT CRUSHING STRENGTH (Cai et al. Eq. 8)
# ==============================================================================

# sigma_f(Phi) = p * Phi^q  at reference size d_ref â‰ˆ 25 mm
SHAPE_STRENGTH_PARAMS = {
    'RC': {'p': 9.35, 'q': 2.13, 'R2': 0.99},
    'RM': {'p': 4.69, 'q': 2.21, 'R2': 0.98},
    'RB': {'p': 3.84, 'q': 1.68, 'R2': 0.90},
}

# ==============================================================================
# 5. CRUSHING ENERGY PIECEWISE (Cai et al. Eq. 10, 11, Table 4)
# ==============================================================================

# For Phi < 0.8: E_f = c * Phi^d  (power law, Eq. 10)
ENERGY_POWER_PARAMS = {
    'RC': {'c': 2061.15, 'd': 1.28},
    'RM': {'c': 2041.24, 'd': 2.66},
    'RB': {'c': 1511.07, 'd': 2.16},
}

# For Phi >= 0.8: E_f = E0 + 2*a * (1 - exp(-Phi/t))  (saturating, Eq. 11)
ENERGY_SATURATING_PARAMS = {
    'RB': {'E0': -1.68e6, 'a': 8.42e5, 't': 0.097},
    'RC': {'E0': -1.36e5, 'a': 6.92e4, 't': 0.142},
    'RM': {'E0': -1.16e5, 'a': 5.90e4, 't': 0.162},
}

# ==============================================================================
# 6. FRACTAL DIMENSION COUPLING (Liang Fig. 4 + Cai Fig. 9)
# ==============================================================================

# Size-dependent D (Liang et al. Fig. 4)
# Format: {material: {sieve_bracket: D_value}}
FRACTAL_SIZE = {
    'RM': {'4.75-10': 1.77, '10-20': 1.91, '20-25': 2.11, 'composite': 2.34},
    'RB': {'4.75-10': 1.68, '10-20': 1.82, '20-25': 2.01, 'composite': 2.26},
    'RC': {'4.75-10': 1.66, '10-20': 1.78, '20-25': 1.87, 'composite': 2.12},
}

# Sphericity-dependent D decrease (Cai et al. Fig. 9)
# D decreases as Phi increases from 0.4 to 1.0
# Format: {material: (D_at_low_Phi, D_at_mid_Phi, D_at_high_Phi)}
FRACTAL_SHAPE = {
    'RB': (2.56, 2.44, 2.34),
    'RC': (2.36, 2.33, 2.26),
    'RM': (2.54, 2.51, 2.36),
}

# Breakage mode probabilities (Liang Fig. 6 & Cai Fig. 8)
# Mode I: Splitting/Penetrating - favored by large, spherical particles
# Mode II: Mixed Corner Rupture - intermediate
# Mode III: Bulk Overall Fragmentation - favored by small, angular particles
BREAKAGE_MODES = ['Mode_I_Splitting_Penetrating',
                  'Mode_II_Mixed_Corner_Rupture',
                  'Mode_III_Bulk_Overall_Fragmentation']

# Standard sieve sizes for gradation curve (mm)
SIEVE_SIZES = [0.075, 0.15, 0.3, 0.6, 1.18, 2.36, 4.75, 9.5, 13.2, 19.0, 26.5, 37.5]


def map_sieve_to_weibull_bracket(d_eq: float) -> str:
    """Map equivalent diameter to the nearest Weibull parameter sieve bracket."""
    if d_eq < 10.0:
        return '4.75-10'
    elif d_eq < 20.0:
        return '10-20'
    else:
        return '20-25'


def map_sieve_to_dimension_bracket(d_eq: float) -> str:
    """Map equivalent diameter to the nearest dimension distribution bracket."""
    if d_eq < 9.5:
        return '4.75-9.5'
    elif d_eq < 19.0:
        return '9.5-19'
    else:
        return '19-37.5'


def generate_dimensions(material: str, sieve_bracket: str, n: int,
                        rng: np.random.Generator) -> np.ndarray:
    """
    Generate tri-axial dimensions (L, I, S) from truncated normal distributions
    matching Cai et al. Table 1 means, with realistic scatter.

    Returns: array of shape (n, 3) with columns [L, I, S], enforcing L >= I >= S.
    """
    means = DIMENSION_MEANS[material][sieve_bracket]
    L_mean, I_mean, S_mean = means

    # Generate with CV-based standard deviations
    L = rng.normal(L_mean, L_mean * DIMENSION_CV['L'], n)
    I = rng.normal(I_mean, I_mean * DIMENSION_CV['I'], n)
    S = rng.normal(S_mean, S_mean * DIMENSION_CV['S'], n)

    # Ensure positivity
    L = np.clip(L, L_mean * 0.5, L_mean * 1.8)
    I = np.clip(I, I_mean * 0.5, I_mean * 1.8)
    S = np.clip(S, S_mean * 0.5, S_mean * 1.8)

    # Enforce L >= I >= S by sorting each row descending
    dims = np.column_stack([L, I, S])
    dims = np.sort(dims, axis=1)[:, ::-1]  # Sort descending per row

    return dims


def compute_shape_indices(L: np.ndarray, I: np.ndarray, S: np.ndarray) -> dict:
    """
    Compute all shape indices from tri-axial dimensions.

    Returns dict of arrays: EI, FI, Phi, Sf, d_eq, d_bagheri, shape_class
    """
    # Elongation Index: EI = I/L
    EI = I / L
    EI = np.clip(EI, 0.29, 0.98)

    # Flatness/Flakiness Index: FI = S/I
    FI = S / I
    FI = np.clip(FI, 0.30, 0.96)

    # Sphericity: Phi = (I*S / L^2)^(1/3)
    Phi = np.cbrt((I * S) / (L ** 2))
    Phi = np.clip(Phi, 0.42, 0.93)

    # Domokos Shape Factor: Sf = [(1/S + 1/I + 1/L) * sqrt(S^2 + I^2 + L^2)] / sqrt(3)
    Sf = ((1.0/S + 1.0/I + 1.0/L) * np.sqrt(S**2 + I**2 + L**2)) / np.sqrt(3)
    Sf = np.clip(Sf, 3.03, 6.58)

    # Equivalent diameter: d = (L*I*S)^(1/3)
    d_eq = np.cbrt(L * I * S)

    # Bagheri corrected equivalent diameter: d0 = 0.887 * (L*I*S)^(1/3)
    d_bagheri = 0.887 * d_eq

    # Zingg/Sneed-Folk Shape Classification
    shape_class = np.full(len(L), '', dtype=object)
    mask_disk  = (EI < 0.67) & (FI >= 0.67)
    mask_block = (EI >= 0.67) & (FI >= 0.67)
    mask_blade = (EI < 0.67) & (FI < 0.67)
    mask_bar   = (EI >= 0.67) & (FI < 0.67)
    shape_class[mask_disk]  = 'Disk'
    shape_class[mask_block] = 'Block'
    shape_class[mask_blade] = 'Blade'
    shape_class[mask_bar]   = 'Bar'

    return {
        'EI': EI, 'FI': FI, 'Phi': Phi, 'Sf': Sf,
        'd_eq': d_eq, 'd_bagheri': d_bagheri,
        'Shape_Class': shape_class,
    }


def compute_crushing_strength(material: str, Phi: np.ndarray,
                               d_bagheri: np.ndarray,
                               rng: np.random.Generator) -> tuple:
    """
    Compute coupled crushing strength Ïƒ_f (MPa) and peak force F_f (kN).

    Couples:
      1. Shape effect: Ïƒ_f,shape = p * Phi^q  (Cai et al. Eq. 8)
      2. Size effect via Weibull scaling (Liang et al. Table 2)
      3. Hiramatsu-Oka: Ïƒ_f = 0.9 * F_f / d0^2  â†’  F_f = Ïƒ_f * d0^2 / 0.9

    Returns: (sigma_f, F_f_kN)
    """
    params = SHAPE_STRENGTH_PARAMS[material]
    d_ref = 25.0  # mm reference diameter from Cai et al.

    # Shape-only strength at reference size
    sigma_shape = params['p'] * np.power(Phi, params['q'])

    # Size scaling: apply Weibull characteristic strength ratio
    sigma_f = np.zeros_like(Phi)
    for i in range(len(Phi)):
        d = d_bagheri[i]
        bracket = map_sieve_to_weibull_bracket(d)
        sigma_f0, m = WEIBULL_PARAMS[material][bracket]

        # Scale shape-strength by ratio of size-dependent Weibull Ïƒ_f0
        # to the reference bracket's Ïƒ_f0
        ref_bracket = '20-25'
        sigma_f0_ref, _ = WEIBULL_PARAMS[material][ref_bracket]

        # Combined: shape effect * size scaling ratio
        size_ratio = sigma_f0 / sigma_f0_ref
        sigma_f[i] = sigma_shape[i] * size_ratio

    # Add experimental noise (MAPE ~5-9%)
    noise_std = 0.07  # ~7% relative noise
    noise = rng.normal(1.0, noise_std, len(Phi))
    noise = np.clip(noise, 0.85, 1.15)
    sigma_f *= noise

    # Ensure physical bounds
    sigma_f = np.clip(sigma_f, 0.5, 15.0)

    # Peak force via Hiramatsu-Oka: Ïƒ_f = 0.9 * F_f / d0^2
    # F_f (N) = Ïƒ_f (MPa) * d0^2 (mm^2) / 0.9
    # Convert d0 from mm to m for proper unit: Ïƒ_f in MPa, d0 in mm
    # Ïƒ_f = 0.9 * F_f / d0^2  where F_f in N, d0 in mm, Ïƒ_f in MPa
    F_f_N = sigma_f * (d_bagheri ** 2) / 0.9
    F_f_kN = F_f_N / 1000.0

    return sigma_f, F_f_kN


def compute_crushing_energy(material: str, Phi: np.ndarray,
                             d_bagheri: np.ndarray,
                             rng: np.random.Generator) -> np.ndarray:
    """
    Compute crushing energy E_f (mJ) using Cai et al. piecewise formulation.

    For Phi < 0.8:  E_f = c * Phi^d  (power law, Eq. 10)
    For Phi >= 0.8: E_f = E0 + 2*a * (1 - exp(-Phi/t))  (saturating, Eq. 11)

    Apply volumetric size scaling: (d / d_ref)^3
    """
    d_ref = 25.0  # mm reference
    power_params = ENERGY_POWER_PARAMS[material]
    sat_params = ENERGY_SATURATING_PARAMS[material]

    E_f = np.zeros_like(Phi)

    # Power law region (Phi < 0.8)
    mask_low = Phi < 0.8
    if np.any(mask_low):
        E_f[mask_low] = power_params['c'] * np.power(Phi[mask_low], power_params['d'])

    # Saturating region (Phi >= 0.8)
    mask_high = Phi >= 0.8
    if np.any(mask_high):
        E_f[mask_high] = (sat_params['E0'] +
                          2.0 * sat_params['a'] * (1.0 - np.exp(-Phi[mask_high] / sat_params['t'])))

    # Apply volumetric size scaling
    size_scale = (d_bagheri / d_ref) ** 3
    E_f *= size_scale

    # Add experimental noise (MAPE ~5-9%)
    noise = rng.normal(1.0, 0.07, len(Phi))
    noise = np.clip(noise, 0.85, 1.15)
    E_f *= noise

    # Ensure positive energy
    E_f = np.clip(E_f, 1.0, None)

    return E_f


def compute_fractal_dimension(material: str, Phi: np.ndarray,
                               d_bagheri: np.ndarray,
                               rng: np.random.Generator) -> np.ndarray:
    """
    Compute post-breakage fractal dimension D by coupling:
      1. Size effect (Liang et al. Fig. 4): D increases with particle size
      2. Shape effect (Cai et al. Fig. 9): D decreases as Phi increases

    Linear interpolation is used for both effects.
    """
    # Size-dependent base D
    D_size = np.zeros_like(Phi)
    size_params = FRACTAL_SIZE[material]
    for i in range(len(Phi)):
        d = d_bagheri[i]
        bracket = map_sieve_to_weibull_bracket(d)
        D_size[i] = size_params[bracket]

    # Shape-dependent modulation
    # Interpolate from Cai Fig. 9: at Phi=0.4 â†’ D_high, Phi=0.7 â†’ D_mid, Phi=1.0 â†’ D_low
    D_shape_vals = FRACTAL_SHAPE[material]  # (D_low_Phi, D_mid_Phi, D_high_Phi)
    phi_anchors = np.array([0.4, 0.7, 1.0])
    D_shape_anchors = np.array(D_shape_vals)

    D_shape = np.interp(Phi, phi_anchors, D_shape_anchors)

    # Couple: weighted average of size and shape effects
    # Use D_size as baseline and modulate by shape effect's deviation from its mean
    D_shape_mean = np.mean(D_shape_anchors)
    shape_modulation = (D_shape - D_shape_mean) / D_shape_mean  # fractional deviation

    D = D_size * (1.0 + 0.3 * shape_modulation)  # 30% shape influence

    # Add noise
    noise = rng.normal(0, 0.03, len(Phi))
    D += noise

    # Clip to physically meaningful range
    D = np.clip(D, 1.5, 2.7)

    return D


def compute_gradation_curve(D: float, d_max: float) -> dict:
    """
    Compute post-crushing percentage passing using fractal gradation model.

    F(d_i) = (d_i / d_max)^(3-D) * 100

    Returns dict of {sieve_size_mm: percent_passing}
    """
    gradation = {}
    for d_i in SIEVE_SIZES:
        if d_i <= d_max:
            pct = ((d_i / d_max) ** (3.0 - D)) * 100.0
        else:
            pct = 100.0
        gradation[f'Pass_{d_i}mm'] = round(min(pct, 100.0), 2)
    return gradation


def assign_breakage_mode(material: str, Phi: np.ndarray,
                          d_bagheri: np.ndarray,
                          rng: np.random.Generator) -> np.ndarray:
    """
    Assign breakage mode based on material, size, and sphericity.

    Logic from Liang et al. Fig. 6 & Cai et al. Fig. 8:
    - Mode I (Splitting): High Phi (>0.75), larger size â†’ diametral splitting
    - Mode II (Corner Rupture): Medium Phi (0.55-0.75), medium size â†’ mixed
    - Mode III (Fragmentation): Low Phi (<0.55), smaller size â†’ bulk crushing

    Uses probabilistic assignment with material-dependent thresholds.
    """
    modes = np.full(len(Phi), '', dtype=object)

    for i in range(len(Phi)):
        phi = Phi[i]
        d = d_bagheri[i]

        # Base probabilities (Phi-driven)
        if phi > 0.75:
            p_mode1, p_mode2, p_mode3 = 0.60, 0.30, 0.10
        elif phi > 0.55:
            p_mode1, p_mode2, p_mode3 = 0.20, 0.55, 0.25
        else:
            p_mode1, p_mode2, p_mode3 = 0.10, 0.25, 0.65

        # Size modulation: larger particles â†’ more Mode I splitting
        if d > 20.0:
            p_mode1 += 0.10
            p_mode3 -= 0.10
        elif d < 8.0:
            p_mode3 += 0.10
            p_mode1 -= 0.10

        # Material modulation
        if material == 'RB':
            # Brick is weaker, more fragmentation
            p_mode3 += 0.05
            p_mode1 -= 0.05
        elif material == 'RC':
            # Concrete is stronger, more splitting
            p_mode1 += 0.05
            p_mode3 -= 0.05

        # Normalize probabilities
        probs = np.array([p_mode1, p_mode2, p_mode3])
        probs = np.clip(probs, 0.02, None)
        probs /= probs.sum()

        # Probabilistic assignment
        mode_idx = rng.choice(3, p=probs)
        modes[i] = BREAKAGE_MODES[mode_idx]

    return modes


def generate_dataset(n_per_material: int = 1200, seed: int = 42) -> pd.DataFrame:
    """
    Generate the complete coupled aggregate breakage dataset.

    Parameters:
        n_per_material: Number of samples per material type (default 1200)
        seed: Random seed for reproducibility

    Returns:
        DataFrame with N = 3 * n_per_material samples
    """
    rng = np.random.default_rng(seed)

    # Distribute samples across sieve brackets
    # 4 brackets (including Liang's 4.75-10, 10-20, 20-25 mapped to Cai's brackets)
    brackets = ['4.75-9.5', '9.5-19', '19-37.5']
    n_per_bracket = n_per_material // len(brackets)
    remainder = n_per_material % len(brackets)

    all_records = []

    for material in ['RC', 'RB', 'RM']:
        mat_props = MATERIAL_PROPS[material]

        for b_idx, bracket in enumerate(brackets):
            n_samples = n_per_bracket + (1 if b_idx < remainder else 0)

            # Generate dimensions
            dims = generate_dimensions(material, bracket, n_samples, rng)
            L, I, S = dims[:, 0], dims[:, 1], dims[:, 2]

            # Compute shape indices
            shape = compute_shape_indices(L, I, S)

            # Compute targets
            sigma_f, F_f_kN = compute_crushing_strength(
                material, shape['Phi'], shape['d_bagheri'], rng)

            E_f = compute_crushing_energy(
                material, shape['Phi'], shape['d_bagheri'], rng)

            D = compute_fractal_dimension(
                material, shape['Phi'], shape['d_bagheri'], rng)

            breakage_mode = assign_breakage_mode(
                material, shape['Phi'], shape['d_bagheri'], rng)

            # Build records
            for i in range(n_samples):
                record = {
                    'Material': material,
                    'Material_Name': mat_props['name'],
                    'Sieve_Bracket': bracket,
                    'L_mm': round(L[i], 2),
                    'I_mm': round(I[i], 2),
                    'S_mm': round(S[i], 2),
                    'EI': round(shape['EI'][i], 4),
                    'FI': round(shape['FI'][i], 4),
                    'Sphericity': round(shape['Phi'][i], 4),
                    'Domokos_Sf': round(shape['Sf'][i], 4),
                    'Shape_Class': shape['Shape_Class'][i],
                    'd_eq_mm': round(shape['d_eq'][i], 2),
                    'd_bagheri_mm': round(shape['d_bagheri'][i], 2),
                    'Apparent_Density_gcm3': mat_props['apparent_density'],
                    'Bulk_Density_gcm3': mat_props['bulk_density'],
                    'Elastic_Modulus_GPa': mat_props['elastic_modulus'],
                    'Poisson_Ratio': mat_props['poisson_ratio'],
                    # Targets
                    'Sigma_f_MPa': round(sigma_f[i], 4),
                    'F_f_kN': round(F_f_kN[i], 4),
                    'E_f_mJ': round(E_f[i], 2),
                    'Fractal_Dim_D': round(D[i], 4),
                    'Breakage_Mode': breakage_mode[i],
                }

                # Add gradation curve columns
                d_max = shape['d_bagheri'][i]
                gradation = compute_gradation_curve(D[i], d_max)
                record.update(gradation)

                all_records.append(record)

    df = pd.DataFrame(all_records)

    # Shuffle
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)

    return df


def validate_dataset(df: pd.DataFrame) -> dict:
    """Validate dataset integrity and report statistics."""
    report = {
        'total_rows': len(df),
        'null_count': int(df.isnull().sum().sum()),
        'material_counts': df['Material'].value_counts().to_dict(),
        'shape_class_counts': df['Shape_Class'].value_counts().to_dict(),
        'breakage_mode_counts': df['Breakage_Mode'].value_counts().to_dict(),
        'sigma_f_stats': {
            'mean': round(df['Sigma_f_MPa'].mean(), 3),
            'std': round(df['Sigma_f_MPa'].std(), 3),
            'min': round(df['Sigma_f_MPa'].min(), 3),
            'max': round(df['Sigma_f_MPa'].max(), 3),
        },
        'E_f_stats': {
            'mean': round(df['E_f_mJ'].mean(), 1),
            'std': round(df['E_f_mJ'].std(), 1),
            'min': round(df['E_f_mJ'].min(), 1),
            'max': round(df['E_f_mJ'].max(), 1),
        },
        'D_stats': {
            'mean': round(df['Fractal_Dim_D'].mean(), 3),
            'std': round(df['Fractal_Dim_D'].std(), 3),
            'min': round(df['Fractal_Dim_D'].min(), 3),
            'max': round(df['Fractal_Dim_D'].max(), 3),
        },
        'sphericity_range': (round(df['Sphericity'].min(), 3),
                             round(df['Sphericity'].max(), 3)),
    }
    return report


if __name__ == '__main__':
    print("=" * 70)
    print("PHYSICS-INFORMED DATASET GENERATOR")
    print("Coupled Size Ã— Shape Aggregate Crushing Mechanics")
    print("=" * 70)

    # Create output directory
    data_dir = Path(__file__).parent.parent / 'data'
    data_dir.mkdir(exist_ok=True)

    # Generate dataset
    print("\n[1/3] Generating coupled aggregate breakage dataset (N=3600)...")
    df = generate_dataset(n_per_material=1200, seed=42)

    # Save
    output_path = data_dir / 'coupled_aggregate_breakage_dataset.csv'
    df.to_csv(output_path, index=False)
    print(f"  -> Saved to {output_path}")

    # Validate
    print("\n[2/3] Validating dataset integrity...")
    report = validate_dataset(df)

    print(f"  Total rows: {report['total_rows']}")
    print(f"  Null values: {report['null_count']}")
    print(f"  Material distribution: {report['material_counts']}")
    print(f"  Shape classes: {report['shape_class_counts']}")
    print(f"  Breakage modes: {report['breakage_mode_counts']}")
    print(f"  Ïƒ_f range: {report['sigma_f_stats']['min']} â€“ {report['sigma_f_stats']['max']} MPa")
    print(f"  E_f range: {report['E_f_stats']['min']} â€“ {report['E_f_stats']['max']} mJ")
    print(f"  D range: {report['D_stats']['min']} â€“ {report['D_stats']['max']}")
    print(f"  Sphericity range: {report['sphericity_range']}")

    # Assertions
    assert report['total_rows'] == 3600, f"Expected 3600 rows, got {report['total_rows']}"
    assert report['null_count'] == 0, f"Found {report['null_count']} null values"
    assert all(v == 1200 for v in report['material_counts'].values()), \
        f"Unequal material distribution: {report['material_counts']}"

    print("\n[3/3] âœ“ All validations passed!")
    print(f"\nDataset columns ({len(df.columns)}):")
    for col in df.columns:
        print(f"  - {col}: {df[col].dtype}")
    print("\n" + "=" * 70)
    print("DATASET GENERATION COMPLETE")
    print("=" * 70)

