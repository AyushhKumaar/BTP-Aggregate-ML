"""
Interactive Engineering Suite - Streamlit Application
for Physics-Informed Aggregate Crushing Prediction & Post-Breakage Gradation.

Audited and benchmarked against published experimental literature:
  - Liang et al. (2025): Case Studies in Construction Materials 23, e05603 (DOI: 10.1016/j.cscm.2025.e05603)
  - Cai et al. (2024): Construction and Building Materials 439, 137363 (DOI: 10.1016/j.conbuildmat.2024.137363)
  - Li et al. (2021): Advances in Materials Science and Engineering 2021, 6097897 (DOI: 10.1155/2021/6097897)

Tabs:
  1. Single-Particle Virtual UTM & Sieve Gradation Lab
  2. Multi-Size & Shape Scaling Simulator (Audited & Validated)
  3. Computer Vision Aggregate Scanner
  4. Explainable AI & Model Benchmarks
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from pathlib import Path
import cv2
import json
import sys

# Add project root and src to path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
SRC_DIR = PROJECT_ROOT / 'src'
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

try:
    from src.data_generator import (
        MATERIAL_PROPS, SHAPE_STRENGTH_PARAMS, ENERGY_POWER_PARAMS,
        ENERGY_SATURATING_PARAMS, WEIBULL_PARAMS, FRACTAL_SIZE, FRACTAL_SHAPE,
        SIEVE_SIZES, compute_shape_indices, compute_gradation_curve,
        map_sieve_to_weibull_bracket
    )
    from src.inverse_designer import (
        transform_particle, generate_scaling_grid,
        get_continuous_weibull_params, get_continuous_fractal_dimension,
        compute_validation_error_metrics, EXPERIMENTAL_BENCHMARKS
    )
except ImportError:
    from data_generator import (
        MATERIAL_PROPS, SHAPE_STRENGTH_PARAMS, ENERGY_POWER_PARAMS,
        ENERGY_SATURATING_PARAMS, WEIBULL_PARAMS, FRACTAL_SIZE, FRACTAL_SHAPE,
        SIEVE_SIZES, compute_shape_indices, compute_gradation_curve,
        map_sieve_to_weibull_bracket
    )
    from inverse_designer import (
        transform_particle, generate_scaling_grid,
        get_continuous_weibull_params, get_continuous_fractal_dimension,
        compute_validation_error_metrics, EXPERIMENTAL_BENCHMARKS
    )

# ==============================================================================
# Page Config
# ==============================================================================
st.set_page_config(
    page_title="Aggregate Crushing ML Lab",
    page_icon="🪨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for dark engineering dashboard
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1.2rem 0;
        background: linear-gradient(135deg, #1e3a8a 0%, #3b0764 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .metric-card {
        background: #1e293b;
        border-radius: 8px;
        padding: 0.9rem;
        text-align: center;
        border-left: 4px solid #3b82f6;
        color: #f8fafc;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 8px 8px 0 0;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🪨 Physics-Informed Aggregate Crushing Lab</h1>
    <p style="margin-top: 5px; opacity: 0.9;">Physics-Informed Machine Learning & Mechanistic Scaling for Recycled Concrete, Brick & Mortar Aggregates</p>
</div>
""", unsafe_allow_html=True)

RESULTS_DIR = PROJECT_ROOT / 'results'
FIGURES_DIR = RESULTS_DIR / 'figures'


def predict_single_particle(L, I, S, material, continuous_scaling=True):
    """Predict all crushing properties for a single particle."""
    if L <= 0 or I <= 0 or S <= 0:
        raise ValueError("Tri-axial dimensions L, I, S must be strictly positive (> 0 mm).")

    dims = sorted([float(L), float(I), float(S)], reverse=True)
    L, I, S = dims

    shape = compute_shape_indices(
        np.array([L]), np.array([I]), np.array([S])
    )

    Phi = shape['Phi'][0]
    d_eq = shape['d_eq'][0]
    d0 = shape['d_bagheri'][0]

    params = SHAPE_STRENGTH_PARAMS[material]
    d_ref = 25.0
    sigma_f0_ref, _ = WEIBULL_PARAMS[material]['20-25']

    # Shape-only crushing strength at reference size
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

    # Hiramatsu & Oka (1966) peak force
    F_f_N = sigma_f * (d0 ** 2) / 0.9
    F_f_kN = F_f_N / 1000.0

    # Crushing energy estimation (Cai et al. 2024 piecewise)
    if Phi < 0.8:
        ep = ENERGY_POWER_PARAMS[material]
        E_f = ep['c'] * (Phi ** ep['d'])
    else:
        es = ENERGY_SATURATING_PARAMS[material]
        E_f = es['E0'] + 2 * es['a'] * (1.0 - np.exp(-Phi / es['t']))
    E_f *= (d0 / d_ref) ** 3
    E_f = max(E_f, 1.0)

    # Gradation
    gradation = compute_gradation_curve(D, d0)

    # Breakage mode classification
    if Phi > 0.75 and d0 > 15:
        mode = 'Mode I: Splitting/Penetrating'
    elif Phi < 0.55 or d0 < 8:
        mode = 'Mode III: Bulk Fragmentation'
    else:
        mode = 'Mode II: Mixed Corner Rupture'

    # Weibull survival probability
    P_s = np.exp(-((sigma_f / sigma_f0) ** m))

    return {
        'L': L, 'I': I, 'S': S,
        'EI': shape['EI'][0], 'FI': shape['FI'][0],
        'Phi': Phi, 'Sf': shape['Sf'][0],
        'd_eq': d_eq, 'd0': d0,
        'shape_class': shape['Shape_Class'][0],
        'sigma_f': sigma_f, 'F_f_kN': F_f_kN,
        'E_f': E_f, 'D': D,
        'breakage_mode': mode,
        'P_s': P_s, 'm': m, 'sigma_f0': sigma_f0,
        'gradation': gradation,
    }


