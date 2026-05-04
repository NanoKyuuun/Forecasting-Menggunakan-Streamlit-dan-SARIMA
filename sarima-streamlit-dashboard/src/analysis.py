"""Time-series analysis helpers for PRD-05."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import acf, adfuller, pacf


@dataclass(frozen=True)
class AdfResult:
    """ADF stationarity test result."""

    success: bool
    message: str
    adf_statistic: float | None = None
    p_value: float | None = None
    used_lag: int | None = None
    n_obs: int | None = None
    critical_values: dict[str, float] | None = None
    is_stationary: bool | None = None


@dataclass(frozen=True)
class AnalysisResult:
    """Complete analysis payload for the analysis page."""

    series: pd.Series
    stats_df: pd.DataFrame
    rolling_df: pd.DataFrame
    decomposition_df: pd.DataFrame | None
    adf_result: AdfResult
    correlation_df: pd.DataFrame
    rolling_window: int
    notes: list[str]
    warnings: list[str]


def prepare_series(series: pd.Series) -> pd.Series:
    """Return a numeric, sorted time series suitable for analysis."""
    prepared = series.copy()
    prepared.index = pd.to_datetime(prepared.index, errors="coerce")
    prepared = prepared[prepared.index.notna()]
    prepared = pd.to_numeric(prepared, errors="coerce")
    prepared = prepared.sort_index()
    return prepared


def calculate_descriptive_stats(series: pd.Series) -> pd.DataFrame:
    """Return descriptive statistics required by the PRD."""
    clean_series = series.dropna()
    values: list[tuple[str, Any]] = [
        ("count", int(clean_series.count())),
        ("mean", clean_series.mean()),
        ("median", clean_series.median()),
        ("min", clean_series.min()),
        ("max", clean_series.max()),
        ("std", clean_series.std()),
    ]
    return pd.DataFrame(values, columns=["Metrik", "Nilai"])


def get_rolling_window(frequency_label: str, observation_count: int) -> int:
    """Select the rolling window according to PRD guidance."""
    if frequency_label == "Bulanan":
        return 12

    if observation_count >= 4:
        return 3

    return 2


def calculate_rolling(series: pd.Series, window: int) -> pd.DataFrame:
    """Return rolling mean and rolling standard deviation."""
    return pd.DataFrame(
        {
            "periode": series.index,
            "aktual": series.values,
            "rolling_mean": series.rolling(window=window).mean().values,
            "rolling_std": series.rolling(window=window).std().values,
        }
    )


def can_decompose(series: pd.Series, period: int) -> bool:
    """Return True when data is long enough for seasonal decomposition."""
    return len(series.dropna()) >= period * 2


def run_decomposition(series: pd.Series, frequency_label: str) -> pd.DataFrame | None:
    """Run monthly seasonal decomposition when data is sufficient."""
    if frequency_label != "Bulanan" or not can_decompose(series, 12):
        return None

    clean_series = series.dropna()
    result = seasonal_decompose(clean_series, model="additive", period=12)
    return pd.DataFrame(
        {
            "periode": clean_series.index,
            "observed": result.observed.values,
            "trend": result.trend.values,
            "seasonal": result.seasonal.values,
            "resid": result.resid.values,
        }
    )


def run_adf_test(series: pd.Series) -> AdfResult:
    """Run the Augmented Dickey-Fuller stationarity test when data is sufficient."""
    clean_series = series.dropna()
    if len(clean_series) < 8:
        return AdfResult(False, "Data terlalu sedikit untuk ADF Test yang kuat.")

    if clean_series.nunique() <= 1:
        return AdfResult(False, "ADF Test tidak dapat dijalankan karena nilai time series konstan.")

    try:
        result = adfuller(clean_series)
    except Exception as exc:
        return AdfResult(False, f"ADF Test gagal dijalankan: {exc}")

    p_value = float(result[1])
    return AdfResult(
        success=True,
        message="Data stasioner." if p_value < 0.05 else "Data belum stasioner.",
        adf_statistic=float(result[0]),
        p_value=p_value,
        used_lag=int(result[2]),
        n_obs=int(result[3]),
        critical_values={key: float(value) for key, value in result[4].items()},
        is_stationary=p_value < 0.05,
    )


def calculate_acf_pacf(series: pd.Series, max_lag: int | None = None) -> pd.DataFrame:
    """Return ACF and PACF values when enough observations are available."""
    clean_series = series.dropna()
    if len(clean_series) < 8 or clean_series.nunique() <= 1:
        return pd.DataFrame(columns=["Lag", "ACF", "PACF"])

    allowed_lag = max(1, (len(clean_series) // 2) - 1)
    nlags = min(max_lag or 20, allowed_lag)
    if nlags < 2:
        return pd.DataFrame(columns=["Lag", "ACF", "PACF"])

    try:
        acf_values = acf(clean_series, nlags=nlags, fft=False)
        pacf_values = pacf(clean_series, nlags=nlags, method="ywm")
    except Exception:
        return pd.DataFrame(columns=["Lag", "ACF", "PACF"])

    return pd.DataFrame(
        {
            "Lag": list(range(nlags + 1)),
            "ACF": acf_values,
            "PACF": pacf_values,
        }
    )


def analyze_time_series(series: pd.Series, frequency_label: str) -> AnalysisResult:
    """Build all PRD-05 analysis artifacts from the final time series."""
    prepared_series = prepare_series(series)
    clean_series = prepared_series.dropna()
    observation_count = len(clean_series)
    rolling_window = get_rolling_window(frequency_label, observation_count)

    warnings: list[str] = []
    notes: list[str] = []

    if prepared_series.empty:
        warnings.append("Time series final belum tersedia untuk dianalisis.")
    if frequency_label == "Tahunan" and observation_count < 8:
        warnings.append("Data tahunan pendek. Pola tren dapat dibaca, tetapi pembuktian statistik masih terbatas.")
    if frequency_label == "Bulanan" and observation_count < 24:
        warnings.append("Data bulanan kurang dari 24 observasi sehingga dekomposisi musiman belum kuat.")

    decomposition_df = run_decomposition(prepared_series, frequency_label)
    if decomposition_df is not None:
        notes.append("Dekomposisi musiman bulanan berhasil dijalankan dengan period 12.")
    elif frequency_label == "Bulanan":
        notes.append("Dekomposisi dilewati karena data bulanan belum mencapai minimal 24 observasi.")
    else:
        notes.append("Dekomposisi musiman dilewati untuk mode tahunan.")

    adf_result = run_adf_test(prepared_series)
    if adf_result.success:
        notes.append("ADF Test berhasil dijalankan.")
    else:
        notes.append(adf_result.message)

    correlation_df = calculate_acf_pacf(prepared_series)
    if correlation_df.empty:
        notes.append("ACF/PACF dilewati atau belum kuat karena observasi terlalu sedikit/konstan.")
    else:
        notes.append("ACF/PACF berhasil dihitung.")

    return AnalysisResult(
        series=prepared_series,
        stats_df=calculate_descriptive_stats(prepared_series),
        rolling_df=calculate_rolling(prepared_series, rolling_window),
        decomposition_df=decomposition_df,
        adf_result=adf_result,
        correlation_df=correlation_df,
        rolling_window=rolling_window,
        notes=notes,
        warnings=warnings,
    )
