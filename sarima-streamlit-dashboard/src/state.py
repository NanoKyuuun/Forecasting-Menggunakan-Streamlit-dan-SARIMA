"""Session-state helpers for the dashboard workflow."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

import streamlit as st


DEFAULT_MODEL_CONFIG: dict[str, Any] = {
    "order": (1, 1, 1),
    "seasonal_order": (0, 0, 0, 0),
    "parameter_mode": "Manual",
}


DEFAULT_SESSION_STATE: dict[str, Any] = {
    "raw_df": None,
    "clean_df": None,
    "ts_series": None,
    "freq": "Tahunan",
    "data_mode": "Belum dipilih",
    "model_config": DEFAULT_MODEL_CONFIG,
    "train": None,
    "test": None,
    "model_fit": None,
    "metrics": None,
    "forecast_df": None,
    "uploaded_file": None,
    "uploaded_file_name": None,
    "column_time": None,
    "column_target": None,
    "column_prodi": None,
    "selected_prodi": "Semua prodi",
    "missing_period_strategy": "Biarkan kosong",
    "forecast_horizon": 3,
    "current_page": "Overview",
    "processing_notes": [],
    "model_requested": False,
}


def initialize_session_state() -> None:
    """Populate all session-state keys required by the PRD workflow."""
    for key, value in DEFAULT_SESSION_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = deepcopy(value)


def get_dataframe_columns(state_key: str = "raw_df") -> list[str]:
    """Return dataframe columns from session state when data is available."""
    dataframe = st.session_state.get(state_key)
    if dataframe is None or not hasattr(dataframe, "columns"):
        return []

    return [str(column) for column in dataframe.columns]


def has_time_series_data() -> bool:
    """Return True when transformed time-series data exists."""
    series = st.session_state.get("ts_series")
    return series is not None and hasattr(series, "__len__") and len(series) > 0
