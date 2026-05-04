# Dashboard Streamlit SARIMA

Folder ini berisi implementasi aplikasi dashboard forecasting pendaftaran mahasiswa baru berdasarkan `../PRD.md`.

## Menjalankan Aplikasi

Cara paling mudah dari root repo:

```powershell
setup.bat
run.bat
```

Untuk port custom:

```powershell
run.bat 8511
```

Cara manual dari folder aplikasi:

```powershell
cd sarima-streamlit-dashboard
pip install -r requirements.txt
streamlit run app.py
```

Tahap saat ini menyelesaikan issue PRD-09: interpretasi otomatis berbahasa Indonesia pada setiap tahap utama dan halaman Kesimpulan untuk ringkasan akademik, keterbatasan, serta saran pengembangan.
