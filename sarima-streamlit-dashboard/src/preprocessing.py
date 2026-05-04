"""Data validation and cleaning helpers for PRD-03."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd


TARGET_MISSING_FILL_ZERO = "Isi 0"
TARGET_MISSING_DROP = "Hapus baris"


@dataclass(frozen=True)
class OutlierBounds:
    """IQR limits used to mark target outliers."""

    q1: float | None
    q3: float | None
    iqr: float | None
    lower: float | None
    upper: float | None


@dataclass(frozen=True)
class PreprocessingResult:
    """Result object returned by the preprocessing workflow."""

    clean_df: pd.DataFrame
    missing_summary: pd.DataFrame
    outlier_df: pd.DataFrame
    outlier_bounds: OutlierBounds
    column_map: dict[str, str]
    selected_columns: dict[str, str | None]
    notes: list[str]
    errors: list[str]
    rows_before: int
    rows_after: int
    full_duplicate_count: int
    key_duplicate_count: int


def normalize_column_name(column: Any) -> str:
    """Return the PRD-normalized version of a dataframe column name."""
    return str(column).strip().lower().replace(" ", "_")


def _deduplicate_column_names(columns: list[str]) -> list[str]:
    counts: dict[str, int] = {}
    unique_columns: list[str] = []

    for column in columns:
        if column not in counts:
            counts[column] = 1
            unique_columns.append(column)
            continue

        counts[column] += 1
        unique_columns.append(f"{column}_{counts[column]}")

    return unique_columns


def clean_column_names(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, str]]:
    """Clean dataframe column names and return the original-to-clean mapping."""
    dataframe = dataframe.copy()
    original_columns = [str(column) for column in dataframe.columns]
    cleaned_columns = [normalize_column_name(column) for column in original_columns]
    unique_columns = _deduplicate_column_names(cleaned_columns)
    dataframe.columns = unique_columns
    return dataframe, dict(zip(original_columns, unique_columns))


def _resolve_selected_column(column_name: str | None, column_map: dict[str, str]) -> str | None:
    if not column_name:
        return None

    if column_name in column_map:
        return column_map[column_name]

    normalized = normalize_column_name(column_name)
    if normalized in column_map.values():
        return normalized

    return None


def _infer_time_mode(series: pd.Series, frequency: str) -> str:
    if frequency != "Tahunan":
        return "date"

    numeric_values = pd.to_numeric(series, errors="coerce")
    valid_values = numeric_values.dropna()
    if valid_values.empty:
        return "date"

    year_like = valid_values.between(1900, 2200).mean()
    return "year" if year_like >= 0.8 else "date"


def convert_time_column(dataframe: pd.DataFrame, time_col: str, frequency: str) -> tuple[pd.DataFrame, str]:
    """Convert the selected time column into pandas datetimes."""
    dataframe = dataframe.copy()
    time_mode = _infer_time_mode(dataframe[time_col], frequency)

    if time_mode == "year":
        years = pd.to_numeric(dataframe[time_col], errors="coerce").astype("Int64")
        dataframe[time_col] = pd.to_datetime(years.astype("string") + "-01-01", errors="coerce")
        return dataframe, time_mode

    dataframe[time_col] = pd.to_datetime(dataframe[time_col], errors="coerce")
    return dataframe, time_mode


def convert_target_to_numeric(dataframe: pd.DataFrame, target_col: str) -> pd.DataFrame:
    """Convert the selected target column into numeric values."""
    dataframe = dataframe.copy()
    dataframe[target_col] = pd.to_numeric(dataframe[target_col], errors="coerce")
    return dataframe


def build_missing_summary(
    dataframe: pd.DataFrame,
    time_col: str,
    target_col: str,
    category_col: str | None,
    target_missing_action: str,
) -> pd.DataFrame:
    """Return a column-level missing-value report with the PRD action note."""
    actions: dict[str, str] = {
        time_col: "Hapus baris",
        target_col: "Isi 0" if target_missing_action == TARGET_MISSING_FILL_ZERO else "Hapus baris",
    }
    if category_col:
        actions[category_col] = 'Isi "Tidak Diketahui"'

    row_count = len(dataframe)
    rows: list[dict[str, Any]] = []
    for column in dataframe.columns:
        missing_count = int(dataframe[column].isna().sum())
        missing_percentage = 0.0 if row_count == 0 else round((missing_count / row_count) * 100, 2)
        rows.append(
            {
                "Kolom": column,
                "Missing": missing_count,
                "Missing (%)": missing_percentage,
                "Tindakan": actions.get(column, "Tidak diubah"),
            }
        )

    return pd.DataFrame(rows)


def detect_outliers_iqr(dataframe: pd.DataFrame, target_col: str) -> tuple[pd.DataFrame, OutlierBounds]:
    """Mark target outliers using the IQR rule without removing rows."""
    if dataframe.empty or target_col not in dataframe.columns:
        return dataframe.head(0).copy(), OutlierBounds(None, None, None, None, None)

    series = pd.to_numeric(dataframe[target_col], errors="coerce").dropna()
    if series.empty:
        return dataframe.head(0).copy(), OutlierBounds(None, None, None, None, None)

    q1 = float(series.quantile(0.25))
    q3 = float(series.quantile(0.75))
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    mask = (dataframe[target_col] < lower) | (dataframe[target_col] > upper)
    outliers = dataframe.loc[mask].copy()
    return outliers, OutlierBounds(q1, q3, iqr, lower, upper)


def _empty_result(
    dataframe: pd.DataFrame,
    column_map: dict[str, str],
    selected_columns: dict[str, str | None],
    errors: list[str],
) -> PreprocessingResult:
    return PreprocessingResult(
        clean_df=pd.DataFrame(),
        missing_summary=pd.DataFrame(columns=["Kolom", "Missing", "Missing (%)", "Tindakan"]),
        outlier_df=pd.DataFrame(),
        outlier_bounds=OutlierBounds(None, None, None, None, None),
        column_map=column_map,
        selected_columns=selected_columns,
        notes=[],
        errors=errors,
        rows_before=len(dataframe),
        rows_after=0,
        full_duplicate_count=0,
        key_duplicate_count=0,
    )


def preprocess_data(
    dataframe: pd.DataFrame,
    time_col: str | None,
    target_col: str | None,
    category_col: str | None = None,
    *,
    frequency: str = "Tahunan",
    target_missing_action: str = TARGET_MISSING_FILL_ZERO,
) -> PreprocessingResult:
    """Clean and validate raw data into `clean_df` for downstream transformation."""
    cleaned_df, column_map = clean_column_names(dataframe)
    selected_columns = {
        "time": _resolve_selected_column(time_col, column_map),
        "target": _resolve_selected_column(target_col, column_map),
        "category": _resolve_selected_column(category_col, column_map),
    }

    errors: list[str] = []
    if not selected_columns["time"]:
        errors.append("Kolom waktu belum dipilih atau tidak ditemukan.")
    if not selected_columns["target"]:
        errors.append("Kolom target belum dipilih atau tidak ditemukan.")
    if selected_columns["time"] and selected_columns["time"] == selected_columns["target"]:
        errors.append("Kolom waktu dan target tidak boleh sama.")
    if selected_columns["category"] and selected_columns["category"] in {
        selected_columns["time"],
        selected_columns["target"],
    }:
        errors.append("Kolom prodi/jurusan tidak boleh sama dengan kolom waktu atau target.")

    if errors:
        return _empty_result(cleaned_df, column_map, selected_columns, errors)

    time_column = selected_columns["time"]
    target_column = selected_columns["target"]
    category_column = selected_columns["category"]
    assert time_column is not None
    assert target_column is not None

    notes: list[str] = []
    working_df, time_mode = convert_time_column(cleaned_df, time_column, frequency)
    working_df = convert_target_to_numeric(working_df, target_column)

    if category_column:
        working_df[category_column] = working_df[category_column].astype("string").str.strip()
        working_df[category_column] = working_df[category_column].replace("", pd.NA)

    missing_summary = build_missing_summary(
        working_df,
        time_column,
        target_column,
        category_column,
        target_missing_action,
    )

    rows_before = len(working_df)
    missing_time_count = int(working_df[time_column].isna().sum())
    if missing_time_count:
        working_df = working_df.dropna(subset=[time_column])
        notes.append(f"{missing_time_count} baris dihapus karena kolom waktu tidak valid/kosong.")

    missing_target_count = int(working_df[target_column].isna().sum())
    if missing_target_count and target_missing_action == TARGET_MISSING_DROP:
        working_df = working_df.dropna(subset=[target_column])
        notes.append(f"{missing_target_count} baris dihapus karena target kosong/tidak numerik.")
    elif missing_target_count:
        working_df[target_column] = working_df[target_column].fillna(0)
        notes.append(f"{missing_target_count} nilai target kosong/tidak numerik diisi 0.")

    if category_column:
        missing_category_count = int(working_df[category_column].isna().sum())
        if missing_category_count:
            working_df[category_column] = working_df[category_column].fillna("Tidak Diketahui")
            notes.append(f'{missing_category_count} nilai prodi/jurusan kosong diisi "Tidak Diketahui".')

    full_duplicate_count = int(working_df.duplicated().sum())
    if full_duplicate_count:
        working_df = working_df.drop_duplicates()
        notes.append(f"{full_duplicate_count} duplikasi penuh dihapus.")

    key_columns = [time_column]
    if category_column:
        key_columns.append(category_column)

    key_duplicate_count = int(working_df.duplicated(subset=key_columns, keep=False).sum())
    output_columns = [*key_columns, target_column]
    clean_df = working_df.loc[:, output_columns].copy()

    if key_duplicate_count:
        clean_df = (
            clean_df.groupby(key_columns, dropna=False, as_index=False)[target_column]
            .sum()
            .sort_values(key_columns)
            .reset_index(drop=True)
        )
        if category_column:
            notes.append(f"{key_duplicate_count} baris duplikasi periode dan prodi digabung dengan sum.")
        else:
            notes.append(f"{key_duplicate_count} baris duplikasi periode digabung dengan sum.")
    else:
        clean_df = clean_df.sort_values(key_columns).reset_index(drop=True)

    outlier_df, outlier_bounds = detect_outliers_iqr(clean_df, target_column)

    if time_mode == "year":
        notes.append("Kolom waktu dikenali sebagai tahun dan dikonversi ke tanggal 1 Januari.")
    else:
        notes.append("Kolom waktu dikonversi sebagai tanggal/periode.")

    if outlier_df.empty:
        notes.append("Tidak ada outlier target berdasarkan metode IQR.")
    else:
        notes.append(f"{len(outlier_df)} outlier target ditandai berdasarkan metode IQR.")

    return PreprocessingResult(
        clean_df=clean_df,
        missing_summary=missing_summary,
        outlier_df=outlier_df,
        outlier_bounds=outlier_bounds,
        column_map=column_map,
        selected_columns=selected_columns,
        notes=notes,
        errors=[],
        rows_before=rows_before,
        rows_after=len(clean_df),
        full_duplicate_count=full_duplicate_count,
        key_duplicate_count=key_duplicate_count,
    )
