# Dashboard Forecasting PMB dengan Streamlit dan SARIMA

Dashboard ini digunakan untuk membantu analisis dan forecasting jumlah pendaftaran mahasiswa baru berdasarkan data historis. Aplikasi dibuat dengan Streamlit dan model SARIMA/SARIMAX, sehingga pengguna dapat menjalankan alur penelitian dari upload dataset sampai kesimpulan akhir dalam satu dashboard.

Dokumentasi ini ditulis untuk pengguna yang ingin memahami:

- fungsi aplikasi ini,
- cara menjalankannya,
- data apa yang harus disiapkan,
- urutan penggunaan menu,
- hasil yang muncul di setiap tahap,
- dan apa yang harus dilakukan setelah satu tahap selesai.

## Fungsi Aplikasi

Aplikasi ini bukan hanya menampilkan grafik data. Alur utamanya dibuat untuk kebutuhan penelitian forecasting:

1. Membaca dataset pendaftaran mahasiswa baru dari file CSV, XLS, atau XLSX.
2. Membersihkan data: validasi kolom, missing value, duplikasi, dan outlier.
3. Mengubah data menjadi time series tahunan atau bulanan.
4. Menganalisis pola historis, statistik deskriptif, ADF, ACF, dan PACF.
5. Melatih model SARIMA/SARIMAX.
6. Mengevaluasi model dengan data testing.
7. Membuat forecast periode berikutnya.
8. Menyediakan interpretasi otomatis dan kesimpulan.
9. Mengunduh hasil forecast dalam CSV.

## Cara Menjalankan

Cara termudah di Windows adalah dari root repo ini.

### 1. Setup pertama kali

Jalankan:

```powershell
setup.bat
```

Script ini akan:

- membuat virtual environment `.venv` jika belum ada,
- memakai Python yang tersedia di komputer,
- menginstall dependency dari `sarima-streamlit-dashboard/requirements.txt`.

Jika setup berhasil, akan muncul pesan:

```text
[OK] Setup selesai.
```

### 2. Jalankan aplikasi

Jalankan:

```powershell
run.bat
```

Secara default aplikasi berjalan di:

```text
http://localhost:8501
```

Jika ingin memakai port lain:

```powershell
run.bat 8511
```

Lalu buka:

```text
http://localhost:8511
```

### 3. Cara manual jika tidak memakai BAT

