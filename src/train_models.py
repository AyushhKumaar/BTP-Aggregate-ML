"""
Multi-Task ML & Deep Learning Training Pipeline for Recycled Aggregate Crushing.

Trains, tunes, and evaluates multiple regression and classification models:
  - Ridge / Polynomial Regression (baseline)
  - Random Forest
  - XGBoost
  - LightGBM
  - CatBoost
  - Physics-Informed MLP Neural Network

Generates publication-ready figures at 300 DPI.
"""

import warnings
warnings.filterwarnings('ignore')

import sys
from pathlib import Path

# Add project root and src directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import json
import joblib

from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.preprocessing import StandardScaler, LabelEncoder, PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.metrics import (
    r2_score, mean_squared_error, mean_absolute_error,
    accuracy_score, f1_score, roc_auc_score, confusion_matrix,
    classification_report
)
from sklearn.multioutput import MultiOutputRegressor

import xgboost as xgb
import lightgbm as lgb
import catboost as cb

# Import data generator constants
try:
    from src.data_generator import (
        MATERIAL_PROPS, SHAPE_STRENGTH_PARAMS, ENERGY_POWER_PARAMS,
        ENERGY_SATURATING_PARAMS, WEIBULL_PARAMS, FRACTAL_SIZE, FRACTAL_SHAPE,
        SIEVE_SIZES
    )
except ImportError:
    from data_generator import (
        MATERIAL_PROPS, SHAPE_STRENGTH_PARAMS, ENERGY_POWER_PARAMS,
        ENERGY_SATURATING_PARAMS, WEIBULL_PARAMS, FRACTAL_SIZE, FRACTAL_SHAPE,
        SIEVE_SIZES
    )

# Try SHAP import
try:
    import shap
    HAS_SHAP = True
except ImportError:
    HAS_SHAP = False
    print("WARNING: SHAP not available. Feature importance plots will be fallback.")

# ==============================================================================
# Configuration
# ==============================================================================

DATA_PATH = PROJECT_ROOT / 'data' / 'coupled_aggregate_breakage_dataset.csv'
RESULTS_DIR = PROJECT_ROOT / 'results'
FIGURES_DIR = RESULTS_DIR / 'figures'
MODELS_DIR = RESULTS_DIR / 'models'

