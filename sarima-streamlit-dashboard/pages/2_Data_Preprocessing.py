"""Streamlit native page wrapper for Data & Preprocessing."""

from __future__ import annotations

import streamlit as st

from src.data_preprocessing_page import render_data_preprocessing_page
from src.page_registry import PAGE_OPTIONS
from src.sidebar import render_sidebar
from src.state import initialize_session_state


st.set_page_config(page_title="Data & Preprocessing - Dashboard SARIMA", layout="wide")
initialize_session_state()
st.session_state["current_page"] = "Data & Preprocessing"
render_sidebar(PAGE_OPTIONS)
render_data_preprocessing_page()