def create_ellipsoid_mesh(L, I, S, n_points=30):
    """Create 3D ellipsoid mesh for particle visualization."""
    u = np.linspace(0, 2 * np.pi, n_points)
    v = np.linspace(0, np.pi, n_points)
    x = (L/2) * np.outer(np.cos(u), np.sin(v))
    y = (I/2) * np.outer(np.sin(u), np.sin(v))
    z = (S/2) * np.outer(np.ones_like(u), np.cos(v))
    return x, y, z


def create_force_displacement_curve(sigma_f, d0, E_mod):
    """
    Simulate a representative force-displacement curve for single-particle crushing
    using Hertzian contact elasticity up to peak failure, followed by exponential brittle post-peak softening.
    """
    delta_max = d0 * sigma_f / (E_mod * 1000)  # mm
    delta_max = max(delta_max, 0.05)

    delta_pre = np.linspace(0, delta_max, 100)
    F_peak = sigma_f * (d0 ** 2) / 0.9  # N
    F_pre = F_peak * (delta_pre / delta_max) ** 1.5

    delta_post = np.linspace(delta_max, delta_max * 2.5, 50)
    F_post = F_peak * np.exp(-5 * (delta_post - delta_max) / delta_max)

    rng = np.random.default_rng(42)
    F_post *= (1 + rng.normal(0, 0.15, len(F_post)))
    F_post = np.clip(F_post, 0, None)

    delta = np.concatenate([delta_pre, delta_post])
    F = np.concatenate([F_pre, F_post])

    return delta, F


# ==============================================================================
# TABS SETUP
# ==============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🔬 Virtual UTM & Sieve Lab",
    "📐 Size & Shape Scaler (Audited)",
    "📷 CV Aggregate Scanner",
    "📊 AI & Benchmarks"
])

