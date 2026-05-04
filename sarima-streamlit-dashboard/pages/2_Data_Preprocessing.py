"""Streamlit native page wrapper for Data & Preprocessing."""

from __future__ import annotations

import streamlit as st

from src.data_preprocessing_page import render_data_preprocessing_page
from src.page_registry import PAGE_OPTIONS
from src.sidebar import render_sidebar
from src.state import initialize_session_state
from src.workflow import PAGE_DATA


st.set_page_config(page_title="Data dan Preprocessing - Dashboard SARIMA", layout="wide")
initialize_session_state()
st.session_state["current_page"] = PAGE_DATA
render_sidebar(PAGE_OPTIONS)
render_data_preprocessing_page()
