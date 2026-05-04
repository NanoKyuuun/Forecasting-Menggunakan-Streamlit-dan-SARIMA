"""Analisis Time Series page for PRD-05."""

from __future__ import annotations

from typing import Any

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.analysis import AdfResult, AnalysisResult, analyze_time_series
from src.interpretation import interpret_analysis


def _render_input_state(series: Any) -> bool:
    if series is not None and hasattr(series, "__len__") and len(series) > 0:
        return True

    st.info("Time series final belum tersedia.")
    st.write("Selesaikan halaman Data Transformation terlebih dahulu sampai `ts_series` berhasil dibuat.")
    return False


def _run_analysis(series: pd.Series) -> AnalysisResult:
    result = analyze_time_series(series, st.session_state.get("freq", "Tahunan"))
    st.session_state["analysis_report"] = result
    st.session_state["descriptive_stats"] = result.stats_df
    st.session_state["rolling_df"] = result.rolling_df
    st.session_state["correlation_df"] = result.correlation_df
    st.session_state["adf_result"] = result.adf_result
    return result


def _format_number(value: Any) -> str:
    if value is None or pd.isna(value):
        return "-"

    if isinstance(value, (int, float)):
        return f"{value:,.4f}"

    return str(value)


def _render_historical_chart(result: AnalysisResult) -> None:
    st.subheader("Grafik Historis")
    chart_df = result.series.reset_index()
    chart_df.columns = ["periode", "nilai"]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=chart_df["periode"],
            y=chart_df["nilai"],
            mode="lines+markers",
            name="Aktual",
            line={"color": "#2563eb", "width": 2},
        )
    )
    fig.update_layout(
        height=420,
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
        xaxis_title="Periode",
        yaxis_title="Nilai",
        hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_stats(result: AnalysisResult) -> None:
    st.subheader("Statistik Deskriptif")
    stats_df = result.stats_df.copy()
    stats_df["Nilai"] = stats_df["Nilai"].map(_format_number)
    st.dataframe(stats_df, use_container_width=True, hide_index=True)


def _render_rolling(result: AnalysisResult) -> None:
    st.subheader("Rolling Mean dan Rolling Std")
    st.caption(f"Window rolling yang digunakan: {result.rolling_window} periode.")
    st.dataframe(result.rolling_df, use_container_width=True, hide_index=True)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=result.rolling_df["periode"],
            y=result.rolling_df["aktual"],
            mode="lines+markers",
            name="Aktual",
            line={"color": "#2563eb", "width": 2},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=result.rolling_df["periode"],
            y=result.rolling_df["rolling_mean"],
            mode="lines",
            name="Rolling Mean",
            line={"color": "#16a34a", "width": 2},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=result.rolling_df["periode"],
            y=result.rolling_df["rolling_std"],
            mode="lines",
            name="Rolling Std",
            line={"color": "#dc2626", "width": 2, "dash": "dot"},
        )
    )
    fig.update_layout(
        height=420,
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
        xaxis_title="Periode",
        yaxis_title="Nilai",
        hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_decomposition(result: AnalysisResult) -> None:
    st.subheader("Dekomposisi Musiman")
    if result.decomposition_df is None:
        st.info("Dekomposisi musiman belum dijalankan untuk kondisi data saat ini.")
        return

    st.dataframe(result.decomposition_df, use_container_width=True, hide_index=True)
    fig = go.Figure()
    for column, color in [
        ("observed", "#2563eb"),
        ("trend", "#16a34a"),
        ("seasonal", "#f59e0b"),
        ("resid", "#64748b"),
    ]:
        fig.add_trace(
            go.Scatter(
                x=result.decomposition_df["periode"],
                y=result.decomposition_df[column],
                mode="lines",
                name=column,
                line={"color": color, "width": 2},
            )
        )
    fig.update_layout(
        height=440,
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
        xaxis_title="Periode",
        yaxis_title="Komponen",
        hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_adf_result(adf_result: AdfResult) -> None:
    st.subheader("ADF Test")
    if not adf_result.success:
        st.warning(adf_result.message)
        return

    columns = st.columns(4)
    columns[0].metric("ADF Statistic", _format_number(adf_result.adf_statistic))
    columns[1].metric("p-value", _format_number(adf_result.p_value))
    columns[2].metric("Used Lag", adf_result.used_lag)
    columns[3].metric("N Obs", adf_result.n_obs)

    if adf_result.is_stationary:
        st.success("p-value < 0.05, data dapat dianggap stasioner.")
    else:
        st.warning("p-value >= 0.05, data belum stasioner.")

    critical_values = adf_result.critical_values or {}
    critical_df = pd.DataFrame(
        [{"Level": key, "Critical Value": value} for key, value in critical_values.items()]
    )
    st.dataframe(critical_df, use_container_width=True, hide_index=True)


def _render_acf_pacf(result: AnalysisResult) -> None:
    st.subheader("ACF dan PACF")
    if result.correlation_df.empty:
        st.warning("Jumlah observasi terlalu sedikit untuk membaca ACF/PACF secara kuat.")
        return

    st.dataframe(result.correlation_df, use_container_width=True, hide_index=True)
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=result.correlation_df["Lag"],
            y=result.correlation_df["ACF"],
            name="ACF",
            marker_color="#2563eb",
        )
    )
    fig.add_trace(
        go.Bar(
            x=result.correlation_df["Lag"],
            y=result.correlation_df["PACF"],
            name="PACF",
            marker_color="#16a34a",
        )
    )
    fig.update_layout(
        barmode="group",
        height=420,
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
        xaxis_title="Lag",
        yaxis_title="Korelasi",
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_interpretation(result: AnalysisResult) -> None:
    st.subheader("Interpretasi Otomatis")
    for warning in result.warnings:
        st.warning(warning)

    for item in interpret_analysis(result, st.session_state.get("freq", "Tahunan")):
        st.write(f"- {item}")

    with st.expander("Catatan teknis analisis"):
        for note in result.notes:
            st.write(f"- {note}")


def render_analysis_page() -> None:
    """Render the PRD-05 time-series analysis page."""
    st.title("Analisis Time Series")
    st.caption("Tahap PRD-05: grafik historis, statistik, rolling, dekomposisi, ADF, ACF, dan PACF.")

    series = st.session_state.get("ts_series")
    if not _render_input_state(series):
        return

    result = _run_analysis(series)
    _render_interpretation(result)
    _render_historical_chart(result)

    left_column, right_column = st.columns([1, 1], gap="large")
    with left_column:
        _render_stats(result)
        _render_adf_result(result.adf_result)

    with right_column:
        _render_rolling(result)

    _render_decomposition(result)
    _render_acf_pacf(result)
