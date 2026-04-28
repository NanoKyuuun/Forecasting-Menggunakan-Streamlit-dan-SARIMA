# Rancangan Final Project Dashboard Tugas Akhir: Forecasting Menggunakan Streamlit dan SARIMA

## 1. Ringkasan Utama

Dokumen ini berisi rancangan final untuk project tugas akhir berbasis **dashboard forecasting menggunakan Streamlit dan metode SARIMA**. Rancangan ini dibuat untuk membantu memperjelas flow aplikasi, batasan fitur, kebutuhan data, struktur halaman, alur analisis, serta strategi implementasi agar project tidak hanya terlihat bagus dari sisi tampilan, tetapi juga kuat secara akademik dan realistis untuk dikerjakan.

Berdasarkan kebutuhan tugas akhir, pendekatan yang paling tepat bukanlah dashboard bisnis murni dan bukan juga dashboard operasional penuh. Pendekatan yang paling aman adalah **dashboard penelitian forecasting**. Artinya, dashboard harus mengikuti alur berpikir penelitian, mulai dari data, preprocessing, analisis time series, pemodelan SARIMA, evaluasi model, hingga hasil forecasting dan interpretasi.

Flow final yang direkomendasikan adalah:

```text
Overview Penelitian
→ Data & Preprocessing
→ Analisis Time Series
→ Pemodelan SARIMA
→ Evaluasi & Diagnostik Model
→ Forecasting & Interpretasi
→ Kesimpulan / Rekomendasi Ringkas
```

Dengan flow tersebut, dashboard akan lebih mudah dipahami oleh client, lebih siap dipresentasikan saat sidang, dan lebih kuat ketika diuji oleh dosen pembimbing atau dosen penguji.

---

## 2. Konteks Project

Project ini dibuat untuk kebutuhan **TA / tugas akhir** yang menggunakan pendekatan forecasting time series. Teknologi utama yang digunakan adalah:

- **Streamlit** sebagai framework dashboard.
- **Python** sebagai bahasa pemrograman utama.
- **SARIMA** sebagai metode forecasting.
- Library analisis data seperti `pandas`, `numpy`, `statsmodels`, dan visualisasi seperti `matplotlib`, `plotly`, atau `seaborn` jika diperlukan.

Dashboard ini tidak hanya berfungsi untuk menampilkan hasil prediksi, tetapi juga sebagai media untuk menjelaskan proses penelitian. Karena itu, dashboard harus mampu menjawab pertanyaan berikut:

1. Data apa yang digunakan?
2. Bagaimana data dibersihkan dan dipersiapkan?
3. Apakah data memiliki pola tren atau musiman?
4. Mengapa SARIMA layak digunakan?
5. Bagaimana parameter SARIMA dipilih?
6. Seberapa baik performa model?
7. Bagaimana hasil forecast ke depan?
8. Apa makna dari hasil forecast tersebut?

Jika dashboard mampu menjawab pertanyaan-pertanyaan di atas, maka dashboard tidak hanya menjadi aplikasi visualisasi, tetapi juga menjadi alat bantu pembuktian metodologi penelitian.

---

## 3. Masalah Utama yang Harus Diselesaikan

Masalah utama pada project seperti ini biasanya bukan hanya pada coding, tetapi pada **ketidakjelasan flow**. Client sering kali tahu ingin membuat dashboard forecasting, tetapi belum memahami struktur yang tepat untuk tugas akhir.

Beberapa masalah yang perlu diantisipasi:

### 3.1 Client belum tahu dashboard seperti apa yang dibutuhkan

Client mungkin hanya mengatakan ingin membuat dashboard prediksi. Namun, dashboard prediksi bisa memiliki banyak bentuk, misalnya:

- dashboard bisnis yang fokus pada KPI,
- dashboard analitik yang fokus pada proses penelitian,
- dashboard operasional yang fokus pada rekomendasi tindakan.

Untuk kebutuhan tugas akhir, dashboard yang paling cocok adalah **dashboard analitik / penelitian**, karena tugas akhir menuntut penjelasan proses, bukan hanya hasil akhir.

### 3.2 Risiko scope terlalu besar

Jika semua ide dimasukkan, dashboard bisa menjadi terlalu berat. Contohnya:

- fitur alert stok,
- rekomendasi produksi,
- dashboard operasional,
- input banyak produk,
- multi cabang,
- login user,
- export laporan lengkap,
- perbandingan banyak model.

Fitur-fitur tersebut terlihat menarik, tetapi bisa membuat project melebar. Untuk TA, yang paling penting adalah flow penelitian dan hasil forecasting yang dapat dipertanggungjawabkan.

### 3.3 Risiko dashboard hanya menjadi tampilan grafik

Jika dashboard hanya menampilkan grafik forecast tanpa proses analisis, maka secara akademik akan lemah. Penguji bisa bertanya:

- Mengapa menggunakan SARIMA?
- Apakah datanya stasioner?
- Apakah ada pola musiman?
- Bagaimana parameter model dipilih?
- Bagaimana model dievaluasi?
- Apakah hasil prediksi dapat dipercaya?

Karena itu, dashboard harus menunjukkan proses analisis secara runtut.

---

## 4. Rekomendasi Konsep Final

Konsep final yang paling disarankan adalah:

> **Dashboard Penelitian Forecasting Berbasis Streamlit Menggunakan Metode SARIMA**

Konsep ini menempatkan dashboard sebagai media presentasi penelitian. Bukan hanya untuk menampilkan angka prediksi, tetapi juga untuk memperlihatkan proses ilmiah yang dilakukan.

Dashboard harus memiliki karakter:

- sistematis,
- semi-formal,
- akademik,
- mudah dibaca,
- tidak terlalu dekoratif,
- fokus pada data, model, hasil, dan interpretasi.

---

## 5. Alasan Memilih Dashboard Penelitian Forecasting

### 5.1 Lebih cocok untuk tugas akhir

Tugas akhir biasanya dinilai dari:

- kejelasan masalah,
- kesesuaian metode,
- proses penelitian,
- hasil analisis,
- kemampuan menjelaskan hasil,
- kemampuan mempertanggungjawabkan metode.

Dashboard bisnis murni biasanya hanya fokus pada hasil akhir. Sementara itu, dashboard penelitian memperlihatkan proses dari awal sampai akhir. Ini jauh lebih cocok untuk kebutuhan akademik.

### 5.2 Memudahkan presentasi sidang

Saat sidang, mahasiswa dapat menjelaskan dashboard mengikuti alur halaman:

1. Menjelaskan topik dan dataset.
2. Menjelaskan preprocessing.
3. Menjelaskan pola data.
4. Menjelaskan pemilihan SARIMA.
5. Menjelaskan evaluasi model.
6. Menjelaskan hasil forecast.
7. Menjelaskan kesimpulan.

Dengan alur seperti ini, presentasi akan lebih runtut dan tidak membingungkan.

### 5.3 Lebih aman dari pertanyaan penguji

Penguji biasanya tidak hanya melihat tampilan, tetapi juga mempertanyakan metodologi. Jika dashboard sudah menampilkan preprocessing, ADF test, ACF/PACF, parameter model, evaluasi error, dan interpretasi, maka mahasiswa akan lebih siap menjawab pertanyaan.

---

## 6. Batasan Scope Project

Agar project realistis untuk dikerjakan, scope harus dibatasi dengan jelas.

### 6.1 Scope utama yang wajib dikerjakan

Fitur wajib project:

1. Menampilkan data historis.
2. Melakukan preprocessing data.
3. Menampilkan visualisasi time series.
4. Melakukan analisis pola tren dan musiman.
5. Melakukan uji stasioneritas.
6. Menampilkan ACF dan PACF.
7. Melatih model SARIMA.
8. Menampilkan parameter model.
9. Mengevaluasi model.
10. Menampilkan hasil forecast.
11. Menampilkan confidence interval.
12. Menampilkan tabel hasil prediksi.
13. Menampilkan interpretasi hasil.

