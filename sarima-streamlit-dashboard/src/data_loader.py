"""Dataset loading and raw-data preview helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd


SUPPORTED_EXTENSIONS = {".csv", ".xls", ".xlsx"}


class DataLoadError(ValueError):
    """Raised when an uploaded dataset cannot be loaded safely."""


@dataclass(frozen=True)
class LoadedFileMetadata:
    """Metadata captured from an uploaded raw dataset."""

    file_name: str
    extension: str
    file_size_bytes: int | None
    row_count: int
    column_count: int
    columns: list[str]
    dtypes: dict[str, str]
    dataset_shape: str


def _get_file_name(uploaded_file: Any) -> str:
    file_name = getattr(uploaded_file, "name", None)
    if not file_name:
        raise DataLoadError("Nama file tidak ditemukan.")

    return str(file_name)


def _get_extension(uploaded_file: Any) -> str:
    file_name = _get_file_name(uploaded_file)
    extension = Path(file_name).suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise DataLoadError("Format file tidak didukung. Gunakan CSV, XLS, atau XLSX.")

    return extension


def _rewind(uploaded_file: Any) -> None:
    if hasattr(uploaded_file, "seek"):
        uploaded_file.seek(0)


def _read_csv(uploaded_file: Any) -> pd.DataFrame:
    _rewind(uploaded_file)
    try:
        return pd.read_csv(uploaded_file)
    except UnicodeDecodeError:
        _rewind(uploaded_file)
        return pd.read_csv(uploaded_file, encoding="latin1")


def _read_excel(uploaded_file: Any) -> pd.DataFrame:
    _rewind(uploaded_file)
    return pd.read_excel(uploaded_file)


def _validate_loaded_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    if dataframe is None:
        raise DataLoadError("Dataset tidak berhasil dibaca.")

    if dataframe.empty and len(dataframe.columns) == 0:
        raise DataLoadError("Dataset kosong atau tidak memiliki kolom.")

    dataframe.columns = [str(column) for column in dataframe.columns]
    return dataframe


def load_data(uploaded_file: Any) -> pd.DataFrame | None:
    """Read uploaded CSV/XLS/XLSX data and return a raw DataFrame."""
    if uploaded_file is None:
        return None

    extension = _get_extension(uploaded_file)

    try:
        if extension == ".csv":
            dataframe = _read_csv(uploaded_file)
        else:
            dataframe = _read_excel(uploaded_file)
    except pd.errors.EmptyDataError as exc:
        raise DataLoadError("File kosong atau tidak memiliki data yang dapat dibaca.") from exc
    except ImportError as exc:
        raise DataLoadError("Library pembaca Excel belum tersedia. Periksa requirements.txt.") from exc
    except ValueError as exc:
        raise DataLoadError(f"Dataset tidak dapat dibaca: {exc}") from exc
    except Exception as exc:
        raise DataLoadError("Dataset tidak dapat dibaca. Pastikan format dan isi file benar.") from exc

    return _validate_loaded_dataframe(dataframe)


def get_file_signature(uploaded_file: Any) -> str | None:
    """Build a stable signature for the current uploaded file."""
    if uploaded_file is None:
        return None

    file_name = _get_file_name(uploaded_file)
    size = getattr(uploaded_file, "size", None)
    if size is None and hasattr(uploaded_file, "getbuffer"):
        size = len(uploaded_file.getbuffer())

    return f"{file_name}:{size}"


def detect_dataset_shape(dataframe: pd.DataFrame) -> str:
    """Return a lightweight dataset-shape label based on raw columns."""
    normalized_columns = {str(column).strip().lower() for column in dataframe.columns}

    if {"tahun", "jumlah_pendaftar"}.issubset(normalized_columns):
        return "Tahunan agregat"

    if {"periode", "jumlah_pendaftar"}.issubset(normalized_columns):
        return "Bulanan agregat"

    if {"tanggal_daftar", "nama", "prodi"}.issubset(normalized_columns):
        return "Mentah per pendaftar"

    if "tahun" in normalized_columns:
        return "Kemungkinan data tahunan"

    if normalized_columns.intersection({"periode", "bulan", "tanggal", "tanggal_daftar"}):
        return "Kemungkinan data bulanan atau tanggal"

    return "Belum teridentifikasi"


def build_file_metadata(uploaded_file: Any, dataframe: pd.DataFrame) -> LoadedFileMetadata:
    """Collect file and dataframe metadata for the raw preview page."""
    file_name = _get_file_name(uploaded_file)
    extension = _get_extension(uploaded_file)
    size = getattr(uploaded_file, "size", None)
    if size is None and hasattr(uploaded_file, "getbuffer"):
        size = len(uploaded_file.getbuffer())

    return LoadedFileMetadata(
        file_name=file_name,
        extension=extension.lstrip(".").upper(),
        file_size_bytes=size,
        row_count=len(dataframe),
        column_count=len(dataframe.columns),
        columns=[str(column) for column in dataframe.columns],
        dtypes={str(column): str(dtype) for column, dtype in dataframe.dtypes.items()},
        dataset_shape=detect_dataset_shape(dataframe),
    )


def summarize_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Return a column-level summary for the raw dataset preview."""
    row_count = len(dataframe)
    rows: list[dict[str, Any]] = []
    for column in dataframe.columns:
        missing_count = int(dataframe[column].isna().sum())
        non_null_count = int(dataframe[column].notna().sum())
        missing_percentage = 0.0 if row_count == 0 else round((missing_count / row_count) * 100, 2)
        sample_values = dataframe[column].dropna().head(3).astype(str).tolist()
        rows.append(
            {
                "Kolom": str(column),
                "Tipe Data": str(dataframe[column].dtype),
                "Non Null": non_null_count,
                "Missing": missing_count,
                "Missing (%)": missing_percentage,
                "Contoh Nilai": ", ".join(sample_values) if sample_values else "-",
            }
        )

    return pd.DataFrame(rows)


def metadata_to_dict(metadata: LoadedFileMetadata) -> dict[str, Any]:
    """Convert metadata dataclass into plain session-state data."""
    return {
        "file_name": metadata.file_name,
        "extension": metadata.extension,
        "file_size_bytes": metadata.file_size_bytes,
        "row_count": metadata.row_count,
        "column_count": metadata.column_count,
        "columns": metadata.columns,
        "dtypes": metadata.dtypes,
        "dataset_shape": metadata.dataset_shape,
    }
