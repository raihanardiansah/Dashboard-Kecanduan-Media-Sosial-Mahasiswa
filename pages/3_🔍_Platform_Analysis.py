"""
Page 3: Analisis Platform
=========================
Perbandingan dampak berbagai platform media sosial
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Analisis Platform", page_icon="P", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv('dataset_looker_student_social_media_clean.csv')

st.title("Analisis Platform Media Sosial")
st.markdown("---")

df = load_data()

# Platform selector
platforms = sorted(df['Platform_Type'].unique())
selected_platforms = st.multiselect(
    "Pilih Platform untuk Dibandingkan:",
    platforms,
    default=platforms
)

filtered_df = df[df['Platform_Type'].isin(selected_platforms)]

# KPIs by Platform
st.subheader("Metrik Per Platform")

platform_stats = filtered_df.groupby('Platform_Type').agg({
    'Student_ID': 'count',
    'Avg_Daily_Usage_Hours': 'mean',
    'Addicted_Score': 'mean',
    'Mental_Health_Score': 'mean',
    'Sleep_Hours_Per_Night': 'mean'
}).round(2)

platform_stats.columns = ['Jumlah Users', 'Avg Usage (jam)', 'Avg Addiction', 'Avg Mental Health', 'Avg Sleep (jam)']
platform_stats = platform_stats.sort_values('Jumlah Users', ascending=False)

st.dataframe(platform_stats, use_container_width=True)

st.markdown("---")

# Row 1: Usage & Addiction by Platform
col1, col2 = st.columns(2)

with col1:
    st.subheader("Rata-rata Penggunaan per Platform")
    usage_by_platform = filtered_df.groupby('Platform_Type')['Avg_Daily_Usage_Hours'].mean().sort_values(ascending=False)
    
    fig1 = px.bar(
        x=usage_by_platform.values,
        y=usage_by_platform.index,
        orientation='h',
        color=usage_by_platform.values,
        color_continuous_scale='Oranges'
    )
    fig1.add_vline(x=4, line_dash="dash", line_color="red",
                   annotation_text="Threshold 4 jam")
    fig1.update_layout(showlegend=False, xaxis_title="Jam per Hari", yaxis_title="")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Addiction Score per Platform")
    addiction_by_platform = filtered_df.groupby('Platform_Type')['Addicted_Score'].mean().sort_values(ascending=False)
    
    fig2 = px.bar(
        x=addiction_by_platform.values,
        y=addiction_by_platform.index,
        orientation='h',
        color=addiction_by_platform.values,
        color_continuous_scale='Reds'
    )
    fig2.add_vline(x=8.67, line_dash="dash", line_color="darkred",
                   annotation_text="Threshold Risiko Tinggi")
    fig2.update_layout(showlegend=False, xaxis_title="Addiction Score", yaxis_title="")
    st.plotly_chart(fig2, use_container_width=True)

# Row 2: Mental Health & Sleep Impact
col1, col2 = st.columns(2)

with col1:
    st.subheader("Dampak Kesehatan Mental")
    mental_by_platform = filtered_df.groupby('Platform_Type')['Mental_Health_Score'].mean().sort_values()
    
    fig3 = px.bar(
        x=mental_by_platform.values,
        y=mental_by_platform.index,
        orientation='h',
        color=mental_by_platform.values,
        color_continuous_scale='RdYlGn'
    )
    fig3.add_vline(x=6, line_dash="dash", line_color="orange",
                   annotation_text="Threshold Mental Health Buruk")
    fig3.update_layout(showlegend=False, xaxis_title="Mental Health Score", yaxis_title="")
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("Dampak Kualitas Tidur")
    sleep_by_platform = filtered_df.groupby('Platform_Type')['Sleep_Hours_Per_Night'].mean().sort_values()
    
    fig4 = px.bar(
        x=sleep_by_platform.values,
        y=sleep_by_platform.index,
        orientation='h',
        color=sleep_by_platform.values,
        color_continuous_scale='Blues'
    )
    fig4.add_vline(x=6, line_dash="dash", line_color="red",
                   annotation_text="Minimum Sleep")
    fig4.update_layout(showlegend=False, xaxis_title="Jam Tidur per Malam", yaxis_title="")
    st.plotly_chart(fig4, use_container_width=True)

# Row 3: Bubble Chart - Platform Impact Matrix
st.markdown("---")
st.subheader("Platform Impact Matrix")

platform_summary = filtered_df.groupby('Platform_Type').agg({
    'Avg_Daily_Usage_Hours': 'mean',
    'Mental_Health_Score': 'mean',
    'Student_ID': 'count',
    'Addicted_Score': 'mean'
}).reset_index()

fig5 = px.scatter(
    platform_summary,
    x='Avg_Daily_Usage_Hours',
    y='Mental_Health_Score',
    size='Student_ID',
    color='Addicted_Score',
    hover_name='Platform_Type',
    color_continuous_scale='RdYlGn_r',
    size_max=60
)

# Add quadrant lines
fig5.add_hline(y=6, line_dash="dash", line_color="gray", opacity=0.5)
fig5.add_vline(x=4, line_dash="dash", line_color="gray", opacity=0.5)

# Add quadrant labels
fig5.add_annotation(x=2, y=8.5, text="IDEAL<br>(Low Usage, Good Mental Health)", 
                    showarrow=False, bgcolor="lightgreen", opacity=0.7)
fig5.add_annotation(x=6.5, y=8.5, text="CONCERN<br>(High Usage, Good Mental Health)", 
                    showarrow=False, bgcolor="lightyellow", opacity=0.7)
fig5.add_annotation(x=2, y=4.5, text="MONITOR<br>(Low Usage, Poor Mental Health)", 
                    showarrow=False, bgcolor="lightyellow", opacity=0.7)
fig5.add_annotation(x=6.5, y=4.5, text="DANGER<br>(High Usage, Poor Mental Health)", 
                    showarrow=False, bgcolor="lightcoral", opacity=0.7)

fig5.update_layout(
    xaxis_title="Rata-rata Penggunaan (jam/hari)",
    yaxis_title="Rata-rata Mental Health Score",
    height=500
)
st.plotly_chart(fig5, use_container_width=True)

# Row 4: Addiction Level Distribution by Platform
st.markdown("---")
st.subheader("Distribusi Tingkat Kecanduan per Platform")

addiction_dist = filtered_df.groupby(['Platform_Type', 'Addiction_Level']).size().reset_index(name='count')

fig6 = px.bar(
    addiction_dist,
    x='Platform_Type',
    y='count',
    color='Addiction_Level',
    color_discrete_map={
        'Risiko Rendah': '#4CAF50',
        'Risiko Sedang': '#FF9800',
        'Risiko Tinggi': '#F44336'
    },
    barmode='stack'
)
fig6.update_layout(xaxis_title="", yaxis_title="Jumlah Mahasiswa", height=400)
st.plotly_chart(fig6, use_container_width=True)

# Platform Rankings
st.markdown("---")
st.subheader("Ranking Platform")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Platform Paling Berisiko:**")
    risky = platform_summary.nlargest(3, 'Addicted_Score')[['Platform_Type', 'Addicted_Score']]
    for idx, row in risky.iterrows():
        st.error(f"**{row['Platform_Type']}**: Addiction Score {row['Addicted_Score']:.1f}")

with col2:
    st.markdown("**Platform Paling Aman:**")
    safe = platform_summary.nsmallest(3, 'Addicted_Score')[['Platform_Type', 'Addicted_Score']]
    for idx, row in safe.iterrows():
        st.success(f"**{row['Platform_Type']}**: Addiction Score {row['Addicted_Score']:.1f}")

# Insights
st.markdown("---")
st.info("""
**Key Insights:**
- **Visual/Photo** platform (Instagram, Snapchat) memiliki user base terbesar dan addiction score tinggi
- **Video Pendek** (TikTok) memiliki rata-rata penggunaan TERTINGGI (>5.5 jam/hari)
- **Profesional** (LinkedIn) paling aman dengan usage terendah dan mental health terbaik
- Platform dengan usage >5 jam cenderung memiliki mental health score <6 (buruk)
""")
