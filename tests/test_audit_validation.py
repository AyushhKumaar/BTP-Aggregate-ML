"""
Automated Validation and Scientific Audit Test Suite.
Tests:
  1. Baseline Particle (L=25, I=18, S=12 mm, RC) intermediate and final values.
  2. Input sanitization and boundary condition handling (L, I, S > 0, L >= I >= S).
  3. Physical monotonicity:
     - Strength decreases with increasing particle size (Weibull scaling).
     - Peak force & energy increase with increasing particle size.
     - Strength increases with increasing sphericity.
  4. Material hierarchy: RC > RB, RM in crushing strength and energy.
  5. Quantitative error metrics against published laboratory benchmarks (Cai 2024, Liang 2025).
  6. Post-crushing sieve gradation bounds [0, 100] and monotonic non-decreasing behavior.
"""

import unittest
import numpy as np
import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
SRC_DIR = PROJECT_ROOT / 'src'
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from src.data_generator import (
    compute_shape_indices, compute_gradation_curve, MATERIAL_PROPS, WEIBULL_PARAMS
)
from src.inverse_designer import (
    transform_particle, generate_scaling_grid,
    get_continuous_weibull_params, get_continuous_fractal_dimension,
    compute_validation_error_metrics, EXPERIMENTAL_BENCHMARKS
)


