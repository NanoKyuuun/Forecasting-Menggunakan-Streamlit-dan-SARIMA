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
    "time_series_df": None,
    "aggregated_df": None,
    "freq": "Tahunan",
    "freq_code": "YS",
    "data_mode": "Belum dipilih",
    "model_config": DEFAULT_MODEL_CONFIG,
    "train": None,
    "test": None,
    "model_fit": None,
    "metrics": None,
    "forecast_df": None,
    "uploaded_file": None,
    "uploaded_file_name": None,
    "uploaded_file_signature": None,
    "data_metadata": None,
    "data_load_error": None,
    "dataset_shape": None,
    "preprocessing_report": None,
    "transformation_report": None,
    "analysis_report": None,
    "descriptive_stats": None,
    "rolling_df": None,
    "correlation_df": None,
    "adf_result": None,
    "target_missing_action": "Isi 0",
    "column_time": None,
    "column_target": None,
    "column_prodi": None,
    "selected_prodi": "Semua prodi",
    "missing_period_strategy": "Isi 0",
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


def reset_after_raw_data_change() -> None:
    """Clear downstream state when a new raw dataset is loaded."""
    keys_to_clear = [
        "clean_df",
        "ts_series",
        "time_series_df",
        "aggregated_df",
        "train",
        "test",
        "model_fit",
        "metrics",
        "forecast_df",
        "preprocessing_report",
        "transformation_report",
        "analysis_report",
        "descriptive_stats",
        "rolling_df",
        "correlation_df",
        "adf_result",
    ]
    for key in keys_to_clear:
        st.session_state[key] = None

    st.session_state["processing_notes"] = []
    st.session_state["model_requested"] = False


def reset_uploaded_data_state() -> None:
    """Clear raw-data and downstream state when the upload is removed."""
    st.session_state["raw_df"] = None
    st.session_state["uploaded_file"] = None
    st.session_state["uploaded_file_name"] = None
    st.session_state["uploaded_file_signature"] = None
    st.session_state["data_metadata"] = None
    st.session_state["data_load_error"] = None
    st.session_state["dataset_shape"] = None
    st.session_state["column_time"] = None
    st.session_state["column_target"] = None
    st.session_state["column_prodi"] = None
    st.session_state["selected_prodi"] = "Semua prodi"
    reset_after_raw_data_change()
