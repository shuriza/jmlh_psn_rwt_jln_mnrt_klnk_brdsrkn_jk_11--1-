# Dashboard Visualisasi Data JKN
# Ujian Tengah Semester - Ilmu Data

## 📊 Deskripsi Proyek
Dashboard visualisasi data untuk menganalisis **Jumlah Peserta Rawat Jalan Menurut Kelompok Berdasarkan JKN**. Proyek ini mencakup preprocessing data, analisis statistik deskriptif, dan visualisasi interaktif berbasis web menggunakan Flask.

## 🎯 Tujuan Proyek
1. ✅ Melakukan preprocessing data (missing values, duplikat, outliers)
2. ✅ Menghitung statistik deskriptif untuk setiap atribut
3. ✅ Membuat visualisasi data yang informatif
4. ✅ Membangun dashboard web dengan Flask
5. ✅ Deploy ke PythonAnywhere.com

## 📁 Struktur Proyek
```
jmlh_psn_rwt_jln_mnrt_klnk_brdsrkn_jk_11/
│
├── app.py                          # Aplikasi Flask utama
├── data_preprocessing.py           # Script preprocessing data
├── statistical_analysis.py         # Script analisis statistik
├── data_visualization.py           # Script visualisasi data
├── requirements.txt                # Dependencies Python
├── README.md                       # Dokumentasi proyek
│
├── templates/                      # Template HTML
│   ├── index.html                 # Halaman utama
│   ├── visualizations.html        # Halaman visualisasi
│   └── about.html                 # Halaman tentang
│
├── static/                         # File statis (gambar, CSS, JS)
│   ├── *.png                      # Visualisasi statis
│   └── *.html                     # Visualisasi interaktif
│
├── jmlh_psn_rwt_jln_mnrt_klnk_brdsrkn_jk_11.xlsx  # Dataset original
├── data_cleaned.csv               # Dataset setelah preprocessing
└── statistics_report.txt          # Laporan statistik
```

## 🚀 Cara Menjalankan Proyek

### 1. Persiapan Environment
```bash
# Buat virtual environment (opsional tapi direkomendasikan)
python -m venv .venv

# Aktivasi virtual environment
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
```

### 2. Preprocessing Data
```bash
# Jalankan script preprocessing
python data_preprocessing.py
```
Output:
- `data_cleaned.csv` - Dataset yang sudah dibersihkan
- Laporan preprocessing di console

### 3. Analisis Statistik
```bash
# Jalankan analisis statistik
python statistical_analysis.py
```
Output:
- `statistics_report.txt` - Laporan statistik lengkap
- `correlation_matrix.png` - Visualisasi korelasi

### 4. Generate Visualisasi
```bash
# Jalankan script visualisasi
python data_visualization.py
```
Output:
- Berbagai visualisasi di folder `static/`
- Visualisasi interaktif dalam format HTML

### 5. Jalankan Dashboard
```bash
# Jalankan aplikasi Flask
python app.py
```
Akses dashboard di browser: `http://127.0.0.1:5000`

## 📊 Fitur Dashboard

### 1. Halaman Home (`/`)
- Ringkasan statistik dataset
- Informasi jumlah baris, kolom, missing values
- Statistik deskriptif untuk kolom numerik dan kategorikal
- Preview visualisasi

### 2. Halaman Visualisasi (`/visualizations`)
- Dashboard ringkasan data
- Distribusi data (histogram, boxplot)
- Matriks korelasi
- Visualisasi interaktif dengan Plotly
- Grafik perbandingan antar kategori
- Time series plot (jika ada data temporal)

### 3. Halaman Tentang (`/about`)
- Informasi proyek
- Metodologi
- Teknologi yang digunakan
- Panduan deployment

## 🔧 Teknologi yang Digunakan

### Backend
- **Python 3.x** - Bahasa pemrograman utama
- **Flask** - Web framework
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **SciPy** - Scientific computing

### Visualisasi
- **Matplotlib** - Static plotting
- **Seaborn** - Statistical visualization
- **Plotly** - Interactive visualization

