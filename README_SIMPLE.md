# Dashboard Visualisasi Data JKN
## UTS Ilmu Data 2025

Dashboard web untuk analisis data Jumlah Peserta Rawat Jalan JKN menggunakan Flask.

---

## 📋 Requirement UTS yang Sudah Dipenuhi

### ✅ 1. Dataset
- **File**: `jmlh_psn_rwt_jln_mnrt_klnk_brdsrkn_jk_11.xlsx`
- **Records**: 7,890 baris
- **Attributes**: 10 kolom
- **Sumber**: Data JKN Jawa Timur (2018-2025)

### ✅ 2. Data Preprocessing
- **Missing Values**: 0 (tidak ada)
- **Data Duplikat**: 0 (tidak ada)
- **Outliers**: 748 outliers (9.48%) ditangani dengan metode IQR capping
- **Output**: `data_cleaned.csv`

### ✅ 3. Statistik Deskriptif
Untuk semua atribut numerik:
- Mean, Median, Mode
- Standard Deviation, Variance
- Min, Max, Range, IQR
- Skewness, Kurtosis
- Quartiles (Q1, Q2, Q3)

Untuk semua atribut kategorikal:
- Unique values
- Mode
- Frequency distribution

### ✅ 4. Visualisasi Data
Total 39+ visualisasi:
- Dashboard ringkasan
- Histogram & Boxplot
- Bar charts kategorikal
- Time series plots
- Comparison charts
- Correlation heatmap
- Interactive Plotly charts

### ✅ 5. Dashboard Flask
- Framework: Flask
- 2 halaman web (Home, Visualisasi)
- RESTful API
- Responsive design (Bootstrap 5)
- Interactive visualizations

### ✅ 6. Siap Upload PythonAnywhere
Semua file siap untuk deployment.

---

## 🚀 Cara Menjalankan

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan Script (Optional)
```bash
python data_preprocessing.py
python statistical_analysis.py
python data_visualization.py
```

### 3. Jalankan Dashboard
```bash
python app.py
```

### 4. Akses Browser
Buka: `http://127.0.0.1:5000`

---

## 📁 Struktur File

```
├── app.py                      # Aplikasi Flask
├── data_preprocessing.py       # Preprocessing
├── statistical_analysis.py     # Analisis statistik
├── data_visualization.py       # Generate visualisasi
│
├── templates/
│   ├── index.html             # Halaman home
│   └── visualizations.html    # Halaman visualisasi
│
├── static/                     # Folder visualisasi (39+ files)
│
├── jmlh_psn_rwt_jln_mnrt_klnk_brdsrkn_jk_11.xlsx  # Dataset
├── data_cleaned.csv           # Dataset bersih
├── requirements.txt           # Dependencies
└── README.md                  # Dokumentasi
```

---

## 📊 Hasil Analisis Singkat

**Kualitas Data**: EXCELLENT
- ✓ No missing values
- ✓ No duplicates
- ✓ Outliers handled

**Distribusi**:
- Gender: 50-50 (balanced)
- Klinik: 61 jenis berbeda
- Periode: 2018-2025

**Statistik Utama**:
- Mean pasien: 78.24
- Median: 48
- Range: 0-271 (setelah capping)

---

## 🌐 Upload ke PythonAnywhere

### Langkah Singkat:
1. Buat akun di pythonanywhere.com
2. Upload semua file proyek
3. Install dependencies:
   ```bash
   pip3.10 install --user -r requirements.txt
   ```
4. Buat web app → Manual configuration → Python 3.10
5. Edit WSGI file:
   ```python
   import sys
   project_home = '/home/username/dashboard-jkn'
   if project_home not in sys.path:
       sys.path = [project_home] + sys.path
   from app import app as application
   ```
6. Set static files:
   - URL: `/static/`
   - Directory: `/home/username/dashboard-jkn/static/`
7. Reload web app
8. Akses: `username.pythonanywhere.com`

---

## 💻 Teknologi

- Python 3.x
- Flask (web framework)
- Pandas (data processing)
- Matplotlib & Seaborn (static visualization)
- Plotly (interactive visualization)
- Bootstrap 5 (frontend)

---

## 📝 Catatan

- Dataset sudah di-preprocessing
- Semua visualisasi sudah di-generate di folder `static/`
- Dashboard siap digunakan tanpa perlu run script lagi
- Untuk re-generate visualisasi, jalankan script masing-masing

---

**Created for UTS Ilmu Data 2025**
