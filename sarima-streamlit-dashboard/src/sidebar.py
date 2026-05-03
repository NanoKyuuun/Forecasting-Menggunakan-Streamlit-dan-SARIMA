"""Global sidebar controls for the Streamlit dashboard."""

from __future__ import annotations

from typing import Any

import streamlit as st

from src.state import get_dataframe_columns, reset_uploaded_data_state


FREQUENCY_OPTIONS = ["Tahunan", "Bulanan"]
MISSING_PERIOD_OPTIONS = ["Biarkan kosong", "Isi 0", "Forward fill", "Interpolasi"]
PARAMETER_MODE_OPTIONS = ["Manual", "Auto AIC sederhana"]


def _select_column(label: str, key: str, columns: list[str]) -> str | None:
    if not columns:
        st.sidebar.selectbox(label, ["Belum ada dataset"], disabled=True, key=f"{key}_disabled")
        st.session_state[key] = None
        return None

    options = ["Tidak dipilih", *columns]
    current_value = st.session_state.get(key)
    index = options.index(current_value) if current_value in options else 0
    selected = st.sidebar.selectbox(label, options, index=index, key=f"{key}_select")
    st.session_state[key] = None if selected == "Tidak dipilih" else selected
    return st.session_state[key]


def _render_manual_parameter_inputs() -> dict[str, Any]:
    st.sidebar.caption("Parameter SARIMA manual")
    col_p, col_d, col_q = st.sidebar.columns(3)
    p = col_p.number_input("p", min_value=0, max_value=5, value=1, step=1)
    d = col_d.number_input("d", min_value=0, max_value=2, value=1, step=1)
    q = col_q.number_input("q", min_value=0, max_value=5, value=1, step=1)

    frequency = st.session_state.get("freq", "Tahunan")
    default_s = 12 if frequency == "Bulanan" else 0
    seasonal_disabled = frequency == "Tahunan"

    col_p_seasonal, col_d_seasonal, col_q_seasonal, col_s = st.sidebar.columns(4)
    seasonal_p = col_p_seasonal.number_input(
        "P",
        min_value=0,
        max_value=3,
        value=0,
        step=1,
        disabled=seasonal_disabled,
    )
    seasonal_d = col_d_seasonal.number_input(
        "D",
        min_value=0,
        max_value=2,
        value=0,
        step=1,
        disabled=seasonal_disabled,
    )
    seasonal_q = col_q_seasonal.number_input(
        "Q",
        min_value=0,
        max_value=3,
        value=0,
        step=1,
        disabled=seasonal_disabled,
    )
    seasonal_s = col_s.number_input(
        "s",
        min_value=0,
        max_value=24,
        value=default_s,
        step=1,
        disabled=seasonal_disabled,
    )

    seasonal_order = (0, 0, 0, 0)
    if frequency == "Bulanan":
        seasonal_order = (seasonal_p, seasonal_d, seasonal_q, seasonal_s)

    return {
        "order": (p, d, q),
        "seasonal_order": seasonal_order,
        "parameter_mode": "Manual",
    }


def render_sidebar(page_options: list[str]) -> dict[str, Any]:
    """Render all global sidebar controls and sync them into session state."""
    st.sidebar.title("Pengaturan Dashboard")

    uploaded_file = st.sidebar.file_uploader(
        "Upload Dataset",
        type=["csv", "xls", "xlsx"],
        help="Dataset akan diproses pada halaman Data & Preprocessing.",
    )
    if uploaded_file is not None:
        st.session_state["uploaded_file"] = uploaded_file
        st.session_state["uploaded_file_name"] = uploaded_file.name
    elif st.session_state.get("uploaded_file") is not None:
        reset_uploaded_data_state()

    current_page = st.session_state.get("current_page", page_options[0])
    page_index = page_options.index(current_page) if current_page in page_options else 0
    page = st.sidebar.radio("Pilih Halaman", page_options, index=page_index)
    st.session_state["current_page"] = page

    columns = get_dataframe_columns("raw_df")
    _select_column("Pilih Kolom Waktu", "column_time", columns)
    _select_column("Pilih Kolom Target", "column_target", columns)
    _select_column("Pilih Kolom Prodi/Jurusan", "column_prodi", columns)

    if st.session_state.get("column_prodi") is None:
        st.sidebar.selectbox("Pilih Prodi", ["Semua prodi"], disabled=True)
        st.session_state["selected_prodi"] = "Semua prodi"
    else:
        st.sidebar.selectbox("Pilih Prodi", ["Semua prodi"], key="selected_prodi")

    frequency = st.sidebar.selectbox(
        "Pilih Frekuensi Data",
        FREQUENCY_OPTIONS,
        index=FREQUENCY_OPTIONS.index(st.session_state.get("freq", "Tahunan")),
    )
    st.session_state["freq"] = frequency
    st.session_state["data_mode"] = frequency

    missing_strategy = st.sidebar.selectbox(
        "Strategi Missing Period",
        MISSING_PERIOD_OPTIONS,
        index=MISSING_PERIOD_OPTIONS.index(st.session_state.get("missing_period_strategy", "Biarkan kosong")),
    )
    st.session_state["missing_period_strategy"] = missing_strategy

    horizon = st.sidebar.number_input(
        "Horizon Forecast",
        min_value=1,
        max_value=60,
        value=int(st.session_state.get("forecast_horizon", 3)),
        step=1,
    )
    st.session_state["forecast_horizon"] = int(horizon)

    parameter_mode = st.sidebar.radio(
        "Mode Parameter",
        PARAMETER_MODE_OPTIONS,
        index=PARAMETER_MODE_OPTIONS.index(
            st.session_state.get("model_config", {}).get("parameter_mode", "Manual")
        ),
    )

    if parameter_mode == "Manual":
        model_config = _render_manual_parameter_inputs()
    else:
        model_config = {
            "order": None,
            "seasonal_order": (0, 0, 0, 0) if frequency == "Tahunan" else None,
            "parameter_mode": parameter_mode,
        }
        st.sidebar.caption("Auto search akan diaktifkan pada tahap modeling.")

    st.session_state["model_config"] = model_config

    can_process_model = st.session_state.get("ts_series") is not None
    if st.sidebar.button("Proses Model", disabled=not can_process_model):
        st.session_state["model_requested"] = True

    return {
        "page": page,
        "uploaded_file": uploaded_file,
        "frequency": frequency,
        "missing_strategy": missing_strategy,
        "forecast_horizon": int(horizon),
        "model_config": model_config,
    }