### 6.2 Scope tambahan yang disarankan

Fitur tambahan yang sangat disarankan jika waktu cukup:

1. Download hasil forecast dalam bentuk CSV.
2. Perbandingan SARIMA dengan baseline sederhana.
3. Diagnostik residual.
4. Input horizon forecast dari sidebar.
5. Interpretasi otomatis sederhana.
6. Export grafik atau laporan sederhana.

### 6.3 Scope yang sebaiknya tidak dipaksakan

Fitur berikut sebaiknya tidak menjadi prioritas awal:

1. Login multi user.
2. Role admin dan user.
3. Dashboard operasional stok penuh.
4. Rekomendasi produksi yang kompleks.
5. Integrasi database besar.
6. Notifikasi otomatis.
7. Deployment multi environment yang kompleks.
8. Perbandingan terlalu banyak model forecasting.

Fitur tersebut bisa dijadikan bagian pengembangan lanjutan, bukan inti tugas akhir.

---

## 7. Target Pengguna Dashboard

Dashboard ini memiliki beberapa target pengguna:

### 7.1 Mahasiswa / peneliti

Mahasiswa menggunakan dashboard untuk:

- menguji data,
- melihat proses analisis,
- menjalankan model,
- menampilkan hasil prediksi,
- mempersiapkan presentasi sidang.

### 7.2 Dosen pembimbing

Dosen pembimbing menggunakan dashboard untuk:

- mengecek apakah flow penelitian sudah benar,
- melihat apakah metode SARIMA digunakan secara tepat,
- mengevaluasi kelayakan hasil forecast,
- memberikan masukan terhadap proses analisis.

### 7.3 Dosen penguji

Dosen penguji menggunakan dashboard untuk:

- memahami alur penelitian,
- melihat bukti analisis,
- mengecek kesesuaian data dan metode,
- menilai apakah kesimpulan sesuai dengan hasil.

### 7.4 Client / pemilik data

Client menggunakan dashboard untuk:

- melihat hasil forecast,
- memahami tren data,
- membaca insight sederhana,
- mengetahui proyeksi periode mendatang.

---

## 8. Flow Besar Sistem

Flow besar sistem dapat digambarkan seperti berikut:

```text
User membuka dashboard
        ↓
User memilih / mengunggah dataset
        ↓
Sistem membaca dan memvalidasi data
        ↓
Sistem melakukan preprocessing
        ↓
Sistem menampilkan overview data
        ↓
Sistem melakukan analisis time series
        ↓
Sistem membangun model SARIMA
        ↓
Sistem mengevaluasi model
        ↓
Sistem menghasilkan forecast
        ↓
Sistem menampilkan grafik, tabel, dan interpretasi
        ↓
User dapat membaca atau mengunduh hasil forecast
```

Flow ini cukup sederhana, tetapi sudah mencakup kebutuhan penelitian secara lengkap.

---

## 9. Struktur Halaman Dashboard Final

Struktur final yang direkomendasikan terdiri dari 7 halaman utama:

1. **Overview Penelitian**
2. **Data & Preprocessing**
3. **Analisis Time Series**
4. **Pemodelan SARIMA**
5. **Evaluasi & Diagnostik Model**
6. **Forecasting & Interpretasi**
7. **Kesimpulan / Rekomendasi**

Jika ingin dibuat lebih ringkas, halaman 5 dan 6 bisa digabung. Namun untuk tugas akhir, pemisahan halaman akan membuat alur lebih jelas.

---

# 10. Halaman 1 — Overview Penelitian

## 10.1 Tujuan halaman

Halaman Overview adalah halaman pembuka. Fungsinya untuk memberi gambaran cepat kepada pengguna mengenai topik penelitian, data yang digunakan, metode yang dipakai, dan hasil utama.

Halaman ini harus menjawab:

- Penelitian ini tentang apa?
- Apa yang diprediksi?
- Data apa yang digunakan?
- Metode apa yang digunakan?
- Apa hasil ringkas dari model?

## 10.2 Komponen yang perlu ditampilkan

### 10.2.1 Judul dashboard

Contoh judul:

> Dashboard Forecasting Penjualan Menggunakan Metode SARIMA

Judul harus spesifik. Hindari judul yang terlalu umum seperti:

> Dashboard Forecasting

Judul yang baik harus menyebut objek dan metode.

### 10.2.2 Deskripsi singkat penelitian

Tambahkan paragraf singkat yang menjelaskan tujuan project.

Contoh:

> Dashboard ini dirancang untuk membantu menganalisis data penjualan historis dan menghasilkan prediksi penjualan pada periode berikutnya menggunakan metode SARIMA. Dashboard menampilkan proses mulai dari preprocessing data, analisis pola time series, pemodelan, evaluasi, hingga interpretasi hasil forecast.

### 10.2.3 Informasi dataset

Tampilkan informasi seperti:

- nama dataset,
- jumlah observasi,
- periode awal data,
- periode akhir data,
- frekuensi data,
- variabel target,
- jumlah missing value,
- jumlah data setelah preprocessing.

### 10.2.4 Metrik utama

Gunakan card metric untuk menampilkan angka penting:

- total data,
- nilai aktual terakhir,
- forecast periode berikutnya,
- nilai MAE/RMSE/MAPE,
- parameter SARIMA terbaik.

Contoh tampilan metric:

```text
+-------------------+-------------------+-------------------+-------------------+
| Total Observasi   | Aktual Terakhir   | Forecast Next     | MAPE Model        |
| 120 data          | 1.250             | 1.310             | 8.4%              |
+-------------------+-------------------+-------------------+-------------------+
```

### 10.2.5 Grafik ringkas aktual dan forecast

Tampilkan grafik utama yang memperlihatkan:

- data historis,
- hasil fitting model,
- forecast beberapa periode ke depan,
- confidence interval jika tersedia.

Grafik ini menjadi visual utama yang pertama kali dilihat oleh client atau penguji.

## 10.3 Catatan desain

Halaman Overview tidak boleh terlalu penuh. Jangan memasukkan ACF/PACF, residual, dan statistik terlalu detail di halaman ini. Detail teknis sebaiknya diletakkan di halaman analisis atau pemodelan.

---

# 11. Halaman 2 — Data & Preprocessing

## 11.1 Tujuan halaman

Halaman ini digunakan untuk menunjukkan bahwa data tidak langsung dipakai begitu saja, tetapi diproses terlebih dahulu agar layak digunakan dalam model time series.

Dalam tugas akhir, preprocessing penting karena penguji bisa menanyakan:

- Apakah format tanggal sudah benar?
- Apakah data sudah diurutkan berdasarkan waktu?
- Apakah ada missing value?
- Bagaimana cara menangani data kosong?
- Apakah data sudah sesuai frekuensi waktu?

## 11.2 Komponen yang perlu ditampilkan

### 11.2.1 Upload atau pemilihan dataset

Jika dashboard mendukung upload file, gunakan komponen:

```python
uploaded_file = st.file_uploader("Upload dataset", type=["csv", "xlsx"])
```

Jika dataset sudah tetap, cukup gunakan pilihan dataset:

```python
dataset_option = st.sidebar.selectbox("Pilih dataset", ["Data Penjualan", "Data Permintaan"])
```

### 11.2.2 Preview data mentah

Tampilkan beberapa baris awal data:

```python
st.dataframe(df.head())
```

Tujuannya agar pengguna tahu bentuk data yang digunakan.

### 11.2.3 Informasi kolom

Tampilkan:

- nama kolom tanggal,
- nama kolom target,
- tipe data setiap kolom,
- jumlah baris,
- jumlah kolom.

### 11.2.4 Validasi kolom tanggal

Kolom tanggal harus diubah ke format datetime:

```python
df[date_col] = pd.to_datetime(df[date_col])
```

Setelah itu data harus diurutkan:

```python
df = df.sort_values(date_col)
```

