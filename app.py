"""
Dashboard Flask untuk Visualisasi Data
Dataset: Jumlah Peserta Rawat Jalan Menurut Kelompok Berdasarkan JKN
"""

from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
import os
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = Flask(__name__)

# Global variable untuk dataset
df = None

def load_dataset():
    """Load dataset"""
    global df
    try:
        if os.path.exists('data_cleaned.csv'):
            df = pd.read_csv('data_cleaned.csv')
            print("✓ Data cleaned dimuat")
        else:
            df = pd.read_excel('jmlh_psn_rwt_jln_mnrt_klnk_brdsrkn_jk_11.xlsx')
            print("✓ Data original dimuat")
        return True
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        return False

def get_basic_stats():
    """Dapatkan statistik dasar dataset"""
    stats = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'numeric_columns': len(df.select_dtypes(include=[np.number]).columns),
        'categorical_columns': len(df.select_dtypes(include=['object']).columns),
        'missing_values': int(df.isnull().sum().sum())
    }
    return stats

def get_column_stats():
    """Dapatkan statistik per kolom"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    stats = {
        'numeric': {},
        'categorical': {}
    }
    
    for col in numeric_cols:
        stats['numeric'][col] = {
            'count': int(df[col].count()),
            'mean': float(df[col].mean()),
            'median': float(df[col].median()),
            'std': float(df[col].std()),
            'min': float(df[col].min()),
            'max': float(df[col].max())
        }
    
    for col in categorical_cols:
        stats['categorical'][col] = {
            'count': int(df[col].count()),
            'unique': int(df[col].nunique()),
            'top_values': df[col].value_counts().head(5).to_dict()
        }
    
    return stats

@app.route('/')
def index():
    """Halaman utama dashboard"""
    if df is None:
        return "Error: Dataset tidak dapat dimuat!", 500
    
    basic_stats = get_basic_stats()
    column_stats = get_column_stats()
    
    return render_template('index.html', 
                         basic_stats=basic_stats,
                         column_stats=column_stats,
                         columns=df.columns.tolist())

@app.route('/api/data')
def get_data():
    """API endpoint untuk mendapatkan data"""
    if df is None:
        return jsonify({'error': 'Dataset tidak dimuat'}), 500
    
    # Ambil 100 baris pertama untuk preview
    data = df.head(100).to_dict('records')
    return jsonify(data)

@app.route('/api/stats')
def get_stats():
    """API endpoint untuk mendapatkan statistik"""
    if df is None:
        return jsonify({'error': 'Dataset tidak dimuat'}), 500
    
    basic_stats = get_basic_stats()
    column_stats = get_column_stats()
    
    return jsonify({
        'basic': basic_stats,
        'columns': column_stats
    })

@app.route('/api/visualization/distribution/<column>')
def get_distribution_plot(column):
    """API endpoint untuk plot distribusi"""
    if df is None or column not in df.columns:
        return jsonify({'error': 'Invalid request'}), 400
    
    if df[column].dtype in [np.int64, np.float64]:
        # Histogram untuk data numerik
        fig = px.histogram(df, x=column, nbins=30,
                          title=f'Distribusi {column}',
                          labels={column: column, 'count': 'Frekuensi'})
        fig.update_layout(
            template='plotly_white',
            showlegend=False
        )
    else:
        # Bar chart untuk data kategorikal
        value_counts = df[column].value_counts().head(15)
        fig = px.bar(x=value_counts.index, y=value_counts.values,
                    title=f'Distribusi {column} (Top 15)',
                    labels={'x': column, 'y': 'Jumlah'})
        fig.update_layout(
            template='plotly_white',
            showlegend=False
        )
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return jsonify({'plot': graphJSON})

@app.route('/api/visualization/comparison/<cat_col>/<num_col>')
def get_comparison_plot(cat_col, num_col):
    """API endpoint untuk plot perbandingan"""
    if df is None or cat_col not in df.columns or num_col not in df.columns:
        return jsonify({'error': 'Invalid request'}), 400
    
    # Ambil top 10 kategori
    top_categories = df[cat_col].value_counts().head(10).index
    df_filtered = df[df[cat_col].isin(top_categories)]
    
    # Grouped bar chart
    fig = px.bar(df_filtered, x=cat_col, y=num_col,
                title=f'{num_col} berdasarkan {cat_col}',
                labels={cat_col: cat_col, num_col: num_col})
    fig.update_layout(
        template='plotly_white',
        xaxis_tickangle=-45
    )
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return jsonify({'plot': graphJSON})

@app.route('/api/visualization/correlation')
def get_correlation_plot():
    """API endpoint untuk correlation heatmap"""
    if df is None:
        return jsonify({'error': 'Dataset tidak dimuat'}), 500
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) < 2:
        return jsonify({'error': 'Tidak cukup kolom numerik'}), 400
    
    corr = df[numeric_cols].corr()
    
    fig = px.imshow(corr,
                   text_auto='.2f',
                   aspect='auto',
                   title='Matriks Korelasi',
                   color_continuous_scale='RdBu_r',
                   color_continuous_midpoint=0)
    fig.update_layout(template='plotly_white')
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return jsonify({'plot': graphJSON})

@app.route('/api/visualization/timeseries/<time_col>/<num_col>')
def get_timeseries_plot(time_col, num_col):
    """API endpoint untuk plot time series"""
    if df is None or time_col not in df.columns or num_col not in df.columns:
        return jsonify({'error': 'Invalid request'}), 400
    
    # Group by dan aggregate
    grouped = df.groupby(time_col)[num_col].sum().reset_index()
    
    fig = px.line(grouped, x=time_col, y=num_col,
                 title=f'Tren {num_col} per {time_col}',
                 markers=True)
    fig.update_layout(
        template='plotly_white',
        xaxis_title=time_col,
        yaxis_title=num_col
    )
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return jsonify({'plot': graphJSON})

@app.route('/visualizations')
def visualizations():
    """Halaman visualisasi"""
    if df is None:
        return "Error: Dataset tidak dapat dimuat!", 500
    
    return render_template('visualizations.html',
                         columns=df.columns.tolist(),
                         numeric_columns=df.select_dtypes(include=[np.number]).columns.tolist(),
                         categorical_columns=df.select_dtypes(include=['object']).columns.tolist())

if __name__ == '__main__':
    # Load dataset saat startup
    if load_dataset():
        print("\n" + "="*60)
        print("DASHBOARD FLASK SIAP!")
        print("="*60)
        print(f"Dataset: {len(df)} baris, {len(df.columns)} kolom")
        print("\nAkses dashboard di: http://127.0.0.1:5000")
        print("="*60 + "\n")
        
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("✗ Gagal memuat dataset. Pastikan file dataset tersedia!")
