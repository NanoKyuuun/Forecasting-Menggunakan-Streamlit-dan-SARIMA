"""Streamlit native page wrapper for Analisis Time Series."""

from __future__ import annotations

import streamlit as st

from src.analysis_page import render_analysis_page
from src.page_registry import PAGE_OPTIONS
from src.sidebar import render_sidebar
from src.state import initialize_session_state


st.set_page_config(page_title="Analisis Time Series - Dashboard SARIMA", layout="wide")
initialize_session_state()
st.session_state["current_page"] = "Analisis Time Series"
render_sidebar(PAGE_OPTIONS)
render_analysis_page()