### 11.2.5 Validasi nilai target

Kolom target harus berupa numerik. Jika masih string, ubah ke numeric:

```python
df[target_col] = pd.to_numeric(df[target_col], errors="coerce")
```

### 11.2.6 Cek missing value

Tampilkan jumlah missing value:

```python
missing_values = df.isnull().sum()
st.dataframe(missing_values)
```

Jika ada missing value, jelaskan metode penanganannya, misalnya:

- menghapus baris kosong,
- interpolasi,
- forward fill,
- mengganti dengan nilai rata-rata,
- atau metode lain yang sesuai.

Untuk time series, interpolasi atau forward fill sering lebih masuk akal daripada langsung mengganti dengan rata-rata, tetapi harus disesuaikan dengan konteks data.

### 11.2.7 Cek duplikasi

Tampilkan jumlah data duplikat:

```python
duplicate_count = df.duplicated().sum()
st.metric("Jumlah Duplikasi", duplicate_count)
```

Jika ada duplikasi, jelaskan apakah dihapus atau digabung.

### 11.2.8 Resampling data

Jika data perlu dibuat bulanan, mingguan, atau harian, lakukan resampling.

Contoh resampling bulanan:

```python
df = df.set_index(date_col)
df_monthly = df[target_col].resample("M").sum()
```

Bagian ini penting jika data awal masih berupa transaksi harian tetapi model ingin memprediksi data bulanan.

### 11.2.9 Output data bersih

Tampilkan data akhir setelah preprocessing:

- jumlah data sebelum preprocessing,
- jumlah data setelah preprocessing,
- rentang tanggal akhir,
- contoh data hasil preprocessing.

## 11.3 Interpretasi yang perlu ditulis

Contoh narasi:

> Data telah melalui proses preprocessing dengan mengubah kolom tanggal ke format datetime, mengurutkan data berdasarkan waktu, memeriksa missing value, menghapus duplikasi, dan melakukan resampling bulanan agar sesuai dengan kebutuhan analisis time series. Data hasil preprocessing kemudian digunakan sebagai input untuk analisis dan pemodelan SARIMA.

---

# 12. Halaman 3 — Analisis Time Series

## 12.1 Tujuan halaman

Halaman ini digunakan untuk memahami karakteristik data sebelum model SARIMA dibuat. Dalam time series, analisis awal sangat penting karena model harus disesuaikan dengan pola data.

Halaman ini harus membantu menjawab:

- Apakah data memiliki tren?
- Apakah data memiliki musiman?
- Apakah data stasioner?
- Apakah perlu differencing?
- Apakah SARIMA memang relevan?

## 12.2 Komponen yang perlu ditampilkan

### 12.2.1 Grafik data historis

Tampilkan line chart data dari waktu ke waktu.

Grafik ini digunakan untuk membaca pola umum:

- apakah naik,
- apakah turun,
- apakah fluktuatif,
- apakah ada pola berulang.

### 12.2.2 Statistik deskriptif

Tampilkan statistik sederhana:

- mean,
- median,
- minimum,
- maximum,
- standard deviation,
- jumlah observasi.

Contoh:

```python
st.dataframe(df[target_col].describe())
```

### 12.2.3 Rolling mean dan rolling standard deviation

Rolling mean membantu melihat kecenderungan tren. Rolling standard deviation membantu melihat perubahan volatilitas.

Contoh:

```python
rolling_mean = series.rolling(window=12).mean()
rolling_std = series.rolling(window=12).std()
```

Untuk data bulanan, window 12 sering digunakan karena mewakili satu tahun.

### 12.2.4 Dekomposisi time series

Dekomposisi memisahkan data menjadi:

- trend,
- seasonality,
- residual.

Contoh:

```python
from statsmodels.tsa.seasonal import seasonal_decompose

decomposition = seasonal_decompose(series, model="additive", period=12)
```

Jika data bulanan dan memiliki pola tahunan, `period=12` biasanya digunakan. Jika data mingguan, period dapat disesuaikan.

### 12.2.5 Uji stasioneritas ADF

ADF Test digunakan untuk melihat apakah data stasioner atau tidak.

Yang perlu ditampilkan:

- ADF Statistic,
- p-value,
- critical value,
- keputusan.

Aturan sederhana:

```text
Jika p-value < 0.05 → data dianggap stasioner.
Jika p-value >= 0.05 → data belum stasioner.
```

### 12.2.6 Interpretasi ADF

Contoh interpretasi:

> Berdasarkan hasil ADF Test, nilai p-value lebih besar dari 0.05 sehingga data belum stasioner. Oleh karena itu, diperlukan proses differencing sebelum dilakukan pemodelan SARIMA.

Atau:

> Berdasarkan hasil ADF Test, nilai p-value lebih kecil dari 0.05 sehingga data dapat dianggap stasioner dan dapat dilanjutkan ke proses pemodelan.

### 12.2.7 Grafik ACF dan PACF awal

ACF dan PACF digunakan untuk membaca pola autokorelasi dan membantu pemilihan parameter model.

- ACF membantu membaca kemungkinan nilai `q` dan `Q`.
- PACF membantu membaca kemungkinan nilai `p` dan `P`.

Namun, untuk client atau penguji non-teknis, jangan terlalu panjang menjelaskan ACF/PACF. Cukup tampilkan grafik dan interpretasi singkat.

## 12.3 Interpretasi yang perlu ditulis

Contoh narasi:

> Hasil analisis time series menunjukkan bahwa data memiliki pola tren dan kemungkinan pola musiman. Hal ini terlihat dari grafik historis dan hasil dekomposisi. Karena terdapat indikasi pola musiman, metode SARIMA dipilih karena mampu menangani komponen non-musiman dan musiman dalam data time series.

---

# 13. Halaman 4 — Pemodelan SARIMA

## 13.1 Tujuan halaman

Halaman ini menjelaskan proses pembentukan model SARIMA. Ini adalah bagian penting karena menunjukkan bahwa model tidak dibuat secara asal, melainkan melalui proses pemilihan parameter dan training.

Halaman ini harus menjawab:

- Apa itu SARIMA secara singkat?
- Parameter apa yang digunakan?
- Bagaimana parameter dipilih?
- Bagaimana data training dan testing dibagi?
- Bagaimana model dilatih?

## 13.2 Penjelasan singkat SARIMA

Tambahkan penjelasan singkat:

> SARIMA adalah pengembangan dari ARIMA yang digunakan untuk memodelkan data time series dengan pola musiman. SARIMA memiliki parameter non-musiman `(p,d,q)` dan parameter musiman `(P,D,Q,s)`, sehingga lebih sesuai digunakan ketika data memiliki pola berulang pada periode tertentu.

Jangan terlalu panjang menjelaskan teori di dashboard. Penjelasan teoritis detail sebaiknya tetap ada di laporan TA, bukan memenuhi dashboard.

## 13.3 Parameter SARIMA

Parameter SARIMA terdiri dari:

```text
SARIMA(p, d, q)(P, D, Q, s)
```

Penjelasan:

| Parameter | Makna |
|---|---|
| p | orde autoregressive non-musiman |
| d | jumlah differencing non-musiman |
| q | orde moving average non-musiman |
| P | orde autoregressive musiman |
| D | jumlah differencing musiman |
| Q | orde moving average musiman |
| s | panjang periode musiman |

Contoh untuk data bulanan:

```text
SARIMA(1,1,1)(1,1,1,12)
```

Artinya data menggunakan komponen non-musiman `(1,1,1)` dan komponen musiman `(1,1,1,12)` dengan periode musiman 12 bulan.

## 13.4 Metode pemilihan parameter

Ada dua opsi pemilihan parameter:

### 13.4.1 Manual berdasarkan ACF/PACF

Jika parameter dipilih manual, tampilkan alasan singkat:

> Parameter dipilih berdasarkan pola ACF dan PACF setelah proses differencing. Nilai p dan q ditentukan dari lag signifikan pada grafik PACF dan ACF, sedangkan parameter musiman ditentukan berdasarkan pola lag musiman.

