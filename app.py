import streamlit as st
import pandas as pd
import joblib

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Surrogate Model | Pulo Aceh",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# MODERN ENTERPRISE CSS STYLING
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    :root {
        --bg-main: #0b1220;
        --bg-panel: #ffffff;
        --accent-1: #6366f1;
        --accent-2: #06b6d4;
        --accent-3: #f59e0b;
        --text-dark: #0f172a;
        --text-muted: #64748b;
        --border-soft: #e2e8f0;
    }

    .stApp {
        background: linear-gradient(180deg, #f4f6fb 0%, #eef1f8 100%);
    }

    /* ---------- Header Banner ---------- */
    .dashboard-header {
        position: relative;
        overflow: hidden;
        background: linear-gradient(120deg, #0b1220 0%, #1e2749 45%, #3730a3 100%);
        padding: 2.6rem 2rem;
        border-radius: 24px;
        color: white;
        margin-bottom: 1.8rem;
        box-shadow: 0 20px 40px -12px rgba(30, 39, 73, 0.45);
        text-align: center;
    }
    .dashboard-header::before {
        content: "";
        position: absolute;
        top: -60px; right: -60px;
        width: 220px; height: 220px;
        background: radial-gradient(circle, rgba(6,182,212,0.35) 0%, rgba(6,182,212,0) 70%);
        border-radius: 50%;
    }
    .dashboard-header::after {
        content: "";
        position: absolute;
        bottom: -80px; left: -40px;
        width: 260px; height: 260px;
        background: radial-gradient(circle, rgba(99,102,241,0.35) 0%, rgba(99,102,241,0) 70%);
        border-radius: 50%;
    }
    .dashboard-eyebrow {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #a5b4fc;
        background: rgba(99,102,241,0.15);
        border: 1px solid rgba(165,180,252,0.3);
        padding: 0.3rem 0.9rem;
        border-radius: 50px;
        margin-bottom: 1rem;
    }
    .dashboard-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.1rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 0.6rem;
        color: #ffffff;
        position: relative;
        z-index: 1;
    }
    .dashboard-subtitle {
        font-size: 0.95rem;
        color: #cbd5e1;
        font-weight: 400;
        line-height: 1.6;
        max-width: 620px;
        margin: 0 auto;
        position: relative;
        z-index: 1;
    }

    /* ---------- Status Badges ---------- */
    .badge-safe, .badge-warning, .badge-critical {
        padding: 0.55rem 1.2rem;
        border-radius: 50px;
        font-weight: 700;
        font-size: 0.88rem;
        display: inline-block;
        letter-spacing: 0.2px;
    }
    .badge-safe {
        background: linear-gradient(120deg, #dcfce7, #bbf7d0);
        color: #166534;
        border: 1px solid #86efac;
        box-shadow: 0 4px 10px -4px rgba(22,101,52,0.3);
    }
    .badge-warning {
        background: linear-gradient(120deg, #fef3c7, #fde68a);
        color: #92400e;
        border: 1px solid #fcd34d;
        box-shadow: 0 4px 10px -4px rgba(146,64,14,0.3);
    }
    .badge-critical {
        background: linear-gradient(120deg, #fee2e2, #fecaca);
        color: #991b1b;
        border: 1px solid #fca5a5;
        box-shadow: 0 4px 10px -4px rgba(153,27,27,0.3);
    }

    /* ---------- Cards ---------- */
    .glass-card {
        background: var(--bg-panel);
        border-radius: 18px;
        padding: 1.6rem 1.7rem;
        border: 1px solid var(--border-soft);
        box-shadow: 0 8px 24px -10px rgba(15, 23, 42, 0.08);
        height: 100%;
    }
    .card-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.02rem;
        font-weight: 700;
        color: var(--text-dark);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .scenario-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.6rem 0;
        border-bottom: 1px dashed var(--border-soft);
        font-size: 0.9rem;
    }
    .scenario-row:last-child { border-bottom: none; }
    .scenario-label { color: var(--text-muted); font-weight: 500; }
    .scenario-value {
        color: var(--text-dark);
        font-weight: 700;
        font-family: 'Space Grotesk', sans-serif;
        background: #eef2ff;
        padding: 0.15rem 0.6rem;
        border-radius: 8px;
    }

    /* ---------- Metric look ---------- */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
        border: 1px solid var(--border-soft);
        border-radius: 14px;
        padding: 1rem 1.2rem;
    }
    div[data-testid="stMetricLabel"] { font-weight: 600; color: var(--text-muted); }
    div[data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', sans-serif;
        color: var(--text-dark);
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b1220 0%, #151f38 100%);
        border-right: none;
    }
    section[data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    section[data-testid="stSidebar"] h3 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] .stSubheader, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.1);
    }
    section[data-testid="stSidebar"] input, 
    section[data-testid="stSidebar"] select,
    section[data-testid="stSidebar"] .stNumberInput input {
        background-color: #1e2749 !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #1e2749 !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
    }
    section[data-testid="stSidebar"] .stAlert {
        background: linear-gradient(120deg, rgba(99,102,241,0.18), rgba(6,182,212,0.15));
        border: 1px solid rgba(165,180,252,0.3);
        border-radius: 12px;
    }

    /* ---------- Buttons ---------- */
    div.stButton > button {
        background: linear-gradient(120deg, #6366f1, #4338ca);
        color: white;
        font-weight: 700;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1rem;
        letter-spacing: 0.3px;
        box-shadow: 0 8px 20px -6px rgba(67, 56, 202, 0.5);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 24px -6px rgba(67, 56, 202, 0.6);
        color: white;
    }

    /* ---------- Expander ---------- */
    .streamlit-expanderHeader {
        font-weight: 700;
        color: var(--text-dark);
        background-color: #f8fafc;
        border-radius: 12px;
    }

    /* ---------- Section heading ---------- */
    .section-heading {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.15rem;
        color: var(--text-dark);
        margin: 0.4rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    footer, #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD MODEL
# ============================================================
@st.cache_resource
def load_model():
    try:
        return joblib.load('model_stabilitas.pkl')
    except Exception:
        return None

model = load_model()

# Daftar Bus Spesifik Pulo Aceh
VALID_BUS_LIST = [17, 18, 19, 20, 21, 22]

# ============================================================
# SIDEBAR - PARAMETER SKENARIO PULO ACEH
# ============================================================
with st.sidebar:
    st.markdown("### ⚡ Pulo Aceh Grid")
    st.markdown(
        "<p style='color:#94a3b8; font-size:0.85rem; line-height:1.5;'>"
        "Surrogate Model Screening Integrasi PLTS & PLTB berbasis Random Forest.</p>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    st.subheader("🎛️ Parameter Operasi")
    w_load_scaling = st.number_input(
        "📈 Load Scaling (p.u.)",
        min_value=1.00, max_value=2.00, value=1.00, step=0.01, format="%.2f",
        help="Ketik faktor pengali beban sistem eksisting Pulo Aceh (1.00 - 2.00)"
    )

    st.subheader("☀️ Pembangkit Listrik Tenaga Surya")
    w_plts = st.number_input(
        "Kapasitas PLTS (kW)",
        min_value=0.0, max_value=300.0, value=100.0, step=10.0, format="%.1f",
        help="Ketik kapasitas PLTS (maks. 300 kW)"
    )
    w_lok_plts = st.selectbox("📍 Lokasi Bus PLTS", options=VALID_BUS_LIST, index=0, help="Pilih nomor bus penempatan PLTS")

    st.subheader("🌬️ Pembangkit Listrik Tenaga Bayu")
    w_pltb = st.number_input(
        "Kapasitas PLTB (kW)",
        min_value=0.0, max_value=300.0, value=100.0, step=10.0, format="%.1f",
        help="Ketik kapasitas PLTB (maks. 300 kW)"
    )
    w_lok_pltb = st.selectbox("📍 Lokasi Bus PLTB", options=VALID_BUS_LIST, index=1, help="Pilih nomor bus penempatan PLTB")

    w_total_dg = w_plts + w_pltb
    base_actual_load = 91.42  # kW (Beban aktual eksisting Pulo Aceh)
    current_system_load = base_actual_load * w_load_scaling
    penetration_pct = (w_total_dg / current_system_load) * 100

    st.markdown("---")
    st.info(f"**Total Kapasitas DG:** {w_total_dg:.1f} kW\n\n**Penetrasi DG:** {penetration_pct:.1f}%")

# ============================================================
# MAIN CONTENT AREA
# ============================================================
st.markdown("""
<div class="dashboard-header">
    <div class="dashboard-eyebrow">Skripsi · Teknik Elektro USK</div>
    <div class="dashboard-title">⚡ Surrogate Model Kestabilan Tegangan — Pulo Aceh</div>
    <div class="dashboard-subtitle">Fast screening tool berbasis Random Forest Machine Learning untuk memprediksi Fast Voltage Stability Index (FVSI) pada jaringan distribusi terintegrasi PLTS & PLTB.</div>
</div>
""", unsafe_allow_html=True)

if model is None:
    st.error("⚠️ File model `model_stabilitas.pkl` tidak ditemukan atau gagal dimuat! Pastikan file model sudah di-upload ke repository GitHub.")
else:
    input_df = pd.DataFrame([[
        w_load_scaling,
        w_plts,
        w_pltb,
        w_total_dg,
        w_lok_plts,
        w_lok_pltb
    ]], columns=['Load Scaling', 'PLTS', 'PLTB', 'Total DG', 'Lokasi PLTS', 'Lokasi PLTB'])

    st.markdown("<br>", unsafe_allow_html=True)
    col_space1, col_btn, col_space2 = st.columns([1, 2, 1])
    with col_btn:
        predict_button = st.button("🔍 Jalankan Prediksi", type="primary", use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if predict_button:
        hasil_pred = model.predict(input_df)[0]

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

        col1, col2 = st.columns([1.5, 1])

        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">📊 Hasil Surrogate Model</div>', unsafe_allow_html=True)
            m_col1, m_col2 = st.columns(2)
            with m_col1:
                st.metric(label="Estimasi FVSI Max (Prediksi)", value=f"{hasil_pred:.6f}")
            with m_col2:
                st.markdown("<p style='color:#64748b; font-weight:600; font-size:0.85rem; margin-bottom:0.5rem;'>Status Kestabilan</p>", unsafe_allow_html=True)
                st.markdown(f"<span class='{badge_class}'>✓ {status_text}</span>", unsafe_allow_html=True)

            st.markdown(f"<p style='margin-top: 1.4rem; color: #475569; font-size: 0.92rem; line-height:1.6;'>{desc_text}</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">📋 Skenario & Penetrasi</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="scenario-row"><span class="scenario-label">Load Scaling</span><span class="scenario-value">{w_load_scaling:.2f}</span></div>
            <div class="scenario-row"><span class="scenario-label">Total Kapasitas DG</span><span class="scenario-value">{w_total_dg:.1f} kW</span></div>
            <div class="scenario-row"><span class="scenario-label">Penetrasi DG</span><span class="scenario-value">{penetration_pct:.1f}%</span></div>
            <div class="scenario-row"><span class="scenario-label">PLTS</span><span class="scenario-value">{w_plts:.0f} kW · Bus {w_lok_plts}</span></div>
            <div class="scenario-row"><span class="scenario-label">PLTB</span><span class="scenario-value">{w_pltb:.0f} kW · Bus {w_lok_pltb}</span></div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# RUANG LINGKUP & BATASAN PENELITIAN
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
