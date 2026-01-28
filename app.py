"""
Dashboard Kecanduan Media Sosial Mahasiswa
==========================================
Dashboard interaktif untuk menganalisis pola kecanduan media sosial
berdasarkan Bergen Social Media Addiction Scale (BSMAS)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page config
st.set_page_config(
    page_title="Dashboard Kecanduan Media Sosial",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1976D2;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1976D2;
    }
    .danger { border-left-color: #F44336; }
    .warning { border-left-color: #FF9800; }
    .success { border-left-color: #4CAF50; }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('dataset_looker_student_social_media_clean.csv')
    return df

# Main app
def main():
    st.markdown('<h1 class="main-header">Dashboard Kecanduan Media Sosial Mahasiswa</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Load data
    try:
        df = load_data()
    except FileNotFoundError:
        st.error("❌ File 'dataset_looker_student_social_media_clean.csv' tidak ditemukan!")
        st.info("Pastikan file CSV ada di folder yang sama dengan app.py")
        return
    
    # Sidebar filters
    st.sidebar.header("Filter Data")
    
    # Gender filter
    gender_options = ["Semua"] + list(df['Gender'].unique())
    selected_gender = st.sidebar.selectbox("Gender:", gender_options)
    
    # Age group filter
    age_options = ["Semua"] + sorted(df['Age_Group'].unique())
    selected_age = st.sidebar.selectbox("Kelompok Usia:", age_options)
    
    # Platform filter
    platform_options = ["Semua"] + sorted(df['Platform_Type'].unique())
    selected_platform = st.sidebar.selectbox("Jenis Platform:", platform_options)
    
    # Addiction level filter
    addiction_options = ["Semua"] + list(df['Addiction_Level'].unique())
    selected_addiction = st.sidebar.selectbox("Tingkat Kecanduan:", addiction_options)
    
    # Vulnerable group checkbox
    show_vulnerable = st.sidebar.checkbox("Tampilkan Hanya Kelompok Rentan", False)
    
    # Apply filters
    filtered_df = df.copy()
    if selected_gender != "Semua":
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    if selected_age != "Semua":
        filtered_df = filtered_df[filtered_df['Age_Group'] == selected_age]
    if selected_platform != "Semua":
        filtered_df = filtered_df[filtered_df['Platform_Type'] == selected_platform]
    if selected_addiction != "Semua":
        filtered_df = filtered_df[filtered_df['Addiction_Level'] == selected_addiction]
    if show_vulnerable:
        filtered_df = filtered_df[filtered_df['Vulnerable_Group'].str.contains("Ya", na=False)]
    
    st.sidebar.markdown(f"**Total Data Terfilter:** {len(filtered_df)} dari {len(df)}")
    
    # KPI Section
    st.header("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total = len(filtered_df)
        st.metric("Total Mahasiswa", f"{total:,}", help="Total mahasiswa dalam dataset")
    
    with col2:
        high_risk = len(filtered_df[filtered_df['High_Risk_Addiction'] == 'Ya'])
        pct_high_risk = (high_risk / total * 100) if total > 0 else 0
        st.metric(
            "Risiko Tinggi", 
            f"{high_risk}",
            delta=f"{pct_high_risk:.1f}%",
            delta_color="inverse",
            help="Mahasiswa dengan skor kecanduan ≥8.67 (standar BSMAS)"
        )
    
    with col3:
        vulnerable = len(filtered_df[filtered_df['Vulnerable_Group'].str.contains("Ya", na=False)])
        pct_vulnerable = (vulnerable / total * 100) if total > 0 else 0
        st.metric(
            "Kelompok Rentan",
            f"{vulnerable}",
            delta=f"{pct_vulnerable:.1f}%",
            delta_color="inverse",
            help="Perempuan muda (≤21 th) & Laki-laki sangat muda (≤19 th)"
        )
    
    with col4:
        high_usage = len(filtered_df[filtered_df['Usage_Duration_Category'] == 'Penggunaan Tinggi (>4 jam)'])
        pct_high_usage = (high_usage / total * 100) if total > 0 else 0
        st.metric(
            "Penggunaan >4 Jam",
            f"{high_usage}",
            delta=f"{pct_high_usage:.1f}%",
            delta_color="inverse",
            help="Mahasiswa yang menggunakan media sosial >4 jam/hari"
        )
    
    st.markdown("---")
    
    # Row 1: Addiction Level & Platform Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribusi Tingkat Kecanduan")
        addiction_counts = filtered_df['Addiction_Level'].value_counts()
        fig1 = px.pie(
            values=addiction_counts.values,
            names=addiction_counts.index,
            color=addiction_counts.index,
            color_discrete_map={
                'Risiko Rendah': '#4CAF50',
                'Risiko Sedang': '#FF9800',
                'Risiko Tinggi': '#F44336'
            },
            hole=0.4
        )
        fig1.update_traces(textposition='inside', textinfo='percent+label')
        fig1.update_layout(showlegend=True, height=400)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("Platform Paling Populer")
        platform_counts = filtered_df['Platform_Type'].value_counts().head(7)
        fig2 = px.bar(
            x=platform_counts.values,
            y=platform_counts.index,
            orientation='h',
            color=platform_counts.values,
            color_continuous_scale='Blues'
        )
        fig2.update_layout(
            showlegend=False,
            xaxis_title="Jumlah Pengguna",
            yaxis_title="",
            height=400
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Row 2: Age-Gender Heatmap & Usage vs Mental Health
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Heatmap: Usia vs Gender vs Kecanduan")
        pivot = filtered_df.pivot_table(
            values='Addicted_Score',
            index='Age_Group',
            columns='Gender',
            aggfunc='mean'
        )
        fig3 = px.imshow(
            pivot,
            labels=dict(x="Gender", y="Kelompok Usia", color="Avg Addiction Score"),
            color_continuous_scale='RdYlGn_r',
            aspect="auto"
        )
        fig3.update_layout(height=400)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.subheader("Penggunaan vs Kesehatan Mental")
        
        # Coba dengan trendline, jika statsmodels tidak ada, skip trendline
        try:
            fig4 = px.scatter(
                filtered_df,
                x='Avg_Daily_Usage_Hours',
                y='Mental_Health_Score',
                color='Addiction_Level',
                size='Sleep_Hours_Per_Night',
                hover_data=['Gender', 'Age', 'Platform_Type'],
                color_discrete_map={
                    'Risiko Rendah': '#4CAF50',
                    'Risiko Sedang': '#FF9800',
                    'Risiko Tinggi': '#F44336'
                },
                trendline="ols"
            )
        except (ImportError, ModuleNotFoundError):
            # Fallback: tanpa trendline jika statsmodels tidak terinstall
            fig4 = px.scatter(
                filtered_df,
                x='Avg_Daily_Usage_Hours',
                y='Mental_Health_Score',
                color='Addiction_Level',
                size='Sleep_Hours_Per_Night',
                hover_data=['Gender', 'Age', 'Platform_Type'],
                color_discrete_map={
                    'Risiko Rendah': '#4CAF50',
                    'Risiko Sedang': '#FF9800',
                    'Risiko Tinggi': '#F44336'
                }
            )
        
        fig4.add_hline(y=6, line_dash="dash", line_color="red", 
                       annotation_text="Threshold Kesehatan Mental Buruk")
        fig4.add_vline(x=4, line_dash="dash", line_color="orange",
                       annotation_text="Threshold Penggunaan Tinggi")
        fig4.update_layout(height=400)
        st.plotly_chart(fig4, use_container_width=True)
    
    # Row 3: Mental Health & Sleep Quality
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribusi Kesehatan Mental")
        mental_counts = filtered_df['Mental_Health_Detail'].value_counts()
        fig5 = px.bar(
            x=mental_counts.index,
            y=mental_counts.values,
            color=mental_counts.index,
            color_discrete_map={
                'Sangat Buruk (1-3)': '#F44336',
                'Buruk (4-5)': '#FF9800',
                'Sedang (6-7)': '#FFC107',
                'Baik (8-10)': '#4CAF50'
            }
        )
        fig5.update_layout(
            showlegend=False,
            xaxis_title="",
            yaxis_title="Jumlah Mahasiswa",
            height=400
        )
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        st.subheader("Distribusi Kualitas Tidur")
        sleep_counts = filtered_df['Sleep_Quality_Detail'].value_counts()
        sleep_order = ['Sangat Kurang (<5h)', 'Kurang (5-6h)', 'Cukup (6-7h)', 'Baik (7-9h)', 'Berlebihan (>9h)']
        sleep_counts = sleep_counts.reindex([x for x in sleep_order if x in sleep_counts.index])
        
        fig6 = px.bar(
            x=sleep_counts.index,
            y=sleep_counts.values,
            color=sleep_counts.index,
            color_discrete_sequence=px.colors.sequential.Reds_r
        )
        fig6.update_layout(
            showlegend=False,
            xaxis_title="",
            yaxis_title="Jumlah Mahasiswa",
            height=400
        )
        st.plotly_chart(fig6, use_container_width=True)
    
    # Statistics Summary
    st.markdown("---")
    st.header("Statistik Ringkasan")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Penggunaan Media Sosial")
        avg_usage = filtered_df['Avg_Daily_Usage_Hours'].mean()
        st.metric("Rata-rata Penggunaan", f"{avg_usage:.1f} jam/hari")
        st.write(filtered_df['Avg_Daily_Usage_Hours'].describe().round(2))
    
    with col2:
        st.subheader("Kesehatan Mental")
        avg_mental = filtered_df['Mental_Health_Score'].mean()
        st.metric("Rata-rata Skor", f"{avg_mental:.1f}/10")
        st.write(filtered_df['Mental_Health_Score'].describe().round(2))
    
    with col3:
        st.subheader("Kualitas Tidur")
        avg_sleep = filtered_df['Sleep_Hours_Per_Night'].mean()
        st.metric("Rata-rata Tidur", f"{avg_sleep:.1f} jam/malam")
        st.write(filtered_df['Sleep_Hours_Per_Night'].describe().round(2))
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; padding: 2rem;'>
        <p>Dashboard Analisis Kecanduan Media Sosial Mahasiswa</p>
        <p>Berdasarkan Bergen Social Media Addiction Scale (BSMAS)</p>
        <p style='font-size: 0.8rem;'>Data: {total} mahasiswa dari {countries} negara</p>
    </div>
    """.format(total=len(df), countries=df['Country'].nunique()), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