```powershell
cd sarima-streamlit-dashboard
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Jika `.venv` belum ada, jalankan `setup.bat` terlebih dahulu.

## Format Dataset yang Didukung

Format file:

- `.csv`
- `.xls`
- `.xlsx`

Minimal dataset harus memiliki:

| Kebutuhan | Contoh Kolom | Keterangan |
|---|---|---|
| Kolom waktu | `tahun`, `tanggal`, `periode` | Dipakai sebagai index waktu |
| Kolom target | `jumlah_pendaftar`, `pendaftar`, `total` | Angka yang akan dianalisis dan diprediksi |
| Kolom prodi/jurusan | `prodi`, `jurusan` | Opsional, untuk filter per prodi |

Contoh dataset tahunan:

| tahun | prodi | jumlah_pendaftar |
|---|---|---:|
| 2021 | Teknik Informatika | 120 |
| 2022 | Teknik Informatika | 135 |
| 2023 | Teknik Informatika | 150 |

Contoh dataset bulanan:

| tanggal | prodi | jumlah_pendaftar |
|---|---|---:|
| 2023-01-01 | Manajemen | 20 |
| 2023-02-01 | Manajemen | 25 |
| 2023-03-01 | Manajemen | 23 |

Catatan penting:

- Data tahunan digunakan untuk membaca tren antar tahun.
- Data bulanan dapat dipakai untuk pola musiman jika jumlah observasi cukup.
- Aplikasi tidak membuat data bulanan palsu dari data tahunan.
- Untuk SARIMA musiman bulanan yang lebih kuat, idealnya tersedia minimal 24 observasi bulanan.

## Alur Penggunaan Dashboard

Dashboard sudah disusun sebagai alur kerja bertahap. Ikuti menu dari atas ke bawah.

### 1. Beranda

Fungsi:

- menampilkan status alur kerja,
- menunjukkan tahap mana yang sudah selesai,
- memberi rekomendasi langkah berikutnya,
- menampilkan ringkasan observasi, mode data, MAPE, dan forecast jika sudah tersedia.

Yang harus dilakukan:

- jika baru mulai, lanjut ke menu `Data dan Preprocessing`,
- jika sudah memproses data, lihat rekomendasi langkah berikutnya di Beranda atau sidebar.

Hasil yang muncul:

- progress alur,
- ringkasan dataset,
- grafik historis singkat,
- forecast singkat jika forecast sudah dibuat.

### 2. Data dan Preprocessing

Fungsi:

- membaca dataset,
- menampilkan preview data mentah,
- membersihkan nama kolom,
- memvalidasi kolom waktu, target, dan prodi,
- mendeteksi missing value,
- menangani duplikasi,
- menandai outlier dengan metode IQR.

Yang harus dilakukan:

1. Unggah dataset lewat sidebar.
2. Pilih `Kolom Waktu`.
3. Pilih `Kolom Target`.
4. Pilih `Kolom Prodi/Jurusan` jika ada.
5. Pilih strategi missing value target.
6. Baca hasil validasi dan catatan cleaning.

Hasil yang muncul:

- preview data mentah,
- laporan kolom,
- laporan missing value,
- laporan duplikasi,
- laporan outlier,
- tabel data bersih,
- interpretasi otomatis preprocessing.

Setelah selesai:

- lanjut ke `Transformasi Data`.

### 3. Transformasi Data

Fungsi:

- mengubah data bersih menjadi time series,
- memilih frekuensi tahunan atau bulanan,
- menerapkan filter prodi,
- mengisi periode hilang sesuai strategi yang dipilih,
- membuat time series final untuk analisis dan modeling.

Yang harus dilakukan:

1. Pastikan data bersih sudah tersedia.
2. Pilih `Frekuensi Data` di sidebar: `Tahunan` atau `Bulanan`.
3. Pilih filter prodi jika diperlukan.
4. Pilih strategi periode hilang.
5. Buka menu `Transformasi Data`.

Hasil yang muncul:

- ringkasan periode awal dan akhir,
- jumlah observasi,
- data hasil agregasi,
- time series final,
- grafik time series,
- tombol unduh time series CSV,
- interpretasi otomatis transformasi.

Setelah selesai:

- lanjut ke `Analisis Time Series`.

### 4. Analisis Time Series

Fungsi:

- membaca pola historis data,
- menampilkan grafik historis,
- menghitung statistik deskriptif,
- menampilkan rolling mean dan rolling standard deviation,
- menjalankan ADF Test jika data cukup,
- menghitung ACF dan PACF jika data cukup.

Yang harus dilakukan:

- pastikan `Transformasi Data` sudah menghasilkan time series final,
- buka menu `Analisis Time Series`,
- baca interpretasi otomatis dan warning metodologis.

Hasil yang muncul:

- grafik historis,
- statistik deskriptif,
- rolling mean dan rolling std,
- hasil ADF Test,
- ACF/PACF,
- interpretasi otomatis analisis.

Setelah selesai:

- lanjut ke `Pemodelan SARIMA`.

### 5. Pemodelan SARIMA

Fungsi:

- membagi time series menjadi train dan test secara berurutan berdasarkan waktu,
- melatih model SARIMA/SARIMAX,
- menampilkan parameter model,
- menampilkan AIC dan BIC,
- menyimpan model untuk evaluasi dan forecasting.

Yang harus dilakukan:

1. Pastikan time series final sudah tersedia.
2. Pilih `Mode Parameter` di sidebar:
   - `Manual` untuk mengatur parameter sendiri,
   - `Auto AIC sederhana` untuk pencarian parameter kecil berbasis AIC.
3. Klik `Latih Model` di halaman modeling atau `Latih / Proses Model` di sidebar.

Hasil yang muncul:

- konfigurasi model,
- jumlah data train dan test,
- grafik train-test,
- tabel train-test,
- AIC dan BIC,
- ringkasan model,
- interpretasi otomatis modeling.

Setelah selesai:

- lanjut ke `Evaluasi Model`.

### 6. Evaluasi Model

Fungsi:

- membuat prediksi pada data testing,
- membandingkan aktual vs prediksi,
- menghitung metrik error,
- membaca residual model.

Metrik yang dihitung:

- MAE,
- MSE,
- RMSE,
- MAPE.

Catatan MAPE:

- Jika data aktual testing memiliki nilai `0`, MAPE tidak dihitung agar tidak terjadi pembagian dengan nol.

Hasil yang muncul:

- metrik evaluasi,
- grafik aktual vs prediksi,
- tabel aktual vs prediksi,
- plot residual,
- histogram residual,
- residual ACF jika data cukup,
- Ljung-Box jika data cukup,
- interpretasi otomatis evaluasi.

Setelah selesai:

- lanjut ke `Forecasting dan Interpretasi`.

### 7. Forecasting dan Interpretasi

Fungsi:

- melatih final model menggunakan seluruh time series,
- membuat forecast periode masa depan,
- menampilkan confidence interval,
- menyediakan tabel dan grafik forecast,
- menyediakan file CSV hasil forecast.

Yang harus dilakukan:

1. Pastikan model sudah berhasil dilatih.
2. Atur `Horizon Forecast` di sidebar.
3. Buka menu `Forecasting dan Interpretasi`.

Hasil yang muncul:

- horizon forecast,
- order dan seasonal order,
- forecast pertama dan terakhir,
- tren akhir forecast,
- grafik historis + forecast,
- confidence interval,
- tabel forecast,
- tombol unduh forecast CSV,
- interpretasi otomatis forecast.

Kolom tabel forecast:

| Kolom | Arti |
|---|---|
| `periode` | Periode prediksi |
| `forecast` | Nilai prediksi |
| `lower_bound` | Batas bawah confidence interval |
| `upper_bound` | Batas atas confidence interval |
| `perubahan` | Selisih dari periode sebelumnya |
| `tren` | Naik, Turun, atau Stabil |

Setelah selesai:

- lanjut ke `Kesimpulan`.

### 8. Kesimpulan

Fungsi:

- merangkum seluruh hasil dashboard,
- menjelaskan kondisi dataset,
- menjelaskan mode data,
- merangkum model,
- merangkum evaluasi,
- merangkum forecast,
- menampilkan keterbatasan metodologis,
- memberi saran pengembangan.

Hasil yang muncul:

- ringkasan dataset,
- ringkasan transformasi,
- ringkasan model,
- ringkasan evaluasi,
- ringkasan forecast,
- catatan keterbatasan,
- saran pengembangan.

Jika sebagian tahap belum dijalankan:

- halaman tetap aman dibuka,
- bagian yang belum tersedia akan menampilkan keterangan bahwa output belum dibuat.

## Cara Membaca Hasil

### Jika forecast naik

Artinya model memperkirakan jumlah pendaftar cenderung meningkat pada periode mendatang. Hasil ini dapat dipakai sebagai indikasi awal untuk perencanaan kapasitas, promosi, atau evaluasi strategi PMB.

### Jika forecast turun

Artinya model memperkirakan jumlah pendaftar cenderung menurun. Hasil ini perlu dibaca bersama konteks kampus, strategi promosi, perubahan kebijakan, dan kondisi eksternal.

### Jika forecast stabil

Artinya model memperkirakan jumlah pendaftar relatif tidak berubah besar. Ini dapat menjadi dasar untuk mempertahankan strategi berjalan, tetapi tetap perlu evaluasi data tambahan.

### Jika confidence interval lebar

Artinya ketidakpastian forecast lebih tinggi. Biasanya ini terjadi karena data sedikit, data fluktuatif, atau pola historis belum cukup kuat.

### Jika evaluasi model kurang kuat

Jika data testing sangat sedikit, metrik evaluasi hanya bersifat indikatif. Untuk kesimpulan akademik yang lebih kuat, tambahkan data historis.

## Keterbatasan Metodologis

Hal yang perlu diperhatikan saat menjelaskan hasil:

- Data tahunan pendek tidak cukup untuk membuktikan pola musiman.
- Model pada data tahunan lebih tepat disebut analisis tren dan forecast awal.
- Data bulanan kurang dari 24 observasi belum cukup kuat untuk SARIMA musiman.
- Hasil forecast adalah estimasi berbasis pola historis, bukan kepastian.
- Interpretasi akhir tetap perlu mempertimbangkan konteks PMB, kebijakan kampus, promosi, dan faktor eksternal.

## Troubleshooting

### `run.bat` meminta setup

Jalankan:

```powershell
setup.bat
```

Lalu ulangi:

```powershell
run.bat
```

### Port sudah dipakai

Jalankan dengan port lain:

```powershell
run.bat 8511
```

### Dataset tidak terbaca

Periksa:

- format file harus CSV/XLS/XLSX,
- file memiliki header kolom,
- file tidak sedang rusak atau terkunci,
- kolom waktu dan target memang ada.

### Pilihan kolom belum muncul di sidebar

Pastikan dataset sudah berhasil dibaca pada menu `Data dan Preprocessing`.

### Modeling gagal

Coba:

- gunakan parameter lebih sederhana,
- pilih mode `Auto AIC sederhana`,
- pastikan jumlah observasi tidak terlalu sedikit,
- pastikan target sudah numerik.

### Forecast belum muncul

Pastikan:

- time series final sudah tersedia,
- model sudah berhasil dilatih,
- horizon forecast sudah diisi,
- menu `Forecasting dan Interpretasi` sudah dibuka.

## Struktur Project

```text
.
|-- setup.bat
|-- run.bat
|-- PRD.md
|-- README.md
`-- sarima-streamlit-dashboard/
    |-- app.py
    |-- requirements.txt
    |-- pages/
    |-- src/
    |-- data/
    `-- assets/