class TestScientificAudit(unittest.TestCase):

    def setUp(self):
        self.L_base = 25.0
        self.I_base = 18.0
        self.S_base = 12.0
        self.material = 'RC'

    def test_baseline_particle_derived_properties(self):
        """Verify baseline particle calculations match analytical derivation."""
        # Equivalent diameters
        d_eq_expected = (25.0 * 18.0 * 12.0) ** (1.0 / 3.0)  # ~17.544 mm
        d0_expected = 0.887 * d_eq_expected                  # ~15.562 mm
        Phi_expected = ((18.0 * 12.0) / (25.0 ** 2)) ** (1.0 / 3.0)  # ~0.7018
        EI_expected = 18.0 / 25.0                              # 0.720
        FI_expected = 12.0 / 18.0                              # 0.667

        shape = compute_shape_indices(
            np.array([self.L_base]), np.array([self.I_base]), np.array([self.S_base])
        )

        self.assertAlmostEqual(shape['d_eq'][0], d_eq_expected, places=2)
        self.assertAlmostEqual(shape['d_bagheri'][0], d0_expected, places=2)
        self.assertAlmostEqual(shape['Phi'][0], Phi_expected, places=3)
        self.assertAlmostEqual(shape['EI'][0], EI_expected, places=3)
        self.assertAlmostEqual(shape['FI'][0], FI_expected, places=3)

    def test_baseline_transformation_metrics(self):
        """Verify baseline particle crushing predictions lie in expected physical ranges."""
        df = transform_particle(self.L_base, self.I_base, self.S_base, self.material, continuous_scaling=True)
        scale_rows = df[df['Morph_Target'].isna()]
        base_row = scale_rows[scale_rows['Scale_Factor'] == 1.0].iloc[0]

        # Strength should be ~ 4.45 - 4.55 MPa
        self.assertGreater(base_row['Sigma_f_MPa'], 4.30)
        self.assertLess(base_row['Sigma_f_MPa'], 4.65)

        # Force should be ~ 1.15 - 1.25 kN
        self.assertGreater(base_row['F_f_kN'], 1.15)
        self.assertLess(base_row['F_f_kN'], 1.30)

        # Crushing energy should be ~ 300 - 330 mJ
        self.assertGreater(base_row['E_f_mJ'], 290.0)
        self.assertLess(base_row['E_f_mJ'], 340.0)

        # Fractal dimension should be ~ 1.78 - 1.85
        self.assertGreater(base_row['Fractal_Dim_D'], 1.75)
        self.assertLess(base_row['Fractal_Dim_D'], 1.85)

    def test_input_validation(self):
        """Verify non-physical inputs (negative/zero dimensions) raise ValueError."""
        with self.assertRaises(ValueError):
            transform_particle(-5.0, 18.0, 12.0, 'RC')

        with self.assertRaises(ValueError):
            transform_particle(25.0, 0.0, 12.0, 'RC')

        with self.assertRaises(ValueError):
            generate_scaling_grid(25.0, 18.0, -2.0, 'RC')

    def test_auto_sorting_of_dimensions(self):
        """Verify dimensions are correctly ordered descending (L >= I >= S)."""
        df_sorted = transform_particle(12.0, 25.0, 18.0, 'RC')
        scale_row = df_sorted[df_sorted['Scale_Factor'] == 1.0].iloc[0]
        self.assertEqual(scale_row['L_mm'], 25.0)
        self.assertEqual(scale_row['I_mm'], 18.0)
        self.assertEqual(scale_row['S_mm'], 12.0)

    def test_physical_size_scaling_monotonicity(self):
        """
        Verify physical trends across size scaling:
        - Strength decreases as particle size increases (Weibull weakest link).
        - Peak force increases as particle size increases (F ~ sigma * d^2).
        - Crushing energy increases as particle size increases (volume scaling ~ d^3).
        """
        scale_factors = np.array([0.5, 0.75, 1.0, 1.5, 2.0])
        df = transform_particle(self.L_base, self.I_base, self.S_base, self.material,
                                scale_factors=scale_factors, continuous_scaling=True)
        scale_rows = df[df['Morph_Target'].isna()]

        sigmas = scale_rows['Sigma_f_MPa'].values
        forces = scale_rows['F_f_kN'].values
        energies = scale_rows['E_f_mJ'].values

        # Strength must decrease monotonically
        self.assertTrue(np.all(np.diff(sigmas) < 0), f"Strength not decreasing: {sigmas}")

        # Force must increase monotonically
        self.assertTrue(np.all(np.diff(forces) > 0), f"Force not increasing: {forces}")

        # Energy must increase monotonically
        self.assertTrue(np.all(np.diff(energies) > 0), f"Energy not increasing: {energies}")

    def test_morphology_monotonicity(self):
        """
        Verify shape effect:
        - More spherical particles (higher Phi) have higher crushing strength and energy.
        """
        df = transform_particle(self.L_base, self.I_base, self.S_base, self.material)
        morph_rows = df[df['Morph_Target'].notna()].copy()
        morph_rows = morph_rows.sort_values(by='Sphericity')

        sigmas = morph_rows['Sigma_f_MPa'].values
        # As sphericity increases, strength must increase
        self.assertTrue(np.all(np.diff(sigmas) > 0), f"Strength not increasing with Phi: {sigmas}")

    def test_material_hierarchy(self):
        """
        Under identical size and shape, Recycled Concrete (RC) has higher crushing
        strength than Recycled Brick (RB) and Recycled Mortar (RM), matching Cai et al. Fig 11.
        """
        df_rc = transform_particle(25.0, 18.0, 12.0, 'RC')
        df_rb = transform_particle(25.0, 18.0, 12.0, 'RB')
        df_rm = transform_particle(25.0, 18.0, 12.0, 'RM')

        sigma_rc = df_rc[df_rc['Scale_Factor'] == 1.0]['Sigma_f_MPa'].values[0]
        sigma_rb = df_rb[df_rb['Scale_Factor'] == 1.0]['Sigma_f_MPa'].values[0]
        sigma_rm = df_rm[df_rm['Scale_Factor'] == 1.0]['Sigma_f_MPa'].values[0]

        self.assertGreater(sigma_rc, sigma_rb)
        self.assertGreater(sigma_rc, sigma_rm)

    def test_validation_error_metrics(self):
        """
        Verify model error metrics against published laboratory benchmarks
        (Cai et al. 2024 & Liang et al. 2025):
        - MAE < 0.15 MPa
        - MAPE < 5.0%
        """
        metrics = compute_validation_error_metrics('RC')
        self.assertLess(metrics['MAE_MPa'], 0.15, f"MAE too high: {metrics['MAE_MPa']}")
        self.assertLess(metrics['MAPE_pct'], 5.0, f"MAPE too high: {metrics['MAPE_pct']}")

    def test_sieve_gradation_validity(self):
        """Verify post-crushing gradation percentages are within [0, 100]% and monotonic."""
        grad = compute_gradation_curve(D=1.80, d_max=15.56)
        sieve_sizes = [float(k.replace('Pass_', '').replace('mm', '')) for k in grad.keys()]
        pcts = list(grad.values())

        for p in pcts:
            self.assertGreaterEqual(p, 0.0)
            self.assertLessEqual(p, 100.0)

        # Must be non-decreasing with sieve size
        self.assertTrue(np.all(np.diff(pcts) >= 0), f"Gradation curve is not non-decreasing: {pcts}")


if __name__ == '__main__':
    unittest.main()
