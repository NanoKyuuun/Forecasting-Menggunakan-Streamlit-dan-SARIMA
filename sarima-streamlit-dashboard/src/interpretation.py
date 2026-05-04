"""Automatic Indonesian interpretation helpers for PRD-09."""

from __future__ import annotations

from typing import Any, Mapping

import pandas as pd


def _safe_len(value: Any) -> int:
    if value is None or not hasattr(value, "__len__"):
        return 0
    return len(value)


def _format_number(value: Any) -> str:
    if value is None or pd.isna(value):
        return "-"
    if isinstance(value, (int, float)):
        return f"{value:,.4f}"
    return str(value)


def _format_period(value: Any) -> str:
    if value is None or pd.isna(value):
        return "-"
    if hasattr(value, "strftime"):
        return value.strftime("%Y-%m-%d")
    return str(value)


def _series_trend_text(series: Any) -> str:
    if series is None or not hasattr(series, "dropna"):
        return "Tren historis belum dapat dibaca karena time series final belum tersedia."

    clean_series = pd.Series(series).dropna()
    if len(clean_series) < 2:
        return "Tren historis belum cukup kuat dibaca karena observasi kurang dari dua periode."

    first_value = float(clean_series.iloc[0])
    last_value = float(clean_series.iloc[-1])
    if last_value > first_value:
        direction = "meningkat"
    elif last_value < first_value:
        direction = "menurun"
    else:
        direction = "relatif stabil"

    return (
        f"Secara historis, nilai bergerak {direction} dari {_format_number(first_value)} "
        f"menjadi {_format_number(last_value)}."
    )


def methodology_narrative(data_mode: str, observation_count: int) -> list[str]:
    """Return safe methodology notes for annual/monthly data."""
    if observation_count <= 0:
        return [
            "Mode data belum memiliki time series final yang siap ditafsirkan.",
            "Kesimpulan metodologis akan lebih kuat setelah transformasi time series selesai dijalankan.",
        ]

    if data_mode == "Bulanan":
        if observation_count < 24:
            return [
                "Data bulanan kurang dari 24 observasi. SARIMA musiman dapat dicoba, tetapi hasilnya belum cukup kuat untuk dijadikan kesimpulan final.",
                "Interpretasi bulanan sebaiknya difokuskan pada pola awal dan perlu divalidasi dengan data tambahan.",
            ]
        return [
            "Data pendaftaran mahasiswa tersedia dalam bentuk bulanan, sehingga model SARIMA musiman dapat digunakan untuk menganalisis pola berulang dalam satu tahun.",
            "Interpretasi musiman tetap perlu dikaitkan dengan konteks kalender akademik dan periode penerimaan mahasiswa baru.",
        ]

    if observation_count and observation_count < 8:
        return [
            "Data tahunan memiliki jumlah observasi terbatas. Model digunakan untuk analisis tren dan forecast awal.",
            "Komponen musiman tidak diaktifkan karena pola musiman tidak dapat diuji secara kuat dari data tahunan yang pendek.",
        ]

    return [
        "Data pendaftaran mahasiswa tersedia dalam bentuk rekap tahunan, sehingga analisis utama difokuskan pada tren perubahan jumlah pendaftar dari tahun ke tahun.",
        "Model yang digunakan bersifat non-musiman karena data tahunan tidak menyediakan informasi pola bulanan dalam satu tahun.",
    ]


def interpret_dataset(raw_df: Any, uploaded_file_name: str | None = None) -> list[str]:
    """Interpret loaded dataset condition."""
    if raw_df is None or not hasattr(raw_df, "shape"):
        return ["Dataset belum dimuat. Upload file CSV/XLS/XLSX untuk memulai alur analisis."]

    row_count, column_count = raw_df.shape
    file_text = f" dari file {uploaded_file_name}" if uploaded_file_name else ""
    return [
        f"Dataset{file_text} berhasil dimuat dengan {row_count} baris dan {column_count} kolom.",
        "Kolom waktu, target, dan prodi/jurusan perlu dipilih sesuai struktur dataset agar alur preprocessing sampai forecasting konsisten.",
    ]


