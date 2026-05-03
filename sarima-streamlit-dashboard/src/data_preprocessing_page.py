"""Data & Preprocessing page focused on raw data loading for PRD-02."""

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


def render_data_preprocessing_page() -> None:
    """Render raw data loading and preview UI."""
    st.title("Data & Preprocessing")
    st.caption("Tahap PRD-02: load dataset CSV/XLS/XLSX dan preview data mentah.")

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

    st.info(
        "Tahap berikutnya adalah validasi kolom, missing value, duplikasi, outlier, dan cleaning data pada issue PRD-03."
    )
