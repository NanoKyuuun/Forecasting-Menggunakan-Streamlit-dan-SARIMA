"""Page names used by the custom dashboard navigation."""

from __future__ import annotations


PAGE_OPTIONS: list[str] = [
    "Overview",
    "Data & Preprocessing",
    "Data Transformation",
    "Analisis Time Series",
    "Pemodelan SARIMA",
    "Evaluasi Model",
    "Forecasting & Interpretasi",
    "Kesimpulan",
]


PAGE_DESCRIPTIONS: dict[str, str] = {
    "Data & Preprocessing": "Issue PRD-02 dan PRD-03",
    "Data Transformation": "Issue PRD-04",
    "Analisis Time Series": "Issue PRD-05",
    "Pemodelan SARIMA": "Issue PRD-06",
    "Evaluasi Model": "Issue PRD-07",
    "Forecasting & Interpretasi": "Issue PRD-08 dan PRD-09",
    "Kesimpulan": "Issue PRD-09",
}
