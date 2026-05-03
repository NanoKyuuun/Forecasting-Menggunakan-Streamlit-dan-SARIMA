"""Streamlit native page wrapper for Data Transformation."""

from __future__ import annotations

import streamlit as st

from src.page_placeholders import render_placeholder_page
from src.page_registry import PAGE_OPTIONS
from src.sidebar import render_sidebar
from src.state import initialize_session_state


st.set_page_config(page_title="Data Transformation - Dashboard SARIMA", layout="wide")
initialize_session_state()
st.session_state["current_page"] = "Data Transformation"
render_sidebar(PAGE_OPTIONS)
render_placeholder_page("Data Transformation")
