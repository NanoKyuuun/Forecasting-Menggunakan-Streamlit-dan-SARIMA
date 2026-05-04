"""SARIMA/SARIMAX modeling helpers for PRD-06."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Any
from warnings import catch_warnings, simplefilter

import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX


MANUAL_MODE = "Manual"
AUTO_AIC_MODE = "Auto AIC sederhana"


@dataclass(frozen=True)
class ModelDefaults:
    """Default SARIMAX configuration derived from data frequency."""

    mode_label: str
    model_label: str
    order: tuple[int, int, int]
    seasonal_order: tuple[int, int, int, int]
    seasonal_enabled: bool
    warning: str | None = None


@dataclass(frozen=True)
class ModelingResult:
    """Result object returned by the modeling workflow."""

    model_fit: Any | None
    train: pd.Series | None
    test: pd.Series | None
    order: tuple[int, int, int] | None
    seasonal_order: tuple[int, int, int, int] | None
    parameter_mode: str
    mode_label: str
    model_label: str
    aic: float | None
    bic: float | None
    summary_text: str | None
    notes: list[str]
    warnings: list[str]
    errors: list[str]


def prepare_model_series(series: pd.Series) -> pd.Series:
    """Return numeric time series without missing values for model training."""
    prepared = series.copy()
    prepared.index = pd.to_datetime(prepared.index, errors="coerce")
    prepared = prepared[prepared.index.notna()]
    prepared = pd.to_numeric(prepared, errors="coerce")
    prepared = prepared.dropna().sort_index()
    return prepared.astype(float)


def get_model_defaults(frequency_label: str, n_obs: int) -> ModelDefaults:
    """Return adaptive defaults for annual/monthly data."""
    if frequency_label == "Bulanan":
        if n_obs >= 24:
            return ModelDefaults(
                mode_label="Bulanan",
                model_label="SARIMA musiman",
                order=(1, 1, 1),
                seasonal_order=(1, 1, 1, 12),
                seasonal_enabled=True,
            )

        return ModelDefaults(
            mode_label="Bulanan",
            model_label="SARIMAX non-musiman fallback",
            order=(1, 1, 1),
            seasonal_order=(0, 0, 0, 0),
            seasonal_enabled=False,
            warning=(
                "Data bulanan kurang dari 24 observasi. Komponen musiman dinonaktifkan agar training lebih stabil."
            ),
        )

    warning = None
    if n_obs < 8:
        warning = (
            "Data tahunan memiliki observasi terbatas. Model dipakai sebagai analisis tren awal dan tidak memakai "
            "komponen musiman."
        )

    return ModelDefaults(
        mode_label="Tahunan",
        model_label="SARIMAX non-musiman",
        order=(1, 1, 0),
        seasonal_order=(0, 0, 0, 0),
        seasonal_enabled=False,
        warning=warning,
    )


def split_train_test(series: pd.Series, test_size: float = 0.2) -> tuple[pd.Series, pd.Series]:
    """Split time series into train/test preserving chronological order."""
    clean_series = prepare_model_series(series)
    n_obs = len(clean_series)

    if n_obs < 3:
        raise ValueError("Data terlalu sedikit untuk train-test split.")

    if n_obs < 8:
        return clean_series.iloc[:-1], clean_series.iloc[-1:]

    train_size = int(n_obs * (1 - test_size))
    train_size = min(max(train_size, 2), n_obs - 1)
    return clean_series.iloc[:train_size], clean_series.iloc[train_size:]


def train_sarima_model(
    train: pd.Series,
    order: tuple[int, int, int],
    seasonal_order: tuple[int, int, int, int],
) -> Any:
    """Train a SARIMAX model with a small, dashboard-friendly fit budget."""
    with catch_warnings():
        simplefilter("ignore")
        model = SARIMAX(
            train,
            order=order,
            seasonal_order=seasonal_order,
            enforce_stationarity=False,
            enforce_invertibility=False,
        )
        return model.fit(disp=False, maxiter=100)


def _candidate_orders(n_obs: int) -> list[tuple[int, int, int]]:
    pdq = list(product(range(0, 2), range(0, 2), range(0, 2)))
    if n_obs < 8:
        return [(0, 1, 0), (1, 1, 0), (0, 1, 1), (1, 0, 0)]
    return pdq


def auto_search_sarima(
    train: pd.Series,
    frequency_label: str,
    seasonal_enabled: bool,
) -> tuple[Any | None, tuple[int, int, int] | None, tuple[int, int, int, int] | None, list[str]]:
    """Run a deliberately small AIC search and return the best model."""
    notes: list[str] = []
    seasonal_orders = [(0, 0, 0, 0)]
    if frequency_label == "Bulanan" and seasonal_enabled:
        seasonal_orders = [(0, 0, 0, 0), (1, 0, 0, 12), (0, 1, 1, 12)]

    best_model = None
    best_order = None
    best_seasonal_order = None
    best_aic = np.inf

    for order in _candidate_orders(len(train)):
        for seasonal_order in seasonal_orders:
            try:
                model_fit = train_sarima_model(train, order, seasonal_order)
            except Exception:
                continue

            aic = getattr(model_fit, "aic", np.inf)
            if np.isfinite(aic) and aic < best_aic:
                best_model = model_fit
                best_order = order
                best_seasonal_order = seasonal_order
                best_aic = float(aic)

    if best_model is not None:
        notes.append(f"Auto AIC memilih order={best_order} dan seasonal_order={best_seasonal_order}.")

    return best_model, best_order, best_seasonal_order, notes


def _coerce_order(value: Any, fallback: tuple[int, int, int]) -> tuple[int, int, int]:
    if not isinstance(value, tuple) or len(value) != 3:
        return fallback

    return tuple(int(part) for part in value)


def _coerce_seasonal_order(value: Any, fallback: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    if not isinstance(value, tuple) or len(value) != 4:
        return fallback

    return tuple(int(part) for part in value)


def fit_model(
    series: pd.Series,
    frequency_label: str,
    model_config: dict[str, Any] | None = None,
) -> ModelingResult:
    """Train a SARIMAX model and package all PRD-06 outputs."""
    model_config = model_config or {}
    clean_series = prepare_model_series(series)
    warnings: list[str] = []
    notes: list[str] = []

    if len(clean_series) < 3:
        return ModelingResult(
            model_fit=None,
            train=None,
            test=None,
            order=None,
            seasonal_order=None,
            parameter_mode=model_config.get("parameter_mode", MANUAL_MODE),
            mode_label=frequency_label,
            model_label="-",
            aic=None,
            bic=None,
            summary_text=None,
            notes=[],
            warnings=[],
            errors=["Data terlalu sedikit untuk melatih model. Minimal diperlukan 3 observasi."],
        )

    defaults = get_model_defaults(frequency_label, len(clean_series))
    if defaults.warning:
        warnings.append(defaults.warning)

    try:
        train, test = split_train_test(clean_series)
    except ValueError as exc:
        return ModelingResult(
            model_fit=None,
            train=None,
            test=None,
            order=None,
            seasonal_order=None,
            parameter_mode=model_config.get("parameter_mode", MANUAL_MODE),
            mode_label=defaults.mode_label,
            model_label=defaults.model_label,
            aic=None,
            bic=None,
            summary_text=None,
            notes=[],
            warnings=warnings,
            errors=[str(exc)],
        )

    parameter_mode = str(model_config.get("parameter_mode", MANUAL_MODE))

    if parameter_mode == AUTO_AIC_MODE:
        model_fit, order, seasonal_order, auto_notes = auto_search_sarima(
            train,
            frequency_label,
            defaults.seasonal_enabled,
        )
        notes.extend(auto_notes)
        if model_fit is None or order is None or seasonal_order is None:
            return ModelingResult(
                model_fit=None,
                train=train,
                test=test,
                order=None,
                seasonal_order=None,
                parameter_mode=parameter_mode,
                mode_label=defaults.mode_label,
                model_label=defaults.model_label,
                aic=None,
                bic=None,
                summary_text=None,
                notes=notes,
                warnings=warnings,
                errors=["Auto AIC tidak menemukan kombinasi parameter yang berhasil dilatih."],
            )
    else:
        order = _coerce_order(model_config.get("order"), defaults.order)
        seasonal_order = _coerce_seasonal_order(model_config.get("seasonal_order"), defaults.seasonal_order)
        if not defaults.seasonal_enabled:
            seasonal_order = (0, 0, 0, 0)
        try:
            model_fit = train_sarima_model(train, order, seasonal_order)
        except Exception as exc:
            return ModelingResult(
                model_fit=None,
                train=train,
                test=test,
                order=order,
                seasonal_order=seasonal_order,
                parameter_mode=parameter_mode,
                mode_label=defaults.mode_label,
                model_label=defaults.model_label,
                aic=None,
                bic=None,
                summary_text=None,
                notes=notes,
                warnings=warnings,
                errors=[f"Training model gagal: {exc}"],
            )

    summary_text = None
    try:
        summary_text = str(model_fit.summary())
    except Exception:
        summary_text = "Ringkasan model tidak tersedia."

    notes.append("Train-test split dilakukan berdasarkan urutan waktu tanpa shuffle.")
    if defaults.mode_label == "Tahunan":
        notes.append("Komponen musiman tidak diaktifkan untuk data tahunan.")
    elif defaults.seasonal_enabled:
        notes.append("Komponen musiman bulanan memakai seasonal period 12.")

    return ModelingResult(
        model_fit=model_fit,
        train=train,
        test=test,
        order=order,
        seasonal_order=seasonal_order,
        parameter_mode=parameter_mode,
        mode_label=defaults.mode_label,
        model_label=defaults.model_label,
        aic=float(model_fit.aic) if np.isfinite(model_fit.aic) else None,
        bic=float(model_fit.bic) if np.isfinite(model_fit.bic) else None,
        summary_text=summary_text,
        notes=notes,
        warnings=warnings,
        errors=[],
    )
