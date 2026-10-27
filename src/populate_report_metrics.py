"""
Populate actual training metrics into docs/BTP_Final_Report.md
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
report_path = PROJECT_ROOT / 'docs' / 'BTP_Final_Report.md'
text = report_path.read_text(encoding='utf-8')

with open(PROJECT_ROOT / 'results' / 'metrics_summary.json', 'r') as f:
    metrics = json.load(f)

reg = metrics['regression']
clf = metrics['classification']

replacements = {
    # XGBoost
    '[R2_XGBOOST_SIGMA]': f"{reg['XGBoost']['Sigma_f_MPa']['R2']:.4f}",
    '[RMSE_XGBOOST_SIGMA]': f"{reg['XGBoost']['Sigma_f_MPa']['RMSE']:.4f}",
    '[MAE_XGBOOST_SIGMA]': f"{reg['XGBoost']['Sigma_f_MPa']['MAE']:.4f}",
    '[MAPE_XGBOOST_SIGMA]': f"{reg['XGBoost']['Sigma_f_MPa']['MAPE']:.2f}%",

    '[R2_XGBOOST_FF]': f"{reg['XGBoost']['F_f_kN']['R2']:.4f}",
    '[RMSE_XGBOOST_FF]': f"{reg['XGBoost']['F_f_kN']['RMSE']:.4f}",
    '[MAE_XGBOOST_FF]': f"{reg['XGBoost']['F_f_kN']['MAE']:.4f}",
    '[MAPE_XGBOOST_FF]': f"{reg['XGBoost']['F_f_kN']['MAPE']:.2f}%",

    '[R2_XGBOOST_EF]': f"{reg['XGBoost']['E_f_mJ']['R2']:.4f}",
    '[RMSE_XGBOOST_EF]': f"{reg['XGBoost']['E_f_mJ']['RMSE']:.4f}",
    '[MAE_XGBOOST_EF]': f"{reg['XGBoost']['E_f_mJ']['MAE']:.4f}",
    '[MAPE_XGBOOST_EF]': f"{reg['XGBoost']['E_f_mJ']['MAPE']:.2f}%",

    '[R2_XGBOOST_D]': f"{reg['XGBoost']['Fractal_Dim_D']['R2']:.4f}",
    '[RMSE_XGBOOST_D]': f"{reg['XGBoost']['Fractal_Dim_D']['RMSE']:.4f}",
    '[MAE_XGBOOST_D]': f"{reg['XGBoost']['Fractal_Dim_D']['MAE']:.4f}",
    '[MAPE_XGBOOST_D]': f"{reg['XGBoost']['Fractal_Dim_D']['MAPE']:.2f}%",

    # Random Forest
    '[R2_RF_SIGMA]': f"{reg['RandomForest']['Sigma_f_MPa']['R2']:.4f}",
    '[RMSE_RF_SIGMA]': f"{reg['RandomForest']['Sigma_f_MPa']['RMSE']:.4f}",
    '[MAE_RF_SIGMA]': f"{reg['RandomForest']['Sigma_f_MPa']['MAE']:.4f}",
    '[MAPE_RF_SIGMA]': f"{reg['RandomForest']['Sigma_f_MPa']['MAPE']:.2f}%",

    '[R2_RF_FF]': f"{reg['RandomForest']['F_f_kN']['R2']:.4f}",
    '[RMSE_RF_FF]': f"{reg['RandomForest']['F_f_kN']['RMSE']:.4f}",
    '[MAE_RF_FF]': f"{reg['RandomForest']['F_f_kN']['MAE']:.4f}",
    '[MAPE_RF_FF]': f"{reg['RandomForest']['F_f_kN']['MAPE']:.2f}%",

    '[R2_RF_EF]': f"{reg['RandomForest']['E_f_mJ']['R2']:.4f}",
    '[RMSE_RF_EF]': f"{reg['RandomForest']['E_f_mJ']['RMSE']:.4f}",
    '[MAE_RF_EF]': f"{reg['RandomForest']['E_f_mJ']['MAE']:.4f}",
    '[MAPE_RF_EF]': f"{reg['RandomForest']['E_f_mJ']['MAPE']:.2f}%",

    '[R2_RF_D]': f"{reg['RandomForest']['Fractal_Dim_D']['R2']:.4f}",
    '[RMSE_RF_D]': f"{reg['RandomForest']['Fractal_Dim_D']['RMSE']:.4f}",
    '[MAE_RF_D]': f"{reg['RandomForest']['Fractal_Dim_D']['MAE']:.4f}",
    '[MAPE_RF_D]': f"{reg['RandomForest']['Fractal_Dim_D']['MAPE']:.2f}%",

    # LightGBM
    '[R2_LGBM_SIGMA]': f"{reg['LightGBM']['Sigma_f_MPa']['R2']:.4f}",
    '[RMSE_LGBM_SIGMA]': f"{reg['LightGBM']['Sigma_f_MPa']['RMSE']:.4f}",
    '[MAE_LGBM_SIGMA]': f"{reg['LightGBM']['Sigma_f_MPa']['MAE']:.4f}",
    '[MAPE_LGBM_SIGMA]': f"{reg['LightGBM']['Sigma_f_MPa']['MAPE']:.2f}%",

    '[R2_LGBM_FF]': f"{reg['LightGBM']['F_f_kN']['R2']:.4f}",
    '[RMSE_LGBM_FF]': f"{reg['LightGBM']['F_f_kN']['RMSE']:.4f}",
    '[MAE_LGBM_FF]': f"{reg['LightGBM']['F_f_kN']['MAE']:.4f}",
    '[MAPE_LGBM_FF]': f"{reg['LightGBM']['F_f_kN']['MAPE']:.2f}%",

    '[R2_LGBM_EF]': f"{reg['LightGBM']['E_f_mJ']['R2']:.4f}",
    '[RMSE_LGBM_EF]': f"{reg['LightGBM']['E_f_mJ']['RMSE']:.4f}",
    '[MAE_LGBM_EF]': f"{reg['LightGBM']['E_f_mJ']['MAE']:.4f}",
    '[MAPE_LGBM_EF]': f"{reg['LightGBM']['E_f_mJ']['MAPE']:.2f}%",

    '[R2_LGBM_D]': f"{reg['LightGBM']['Fractal_Dim_D']['R2']:.4f}",
    '[RMSE_LGBM_D]': f"{reg['LightGBM']['Fractal_Dim_D']['RMSE']:.4f}",
    '[MAE_LGBM_D]': f"{reg['LightGBM']['Fractal_Dim_D']['MAE']:.4f}",
    '[MAPE_LGBM_D]': f"{reg['LightGBM']['Fractal_Dim_D']['MAPE']:.2f}%",

    # CatBoost
    '[R2_CATBOOST_SIGMA]': f"{reg['CatBoost']['Sigma_f_MPa']['R2']:.4f}",
    '[RMSE_CATBOOST_SIGMA]': f"{reg['CatBoost']['Sigma_f_MPa']['RMSE']:.4f}",
    '[MAE_CATBOOST_SIGMA]': f"{reg['CatBoost']['Sigma_f_MPa']['MAE']:.4f}",
    '[MAPE_CATBOOST_SIGMA]': f"{reg['CatBoost']['Sigma_f_MPa']['MAPE']:.2f}%",

    '[R2_CATBOOST_FF]': f"{reg['CatBoost']['F_f_kN']['R2']:.4f}",
    '[RMSE_CATBOOST_FF]': f"{reg['CatBoost']['F_f_kN']['RMSE']:.4f}",
    '[MAE_CATBOOST_FF]': f"{reg['CatBoost']['F_f_kN']['MAE']:.4f}",
    '[MAPE_CATBOOST_FF]': f"{reg['CatBoost']['F_f_kN']['MAPE']:.2f}%",

    '[R2_CATBOOST_EF]': f"{reg['CatBoost']['E_f_mJ']['R2']:.4f}",
    '[RMSE_CATBOOST_EF]': f"{reg['CatBoost']['E_f_mJ']['RMSE']:.4f}",
    '[MAE_CATBOOST_EF]': f"{reg['CatBoost']['E_f_mJ']['MAE']:.4f}",
    '[MAPE_CATBOOST_EF]': f"{reg['CatBoost']['E_f_mJ']['MAPE']:.2f}%",

    '[R2_CATBOOST_D]': f"{reg['CatBoost']['Fractal_Dim_D']['R2']:.4f}",
    '[RMSE_CATBOOST_D]': f"{reg['CatBoost']['Fractal_Dim_D']['RMSE']:.4f}",
    '[MAE_CATBOOST_D]': f"{reg['CatBoost']['Fractal_Dim_D']['MAE']:.4f}",
    '[MAPE_CATBOOST_D]': f"{reg['CatBoost']['Fractal_Dim_D']['MAPE']:.2f}%",

    # MLP
    '[R2_MLP_SIGMA]': f"{reg['MLP_Neural']['Sigma_f_MPa']['R2']:.4f}",
    '[RMSE_MLP_SIGMA]': f"{reg['MLP_Neural']['Sigma_f_MPa']['RMSE']:.4f}",
    '[MAE_MLP_SIGMA]': f"{reg['MLP_Neural']['Sigma_f_MPa']['MAE']:.4f}",
    '[MAPE_MLP_SIGMA]': f"{reg['MLP_Neural']['Sigma_f_MPa']['MAPE']:.2f}%",

    '[R2_MLP_FF]': f"{reg['MLP_Neural']['F_f_kN']['R2']:.4f}",
    '[RMSE_MLP_FF]': f"{reg['MLP_Neural']['F_f_kN']['RMSE']:.4f}",
    '[MAE_MLP_FF]': f"{reg['MLP_Neural']['F_f_kN']['MAE']:.4f}",
    '[MAPE_MLP_FF]': f"{reg['MLP_Neural']['F_f_kN']['MAPE']:.2f}%",

    '[R2_MLP_EF]': f"{reg['MLP_Neural']['E_f_mJ']['R2']:.4f}",
    '[RMSE_MLP_EF]': f"{reg['MLP_Neural']['E_f_mJ']['RMSE']:.4f}",
    '[MAE_MLP_EF]': f"{reg['MLP_Neural']['E_f_mJ']['MAE']:.4f}",
    '[MAPE_MLP_EF]': f"{reg['MLP_Neural']['E_f_mJ']['MAPE']:.2f}%",

    '[R2_MLP_D]': f"{reg['MLP_Neural']['Fractal_Dim_D']['R2']:.4f}",
    '[RMSE_MLP_D]': f"{reg['MLP_Neural']['Fractal_Dim_D']['RMSE']:.4f}",
    '[MAE_MLP_D]': f"{reg['MLP_Neural']['Fractal_Dim_D']['MAE']:.4f}",
    '[MAPE_MLP_D]': f"{reg['MLP_Neural']['Fractal_Dim_D']['MAPE']:.2f}%",

    # Ridge
    '[R2_RIDGE_SIGMA]': f"{reg['Ridge_Poly']['Sigma_f_MPa']['R2']:.4f}",
    '[RMSE_RIDGE_SIGMA]': f"{reg['Ridge_Poly']['Sigma_f_MPa']['RMSE']:.4f}",
    '[MAE_RIDGE_SIGMA]': f"{reg['Ridge_Poly']['Sigma_f_MPa']['MAE']:.4f}",
    '[MAPE_RIDGE_SIGMA]': f"{reg['Ridge_Poly']['Sigma_f_MPa']['MAPE']:.2f}%",

    '[R2_RIDGE_FF]': f"{reg['Ridge_Poly']['F_f_kN']['R2']:.4f}",
    '[RMSE_RIDGE_FF]': f"{reg['Ridge_Poly']['F_f_kN']['RMSE']:.4f}",
    '[MAE_RIDGE_FF]': f"{reg['Ridge_Poly']['F_f_kN']['MAE']:.4f}",
    '[MAPE_RIDGE_FF]': f"{reg['Ridge_Poly']['F_f_kN']['MAPE']:.2f}%",

    '[R2_RIDGE_EF]': f"{reg['Ridge_Poly']['E_f_mJ']['R2']:.4f}",
    '[RMSE_RIDGE_EF]': f"{reg['Ridge_Poly']['E_f_mJ']['RMSE']:.4f}",
    '[MAE_RIDGE_EF]': f"{reg['Ridge_Poly']['E_f_mJ']['MAE']:.4f}",
    '[MAPE_RIDGE_EF]': f"{reg['Ridge_Poly']['E_f_mJ']['MAPE']:.2f}%",

    '[R2_RIDGE_D]': f"{reg['Ridge_Poly']['Fractal_Dim_D']['R2']:.4f}",
    '[RMSE_RIDGE_D]': f"{reg['Ridge_Poly']['Fractal_Dim_D']['RMSE']:.4f}",
    '[MAE_RIDGE_D]': f"{reg['Ridge_Poly']['Fractal_Dim_D']['MAE']:.4f}",
    '[MAPE_RIDGE_D]': f"{reg['Ridge_Poly']['Fractal_Dim_D']['MAPE']:.2f}%",

    # Classification
    '[ACC_XGBOOST_MODE]': f"{clf['XGBoost']['Accuracy']*100:.2f}%",
    '[F1_XGBOOST_MODE]': f"{clf['XGBoost']['Macro_F1']:.4f}",
    '[AUC_XGBOOST_MODE]': f"{clf['XGBoost']['ROC_AUC']:.4f}",

    '[ACC_RF_MODE]': f"{clf['RandomForest']['Accuracy']*100:.2f}%",
    '[F1_RF_MODE]': f"{clf['RandomForest']['Macro_F1']:.4f}",
    '[AUC_RF_MODE]': f"{clf['RandomForest']['ROC_AUC']:.4f}",

    '[ACC_MLP_MODE]': f"{clf['MLP']['Accuracy']*100:.2f}%",
    '[F1_MLP_MODE]': f"{clf['MLP']['Macro_F1']:.4f}",
    '[AUC_MLP_MODE]': f"{clf['MLP']['ROC_AUC']:.4f}",
}

count = 0
for k, v in replacements.items():
    if f"`{k}`" in text:
        text = text.replace(f"`{k}`", v)
        count += 1
    elif k in text:
        text = text.replace(k, v)
        count += 1

report_path.write_text(text, encoding='utf-8')
print(f"Successfully replaced {count} placeholder metrics in docs/BTP_Final_Report.md!")
