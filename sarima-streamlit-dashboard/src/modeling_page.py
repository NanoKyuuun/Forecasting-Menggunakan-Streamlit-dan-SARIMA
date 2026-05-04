"""Pemodelan SARIMA page for PRD-06."""

from __future__ import annotations

from typing import Any

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.modeling import ModelingResult, fit_model


def _render_input_state(series: Any) -> bool:
    if series is not None and hasattr(series, "__len__") and len(series) > 0:
        return True

    st.info("Time series final belum tersedia.")
    st.write("Selesaikan halaman Data Transformation terlebih dahulu sampai `ts_series` berhasil dibuat.")
    return False


def _format_number(value: Any) -> str:
    if value is None or pd.isna(value):
        return "-"

    if isinstance(value, (int, float)):
        return f"{value:,.4f}"

    return str(value)


def _save_modeling_result(result: ModelingResult) -> None:
    st.session_state["modeling_report"] = result
    st.session_state["train"] = result.train
    st.session_state["test"] = result.test

    if result.errors:
        st.session_state["model_fit"] = None
        st.session_state["model_aic"] = None
        st.session_state["model_bic"] = None
    else:
        st.session_state["model_fit"] = result.model_fit
        st.session_state["model_aic"] = result.aic
        st.session_state["model_bic"] = result.bic

    downstream_keys = ["metrics", "forecast_df"]
    for key in downstream_keys:
        st.session_state[key] = None


def _run_modeling() -> ModelingResult:
    result = fit_model(
        st.session_state.get("ts_series"),
        st.session_state.get("freq", "Tahunan"),
        st.session_state.get("model_config", {}),
    )
    _save_modeling_result(result)
    st.session_state["model_requested"] = False
    return result


def _get_current_result() -> ModelingResult | None:
    result = st.session_state.get("modeling_report")
    if isinstance(result, ModelingResult):
        return result
    return None


def _render_training_controls() -> ModelingResult | None:
    columns = st.columns([1, 3])
    should_train = columns[0].button("Latih Model", type="primary", use_container_width=True)
    columns[1].caption("Tombol ini memakai konfigurasi parameter dari sidebar.")

    if should_train or st.session_state.get("model_requested"):
        with st.spinner("Melatih model SARIMA/SARIMAX..."):
            return _run_modeling()

    return _get_current_result()


def _render_errors(result: ModelingResult) -> bool:
    if not result.errors:
        return False

    for error in result.errors:
        st.error(error)
    return True


def _render_model_config(result: ModelingResult) -> None:
    st.subheader("Konfigurasi Model")
    columns = st.columns(4)
    columns[0].metric("Mode Data", result.mode_label)
    columns[1].metric("Model", result.model_label)
    columns[2].metric("Parameter Mode", result.parameter_mode)
    columns[3].metric("Seasonal Order", str(result.seasonal_order or "-"))

    columns = st.columns(2)
    columns[0].write(f"Order: `{result.order}`")
    columns[1].write(f"Seasonal order: `{result.seasonal_order}`")

    for warning in result.warnings:
        st.warning(warning)


def _render_split_metrics(result: ModelingResult) -> None:
    st.subheader("Train-Test Split")
    train_count = 0 if result.train is None else len(result.train)
    test_count = 0 if result.test is None else len(result.test)
    columns = st.columns(4)
    columns[0].metric("Jumlah Train", train_count)
    columns[1].metric("Jumlah Test", test_count)
    columns[2].metric("AIC", _format_number(result.aic))
    columns[3].metric("BIC", _format_number(result.bic))


def _render_train_test_chart(result: ModelingResult) -> None:
    if result.train is None or result.test is None:
        return

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=result.train.index,
            y=result.train.values,
            mode="lines+markers",
            name="Train",
            line={"color": "#2563eb", "width": 2},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=result.test.index,
            y=result.test.values,
            mode="lines+markers",
            name="Test",
            line={"color": "#dc2626", "width": 2},
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


def _render_train_test_tables(result: ModelingResult) -> None:
    if result.train is None or result.test is None:
        return

    train_df = result.train.reset_index()
    train_df.columns = ["periode", "train"]
    test_df = result.test.reset_index()
    test_df.columns = ["periode", "test"]

    left_column, right_column = st.columns(2, gap="large")
    with left_column:
        st.write("Data Train")
        st.dataframe(train_df, use_container_width=True, hide_index=True)
    with right_column:
        st.write("Data Test")
        st.dataframe(test_df, use_container_width=True, hide_index=True)


def _render_model_summary(result: ModelingResult) -> None:
    with st.expander("Ringkasan Model"):
        if result.summary_text:
            st.code(result.summary_text, language="text")
        else:
            st.write("Ringkasan model belum tersedia.")

    with st.expander("Catatan Modeling"):
        if not result.notes:
            st.write("- Tidak ada catatan modeling.")
        for note in result.notes:
            st.write(f"- {note}")


def _render_result(result: ModelingResult) -> None:
    _render_model_config(result)
    if _render_errors(result):
        return

    st.success('Model berhasil dilatih dan tersimpan di `st.session_state["model_fit"]`.')
    _render_split_metrics(result)
    _render_train_test_chart(result)
    _render_train_test_tables(result)
    _render_model_summary(result)


def render_modeling_page() -> None:
    """Render the PRD-06 modeling page."""
    st.title("Pemodelan SARIMA")
    st.caption("Tahap PRD-06: train-test split, training SARIMAX, AIC, BIC, dan penyimpanan model.")

    series = st.session_state.get("ts_series")
    if not _render_input_state(series):
        return

    result = _render_training_controls()
    if result is None:
        st.info("Model belum dilatih. Gunakan tombol Latih Model atau tombol Proses Model di sidebar.")
        return

    _render_result(result)