### 13.4.2 Otomatis berdasarkan AIC/BIC

Jika menggunakan auto search, tampilkan:

- kombinasi parameter yang diuji,
- parameter terbaik,
- nilai AIC/BIC,
- alasan model dipilih.

Contoh narasi:

> Model terbaik dipilih berdasarkan nilai AIC terkecil dari beberapa kombinasi parameter SARIMA. Semakin kecil nilai AIC, semakin baik keseimbangan antara akurasi model dan kompleksitas model.

## 13.5 Pembagian data training dan testing

Untuk evaluasi model, data sebaiknya dibagi menjadi train dan test.

Contoh:

```text
Data training: 80%
Data testing : 20%
```

Atau untuk time series:

```text
Data training: Januari 2018 - Desember 2022
Data testing : Januari 2023 - Desember 2023
```

Penting: jangan melakukan split secara acak. Untuk time series, pembagian harus mengikuti urutan waktu.

## 13.6 Training model

Contoh implementasi:

```python
from statsmodels.tsa.statespace.sarimax import SARIMAX

model = SARIMAX(
    train,
    order=(p, d, q),
    seasonal_order=(P, D, Q, s),
    enforce_stationarity=False,
    enforce_invertibility=False
)

model_fit = model.fit()
```

## 13.7 Output yang perlu ditampilkan

Tampilkan informasi berikut:

- parameter model,
- nilai AIC,
- nilai BIC jika digunakan,
- jumlah data training,
- jumlah data testing,
- status training model,
- ringkasan model jika diperlukan.

Namun, ringkasan model statistik yang terlalu panjang sebaiknya dimasukkan ke dalam `st.expander()` agar tampilan tidak padat.

Contoh:

```python
with st.expander("Lihat Ringkasan Model"):
    st.text(model_fit.summary())
```

---

# 14. Halaman 5 — Evaluasi & Diagnostik Model

## 14.1 Tujuan halaman

Halaman ini digunakan untuk membuktikan bahwa model yang dibuat memiliki performa yang dapat diterima. Ini adalah salah satu bagian paling penting untuk tugas akhir.

Halaman ini harus menjawab:

- Seberapa besar error model?
- Apakah model cukup baik mengikuti data aktual?
- Apakah residual model masih berpola?
- Apakah SARIMA lebih baik dibanding baseline sederhana?

## 14.2 Metrik evaluasi

Metrik yang disarankan:

### 14.2.1 MAE

MAE mengukur rata-rata selisih absolut antara data aktual dan prediksi.

```text
MAE kecil → prediksi lebih dekat dengan nilai aktual.
```

### 14.2.2 RMSE

RMSE memberikan penalti lebih besar terhadap error yang besar.

```text
RMSE kecil → model lebih stabil terhadap kesalahan besar.
```

### 14.2.3 MAPE

MAPE mengukur rata-rata persentase error.

```text
MAPE kecil → persentase kesalahan model semakin rendah.
```

MAPE mudah dipahami oleh client karena berbentuk persentase. Namun, MAPE kurang cocok jika data memiliki nilai nol atau sangat kecil.

## 14.3 Tabel evaluasi model

Tampilkan tabel:

| Metrik | Nilai | Interpretasi |
|---|---:|---|
| MAE | ... | Rata-rata error absolut model |
| RMSE | ... | Error model dengan penalti besar |
| MAPE | ... | Rata-rata persentase kesalahan |

## 14.4 Grafik aktual vs prediksi

Tampilkan grafik yang membandingkan data testing aktual dan prediksi model.

Tujuannya agar pengguna bisa melihat apakah model mengikuti pola data aktual.

## 14.5 Diagnostik residual

Residual adalah selisih antara nilai aktual dan nilai prediksi.

```text
Residual = Aktual - Prediksi
```

Diagnostik residual penting karena model yang baik idealnya memiliki residual yang acak dan tidak menyimpan pola besar.

Komponen yang disarankan:

1. Plot residual dari waktu ke waktu.
2. Distribusi residual.
3. ACF residual.
4. Uji Ljung-Box jika memungkinkan.

## 14.6 Interpretasi residual

Contoh interpretasi:

> Plot residual menunjukkan bahwa error model menyebar di sekitar nilai nol dan tidak membentuk pola tren yang kuat. Hal ini menunjukkan bahwa model sudah cukup baik dalam menangkap pola utama data.

Jika residual masih berpola:

> Residual masih menunjukkan pola tertentu, sehingga model kemungkinan belum sepenuhnya menangkap karakteristik data. Perbaikan dapat dilakukan dengan menguji kombinasi parameter SARIMA lain atau membandingkan dengan metode forecasting lain.

## 14.7 Perbandingan dengan baseline model

Agar SARIMA terlihat lebih kuat, disarankan menambahkan baseline sederhana.

Baseline yang dapat digunakan:

- Naive Forecast,
- Moving Average,
- Seasonal Naive,
- ARIMA non-musiman.

Contoh tabel:

| Model | MAE | RMSE | MAPE | Keterangan |
|---|---:|---:|---:|---|
| Naive Forecast | ... | ... | ... | Baseline sederhana |
| Moving Average | ... | ... | ... | Pembanding sederhana |
| SARIMA | ... | ... | ... | Model utama penelitian |

Jika SARIMA lebih baik, narasinya:

> Berdasarkan hasil evaluasi, model SARIMA menghasilkan nilai error yang lebih rendah dibandingkan baseline sederhana, sehingga SARIMA dipilih sebagai model utama untuk menghasilkan forecast.

Jika SARIMA tidak lebih baik, tetap jujur:

> Berdasarkan hasil evaluasi, performa SARIMA belum lebih baik dibandingkan baseline. Hal ini dapat disebabkan oleh pola data yang kurang musiman, jumlah data yang terbatas, atau parameter model yang belum optimal.

Kejujuran seperti ini justru terlihat lebih akademik.

---

# 15. Halaman 6 — Forecasting & Interpretasi

## 15.1 Tujuan halaman

Halaman ini menampilkan hasil akhir dari proses forecasting. Halaman ini harus mudah dipahami oleh client dan penguji.

Halaman ini harus menjawab:

- Berapa prediksi periode berikutnya?
- Bagaimana tren ke depan?
- Apakah hasil forecast naik atau turun?
- Seberapa lebar rentang ketidakpastian forecast?
- Apa interpretasi hasilnya?

## 15.2 Input horizon forecast

Tambahkan input horizon forecast pada sidebar.

Contoh:

```python
forecast_steps = st.sidebar.slider("Horizon Forecast", min_value=1, max_value=24, value=12)
```

Untuk data bulanan, horizon 12 berarti prediksi 12 bulan ke depan.

## 15.3 Grafik forecast

Grafik forecast harus menampilkan:

- data historis,
- data testing jika ada,
- hasil prediksi,
- confidence interval.

Confidence interval penting agar hasil forecast tidak terlihat sebagai angka yang pasti sepenuhnya.

## 15.4 Tabel hasil forecast

Tabel hasil forecast sebaiknya berisi:

| Periode | Forecast | Lower Bound | Upper Bound |
|---|---:|---:|---:|
| 2024-01 | ... | ... | ... |
| 2024-02 | ... | ... | ... |
| 2024-03 | ... | ... | ... |

Jika ingin lebih informatif, tambahkan kolom:

- perubahan dari periode sebelumnya,
- persentase perubahan,
- kategori tren.

Contoh:

| Periode | Forecast | Perubahan | Tren |
|---|---:|---:|---|
| 2024-01 | 1.200 | +50 | Naik |
| 2024-02 | 1.260 | +60 | Naik |

## 15.5 Interpretasi hasil forecast

Interpretasi harus singkat dan langsung menjelaskan makna grafik.

Contoh jika tren naik:

> Hasil forecast menunjukkan adanya kecenderungan peningkatan pada beberapa periode mendatang. Pola ini menunjukkan bahwa permintaan atau penjualan diperkirakan mengalami kenaikan secara bertahap.

Contoh jika tren turun:

> Hasil forecast menunjukkan kecenderungan penurunan pada periode mendatang. Kondisi ini perlu diperhatikan karena dapat mengindikasikan pelemahan permintaan berdasarkan pola historis.

Contoh jika fluktuatif:

> Hasil forecast menunjukkan pola yang berfluktuasi, namun masih mengikuti pola musiman yang terlihat pada data historis. Hal ini menunjukkan bahwa faktor musiman masih memengaruhi nilai prediksi ke depan.

## 15.6 Download hasil forecast

Tambahkan fitur download:

```python
csv = forecast_df.to_csv(index=False)

st.download_button(
    label="Download Hasil Forecast",
    data=csv,
    file_name="hasil_forecast.csv",
    mime="text/csv"
)
```

Fitur ini sederhana tetapi memberi kesan profesional.

---

# 16. Halaman 7 — Kesimpulan / Rekomendasi Ringkas

## 16.1 Tujuan halaman

Halaman ini digunakan untuk merangkum hasil penelitian dan memberikan interpretasi akhir.

Halaman ini tidak perlu terlalu panjang. Fokusnya adalah menyimpulkan:

- data yang digunakan,
- model yang dipilih,
- performa model,
- hasil forecast,
- saran pengembangan.

## 16.2 Isi yang disarankan

### 16.2.1 Kesimpulan data

Contoh:

> Data yang digunakan merupakan data time series dengan periode bulanan. Berdasarkan hasil analisis, data menunjukkan adanya pola tren dan musiman sehingga metode SARIMA relevan digunakan.

### 16.2.2 Kesimpulan model

Contoh:

> Model SARIMA dengan parameter tertentu dipilih karena menghasilkan nilai evaluasi yang lebih baik dibandingkan baseline sederhana dan mampu mengikuti pola historis data dengan cukup baik.

### 16.2.3 Kesimpulan forecast

Contoh:

> Hasil forecast menunjukkan bahwa nilai pada periode mendatang diperkirakan mengalami peningkatan secara bertahap dengan rentang ketidakpastian yang masih wajar berdasarkan confidence interval.

### 16.2.4 Saran pengembangan

Contoh:

> Pengembangan selanjutnya dapat dilakukan dengan membandingkan metode SARIMA dengan model lain seperti Prophet, LSTM, atau XGBoost, serta menambahkan data eksternal agar hasil forecast lebih akurat.

---

# 17. Navigasi Dashboard

Navigasi yang paling disarankan adalah menggunakan sidebar.

Contoh menu:

```text
Sidebar
├── Overview Penelitian
├── Data & Preprocessing
├── Analisis Time Series
├── Pemodelan SARIMA
├── Evaluasi & Diagnostik
├── Forecasting & Interpretasi
└── Kesimpulan
```

Sidebar juga dapat memuat input global seperti:

- upload dataset,
- pilihan kolom tanggal,
- pilihan kolom target,
- frekuensi data,
- horizon forecast,
- parameter SARIMA,
- tombol proses model.

---

# 18. Wireframe Dashboard Final

## 18.1 Wireframe umum

```text
+------------------------------------------------------+
| SIDEBAR                                              |
| - Upload / pilih dataset                             |
| - Pilih halaman                                      |
| - Pilih kolom tanggal                                |
| - Pilih kolom target                                 |
| - Pilih frekuensi data                               |
| - Horizon forecast                                   |
| - Parameter SARIMA                                   |
| - Tombol jalankan model                              |
+------------------------------------------------------+

+------------------------------------------------------+
| JUDUL HALAMAN                                        |
| Deskripsi singkat halaman                            |
+------------------------------------------------------+

+------------------------------------------------------+
| Metric 1 | Metric 2 | Metric 3 | Metric 4           |
+------------------------------------------------------+

+------------------------------------------------------+
| Grafik utama                                         |
+------------------------------------------------------+

+------------------------------------------------------+
| Tabel / Grafik pendukung                             |
+------------------------------------------------------+

+------------------------------------------------------+
| Interpretasi singkat                                 |
+------------------------------------------------------+
```

## 18.2 Wireframe halaman overview

```text
Judul Dashboard
Deskripsi singkat penelitian

[Total Data] [Periode Data] [Aktual Terakhir] [Forecast Berikutnya]

Grafik Historis + Forecast Ringkas

Insight Singkat
```

## 18.3 Wireframe halaman preprocessing

```text
Judul: Data & Preprocessing

Upload / Pilih Dataset
Preview Data Mentah

[Jumlah Baris] [Jumlah Kolom] [Missing Value] [Duplikasi]

Tabel Info Kolom
Tabel Missing Value
Data Setelah Preprocessing

Catatan Proses Preprocessing
```

## 18.4 Wireframe halaman analisis time series

```text
Judul: Analisis Time Series

Grafik Data Historis
Statistik Deskriptif
Rolling Mean & Rolling Std
Dekomposisi Trend / Seasonal / Residual
ADF Test
ACF & PACF
Interpretasi Pola Data
```

## 18.5 Wireframe halaman pemodelan

```text
Judul: Pemodelan SARIMA

Penjelasan Singkat SARIMA
Parameter Model
Train-Test Split
AIC / BIC
Hasil Fitting Model
Ringkasan Model dalam Expander
```

## 18.6 Wireframe halaman evaluasi

```text
Judul: Evaluasi & Diagnostik Model

[MAE] [RMSE] [MAPE]

Grafik Aktual vs Prediksi
Tabel Evaluasi
Plot Residual
ACF Residual
Perbandingan Baseline vs SARIMA
Interpretasi Evaluasi
```

## 18.7 Wireframe halaman forecast

```text
Judul: Forecasting & Interpretasi

Input Horizon Forecast
Grafik Forecast + Confidence Interval
Tabel Hasil Forecast
Download CSV
Interpretasi Hasil
```

---

# 19. Struktur File Project

Struktur project yang disarankan:

```text
project-sarima-dashboard/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── raw/
│   │   └── dataset.csv
│   └── processed/
│       └── dataset_clean.csv
│
├── src/
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── analysis.py
│   ├── modeling.py
│   ├── evaluation.py
│   ├── forecasting.py
│   └── visualization.py
│
├── pages/
│   ├── 1_Overview.py
│   ├── 2_Data_Preprocessing.py
│   ├── 3_Analisis_Time_Series.py
│   ├── 4_Pemodelan_SARIMA.py
│   ├── 5_Evaluasi_Diagnostik.py
│   ├── 6_Forecasting_Interpretasi.py
│   └── 7_Kesimpulan.py
│
└── assets/
    └── images/
```

Jika ingin sederhana, semua bisa dibuat dalam satu `app.py`. Namun untuk project yang rapi dan mudah dijelaskan, struktur modular lebih disarankan.

---

# 20. Penjelasan Modul Project

## 20.1 `app.py`

File utama untuk menjalankan aplikasi Streamlit.

Berisi:

- konfigurasi halaman,
- sidebar utama,
- pemanggilan halaman,
- pengaturan session state jika diperlukan.

## 20.2 `data_loader.py`

Berfungsi untuk membaca data dari CSV atau Excel.

Isi fungsi:

- membaca file,
- validasi format file,
- mengembalikan dataframe.

## 20.3 `preprocessing.py`

Berisi fungsi preprocessing:

- konversi tanggal,
- sorting data,
- handling missing value,
- handling duplikasi,
- resampling,
- agregasi data.

## 20.4 `analysis.py`

Berisi fungsi analisis time series:

- statistik deskriptif,
- rolling mean,
- rolling standard deviation,
- decomposition,
- ADF test,
- ACF/PACF.

## 20.5 `modeling.py`

Berisi fungsi pemodelan SARIMA:

- train-test split,
- training SARIMA,
- auto parameter search jika digunakan,
- penyimpanan hasil model.

