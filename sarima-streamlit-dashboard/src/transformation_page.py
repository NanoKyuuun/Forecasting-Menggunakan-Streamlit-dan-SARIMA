"""Data Transformation page for PRD-04."""

from __future__ import annotations

from typing import Any

import streamlit as st

from src.transformation import TransformationResult, transform_to_timeseries


def _get_selected_columns() -> dict[str, str | None]:
    report = st.session_state.get("preprocessing_report")
    if report is not None and hasattr(report, "selected_columns"):
        return report.selected_columns

    return {
        "time": st.session_state.get("column_time"),
        "target": st.session_state.get("column_target"),
        "category": st.session_state.get("column_prodi"),
    }


def _run_transformation(clean_df: Any) -> TransformationResult:
    selected_columns = _get_selected_columns()
    result = transform_to_timeseries(
        clean_df,
        selected_columns.get("time"),
        selected_columns.get("target"),
        category_col=selected_columns.get("category"),
        selected_category=st.session_state.get("selected_prodi", "Semua prodi"),
        frequency_label=st.session_state.get("freq", "Tahunan"),
        missing_period_strategy=st.session_state.get("missing_period_strategy", "Isi 0"),
    )
    st.session_state["transformation_report"] = result

    if result.errors:
        st.session_state["ts_series"] = None
        st.session_state["time_series_df"] = None
        st.session_state["aggregated_df"] = None
    else:
        st.session_state["ts_series"] = result.series
        st.session_state["time_series_df"] = result.time_series_df
        st.session_state["aggregated_df"] = result.aggregated_df
        st.session_state["freq"] = result.frequency_label
        st.session_state["freq_code"] = result.frequency_code
        st.session_state["data_mode"] = result.data_mode

    analysis_keys = [
        "analysis_report",
        "descriptive_stats",
        "rolling_df",
        "correlation_df",
        "adf_result",
        "train",
        "test",
        "model_fit",
        "modeling_report",
        "evaluation_report",
        "model_aic",
        "model_bic",
        "metrics",
        "prediction_df",
        "residual_df",
        "residual_acf_df",
        "ljung_box_df",
        "forecast_df",
    ]
    for key in analysis_keys:
        st.session_state[key] = None

    return result


def _format_period(value: Any) -> str:
    if value is None:
        return "-"

    if hasattr(value, "strftime"):
        return value.strftime("%Y-%m-%d")

    return str(value)


def _render_input_state(clean_df: Any) -> bool:
    if clean_df is not None:
        return True

    st.info("Data bersih belum tersedia.")
    st.write("Selesaikan halaman Data & Preprocessing terlebih dahulu sampai `clean_df` berhasil dibuat.")
    return False


def _render_configuration(result: TransformationResult) -> None:
    st.subheader("Konfigurasi Transformasi")
    columns = st.columns(4)
    columns[0].metric("Mode Data", result.data_mode)
    columns[1].metric("Kode Frekuensi", result.frequency_code)
    columns[2].metric("Filter Prodi", result.selected_category)
    columns[3].metric("Missing Period", result.missing_period_strategy)


def _render_errors(result: TransformationResult) -> bool:
    if not result.errors:
        return False

    for error in result.errors:
        st.error(error)
    return True


def _render_summary(result: TransformationResult) -> None:
    st.subheader("Ringkasan Time Series")
    columns = st.columns(5)
    columns[0].metric("Periode Awal", _format_period(result.period_start))
    columns[1].metric("Periode Akhir", _format_period(result.period_end))
    columns[2].metric("Observasi Terisi", result.observation_count)
    columns[3].metric("Total Periode", len(result.series))
    columns[4].metric("Baris Agregasi", len(result.aggregated_df))

    for warning in result.warnings:
        st.warning(warning)


def _render_aggregation(result: TransformationResult) -> None:
    st.subheader("Data Hasil Agregasi")
    st.dataframe(result.aggregated_df, use_container_width=True, hide_index=True)


def _render_timeseries(result: TransformationResult) -> None:
    st.subheader("Time Series Final")
    st.dataframe(result.time_series_df, use_container_width=True, hide_index=True)

    if result.series.dropna().empty:
        st.warning("Time series belum memiliki nilai terisi untuk divisualisasikan.")
    else:
        st.line_chart(result.series, use_container_width=True)

    csv_data = result.time_series_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Time Series CSV",
        data=csv_data,
        file_name="time_series_final.csv",
        mime="text/csv",
    )


def _render_notes(result: TransformationResult) -> None:
    with st.expander("Catatan Transformasi"):
        if not result.notes:
            st.write("- Tidak ada catatan transformasi.")
        for note in result.notes:
            st.write(f"- {note}")


def render_transformation_page() -> None:
    """Render the PRD-04 data-transformation page."""
    st.title("Data Transformation")
    st.caption("Tahap PRD-04: agregasi data bersih menjadi time series final.")

    clean_df = st.session_state.get("clean_df")
    if not _render_input_state(clean_df):
        return

    result = _run_transformation(clean_df)
    _render_configuration(result)
    if _render_errors(result):
        return

    _render_summary(result)
    _render_aggregation(result)
    _render_timeseries(result)
    _render_notes(result)
