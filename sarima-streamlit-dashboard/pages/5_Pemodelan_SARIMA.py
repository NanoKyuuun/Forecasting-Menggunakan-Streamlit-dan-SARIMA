"""Streamlit native page wrapper for Pemodelan SARIMA."""

from __future__ import annotations

import streamlit as st

from src.modeling_page import render_modeling_page
from src.page_registry import PAGE_OPTIONS
from src.sidebar import render_sidebar
from src.state import initialize_session_state
from src.workflow import PAGE_MODELING


st.set_page_config(page_title="Pemodelan SARIMA - Dashboard SARIMA", layout="wide")
initialize_session_state()
st.session_state["current_page"] = PAGE_MODELING
render_sidebar(PAGE_OPTIONS)
render_modeling_page()