### Frontend
- **Bootstrap 5** - CSS framework
- **HTML5/CSS3** - Markup dan styling
- **JavaScript** - Interactivity

## 📈 Proses Data Preprocessing

### 1. Missing Values
- **Deteksi**: Identifikasi kolom dengan missing values
- **Handling**: 
  - Kolom numerik: Diisi dengan median
  - Kolom kategorikal: Diisi dengan modus

### 2. Data Duplikat
- **Deteksi**: Cek baris duplikat
- **Handling**: Hapus duplikat, simpan 1 instance

### 3. Outliers
- **Deteksi**: IQR (Interquartile Range) method
- **Formula**: 
  - Lower bound = Q1 - 1.5 × IQR
  - Upper bound = Q3 + 1.5 × IQR
- **Handling**: Capping (nilai outlier diganti dengan batas)

## 📊 Statistik Deskriptif

Untuk setiap atribut numerik:
- **Central Tendency**: Mean, Median, Mode
- **Dispersion**: Standard Deviation, Variance, Range, IQR
- **Shape**: Skewness, Kurtosis
- **Distribution**: Min, Q1, Q2 (Median), Q3, Max

Untuk setiap atribut kategorikal:
- Jumlah unique values
- Mode (nilai paling sering)
- Frekuensi top values

## 📊 Jenis Visualisasi

1. **Histogram** - Distribusi data numerik
2. **Boxplot** - Identifikasi outliers dan spread data
3. **Bar Chart** - Frekuensi data kategorikal
4. **Heatmap** - Korelasi antar variabel
5. **Line Chart** - Trend data time series
6. **Scatter Plot** - Hubungan antar variabel
7. **Interactive Plots** - Plotly untuk eksplorasi detail

## 🌐 Deployment ke PythonAnywhere

### Langkah-langkah:

1. **Upload Files**
   - Upload semua file proyek ke PythonAnywhere
   - Gunakan Git atau upload manual

2. **Install Dependencies**
   ```bash
   pip install --user -r requirements.txt
   ```

3. **Setup Web App**
   - Buat new web app
   - Pilih Flask
   - Python version: 3.x

4. **Configure WSGI File**
   ```python
   import sys
   path = '/home/yourusername/dashboard-jkn'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

5. **Static Files**
   - URL: `/static/`
   - Directory: `/home/yourusername/dashboard-jkn/static/`

6. **Reload Web App**
   - Klik tombol "Reload"
   - Akses di: `yourusername.pythonanywhere.com`

## 📝 Materi Presentasi (13 Oktober 2025)

### 1. Dataset (2-3 menit)
- Sumber data: Data JKN peserta rawat jalan
- Struktur dataset: Jumlah baris, kolom, tipe data
- Deskripsi singkat setiap atribut

### 2. Data Preprocessing (3-4 menit)
- **Missing Values**: 
  - Berapa banyak? Di kolom mana?
  - Metode handling yang digunakan
- **Duplikat**: 
  - Ada atau tidak?
  - Jumlah dan cara handling
- **Outliers**: 
  - Deteksi dengan IQR method
  - Visualisasi boxplot
  - Cara handling (capping)

### 3. Analisis Data untuk Dashboard (3-4 menit)
- **Statistik Deskriptif**: 
  - Mean, median, std untuk kolom utama
  - Distribusi data
- **Visualisasi yang akan ditampilkan**:
  - Distribusi peserta per kategori
  - Trend time series (jika ada)
  - Korelasi antar variabel
  - Perbandingan antar kelompok
- **Insight yang didapat**: 
  - Pola menarik dari data
  - Temuan penting

## 🎓 Informasi Akademik

- **Mata Kuliah**: Ilmu Data
- **Tugas**: Ujian Tengah Semester
- **Tanggal Presentasi**: 13 Oktober 2025
- **Durasi**: ~10 menit

## 📞 Support

Jika ada pertanyaan atau issue, silakan buat issue di repository atau hubungi melalui email.

## 📄 License

Project ini dibuat untuk keperluan akademik.

---

**Dibuat dengan ❤️ untuk Ujian Tengah Semester Ilmu Data 2025**
