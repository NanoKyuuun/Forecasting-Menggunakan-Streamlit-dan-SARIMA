"""Entry point dashboard forecasting SARIMA/SARIMAX."""

from __future__ import annotations

import streamlit as st

from src.analysis_page import render_analysis_page
from src.conclusion_page import render_conclusion_page
from src.data_preprocessing_page import render_data_preprocessing_page
from src.evaluation_page import render_evaluation_page
from src.forecasting_page import render_forecasting_page
from src.modeling_page import render_modeling_page
from src.overview import render_overview
from src.page_placeholders import render_placeholder_page
from src.page_registry import PAGE_OPTIONS
from src.sidebar import render_sidebar
from src.state import initialize_session_state
from src.transformation_page import render_transformation_page
from src.workflow import (
    PAGE_ANALYSIS,
    PAGE_BERANDA,
    PAGE_CONCLUSION,
    PAGE_DATA,
    PAGE_EVALUATION,
    PAGE_FORECASTING,
    PAGE_MODELING,
    PAGE_TRANSFORMATION,
    normalize_page_name,
)


def render_selected_page(page_name: str) -> None:
    """Render the selected dashboard page."""
    page_name = normalize_page_name(page_name)
    if page_name == PAGE_BERANDA:
        render_overview()
        return

    if page_name == PAGE_DATA:
        render_data_preprocessing_page()
        return

    if page_name == PAGE_TRANSFORMATION:
        render_transformation_page()
        return

    if page_name == PAGE_ANALYSIS:
        render_analysis_page()
        return

    if page_name == PAGE_MODELING:
        render_modeling_page()
        return

    if page_name == PAGE_EVALUATION:
        render_evaluation_page()
        return

    if page_name == PAGE_FORECASTING:
        render_forecasting_page()
        return

    if page_name == PAGE_CONCLUSION:
        render_conclusion_page()
        return

    render_placeholder_page(page_name)


def main() -> None:
    st.set_page_config(
        page_title="Dashboard Forecasting PMB SARIMA",
        page_icon=":chart_with_upwards_trend:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    initialize_session_state()
    sidebar_state = render_sidebar(PAGE_OPTIONS)
    render_selected_page(sidebar_state["page"])


if __name__ == "__main__":
    main()
