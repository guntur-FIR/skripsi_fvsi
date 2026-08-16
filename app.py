import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Prediksi Kestabilan FVSI Max", page_icon="⚡", layout="centered")

st.title("⚡ Dashboard Surrogate Model Kestabilan Tegangan")
st.write("Sistem Pendukung Keputusan Berbasis Machine Learning untuk Analisis FVSI Max.")

@st.cache_resource
def load_model():
    try:
        return joblib.load('model_stabilitas.pkl')
    except Exception as e:
        return None

model = load_model()

if model is None:
    st.error("⚠️ File model 'model_stabilitas.pkl' tidak dapat dimuat! Pastikan nama file sudah benar.")
else:
    st.sidebar.header("🔧 Panel Skenario Input")
    w_load_scaling = st.sidebar.number_input("Load Scaling", value=1.00, step=0.01)
    w_plts = st.sidebar.number_input("Kapasitas PLTS (kW)", value=100.0, step=10.0)
    w_pltb = st.sidebar.number_input("Kapasitas PLTB (kW)", value=100.0, step=10.0)
    w_lok_plts = st.sidebar.number_input("Lokasi Bus PLTS", value=15, step=1)
    w_lok_pltb = st.sidebar.number_input("Lokasi Bus PLTB", value=20, step=1)

    w_total_dg = w_plts + w_pltb
    st.sidebar.markdown("---")
    st.sidebar.text(f"Total DG Terhitung: {w_total_dg:.2f} kW")

    if st.button("🚀 Jalankan Analisis Prediksi"):
        input_df = pd.DataFrame([[w_load_scaling, w_plts, w_pltb, w_total_dg, w_lok_plts, w_lok_pltb]], 
                                columns=['Load Scaling', 'PLTS', 'PLTB', 'Total DG', 'Lokasi PLTS', 'Lokasi PLTB'])
        
        hasil_pred = model.predict(input_df)[0]
        
        if hasil_pred < 0.90:
            status, color = "AMAN (STABIL)", "green"
        elif hasil_pred < 1.00:
            status, color = "WARNING (WASPADA)", "orange"
        else:
            status, color = "KRITIS (TIDAK STABIL)", "red"
            
        st.markdown("### 📊 Hasil Evaluasi Sistem:")
        st.metric(label="Estimasi FVSI Max", value=f"{hasil_pred:.6f}")
        st.markdown(f"**Status Sistem:** :{color}[**{status}**]")

# 2. Perintah untuk langsung mendownload file app.py ke laptop
from google.colab import files
files.download('app.py')
