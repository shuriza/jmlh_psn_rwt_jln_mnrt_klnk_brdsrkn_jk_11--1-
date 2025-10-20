"""
Script untuk Analisis Statistik Deskriptif
Dataset: Jumlah Peserta Rawat Jalan Menurut Kelompok Berdasarkan JKN
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class StatisticalAnalyzer:
    def __init__(self, filepath):
        """Initialize dengan filepath dataset"""
        self.filepath = filepath
        self.df = None
        
    def load_data(self):
        """Load dataset"""
        try:
            if self.filepath.endswith('.csv'):
                self.df = pd.read_csv(self.filepath)
            elif self.filepath.endswith('.xlsx'):
                self.df = pd.read_excel(self.filepath)
            print(f"✓ Data berhasil dimuat: {len(self.df)} baris, {len(self.df.columns)} kolom")
            return True
        except Exception as e:
            print(f"✗ Error: {e}")
            return False
    
    def descriptive_statistics(self):
        """Hitung statistik deskriptif untuk semua atribut"""
        print("\n" + "="*80)
        print("STATISTIK DESKRIPTIF")
        print("="*80)
        
        # Untuk kolom numerik
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) > 0:
            print("\n📊 KOLOM NUMERIK:")
            print("-" * 80)
            
            for col in numeric_cols:
                print(f"\n{col}:")
                print(f"  Count         : {self.df[col].count()}")
                print(f"  Mean          : {self.df[col].mean():.2f}")
                print(f"  Median        : {self.df[col].median():.2f}")
                print(f"  Mode          : {self.df[col].mode().values[0] if len(self.df[col].mode()) > 0 else 'N/A'}")
                print(f"  Std Dev       : {self.df[col].std():.2f}")
                print(f"  Variance      : {self.df[col].var():.2f}")
                print(f"  Min           : {self.df[col].min():.2f}")
                print(f"  Q1 (25%)      : {self.df[col].quantile(0.25):.2f}")
                print(f"  Q2 (50%)      : {self.df[col].quantile(0.50):.2f}")
                print(f"  Q3 (75%)      : {self.df[col].quantile(0.75):.2f}")
                print(f"  Max           : {self.df[col].max():.2f}")
                print(f"  Range         : {self.df[col].max() - self.df[col].min():.2f}")
                print(f"  IQR           : {self.df[col].quantile(0.75) - self.df[col].quantile(0.25):.2f}")
                print(f"  Skewness      : {self.df[col].skew():.2f}")
                print(f"  Kurtosis      : {self.df[col].kurtosis():.2f}")
        
        # Untuk kolom kategorikal
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        
        if len(categorical_cols) > 0:
            print("\n📊 KOLOM KATEGORIKAL:")
            print("-" * 80)
            
            for col in categorical_cols:
                print(f"\n{col}:")
                print(f"  Count         : {self.df[col].count()}")
                print(f"  Unique Values : {self.df[col].nunique()}")
                print(f"  Mode          : {self.df[col].mode().values[0] if len(self.df[col].mode()) > 0 else 'N/A'}")
                print(f"  Top 5 Values  :")
                top_values = self.df[col].value_counts().head()
                for val, count in top_values.items():
                    print(f"    - {val}: {count} ({count/len(self.df)*100:.1f}%)")
    
    def save_statistics_report(self, output_path='statistics_report.txt'):
        """Simpan laporan statistik ke file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("LAPORAN STATISTIK DESKRIPTIF\n")
            f.write("="*80 + "\n\n")
            
            # Statistik numerik
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            
            if len(numeric_cols) > 0:
                f.write("KOLOM NUMERIK:\n")
                f.write("-" * 80 + "\n\n")
                
                for col in numeric_cols:
                    f.write(f"{col}:\n")
                    f.write(f"  Count         : {self.df[col].count()}\n")
                    f.write(f"  Mean          : {self.df[col].mean():.2f}\n")
                    f.write(f"  Median        : {self.df[col].median():.2f}\n")
                    f.write(f"  Std Dev       : {self.df[col].std():.2f}\n")
                    f.write(f"  Min           : {self.df[col].min():.2f}\n")
                    f.write(f"  Max           : {self.df[col].max():.2f}\n\n")
            
            # Statistik kategorikal
            categorical_cols = self.df.select_dtypes(include=['object']).columns
            
            if len(categorical_cols) > 0:
                f.write("\nKOLOM KATEGORIKAL:\n")
                f.write("-" * 80 + "\n\n")
                
                for col in categorical_cols:
                    f.write(f"{col}:\n")
                    f.write(f"  Unique Values : {self.df[col].nunique()}\n")
                    f.write(f"  Mode          : {self.df[col].mode().values[0]}\n\n")
        
        print(f"\n✓ Laporan statistik disimpan ke: {output_path}")
    
    def correlation_analysis(self):
        """Analisis korelasi antar variabel numerik"""
        print("\n" + "="*80)
        print("ANALISIS KORELASI")
        print("="*80)
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) > 1:
            corr_matrix = self.df[numeric_cols].corr()
            print("\nMatriks Korelasi:")
            print(corr_matrix)
            
            # Simpan visualisasi korelasi
            plt.figure(figsize=(12, 8))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                       fmt='.2f', square=True, linewidths=1)
            plt.title('Matriks Korelasi Antar Variabel', fontsize=16, fontweight='bold')
            plt.tight_layout()
            plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
            print("\n✓ Visualisasi korelasi disimpan ke: correlation_matrix.png")
            plt.close()
        else:
            print("\n⚠ Tidak cukup kolom numerik untuk analisis korelasi")


def main():
    """Main function"""
    # Load data cleaned jika ada, jika tidak load data original
    try:
        analyzer = StatisticalAnalyzer('data_cleaned.csv')
        if not analyzer.load_data():
            raise Exception("Data cleaned tidak ditemukan")
    except:
        print("⚠ Menggunakan data original...")
        analyzer = StatisticalAnalyzer('jmlh_psn_rwt_jln_mnrt_klnk_brdsrkn_jk_11.xlsx')
        if not analyzer.load_data():
            return
    
    # Analisis statistik deskriptif
    analyzer.descriptive_statistics()
    
    # Analisis korelasi
    analyzer.correlation_analysis()
    
    # Simpan laporan
    analyzer.save_statistics_report()
    
    print("\n" + "="*80)
    print("ANALISIS STATISTIK SELESAI!")
    print("="*80)


if __name__ == "__main__":
    main()
