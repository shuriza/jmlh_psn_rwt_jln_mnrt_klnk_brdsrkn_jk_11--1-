"""
Script untuk Preprocessing Data
Dataset: Jumlah Peserta Rawat Jalan Menurut Kelompok Berdasarkan JKN
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style untuk visualisasi
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class DataPreprocessor:
    def __init__(self, filepath):
        """Initialize dengan filepath dataset"""
        self.filepath = filepath
        self.df = None
        self.df_cleaned = None
        self.stats_summary = {}
        
    def load_data(self):
        """Load dataset dari file Excel"""
        print("="*60)
        print("LOADING DATA")
        print("="*60)
        try:
            self.df = pd.read_excel(self.filepath)
            print(f"✓ Data berhasil dimuat!")
            print(f"  Jumlah baris: {len(self.df)}")
            print(f"  Jumlah kolom: {len(self.df.columns)}")
            print(f"\nKolom yang tersedia:")
            for i, col in enumerate(self.df.columns, 1):
                print(f"  {i}. {col}")
            return True
        except Exception as e:
            print(f"✗ Error saat memuat data: {e}")
            return False
    
    def explore_data(self):
        """Eksplorasi awal data"""
        print("\n" + "="*60)
        print("EKSPLORASI DATA")
        print("="*60)
        
        print("\n1. Preview Data (5 baris pertama):")
        print(self.df.head())
        
        print("\n2. Informasi Dataset:")
        print(self.df.info())
        
        print("\n3. Deskripsi Statistik:")
        print(self.df.describe())
        
    def check_missing_values(self):
        """Cek dan tampilkan missing values"""
        print("\n" + "="*60)
        print("ANALISIS MISSING VALUES")
        print("="*60)
        
        missing = self.df.isnull().sum()
        missing_percent = (self.df.isnull().sum() / len(self.df)) * 100
        
        missing_df = pd.DataFrame({
            'Kolom': missing.index,
            'Jumlah Missing': missing.values,
            'Persentase (%)': missing_percent.values
        })
        
        missing_df = missing_df[missing_df['Jumlah Missing'] > 0].sort_values('Jumlah Missing', ascending=False)
        
        if len(missing_df) > 0:
            print("\n⚠ Ditemukan missing values:")
            print(missing_df.to_string(index=False))
            self.stats_summary['missing_values'] = missing_df
            return True
        else:
            print("\n✓ Tidak ada missing values dalam dataset!")
            self.stats_summary['missing_values'] = None
            return False
    
    def check_duplicates(self):
        """Cek data duplikat"""
        print("\n" + "="*60)
        print("ANALISIS DATA DUPLIKAT")
        print("="*60)
        
        duplicates = self.df.duplicated().sum()
        print(f"\nJumlah baris duplikat: {duplicates}")
        
        if duplicates > 0:
            print("⚠ Ditemukan data duplikat!")
            self.stats_summary['duplicates'] = duplicates
            return True
        else:
            print("✓ Tidak ada data duplikat!")
            self.stats_summary['duplicates'] = 0
            return False
    
    def detect_outliers(self):
        """Deteksi outliers menggunakan IQR method"""
        print("\n" + "="*60)
        print("DETEKSI OUTLIERS (IQR Method)")
        print("="*60)
        
        # Ambil hanya kolom numerik
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        outliers_info = {}
        
        for col in numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
            
            if len(outliers) > 0:
                outliers_info[col] = {
                    'count': len(outliers),
                    'percentage': (len(outliers) / len(self.df)) * 100,
                    'lower_bound': lower_bound,
                    'upper_bound': upper_bound
                }
        
        if outliers_info:
            print("\n⚠ Ditemukan outliers pada kolom berikut:")
            for col, info in outliers_info.items():
                print(f"\n  {col}:")
                print(f"    - Jumlah outliers: {info['count']}")
                print(f"    - Persentase: {info['percentage']:.2f}%")
                print(f"    - Batas bawah: {info['lower_bound']:.2f}")
                print(f"    - Batas atas: {info['upper_bound']:.2f}")
            self.stats_summary['outliers'] = outliers_info
            return True
        else:
            print("\n✓ Tidak ada outliers terdeteksi!")
            self.stats_summary['outliers'] = None
            return False
    
    def handle_missing_values(self):
        """Handle missing values"""
        print("\n" + "="*60)
        print("HANDLING MISSING VALUES")
        print("="*60)
        
        self.df_cleaned = self.df.copy()
        
        if self.df_cleaned.isnull().sum().sum() > 0:
            # Untuk kolom numerik, isi dengan median
            numeric_cols = self.df_cleaned.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if self.df_cleaned[col].isnull().sum() > 0:
                    median_val = self.df_cleaned[col].median()
                    self.df_cleaned[col].fillna(median_val, inplace=True)
                    print(f"✓ Kolom '{col}': Missing values diisi dengan median ({median_val})")
            
            # Untuk kolom kategorikal, isi dengan modus
            categorical_cols = self.df_cleaned.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                if self.df_cleaned[col].isnull().sum() > 0:
                    mode_val = self.df_cleaned[col].mode()[0]
                    self.df_cleaned[col].fillna(mode_val, inplace=True)
                    print(f"✓ Kolom '{col}': Missing values diisi dengan modus ({mode_val})")
        else:
            print("✓ Tidak ada missing values yang perlu di-handle!")
    
    def handle_duplicates(self):
        """Remove data duplikat"""
        print("\n" + "="*60)
        print("HANDLING DUPLICATES")
        print("="*60)
        
        if self.df_cleaned is None:
            self.df_cleaned = self.df.copy()
        
        before = len(self.df_cleaned)
        self.df_cleaned.drop_duplicates(inplace=True)
        after = len(self.df_cleaned)
        removed = before - after
        
        if removed > 0:
            print(f"✓ {removed} baris duplikat telah dihapus!")
        else:
            print("✓ Tidak ada duplikat yang perlu dihapus!")
    
    def handle_outliers(self, method='cap'):
        """Handle outliers dengan capping atau removal"""
        print("\n" + "="*60)
        print(f"HANDLING OUTLIERS (Method: {method})")
        print("="*60)
        
        if self.df_cleaned is None:
            self.df_cleaned = self.df.copy()
        
        numeric_cols = self.df_cleaned.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            Q1 = self.df_cleaned[col].quantile(0.25)
            Q3 = self.df_cleaned[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            if method == 'cap':
                # Capping: ganti outliers dengan batas
                before_outliers = len(self.df_cleaned[(self.df_cleaned[col] < lower_bound) | 
                                                       (self.df_cleaned[col] > upper_bound)])
                
                self.df_cleaned[col] = self.df_cleaned[col].clip(lower=lower_bound, upper=upper_bound)
                
                if before_outliers > 0:
                    print(f"✓ Kolom '{col}': {before_outliers} outliers di-cap")
            elif method == 'remove':
                # Removal: hapus baris dengan outliers
                before = len(self.df_cleaned)
                self.df_cleaned = self.df_cleaned[(self.df_cleaned[col] >= lower_bound) & 
                                                   (self.df_cleaned[col] <= upper_bound)]
                after = len(self.df_cleaned)
                removed = before - after
                
                if removed > 0:
                    print(f"✓ Kolom '{col}': {removed} baris dengan outliers dihapus")
    
    def save_cleaned_data(self, output_path='data_cleaned.csv'):
        """Simpan data yang sudah dibersihkan"""
        print("\n" + "="*60)
        print("MENYIMPAN DATA BERSIH")
        print("="*60)
        
        if self.df_cleaned is not None:
            self.df_cleaned.to_csv(output_path, index=False)
            print(f"✓ Data bersih telah disimpan ke: {output_path}")
            print(f"  Jumlah baris: {len(self.df_cleaned)}")
            print(f"  Jumlah kolom: {len(self.df_cleaned.columns)}")
        else:
            print("⚠ Tidak ada data bersih untuk disimpan!")
    
    def generate_report(self):
        """Generate laporan preprocessing"""
        print("\n" + "="*60)
        print("LAPORAN PREPROCESSING")
        print("="*60)
        
        print(f"\nData Original:")
        print(f"  - Jumlah baris: {len(self.df)}")
        print(f"  - Jumlah kolom: {len(self.df.columns)}")
        
        if self.df_cleaned is not None:
            print(f"\nData Setelah Preprocessing:")
            print(f"  - Jumlah baris: {len(self.df_cleaned)}")
            print(f"  - Jumlah kolom: {len(self.df_cleaned.columns)}")
            print(f"  - Baris yang dihapus: {len(self.df) - len(self.df_cleaned)}")
        
        print(f"\nRingkasan Masalah Data:")
        if self.stats_summary.get('missing_values') is not None:
            print(f"  - Missing values: Ditemukan")
        else:
            print(f"  - Missing values: Tidak ada")
            
        print(f"  - Data duplikat: {self.stats_summary.get('duplicates', 0)}")
        
        if self.stats_summary.get('outliers'):
            print(f"  - Outliers: Ditemukan pada {len(self.stats_summary['outliers'])} kolom")
        else:
            print(f"  - Outliers: Tidak ditemukan")


def main():
    """Main function untuk menjalankan preprocessing"""
    # Path ke dataset
    filepath = 'jmlh_psn_rwt_jln_mnrt_klnk_brdsrkn_jk_11.xlsx'
    
    # Inisialisasi preprocessor
    preprocessor = DataPreprocessor(filepath)
    
    # Load data
    if not preprocessor.load_data():
        return
    
    # Eksplorasi data
    preprocessor.explore_data()
    
    # Cek masalah dalam data
    has_missing = preprocessor.check_missing_values()
    has_duplicates = preprocessor.check_duplicates()
    has_outliers = preprocessor.detect_outliers()
    
    # Handle masalah data
    if has_missing:
        preprocessor.handle_missing_values()
    
    if has_duplicates:
        preprocessor.handle_duplicates()
    
    if has_outliers:
        # Gunakan capping untuk handle outliers
        preprocessor.handle_outliers(method='cap')
    
    # Simpan data bersih
    preprocessor.save_cleaned_data('data_cleaned.csv')
    
    # Generate laporan
    preprocessor.generate_report()
    
    print("\n" + "="*60)
    print("PREPROCESSING SELESAI!")
    print("="*60)


if __name__ == "__main__":
    main()
