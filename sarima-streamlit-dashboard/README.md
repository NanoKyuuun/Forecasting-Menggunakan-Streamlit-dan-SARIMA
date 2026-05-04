# Dashboard Streamlit SARIMA

Folder ini berisi implementasi aplikasi dashboard forecasting pendaftaran mahasiswa baru berdasarkan `../PRD.md`.

## Menjalankan Aplikasi

```powershell
cd sarima-streamlit-dashboard
pip install -r requirements.txt
streamlit run app.py
```

Tahap saat ini menyelesaikan issue PRD-08: final model dilatih ulang pada seluruh time series, horizon forecast, confidence interval, tabel/grafik forecast, dan download CSV.