def interpret_preprocessing(result: Any) -> list[str]:
    """Interpret preprocessing output."""
    if result is None:
        return ["Preprocessing belum dijalankan."]
    if getattr(result, "errors", None):
        return [f"Preprocessing belum valid: {'; '.join(result.errors)}"]

    missing_total = 0
    missing_summary = getattr(result, "missing_summary", None)
    if missing_summary is not None and "Missing" in getattr(missing_summary, "columns", []):
        missing_total = int(pd.to_numeric(missing_summary["Missing"], errors="coerce").fillna(0).sum())

    outlier_count = _safe_len(getattr(result, "outlier_df", None))
    notes = [
        f"Preprocessing menghasilkan {getattr(result, 'rows_after', 0)} baris data bersih dari {getattr(result, 'rows_before', 0)} baris awal.",
        f"Total missing value yang terdeteksi pada laporan kolom adalah {missing_total}.",
        f"Duplikasi penuh terdeteksi {getattr(result, 'full_duplicate_count', 0)} baris dan duplikasi periode/prodi terdeteksi {getattr(result, 'key_duplicate_count', 0)} baris.",
    ]
    if outlier_count:
        notes.append(f"Sebanyak {outlier_count} baris ditandai sebagai outlier IQR; outlier tidak dihapus otomatis agar keputusan tetap transparan.")
    else:
        notes.append("Tidak ada outlier target berdasarkan metode IQR.")
    return notes


def interpret_transformation(result: Any) -> list[str]:
    """Interpret transformation and data mode output."""
    if result is None:
        return ["Transformasi time series belum dijalankan."]
    if getattr(result, "errors", None):
        return [f"Transformasi belum valid: {'; '.join(result.errors)}"]

    data_mode = getattr(result, "data_mode", "Tahunan")
    observation_count = int(getattr(result, "observation_count", 0))
    notes = [
        f"Data ditransformasikan menjadi mode {data_mode} dengan {observation_count} observasi terisi.",
        f"Periode analisis berjalan dari {_format_period(getattr(result, 'period_start', None))} sampai {_format_period(getattr(result, 'period_end', None))}.",
        f"Strategi periode hilang yang digunakan adalah {getattr(result, 'missing_period_strategy', '-')}.",
        _series_trend_text(getattr(result, "series", None)),
    ]
    notes.extend(methodology_narrative(data_mode, observation_count))
    return notes


def interpret_analysis(result: Any, data_mode: str = "Tahunan") -> list[str]:
    """Interpret time-series analysis output."""
    if result is None:
        return ["Analisis time series belum dijalankan."]

    series = getattr(result, "series", None)
    observation_count = _safe_len(series.dropna() if hasattr(series, "dropna") else series)
    notes = [_series_trend_text(series)]

    adf_result = getattr(result, "adf_result", None)
    if adf_result is not None and getattr(adf_result, "success", False):
        p_value = getattr(adf_result, "p_value", None)
        if getattr(adf_result, "is_stationary", False):
            notes.append(f"ADF Test menghasilkan p-value {_format_number(p_value)}, sehingga data dapat dianggap stasioner pada batas 0,05.")
        else:
            notes.append(f"ADF Test menghasilkan p-value {_format_number(p_value)}, sehingga data belum stasioner pada batas 0,05.")
    elif adf_result is not None:
        notes.append(getattr(adf_result, "message", "ADF Test belum dapat dijalankan."))
    else:
        notes.append("ADF Test belum tersedia.")

    correlation_df = getattr(result, "correlation_df", None)
    if correlation_df is not None and not correlation_df.empty:
        notes.append("ACF/PACF berhasil dihitung sebagai referensi pola autokorelasi.")
    else:
        notes.append("ACF/PACF belum cukup kuat atau belum tersedia karena observasi terbatas/konstan.")

    notes.extend(methodology_narrative(data_mode, observation_count))
    return notes


def interpret_modeling(result: Any, data_mode: str = "Tahunan") -> list[str]:
    """Interpret model training output."""
    if result is None:
        return ["Model belum dilatih."]
    if getattr(result, "errors", None):
        return [f"Model belum valid: {'; '.join(result.errors)}"]

    train_count = _safe_len(getattr(result, "train", None))
    test_count = _safe_len(getattr(result, "test", None))
    notes = [
        f"Model {getattr(result, 'model_label', '-')} berhasil dilatih dengan order {getattr(result, 'order', '-')} dan seasonal_order {getattr(result, 'seasonal_order', '-')}.",
        f"Pembagian data dilakukan berurutan berdasarkan waktu: {train_count} observasi train dan {test_count} observasi test.",
        f"Nilai AIC model adalah {_format_number(getattr(result, 'aic', None))} dan BIC adalah {_format_number(getattr(result, 'bic', None))}.",
    ]
    notes.extend(methodology_narrative(data_mode, train_count + test_count))
    return notes