## 20.6 `evaluation.py`

Berisi fungsi evaluasi:

- MAE,
- RMSE,
- MAPE,
- residual analysis,
- baseline comparison.

## 20.7 `forecasting.py`

Berisi fungsi forecast:

- forecast beberapa periode ke depan,
- confidence interval,
- pembuatan tabel hasil forecast.

## 20.8 `visualization.py`

Berisi fungsi visualisasi:

- plot historis,
- plot forecast,
- plot actual vs predicted,
- plot residual,
- plot decomposition.

---

# 21. Rekomendasi Tech Stack

## 21.1 Library utama

```text
streamlit
pandas
numpy
statsmodels
scikit-learn
matplotlib
plotly
openpyxl
```

## 21.2 Library opsional

```text
pmdarima
seaborn
scipy
```

Catatan:

- `pmdarima` berguna untuk `auto_arima`, tetapi kadang instalasinya bisa bermasalah tergantung environment.
- Jika ingin lebih aman, parameter SARIMA bisa ditentukan manual atau dengan grid search sederhana.
- `plotly` disarankan untuk grafik interaktif di dashboard.

---

# 22. Format Dataset yang Disarankan

Dataset minimal sebaiknya memiliki dua kolom utama:

| tanggal | nilai |
|---|---:|
| 2020-01-01 | 120 |
| 2020-02-01 | 135 |
| 2020-03-01 | 128 |

Kolom wajib:

1. Kolom tanggal / periode.
2. Kolom nilai target yang ingin diprediksi.

Kolom opsional:

- nama produk,
- kategori,
- cabang,
- wilayah,
- stok,
- target penjualan.

Namun untuk versi TA yang aman, cukup gunakan satu variabel target terlebih dahulu.

---

# 23. Validasi Dataset

Sebelum model dijalankan, sistem perlu melakukan validasi:

1. Dataset tidak kosong.
2. Kolom tanggal tersedia.
3. Kolom target tersedia.
4. Kolom tanggal bisa dikonversi ke datetime.
5. Kolom target bisa dikonversi ke numerik.
6. Data memiliki jumlah observasi yang cukup.
7. Data sudah memiliki urutan waktu yang benar.
8. Frekuensi data sesuai dengan parameter musiman.

Jika validasi gagal, tampilkan pesan yang jelas.

Contoh:

```text
Data tidak dapat diproses karena kolom tanggal tidak ditemukan.
```

Atau:

```text
Jumlah data terlalu sedikit untuk membangun model SARIMA musiman. Gunakan minimal 2 siklus musiman.
```

---

# 24. Aturan Jumlah Data Minimum

Untuk SARIMA, jumlah data harus cukup. Jika data bulanan dengan pola tahunan, minimal idealnya ada lebih dari 24 data atau 2 tahun data. Lebih baik lagi jika ada 36 sampai 60 observasi.

Contoh:

| Frekuensi | Seasonal Period | Minimal Data yang Disarankan |
|---|---:|---:|
| Bulanan | 12 | minimal 24–36 data |
| Mingguan | 52 | minimal 104 data |
| Harian | 7 atau 365 | tergantung pola musiman |

Jika data terlalu sedikit, model SARIMA bisa tidak stabil.

---

# 25. Strategi Pemilihan Parameter SARIMA

Ada tiga strategi yang bisa dipilih.

## 25.1 Strategi sederhana

Gunakan parameter tetap yang sudah diuji.

Kelebihan:

- mudah diimplementasikan,
- stabil,
- cocok untuk TA jika waktu terbatas.

Kekurangan:

- kurang fleksibel,
- harus ada alasan pemilihan parameter.

## 25.2 Strategi manual berdasarkan ACF/PACF

Gunakan hasil ACF dan PACF untuk menentukan parameter.

Kelebihan:

- lebih akademik,
- mudah dijelaskan saat sidang.

Kekurangan:

- membutuhkan pemahaman lebih baik,
- interpretasi bisa subjektif.

## 25.3 Strategi auto search berdasarkan AIC

Sistem mencoba beberapa kombinasi parameter dan memilih yang AIC-nya paling kecil.

Kelebihan:

- lebih otomatis,
- terlihat kuat secara teknis.

Kekurangan:

- bisa lambat,
- perlu pembatasan kombinasi parameter,
- rawan error jika data sedikit.

## 25.4 Rekomendasi

Untuk project TA, strategi paling aman adalah:

```text
Gunakan ACF/PACF sebagai dasar penjelasan,
lalu gunakan AIC untuk memilih model terbaik dari beberapa kandidat.
```

Dengan begitu, dashboard tetap terlihat akademik dan juga praktis.

---

# 26. Evaluasi Model yang Disarankan

Evaluasi minimal:

1. MAE
2. RMSE
3. MAPE

Evaluasi tambahan:

1. AIC
2. BIC
3. Residual plot
4. Ljung-Box test
5. Baseline comparison

Jika waktu terbatas, cukup gunakan:

```text
MAE + RMSE + MAPE + Grafik Aktual vs Prediksi
```

Jika ingin lebih kuat, tambahkan:

```text
Residual Plot + ACF Residual + Baseline Comparison
```

---

# 27. Interpretasi Hasil Evaluasi

Dashboard harus menyediakan interpretasi singkat agar angka tidak berdiri sendiri.

Contoh:

```text
Nilai MAPE sebesar 8.4% menunjukkan bahwa rata-rata kesalahan prediksi model berada pada kisaran 8.4% terhadap nilai aktual. Semakin kecil nilai MAPE, semakin baik performa model.
```

Contoh lain:

```text
Grafik aktual vs prediksi menunjukkan bahwa model mampu mengikuti pola utama data testing, meskipun masih terdapat beberapa selisih pada periode dengan fluktuasi tinggi.
```

---

# 28. Fitur Dashboard Berdasarkan Prioritas

## 28.1 Prioritas Wajib

| Fitur | Keterangan |
|---|---|
| Load dataset | Membaca data CSV/Excel |
| Preview data | Menampilkan data mentah |
| Preprocessing | Membersihkan dan menyiapkan data |
| Grafik historis | Melihat pola data |
| Statistik deskriptif | Memahami karakter data |
| Dekomposisi | Melihat trend dan seasonality |
| ADF Test | Menguji stasioneritas |
| ACF/PACF | Mendukung pemilihan parameter |
| SARIMA model | Model utama forecasting |
| Evaluasi model | Mengukur performa model |
| Forecast chart | Menampilkan hasil prediksi |
| Forecast table | Menampilkan angka prediksi |
| Interpretasi | Menjelaskan hasil |

## 28.2 Prioritas Sangat Disarankan

| Fitur | Keterangan |
|---|---|
| Train-test split | Evaluasi lebih jelas |
| Confidence interval | Menunjukkan ketidakpastian prediksi |
| Download forecast | Memudahkan penggunaan hasil |
| Residual diagnostic | Memperkuat evaluasi model |
| Baseline comparison | Membuktikan SARIMA lebih layak |

## 28.3 Prioritas Opsional

| Fitur | Keterangan |
|---|---|
| Multi produk | Jika dataset memiliki banyak produk |
| Multi cabang | Jika dataset memiliki banyak cabang |
| Alert sederhana | Jika ada threshold bisnis |
| Rekomendasi stok | Jika ada data stok |
| Export report PDF | Jika dibutuhkan untuk laporan |

---

# 29. Fitur yang Sebaiknya Ditunda

Fitur berikut sebaiknya tidak dikerjakan di awal:

1. Login user.
2. Role management.
3. Dashboard admin.
4. Database online.
5. Notifikasi email.
6. Integrasi API eksternal.
7. Model machine learning kompleks.
8. Deployment production-level.

Alasannya sederhana: fitur-fitur tersebut tidak langsung memperkuat inti TA, yaitu forecasting menggunakan SARIMA.

---

# 30. Risiko Project dan Solusi