# Create directories
for d in [RESULTS_DIR, FIGURES_DIR, MODELS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# DPI for publication figures
DPI = 300

# Feature columns for regression
FEATURE_COLS = [
    'L_mm', 'I_mm', 'S_mm',
    'EI', 'FI', 'Sphericity', 'Domokos_Sf',
    'd_eq_mm', 'd_bagheri_mm',
    'Apparent_Density_gcm3', 'Bulk_Density_gcm3',
    'Elastic_Modulus_GPa', 'Poisson_Ratio',
]

# Categorical feature for encoding
CAT_FEATURES = ['Material', 'Shape_Class', 'Sieve_Bracket']

# Regression targets
REG_TARGETS = ['Sigma_f_MPa', 'F_f_kN', 'E_f_mJ', 'Fractal_Dim_D']

# Classification target
CLF_TARGET = 'Breakage_Mode'

# Color palette
COLORS = {
    'RC': '#2196F3',   # Blue
    'RB': '#F44336',   # Red
    'RM': '#4CAF50',   # Green
}

MODEL_COLORS = {
    'Ridge_Poly': '#9C27B0',
    'RandomForest': '#4CAF50',
    'XGBoost': '#FF9800',
    'LightGBM': '#2196F3',
    'CatBoost': '#F44336',
    'MLP_Neural': '#607D8B',
}


def mape(y_true, y_pred):
    """Mean Absolute Percentage Error."""
    mask = y_true != 0
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100


def load_and_prepare_data():
    """Load dataset and prepare features/targets."""
    print("\n[DATA] Loading dataset...")
    df = pd.read_csv(DATA_PATH)
    print(f"  Loaded {len(df)} samples with {len(df.columns)} columns")

    # Encode categorical features
    le_material = LabelEncoder()
    le_shape = LabelEncoder()
    le_sieve = LabelEncoder()

    df['Material_Enc'] = le_material.fit_transform(df['Material'])
    df['Shape_Class_Enc'] = le_shape.fit_transform(df['Shape_Class'])
    df['Sieve_Bracket_Enc'] = le_sieve.fit_transform(df['Sieve_Bracket'])

    # All numeric features
    feature_cols = FEATURE_COLS + ['Material_Enc', 'Shape_Class_Enc', 'Sieve_Bracket_Enc']

    X = df[feature_cols].values
    y_reg = df[REG_TARGETS].values

    # Classification target
    le_mode = LabelEncoder()
    y_clf = le_mode.fit_transform(df[CLF_TARGET])

    # Train/test split
    X_train, X_test, y_reg_train, y_reg_test, y_clf_train, y_clf_test = \
        train_test_split(X, y_reg, y_clf, test_size=0.2, random_state=42, stratify=y_clf)

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return {
        'df': df,
        'X_train': X_train, 'X_test': X_test,
        'X_train_scaled': X_train_scaled, 'X_test_scaled': X_test_scaled,
        'y_reg_train': y_reg_train, 'y_reg_test': y_reg_test,
        'y_clf_train': y_clf_train, 'y_clf_test': y_clf_test,
        'scaler': scaler,
        'le_material': le_material, 'le_shape': le_shape,
        'le_sieve': le_sieve, 'le_mode': le_mode,
        'feature_cols': feature_cols,
    }


def train_regression_models(data):
    """Train all regression models and return predictions + metrics."""
    X_train = data['X_train_scaled']
    X_test = data['X_test_scaled']
    y_train = data['y_reg_train']
    y_test = data['y_reg_test']

    models = {}
    predictions = {}
    metrics = {}

    # 1. Ridge Polynomial Regression (degree=2)
    print("\n  [1/6] Training Ridge Polynomial Regression...")
    poly = PolynomialFeatures(degree=2, include_bias=False, interaction_only=False)
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.transform(X_test)

    ridge_models = {}
    ridge_preds = np.zeros_like(y_test)
    for i, target in enumerate(REG_TARGETS):
        ridge = Ridge(alpha=1.0)
        ridge.fit(X_train_poly, y_train[:, i])
        ridge_preds[:, i] = ridge.predict(X_test_poly)
        ridge_models[target] = ridge

    models['Ridge_Poly'] = {'models': ridge_models, 'poly': poly}
    predictions['Ridge_Poly'] = ridge_preds

    # 2. Random Forest
    print("  [2/6] Training Random Forest Regressor...")
    rf_models = {}
    rf_preds = np.zeros_like(y_test)
    for i, target in enumerate(REG_TARGETS):
        rf = RandomForestRegressor(
            n_estimators=200, max_depth=15, min_samples_split=5,
            min_samples_leaf=2, random_state=42, n_jobs=-1
        )
        rf.fit(X_train, y_train[:, i])
        rf_preds[:, i] = rf.predict(X_test)
        rf_models[target] = rf

    models['RandomForest'] = rf_models
    predictions['RandomForest'] = rf_preds

    # 3. XGBoost
    print("  [3/6] Training XGBoost Regressor...")
    xgb_models = {}
    xgb_preds = np.zeros_like(y_test)
    for i, target in enumerate(REG_TARGETS):
        xgb_model = xgb.XGBRegressor(
            n_estimators=300, max_depth=8, learning_rate=0.05,
            subsample=0.8, colsample_bytree=0.8,
            reg_alpha=0.1, reg_lambda=1.0,
            random_state=42, n_jobs=-1, verbosity=0
        )
        xgb_model.fit(X_train, y_train[:, i])
        xgb_preds[:, i] = xgb_model.predict(X_test)
        xgb_models[target] = xgb_model

    models['XGBoost'] = xgb_models
    predictions['XGBoost'] = xgb_preds

    # 4. LightGBM
    print("  [4/6] Training LightGBM Regressor...")
    lgb_models = {}
    lgb_preds = np.zeros_like(y_test)
    for i, target in enumerate(REG_TARGETS):
        lgb_model = lgb.LGBMRegressor(
            n_estimators=300, max_depth=8, learning_rate=0.05,
            subsample=0.8, colsample_bytree=0.8,
            reg_alpha=0.1, reg_lambda=1.0,
            random_state=42, n_jobs=-1, verbose=-1
        )
        lgb_model.fit(X_train, y_train[:, i])
        lgb_preds[:, i] = lgb_model.predict(X_test)
        lgb_models[target] = lgb_model

    models['LightGBM'] = lgb_models
    predictions['LightGBM'] = lgb_preds

    # 5. CatBoost
    print("  [5/6] Training CatBoost Regressor...")
    cat_models = {}
    cat_preds = np.zeros_like(y_test)
    for i, target in enumerate(REG_TARGETS):
        cat_model = cb.CatBoostRegressor(
            iterations=300, depth=8, learning_rate=0.05,
            l2_leaf_reg=3.0, random_seed=42, verbose=0
        )
        cat_model.fit(X_train, y_train[:, i])
        cat_preds[:, i] = cat_model.predict(X_test)
        cat_models[target] = cat_model

    models['CatBoost'] = cat_models
    predictions['CatBoost'] = cat_preds

    # 6. MLP Neural Network (Physics-Informed via feature engineering)
    print("  [6/6] Training MLP Neural Network...")
    mlp_models = {}
    mlp_preds = np.zeros_like(y_test)
    for i, target in enumerate(REG_TARGETS):
        mlp = MLPRegressor(
            hidden_layer_sizes=(128, 64, 32),
            activation='relu', solver='adam',
            alpha=0.001, learning_rate='adaptive',
            learning_rate_init=0.001,
            max_iter=500, random_state=42,
            early_stopping=True, validation_fraction=0.1,
            n_iter_no_change=20, batch_size=64,
        )
        mlp.fit(X_train, y_train[:, i])
        mlp_preds[:, i] = mlp.predict(X_test)
        mlp_models[target] = mlp

    models['MLP_Neural'] = mlp_models
    predictions['MLP_Neural'] = mlp_preds

    # Compute metrics for all models
    print("\n  Computing metrics...")
    for model_name, preds in predictions.items():
        metrics[model_name] = {}
        for i, target in enumerate(REG_TARGETS):
            r2 = r2_score(y_test[:, i], preds[:, i])
            rmse = np.sqrt(mean_squared_error(y_test[:, i], preds[:, i]))
            mae = mean_absolute_error(y_test[:, i], preds[:, i])
            mape_val = mape(y_test[:, i], preds[:, i])
            metrics[model_name][target] = {
                'R2': round(float(r2), 4),
                'RMSE': round(float(rmse), 4),
                'MAE': round(float(mae), 4),
                'MAPE': round(float(mape_val), 2),
            }

    return models, predictions, metrics


def train_classification_models(data):
    """Train classification models for breakage mode prediction."""
    X_train = data['X_train_scaled']
    X_test = data['X_test_scaled']
    y_train = data['y_clf_train']
    y_test = data['y_clf_test']

    clf_models = {}
    clf_predictions = {}
    clf_metrics = {}

    # 1. Random Forest Classifier
    print("\n  [CLF 1/3] Training Random Forest Classifier...")
    rf_clf = RandomForestClassifier(
        n_estimators=200, max_depth=15, min_samples_split=5,
        random_state=42, n_jobs=-1
    )
    rf_clf.fit(X_train, y_train)
    rf_pred = rf_clf.predict(X_test)
    rf_proba = rf_clf.predict_proba(X_test)
    clf_models['RandomForest'] = rf_clf
    clf_predictions['RandomForest'] = {'pred': rf_pred, 'proba': rf_proba}

    # 2. XGBoost Classifier
    print("  [CLF 2/3] Training XGBoost Classifier...")
    xgb_clf = xgb.XGBClassifier(
        n_estimators=300, max_depth=8, learning_rate=0.05,
        random_state=42, n_jobs=-1, verbosity=0,
        eval_metric='mlogloss'
    )
    xgb_clf.fit(X_train, y_train)
    xgb_pred = xgb_clf.predict(X_test)
    xgb_proba = xgb_clf.predict_proba(X_test)
    clf_models['XGBoost'] = xgb_clf
    clf_predictions['XGBoost'] = {'pred': xgb_pred, 'proba': xgb_proba}

    # 3. MLP Classifier
    print("  [CLF 3/3] Training MLP Classifier...")
    mlp_clf = MLPClassifier(
        hidden_layer_sizes=(128, 64, 32),
        activation='relu', solver='adam',
        alpha=0.001, max_iter=500,
        random_state=42, early_stopping=True
    )
    mlp_clf.fit(X_train, y_train)
    mlp_pred = mlp_clf.predict(X_test)
    mlp_proba = mlp_clf.predict_proba(X_test)
    clf_models['MLP'] = mlp_clf
    clf_predictions['MLP'] = {'pred': mlp_pred, 'proba': mlp_proba}

    # Compute metrics
    n_classes = len(np.unique(y_test))
    for model_name, preds_dict in clf_predictions.items():
        pred = preds_dict['pred']
        proba = preds_dict['proba']
        acc = accuracy_score(y_test, pred)
        f1 = f1_score(y_test, pred, average='macro')
        try:
            if n_classes == 2:
                auc = roc_auc_score(y_test, proba[:, 1])
            else:
                auc = roc_auc_score(y_test, proba, multi_class='ovr', average='macro')
        except ValueError:
            auc = 0.0
        clf_metrics[model_name] = {
            'Accuracy': round(float(acc), 4),
            'Macro_F1': round(float(f1), 4),
            'ROC_AUC': round(float(auc), 4),
        }

    return clf_models, clf_predictions, clf_metrics


# ==============================================================================
# FIGURE GENERATION
# ==============================================================================

def fig1_zingg_classification(df):
    """Fig 1: Zingg shape classification scatter plot."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=True)
    shape_markers = {'Disk': 's', 'Block': 'o', 'Blade': '^', 'Bar': 'D'}
    shape_colors = {'Disk': '#FF6B6B', 'Block': '#4ECDC4', 'Blade': '#45B7D1', 'Bar': '#FFA07A'}

    for idx, material in enumerate(['RC', 'RB', 'RM']):
        ax = axes[idx]
        subset = df[df['Material'] == material]
        for shape_cls in ['Disk', 'Block', 'Blade', 'Bar']:
            mask = subset['Shape_Class'] == shape_cls
            ax.scatter(
                subset.loc[mask, 'EI'], subset.loc[mask, 'FI'],
                marker=shape_markers[shape_cls], c=shape_colors[shape_cls],
                label=shape_cls, alpha=0.5, s=20, edgecolors='none'
            )
        # Add classification boundaries
        ax.axhline(y=0.67, color='gray', linestyle='--', linewidth=1, alpha=0.7)
        ax.axvline(x=0.67, color='gray', linestyle='--', linewidth=1, alpha=0.7)
        ax.set_xlabel('Elongation Index (I/L)', fontsize=12)
        if idx == 0:
            ax.set_ylabel('Flatness Index (S/I)', fontsize=12)
        ax.set_title(f'{material}', fontsize=13, fontweight='bold')
        ax.set_xlim(0.25, 1.0)
        ax.set_ylim(0.25, 1.0)
        ax.legend(loc='upper left', fontsize=9)
        ax.grid(True, alpha=0.3)

        # Add quadrant labels
        ax.text(0.45, 0.82, 'Disk', fontsize=9, ha='center', color='gray', style='italic')
        ax.text(0.83, 0.82, 'Block', fontsize=9, ha='center', color='gray', style='italic')
        ax.text(0.45, 0.45, 'Blade', fontsize=9, ha='center', color='gray', style='italic')
        ax.text(0.83, 0.45, 'Bar', fontsize=9, ha='center', color='gray', style='italic')

    fig.suptitle('Zingg Shape Classification of Recycled Aggregates', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / 'fig1_zingg_shape_classification.png', dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print("  [OK] fig1_zingg_shape_classification.png")


def fig2_weibull_survival(df):
    """Fig 2: Weibull survival curves."""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    line_styles = {'4.75-9.5': '-', '9.5-19': '--', '19-37.5': '-.'}

    for idx, material in enumerate(['RC', 'RB', 'RM']):
        subset = df[df['Material'] == material]

        # Top row: Ps vs sigma_f
        ax1 = axes[0, idx]
        for bracket in ['4.75-9.5', '9.5-19', '19-37.5']:
            bracket_data = subset[subset['Sieve_Bracket'] == bracket]['Sigma_f_MPa'].sort_values()
            n = len(bracket_data)
            ps = np.arange(n, 0, -1) / (n + 1)  # Survival probability
            ax1.plot(bracket_data, ps, line_styles[bracket],
                     color=COLORS[material], label=bracket + ' mm', linewidth=1.5)
        ax1.set_xlabel(r'$\sigma_f$ (MPa)', fontsize=11)
        ax1.set_ylabel(r'Survival Probability $P_s$', fontsize=11)
        ax1.set_title(f'{material}', fontsize=12, fontweight='bold')
        ax1.legend(fontsize=9)
        ax1.grid(True, alpha=0.3)

        # Bottom row: ln(ln(1/Ps)) vs ln(sigma_f) - Weibull plot
        ax2 = axes[1, idx]
        for bracket in ['4.75-9.5', '9.5-19', '19-37.5']:
            bracket_data = subset[subset['Sieve_Bracket'] == bracket]['Sigma_f_MPa'].sort_values()
            n = len(bracket_data)
            ps = np.arange(n, 0, -1) / (n + 1)
            valid = (ps > 0.01) & (ps < 0.99) & (bracket_data > 0)
            ln_sigma = np.log(bracket_data[valid])
            ln_ln_inv_ps = np.log(np.log(1.0 / ps[valid]))
            ax2.plot(ln_sigma, ln_ln_inv_ps, line_styles[bracket],
                     color=COLORS[material], label=bracket + ' mm', linewidth=1.5)
        ax2.set_xlabel(r'$\ln(\sigma_f)$', fontsize=11)
        ax2.set_ylabel(r'$\ln(\ln(1/P_s))$', fontsize=11)
        ax2.set_title(f'{material} - Weibull Plot', fontsize=12, fontweight='bold')
        ax2.legend(fontsize=9)
        ax2.grid(True, alpha=0.3)

    fig.suptitle('Weibull Survival Analysis of Single-Particle Crushing Strength',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / 'fig2_weibull_survival_curves.png', dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print("  [OK] fig2_weibull_survival_curves.png")


def fig3_strength_energy_sphericity(df):
    """Fig 3: Crushing strength and energy vs sphericity."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

    # Left: Strength vs Sphericity
    ax1 = axes[0]
    for material in ['RC', 'RB', 'RM']:
        subset = df[df['Material'] == material]
        ax1.scatter(subset['Sphericity'], subset['Sigma_f_MPa'],
                    c=COLORS[material], label=material, alpha=0.3, s=10, edgecolors='none')
        # Fit curve
        phi_range = np.linspace(0.42, 0.93, 100)
        params = SHAPE_STRENGTH_PARAMS[material]
        sigma_fit = params['p'] * phi_range ** params['q']
        ax1.plot(phi_range, sigma_fit, color=COLORS[material], linewidth=2,
                 label=f'{material}: p={params["p"]}, q={params["q"]}')

    ax1.set_xlabel(r'Sphericity ($\Phi$)', fontsize=12)
    ax1.set_ylabel(r'Crushing Strength $\sigma_f$ (MPa)', fontsize=12)
    ax1.set_title(r'Crushing Strength vs Sphericity ($\Phi$)', fontsize=13, fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Right: Energy vs Sphericity
    ax2 = axes[1]
    for material in ['RC', 'RB', 'RM']:
        subset = df[df['Material'] == material]
        ax2.scatter(subset['Sphericity'], subset['E_f_mJ'],
                    c=COLORS[material], label=material, alpha=0.3, s=10, edgecolors='none')

    ax2.set_xlabel(r'Sphericity ($\Phi$)', fontsize=12)
    ax2.set_ylabel(r'Crushing Energy $E_f$ (mJ)', fontsize=12)
    ax2.set_title(r'Crushing Energy vs Sphericity ($\Phi$)', fontsize=13, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    fig.savefig(FIGURES_DIR / 'fig3_strength_energy_vs_sphericity.png', dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print("  [OK] fig3_strength_energy_vs_sphericity.png")


def fig4_fractal_gradation(df):
    """Fig 4: Post-crushing fractal gradation curves."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    sieve_cols = [c for c in df.columns if c.startswith('Pass_')]
    sieve_vals = [float(c.replace('Pass_', '').replace('mm', '')) for c in sieve_cols]

    for idx, material in enumerate(['RC', 'RB', 'RM']):
        ax = axes[idx]
        subset = df[df['Material'] == material]

        for bracket in ['4.75-9.5', '9.5-19', '19-37.5']:
            bracket_data = subset[subset['Sieve_Bracket'] == bracket]
            mean_passing = bracket_data[sieve_cols].mean()
            ax.semilogx(sieve_vals, mean_passing.values, 'o-',
                        label=bracket + ' mm', linewidth=1.5, markersize=4)

        ax.set_xlabel('Sieve Size (mm)', fontsize=11)
        if idx == 0:
            ax.set_ylabel('Percentage Passing (%)', fontsize=11)
        ax.set_title(f'{material}', fontsize=12, fontweight='bold')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3, which='both')
        ax.set_ylim(0, 105)

    fig.suptitle('Post-Crushing Fractal Gradation Curves', fontsize=14, fontweight='bold')
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / 'fig4_fractal_gradation_curves.png', dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print("  [OK] fig4_fractal_gradation_curves.png")


def fig5_model_comparison(reg_metrics):
    """Fig 5: Model comparison bar charts (R2, RMSE, MAE, MAPE)."""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    metric_names = ['R2', 'RMSE', 'MAE', 'MAPE']
    metric_labels = ['R2 Score', 'RMSE', 'MAE', 'MAPE (%)']

    model_names = list(reg_metrics.keys())
    x = np.arange(len(REG_TARGETS))
    width = 0.12

    for m_idx, (metric_name, metric_label) in enumerate(zip(metric_names, metric_labels)):
        ax = axes[m_idx // 2, m_idx % 2]
        for i, model_name in enumerate(model_names):
            vals = [reg_metrics[model_name][t][metric_name] for t in REG_TARGETS]
            offset = (i - len(model_names)/2 + 0.5) * width
            bars = ax.bar(x + offset, vals, width, label=model_name,
                          color=MODEL_COLORS.get(model_name, '#999999'), alpha=0.85)

        ax.set_xlabel('Target Variable', fontsize=11)
        ax.set_ylabel(metric_label, fontsize=11)
        ax.set_title(metric_label, fontsize=12, fontweight='bold')
        ax.set_xticks(x)
        target_labels = [r'$\sigma_f$ (MPa)', r'$F_f$ (kN)', r'$E_f$ (mJ)', r'$D$']
        ax.set_xticklabels(target_labels, fontsize=10)
        ax.legend(fontsize=8, loc='best')
        ax.grid(True, alpha=0.3, axis='y')

    fig.suptitle('Model Performance Comparison Across Target Variables',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / 'fig5_model_comparison_metrics.png', dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print("  [OK] fig5_model_comparison_metrics.png")


def fig6_parity_plots(y_test, predictions, best_model_name='XGBoost'):
    """Fig 6: Actual vs Predicted parity plots."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    preds = predictions[best_model_name]

    target_labels = [r'$\sigma_f$ (MPa)', r'$F_f$ (kN)', r'$E_f$ (mJ)', r'Fractal Dim $D$']

    for i, (target, label) in enumerate(zip(REG_TARGETS, target_labels)):
        ax = axes[i // 2, i % 2]
        y_true = y_test[:, i]
        y_pred = preds[:, i]

        ax.scatter(y_true, y_pred, alpha=0.4, s=15, c='#2196F3', edgecolors='none')

        # Perfect prediction line
        lims = [min(y_true.min(), y_pred.min()), max(y_true.max(), y_pred.max())]
        margin = (lims[1] - lims[0]) * 0.05
        lims = [lims[0] - margin, lims[1] + margin]
        ax.plot(lims, lims, 'k-', linewidth=1.5, label='Perfect Prediction')

        # +/-10% error bands
        ax.plot(lims, [l * 1.1 for l in lims], 'r--', linewidth=1, alpha=0.7, label='+/-10% Error')
        ax.plot(lims, [l * 0.9 for l in lims], 'r--', linewidth=1, alpha=0.7)

        # Fill the error band
        ax.fill_between(lims, [l * 0.9 for l in lims], [l * 1.1 for l in lims],
                        alpha=0.1, color='red')

        r2 = r2_score(y_true, y_pred)
        ax.text(0.05, 0.92, f'R2 = {r2:.4f}', transform=ax.transAxes,
                fontsize=11, fontweight='bold', 
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

        ax.set_xlabel(f'Actual {label}', fontsize=11)
        ax.set_ylabel(f'Predicted {label}', fontsize=11)
        ax.set_title(f'{label} - {best_model_name}', fontsize=12, fontweight='bold')
        ax.legend(fontsize=9, loc='lower right')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(lims)
        ax.set_ylim(lims)

    plt.tight_layout()
    fig.savefig(FIGURES_DIR / 'fig6_actual_vs_predicted_parity.png', dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print("  [OK] fig6_actual_vs_predicted_parity.png")


def fig7_confusion_matrix(y_test, clf_predictions, le_mode, best_clf='XGBoost'):
    """Fig 7: Breakage mode confusion matrix."""
    pred = clf_predictions[best_clf]['pred']
    cm = confusion_matrix(y_test, pred)
    class_names = le_mode.classes_
    short_names = [n.replace('Mode_', 'M').replace('_', '\n')[:25] for n in class_names]

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=short_names, yticklabels=short_names, ax=ax)
    ax.set_xlabel('Predicted', fontsize=12)
    ax.set_ylabel('Actual', fontsize=12)
    ax.set_title(f'Breakage Mode Confusion Matrix ({best_clf})', fontsize=13, fontweight='bold')
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / 'fig7_breakage_mode_confusion_matrix.png', dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print("  [OK] fig7_breakage_mode_confusion_matrix.png")


def fig8_shap_importance(data, models, best_model_name='XGBoost'):
    """Fig 8: SHAP feature importance plots."""
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))
    feature_names = data['feature_cols']

    for i, target in enumerate(REG_TARGETS):
        ax = axes[i // 2, i % 2]
        model = models[best_model_name][target]

        plotted = False
        if HAS_SHAP:
            try:
                explainer = shap.TreeExplainer(model)
                shap_values = explainer.shap_values(data['X_test_scaled'][:200])
                if hasattr(shap_values, 'values'):
                    vals = shap_values.values
                else:
                    vals = np.array(shap_values)
                mean_shap = np.abs(vals).mean(axis=0)
                sorted_idx = np.argsort(mean_shap)[-12:]
                ax.barh(range(len(sorted_idx)), mean_shap[sorted_idx], color='#FF6B6B')
                ax.set_yticks(range(len(sorted_idx)))
                ax.set_yticklabels([feature_names[j] for j in sorted_idx], fontsize=9)
                ax.set_title(f'{target} - Mean |SHAP Value|', fontsize=11, fontweight='bold')
                ax.grid(True, alpha=0.3, axis='x')
                plotted = True
            except Exception as e:
                plotted = False

        if not plotted:
            # Fallback to model feature importances
            if hasattr(model, 'feature_importances_'):
                importances = model.feature_importances_
                sorted_idx = np.argsort(importances)[-12:]
                ax.barh(range(len(sorted_idx)), importances[sorted_idx], color='#2196F3')
                ax.set_yticks(range(len(sorted_idx)))
                ax.set_yticklabels([feature_names[j] for j in sorted_idx], fontsize=9)
                ax.set_title(f'{target} - Feature Importance', fontsize=11, fontweight='bold')
                ax.grid(True, alpha=0.3, axis='x')
            else:
                ax.text(0.5, 0.5, 'Feature Importance Not Available',
                        transform=ax.transAxes, ha='center', va='center')

    fig.suptitle(f'Feature Importance Attribution ({best_model_name})', fontsize=14, fontweight='bold')
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / 'fig8_shap_feature_importance.png', dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print("  [OK] fig8_shap_feature_importance.png")


def fig9_partial_dependence(df, models, data, best_model_name='XGBoost'):
    """Fig 9: 2D partial dependence contour heatmaps."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    feature_names = data['feature_cols']

    phi_idx = feature_names.index('Sphericity')
    d_idx = feature_names.index('d_bagheri_mm')

    phi_range = np.linspace(0.42, 0.93, 40)
    d_range = np.linspace(4.0, 35.0, 40)
    Phi_grid, D_grid = np.meshgrid(phi_range, d_range)

    X_median = np.median(data['X_train'], axis=0)

    targets_to_plot = [
        ('Sigma_f_MPa', r'$\sigma_f$ (MPa)'),
        ('Fractal_Dim_D', r'Fractal Dim $D$'),
        ('F_f_kN', r'$F_f$ (kN)'),
        ('E_f_mJ', r'$E_f$ (mJ)')
    ]

    scaler = data['scaler']

    for plot_idx, (target, label) in enumerate(targets_to_plot):
        ax = axes[plot_idx // 2, plot_idx % 2]
        model = models[best_model_name][target]

        # Vectorized batch prediction
        n_pts = len(phi_range) * len(d_range)
        grid_samples = np.repeat(X_median.reshape(1, -1), n_pts, axis=0)
        for i_p, phi in enumerate(phi_range):
            for i_d, d_val in enumerate(d_range):
                row_idx = i_d * len(phi_range) + i_p
                grid_samples[row_idx, phi_idx] = phi
                grid_samples[row_idx, d_idx] = d_val

        grid_samples_scaled = scaler.transform(grid_samples)
        preds = model.predict(grid_samples_scaled)
        Z = preds.reshape(len(d_range), len(phi_range))

        contour = ax.contourf(Phi_grid, D_grid, Z, levels=20, cmap='RdYlBu_r')
        cbar = fig.colorbar(contour, ax=ax)
        cbar.set_label(label, fontsize=10)
        ax.set_xlabel(r'Sphericity ($\Phi$)', fontsize=11)
        ax.set_ylabel(r'Particle Size $d_0$ (mm)', fontsize=11)
        ax.set_title(f'Partial Dependence: {label}', fontsize=12, fontweight='bold')

    plt.tight_layout()
    fig.savefig(FIGURES_DIR / 'fig9_partial_dependence_contours.png', dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print("  [OK] fig9_partial_dependence_contours.png")


def save_metrics(reg_metrics, clf_metrics):
    """Save all metrics to CSV and JSON."""
    rows = []
    for model_name, targets in reg_metrics.items():
        for target, metrics in targets.items():
            rows.append({
                'Model': model_name,
                'Target': target,
                **metrics
            })
    reg_df = pd.DataFrame(rows)
    reg_df.to_csv(RESULTS_DIR / 'regression_metrics.csv', index=False)

    clf_df = pd.DataFrame([
        {'Model': model_name, **metrics}
        for model_name, metrics in clf_metrics.items()
    ])
    clf_df.to_csv(RESULTS_DIR / 'classification_metrics.csv', index=False)

    summary = {
        'regression': reg_metrics,
        'classification': clf_metrics,
    }
    with open(RESULTS_DIR / 'metrics_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\n  [OK] Saved metrics to {RESULTS_DIR}")
    return reg_df, clf_df


def save_models(models, clf_models, data):
    """Save trained models and scaler."""
    joblib.dump(data['scaler'], MODELS_DIR / 'scaler.pkl')
    joblib.dump(data['le_material'], MODELS_DIR / 'le_material.pkl')
    joblib.dump(data['le_shape'], MODELS_DIR / 'le_shape.pkl')
    joblib.dump(data['le_sieve'], MODELS_DIR / 'le_sieve.pkl')
    joblib.dump(data['le_mode'], MODELS_DIR / 'le_mode.pkl')

    # Save XGBoost regression models
    for target, model in models['XGBoost'].items():
        joblib.dump(model, MODELS_DIR / f'xgb_reg_{target}.pkl')

    # Save CatBoost regression models
    for target, model in models['CatBoost'].items():
        joblib.dump(model, MODELS_DIR / f'cat_reg_{target}.pkl')

    # Save best classification model
    joblib.dump(clf_models['XGBoost'], MODELS_DIR / 'xgb_clf_breakage_mode.pkl')

    # Save Random Forest regression models
    for target, model in models['RandomForest'].items():
        joblib.dump(model, MODELS_DIR / f'rf_reg_{target}.pkl')

    print(f"  [OK] Saved models to {MODELS_DIR}")


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    print("=" * 70)
    print("MULTI-TASK ML TRAINING PIPELINE")
    print("Physics-Informed Aggregate Crushing Prediction")
    print("=" * 70)

    # Load data
    data = load_and_prepare_data()

    # Train regression models
    print("\n" + "=" * 50)
    print("REGRESSION TRAINING")
    print("=" * 50)
    reg_models, reg_predictions, reg_metrics = train_regression_models(data)

    # Print regression metrics summary
    print("\n" + "-" * 50)
    print("REGRESSION METRICS SUMMARY")
    print("-" * 50)
    for model_name, targets in reg_metrics.items():
        print(f"\n  {model_name}:")
        for target, m in targets.items():
            print(f"    {target}: R2={m['R2']:.4f}, RMSE={m['RMSE']:.4f}, "
                  f"MAE={m['MAE']:.4f}, MAPE={m['MAPE']:.1f}%")

    # Train classification models
    print("\n" + "=" * 50)
    print("CLASSIFICATION TRAINING")
    print("=" * 50)
    clf_models, clf_predictions, clf_metrics = train_classification_models(data)

    print("\n" + "-" * 50)
    print("CLASSIFICATION METRICS SUMMARY")
    print("-" * 50)
    for model_name, m in clf_metrics.items():
        print(f"  {model_name}: Acc={m['Accuracy']:.4f}, "
              f"F1={m['Macro_F1']:.4f}, AUC={m['ROC_AUC']:.4f}")

    # Generate figures
    print("\n" + "=" * 50)
    print("GENERATING PUBLICATION FIGURES (300 DPI)")
    print("=" * 50)

    df = data['df']
    fig1_zingg_classification(df)
    fig2_weibull_survival(df)
    fig3_strength_energy_sphericity(df)
    fig4_fractal_gradation(df)
    fig5_model_comparison(reg_metrics)
    fig6_parity_plots(data['y_reg_test'], reg_predictions, best_model_name='XGBoost')
    fig7_confusion_matrix(data['y_clf_test'], clf_predictions, data['le_mode'], best_clf='XGBoost')
    fig8_shap_importance(data, reg_models, best_model_name='XGBoost')
    fig9_partial_dependence(df, reg_models, data, best_model_name='XGBoost')

    # Save metrics and models
    print("\n" + "=" * 50)
    print("SAVING RESULTS")
    print("=" * 50)
    reg_df, clf_df = save_metrics(reg_metrics, clf_metrics)
    save_models(reg_models, clf_models, data)

    # Final report
    print("\n" + "=" * 70)
    print("TRAINING PIPELINE COMPLETE")
    print("=" * 70)

    best_r2 = {}
    for model_name, targets in reg_metrics.items():
        avg_r2 = np.mean([targets[t]['R2'] for t in REG_TARGETS])
        best_r2[model_name] = avg_r2
    best_model = max(best_r2, key=best_r2.get)
    print(f"\n  Best Regression Model (avg R2): {best_model} = {best_r2[best_model]:.4f}")
    print(f"  All R2 scores > 0.92: {all(v > 0.92 for v in best_r2.values())}")

    return reg_metrics, clf_metrics, reg_models, clf_models


if __name__ == '__main__':
    main()