def interpret_evaluation(result: Any) -> list[str]:
    """Interpret evaluation metrics and residual output."""
    if result is None:
        return ["Evaluasi model belum dijalankan."]
    if getattr(result, "errors", None):
        return [f"Evaluasi belum valid: {'; '.join(result.errors)}"]

    metrics = getattr(result, "metrics", {}) or {}
    notes = [
        f"Evaluasi menghasilkan MAE {_format_number(metrics.get('MAE'))}, RMSE {_format_number(metrics.get('RMSE'))}, dan MAPE {_format_number(metrics.get('MAPE'))}.",
        "Nilai error yang lebih kecil menunjukkan prediksi lebih dekat dengan data aktual pada periode testing.",
    ]
    if metrics.get("MAPE") is None:
        notes.append("MAPE tidak dihitung karena data aktual testing memuat 0 atau belum tersedia.")
    if _safe_len(getattr(result, "actual", None)) <= 1:
        notes.append("Data testing sangat sedikit, sehingga evaluasi model hanya bersifat indikatif.")
    if getattr(result, "ljung_box_df", None) is not None and not result.ljung_box_df.empty:
        notes.append("Ljung-Box tersedia untuk membaca indikasi autokorelasi residual.")
    else:
        notes.append("Diagnostic residual lanjutan dilewati bila residual belum cukup banyak atau konstan.")
    return notes


def interpret_forecast(forecast_df: Any, data_mode: str = "Tahunan") -> list[str]:
    """Interpret forecast direction."""
    if forecast_df is None or not hasattr(forecast_df, "empty") or forecast_df.empty:
        return ["Forecast belum dibuat."]

    first_forecast = float(forecast_df.iloc[0]["forecast"])
    last_forecast = float(forecast_df.iloc[-1]["forecast"])
    if last_forecast > first_forecast:
        trend_text = "Hasil forecast menunjukkan kecenderungan peningkatan jumlah pendaftar pada periode mendatang."
    elif last_forecast < first_forecast:
        trend_text = "Hasil forecast menunjukkan kecenderungan penurunan jumlah pendaftar pada periode mendatang."
    else:
        trend_text = "Hasil forecast menunjukkan jumlah pendaftar cenderung stabil pada periode mendatang."

    notes = [
        trend_text,
        f"Forecast pertama sebesar {_format_number(first_forecast)} dan forecast terakhir sebesar {_format_number(last_forecast)}.",
        "Confidence interval perlu dibaca sebagai rentang ketidakpastian, bukan angka kepastian tunggal.",
    ]
    notes.extend(methodology_narrative(data_mode, _safe_len(forecast_df)))
    return notes


def build_conclusion_sections(state: Mapping[str, Any]) -> dict[str, list[str]]:
    """Build conclusion sections from Streamlit session-state-like mapping."""
    raw_df = state.get("raw_df")
    transformation = state.get("transformation_report")
    modeling = state.get("modeling_report")
    evaluation = state.get("evaluation_report")
    forecast_df = state.get("forecast_df")
    data_mode = state.get("data_mode") or state.get("freq") or "Tahunan"
    series = state.get("ts_series")
    observation_count = _safe_len(pd.Series(series).dropna()) if series is not None else 0

    return {
        "Ringkasan Dataset": interpret_dataset(raw_df, state.get("uploaded_file_name")),
        "Mode Data dan Metodologi": methodology_narrative(str(data_mode), observation_count),
        "Ringkasan Transformasi": interpret_transformation(transformation),
        "Ringkasan Model": interpret_modeling(modeling, str(data_mode)),
        "Ringkasan Evaluasi": interpret_evaluation(evaluation),
        "Ringkasan Forecast": interpret_forecast(forecast_df, str(data_mode)),
        "Catatan Keterbatasan": [
            *methodology_narrative(str(data_mode), observation_count),
            "Dashboard ini mendukung penjelasan tren dan forecast awal; hasil akhir tetap perlu ditafsirkan bersama konteks penerimaan mahasiswa baru.",
        ],
        "Saran Pengembangan": [
            "Tambahkan data historis yang lebih panjang agar evaluasi statistik dan forecast lebih kuat.",
            "Gunakan data bulanan aktual jika ingin menguji komponen musiman SARIMA secara lebih layak.",
            "Bandingkan hasil SARIMA/SARIMAX dengan metode lain sebagai validasi akademik tambahan.",
        ],
    }
