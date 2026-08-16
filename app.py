import streamlit as st
import pandas as pd
import joblib

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="SURROGATE MODEL | Pulo Aceh",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# ENGINEERING-STYLE CSS (dark, electric blue & amber accents)
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp { background: #eef1f5; }

    /* ---------- Header: circuit-board style ---------- */
    .dashboard-header {
        position: relative;
        overflow: hidden;
        background:
            linear-gradient(120deg, #0a0f1c 0%, #0f1b2e 55%, #0d2438 100%);
        background-image:
            linear-gradient(120deg, #0a0f1c 0%, #0f1b2e 55%, #0d2438 100%),
            repeating-linear-gradient(0deg, rgba(56,189,248,0.06) 0px, rgba(56,189,248,0.06) 1px, transparent 1px, transparent 26px),
            repeating-linear-gradient(90deg, rgba(56,189,248,0.06) 0px, rgba(56,189,248,0.06) 1px, transparent 1px, transparent 26px);
        padding: 2.4rem 2rem;
        border-radius: 14px;
        border: 1px solid #1e3a52;
        color: #f1f5f9;
        margin-bottom: 1.6rem;
        text-align: center;
    }
    .dashboard-eyebrow {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #38bdf8;
        border: 1px solid rgba(56,189,248,0.4);
        padding: 0.3rem 0.9rem;
        border-radius: 4px;
        margin-bottom: 1rem;
        background: rgba(56,189,248,0.08);
    }
    .dashboard-title {
        font-size: 1.9rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 0.6rem;
        color: #ffffff;
    }
    .dashboard-subtitle {
        font-size: 0.92rem;
        color: #94a3b8;
        line-height: 1.6;
        max-width: 640px;
        margin: 0 auto;
    }

    /* ---------- Status text (plain sentence, no box) ---------- */
    .status-safe    { color: #16a34a; font-weight: 800; }
    .status-warning { color: #d97706; font-weight: 800; }
    .status-critical{ color: #dc2626; font-weight: 800; }
    .status-sentence {
        font-size: 0.98rem;
        color: #1e293b;
        line-height: 1.7;
        margin-top: 0.6rem;
    }

    /* ---------- Cards ---------- */
    .panel-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 1.5rem 1.6rem;
        border: 1px solid #dbe2ea;
        border-left: 4px solid #0ea5e9;
        box-shadow: 0 6px 16px -8px rgba(15, 23, 42, 0.12);
        height: 100%;
    }
    .card-title {
        font-size: 1rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 1rem;
        letter-spacing: -0.2px;
    }
    .scenario-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.55rem 0;
        border-bottom: 1px solid #eef1f5;
        font-size: 0.88rem;
    }
    .scenario-row:last-child { border-bottom: none; }
    .scenario-label { color: #64748b; font-weight: 500; }
    .scenario-value {
        color: #0f172a;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
    }

    /* ---------- Metrics ---------- */
    div[data-testid="stMetric"] {
        background: #f8fafc;
        border: 1px solid #dbe2ea;
        border-left: 4px solid #f59e0b;
        border-radius: 10px;
        padding: 1rem 1.2rem;
    }
    div[data-testid="stMetricLabel"] { font-weight: 600; color: #64748b; }
    div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace;
        color: #0f172a;
    }

    /* ---------- Sidebar (targeted colors, not wildcard) ---------- */
    section[data-testid="stSidebar"] {
        background: #0a0f1c;
        border-right: 1px solid #1e293b;
    }
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #ffffff !important;
        font-weight: 800;
    }
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stSubheader,
    section[data-testid="stSidebar"] h2 {
        color: #cbd5e1 !important;
    }
    section[data-testid="stSidebar"] .stNumberInput input,
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #101c33 !important;
        color: #f1f5f9 !important;
        border-radius: 8px !important;
        border: 1px solid #24405c !important;
    }
    section[data-testid="stSidebar"] hr { border-color: #1e293b; }

    /* Info box (fixed contrast, explicit colors so it's never invisible) */
    section[data-testid="stSidebar"] .stAlert {
        background: #0f2237 !important;
        border: 1px solid #1e4a6b !important;
        border-radius: 10px;
    }
    section[data-testid="stSidebar"] .stAlert p,
    section[data-testid="stSidebar"] .stAlert div,
    section[data-testid="stSidebar"] .stAlert span {
        color: #7dd3fc !important;
    }

    /* ---------- Buttons ---------- */
    div.stButton > button {
        background: #0ea5e9;
        color: #ffffff;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        letter-spacing: 0.3px;
        transition: background 0.15s ease;
    }
    div.stButton > button:hover {
        background: #0284c7;
        color: #ffffff;
    }

    /* ---------- Expander (explicit colors for mobile readability) ---------- */
    .streamlit-expanderHeader, details summary {
        font-weight: 700 !important;
        color: #0f172a !important;
        background-color: #f8fafc !important;
        border-radius: 8px !important;
    }
    details, .streamlit-expanderContent {
        color: #1e293b !important;
    }
    details p, details li {
        color: #1e293b !important;
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

VALID_BUS_LIST = [17, 18, 19, 20, 21, 22]

# ============================================================
# SIDEBAR - PARAMETER SKENARIO PULO ACEH
# ============================================================
with st.sidebar:
    st.markdown("### 🔌 Pulo Aceh Grid")
    st.markdown(
        "<p style='color:#94a3b8; font-size:0.85rem; line-height:1.5;'>"
        "Surrogate model screening skenario PLTS dan PLTB </p>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    st.subheader("⚙️ Parameter Operasi")
    w_load_scaling = st.number_input(
        "📶 Load Scaling",
        min_value=1.00, max_value=2.00, value=1.00, step=0.01, format="%.2f",
        help="Ketik faktor pengali beban sistem eksisting Pulo Aceh (1.00 - 2.00)"
    )

    st.subheader("🔆 Pembangkit Listrik Tenaga Surya")
    w_plts = st.number_input(
        "Kapasitas PLTS (kW)",
        min_value=0.0, max_value=300.0, value=100.0, step=10.0, format="%.1f",
        help="Ketik kapasitas PLTS (maks. 300 kW)"
    )
    w_lok_plts = st.selectbox("📡 Lokasi Bus PLTS", options=VALID_BUS_LIST, index=0, help="Pilih nomor bus penempatan PLTS")

    st.subheader("🌀 Pembangkit Listrik Tenaga Bayu")
    w_pltb = st.number_input(
        "Kapasitas PLTB (kW)",
        min_value=0.0, max_value=300.0, value=100.0, step=10.0, format="%.1f",
        help="Ketik kapasitas PLTB (maks. 300 kW)"
    )
    w_lok_pltb = st.selectbox("📡 Lokasi Bus PLTB", options=VALID_BUS_LIST, index=1, help="Pilih nomor bus penempatan PLTB")

    w_total_dg = w_plts + w_pltb
    base_actual_load = 91.42 
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
    <div class="dashboard-title">⚡ SURROGATE MODEL — PULO ACEH ⚡ </div>
    <div class="dashboard-subtitle">Fast screening tool untuk memprediksi Fast Voltage Stability Index (FVSI) pada jaringan distribusi skenario PLTS dan PLTB.</div>
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
        predict_button = st.button("Jalankan Prediksi", type="primary", use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if predict_button:
        hasil_pred = model.predict(input_df)[0]

        if hasil_pred < 0.90:
            status_class = "status-safe"
            status_text = "Aman / Stabil"
            desc_text = "Sistem distribusi Pulo Aceh diprediksi berada dalam kondisi operasi normal dan stabil pada skenario ini."
        elif hasil_pred < 1.00:
            status_class = "status-warning"
            status_text = "Waspada / Mendekati Batas"
            desc_text = "Sistem Pulo Aceh mendekati batas kriteria kestabilan pada skenario ini, disarankan verifikasi ulang melalui simulasi DIgSILENT PowerFactory."
        else:
            status_class = "status-critical"
            status_text = "Kritis / Tidak Stabil"
            desc_text = "Indikator FVSI pada skenario ini melebihi batas 1.00 sehingga sistem berpotensi mengalami gangguan kestabilan atau voltage collapse, wajib diverifikasi ulang."

        col1, col2 = st.columns([1.5, 1])

        with col1:
            st.markdown('<div class="panel-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">📊 Hasil Surrogate Model</div>', unsafe_allow_html=True)
            st.metric(label="Estimasi FVSI Max (Prediksi)", value=f"{hasil_pred:.6f}")
            st.markdown(
                f"<p class='status-sentence'>Status kestabilan: <span class='{status_class}'>{status_text}</span>. {desc_text}</p>",
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="panel-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">📋 Skenario Operasi</div>', unsafe_allow_html=True)
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
      * $\\text{FVSI} < 0.90$ → **Aman / Stabil**
      * $0.90 \\le \\text{FVSI} < 1.00$ → **Waspada / Mendekati Batas**
      * $\\text{FVSI} \\ge 1.00$ → **Kritis / Tidak Stabil (Risiko *Voltage Collapse*)**
    * **Catatan Penting:** Model ini merupakan *screening* awal (*surrogate model* berbasis *Random Forest*) dan **bukan pengganti penuh DIgSILENT PowerFactory**. Kondisi mendekati kritis wajib diverifikasi ulang.
    """)

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #64748b; font-size: 0.8rem;'>Skripsi Program Studi Teknik Elektro Universitas Syiah Kuala · Pengembangan Surrogate Model Berbasis Random Forest untuk Prediksi Stabilitas Tegangan pada Sistem Distribusi Berbasis PLTD dengan Skenario Integrasi PLTS dan PLTB di Pulo Aceh</p>",
    unsafe_allow_html=True
)
