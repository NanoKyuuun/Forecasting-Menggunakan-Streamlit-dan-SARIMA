"""Page names used by the custom dashboard navigation."""

from __future__ import annotations

from src.workflow import (
    PAGE_ANALYSIS,
    PAGE_CONCLUSION,
    PAGE_DATA,
    PAGE_EVALUATION,
    PAGE_FORECASTING,
    PAGE_MODELING,
    PAGE_OPTIONS,
    PAGE_TRANSFORMATION,
)


PAGE_DESCRIPTIONS: dict[str, str] = {
    PAGE_DATA: "Issue PRD-02 dan PRD-03",
    PAGE_TRANSFORMATION: "Issue PRD-04",
    PAGE_ANALYSIS: "Issue PRD-05",
    PAGE_MODELING: "Issue PRD-06",
    PAGE_EVALUATION: "Issue PRD-07",
    PAGE_FORECASTING: "Issue PRD-08 dan PRD-09",
    PAGE_CONCLUSION: "Issue PRD-09",
}
