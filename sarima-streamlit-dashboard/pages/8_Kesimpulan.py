"""Streamlit native page wrapper for Kesimpulan."""

from __future__ import annotations

import streamlit as st

from src.conclusion_page import render_conclusion_page
from src.page_registry import PAGE_OPTIONS
from src.sidebar import render_sidebar
from src.state import initialize_session_state
from src.workflow import PAGE_CONCLUSION


st.set_page_config(page_title="Kesimpulan - Dashboard SARIMA", layout="wide")
initialize_session_state()
st.session_state["current_page"] = PAGE_CONCLUSION
render_sidebar(PAGE_OPTIONS)
render_conclusion_page()
