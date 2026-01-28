"""
Page 2: Analisis Kelompok Rentan
================================
Fokus pada perempuan muda dan laki-laki sangat muda yang berisiko tinggi
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Kelompok Rentan", page_icon="⚠", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv('dataset_looker_student_social_media_clean.csv')

st.title("Analisis Kelompok Rentan")
st.markdown("---")

df = load_data()

# Filter hanya kelompok rentan
vulnerable_df = df[df['Vulnerable_Group'].str.contains("Ya", na=False)]

# KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    perempuan_muda = len(vulnerable_df[vulnerable_df['Vulnerable_Group'].str.contains("Perempuan")])
    st.metric("Perempuan Muda (≤21th)", f"{perempuan_muda}", 
              delta=f"{perempuan_muda/len(df)*100:.1f}% dari total")

with col2:
    laki_muda = len(vulnerable_df[vulnerable_df['Vulnerable_Group'].str.contains("Laki-laki")])
    st.metric("Laki-laki Sangat Muda (≤19th)", f"{laki_muda}",
              delta=f"{laki_muda/len(df)*100:.1f}% dari total")

with col3:
    avg_addiction = vulnerable_df['Addicted_Score'].mean()
    st.metric("Avg Addiction Score", f"{avg_addiction:.1f}/10",
              delta="Lebih tinggi dari rata-rata", delta_color="inverse")

with col4:
    high_risk_vulnerable = len(vulnerable_df[vulnerable_df['High_Risk_Addiction'] == 'Ya'])
    st.metric("Risiko Tinggi", f"{high_risk_vulnerable}",
              delta=f"{high_risk_vulnerable/len(vulnerable_df)*100:.1f}%", delta_color="inverse")

st.markdown("---")

# Row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("Breakdown Kelompok Rentan")
    vulnerable_breakdown = vulnerable_df['Vulnerable_Group'].value_counts()
    fig1 = px.pie(
        values=vulnerable_breakdown.values,
        names=vulnerable_breakdown.index,
        color_discrete_sequence=['#FF6B6B', '#FFA07A']
    )
    fig1.update_traces(textposition='inside', textinfo='percent+label+value')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Tingkat Kecanduan per Kelompok")
    vulnerable_addiction = vulnerable_df.groupby(['Vulnerable_Group', 'Addiction_Level']).size().reset_index(name='count')
    fig2 = px.bar(
        vulnerable_addiction,
        x='Vulnerable_Group',
        y='count',
        color='Addiction_Level',
        color_discrete_map={
            'Risiko Rendah': '#4CAF50',
            'Risiko Sedang': '#FF9800',
            'Risiko Tinggi': '#F44336'
        },
        barmode='group'
    )
    st.plotly_chart(fig2, use_container_width=True)

# Row 2
col1, col2 = st.columns(2)

with col1:
    st.subheader("Platform yang Digunakan Kelompok Rentan")
    platform_vulnerable = vulnerable_df['Platform_Type'].value_counts().head(6)
    fig3 = px.bar(
        x=platform_vulnerable.values,
        y=platform_vulnerable.index,
        orientation='h',
        color=platform_vulnerable.values,
        color_continuous_scale='Reds'
    )
    fig3.update_layout(showlegend=False, xaxis_title="Jumlah Pengguna", yaxis_title="")
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("Kesehatan Mental Kelompok Rentan")
    mental_vulnerable = vulnerable_df['Mental_Health_Detail'].value_counts()
    fig4 = px.bar(
        x=mental_vulnerable.index,
        y=mental_vulnerable.values,
        color=mental_vulnerable.index,
        color_discrete_map={
            'Sangat Buruk (1-3)': '#D32F2F',
            'Buruk (4-5)': '#F44336',
            'Sedang (6-7)': '#FF9800',
            'Baik (8-10)': '#4CAF50'
        }
    )
    fig4.update_layout(showlegend=False, xaxis_title="", yaxis_title="Jumlah")
    st.plotly_chart(fig4, use_container_width=True)

# Row 3: High Priority Table
st.markdown("---")
st.subheader("Daftar Prioritas Tinggi (Risiko Tinggi + Kelompok Rentan)")

high_priority = vulnerable_df[
    (vulnerable_df['High_Risk_Addiction'] == 'Ya') |
    (vulnerable_df['Addicted_Score'] >= 8)
].sort_values('Addicted_Score', ascending=False)

if len(high_priority) > 0:
    display_cols = [
        'Student_ID', 'Age', 'Gender', 'Vulnerable_Group', 
        'Platform_Type', 'Avg_Daily_Usage_Hours', 'Addicted_Score',
        'Mental_Health_Score', 'Academic_Impact_Label'
    ]
    
    # Color coding for addiction score
    def highlight_score(val):
        if val >= 9:
            return 'background-color: #F44336; color: white'
        elif val >= 8:
            return 'background-color: #FF9800; color: white'
        return ''
    
    styled_table = high_priority[display_cols].style.applymap(
        highlight_score, 
        subset=['Addicted_Score']
    )
    
    st.dataframe(styled_table, use_container_width=True, height=400)
    
    st.info(f"Total {len(high_priority)} mahasiswa memerlukan perhatian khusus")
else:
    st.success("Tidak ada kelompok rentan dengan risiko tinggi")

# Statistics comparison
st.markdown("---")
st.subheader("Perbandingan: Kelompok Rentan vs Non-Rentan")

non_vulnerable = df[~df['Vulnerable_Group'].str.contains("Ya", na=False)]

comparison_data = {
    'Metrik': [
        'Rata-rata Penggunaan (jam/hari)',
        'Rata-rata Addiction Score',
        'Rata-rata Mental Health Score',
        'Rata-rata Jam Tidur',
        '% Risiko Tinggi',
        '% Terdampak Akademik'
    ],
    'Kelompok Rentan': [
        f"{vulnerable_df['Avg_Daily_Usage_Hours'].mean():.1f}",
        f"{vulnerable_df['Addicted_Score'].mean():.1f}",
        f"{vulnerable_df['Mental_Health_Score'].mean():.1f}",
        f"{vulnerable_df['Sleep_Hours_Per_Night'].mean():.1f}",
        f"{(vulnerable_df['High_Risk_Addiction'] == 'Ya').sum() / len(vulnerable_df) * 100:.1f}%",
        f"{(vulnerable_df['Academic_Impact_Label'] == 'Terdampak').sum() / len(vulnerable_df) * 100:.1f}%"
    ],
    'Non-Rentan': [
        f"{non_vulnerable['Avg_Daily_Usage_Hours'].mean():.1f}",
        f"{non_vulnerable['Addicted_Score'].mean():.1f}",
        f"{non_vulnerable['Mental_Health_Score'].mean():.1f}",
        f"{non_vulnerable['Sleep_Hours_Per_Night'].mean():.1f}",
        f"{(non_vulnerable['High_Risk_Addiction'] == 'Ya').sum() / len(non_vulnerable) * 100:.1f}%",
        f"{(non_vulnerable['Academic_Impact_Label'] == 'Terdampak').sum() / len(non_vulnerable) * 100:.1f}%"
    ]
}

comparison_df = pd.DataFrame(comparison_data)
st.table(comparison_df)

st.warning("""
**Rekomendasi Intervensi:**
1. Fokus pada perempuan usia 16-21 tahun pengguna Instagram/TikTok
2. Program digital wellness untuk kelompok rentan
3. Konseling kesehatan mental prioritas
4. Monitoring penggunaan media sosial >5 jam/hari
""")
