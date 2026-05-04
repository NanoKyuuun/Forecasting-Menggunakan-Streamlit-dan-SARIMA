"""Time-series transformation helpers for PRD-04."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd


FREQUENCY_CODE_MAP = {
    "Tahunan": "YS",
    "Bulanan": "MS",
}

MISSING_STRATEGY_LEAVE = "Biarkan kosong"
MISSING_STRATEGY_ZERO = "Isi 0"
MISSING_STRATEGY_FFILL = "Forward fill"
MISSING_STRATEGY_INTERPOLATE = "Interpolasi"


@dataclass(frozen=True)
class TransformationResult:
    """Result object returned by the data-transformation workflow."""

    aggregated_df: pd.DataFrame
    time_series_df: pd.DataFrame
    series: pd.Series
    frequency_label: str
    frequency_code: str
    data_mode: str
    missing_period_strategy: str
    selected_category: str
    notes: list[str]
    warnings: list[str]
    errors: list[str]
    period_start: Any
    period_end: Any
    observation_count: int
    target_col: str
    time_col: str
    category_col: str | None


def get_frequency_code(frequency_label: str) -> str:
    """Return the pandas frequency code for the selected dashboard label."""
    return FREQUENCY_CODE_MAP.get(frequency_label, "YS")


def _align_to_period(series: pd.Series, frequency_label: str) -> pd.Series:
    datetime_values = pd.to_datetime(series, errors="coerce")
    if frequency_label == "Bulanan":
        return datetime_values.dt.to_period("M").dt.to_timestamp()

    return datetime_values.dt.to_period("Y").dt.to_timestamp()


def _apply_missing_strategy(series: pd.Series, strategy: str) -> pd.Series:
    if strategy == MISSING_STRATEGY_ZERO:
        return series.fillna(0)

    if strategy == MISSING_STRATEGY_FFILL:
        return series.ffill()

    if strategy == MISSING_STRATEGY_INTERPOLATE:
        return series.interpolate()

    return series


def _build_empty_result(
    *,
    frequency_label: str,
    missing_period_strategy: str,
    selected_category: str,
    time_col: str | None,
    target_col: str | None,
    category_col: str | None,
    errors: list[str],
) -> TransformationResult:
    frequency_code = get_frequency_code(frequency_label)
    empty_series = pd.Series(dtype="float64", name=target_col)
    return TransformationResult(
        aggregated_df=pd.DataFrame(),
        time_series_df=pd.DataFrame(columns=[time_col or "periode", target_col or "nilai"]),
        series=empty_series,
        frequency_label=frequency_label,
        frequency_code=frequency_code,
        data_mode=frequency_label,
        missing_period_strategy=missing_period_strategy,
        selected_category=selected_category,
        notes=[],
        warnings=[],
        errors=errors,
        period_start=None,
        period_end=None,
        observation_count=0,
        target_col=target_col or "",
        time_col=time_col or "",
        category_col=category_col,
    )


def _build_period_index(series: pd.Series, frequency_code: str) -> pd.DatetimeIndex:
    if series.empty:
        return pd.DatetimeIndex([])

    return pd.date_range(start=series.index.min(), end=series.index.max(), freq=frequency_code)


def transform_to_timeseries(
    dataframe: pd.DataFrame,
    time_col: str | None,
    target_col: str | None,
    *,
    frequency_label: str = "Tahunan",
    category_col: str | None = None,
    selected_category: str | None = "Semua prodi",
    missing_period_strategy: str = MISSING_STRATEGY_ZERO,
) -> TransformationResult:
    """Transform cleaned data into a final univariate time series."""
    selected_category = selected_category or "Semua prodi"
    frequency_code = get_frequency_code(frequency_label)

    errors: list[str] = []
    if dataframe is None or dataframe.empty:
        errors.append("Data bersih belum tersedia. Jalankan Data dan Preprocessing terlebih dahulu.")
    if not time_col or time_col not in getattr(dataframe, "columns", []):
        errors.append("Kolom waktu hasil preprocessing tidak ditemukan.")
    if not target_col or target_col not in getattr(dataframe, "columns", []):
        errors.append("Kolom target hasil preprocessing tidak ditemukan.")
    if category_col and category_col not in getattr(dataframe, "columns", []):
        errors.append("Kolom prodi/jurusan hasil preprocessing tidak ditemukan.")

    if errors:
        return _build_empty_result(
            frequency_label=frequency_label,
            missing_period_strategy=missing_period_strategy,
            selected_category=selected_category,
            time_col=time_col,
            target_col=target_col,
            category_col=category_col,
            errors=errors,
        )

    assert time_col is not None
    assert target_col is not None

    data = dataframe.copy()
    data[time_col] = _align_to_period(data[time_col], frequency_label)
    data[target_col] = pd.to_numeric(data[target_col], errors="coerce")
    data = data.dropna(subset=[time_col, target_col])

    if category_col:
        data[category_col] = data[category_col].astype("string").fillna("Tidak Diketahui")

    if category_col and selected_category != "Semua prodi":
        data = data[data[category_col].astype(str) == selected_category]

    if data.empty:
        return _build_empty_result(
            frequency_label=frequency_label,
            missing_period_strategy=missing_period_strategy,
            selected_category=selected_category,
            time_col=time_col,
            target_col=target_col,
            category_col=category_col,
            errors=["Tidak ada data setelah filter prodi/jurusan diterapkan."],
        )

    notes: list[str] = []
    warnings: list[str] = []
    period_col = "periode"

    aggregation_columns = [time_col]
    display_columns = [period_col]
    if category_col:
        aggregation_columns.append(category_col)
        display_columns.append(category_col)

    aggregated_df = (
        data.groupby(aggregation_columns, dropna=False, as_index=False)[target_col]
        .sum()
        .rename(columns={time_col: period_col})
        .sort_values(display_columns)
        .reset_index(drop=True)
    )

    series_source = data.groupby(time_col, dropna=False)[target_col].sum().sort_index()
    period_index = _build_period_index(series_source, frequency_code)
    final_series = series_source.reindex(period_index)
    final_series = _apply_missing_strategy(final_series, missing_period_strategy)
    final_series.name = target_col
    final_series.index.name = period_col

    time_series_df = final_series.reset_index().rename(columns={target_col: "nilai"})
    observation_count = int(final_series.count())
    period_start = final_series.index.min() if len(final_series) else None
    period_end = final_series.index.max() if len(final_series) else None

    notes.append(f"Data diagregasi per periode dengan frekuensi {frequency_label} ({frequency_code}).")
    if category_col and selected_category != "Semua prodi":
        notes.append(f"Filter prodi/jurusan diterapkan untuk {selected_category}.")
    elif category_col:
        notes.append("Semua prodi/jurusan digabung menjadi satu deret waktu total.")
    else:
        notes.append("Kolom prodi/jurusan tidak digunakan pada transformasi ini.")

    if missing_period_strategy == MISSING_STRATEGY_ZERO:
        notes.append("Periode hilang diisi 0.")
    elif missing_period_strategy == MISSING_STRATEGY_FFILL:
        notes.append("Periode hilang diisi dengan forward fill.")
    elif missing_period_strategy == MISSING_STRATEGY_INTERPOLATE:
        notes.append("Periode hilang diisi dengan interpolasi.")
    else:
        notes.append("Periode hilang dibiarkan kosong.")

    if frequency_label == "Tahunan" and len(final_series) < 8:
        warnings.append(
            "Data tahunan memiliki jumlah observasi terbatas. Model dipakai sebagai analisis tren awal, "
            "bukan pembuktian musiman yang kuat."
        )
    if frequency_label == "Bulanan" and len(final_series) < 24:
        warnings.append(
            "Data bulanan kurang dari 24 observasi. SARIMA musiman dapat dicoba, tetapi hasil perlu ditafsirkan hati-hati."
        )

    return TransformationResult(
        aggregated_df=aggregated_df,
        time_series_df=time_series_df,
        series=final_series,
        frequency_label=frequency_label,
        frequency_code=frequency_code,
        data_mode=frequency_label,
        missing_period_strategy=missing_period_strategy,
        selected_category=selected_category,
        notes=notes,
        warnings=warnings,
        errors=[],
        period_start=period_start,
        period_end=period_end,
        observation_count=observation_count,
        target_col=target_col,
        time_col=time_col,
        category_col=category_col,
    )