## 30.1 Data terlalu sedikit

Risiko:

- model SARIMA tidak stabil,
- hasil forecast kurang akurat,
- parameter musiman sulit ditentukan.

Solusi:

- gunakan periode data lebih panjang,
- sederhanakan model menjadi ARIMA,
- gunakan baseline sederhana sebagai pembanding,
- jelaskan keterbatasan data di laporan.

## 30.2 Data tidak memiliki pola musiman

Risiko:

- SARIMA kurang relevan,
- hasil model tidak lebih baik dari ARIMA.

Solusi:

- tampilkan dekomposisi,
- bandingkan dengan ARIMA,
- jika pola musiman lemah, jelaskan sebagai temuan penelitian.

## 30.3 Error model besar

Risiko:

- forecast kurang meyakinkan,
- penguji mempertanyakan kualitas model.

Solusi:

- lakukan tuning parameter,
- cek preprocessing,
- cek outlier,
- bandingkan dengan baseline,
- jelaskan kemungkinan penyebab error.

## 30.4 Dashboard terlalu penuh

Risiko:

- pengguna bingung,
- tampilan kurang profesional.

Solusi:

- gunakan sidebar,
- pisahkan halaman,
- gunakan expander untuk detail teknis,
- tulis interpretasi singkat.

## 30.5 Model terlalu lambat

Risiko:

- dashboard terasa berat,
- user harus menunggu lama.

Solusi:

- cache proses dengan `st.cache_data` atau `st.cache_resource`,
- batasi kombinasi parameter,
- gunakan data yang sudah diproses,
- hindari auto search terlalu luas.

---

# 31. Strategi Implementasi Bertahap

## Tahap 1 — Fondasi Dashboard

Target:

- membuat struktur project,
- membuat sidebar,
- membuat navigasi halaman,
- menampilkan dataset,
- membuat preview data.

Output:

- dashboard bisa dibuka,
- data bisa dibaca,
- halaman dasar sudah terbentuk.

## Tahap 2 — Preprocessing

Target:

- validasi kolom tanggal,
- validasi kolom target,
- cleaning missing value,
- sorting data,
- resampling data.

Output:

- data bersih siap dianalisis.

## Tahap 3 — Analisis Time Series

Target:

- grafik historis,
- statistik deskriptif,
- rolling mean,
- decomposition,
- ADF test,
- ACF/PACF.

Output:

- karakteristik data terlihat jelas.

## Tahap 4 — Pemodelan SARIMA

Target:

- train-test split,
- training model,
- pemilihan parameter,
- hasil fitting.

Output:

- model SARIMA berhasil dibuat.

## Tahap 5 — Evaluasi Model

Target:

- MAE,
- RMSE,
- MAPE,
- actual vs predicted,
- residual diagnostic.

Output:

- performa model dapat dijelaskan.

## Tahap 6 — Forecasting

Target:

- forecast beberapa periode ke depan,
- confidence interval,
- tabel hasil prediksi,
- interpretasi hasil,
- download CSV.

Output:

- hasil akhir penelitian dapat ditampilkan.

## Tahap 7 — Finalisasi UI dan Dokumentasi

Target:

- memperbaiki layout,
- menambahkan narasi,
- membuat README,
- menyiapkan screenshot,
- menyiapkan penjelasan sidang.

Output:

- dashboard siap dipresentasikan.

---

# 32. Estimasi Timeline Pengerjaan

Estimasi jika dikerjakan secara rapi:

| Tahap | Durasi Estimasi | Output |
|---|---:|---|
| Setup project | 1 hari | Struktur project dan Streamlit berjalan |
| Load & preprocessing data | 1–2 hari | Data bersih siap pakai |
| Analisis time series | 1–2 hari | Grafik, ADF, decomposition, ACF/PACF |
| Pemodelan SARIMA | 2–3 hari | Model berhasil dilatih |
| Evaluasi model | 1–2 hari | Metrik error dan grafik evaluasi |
| Forecasting | 1–2 hari | Hasil prediksi dan tabel forecast |
| UI polishing | 1–2 hari | Dashboard rapi dan siap demo |
| Dokumentasi | 1 hari | README dan catatan sidang |

Total realistis:

```text
9–15 hari kerja
```

Jika data sudah bersih dan parameter model tidak rumit, bisa lebih cepat. Jika data bermasalah, bisa lebih lama.

---

# 33. Checklist MVP

Gunakan checklist ini untuk memastikan versi minimum sudah layak.

## 33.1 Data

- [ ] Dataset berhasil dibaca.
- [ ] Kolom tanggal valid.
- [ ] Kolom target valid.
- [ ] Missing value dicek.
- [ ] Duplikasi dicek.
- [ ] Data sudah diurutkan berdasarkan waktu.
- [ ] Data sudah sesuai frekuensi analisis.

## 33.2 Analisis

- [ ] Grafik time series tersedia.
- [ ] Statistik deskriptif tersedia.
- [ ] Rolling mean tersedia.
- [ ] Dekomposisi tersedia.
- [ ] ADF Test tersedia.
- [ ] ACF/PACF tersedia.
- [ ] Interpretasi singkat tersedia.

## 33.3 Model

- [ ] Parameter SARIMA ditampilkan.
- [ ] Train-test split jelas.
- [ ] Model berhasil dilatih.
- [ ] Hasil fitting ditampilkan.
- [ ] AIC/BIC ditampilkan jika digunakan.

## 33.4 Evaluasi

- [ ] MAE tersedia.
- [ ] RMSE tersedia.
- [ ] MAPE tersedia.
- [ ] Grafik actual vs predicted tersedia.
- [ ] Interpretasi evaluasi tersedia.

## 33.5 Forecast

- [ ] Horizon forecast dapat dipilih.
- [ ] Grafik forecast tersedia.
- [ ] Confidence interval tersedia.
- [ ] Tabel forecast tersedia.
- [ ] Interpretasi hasil tersedia.
- [ ] Download forecast tersedia jika memungkinkan.

---

# 34. Checklist Sebelum Sidang

Sebelum dashboard dipresentasikan, pastikan:

- [ ] Dashboard bisa dijalankan tanpa error.
- [ ] Semua halaman dapat dibuka.
- [ ] Dataset sudah tersedia.
- [ ] Tidak ada chart kosong.
- [ ] Tidak ada metric bernilai error/NaN tanpa penjelasan.
- [ ] Forecast berhasil muncul.
- [ ] Interpretasi tidak bertentangan dengan grafik.
- [ ] Parameter model dapat dijelaskan.
- [ ] Nilai error dapat dijelaskan.
- [ ] Alasan menggunakan SARIMA dapat dijelaskan.
- [ ] Keterbatasan penelitian sudah disiapkan.

---

# 35. Pertanyaan yang Mungkin Muncul Saat Sidang

## 35.1 Mengapa menggunakan SARIMA?

Jawaban yang bisa disiapkan:

> SARIMA digunakan karena data yang dianalisis merupakan data time series dan memiliki indikasi pola musiman. SARIMA mampu menangani komponen non-musiman dan musiman melalui parameter `(p,d,q)` dan `(P,D,Q,s)`.

## 35.2 Apa bedanya ARIMA dan SARIMA?

Jawaban:

> ARIMA digunakan untuk data time series tanpa komponen musiman yang kuat, sedangkan SARIMA menambahkan parameter musiman sehingga lebih sesuai untuk data yang memiliki pola berulang dalam periode tertentu.

## 35.3 Bagaimana menentukan parameter model?

Jawaban:

> Parameter ditentukan berdasarkan analisis ACF/PACF dan pemilihan model terbaik menggunakan nilai AIC/BIC. Model dengan nilai AIC lebih kecil dipilih karena menunjukkan keseimbangan yang lebih baik antara kecocokan model dan kompleksitas.

## 35.4 Mengapa data harus stasioner?

Jawaban:

