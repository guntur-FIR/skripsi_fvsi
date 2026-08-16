import streamlit as st
import pandas as pd
import joblib

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Surrogate Model | Pulo Aceh",
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

# Daftar Bus Spesifik Pulo Aceh
VALID_BUS_LIST = [17, 18, 19, 20, 21, 22]

# ============================================================
# SIDEBAR - PARAMETER SKENARIO PULO ACEH
# ============================================================
with st.sidebar:
    st.markdown("Pulo Aceh Grid")
    st.markdown("<p style='color: #64748b; font-size: 0.85rem;'>Surrogate Model Screening Integrasi PLTS & PLTB (Random Forest).</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.subheader("Parameter Operasi")
    w_load_scaling = st.slider(
        "Load Scaling (p.u.)", 
        min_value=1.00, max_value=2.00, value=1.00, step=0.01,
        help="Faktor pengali beban sistem eksisting Pulo Aceh (1.00 - 2.00)"
    )

    st.subheader("PLTS")
    w_plts = st.slider("Kapasitas PLTS (kW)", min_value=0.0, max_value=300.0, value=100.0, step=10.0, help="Batasan domain data hingga 300 kW")
    w_lok_plts = st.selectbox("📍 Lokasi Bus PLTS", options=VALID_BUS_LIST, index=0, help="Pilihan bus penempatan PLTS")

    st.subheader("PLTB")
    w_pltb = st.slider("Kapasitas PLTB (kW)", min_value=0.0, max_value=300.0, value=100.0, step=10.0, help="Batasan domain data hingga 300 kW")
    w_lok_pltb = st.selectbox("📍 Lokasi Bus PLTB", options=VALID_BUS_LIST, index=1, help="Pilihan bus penempatan PLTB")

    # Hitung Total DG dan Estimasi Persen Penetrasi (Asumsi kapasitas basis sistem total misal 1000 kW atau 1 MW untuk basis kalkulasi persentase)
    w_total_dg = w_plts + w_pltb
    # Estimasi persentase penetrasi terhadap basis beban/kapasitas sistem Pulo Aceh
    base_system_capacity = 1000.0 # kW (Dapat disesuaikan dengan kapasitas basis sistem eksisting)
    penetration_pct = (w_total_dg / base_system_capacity) * 100
    
    st.markdown("---")
    st.info(f"**Total Kapasitas DG:** {w_total_dg:.1f} kW\n**Penetrasi DG:** {penetration_pct:.1f}%")

# ============================================================
# MAIN CONTENT AREA
# ============================================================

# Header Banner
st.markdown("""
<div class="dashboard-header">
    <div class="dashboard-title">SURROGATE MODEL (FVSI Max) - Pulo Aceh</div>
    <div class="dashboard-subtitle">Fast Screening Tool Berbasis Random Forest Machine Learning untuk Analisis Jaringan Distribusi Pulo Aceh.</div>
</div>
""", unsafe_allow_html=True)

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

    # Tombol Prediksi diletakkan di tengah dengan tampilan menarik
    st.markdown("<br>", unsafe_allow_html=True)
    col_space1, col_btn, col_space2 = st.columns([1, 2, 1])
    with col_btn:
        predict_button = st.button("Prediksi", type="primary", use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if predict_button:
        hasil_pred = model.predict(input_df)[0]
        
        # Penentuan Status Berdasarkan Ambang Batas FVSI
        if hasil_pred < 0.90:
            status_text = "AMAN (STABIL)"
            badge_class = "badge-safe"
            desc_text = "Sistem distribusi Pulo Aceh diprediksi berada dalam kondisi operasi normal dan stabil."
        elif hasil_pred < 1.00:
            status_text = "WARNING (WASPADA)"
            badge_class = "badge-warning"
            desc_text = "Sistem Pulo Aceh mendekati batas kriteria kestabilan. Disarankan untuk memverifikasi ulang via DIgSILENT PowerFactory."
        else:
            status_text = "KRITIS (TIDAK STABIL)"
            badge_class = "badge-critical"
            desc_text = "Peringatan! Indikator FVSI melebihi batas 1.00. Sistem berpotensi mengalami gangguan kestabilan / voltage collapse."

        # Tampilan Hasil Utama (Metrics & Card)
        col1, col2 = st.columns([1.5, 1])

        with col1:
            st.markdown("### 📊 Hasil Surrogate Model")
            m_col1, m_col2 = st.columns(2)
            with m_col1:
                st.metric(label="Estimasi FVSI Max (Prediksi)", value=f"{hasil_pred:.6f}")
            with m_col2:
                st.markdown("**Status Kestabilan:**")
                st.markdown(f"<br><span class='{badge_class}'>✓ {status_text}</span>", unsafe_allow_html=True)
            
            st.markdown(f"<p style='margin-top: 1.5rem; color: #475467; font-size: 0.95rem;'>{desc_text}</p>", unsafe_allow_html=True)

        with col2:
            st.markdown("### 📋 Skenario")
            st.markdown(f"""
            - **Load Scaling:** `{w_load_scaling:.2f} p.u.`
            - **Total Kapasitas DG:** `{w_total_dg:.1f} kW`
            - **Nilai Penetrasi DG:** `{penetration_pct:.1f}%`
            - **PLTS:** `{w_plts} kW` (Bus {w_lok_plts})
            - **PLTB:** `{w_pltb} kW` (Bus {w_lok_pltb})
            """)

# ============================================================
# RUANG LINGKUP & BATASAN PENELITIAN (DI BAGIAN BAWAH)
# ============================================================
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("📌 Informasi Ruang Lingkup & Batasan Penelitian (Pulo Aceh)", expanded=False):
    st.markdown("""
    * **Objek Sistem:** Jaringan distribusi tenaga listrik eksisting berbasis PLTD di wilayah **Pulo Aceh**.
    * **Integrasi DG:** Skenario penambahan **PLTS** dan **PLTB** dengan kapasitas masing-masing hingga **300 kW** (Total DG hingga **600 kW**). Lokasi penempatan bus difokuskan pada **Bus 17, 18, 19, 20, 21, dan 22**.
    * **Ground Truth:** Diperoleh dari simulasi *load flow analysis* kondisi *steady-state* menggunakan **DIgSILENT PowerFactory**.
    * **Parameter Sistem:** Tegangan bus ($V$), daya aktif ($P$), daya reaktif ($Q$), *voltage deviation*, *voltage rise*, dan *Fast Voltage Stability Index* (**FVSI**).
    * **Indikator Status Stabilitas (Ambang Batas FVSI):**
      * $\\text{FVSI} < 0.90$ $\\rightarrow$ **Aman / Stabil**
      * $0.90 \\le \\text{FVSI} < 1.00$ $\\rightarrow$ **Waspada / Mendekati Batas**
      * $\\text{FVSI} \\ge 1.00$ $\\rightarrow$ **Kritis / Tidak Stabil (Risiko *Voltage Collapse*)**
    * **Catatan Penting:** Model ini merupakan *screening* awal (*surrogate model* berbasis *Random Forest*) dan **bukan pengganti penuh DIgSILENT PowerFactory**. Kondisi mendekati kritis wajib diverifikasi ulang.
    """)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #94a3b8; font-size: 0.8rem;'>Skripsi Program Studi Teknik Elektro Universitas Syiah Kuala · Analisis Kestabilan Sistem Pulo Aceh Berbasis Machine Learning</p>", 
    unsafe_allow_html=True
)
