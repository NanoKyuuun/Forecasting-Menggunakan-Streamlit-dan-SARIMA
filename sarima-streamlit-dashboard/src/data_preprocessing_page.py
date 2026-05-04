"""Data & Preprocessing page for PRD-02 and PRD-03."""

from __future__ import annotations

from typing import Any

import streamlit as st

from src.data_loader import (
    DataLoadError,
    build_file_metadata,
    get_file_signature,
    load_data,
    metadata_to_dict,
    summarize_columns,
)
from src.preprocessing import (
    TARGET_MISSING_DROP,
    TARGET_MISSING_FILL_ZERO,
    PreprocessingResult,
    preprocess_data,
)
from src.state import reset_after_raw_data_change


def _format_file_size(size_bytes: int | None) -> str:
    if size_bytes is None:
        return "-"

    if size_bytes < 1024:
        return f"{size_bytes} B"

    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"

    return f"{size_bytes / (1024 * 1024):.1f} MB"


def _load_uploaded_file_if_needed() -> tuple[Any, bool]:
    uploaded_file = st.session_state.get("uploaded_file")
    if uploaded_file is None:
        return None, False

    try:
        signature = get_file_signature(uploaded_file)
    except DataLoadError as exc:
        st.session_state["raw_df"] = None
        st.session_state["data_load_error"] = str(exc)
        return None, False

    if (
        st.session_state.get("uploaded_file_signature") == signature
        and st.session_state.get("raw_df") is not None
    ):
        return st.session_state["raw_df"], False

    try:
        dataframe = load_data(uploaded_file)
        if dataframe is None:
            return None, False
    except DataLoadError as exc:
        st.session_state["raw_df"] = None
        st.session_state["data_metadata"] = None
        st.session_state["dataset_shape"] = None
        st.session_state["data_load_error"] = str(exc)
        st.session_state["uploaded_file_signature"] = signature
        return None, False

    metadata = build_file_metadata(uploaded_file, dataframe)
    st.session_state["raw_df"] = dataframe
    st.session_state["data_metadata"] = metadata_to_dict(metadata)
    st.session_state["dataset_shape"] = metadata.dataset_shape
    st.session_state["data_load_error"] = None
    st.session_state["uploaded_file_signature"] = signature
    reset_after_raw_data_change()
    return dataframe, True


def _render_upload_state() -> None:
    st.info("Upload dataset melalui sidebar. Format yang didukung: CSV, XLS, dan XLSX.")
    st.write(
        "Dataset dapat berupa rekap tahunan, rekap bulanan, atau data mentah per pendaftar. "
        "Tahap ini hanya membaca dan menampilkan data mentah tanpa mengubah isi kolom."
    )


def _render_metrics(metadata: dict[str, Any]) -> None:
    columns = st.columns(4)
    columns[0].metric("Jumlah Baris", metadata["row_count"])
    columns[1].metric("Jumlah Kolom", metadata["column_count"])
    columns[2].metric("Format File", metadata["extension"])
    columns[3].metric("Bentuk Dataset", metadata["dataset_shape"])

    columns = st.columns(2)
    columns[0].write(f"Nama file: `{metadata['file_name']}`")
    columns[1].write(f"Ukuran file: `{_format_file_size(metadata['file_size_bytes'])}`")


def _render_preview(dataframe: Any) -> None:
    st.subheader("Preview Data Mentah")
    preview_count = st.slider("Jumlah baris preview", min_value=5, max_value=10, value=10)
    st.dataframe(dataframe.head(preview_count), use_container_width=True)


def _render_columns(dataframe: Any, metadata: dict[str, Any]) -> None:
    st.subheader("Daftar Kolom dan Tipe Data")
    st.dataframe(summarize_columns(dataframe), use_container_width=True, hide_index=True)

    with st.expander("Daftar nama kolom"):
        for column in metadata["columns"]:
            st.write(f"- `{column}`")


def _render_preprocessing_controls() -> str:
    st.subheader("Validasi dan Cleaning Data")
    current_action = st.session_state.get("target_missing_action", TARGET_MISSING_FILL_ZERO)
    options = [TARGET_MISSING_FILL_ZERO, TARGET_MISSING_DROP]
    index = options.index(current_action) if current_action in options else 0
    target_missing_action = st.radio(
        "Tindakan untuk target kosong/tidak numerik",
        options,
        index=index,
        horizontal=True,
    )
    st.session_state["target_missing_action"] = target_missing_action
    return target_missing_action


def _run_preprocessing(dataframe: Any, target_missing_action: str) -> PreprocessingResult:
    result = preprocess_data(
        dataframe,
        st.session_state.get("column_time"),
        st.session_state.get("column_target"),
        st.session_state.get("column_prodi"),
        frequency=st.session_state.get("freq", "Tahunan"),
        target_missing_action=target_missing_action,
    )
    st.session_state["preprocessing_report"] = result
    downstream_keys = [
        "ts_series",
        "time_series_df",
        "aggregated_df",
        "transformation_report",
        "train",
        "test",
        "model_fit",
        "metrics",
        "forecast_df",
    ]
    for key in downstream_keys:
        st.session_state[key] = None

    if result.errors:
        st.session_state["clean_df"] = None
        st.session_state["processing_notes"] = []
    else:
        st.session_state["clean_df"] = result.clean_df
        st.session_state["processing_notes"] = result.notes

    return result


