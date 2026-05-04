# Dashboard Streamlit SARIMA

Folder ini berisi implementasi aplikasi dashboard forecasting pendaftaran mahasiswa baru berdasarkan `../PRD.md`.

Dokumentasi lengkap untuk pengguna tersedia di:

```text
../README.md
```

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

Tahap saat ini sudah mencakup PRD-09, polish UI/UX, dan script setup/run Windows. Tahap berikutnya adalah PRD-10 untuk testing, error handling, README, dan kesiapan demo.