# ==============================================================================
# TAB 1: Single-Particle Virtual UTM
# ==============================================================================
with tab1:
    st.header("Single-Particle Virtual Universal Testing Machine")
    st.markdown("*Simulate uniaxial compression of a single aggregate particle with 3D morphology and post-crushing gradation analysis.*")

    col_input, col_viz = st.columns([1, 2])

    with col_input:
        st.subheader("Particle Parameters")
        material = st.selectbox(
            "Material Type", ['RC', 'RB', 'RM'],
            format_func=lambda x: f"{x} - {MATERIAL_PROPS[x]['name']}"
        )

        st.markdown("**Tri-axial Dimensions (mm)**")
        L = st.slider("L (Longest Axis)", 5.0, 45.0, 25.0, 0.5)
        I = st.slider("I (Intermediate Axis)", 3.0, 35.0, 18.0, 0.5)
        S = st.slider("S (Shortest Axis)", 2.0, 25.0, 12.0, 0.5)

        # Automatic ordering check
        if L < I or I < S:
            st.info("ℹ️ Dimensions will be ordered such that L ≥ I ≥ S.")

        result = predict_single_particle(L, I, S, material)

        st.markdown("---")
        st.subheader("Morphological Indices")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Elongation (EI)", f"{result['EI']:.3f}")
            st.metric("Sphericity (Φ)", f"{result['Phi']:.3f}")
        with col_b:
            st.metric("Flatness (FI)", f"{result['FI']:.3f}")
            st.metric("Shape Class", result['shape_class'])

        col_c, col_d = st.columns(2)
        with col_c:
            st.metric("d_eq (Nominal)", f"{result['d_eq']:.1f} mm")
        with col_d:
            st.metric("d₀ (Bagheri)", f"{result['d0']:.1f} mm")

    with col_viz:
        x, y, z = create_ellipsoid_mesh(result['L'], result['I'], result['S'])
        fig_3d = go.Figure(data=[go.Surface(
            x=x, y=y, z=z, colorscale='Viridis',
            showscale=False, opacity=0.85
        )])
        fig_3d.update_layout(
            title=f"3D Particle Preview ({result['shape_class']}) — L={result['L']:.1f}, I={result['I']:.1f}, S={result['S']:.1f} mm",
            scene=dict(
                xaxis_title='L (mm)', yaxis_title='I (mm)', zaxis_title='S (mm)',
                aspectmode='data'
            ),
            height=340, margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig_3d, use_container_width=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Crushing Strength σ_f", f"{result['sigma_f']:.2f} MPa")
        with col2:
            st.metric("Peak Force F_f", f"{result['F_f_kN']:.3f} kN")
        with col3:
            st.metric("Est. Energy E_f", f"{result['E_f']:.1f} mJ")
        with col4:
            st.metric("Fractal Dim D", f"{result['D']:.3f}")

        st.info(f"**Predicted Breakage Mode:** {result['breakage_mode']}")
        st.caption(f"Weibull Survival Probability P_s = {result['P_s']:.3f} (m = {result['m']:.2f}, σ_f0 = {result['sigma_f0']:.2f} MPa)")

    col_plt1, col_plt2 = st.columns(2)

    with col_plt1:
        st.subheader("Post-Crushing Sieve Analysis")
        grad = result['gradation']
        sieve_sizes = [float(k.replace('Pass_', '').replace('mm', '')) for k in grad.keys()]
        pct_passing = list(grad.values())

        fig_grad = go.Figure()
        fig_grad.add_trace(go.Scatter(
            x=sieve_sizes, y=pct_passing,
            mode='lines+markers', name='Predicted Gradation',
            line=dict(color='#3b82f6', width=2.5),
            marker=dict(size=8)
        ))
        fig_grad.update_layout(
            xaxis=dict(title='Sieve Aperture Size (mm)', type='log', showgrid=True, gridcolor='#374151'),
            yaxis=dict(title='Cumulative Percentage Passing (%)', range=[0, 105], showgrid=True, gridcolor='#374151'),
            height=340,
            margin=dict(l=50, r=20, t=30, b=40)
        )
        st.plotly_chart(fig_grad, use_container_width=True)

    with col_plt2:
        st.subheader("Simulated Force-Displacement Response")
        E_mod = MATERIAL_PROPS[material]['elastic_modulus']
        delta, F = create_force_displacement_curve(result['sigma_f'], result['d0'], E_mod)

        fig_fd = go.Figure()
        fig_fd.add_trace(go.Scatter(
            x=delta, y=F/1000,
            mode='lines', name='F-Δ Curve',
            line=dict(color='#ef4444', width=2)
        ))
        fig_fd.add_annotation(
            x=delta[99], y=F[99]/1000,
            text=f"Peak: {F[99]/1000:.3f} kN",
            showarrow=True, arrowhead=2
        )
        fig_fd.update_layout(
            xaxis=dict(title='Displacement Δ (mm)', showgrid=True, gridcolor='#374151'),
            yaxis=dict(title='Compressive Force F (kN)', showgrid=True, gridcolor='#374151'),
            height=340,
            margin=dict(l=50, r=20, t=30, b=40)
        )
        st.plotly_chart(fig_fd, use_container_width=True)
        st.caption("ℹ️ *Note: Synthetic numerical force-displacement curve reconstructed from Hertzian contact elasticity and exponential post-peak softening for visualization. Laboratory UTM records raw continuous load-cell and displacement channels.*")


# ==============================================================================
# TAB 2: Multi-Size & Shape Scaling Simulator (Audited & Validated)
# ==============================================================================
with tab2:
    st.header("Size & Shape Scaling Simulator & Experimental Benchmarking")
    st.markdown(
        "*Scale baseline aggregates across sizes (4.75 → 37.5 mm) or morph particle shape morphologies (Zingg classification) "
        "to simulate post-crushing mechanics, benchmarked against real laboratory datasets.*"
    )

    # 1. Scientific Model Status Badge
    st.markdown("""
    <div style="background-color: #0f172a; border-left: 5px solid #3b82f6; padding: 14px 18px; border-radius: 8px; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
            <div>
                <span style="background-color: #15803d; color: #ffffff; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 0.85rem; letter-spacing: 0.5px;">
                    STATUS: PARTIALLY VALIDATED
                </span>
                <span style="color: #93c5fd; font-weight: 600; margin-left: 10px; font-size: 0.95rem;">
                    Calibrated Against Published Laboratory Literature
                </span>
            </div>
            <div style="color: #94a3b8; font-size: 0.82rem;">
                Cross-Checked with Cai et al. (2024), Liang et al. (2025) & Li et al. (2021)
            </div>
        </div>
        <p style="color: #cbd5e1; font-size: 0.85rem; margin: 8px 0 0 0; line-height: 1.45;">
            <strong>Validated Regimes:</strong> Shape-strength power law (0.42 ≤ Φ ≤ 0.93) calibrated on 19–37.5 mm recycled aggregates (Cai et al. 2024; R² = 0.90–0.99); Size-scaling Weibull characteristic strength (4.75–25.0 mm) and fractal dimension D calibrated on Liang et al. (2025; MAPE = 0.2%); Fragmentation range benchmarked against Li et al. (2021; 1.887 ≤ D ≤ 2.631).<br/>
            <strong>Extrapolated / Empirical Regimes:</strong> Particle sizes d₀ > 37.5 mm or d₀ < 4.75 mm are unvalidated extrapolations. Crushing energy is an empirical volumetric power-law estimation ((d₀/25)³), not a sensor-integrated force-displacement curve. Dynamic/impact crushing is not modeled.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_in2, col_out2 = st.columns([1, 2])

    with col_in2:
        st.subheader("Baseline Particle Inputs")
        mat2 = st.selectbox(
            "Material Type", ['RC', 'RB', 'RM'], key='mat2',
            format_func=lambda x: f"{x} - {MATERIAL_PROPS[x]['name']}"
        )
        L2 = st.number_input("Longest Axis L (mm)", min_value=1.0, max_value=60.0, value=25.0, step=0.5, key='L2')
        I2 = st.number_input("Intermediate Axis I (mm)", min_value=1.0, max_value=50.0, value=18.0, step=0.5, key='I2')
        S2 = st.number_input("Shortest Axis S (mm)", min_value=1.0, max_value=40.0, value=12.0, step=0.5, key='S2')

        # Dimension validation & sorting check
        if L2 < I2 or I2 < S2:
            st.warning("⚠️ Tri-axial convention requires L ≥ I ≥ S. Values will be automatically ordered.")
        dims_sorted = sorted([L2, I2, S2], reverse=True)
        L_eff, I_eff, S_eff = dims_sorted

        # Baseline Particle Derived Metrics
        d_eq_base = (L_eff * I_eff * S_eff) ** (1.0 / 3.0)
        d0_base = 0.887 * d_eq_base
        EI_base = I_eff / L_eff
        FI_base = S_eff / I_eff
        Phi_base = ((I_eff * S_eff) / (L_eff ** 2)) ** (1.0 / 3.0)

        # Zingg shape class
        if EI_base < 0.67 and FI_base >= 0.67:
            z_class = 'Disk (Oblate)'
        elif EI_base >= 0.67 and FI_base >= 0.67:
            z_class = 'Block (Equant)'
        elif EI_base < 0.67 and FI_base < 0.67:
            z_class = 'Blade (Triaxial)'
        else:
            z_class = 'Bar (Prolate)'

        st.markdown(f"""
        <div style="background-color: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 12px; margin-top: 10px;">
            <div style="font-weight: 600; color: #60a5fa; margin-bottom: 6px;">Baseline Geometry (Derived)</div>
            <div style="font-size: 0.85rem; color: #e2e8f0; line-height: 1.6;">
                • <strong>Nominal d_eq:</strong> {d_eq_base:.2f} mm<br/>
                • <strong>Bagheri d₀:</strong> <span style="color: #4ade80; font-weight: bold;">{d0_base:.2f} mm</span> (0.887 factor)<br/>
                • <strong>Sphericity Φ:</strong> <span style="color: #fbbf24; font-weight: bold;">{Phi_base:.3f}</span><br/>
                • <strong>Elongation EI (I/L):</strong> {EI_base:.3f}<br/>
                • <strong>Flatness FI (S/I):</strong> {FI_base:.3f}<br/>
                • <strong>Zingg Shape Class:</strong> {z_class}
            </div>
        </div>
        """, unsafe_allow_html=True)

        scaling_mode = st.radio(
            "Size-Scaling Continuity",
            ["Continuous Weibull Interpolation (Smooth)", "Discrete Sieve Brackets (Step-wise)"],
            index=0,
            help="Continuous Weibull interpolates characteristic strength across Liang et al. (2025) table midpoints without artificial step jumps."
        )
        is_continuous = (scaling_mode == "Continuous Weibull Interpolation (Smooth)")

        run_scaling = st.button("🚀 Run Multi-Scale Simulation", type="primary", use_container_width=True)

    with col_out2:
        with st.spinner("Generating multi-dimensional transformation grid..."):
            grid = generate_scaling_grid(L_eff, I_eff, S_eff, mat2, continuous_scaling=is_continuous)
            tf_result = transform_particle(L_eff, I_eff, S_eff, mat2, continuous_scaling=is_continuous)
            val_metrics = compute_validation_error_metrics(mat2)

            # 1. Heatmap: Sigma_f vs (d0, Phi)
            pivot = grid.pivot_table(values='Sigma_f_MPa', index='d_bagheri_mm', columns='Sphericity')

            fig_heat = go.Figure()
            fig_heat.add_trace(go.Heatmap(
                x=pivot.columns.values,
                y=pivot.index.values,
                z=pivot.values,
                colorscale='Viridis',
                colorbar=dict(
                    title=dict(text='Crushing Strength σ_f (MPa)', side='right'),
                    tickfont=dict(size=11)
                ),
                hovertemplate="Sphericity Φ: %{x:.3f}<br>Bagheri d₀: %{y:.1f} mm<br>σ_f: %{z:.2f} MPa<extra></extra>"
            ))
            # Overlay baseline marker
            fig_heat.add_trace(go.Scatter(
                x=[Phi_base], y=[d0_base],
                mode='markers+text',
                marker=dict(symbol='star', size=14, color='#f97316', line=dict(color='white', width=1.5)),
                name='Baseline Particle',
                text=['★ Baseline'],
                textposition='top right',
                textfont=dict(color='white', size=12, family='sans-serif'),
                hoverinfo='text',
                hovertext=f"Baseline: d₀={d0_base:.2f} mm, Φ={Phi_base:.3f}"
            ))
            fig_heat.update_layout(
                title=dict(
                    text=f'Coupled Crushing Strength σ_f (MPa) vs Size (d₀) & Sphericity (Φ) — {MATERIAL_PROPS[mat2]["name"]}',
                    x=0.0, font=dict(size=14)
                ),
                xaxis=dict(title='Sphericity (Φ) [-]', showgrid=True, gridcolor='#334155'),
                yaxis=dict(title='Equivalent Diameter d₀ (Bagheri) (mm)', showgrid=True, gridcolor='#334155'),
                height=370,
                margin=dict(l=60, r=40, t=50, b=55),
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1.0)
            )
            st.plotly_chart(fig_heat, use_container_width=True)

            st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)

            # 2. Three Detailed Subplots with Overlaid Experimental Data
            if 'Morph_Target' in tf_result.columns:
                scale_data = tf_result[tf_result['Morph_Target'].isna()]
            else:
                scale_data = tf_result.head(8)

            fig_scale = make_subplots(
                rows=1, cols=3,
                subplot_titles=[
                    '<b>(a) Crushing Strength σ_f vs Size</b>',
                    '<b>(b) Estimated Energy E_f vs Size</b>',
                    '<b>(c) Fractal Dimension D vs Size</b>'
                ],
                horizontal_spacing=0.10
            )

            # --- SUBPLOT 1: Strength vs Size ---
            fig_scale.add_trace(
                go.Scatter(
                    x=scale_data['d_bagheri_mm'], y=scale_data['Sigma_f_MPa'],
                    mode='lines+markers', name='Model σ_f',
                    line=dict(color='#3b82f6', width=2.5),
                    marker=dict(size=7),
                    hovertemplate="Model: d₀=%{x:.1f} mm<br>σ_f=%{y:.2f} MPa<extra></extra>"
                ),
                row=1, col=1
            )
            # Overlay Liang et al. (2025) Table 2 experimental data points
            liang_pts = EXPERIMENTAL_BENCHMARKS['Liang2025_Table2'][mat2]
            fig_scale.add_trace(
                go.Scatter(
                    x=[p['d0_bagheri'] for p in liang_pts],
                    y=[p['sigma_f0_exp'] for p in liang_pts],
                    mode='markers', name='Liang (2025) Exp. σ_f0',
                    marker=dict(symbol='diamond', size=10, color='#f59e0b', line=dict(color='white', width=1.2)),
                    hovertemplate="Liang (2025): %{text}<br>d₀=%{x:.1f} mm<br>Exp σ_f0=%{y:.2f} MPa<extra></extra>",
                    text=[p['size_bracket'] for p in liang_pts]
                ),
                row=1, col=1
            )

            # --- SUBPLOT 2: Energy vs Size ---
            fig_scale.add_trace(
                go.Scatter(
                    x=scale_data['d_bagheri_mm'], y=scale_data['E_f_mJ'],
                    mode='lines+markers', name='Model E_f',
                    line=dict(color='#ef4444', width=2.5),
                    marker=dict(size=7),
                    hovertemplate="Model Est.: d₀=%{x:.1f} mm<br>E_f=%{y:.1f} mJ<extra></extra>"
                ),
                row=1, col=2
            )
            # Overlay Cai et al. (2024) Fig. 14 experimental benchmark at reference size (d ~ 25 mm)
            cai_energy_pts = EXPERIMENTAL_BENCHMARKS['Cai2024_Fig14_Energy'][mat2]
            cai_ref_eval = [p['E_f_exp_mean'] for p in cai_energy_pts]
            cai_ref_d0 = [22.18, 22.18]
            fig_scale.add_trace(
                go.Scatter(
                    x=cai_ref_d0,
                    y=cai_ref_eval,
                    mode='markers', name='Cai (2024) Exp. E_f',
                    marker=dict(symbol='square', size=9, color='#ec4899', line=dict(color='white', width=1.2)),
                    hovertemplate="Cai (2024): %{text}<br>Exp E_f=%{y:.1f} mJ<extra></extra>",
                    text=[p['Phi_range'] for p in cai_energy_pts]
                ),
                row=1, col=2
            )

            # --- SUBPLOT 3: Fractal Dimension D vs Size ---
            fig_scale.add_trace(
                go.Scatter(
                    x=scale_data['d_bagheri_mm'], y=scale_data['Fractal_Dim_D'],
                    mode='lines+markers', name='Model D',
                    line=dict(color='#22c55e', width=2.5),
                    marker=dict(size=7),
                    hovertemplate="Model: d₀=%{x:.1f} mm<br>D=%{y:.3f}<extra></extra>"
                ),
                row=1, col=3
            )
            # Overlay Liang et al. (2025) Fig. 4 experimental fractal dimensions
            fig_scale.add_trace(
                go.Scatter(
                    x=[p['d0_bagheri'] for p in liang_pts],
                    y=[p['D_exp'] for p in liang_pts],
                    mode='markers', name='Liang (2025) Exp. D',
                    marker=dict(symbol='circle', size=9, color='#10b981', line=dict(color='white', width=1.2)),
                    hovertemplate="Liang (2025): %{text}<br>Exp D=%{y:.2f}<extra></extra>",
                    text=[p['size_bracket'] for p in liang_pts]
                ),
                row=1, col=3
            )
            # Horizontal lines for Li et al. (2021) optimal gradation range [1.887, 2.631]
            fig_scale.add_hline(
                y=1.887, line_dash='dash', line_color='#94a3b8', row=1, col=3,
                annotation_text='Li (2021) D_min (1.89)', annotation_position='bottom right',
                annotation_font=dict(size=9, color='#94a3b8')
            )
            fig_scale.add_hline(
                y=2.631, line_dash='dash', line_color='#94a3b8', row=1, col=3,
                annotation_text='Li (2021) D_max (2.63)', annotation_position='top right',
                annotation_font=dict(size=9, color='#94a3b8')
            )

            # Explicit axis labels and units on ALL 3 subplots
            fig_scale.update_xaxes(title_text='Equivalent Diameter d₀ (mm)', showgrid=True, gridcolor='#334155', row=1, col=1)
            fig_scale.update_yaxes(title_text='Crushing Strength σ_f (MPa)', showgrid=True, gridcolor='#334155', row=1, col=1)

            fig_scale.update_xaxes(title_text='Equivalent Diameter d₀ (mm)', showgrid=True, gridcolor='#334155', row=1, col=2)
            fig_scale.update_yaxes(title_text='Estimated Crushing Energy E_f (mJ)', showgrid=True, gridcolor='#334155', row=1, col=2)

            fig_scale.update_xaxes(title_text='Equivalent Diameter d₀ (mm)', showgrid=True, gridcolor='#334155', row=1, col=3)
            fig_scale.update_yaxes(title_text='Fractal Dimension D [-]', range=[1.4, 2.8], showgrid=True, gridcolor='#334155', row=1, col=3)

            fig_scale.update_layout(
                height=420,
                margin=dict(l=60, r=40, t=85, b=65),
                showlegend=True,
                legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=1.18,
                    xanchor='center',
                    x=0.5,
                    font=dict(size=10.5),
                    bgcolor='rgba(15, 23, 42, 0.75)',
                    bordercolor='#334155',
                    borderwidth=1
                )
            )
            st.plotly_chart(fig_scale, use_container_width=True)
            st.caption("ℹ️ *Note: Crushing energy is an empirical model estimate scaled by (d₀/25)³, not an integrated laboratory load-displacement sensor curve.*")

    # 3. Quantitative Error Analysis & Comparison Table
    st.markdown("---")
    st.subheader("📊 Quantitative Experimental vs. Model Comparison & Error Metrics")
    st.markdown(
        "*Direct validation of model predictions against published laboratory test measurements "
        f"for {MATERIAL_PROPS[mat2]['name']} ({mat2}).*"
    )

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric("Mean Absolute Error (MAE)", f"{val_metrics['MAE_MPa']:.3f} MPa", help="Average absolute error between model predictions and published lab data points.")
    with col_m2:
        st.metric("Root Mean Squared Error (RMSE)", f"{val_metrics['RMSE_MPa']:.3f} MPa", help="Quadratic penalty on larger prediction deviations.")
    with col_m3:
        st.metric("Mean Absolute Percentage Error (MAPE)", f"{val_metrics['MAPE_pct']:.2f}%", help="Relative percentage error across all benchmark points.")

    st.dataframe(val_metrics['comparison_df'], use_container_width=True)

    # 4. Transformed Configurations & CSV Export
    st.markdown("---")
    st.subheader("📑 Transformed Particle Configurations (Size Scaling & Morphological Morphing)")
    st.markdown(
        f"*Projected crushing metrics for baseline particle (L={L_eff:.1f}, I={I_eff:.1f}, S={S_eff:.1f} mm) "
        "across scale factors and Zingg target morphologies at constant equivalent volume.*"
    )

    csv_export = tf_result.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Full Transformation Dataset (CSV)",
        data=csv_export,
        file_name=f"aggregate_scaling_analysis_{mat2}_{int(L_eff)}x{int(I_eff)}x{int(S_eff)}mm.csv",
        mime="text/csv",
        help="Export all size-scaled and shape-morphed particle parameters, strengths, energies, and post-crushing sieve gradations."
    )
    st.dataframe(tf_result.round(3), use_container_width=True)

    # 5. Methodology & Scientific Model Information Expander
    with st.expander("📚 Methodology, Governing Equations, Units & Scientific Assumptions", expanded=False):
        st.markdown(r"""
### 1. Governing Mechanistic Equations

1. **Roughness-Corrected Particle Diameter (Bagheri et al., 2015; Liang et al., 2025 Eq. 1):**
   $$d_0 = 0.887 \sqrt[3]{L \cdot I \cdot S}$$
   *Accounts for porous surface asperities and adhered residual mortar, reducing scatter to $<5\%$ compared to idealized ellipsoidal circumscription.*

2. **Single-Particle Tensile Crushing Strength (Hiramatsu & Oka, 1966; Jaeger, 1967):**
   $$\sigma_f = \frac{0.9 F_f}{d_0^2} \implies F_f = \frac{\sigma_f \cdot d_0^2}{0.9}$$
   *Where $\sigma_f$ is in $\text{MPa}$, $F_f$ is in $\text{N}$ (or $\text{kN}$), and $d_0$ is in $\text{mm}$.*

3. **Shape-Dependent Crushing Strength Power Law (Cai et al., 2024 Eq. 8):**
   $$\sigma_{f,\text{shape}}(\Phi) = p \cdot \Phi^q$$
   *Where sphericity $\Phi = \sqrt[3]{\frac{I \cdot S}{L^2}}$. For RC: $p=9.35, q=2.13$ ($R^2 = 0.99$).*

4. **Weibull Statistical Weakest-Link Size Scaling (Weibull, 1951; Liang et al., 2025 Table 2):**
   $$P_s(\sigma) = \exp\left[ -\left(\frac{\sigma}{\sigma_{f0}}\right)^m \right], \quad \sigma_f(d_0, \Phi) = \sigma_{f,\text{shape}}(\Phi) \cdot \frac{\sigma_{f0}(d_0)}{\sigma_{f0}(d_{ref})}$$
   *Accounts for higher fatal flaw density in larger aggregate volumes.*

5. **Empirical Crushing Energy Formulation (Cai et al., 2024 Eq. 10 & 11):**
   $$E_f(d_0, \Phi) = \begin{cases} 
   c \cdot \Phi^d \cdot \left(\frac{d_0}{d_{ref}}\right)^3 & \text{for } \Phi < 0.8 \\ 
   \left[ E_0 + 2\alpha \left(1 - e^{-\Phi/t}\right) \right] \cdot \left(\frac{d_0}{d_{ref}}\right)^3 & \text{for } \Phi \ge 0.8 
   \end{cases}$$
   *Calibrated for reference size $d_{ref} \approx 25\text{ mm}$ and scaled cubically with volume. Note: This is an empirical model estimate, not a sensor-integrated force-displacement curve.*

6. **Post-Breakage Fractal Gradation (Tyler & Wheatcraft, 1992; Turcotte, 1986; Liang et al., 2025 Eq. 4):**
   $$P(d) = \frac{M(x < d)}{M_T} \times 100\% = \left(\frac{d}{d_{\max}}\right)^{3-D} \times 100\%$$
   *Where $D$ is the post-breakage fractal dimension, coupled between particle size and sphericity.*

---

### 2. Variable Definitions & Engineering Units

| Symbol | Description | SI / Engineering Units | Physical Bounds | Source / Reference |
| :--- | :--- | :--- | :--- | :--- |
| **$L, I, S$** | Longest, intermediate, and shortest particle axes | $\text{mm}$ | $L \ge I \ge S > 0$ | Vernier caliper / 3D scan |
| **$d_{eq}$** | Circumscribed spherical equivalent diameter | $\text{mm}$ | $> 0$ | Geometric definition |
| **$d_0$** | Bagheri roughness-corrected equivalent diameter | $\text{mm}$ | $0.887 \cdot d_{eq}$ | Bagheri et al. (2015); Liang et al. (2025) |
| **$EI$** | Elongation Index ($I/L$) | Dimensionless [-] | $[0.29, 0.98]$ | Zingg (1935); BS 812 |
| **$FI$** | Flatness / Flakiness Index ($S/I$) | Dimensionless [-] | $[0.30, 0.96]$ | Zingg (1935); BS 812 |
| **$\Phi$** | Sphericity ($\sqrt[3]{I \cdot S / L^2}$) | Dimensionless [-] | $[0.42, 0.93]$ | Krumbein (1941); Cai et al. (2024) |
| **$\sigma_f$** | Single-particle crushing strength | $\text{MPa}$ | $[0.5, 15.0]$ | Hiramatsu & Oka (1966) |
| **$F_f$** | Peak crushing failure force | $\text{kN}$ | $> 0$ | Derived: $\sigma_f d_0^2 / 900$ |
| **$E_f$** | Estimated single-particle crushing energy | $\text{mJ}$ | $> 1.0$ | Cai et al. (2024) empirical estimate |
| **$D$** | Post-breakage fractal dimension | Dimensionless [-] | $[1.5, 2.7]$ | Tyler & Wheatcraft (1992); Li et al. (2021) |
| **$m$** | Weibull modulus (strength uniformity) | Dimensionless [-] | $[1.1, 4.0]$ | Liang et al. (2025) Table 2 |
| **$P_s$** | Survival probability at given stress level | Dimensionless [-] | $[0.0, 1.0]$ | Weibull (1951) |

---

### 3. Geotechnical Assumptions & Physical Hypotheses

1. **Tensile Failure Dominance:** Uniaxial compression of irregular particles induces concentrated point contacts at opposing platens, generating a maximum internal tensile stress along the loading axis. Failure occurs by tensile splitting governed by the Hiramatsu-Oka coefficient ($0.9$).
2. **Roughness & Adhered Mortar Inefficiency:** Recycled aggregates possess porous residual cement paste and microcracked surface asperities that do not bear full structural load. The Bagheri coefficient ($0.887$) accounts for this inactive boundary volume.
3. **Weakest-Link Size Scaling:** According to Griffith fracture mechanics and Weibull theory, larger particles contain higher numbers of internal flaws and interfacial transition zone (ITZ) defects, lowering their nominal tensile strength ($\sigma_f \propto d^{-3/m}$).
4. **Sphericity Stress Distribution:** Spherical particles ($\Phi \to 1.0$) distribute contact stresses over wider Hertzian contact patches, suppressing premature shear spalling and raising crushing strength.
5. **Self-Similar Fragmentation:** Post-breakage fragments follow power-law scale invariance, parameterized by the fractal dimension $D$. Higher $D$ values indicate more extensive comminution and greater production of fine powder.

---

### 4. Calibration Datasets & Literature Provenance

- **Cai et al. (2024)** (*Construction and Building Materials* 439, 137363): 270 physical laboratory single-particle crushing tests of recycled aggregate (RC, RB, RM) in the $19\text{–}37.5\text{ mm}$ size fraction with sphericity $\Phi \in [0.42, 0.93]$, combined with PFC3D discrete element method (DEM) simulations.
- **Liang et al. (2025)** (*Case Studies in Construction Materials* 23, e05603): 180 single-particle crushing tests across three calibrated sieve size fractions ($4.75\text{–}10\text{ mm}$, $10\text{–}20\text{ mm}$, $20\text{–}25\text{ mm}$) for recycled concrete, brick, and mortar, providing exact Weibull characteristic strengths $\sigma_{f0}$, moduli $m$, and fractal dimensions $D$.
- **Li et al. (2021)** (*Advances in Materials Science and Engineering* 2021, 6097897): Static compression and impact crushing investigations on recycled brick and concrete aggregate, defining the benchmark optimal gradation fractal dimension range ($1.887 \le D \le 2.631$).

---

### 5. Known Model Limitations & Unvalidated Boundaries

- **Dynamic / Impact Crushing:** The model strictly assumes quasi-static loading ($0.5\text{–}1.0\text{ mm/min}$). High-strain-rate impact failure (drop-weight or Split-Hopkinson bar) involves wave propagation and inertia effects not captured here.
- **Energy Estimation:** Crushing energy is an empirical power-law estimate scaled with volume $(d_0/25)^3$, not a real-time sensor integration of the experimental force-displacement curve.
- **Extreme Size Extrapolation:** Predictions for ultra-fine aggregates ($d_0 < 4.75\text{ mm}$) or boulder-scale aggregates ($d_0 > 37.5\text{ mm}$) represent unvalidated mathematical extrapolations beyond published laboratory test bounds.
- **Heterogeneous Mortar Ratio:** In recycled concrete aggregate, the ratio of adhered mortar to virgin natural stone varies with parent concrete grade; the model uses representative empirical averages from Liang et al. and Cai et al.
        """)


# ==============================================================================
# TAB 3: Computer Vision Aggregate Scanner
# ==============================================================================
with tab3:
    st.header("Computer Vision Aggregate Scanner")
    st.markdown(
        "*Extract planar dimensions, shape indices, and crushing predictions from 2D top-down photographs of aggregates.*"
    )

    with st.expander("📸 Photo Guidelines & Image Preparation Tips (Click to expand)", expanded=True):
        st.markdown("""
        **For accurate automated contour detection and dimension extraction:**
        - **Plain, High-Contrast Background:** Place particles on a clean **white sheet of paper** or flat white tray (or black paper if aggregates are light white/calcite).
        - **Separated Aggregates:** Spread particles so they are **not touching or clustered**. Touching stones merge into a single contour.
        - **Direct 90° Overhead View (Nadir):** Hold the camera/phone directly parallel to the table. Avoid angled or perspective shots.
        - **Diffused, Even Lighting:** Use balanced overhead light to avoid hard cast shadows (which the detector could mistake for stone boundaries).
        - **Scale Calibration:** Use the **Pixel-to-mm Scale** slider below to calibrate your camera resolution (default: `1 px ≈ 0.5 mm`).
        """)

    col_cv1, col_cv2 = st.columns([1, 1])

    with col_cv1:
        uploaded_file = st.file_uploader("Upload aggregate image", type=['jpg', 'png', 'jpeg'])

        st.markdown("**Detection & Calibration Controls**")
        scale = st.slider("Pixel-to-mm Scale (mm/px)", 0.05, 2.0, 0.5, 0.05,
                          help="Calibration factor. At 0.5 mm/px, an aggregate measuring 40 pixels corresponds to 20 mm.")
        bg_mode = st.radio("Background Setup",
                           ["Dark/Colored Particles on White/Light Background", "Light Particles on Black/Dark Background"],
                           index=0)
        min_area = st.slider("Min Particle Filter Area (px²)", 100, 3000, 500, 50,
                             help="Discards camera noise, small dirt dust, and background artifacts.")

        if st.button("🎲 Generate Synthetic Test Image"):
            img = np.ones((500, 700, 3), dtype=np.uint8) * 240
            rng = np.random.default_rng(42)
            n_agg = 12
            for _ in range(n_agg):
                cx, cy = rng.integers(80, 620), rng.integers(80, 420)
                a, b = rng.integers(20, 60), rng.integers(15, 45)
                angle = rng.integers(0, 180)
                color = tuple(int(c) for c in rng.integers(80, 180, 3))
                cv2.ellipse(img, (cx, cy), (a, b), angle, 0, 360, color, -1)
                cv2.ellipse(img, (cx, cy), (a, b), angle, 0, 360, (50, 50, 50), 2)

            st.session_state['cv_image'] = img
            st.success("Synthetic image generated! See detection preview on the right.")

    with col_cv2:
        img_to_process = None

        if uploaded_file is not None:
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            img_to_process = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        elif 'cv_image' in st.session_state:
            img_to_process = st.session_state['cv_image']

        if img_to_process is not None:
            gray = cv2.cvtColor(img_to_process, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            # Adapt threshold direction based on background choice
            if bg_mode == "Dark/Colored Particles on White/Light Background":
                thresh_type = cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
            else:
                thresh_type = cv2.THRESH_BINARY + cv2.THRESH_OTSU

            _, thresh = cv2.threshold(blurred, 0, 255, thresh_type)

            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            valid_contours = [c for c in contours if cv2.contourArea(c) > min_area]

            annotated = img_to_process.copy()
            particles = []

            cv_material = st.selectbox("Material for prediction", ['RC', 'RB', 'RM'], key='cv_mat',
                                       format_func=lambda x: f"{x} - {MATERIAL_PROPS[x]['name']}")

            for i, contour in enumerate(valid_contours):
                rect = cv2.minAreaRect(contour)
                box = cv2.boxPoints(rect)
                box = np.int32(box)

                w, h = rect[1]
                L_px = max(w, h)
                I_px = min(w, h)

                L_mm = L_px * scale
                I_mm = I_px * scale
                # Stereological assumption for plan-view resting aggregate: S ≈ 0.65 * I
                S_mm = I_mm * 0.65

                if L_mm > 2 and I_mm > 1:
                    cv2.drawContours(annotated, [box], 0, (0, 255, 0), 2)
                    cv2.putText(annotated, f'#{i+1}', (int(rect[0][0]), int(rect[0][1])),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                    pred = predict_single_particle(L_mm, I_mm, S_mm, cv_material)
                    particles.append({
                        'ID': i + 1,
                        'L (mm)': round(L_mm, 1),
                        'I (mm)': round(I_mm, 1),
                        'S (mm)': round(S_mm, 1),
                        'EI': round(pred['EI'], 3),
                        'Φ': round(pred['Phi'], 3),
                        'Shape': pred['shape_class'],
                        'σ_f (MPa)': round(pred['sigma_f'], 2),
                        'F_f (kN)': round(pred['F_f_kN'], 3),
                        'E_f (mJ)': round(pred['E_f'], 1),
                        'Fractal D': round(pred['D'], 3),
                    })

            st.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB),
                     caption=f"Detected {len(particles)} valid aggregate particles",
                     use_container_width=True)

            if particles:
                st.markdown(f"**Extracted Morphological & Crushing Properties ({len(particles)} particles):**")
                st.dataframe(pd.DataFrame(particles), use_container_width=True)


# ==============================================================================
# TAB 4: Explainable AI & Model Benchmarks
# ==============================================================================
with tab4:
    st.header("Explainable AI & Model Benchmarks")

    reg_metrics_path = RESULTS_DIR / 'regression_metrics.csv'
    clf_metrics_path = RESULTS_DIR / 'classification_metrics.csv'

    col_m1, col_m2 = st.columns(2)

    with col_m1:
        st.subheader("Regression Metrics")
        if reg_metrics_path.exists():
            reg_df = pd.read_csv(reg_metrics_path)
            st.dataframe(reg_df, use_container_width=True)

            fig_bar = px.bar(reg_df, x='Target', y='R2', color='Model',
                            barmode='group', title='R² Score by Model & Target')
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("Run `src/train_models.py` first to generate metrics.")

    with col_m2:
        st.subheader("Classification Metrics")
        if clf_metrics_path.exists():
            clf_df = pd.read_csv(clf_metrics_path)
            st.dataframe(clf_df, use_container_width=True)
        else:
            st.warning("Run `src/train_models.py` first to generate metrics.")

    st.subheader("Publication Figures (300 DPI)")
    figure_files = sorted(FIGURES_DIR.glob('*.png')) if FIGURES_DIR.exists() else []

    if figure_files:
        cols = st.columns(2)
        for i, fig_path in enumerate(figure_files):
            with cols[i % 2]:
                st.image(str(fig_path), caption=fig_path.name, use_container_width=True)
    else:
        st.info("No figures found. Run the training pipeline to generate them.")
