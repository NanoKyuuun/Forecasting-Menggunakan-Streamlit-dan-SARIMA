"""Workflow metadata and readiness checks for the dashboard UI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


PAGE_BERANDA = "Beranda"
PAGE_DATA = "Data dan Preprocessing"
PAGE_TRANSFORMATION = "Transformasi Data"
PAGE_ANALYSIS = "Analisis Time Series"
PAGE_MODELING = "Pemodelan SARIMA"
PAGE_EVALUATION = "Evaluasi Model"
PAGE_FORECASTING = "Forecasting dan Interpretasi"
PAGE_CONCLUSION = "Kesimpulan"


PAGE_ALIASES: dict[str, str] = {
    "Overview": PAGE_BERANDA,
    "Data & Preprocessing": PAGE_DATA,
    "Data Transformation": PAGE_TRANSFORMATION,
    "Forecasting & Interpretasi": PAGE_FORECASTING,
}


@dataclass(frozen=True)
class WorkflowStep:
    """Display metadata for a dashboard workflow step."""

    number: int
    page: str
    short_label: str
    title: str
    goal: str
    required_input: str
    output: str
    next_step: str


WORKFLOW_STEPS: list[WorkflowStep] = [
    WorkflowStep(
        1,
        PAGE_DATA,
        "Data",
        "Data dan Preprocessing",
        "Membaca dataset, memilih kolom penting, dan membersihkan data awal.",
        "File CSV/XLS/XLSX serta pilihan kolom waktu dan target.",
        "Data bersih siap ditransformasikan menjadi time series.",
        PAGE_TRANSFORMATION,
    ),
    WorkflowStep(
        2,
        PAGE_TRANSFORMATION,
        "Transformasi",
        "Transformasi Data",
        "Mengubah data bersih menjadi deret waktu final sesuai frekuensi.",
        "Data bersih, mode tahunan/bulanan, dan strategi periode hilang.",
        "Time series final untuk analisis dan modeling.",
        PAGE_ANALYSIS,
    ),
    WorkflowStep(
        3,
        PAGE_ANALYSIS,
        "Analisis",
        "Analisis Time Series",
        "Membaca pola historis, statistik, stasioneritas, ACF, dan PACF.",
        "Time series final.",
        "Interpretasi awal pola data dan kesiapan modeling.",
        PAGE_MODELING,
    ),
    WorkflowStep(
        4,
        PAGE_MODELING,
        "Modeling",
        "Pemodelan SARIMA",
        "Melatih model SARIMA/SARIMAX dengan train-test split berurutan.",
        "Time series final dan konfigurasi parameter model.",
        "Model terlatih, data train/test, AIC, dan BIC.",
        PAGE_EVALUATION,
    ),
    WorkflowStep(
        5,
        PAGE_EVALUATION,
        "Evaluasi",
        "Evaluasi Model",
        "Menguji prediksi model terhadap data testing.",
        "Model terlatih dan data testing.",
        "Metrik error, aktual vs prediksi, dan residual.",
        PAGE_FORECASTING,
    ),
    WorkflowStep(
        6,
        PAGE_FORECASTING,
        "Forecast",
        "Forecasting dan Interpretasi",
        "Membuat forecast masa depan dengan confidence interval dan CSV.",
        "Model valid, time series final, dan horizon forecast.",
        "Tabel forecast, grafik forecast, confidence interval, dan CSV.",
        PAGE_CONCLUSION,
    ),
    WorkflowStep(
        7,
        PAGE_CONCLUSION,
        "Kesimpulan",
        "Kesimpulan",
        "Merangkum hasil akhir penelitian dan keterbatasan metodologi.",
        "Output dari tahap-tahap sebelumnya.",
        "Ringkasan akademik untuk demo atau penjelasan tugas akhir.",
        "Selesai",
    ),
]


PAGE_OPTIONS: list[str] = [PAGE_BERANDA, *[step.page for step in WORKFLOW_STEPS]]


def normalize_page_name(page_name: str | None) -> str:
    """Map legacy labels to the current Indonesian page labels."""
    if not page_name:
        return PAGE_BERANDA
    return PAGE_ALIASES.get(page_name, page_name)


def get_step_for_page(page_name: str) -> WorkflowStep | None:
    """Return workflow metadata for a page."""
    normalized = normalize_page_name(page_name)
    for step in WORKFLOW_STEPS:
        if step.page == normalized:
            return step
    return None


def _has_valid_report(state: Mapping[str, Any], key: str) -> bool:
    report = state.get(key)
    return report is not None and not getattr(report, "errors", [])


def is_step_complete(state: Mapping[str, Any], page_name: str) -> bool:
    """Return whether a workflow step has a successful output."""
    page_name = normalize_page_name(page_name)
    if page_name == PAGE_DATA:
        return _has_valid_report(state, "preprocessing_report")
    if page_name == PAGE_TRANSFORMATION:
        return _has_valid_report(state, "transformation_report")
    if page_name == PAGE_ANALYSIS:
        return state.get("analysis_report") is not None
    if page_name == PAGE_MODELING:
        return _has_valid_report(state, "modeling_report")
    if page_name == PAGE_EVALUATION:
        return _has_valid_report(state, "evaluation_report")
    if page_name == PAGE_FORECASTING:
        forecast_df = state.get("forecast_df")
        return forecast_df is not None and hasattr(forecast_df, "empty") and not forecast_df.empty
    if page_name == PAGE_CONCLUSION:
        return is_step_complete(state, PAGE_FORECASTING)
    return False


def is_step_ready(state: Mapping[str, Any], page_name: str) -> bool:
    """Return whether a workflow step can be started."""
    page_name = normalize_page_name(page_name)
    if page_name in {PAGE_BERANDA, PAGE_DATA}:
        return True
    if page_name == PAGE_TRANSFORMATION:
        return state.get("clean_df") is not None
    if page_name in {PAGE_ANALYSIS, PAGE_MODELING}:
        return state.get("ts_series") is not None
    if page_name == PAGE_EVALUATION:
        return state.get("model_fit") is not None and state.get("test") is not None
    if page_name == PAGE_FORECASTING:
        return _has_valid_report(state, "modeling_report")
    if page_name == PAGE_CONCLUSION:
        return any(is_step_complete(state, step.page) for step in WORKFLOW_STEPS[:-1])
    return False


def get_step_status(state: Mapping[str, Any], page_name: str) -> str:
    """Return a short Indonesian status label for a workflow page."""
    if is_step_complete(state, page_name):
        return "Selesai"
    if is_step_ready(state, page_name):
        return "Siap"
    return "Menunggu"


def completed_step_count(state: Mapping[str, Any]) -> int:
    """Return number of completed workflow steps."""
    return sum(1 for step in WORKFLOW_STEPS if is_step_complete(state, step.page))


def get_recommended_page(state: Mapping[str, Any]) -> str:
    """Return the first incomplete ready page as the recommended next action."""
    for step in WORKFLOW_STEPS:
        if not is_step_complete(state, step.page) and is_step_ready(state, step.page):
            return step.page
    return PAGE_CONCLUSION
