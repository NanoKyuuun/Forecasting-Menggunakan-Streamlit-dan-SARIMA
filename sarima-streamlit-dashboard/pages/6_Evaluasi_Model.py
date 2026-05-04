"""Streamlit native page wrapper for Evaluasi Model."""

from __future__ import annotations

import streamlit as st

from src.evaluation_page import render_evaluation_page
from src.page_registry import PAGE_OPTIONS
from src.sidebar import render_sidebar
from src.state import initialize_session_state


st.set_page_config(page_title="Evaluasi Model - Dashboard SARIMA", layout="wide")
initialize_session_state()
st.session_state["current_page"] = "Evaluasi Model"
render_sidebar(PAGE_OPTIONS)
render_evaluation_page()
