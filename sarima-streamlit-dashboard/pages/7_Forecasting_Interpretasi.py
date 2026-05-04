"""Streamlit native page wrapper for Forecasting & Interpretasi."""

from __future__ import annotations

import streamlit as st

from src.forecasting_page import render_forecasting_page
from src.page_registry import PAGE_OPTIONS
from src.sidebar import render_sidebar
from src.state import initialize_session_state
from src.workflow import PAGE_FORECASTING


st.set_page_config(page_title="Forecasting dan Interpretasi - Dashboard SARIMA", layout="wide")
initialize_session_state()
st.session_state["current_page"] = PAGE_FORECASTING
render_sidebar(PAGE_OPTIONS)
render_forecasting_page()