> Data stasioner diperlukan karena model time series seperti ARIMA/SARIMA bekerja lebih baik ketika karakteristik statistik data relatif stabil terhadap waktu. Jika data belum stasioner, proses differencing dilakukan.

## 35.5 Apa arti MAPE?

Jawaban:

> MAPE menunjukkan rata-rata persentase kesalahan prediksi terhadap nilai aktual. Semakin kecil MAPE, semakin baik performa prediksi model.

## 35.6 Apa fungsi confidence interval?

Jawaban:

> Confidence interval menunjukkan rentang ketidakpastian prediksi. Forecast tidak dianggap sebagai nilai pasti, tetapi sebagai estimasi dengan batas bawah dan batas atas.

## 35.7 Apa keterbatasan penelitian ini?

Jawaban:

> Keterbatasannya adalah model hanya menggunakan data historis variabel target. Faktor eksternal seperti promosi, kondisi ekonomi, hari libur, atau perubahan pasar belum dimasukkan, sehingga hasil forecast sangat bergantung pada pola historis data.

---

# 36. Rekomendasi Desain UI

## 36.1 Warna

Gunakan warna netral:

- putih,
- abu-abu muda,
- biru tua,
- hijau gelap,
- hitam untuk teks utama.

Hindari warna terlalu ramai karena dashboard akademik harus terlihat formal.

## 36.2 Layout

Gunakan pola layout:

```text
Judul
Deskripsi
Metric
Grafik utama
Tabel pendukung
Interpretasi
```

Pola ini konsisten dan mudah dibaca.

## 36.3 Grafik

Grafik yang disarankan:

- line chart untuk time series,
- decomposition plot,
- ACF/PACF plot,
- actual vs predicted line chart,
- forecast chart dengan confidence interval,
- residual plot.

## 36.4 Tabel

Tabel yang disarankan:

- preview dataset,
- statistik deskriptif,
- hasil ADF,
- parameter model,
- metrik evaluasi,
- hasil forecast.

## 36.5 Penjelasan

Setiap halaman sebaiknya memiliki interpretasi singkat. Jangan hanya menampilkan grafik dan tabel tanpa narasi.

Format yang baik:

```text
Berdasarkan grafik di atas, terlihat bahwa ...
Hal ini menunjukkan bahwa ...
Dengan demikian, ...
```

---

# 37. Rekomendasi Komponen Streamlit

| Kebutuhan | Komponen Streamlit |
|---|---|
| Judul halaman | `st.title()` |
| Subjudul | `st.subheader()` |
| Deskripsi | `st.write()` / `st.markdown()` |
| Sidebar | `st.sidebar` |
| Upload file | `st.file_uploader()` |
| Pilihan kolom | `st.selectbox()` |
| Horizon forecast | `st.slider()` |
| Metric card | `st.metric()` |
| Tabel | `st.dataframe()` |
| Grafik | `st.pyplot()` / `st.plotly_chart()` |
| Detail tambahan | `st.expander()` |
| Loading process | `st.spinner()` |
| Download file | `st.download_button()` |
| Cache data | `st.cache_data()` |
| Cache model | `st.cache_resource()` |

---

# 38. Contoh Struktur Sidebar

```python
st.sidebar.title("Pengaturan Dashboard")

page = st.sidebar.radio(
    "Pilih Halaman",
    [
        "Overview",
        "Data & Preprocessing",
        "Analisis Time Series",
        "Pemodelan SARIMA",
        "Evaluasi & Diagnostik",
        "Forecasting",
        "Kesimpulan"
    ]
)

uploaded_file = st.sidebar.file_uploader("Upload Dataset", type=["csv", "xlsx"])

forecast_steps = st.sidebar.slider(
    "Horizon Forecast",
    min_value=1,
    max_value=24,
    value=12
)
```

---

# 39. Contoh Alur Kode Sederhana

```python
# 1. Load data
# 2. Preprocessing
# 3. Analisis time series
# 4. Train-test split
# 5. Build SARIMA model
# 6. Evaluate model
# 7. Forecast future values
# 8. Visualize results
```

Contoh alur utama:

```python
if uploaded_file is not None:
    df = load_data(uploaded_file)
    clean_df = preprocess_data(df, date_col, target_col)
    series = clean_df[target_col]

    if page == "Overview":
        show_overview(clean_df, series)

    elif page == "Data & Preprocessing":
        show_preprocessing(df, clean_df)

    elif page == "Analisis Time Series":
        show_time_series_analysis(series)

    elif page == "Pemodelan SARIMA":
        model_fit = train_sarima(series)
        show_modeling_result(model_fit)

    elif page == "Evaluasi & Diagnostik":
        evaluation_result = evaluate_model(series, model_fit)
        show_evaluation(evaluation_result)

    elif page == "Forecasting":
        forecast_df = generate_forecast(model_fit, forecast_steps)
        show_forecast(forecast_df)
```

---

# 40. Acceptance Criteria

Project dapat dianggap selesai jika memenuhi kriteria berikut:

## 40.1 Dari sisi fitur

- Dashboard dapat membaca dataset.
- Data dapat diproses dan divalidasi.
- Grafik historis dapat ditampilkan.
- Analisis time series tersedia.
- Model SARIMA dapat dijalankan.
- Evaluasi model dapat ditampilkan.
- Forecast dapat dihasilkan.
- Hasil forecast dapat dibaca dalam grafik dan tabel.
- Interpretasi tersedia di setiap bagian penting.

## 40.2 Dari sisi akademik

- Alur penelitian terlihat jelas.
- Pemilihan SARIMA memiliki alasan.
- Evaluasi model tersedia.
- Hasil forecast tidak berdiri sendiri tanpa interpretasi.
- Keterbatasan penelitian dapat dijelaskan.

## 40.3 Dari sisi UI/UX

- Navigasi mudah digunakan.
- Halaman tidak terlalu padat.
- Grafik mudah dibaca.
- Tabel rapi.
- Penjelasan singkat dan tidak berlebihan.

---

# 41. Rekomendasi Akhir untuk Client

Rekomendasi yang bisa disampaikan ke client:

> Untuk kebutuhan tugas akhir, dashboard sebaiknya dibuat sebagai dashboard penelitian forecasting, bukan dashboard bisnis murni. Flow terbaik adalah mulai dari overview penelitian, preprocessing data, analisis time series, pemodelan SARIMA, evaluasi model, forecasting, dan interpretasi hasil. Dengan flow ini, dashboard akan lebih kuat secara akademik, lebih mudah dipresentasikan saat sidang, dan lebih aman ketika diuji oleh dosen.

Jika client ingin fitur bisnis seperti KPI dan rekomendasi, fitur tersebut boleh dimasukkan di halaman Overview atau Kesimpulan, tetapi jangan sampai menghilangkan fokus utama penelitian.

---

# 42. Kesimpulan Final

Project ini sebaiknya diarahkan menjadi **dashboard penelitian forecasting berbasis Streamlit dan SARIMA**. Fokus utamanya bukan hanya membuat tampilan prediksi, tetapi membangun alur penelitian yang jelas dan dapat dipertanggungjawabkan.

Struktur final yang paling disarankan adalah:

```text
Overview Penelitian
→ Data & Preprocessing
→ Analisis Time Series
→ Pemodelan SARIMA
→ Evaluasi & Diagnostik Model
→ Forecasting & Interpretasi
→ Kesimpulan / Rekomendasi Ringkas
```

Dengan struktur tersebut, dashboard akan memiliki beberapa keunggulan:

- sesuai untuk tugas akhir,
- mudah dijelaskan kepada pembimbing,
- kuat saat sidang,
- tidak terlalu melebar dari scope utama,
- tetap terlihat profesional,
- dapat dikembangkan lebih lanjut jika dibutuhkan.

Prioritas utama dalam pengerjaan adalah memastikan data bersih, analisis time series jelas, model SARIMA dapat dijelaskan, evaluasi model tersedia, dan hasil forecast memiliki interpretasi yang masuk akal.