def _render_column_validation(result: PreprocessingResult) -> None:
    st.subheader("Validasi Kolom")
    selected_columns = result.selected_columns
    rows = [
        {
            "Kebutuhan": "Kolom waktu",
            "Kolom bersih": selected_columns.get("time") or "-",
            "Status": "Valid" if selected_columns.get("time") else "Belum valid",
        },
        {
            "Kebutuhan": "Kolom target",
            "Kolom bersih": selected_columns.get("target") or "-",
            "Status": "Valid" if selected_columns.get("target") else "Belum valid",
        },
        {
            "Kebutuhan": "Kolom prodi/jurusan",
            "Kolom bersih": selected_columns.get("category") or "-",
            "Status": "Opsional" if selected_columns.get("category") is None else "Valid",
        },
    ]
    st.dataframe(rows, use_container_width=True, hide_index=True)

    with st.expander("Mapping nama kolom setelah dibersihkan"):
        mapping_rows = [
            {"Kolom asli": original, "Kolom bersih": cleaned}
            for original, cleaned in result.column_map.items()
        ]
        st.dataframe(mapping_rows, use_container_width=True, hide_index=True)


def _render_preprocessing_errors(result: PreprocessingResult) -> bool:
    if not result.errors:
        return False

    for error in result.errors:
        st.error(error)
    st.warning("Pilih minimal kolom waktu dan kolom target melalui sidebar sebelum preprocessing dijalankan.")
    return True


def _render_missing_values(result: PreprocessingResult) -> None:
    st.subheader("Missing Value")
    st.dataframe(result.missing_summary, use_container_width=True, hide_index=True)


def _render_duplicates(result: PreprocessingResult) -> None:
    st.subheader("Duplikasi")
    columns = st.columns(4)
    columns[0].metric("Baris Awal", result.rows_before)
    columns[1].metric("Duplikasi Penuh", result.full_duplicate_count)
    columns[2].metric("Duplikasi Periode/Prodi", result.key_duplicate_count)
    columns[3].metric("Baris Bersih", result.rows_after)


def _format_bound(value: float | None) -> str:
    if value is None:
        return "-"
    return f"{value:,.2f}"


def _render_outliers(result: PreprocessingResult) -> None:
    st.subheader("Outlier")
    bounds = result.outlier_bounds
    columns = st.columns(5)
    columns[0].metric("Q1", _format_bound(bounds.q1))
    columns[1].metric("Q3", _format_bound(bounds.q3))
    columns[2].metric("IQR", _format_bound(bounds.iqr))
    columns[3].metric("Batas Bawah", _format_bound(bounds.lower))
    columns[4].metric("Batas Atas", _format_bound(bounds.upper))

    if result.outlier_df.empty:
        st.success("Tidak ada outlier target berdasarkan metode IQR.")
        return

    st.warning(f"{len(result.outlier_df)} baris ditandai sebagai outlier. Outlier tidak dihapus otomatis.")
    st.dataframe(result.outlier_df, use_container_width=True, hide_index=True)


def _render_clean_data(result: PreprocessingResult) -> None:
    st.subheader("Data Bersih")
    st.success('Data bersih tersimpan di `st.session_state["clean_df"]`.')
    st.dataframe(result.clean_df.head(20), use_container_width=True, hide_index=True)

    with st.expander("Catatan proses cleaning"):
        if not result.notes:
            st.write("- Tidak ada catatan cleaning.")
        for note in result.notes:
            st.write(f"- {note}")


def _render_preprocessing_result(result: PreprocessingResult) -> None:
    _render_column_validation(result)
    if _render_preprocessing_errors(result):
        return

    _render_missing_values(result)
    _render_duplicates(result)
    _render_outliers(result)
    _render_clean_data(result)


def render_data_preprocessing_page() -> None:
    """Render raw data loading and preview UI."""
    st.title("Data & Preprocessing")
    st.caption("Tahap PRD-03: validasi kolom, missing value, duplikasi, outlier, dan cleaning data.")

    dataframe, was_reloaded = _load_uploaded_file_if_needed()
    load_error = st.session_state.get("data_load_error")

    if load_error:
        st.error(load_error)
        st.warning("Periksa kembali format file dan pastikan dataset memiliki header kolom.")
        return

    if dataframe is None:
        _render_upload_state()
        return

    if was_reloaded:
        st.success("Dataset berhasil dibaca. Sidebar akan memakai kolom dataset ini untuk tahap berikutnya.")

    metadata = st.session_state.get("data_metadata")
    if not metadata:
        st.warning("Metadata dataset belum tersedia.")
        return

    _render_metrics(metadata)

    if metadata["row_count"] == 0:
        st.warning("Dataset memiliki kolom, tetapi belum memiliki baris data.")

    _render_preview(dataframe)
    _render_columns(dataframe, metadata)

    target_missing_action = _render_preprocessing_controls()
    result = _run_preprocessing(dataframe, target_missing_action)
    _render_preprocessing_result(result)
