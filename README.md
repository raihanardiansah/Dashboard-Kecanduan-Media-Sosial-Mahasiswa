# 📱 Dashboard Kecanduan Media Sosial Mahasiswa

Dashboard interaktif untuk menganalisis pola kecanduan media sosial berdasarkan Bergen Social Media Addiction Scale (BSMAS).

## 🚀 Cara Menjalankan (LOKAL/OFFLINE)

### 1. Install Dependencies

Buka **Command Prompt** atau **PowerShell** di folder ini, lalu jalankan:

```bash
pip install -r requirements.txt
```

### 2. Jalankan Dashboard

```bash
streamlit run app.py
```

### 3. Buka di Browser

Dashboard akan otomatis terbuka di browser di alamat:
```
http://localhost:8501
```

**✅ Dashboard berjalan 100% OFFLINE di komputer Anda!**

---

## 📁 Struktur File

```
PVD/
├── app.py                                    # Halaman utama dashboard
├── pages/
│   ├── 2_📊_Kelompok_Rentan.py              # Analisis kelompok rentan
│   └── 3_🔍_Platform_Analysis.py            # Analisis platform
├── dataset_looker_student_social_media_clean.csv  # Data (HARUS ADA)
├── requirements.txt                          # Dependencies
└── README.md                                 # File ini
```

---

## 📊 Fitur Dashboard

### **Halaman 1: Executive Dashboard** (Main)
- 📌 KPI Cards: Total mahasiswa, Risiko tinggi, Kelompok rentan, Penggunaan tinggi
- 🎯 Donut chart: Distribusi tingkat kecanduan
- 📱 Bar chart: Platform paling populer
- 🔥 Heatmap: Usia vs Gender vs Addiction score
- 💡 Scatter plot: Penggunaan vs Kesehatan mental (dengan trendline)
- 🧠 Bar chart: Distribusi kesehatan mental
- 😴 Bar chart: Distribusi kualitas tidur
- 📈 Statistik ringkasan

**Filter Interaktif:**
- Gender
- Kelompok Usia
- Jenis Platform
- Tingkat Kecanduan
- Checkbox: Kelompok Rentan saja

### **Halaman 2: Kelompok Rentan**
- ⚠️ KPI khusus kelompok rentan
- 📊 Breakdown perempuan muda vs laki-laki sangat muda
- 🎯 Tingkat kecanduan per kelompok
- 📱 Platform favorit kelompok rentan
- 🧠 Kesehatan mental kelompok rentan
- 🚨 Tabel prioritas tinggi (high-risk vulnerable students)
- 📊 Perbandingan: Rentan vs Non-rentan
- ⚠️ Rekomendasi intervensi

### **Halaman 3: Platform Analysis**
- 📊 Tabel metrik per platform (usage, addiction, mental health, sleep)
- ⏱️ Bar chart: Rata-rata penggunaan per platform
- 🎯 Bar chart: Addiction score per platform
- 🧠 Bar chart: Dampak kesehatan mental per platform
- 😴 Bar chart: Dampak kualitas tidur per platform
- 💡 Bubble chart: Platform Impact Matrix (quadrant analysis)
- 📊 Stacked bar: Distribusi tingkat kecanduan per platform
- 🏆 Ranking: Platform paling berisiko vs paling aman
- 💡 Key insights

---

## 🎨 Insight Yang Ditampilkan

### 1. **Kelompok Rentan (Prioritas Intervensi)**
- 50.2% mahasiswa adalah kelompok rentan
- Perempuan muda (≤21 th): 45%
- Laki-laki sangat muda (≤19 th): 5.2%

### 2. **Risiko Kecanduan**
- 7.8% risiko tinggi (threshold ≥8.67 sesuai BSMAS)
- 58.7% risiko sedang
- 33.5% risiko rendah

### 3. **Penggunaan Platform**
- 76% mahasiswa gunakan >4 jam/hari (threshold penelitian)
- Visual/Photo (Instagram/Snapchat): 37% users
- Video Pendek (TikTok): Penggunaan TERTINGGI (5.5 jam/hari)
- Profesional (LinkedIn): Paling aman

### 4. **Dampak Kesehatan**
- 28.7% kesehatan mental buruk
- 53.7% sleep deprived (<6 jam tidur)
- Korelasi negatif: Lebih banyak usage → Mental health lebih buruk

---

## ⚙️ Troubleshooting

### Error: "File not found"
**Solusi:** Pastikan file `dataset_looker_student_social_media_clean.csv` ada di folder yang sama dengan `app.py`

### Error: "Module not found"
**Solusi:** Install dependencies:
```bash
pip install streamlit pandas plotly
```

### Dashboard tidak muncul
**Solusi:** 
1. Pastikan port 8501 tidak dipakai aplikasi lain
2. Coba jalankan dengan port berbeda:
   ```bash
   streamlit run app.py --server.port 8502
   ```

### Data tidak muncul/kosong
**Solusi:** Cek apakah nama kolom di CSV sesuai dengan yang digunakan di code

---

## 🛠️ Customization

### Mengubah Warna
Edit bagian `color_discrete_map` di setiap chart:
```python
color_discrete_map={
    'Risiko Rendah': '#4CAF50',    # Hijau
    'Risiko Sedang': '#FF9800',    # Orange
    'Risiko Tinggi': '#F44336'     # Merah
}
```

### Menambah Filter
Edit bagian `st.sidebar` di `app.py`:
```python
# Contoh: Tambah filter country
country_options = ["Semua"] + sorted(df['Country'].unique())
selected_country = st.sidebar.selectbox("Negara:", country_options)
```

---

## 📚 Teknologi yang Digunakan

- **Streamlit**: Framework dashboard Python
- **Pandas**: Data manipulation
- **Plotly**: Interactive charts
- **Python 3.8+**: Base language

---

## 🌐 Deploy Online (OPSIONAL)

Jika ingin share dashboard ke orang lain:

### 1. Push ke GitHub
```bash
git init
git add .
git commit -m "Initial dashboard"
git push
```

### 2. Deploy ke Streamlit Cloud
1. Buka https://streamlit.io/cloud
2. Connect GitHub repository
3. Deploy!
4. Dapatkan link public: `https://your-app.streamlit.app`

**100% GRATIS!**

---

## 📝 Lisensi & Credits

Dashboard ini dibuat untuk analisis kecanduan media sosial mahasiswa berdasarkan:
- **Bergen Social Media Addiction Scale (BSMAS)**
- Data: 705 mahasiswa dari berbagai negara
- Threshold: Risiko tinggi ≥8.67 (setara 26/30 dalam BSMAS original)

---

## 💡 Tips Penggunaan

1. **Gunakan Filter**: Sidebar filter sangat powerful untuk drill-down analysis
2. **Hover Charts**: Hover mouse di chart untuk melihat detail data
3. **Multi-select**: Filter platform bisa pilih multiple untuk compare
4. **Export Data**: Klik kanan pada tabel → Download as CSV
5. **Screenshot**: Streamlit punya built-in screenshot feature di menu (⋮)

---

## 📞 Support

Jika ada pertanyaan atau error, cek:
1. Pastikan Python version ≥ 3.8
2. Pastikan semua dependencies terinstall
3. Pastikan file CSV ada dan formatnya benar
4. Restart dashboard jika ada perubahan code

---

**Selamat Menganalisis! 📊🎉**
