"""Entry point dashboard forecasting SARIMA/SARIMAX."""

from __future__ import annotations

import streamlit as st

from src.data_preprocessing_page import render_data_preprocessing_page
from src.overview import render_overview
from src.page_placeholders import render_placeholder_page
from src.page_registry import PAGE_OPTIONS
from src.sidebar import render_sidebar
from src.state import initialize_session_state


def render_selected_page(page_name: str) -> None:
    """Render the selected dashboard page."""
    if page_name == "Overview":
        render_overview()
        return

    if page_name == "Data & Preprocessing":
        render_data_preprocessing_page()
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
