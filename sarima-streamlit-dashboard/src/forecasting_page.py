"""Forecasting & Interpretasi page for PRD-08."""

from __future__ import annotations

from typing import Any

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.forecasting import ForecastingResult, generate_forecast
from src.interpretation import interpret_forecast
from src.modeling import ModelingResult
from src.ui_components import render_not_ready_message, render_page_header, render_recommended_action
from src.workflow import PAGE_FORECASTING


def _format_number(value: Any) -> str:
    if value is None or pd.isna(value):
        return "-"
    if isinstance(value, (int, float)):
        return f"{value:,.4f}"
    return str(value)


def _get_modeling_result() -> ModelingResult | None:
    result = st.session_state.get("modeling_report")
    if isinstance(result, ModelingResult) and not result.errors:
        return result
    return None


def _render_input_state() -> bool:
    series = st.session_state.get("ts_series")
    modeling_result = _get_modeling_result()

    if series is not None and hasattr(series, "__len__") and len(series) > 0 and modeling_result is not None:
        if st.session_state.get("evaluation_report") is None:
            st.warning("Evaluasi model belum dijalankan pada sesi ini. Forecast tetap bisa dibuat setelah model valid.")
        return True

    render_not_ready_message(
        PAGE_FORECASTING,
        "Selesaikan Transformasi Data dan Pemodelan SARIMA terlebih dahulu agar forecast dapat dibuat.",
    )
    return False


def _save_forecasting_result(result: ForecastingResult) -> None:
    st.session_state["forecasting_report"] = result
    st.session_state["final_model_fit"] = result.final_model_fit
    st.session_state["forecast_df"] = None if result.forecast_df.empty else result.forecast_df


def _run_forecasting() -> ForecastingResult:
    modeling_result = _get_modeling_result()
    result = generate_forecast(
        st.session_state.get("ts_series"),
        None if modeling_result is None else modeling_result.order,
        None if modeling_result is None else modeling_result.seasonal_order,
        int(st.session_state.get("forecast_horizon", 3)),
        st.session_state.get("freq_code", "YS"),
    )
    _save_forecasting_result(result)
    return result


def _render_errors(result: ForecastingResult) -> bool:
    if not result.errors:
        return False

    for error in result.errors:
        st.error(error)
    return True


def _render_forecast_summary(result: ForecastingResult) -> None:
    st.subheader("Ringkasan Forecast")
    columns = st.columns(4)
    columns[0].metric("Horizon", result.horizon)
    columns[1].metric("Frekuensi", result.freq_code)
    columns[2].metric("Order", str(result.order or "-"))
    columns[3].metric("Seasonal Order", str(result.seasonal_order or "-"))

    if not result.forecast_df.empty:
        first_forecast = result.forecast_df.iloc[0]["forecast"]
        last_forecast = result.forecast_df.iloc[-1]["forecast"]
        trend = result.forecast_df.iloc[-1]["tren"]
        columns = st.columns(3)
        columns[0].metric("Forecast Pertama", _format_number(first_forecast))
        columns[1].metric("Forecast Terakhir", _format_number(last_forecast))
        columns[2].metric("Tren Akhir", trend)

    for warning in result.warnings:
        st.warning(warning)
    for note in result.notes:
        st.write(f"- {note}")


def _render_forecast_chart(result: ForecastingResult) -> None:
    st.subheader("Grafik Forecast")
    series = st.session_state.get("ts_series")
    if series is None or result.forecast_df.empty:
        st.info("Grafik forecast belum tersedia.")
        return

    history = pd.Series(series).dropna()
    forecast_df = result.forecast_df
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=history.index,
            y=history.values,
            mode="lines+markers",
            name="Historis",
            line={"color": "#2563eb", "width": 2},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=forecast_df["periode"],
            y=forecast_df["forecast"],
            mode="lines+markers",
            name="Forecast",
            line={"color": "#f97316", "width": 3},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=forecast_df["periode"],
            y=forecast_df["upper_bound"],
            mode="lines",
            name="Upper Bound",
            line={"color": "rgba(249, 115, 22, 0.25)", "width": 1},
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=forecast_df["periode"],
            y=forecast_df["lower_bound"],
            mode="lines",
            name="Confidence Interval",
            line={"color": "rgba(249, 115, 22, 0.25)", "width": 1},
            fill="tonexty",
            fillcolor="rgba(249, 115, 22, 0.18)",
        )
    )
    fig.update_layout(
        height=460,
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
        xaxis_title="Periode",
        yaxis_title="Nilai",
        hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_forecast_table(result: ForecastingResult) -> None:
    st.subheader("Tabel Forecast")
    if result.forecast_df.empty:
        st.info("Tabel forecast belum tersedia.")
        return

    display_df = result.forecast_df.copy()
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    csv_data = display_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "Unduh Forecast CSV",
        data=csv_data,
        file_name="forecast_sarima.csv",
        mime="text/csv",
        use_container_width=True,
    )


def _render_automatic_interpretation(result: ForecastingResult) -> None:
    st.subheader("Interpretasi Otomatis")
    for item in interpret_forecast(result.forecast_df, st.session_state.get("data_mode", "Tahunan")):
        st.write(f"- {item}")


def render_forecasting_page() -> None:
    """Render the PRD-08 forecasting page."""
    render_page_header(
        PAGE_FORECASTING,
        "Final model, horizon forecast, confidence interval, tabel, grafik, dan CSV.",
    )

    if not _render_input_state():
        return

    with st.spinner("Melatih final model dan membuat forecast..."):
        result = _run_forecasting()

    if _render_errors(result):
        return

    _render_forecast_summary(result)
    _render_automatic_interpretation(result)
    _render_forecast_chart(result)
    _render_forecast_table(result)
    render_recommended_action(PAGE_FORECASTING)
