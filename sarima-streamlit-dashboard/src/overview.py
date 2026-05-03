"""Overview page for the SARIMA forecasting dashboard."""

from __future__ import annotations

from typing import Any

import streamlit as st

from src.state import has_time_series_data


def _safe_len(value: Any) -> int:
    if value is None or not hasattr(value, "__len__"):
        return 0
    return len(value)


def _format_metric_value(value: Any, fallback: str = "-") -> str:
    if value is None:
        return fallback
    return str(value)


def _get_last_actual() -> Any:
    series = st.session_state.get("ts_series")
    if series is None or not hasattr(series, "iloc") or len(series) == 0:
        return None

    return series.iloc[-1]


def _get_time_series_period(boundary: str) -> Any:
    series = st.session_state.get("ts_series")
    if series is None or not hasattr(series, "index") or len(series) == 0:
        return None

    if boundary == "start":
        return series.index[0]
    return series.index[-1]


def _get_next_forecast() -> Any:
    forecast_df = st.session_state.get("forecast_df")
    if forecast_df is None or not hasattr(forecast_df, "empty") or forecast_df.empty:
        return None

    for column in ("forecast", "Forecast", "prediksi", "Prediksi"):
        if column in forecast_df.columns:
            return forecast_df.iloc[0][column]
    return None


def _get_mape() -> Any:
    metrics = st.session_state.get("metrics")
    if not isinstance(metrics, dict):
        return None

    return metrics.get("MAPE") or metrics.get("mape")


def _render_metric_cards() -> None:
    series = st.session_state.get("ts_series")
    columns = st.columns(4)
    columns[0].metric("Total Observasi", _safe_len(series))
    columns[1].metric("Periode Awal", _format_metric_value(_get_time_series_period("start")))
    columns[2].metric("Periode Akhir", _format_metric_value(_get_time_series_period("end")))
    columns[3].metric("Mode Data", st.session_state.get("data_mode", "Belum dipilih"))

    columns = st.columns(3)
    columns[0].metric("Aktual Terakhir", _format_metric_value(_get_last_actual()))
    columns[1].metric("Forecast Berikutnya", _format_metric_value(_get_next_forecast()))
    columns[2].metric("MAPE", _format_metric_value(_get_mape()))


def _render_dataset_summary() -> None:
    raw_df = st.session_state.get("raw_df")
    uploaded_file_name = st.session_state.get("uploaded_file_name")

    st.subheader("Informasi Dataset")
    if raw_df is None:
        st.info("Belum ada dataset yang diproses. Upload dataset melalui sidebar untuk memulai alur penelitian.")
        if uploaded_file_name:
            st.caption(f"File sudah dipilih: {uploaded_file_name}. Proses pembacaan data masuk tahap Data Loader.")
        return

    st.write(f"Nama file: {uploaded_file_name or '-'}")
    st.write(f"Jumlah baris: {len(raw_df)}")
    st.write(f"Jumlah kolom: {len(raw_df.columns)}")
    st.dataframe(raw_df.head(10), use_container_width=True)


def _render_methodology_warning() -> None:
    data_mode = st.session_state.get("data_mode")
    series = st.session_state.get("ts_series")
    observations = _safe_len(series)

    st.subheader("Catatan Metodologis")
    if data_mode == "Tahunan" and 0 < observations < 10:
        st.warning(
            "Data tahunan yang tersedia memiliki jumlah observasi terbatas. "
            "Model digunakan untuk analisis tren dan forecast awal. "
            "Untuk analisis SARIMA musiman yang lebih kuat, diperlukan data bulanan atau mingguan."
        )
        return

    if data_mode == "Tahunan":
        st.info(
            "Mode tahunan tidak memaksakan komponen musiman. "
            "Seasonal order default disiapkan sebagai (0, 0, 0, 0)."
        )
        return

    if data_mode == "Bulanan":
        st.info(
            "Mode bulanan dapat memakai seasonal period 12 jika data bulanan aktual tersedia dan jumlah observasi cukup."
        )
        return

    st.info("Pilih frekuensi data sesuai bentuk dataset. Dashboard tidak membuat data bulanan palsu dari data tahunan.")


def _render_historical_snapshot() -> None:
    st.subheader("Grafik Historis Ringkas")
    if not has_time_series_data():
        st.info("Grafik historis akan tampil setelah data selesai ditransformasi menjadi time series.")
        return

    series = st.session_state["ts_series"]
    st.line_chart(series, use_container_width=True)


def _render_forecast_snapshot() -> None:
    st.subheader("Hasil Forecast Singkat")
    forecast_df = st.session_state.get("forecast_df")
    if forecast_df is None:
        st.info("Hasil forecast akan tampil setelah model selesai dijalankan.")
        return

    st.dataframe(forecast_df.head(5), use_container_width=True)


def render_overview() -> None:
    """Render the research overview page."""
    st.title("Dashboard Forecasting Tren Minat Jurusan Mahasiswa Baru")
    st.caption("Aplikasi penelitian berbasis Streamlit dan SARIMA/SARIMAX untuk analisis pendaftaran mahasiswa baru.")

    _render_metric_cards()
    _render_methodology_warning()

    left_column, right_column = st.columns([1.1, 0.9], gap="large")
    with left_column:
        _render_dataset_summary()
        _render_historical_snapshot()

    with right_column:
        _render_forecast_snapshot()
        st.subheader("Ringkasan Alur")
        st.write(
            "Upload dataset, validasi data, transformasi time series, analisis, modeling, evaluasi, forecasting, "
            "dan kesimpulan disiapkan sebagai alur bertahap sesuai PRD."
        )
