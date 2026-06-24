import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# --- 1. INJEKSI CSS CUSTOM (UI DASHBOARD PROFESIONAL) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: #E0E0E0;
    }
    div[data-testid="metric-container"] {
        background-color: #1E1E1E;
        border-left: 5px solid #D32F2F;
        padding: 5% 5% 5% 10%;
        border-radius: 5px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    .stSlider > div > div > div > div {
        background-color: #D32F2F !important;
    }
    /* Mempercantik tampilan Bar Chart bawaan Streamlit */
    [data-testid="stVegaLiteChart"] {
        background-color: #1E1E1E;
        padding: 1rem;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. PERSIAPAN MODEL DAN BASELINE ---
# Fitur: [Iklan (Juta), Diskon (%)]
X_train = np.array([[5, 10], [10, 20], [15, 5], [20, 25], [25, 15]])
# Target: Keuntungan (Juta)
y_train = np.array([50, 80, 110, 90, 150])

# Melatih model regresi
model = LinearRegression().fit(X_train, y_train)

# Kondisi saat ini: Iklan 10 Juta, Diskon 10%
baseline_input = np.array([[10, 10]])
baseline_pred = model.predict(baseline_input)[0]

# --- 3. IMPLEMENTASI UI INTERAKTIF ---
st.title("🎯 Simulator Kebijakan Profitabilitas")
st.write("Atur **Tuas Kebijakan** di panel samping untuk mensimulasikan skenario *What-If* dan melihat dampaknya terhadap proyeksi keuntungan.")

# Sidebar untuk Variabel Kontrol
st.sidebar.header("🕹️ Tuas Kebijakan (Intervensi)")
iklan_slider = st.sidebar.slider("Anggaran Iklan (Juta Rp)", 0, 50, 10)
diskon_slider = st.sidebar.slider("Besaran Diskon (%)", 0, 50, 10)

# --- 4. ENGINE SIMULASI (ANALISIS WHAT-IF) ---
# Menghitung prediksi intervensi dan Delta
intervention_input = np.array([[iklan_slider, diskon_slider]])
hasil_pred = model.predict(intervention_input)[0]
delta = hasil_pred - baseline_pred

# --- 5. VISUALISASI HASIL ---
# Menampilkan Metrik
col1, col2 = st.columns(2)
col1.metric("Proyeksi Keuntungan (Intervensi)", f"Rp {hasil_pred:.2f} Jt", f"{delta:.2f} Jt")
col2.metric("Target Keuntungan (Baseline)", f"Rp {baseline_pred:.2f} Jt", "Kondisi Saat Ini", delta_color="off")

st.markdown("---")
st.subheader("📊 Perbandingan Skenario")

# Visualisasi Bar Chart
data_plot = pd.DataFrame({
    'Skenario': ['Baseline (Saat Ini)', 'Intervensi (Simulasi)'],
    'Keuntungan (Juta Rp)': [baseline_pred, hasil_pred]
})

st.bar_chart(data=data_plot, x='Skenario', y='Keuntungan (Juta Rp)', color="#D32F2F")

# Elemen Analisis Risiko
if delta > 0:
    st.success(f"**Strategi Optimal!** Skenario ini diproyeksikan menghasilkan tambahan laba sebesar **Rp {delta:.2f} Juta**.")
elif delta < 0:
    st.error(f"**Risiko Penurunan!** Skenario ini berpotensi merugikan dengan estimasi penurunan laba sebesar **Rp {abs(delta):.2f} Juta**.")
else:
    st.info("Kondisi stagnan. Tidak ada perubahan performa dibandingkan kondisi saat ini.")