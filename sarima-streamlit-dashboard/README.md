# Dashboard Streamlit SARIMA

Folder ini berisi implementasi aplikasi dashboard forecasting pendaftaran mahasiswa baru berdasarkan `../PRD.md`.

## Menjalankan Aplikasi

```powershell
cd sarima-streamlit-dashboard
pip install -r requirements.txt
streamlit run app.py
```

Tahap saat ini menyelesaikan issue PRD-06: train-test split berurutan, training SARIMAX, parameter manual/Auto AIC sederhana, AIC/BIC, dan penyimpanan `model_fit`.
