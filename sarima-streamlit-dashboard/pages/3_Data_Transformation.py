"""Streamlit native page wrapper for Data Transformation."""

from __future__ import annotations

import streamlit as st

from src.page_registry import PAGE_OPTIONS
from src.sidebar import render_sidebar
from src.state import initialize_session_state
from src.transformation_page import render_transformation_page
from src.workflow import PAGE_TRANSFORMATION


st.set_page_config(page_title="Transformasi Data - Dashboard SARIMA", layout="wide")
initialize_session_state()
st.session_state["current_page"] = PAGE_TRANSFORMATION
render_sidebar(PAGE_OPTIONS)
render_transformation_page()
