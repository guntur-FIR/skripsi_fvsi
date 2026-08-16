import streamlit as st
import pandas as pd
import joblib

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Voltage Stability Surrogate Model | Pulo Aceh",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# MODERN ENTERPRISE CSS STYLING
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main {
        background-color: #f8fafc;
    }

    /* Header Banner */
    .dashboard-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 2.5rem 3rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.1);
    }
    .dashboard-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 0.5rem;
    }
    .dashboard-subtitle {
        font-size: 1rem;
        color: #94a3b8;
        font-weight: 400;
    }

    /* Status Badges */
    .badge-safe {
        background-color: #dcfce7;
        color: #166534;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-weight: 700;
        font-size: 0.9rem;
        border: 1px solid #bbf7d0;
    }
    .badge-warning {
        background-color: #fef3c7;
        color: #92400e;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-weight: 700;
        font-size: 0.9rem;
        border: 1px solid #fde68a;
    }
    .badge-critical {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-weight: 700;
        font-size: 0.9rem;
        border: 1px solid #fecaca;
    }

    /* Custom Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD MODEL
# ============================================================
@st.cache_resource
def load_model():
    try:
        return joblib.load('model_stabilitas.pkl')
    except Exception as e:
        return None

model = load_model()

# ============================================================
# SIDEBAR - PARAMETER SKENARIO PENELITIAN PULO ACEH
# ============================================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/electricity.png", width=60)
    st.title("Panel Kontrol Skenario")
    st.markdown("<p style='color: #64748b; font-size: 0.85rem;'>Simulasi Integrasi Renewable Energy (PLTS & PLTB) pada Sistem Kelistrikan Pulo Aceh.</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.subheader("⚙️ Parameter Operasi")
    w_load_scaling = st.slider(
        "Load Scaling (p.u.)", 
        min_value=0.50, max_value=2.00, value=1.00, step=0.01,
        help="Faktor pengali beban sistem Pulo Aceh"
    )

    st.subheader("☀️ Pembangkit Listrik Tenaga Surya (PLTS)")
    w_plts = st.number_input("Kapasitas PLTS (kW)", min_value=0.0, max_value=2000.0, value=100.0, step=10.0)
    w_lok_plts = st.number_input("Lokasi Bus PLTS", min_value=1, max_value=100, value=15, step=1, help="Nomor Bus pada Sistem Pulo Aceh")

    st.subheader("🌬️ Pembangkit Listrik Tenaga Bayu (PLTB)")
    w_pltb = st.number_input("Kapasitas PLTB (kW)", min_value=0.0, max_value=2000.0, value=100.0, step=10.0)
    w_lok_pltb = st.number_input("Lokasi Bus PLTB", min_value=1, max_value=100, value=20, step=1, help="Nomor Bus pada Sistem Pulo Aceh")

    # Hitung Total DG secara otomatis
    w_total_dg = w_plts + w_pltb
    
    st.markdown("---")
    st.info(f"**Total Kapasitas DG Terhitung:**\n### {w_total_dg:.2f} kW")

    st.markdown("<br>", unsafe_allow_html=True)
    predict_button = st.button("🚀 Jalankan Prediksi AI", type="primary", use_container_width=True)

# ============================================================
# MAIN CONTENT AREA
# ============================================================

# Header Banner
st.markdown("""
<div class="dashboard-header">
    <div class="dashboard-title"> Surrogate Model - Pulo Aceh</div>
    <div class="dashboard-subtitle">Sistem Penunjang Keputusan Cepat (Fast Screening Tool) Berbasis Machine Learning untuk Analisis Jaringan Kelistrikan Pulo Aceh.</div>
</div>
""", unsafe_allow_html=True)

# Batasan Ruang Lingkup Penelitian Info Box
with st.expander("📌 Informasi Ruang Lingkup & Batasan Penelitian", expanded=False):
    st.markdown("""
    * **Objek Sistem:** Jaringan Kelistrikan Wilayah **Pulo Aceh**.
    * **Sumber Energi Terbarukan:** Integrasi Distributed Generation (DG) jenis **PLTS (Solar)** dan **PLTB (Bayu/Angin)**.
    * **Indikator Kestabilan:** Menggunakan *Fast Voltage Stability Index* Maximum (**FVSI Max**).
    * **Standar Evaluasi:**
      * $\\text{FVSI} < 0.90$ $\\rightarrow$ **Aman / Stabil**
      * $0.90 \\le \\text{FVSI} < 1.00$ $\\rightarrow$ **Waspada / Mendekati Batas Kritis**
      * $\\text{FVSI} \\ge 1.00$ $\\rightarrow$ **Kritis / Tidak Stabil (Risiko Collapse)**
    * **Catatan:** Aplikasi ini berfungsi sebagai *screening* awal pendukung simulasi *DIgSILENT PowerFactory*.
    """)

# Main Prediction Logic
if model is None:
    st.error("⚠️ File model `model_stabilitas.pkl` tidak ditemukan atau gagal dimuat! Pastikan file model sudah di-upload ke repository GitHub.")
else:
    # Siapkan dataframe input sesuai urutan fitur saat training model
    input_df = pd.DataFrame([[
        w_load_scaling, 
        w_plts, 
        w_pltb, 
        w_total_dg, 
        w_lok_plts, 
        w_lok_pltb
    ]], columns=['Load Scaling', 'PLTS', 'PLTB', 'Total DG', 'Lokasi PLTS', 'Lokasi PLTB'])

    if predict_button or True: # Otomatis hitung / jalankan
        hasil_pred = model.predict(input_df)[0]
        
        # Penentuan Status Berdasarkan Ambang Batas FVSI
        if hasil_pred < 0.90:
            status_text = "AMAN (STABIL)"
            badge_class = "badge-safe"
            desc_text = "Sistem Pulo Aceh berada dalam kondisi operasi normal dan stabil. Margin tegangan masih sangat aman."
        elif hasil_pred < 1.00:
            status_text = "WARNING (WASPADA)"
            badge_class = "badge-warning"
            desc_text = "Sistem Pulo Aceh mendekati batas kestabilan. Diperlukan pengaturan daya atau penambahan kompensator."
        else:
            status_text = "KRITIS (TIDAK STABIL)"
            badge_class = "badge-critical"
            desc_text = "Peringatan! Sistem Pulo Aceh berisiko mengalami *voltage collapse* (runtuhnya tegangan)."

        # Tampilan Hasil Utama (Metrics & Card)
        col1, col2 = st.columns([1.5, 1])

        with col1:
            st.markdown("### 📊 Hasil Evaluasi Model")
            m_col1, m_col2 = st.columns(2)
            with m_col1:
                st.metric(label="Estimasi Nilai FVSI Max", value=f"{hasil_pred:.6f}")
            with m_col2:
                st.markdown("**Status Sistem:**")
                st.markdown(f"<br><span class='{badge_class}'>✓ {status_text}</span>", unsafe_allow_html=True)
            
            st.markdown(f"<p style='margin-top: 1.5rem; color: #475467; font-size: 0.95rem;'>{desc_text}</p>", unsafe_allow_html=True)

        with col2:
            st.markdown("### 📋 Ringkasan Skenario")
            st.markdown(f"""
            - **Load Factor:** `{w_load_scaling} p.u.`
            - **Total DG:** `{w_total_dg:.1f} kW`
            - **PLTS:** `{w_plts} kW` (Bus {w_lok_plts})
            - **PLTB:** `{w_pltb} kW` (Bus {w_lok_pltb})
            """)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #94a3b8; font-size: 0.8rem;'>Skripsi Program Studi Teknik Elektro Universitas Syiah Kuala · Surrogate Model Kestabilan Tegangan Pulo Aceh 2026</p>", 
    unsafe_allow_html=True
)
