"""Evaluasi Model page for PRD-07."""

from __future__ import annotations

from typing import Any

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.evaluation import EvaluationResult, evaluate_model
from src.interpretation import interpret_evaluation
from src.ui_components import render_not_ready_message, render_page_header, render_recommended_action
from src.workflow import PAGE_EVALUATION


def _format_number(value: Any) -> str:
    if value is None or pd.isna(value):
        return "-"
    if isinstance(value, (int, float)):
        return f"{value:,.4f}"
    return str(value)


def _render_input_state() -> bool:
    if st.session_state.get("model_fit") is not None and st.session_state.get("test") is not None:
        return True

    render_not_ready_message(
        PAGE_EVALUATION,
        "Selesaikan Pemodelan SARIMA terlebih dahulu sampai model dan data testing tersedia.",
    )
    return False


def _save_evaluation_result(result: EvaluationResult) -> None:
    st.session_state["evaluation_report"] = result
    st.session_state["metrics"] = result.metrics
    st.session_state["prediction_df"] = result.prediction_df
    st.session_state["residual_df"] = result.residual_df
    st.session_state["residual_acf_df"] = result.residual_acf_df
    st.session_state["ljung_box_df"] = result.ljung_box_df


def _run_evaluation() -> EvaluationResult:
    result = evaluate_model(st.session_state.get("model_fit"), st.session_state.get("test"))
    _save_evaluation_result(result)
    return result


def _render_errors(result: EvaluationResult) -> bool:
    if not result.errors:
        return False

    for error in result.errors:
        st.error(error)
    return True


def _render_metrics(result: EvaluationResult) -> None:
    st.subheader("Metrik Evaluasi")
    columns = st.columns(4)
    columns[0].metric("MAE", _format_number(result.metrics.get("MAE")))
    columns[1].metric("MSE", _format_number(result.metrics.get("MSE")))
    columns[2].metric("RMSE", _format_number(result.metrics.get("RMSE")))
    columns[3].metric("MAPE", _format_number(result.metrics.get("MAPE")))

    display_df = result.metrics_df.copy()
    display_df["Nilai"] = display_df["Nilai"].map(_format_number)
    st.dataframe(display_df, use_container_width=True, hide_index=True)


def _render_prediction_chart(result: EvaluationResult) -> None:
    st.subheader("Aktual vs Prediksi")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=result.prediction_df["periode"],
            y=result.prediction_df["aktual"],
            mode="lines+markers",
            name="Aktual",
            line={"color": "#2563eb", "width": 2},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=result.prediction_df["periode"],
            y=result.prediction_df["prediksi"],
            mode="lines+markers",
            name="Prediksi",
            line={"color": "#f97316", "width": 2, "dash": "dash"},
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
    st.dataframe(result.prediction_df, use_container_width=True, hide_index=True)


def _render_residual_plots(result: EvaluationResult) -> None:
    st.subheader("Residual")
    left_column, right_column = st.columns(2, gap="large")

    with left_column:
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=result.residual_df["periode"],
                y=result.residual_df["residual"],
                mode="lines+markers",
                name="Residual",
                line={"color": "#dc2626", "width": 2},
            )
        )
        fig.add_hline(y=0, line_dash="dot", line_color="#64748b")
        fig.update_layout(
            height=360,
            margin={"l": 20, "r": 20, "t": 20, "b": 20},
            xaxis_title="Periode",
            yaxis_title="Aktual - Prediksi",
            hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True)

    with right_column:
        fig = go.Figure()
        fig.add_trace(
            go.Histogram(
                x=result.residual_df["residual"],
                name="Residual",
                marker_color="#0f766e",
            )
        )
        fig.update_layout(
            height=360,
            margin={"l": 20, "r": 20, "t": 20, "b": 20},
            xaxis_title="Residual",
            yaxis_title="Frekuensi",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(result.residual_df, use_container_width=True, hide_index=True)


def _render_residual_diagnostics(result: EvaluationResult) -> None:
    st.subheader("Diagnostic Checking Residual")
    for note in result.notes:
        st.write(f"- {note}")

    left_column, right_column = st.columns(2, gap="large")
    with left_column:
        st.write("Residual ACF")
        if result.residual_acf_df.empty:
            st.info("Residual ACF dilewati karena jumlah residual terlalu sedikit atau residual konstan.")
        else:
            fig = go.Figure()
            fig.add_trace(
                go.Bar(
                    x=result.residual_acf_df["Lag"],
                    y=result.residual_acf_df["ACF"],
                    name="ACF Residual",
                    marker_color="#2563eb",
                )
            )
            fig.update_layout(
                height=340,
                margin={"l": 20, "r": 20, "t": 20, "b": 20},
                xaxis_title="Lag",
                yaxis_title="ACF",
            )
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(result.residual_acf_df, use_container_width=True, hide_index=True)

    with right_column:
        st.write("Ljung-Box")
        if result.ljung_box_df.empty:
            st.info("Ljung-Box dilewati karena jumlah residual belum cukup untuk pengujian yang kuat.")
        else:
            st.dataframe(result.ljung_box_df, use_container_width=True, hide_index=True)
            min_p_value = result.ljung_box_df["p-value"].min()
            if min_p_value >= 0.05:
                st.success("p-value >= 0.05 pada lag yang diuji; autokorelasi residual tidak terindikasi kuat.")
            else:
                st.warning("Ada p-value < 0.05; residual masih mengindikasikan autokorelasi pada lag tertentu.")


def _render_interpretation(result: EvaluationResult) -> None:
    st.subheader("Interpretasi Otomatis")
    for warning in result.warnings:
        st.warning(warning)

    for item in interpret_evaluation(result):
        st.write(f"- {item}")


def render_evaluation_page() -> None:
    """Render the PRD-07 evaluation page."""
    render_page_header(
        PAGE_EVALUATION,
        "Prediksi data testing, metrik error, residual, ACF residual, dan Ljung-Box.",
    )

    if not _render_input_state():
        return

    with st.spinner("Mengevaluasi model terhadap data testing..."):
        result = _run_evaluation()

    if _render_errors(result):
        return

    _render_interpretation(result)
    _render_metrics(result)
    _render_prediction_chart(result)
    _render_residual_plots(result)
    _render_residual_diagnostics(result)
    render_recommended_action(PAGE_EVALUATION)
