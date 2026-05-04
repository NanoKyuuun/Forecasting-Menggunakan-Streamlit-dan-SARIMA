"""Model evaluation helpers for PRD-07."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import acf


@dataclass(frozen=True)
class EvaluationResult:
    """Complete evaluation payload for the evaluation page."""

    actual: pd.Series
    predicted: pd.Series
    prediction_df: pd.DataFrame
    metrics: dict[str, float | None]
    metrics_df: pd.DataFrame
    residuals: pd.Series
    residual_df: pd.DataFrame
    residual_acf_df: pd.DataFrame
    ljung_box_df: pd.DataFrame
    notes: list[str]
    warnings: list[str]
    errors: list[str]


def _empty_result(errors: list[str], warnings: list[str] | None = None) -> EvaluationResult:
    return EvaluationResult(
        actual=pd.Series(dtype=float),
        predicted=pd.Series(dtype=float),
        prediction_df=pd.DataFrame(columns=["periode", "aktual", "prediksi", "error_abs", "error_pct"]),
        metrics={"MAE": None, "MSE": None, "RMSE": None, "MAPE": None},
        metrics_df=pd.DataFrame(columns=["Metrik", "Nilai", "Keterangan"]),
        residuals=pd.Series(dtype=float),
        residual_df=pd.DataFrame(columns=["periode", "residual"]),
        residual_acf_df=pd.DataFrame(columns=["Lag", "ACF"]),
        ljung_box_df=pd.DataFrame(columns=["Lag", "LB Statistic", "p-value"]),
        notes=[],
        warnings=warnings or [],
        errors=errors,
    )


def prepare_test_series(test: pd.Series) -> pd.Series:
    """Return numeric testing data with a datetime index when possible."""
    prepared = test.copy()
    prepared.index = pd.to_datetime(prepared.index, errors="coerce")
    prepared = prepared[prepared.index.notna()]
    prepared = pd.to_numeric(prepared, errors="coerce")
    return prepared.dropna().sort_index().astype(float)


def align_actual_predicted(actual: pd.Series, predicted: pd.Series) -> tuple[pd.Series, pd.Series]:
    """Align actual and predicted values by testing periods."""
    actual_clean = pd.to_numeric(actual, errors="coerce").dropna().astype(float)
    predicted_clean = pd.to_numeric(predicted, errors="coerce").dropna().astype(float)
    length = min(len(actual_clean), len(predicted_clean))

    if length == 0:
        return pd.Series(dtype=float), pd.Series(dtype=float)

    actual_aligned = actual_clean.iloc[:length]
    predicted_aligned = predicted_clean.iloc[:length].copy()
    predicted_aligned.index = actual_aligned.index
    return actual_aligned, predicted_aligned


def calculate_metrics(actual: pd.Series, predicted: pd.Series) -> dict[str, float | None]:
    """Calculate MAE, MSE, RMSE, and zero-safe MAPE."""
    actual_aligned, predicted_aligned = align_actual_predicted(actual, predicted)
    if actual_aligned.empty:
        return {"MAE": None, "MSE": None, "RMSE": None, "MAPE": None}

    errors = actual_aligned - predicted_aligned
    mae = float(np.mean(np.abs(errors)))
    mse = float(np.mean(np.square(errors)))
    rmse = float(np.sqrt(mse))

    mape = None
    if not (actual_aligned == 0).any():
        mape = float(np.mean(np.abs(errors / actual_aligned)) * 100)

    return {"MAE": mae, "MSE": mse, "RMSE": rmse, "MAPE": mape}


def calculate_residuals(actual: pd.Series, predicted: pd.Series) -> pd.Series:
    """Return actual minus predicted values."""
    actual_aligned, predicted_aligned = align_actual_predicted(actual, predicted)
    residuals = actual_aligned - predicted_aligned
    residuals.name = "residual"
    return residuals


def build_prediction_df(actual: pd.Series, predicted: pd.Series) -> pd.DataFrame:
    """Return an aligned actual-vs-predicted table."""
    residual = actual - predicted
    error_pct = pd.Series(np.nan, index=actual.index, dtype=float)
    non_zero_mask = actual != 0
    error_pct.loc[non_zero_mask] = np.abs(residual.loc[non_zero_mask] / actual.loc[non_zero_mask]) * 100

    return pd.DataFrame(
        {
            "periode": actual.index,
            "aktual": actual.values,
            "prediksi": predicted.values,
            "error_abs": np.abs(residual.values),
            "error_pct": error_pct.values,
        }
    )


def build_metrics_df(metrics: dict[str, float | None]) -> pd.DataFrame:
    """Return metrics in a dataframe ready for display."""
    descriptions = {
        "MAE": "Rata-rata absolut selisih aktual dan prediksi.",
        "MSE": "Rata-rata kuadrat error.",
        "RMSE": "Akar dari MSE, kembali ke satuan target.",
        "MAPE": "Persentase error rata-rata; tidak dihitung jika aktual memuat 0.",
    }
    return pd.DataFrame(
        [
            {
                "Metrik": metric,
                "Nilai": value,
                "Keterangan": descriptions[metric],
            }
            for metric, value in metrics.items()
        ]
    )


def calculate_residual_acf(residuals: pd.Series, max_lag: int = 10) -> pd.DataFrame:
    """Return residual ACF when observations are sufficient."""
    clean_residuals = pd.to_numeric(residuals, errors="coerce").dropna()
    if len(clean_residuals) < 4 or clean_residuals.nunique() <= 1:
        return pd.DataFrame(columns=["Lag", "ACF"])

    nlags = min(max_lag, len(clean_residuals) - 1)
    if nlags < 1:
        return pd.DataFrame(columns=["Lag", "ACF"])

    try:
        acf_values = acf(clean_residuals, nlags=nlags, fft=False)
    except Exception:
        return pd.DataFrame(columns=["Lag", "ACF"])

    return pd.DataFrame({"Lag": list(range(nlags + 1)), "ACF": acf_values})


def calculate_ljung_box(residuals: pd.Series, max_lag: int = 10) -> pd.DataFrame:
    """Run Ljung-Box residual autocorrelation test when data is sufficient."""
    clean_residuals = pd.to_numeric(residuals, errors="coerce").dropna()
    if len(clean_residuals) < 6 or clean_residuals.nunique() <= 1:
        return pd.DataFrame(columns=["Lag", "LB Statistic", "p-value"])

    max_allowed_lag = max(1, len(clean_residuals) // 2)
    lags = list(range(1, min(max_lag, max_allowed_lag) + 1))
    if not lags:
        return pd.DataFrame(columns=["Lag", "LB Statistic", "p-value"])

    try:
        result = acorr_ljungbox(clean_residuals, lags=lags, return_df=True)
    except Exception:
        return pd.DataFrame(columns=["Lag", "LB Statistic", "p-value"])

    result.index.name = "Lag"
    return (
        result.reset_index()
        .rename(columns={"lb_stat": "LB Statistic", "lb_pvalue": "p-value"})
        [["Lag", "LB Statistic", "p-value"]]
    )


def evaluate_model(model_fit: Any, test: pd.Series | None) -> EvaluationResult:
    """Evaluate a fitted SARIMAX model against testing data."""
    if model_fit is None:
        return _empty_result(["Model belum tersedia. Latih model pada halaman Pemodelan SARIMA terlebih dahulu."])
    if test is None or not hasattr(test, "__len__"):
        return _empty_result(["Data testing belum tersedia. Jalankan train-test split pada halaman Pemodelan SARIMA."])

    actual = prepare_test_series(test)
    if actual.empty:
        return _empty_result(["Data testing kosong setelah pembersihan nilai tanggal/numerik."])

    try:
        forecast_result = model_fit.get_forecast(steps=len(actual))
        predicted = pd.Series(forecast_result.predicted_mean)
    except Exception as exc:
        return _empty_result([f"Prediksi testing gagal dibuat: {exc}"])

    actual, predicted = align_actual_predicted(actual, predicted)
    if actual.empty:
        return _empty_result(["Aktual dan prediksi tidak dapat disejajarkan."])

    metrics = calculate_metrics(actual, predicted)
    residuals = calculate_residuals(actual, predicted)
    residual_df = pd.DataFrame({"periode": residuals.index, "residual": residuals.values})
    residual_acf_df = calculate_residual_acf(residuals)
    ljung_box_df = calculate_ljung_box(residuals)

    warnings: list[str] = []
    notes: list[str] = []

    if len(actual) <= 1:
        warnings.append("Data testing sangat sedikit, sehingga evaluasi model hanya bersifat indikatif.")
    if metrics["MAPE"] is None:
        warnings.append("MAPE tidak dihitung karena nilai aktual pada data testing memuat 0.")

    if residual_acf_df.empty:
        notes.append("Residual ACF dilewati karena residual terlalu sedikit atau konstan.")
    else:
        notes.append("Residual ACF berhasil dihitung.")

    if ljung_box_df.empty:
        notes.append("Ljung-Box dilewati karena residual belum cukup untuk diagnostic checking yang kuat.")
    else:
        notes.append("Ljung-Box berhasil dihitung untuk membaca indikasi autokorelasi residual.")

    return EvaluationResult(
        actual=actual,
        predicted=predicted,
        prediction_df=build_prediction_df(actual, predicted),
        metrics=metrics,
        metrics_df=build_metrics_df(metrics),
        residuals=residuals,
        residual_df=residual_df,
        residual_acf_df=residual_acf_df,
        ljung_box_df=ljung_box_df,
        notes=notes,
        warnings=warnings,
        errors=[],
    )
