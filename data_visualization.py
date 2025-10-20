"""
Script untuk Visualisasi Data
Dataset: Jumlah Peserta Rawat Jalan Menurut Kelompok Berdasarkan JKN
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

class DataVisualizer:
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
    
    def create_distribution_plots(self):
        """Buat visualisasi distribusi untuk kolom numerik"""
        print("\n📊 Membuat plot distribusi...")
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            print("⚠ Tidak ada kolom numerik untuk divisualisasikan")
            return
        
        # Histogram dan boxplot
        n_cols = len(numeric_cols)
        fig, axes = plt.subplots(n_cols, 2, figsize=(15, 5*n_cols))
        
        if n_cols == 1:
            axes = axes.reshape(1, -1)
        
        for idx, col in enumerate(numeric_cols):
            # Histogram
            axes[idx, 0].hist(self.df[col].dropna(), bins=30, edgecolor='black', alpha=0.7)
            axes[idx, 0].set_title(f'Distribusi {col}', fontweight='bold')
            axes[idx, 0].set_xlabel(col)
            axes[idx, 0].set_ylabel('Frekuensi')
            axes[idx, 0].grid(True, alpha=0.3)
            
            # Boxplot
            axes[idx, 1].boxplot(self.df[col].dropna(), vert=True)
            axes[idx, 1].set_title(f'Boxplot {col}', fontweight='bold')
            axes[idx, 1].set_ylabel(col)
            axes[idx, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('static/distribution_plots.png', dpi=300, bbox_inches='tight')
        print("  ✓ Disimpan: static/distribution_plots.png")
        plt.close()
    
    def create_categorical_plots(self):
        """Buat visualisasi untuk kolom kategorikal"""
        print("\n📊 Membuat plot kategorikal...")
        
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        
        if len(categorical_cols) == 0:
            print("⚠ Tidak ada kolom kategorikal untuk divisualisasikan")
            return
        
        for col in categorical_cols:
            # Bar chart
            plt.figure(figsize=(12, 6))
            value_counts = self.df[col].value_counts().head(15)
            
            plt.bar(range(len(value_counts)), value_counts.values, alpha=0.7)
            plt.xticks(range(len(value_counts)), value_counts.index, rotation=45, ha='right')
            plt.title(f'Distribusi {col} (Top 15)', fontsize=14, fontweight='bold')
            plt.xlabel(col)
            plt.ylabel('Jumlah')
            plt.grid(True, alpha=0.3, axis='y')
            
            plt.tight_layout()
            filename = f'static/categorical_{col.replace(" ", "_").lower()}.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"  ✓ Disimpan: {filename}")
            plt.close()
    
    def create_time_series_plots(self):
        """Buat visualisasi time series jika ada kolom waktu"""
        print("\n📊 Membuat plot time series...")
        
        # Cek apakah ada kolom yang berisi tahun atau tanggal
        time_cols = []
        for col in self.df.columns:
            if 'tahun' in col.lower() or 'year' in col.lower() or 'tanggal' in col.lower():
                time_cols.append(col)
        
        if len(time_cols) == 0:
            print("⚠ Tidak ada kolom waktu terdeteksi")
            return
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for time_col in time_cols:
            for num_col in numeric_cols:
                if num_col != time_col:
                    plt.figure(figsize=(14, 6))
                    
                    # Group by time dan aggregate
                    if self.df[time_col].dtype == 'object':
                        grouped = self.df.groupby(time_col)[num_col].sum().sort_index()
                    else:
                        grouped = self.df.groupby(time_col)[num_col].sum()
                    
                    plt.plot(grouped.index, grouped.values, marker='o', linewidth=2, markersize=8)
                    plt.title(f'Tren {num_col} per {time_col}', fontsize=14, fontweight='bold')
                    plt.xlabel(time_col)
                    plt.ylabel(num_col)
                    plt.grid(True, alpha=0.3)
                    plt.xticks(rotation=45, ha='right')
                    
                    plt.tight_layout()
                    filename = f'static/timeseries_{num_col.replace(" ", "_").lower()}.png'
                    plt.savefig(filename, dpi=300, bbox_inches='tight')
                    print(f"  ✓ Disimpan: {filename}")
                    plt.close()
    
    def create_comparison_plots(self):
        """Buat visualisasi perbandingan antar kategori"""
        print("\n📊 Membuat plot perbandingan...")
        
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if len(categorical_cols) == 0 or len(numeric_cols) == 0:
            print("⚠ Perlu kolom kategorikal dan numerik untuk perbandingan")
            return
        
        for cat_col in categorical_cols:
            for num_col in numeric_cols:
                # Ambil top 10 kategori
                top_categories = self.df[cat_col].value_counts().head(10).index
                df_filtered = self.df[self.df[cat_col].isin(top_categories)]
                
                plt.figure(figsize=(12, 6))
                
                # Grouped bar chart
                grouped = df_filtered.groupby(cat_col)[num_col].agg(['sum', 'mean'])
                
                x = range(len(grouped))
                width = 0.35
                
                plt.bar([i - width/2 for i in x], grouped['sum'], width, label='Total', alpha=0.8)
                plt.bar([i + width/2 for i in x], grouped['mean'], width, label='Rata-rata', alpha=0.8)
                
                plt.xlabel(cat_col)
                plt.ylabel(num_col)
                plt.title(f'{num_col} berdasarkan {cat_col}', fontsize=14, fontweight='bold')
                plt.xticks(x, grouped.index, rotation=45, ha='right')
                plt.legend()
                plt.grid(True, alpha=0.3, axis='y')
                
                plt.tight_layout()
                filename = f'static/comparison_{cat_col.replace(" ", "_").lower()}_{num_col.replace(" ", "_").lower()}.png'
                plt.savefig(filename, dpi=300, bbox_inches='tight')
                print(f"  ✓ Disimpan: {filename}")
                plt.close()
    
    def create_correlation_heatmap(self):
        """Buat heatmap korelasi"""
        print("\n📊 Membuat correlation heatmap...")
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            print("⚠ Tidak cukup kolom numerik untuk korelasi")
            return
        
        plt.figure(figsize=(12, 10))
        corr = self.df[numeric_cols].corr()
        
        sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, 
                   fmt='.2f', square=True, linewidths=1, cbar_kws={"shrink": 0.8})
        
        plt.title('Matriks Korelasi Antar Variabel', fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig('static/correlation_heatmap.png', dpi=300, bbox_inches='tight')
        print("  ✓ Disimpan: static/correlation_heatmap.png")
        plt.close()
    
    def create_interactive_plots(self):
        """Buat visualisasi interaktif dengan Plotly"""
        print("\n📊 Membuat plot interaktif...")
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        
        # Interactive scatter plot
        if len(numeric_cols) >= 2:
            fig = px.scatter(self.df, x=numeric_cols[0], y=numeric_cols[1],
                           color=categorical_cols[0] if len(categorical_cols) > 0 else None,
                           title=f'Scatter Plot: {numeric_cols[0]} vs {numeric_cols[1]}',
                           hover_data=self.df.columns)
            fig.write_html('static/interactive_scatter.html')
            print("  ✓ Disimpan: static/interactive_scatter.html")
        
        # Interactive bar chart
        if len(categorical_cols) > 0 and len(numeric_cols) > 0:
            top_categories = self.df[categorical_cols[0]].value_counts().head(15).index
            df_filtered = self.df[self.df[categorical_cols[0]].isin(top_categories)]
            
            fig = px.bar(df_filtered, x=categorical_cols[0], y=numeric_cols[0],
                        title=f'{numeric_cols[0]} berdasarkan {categorical_cols[0]}',
                        color=numeric_cols[0])
            fig.write_html('static/interactive_bar.html')
            print("  ✓ Disimpan: static/interactive_bar.html")
    
    def create_summary_dashboard(self):
        """Buat dashboard ringkasan"""
        print("\n📊 Membuat dashboard ringkasan...")
        
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Info dataset
        ax1 = fig.add_subplot(gs[0, :])
        ax1.axis('off')
        info_text = f"""
        RINGKASAN DATASET
        
        Jumlah Baris: {len(self.df):,}
        Jumlah Kolom: {len(self.df.columns)}
        Kolom Numerik: {len(self.df.select_dtypes(include=[np.number]).columns)}
        Kolom Kategorikal: {len(self.df.select_dtypes(include=['object']).columns)}
        Missing Values: {self.df.isnull().sum().sum()}
        """
        ax1.text(0.1, 0.5, info_text, fontsize=12, verticalalignment='center',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
        
        # Plot distribusi kolom numerik pertama
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            ax2 = fig.add_subplot(gs[1, 0])
            ax2.hist(self.df[numeric_cols[0]].dropna(), bins=20, edgecolor='black', alpha=0.7)
            ax2.set_title(f'Distribusi {numeric_cols[0]}', fontweight='bold')
            ax2.set_xlabel(numeric_cols[0])
            ax2.set_ylabel('Frekuensi')
            ax2.grid(True, alpha=0.3)
        
        # Plot kategorikal
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            ax3 = fig.add_subplot(gs[1, 1:])
            value_counts = self.df[categorical_cols[0]].value_counts().head(10)
            ax3.barh(range(len(value_counts)), value_counts.values, alpha=0.7)
            ax3.set_yticks(range(len(value_counts)))
            ax3.set_yticklabels(value_counts.index)
            ax3.set_title(f'Top 10 {categorical_cols[0]}', fontweight='bold')
            ax3.set_xlabel('Jumlah')
            ax3.grid(True, alpha=0.3, axis='x')
        
        # Statistik deskriptif
        if len(numeric_cols) > 0:
            ax4 = fig.add_subplot(gs[2, :])
            stats_data = self.df[numeric_cols].describe().T[['mean', 'std', 'min', 'max']]
            
            table_data = []
            for idx, row in stats_data.iterrows():
                table_data.append([idx, f"{row['mean']:.2f}", f"{row['std']:.2f}", 
                                 f"{row['min']:.2f}", f"{row['max']:.2f}"])
            
            ax4.axis('tight')
            ax4.axis('off')
            table = ax4.table(cellText=table_data,
                            colLabels=['Kolom', 'Mean', 'Std Dev', 'Min', 'Max'],
                            cellLoc='left',
                            loc='center',
                            colWidths=[0.3, 0.175, 0.175, 0.175, 0.175])
            table.auto_set_font_size(False)
            table.set_fontsize(9)
            table.scale(1, 2)
            
            # Style header
            for i in range(5):
                table[(0, i)].set_facecolor('#4CAF50')
                table[(0, i)].set_text_props(weight='bold', color='white')
        
        plt.suptitle('Dashboard Ringkasan Data', fontsize=18, fontweight='bold', y=0.98)
        plt.savefig('static/summary_dashboard.png', dpi=300, bbox_inches='tight')
        print("  ✓ Disimpan: static/summary_dashboard.png")
        plt.close()


def main():
    """Main function"""
    # Buat direktori static jika belum ada
    import os
    if not os.path.exists('static'):
        os.makedirs('static')
        print("✓ Direktori 'static' dibuat")
    
    # Load data
    try:
        visualizer = DataVisualizer('data_cleaned.csv')
        if not visualizer.load_data():
            raise Exception("Data cleaned tidak ditemukan")
    except:
        print("⚠ Menggunakan data original...")
        visualizer = DataVisualizer('jmlh_psn_rwt_jln_mnrt_klnk_brdsrkn_jk_11.xlsx')
        if not visualizer.load_data():
            return
    
    print("\n" + "="*80)
    print("MEMBUAT VISUALISASI DATA")
    print("="*80)
    
    # Buat berbagai visualisasi
    visualizer.create_summary_dashboard()
    visualizer.create_distribution_plots()
    visualizer.create_categorical_plots()
    visualizer.create_time_series_plots()
    visualizer.create_comparison_plots()
    visualizer.create_correlation_heatmap()
    visualizer.create_interactive_plots()
    
    print("\n" + "="*80)
    print("VISUALISASI SELESAI!")
    print("="*80)
    print("\n✓ Semua visualisasi telah disimpan di folder 'static'")


if __name__ == "__main__":
    main()
