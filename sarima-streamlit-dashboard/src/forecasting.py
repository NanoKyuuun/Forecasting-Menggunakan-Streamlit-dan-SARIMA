"""Future forecasting helpers for PRD-08."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from src.modeling import prepare_model_series, train_sarima_model


@dataclass(frozen=True)
class ForecastingResult:
    """Complete forecasting payload for the forecasting page."""

    final_model_fit: Any | None
    forecast_df: pd.DataFrame
    order: tuple[int, int, int] | None
    seasonal_order: tuple[int, int, int, int] | None
    horizon: int
    freq_code: str
    notes: list[str]
    warnings: list[str]
    errors: list[str]


def _empty_result(
    errors: list[str],
    horizon: int,
    freq_code: str,
    warnings: list[str] | None = None,
) -> ForecastingResult:
    return ForecastingResult(
        final_model_fit=None,
        forecast_df=pd.DataFrame(
            columns=["periode", "forecast", "lower_bound", "upper_bound", "perubahan", "tren"]
        ),
        order=None,
        seasonal_order=None,
        horizon=horizon,
        freq_code=freq_code,
        notes=[],
        warnings=warnings or [],
        errors=errors,
    )


def build_future_index(last_index: Any, freq_code: str, steps: int) -> pd.DatetimeIndex:
    """Build future periods after the last historical period."""
    last_timestamp = pd.to_datetime(last_index)

    if freq_code == "YS":
        start = last_timestamp + pd.DateOffset(years=1)
        return pd.date_range(start=start, periods=steps, freq="YS")

    if freq_code == "MS":
        start = last_timestamp + pd.DateOffset(months=1)
        return pd.date_range(start=start, periods=steps, freq="MS")

    return pd.date_range(start=last_timestamp, periods=steps + 1, freq=freq_code)[1:]


def _extract_confidence_interval(conf_int: Any, steps: int) -> tuple[np.ndarray, np.ndarray]:
    """Return lower and upper CI arrays from statsmodels output."""
    if isinstance(conf_int, pd.DataFrame) and conf_int.shape[1] >= 2:
        return conf_int.iloc[:steps, 0].to_numpy(dtype=float), conf_int.iloc[:steps, 1].to_numpy(dtype=float)

    values = np.asarray(conf_int, dtype=float)
    if values.ndim == 2 and values.shape[1] >= 2:
        return values[:steps, 0], values[:steps, 1]

    empty = np.full(steps, np.nan)
    return empty, empty


def _trend_label(change: float | None) -> str:
    if change is None or pd.isna(change):
        return "Stabil"
    if change > 0:
        return "Naik"
    if change < 0:
        return "Turun"
    return "Stabil"


def forecast_future(
    model_fit: Any,
    last_index: Any,
    freq_code: str,
    steps: int,
    last_actual: float | None = None,
) -> pd.DataFrame:
    """Generate future forecast table with confidence intervals."""
    forecast_result = model_fit.get_forecast(steps=steps)
    forecast_mean = pd.Series(forecast_result.predicted_mean).iloc[:steps]
    lower_bound, upper_bound = _extract_confidence_interval(forecast_result.conf_int(), steps)
    future_index = build_future_index(last_index, freq_code, steps)

    forecast_df = pd.DataFrame(
        {
            "periode": future_index,
            "forecast": forecast_mean.to_numpy(dtype=float),
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
        }
    )

    previous_values = forecast_df["forecast"].shift(1)
    if last_actual is not None and not pd.isna(last_actual) and not forecast_df.empty:
        previous_values.iloc[0] = float(last_actual)

    forecast_df["perubahan"] = forecast_df["forecast"] - previous_values
    forecast_df["tren"] = forecast_df["perubahan"].map(_trend_label)
    return forecast_df


def generate_forecast(
    series: pd.Series | None,
    order: tuple[int, int, int] | None,
    seasonal_order: tuple[int, int, int, int] | None,
    horizon: int,
    freq_code: str,
) -> ForecastingResult:
    """Train final model on the full series and generate future forecasts."""
    warnings: list[str] = []
    notes: list[str] = []

    if series is None or not hasattr(series, "__len__"):
        return _empty_result(["Time series final belum tersedia."], horizon, freq_code)
    if order is None or seasonal_order is None:
        return _empty_result(["Parameter model belum tersedia. Latih model terlebih dahulu."], horizon, freq_code)
    if horizon < 1:
        return _empty_result(["Horizon forecast minimal 1 periode."], horizon, freq_code)

    clean_series = prepare_model_series(series)
    if len(clean_series) < 3:
        return _empty_result(["Data terlalu sedikit untuk melatih final model forecast."], horizon, freq_code)

    if freq_code == "YS" and horizon > 5:
        warnings.append("PRD merekomendasikan horizon tahunan 1-5 tahun; input saat ini melebihi rentang tersebut.")
    if freq_code == "MS" and horizon > 24:
        warnings.append("PRD merekomendasikan horizon bulanan 1-24 bulan; input saat ini melebihi rentang tersebut.")

    try:
        final_model_fit = train_sarima_model(clean_series, order, seasonal_order)
    except Exception as exc:
        return _empty_result([f"Training final model untuk forecast gagal: {exc}"], horizon, freq_code, warnings)

    try:
        forecast_df = forecast_future(
            final_model_fit,
            clean_series.index[-1],
            freq_code,
            horizon,
            last_actual=float(clean_series.iloc[-1]),
        )
    except Exception as exc:
        return ForecastingResult(
            final_model_fit=final_model_fit,
            forecast_df=pd.DataFrame(
                columns=["periode", "forecast", "lower_bound", "upper_bound", "perubahan", "tren"]
            ),
            order=order,
            seasonal_order=seasonal_order,
            horizon=horizon,
            freq_code=freq_code,
            notes=notes,
            warnings=warnings,
            errors=[f"Forecast future gagal dibuat: {exc}"],
        )

    notes.append("Final model dilatih ulang menggunakan seluruh time series final.")
    notes.append("Confidence interval diambil dari output get_forecast statsmodels.")

    return ForecastingResult(
        final_model_fit=final_model_fit,
        forecast_df=forecast_df,
        order=order,
        seasonal_order=seasonal_order,
        horizon=horizon,
        freq_code=freq_code,
        notes=notes,
        warnings=warnings,
        errors=[],
    )
