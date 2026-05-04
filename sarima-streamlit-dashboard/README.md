# Dashboard Streamlit SARIMA

Folder ini berisi implementasi aplikasi dashboard forecasting pendaftaran mahasiswa baru berdasarkan `../PRD.md`.

## Menjalankan Aplikasi

```powershell
cd sarima-streamlit-dashboard
pip install -r requirements.txt
streamlit run app.py
```

Tahap saat ini menyelesaikan issue PRD-07: evaluasi aktual vs prediksi, MAE/MSE/RMSE/MAPE zero-safe, residual, residual ACF, dan Ljung-Box saat data mencukupi.