```

File penting:

| File/Folder | Fungsi |
|---|---|
| `setup.bat` | Setup environment dan install dependency |
| `run.bat` | Menjalankan dashboard Streamlit |
| `PRD.md` | Dokumen kebutuhan dan spesifikasi produk |
| `sarima-streamlit-dashboard/app.py` | Entry point aplikasi |
| `sarima-streamlit-dashboard/pages/` | Wrapper halaman Streamlit |
| `sarima-streamlit-dashboard/src/` | Modul utama data loader, preprocessing, transformation, analysis, modeling, evaluation, forecasting, dan UI |

## Alur Demo yang Disarankan

Untuk demonstrasi, gunakan urutan ini:

1. Jalankan `setup.bat`.
2. Jalankan `run.bat`.
3. Buka `http://localhost:8501`.
4. Unggah dataset.
5. Pilih kolom waktu, target, dan prodi jika ada.
6. Buka `Data dan Preprocessing`.
7. Lanjut ke `Transformasi Data`.
8. Lanjut ke `Analisis Time Series`.
9. Lanjut ke `Pemodelan SARIMA` dan klik `Latih Model`.
10. Lanjut ke `Evaluasi Model`.
11. Lanjut ke `Forecasting dan Interpretasi`.
12. Unduh CSV forecast jika diperlukan.
13. Buka `Kesimpulan` untuk ringkasan akhir.

## Status Pengembangan

Fitur utama PRD-01 sampai PRD-09 sudah tersedia:

- setup struktur aplikasi,
- data loader,
- preprocessing,
- transformasi time series,
- analisis time series,
- modeling SARIMA/SARIMAX,
- evaluasi model,
- forecasting,
- interpretasi otomatis,
- halaman kesimpulan,
- polish alur UI/UX,
- script setup/run Windows.

Tahap berikutnya adalah PRD-10:

- testing end-to-end,
- error handling tambahan,
- validasi demo readiness,
- finalisasi README dan dokumentasi pendukung.
