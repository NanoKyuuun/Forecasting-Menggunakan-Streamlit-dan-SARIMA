"""Kesimpulan page for PRD-09."""

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st

from src.interpretation import build_conclusion_sections
from src.ui_components import render_page_header
from src.workflow import PAGE_CONCLUSION


def _safe_len(value: Any) -> int:
    if value is None or not hasattr(value, "__len__"):
        return 0
    return len(value)


def _format_value(value: Any) -> str:
    if value is None or pd.isna(value):
        return "-"
    if isinstance(value, (int, float)):
        return f"{value:,.4f}"
    return str(value)


def _count_completed_outputs() -> int:
    keys = [
        "raw_df",
        "preprocessing_report",
        "transformation_report",
        "analysis_report",
        "modeling_report",
        "evaluation_report",
        "forecast_df",
    ]
    return sum(1 for key in keys if st.session_state.get(key) is not None)


def _render_metric_cards() -> None:
    raw_df = st.session_state.get("raw_df")
    series = st.session_state.get("ts_series")
    metrics = st.session_state.get("metrics") or {}
    forecast_df = st.session_state.get("forecast_df")

    columns = st.columns(4)
    columns[0].metric("Output Tersedia", f"{_count_completed_outputs()}/7")
    columns[1].metric("Baris Dataset", _safe_len(raw_df))
    columns[2].metric("Observasi Time Series", _safe_len(series))
    columns[3].metric("Mode Data", st.session_state.get("data_mode", "Belum dipilih"))

    columns = st.columns(3)
    columns[0].metric("MAPE", _format_value(metrics.get("MAPE")))
    if forecast_df is not None and hasattr(forecast_df, "empty") and not forecast_df.empty:
        columns[1].metric("Forecast Berikutnya", _format_value(forecast_df.iloc[0]["forecast"]))
        columns[2].metric("Tren Forecast", str(forecast_df.iloc[-1]["tren"]))
    else:
        columns[1].metric("Forecast Berikutnya", "-")
        columns[2].metric("Tren Forecast", "-")


def _render_section(title: str, items: list[str]) -> None:
    st.subheader(title)
    for item in items:
        st.write(f"- {item}")


def render_conclusion_page() -> None:
    """Render PRD-09 conclusion summary."""
    render_page_header(
        PAGE_CONCLUSION,
        "Ringkasan hasil, interpretasi otomatis, keterbatasan, dan saran pengembangan.",
    )

    _render_metric_cards()

    sections = build_conclusion_sections(st.session_state)
    for title, items in sections.items():
        _render_section(title, items)
