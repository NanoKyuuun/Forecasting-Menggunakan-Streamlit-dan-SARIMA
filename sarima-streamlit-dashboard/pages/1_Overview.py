"""Streamlit native page wrapper for Overview."""

from __future__ import annotations

import streamlit as st

from src.overview import render_overview
from src.sidebar import render_sidebar
from src.page_registry import PAGE_OPTIONS
from src.state import initialize_session_state


st.set_page_config(page_title="Overview - Dashboard SARIMA", layout="wide")
initialize_session_state()
render_sidebar(PAGE_OPTIONS)
render_overview()
