import streamlit as st
import pandas as pd
import joblib

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Voltage Stability Surrogate Model",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "page": "home",
    "active_input": None,
    "load_scaling": 1.00,
    "plts": 100.0,
    "pltb": 100.0,
    "bus_plts": 15,
    "bus_pltb": 20,
    "result": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():
    try:
        return joblib.load("model_stabilitas.pkl")
    except Exception:
        return None


model = load_model()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 85% 10%, rgba(29,78,216,0.08), transparent 28%),
        radial-gradient(circle at 10% 90%, rgba(14,165,233,0.06), transparent 25%),
        #f8fafc;
}

/* Remove sidebar */
section[data-testid="stSidebar"] {
    display: none;
}

/* Main container */
.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* ============================================================
   HOME
   ============================================================ */

.hero {
    background:
        linear-gradient(135deg, #0f172a 0%, #172554 55%, #1e3a8a 100%);
    border-radius: 28px;
    padding: 3.8rem 4rem;
    color: white;
    position: relative;
    overflow: hidden;
    margin-bottom: 1.5rem;
}

.hero:after {
    content: "";
    position: absolute;
    width: 350px;
    height: 350px;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,0.10);
    right: -100px;
    top: -130px;
}

.hero-small {
    font-size: 0.78rem;
    letter-spacing: 2px;
    font-weight: 600;
    color: #93c5fd;
    margin-bottom: 1rem;
}

.hero-title {
    font-size: 3rem;
    line-height: 1.08;
    font-weight: 800;
    letter-spacing: -1.5px;
    max-width: 700px;
}

.hero-title span {
    color: #60a5fa;
}

.hero-description {
    margin-top: 1rem;
    max-width: 650px;
    font-size: 0.98rem;
    line-height: 1.7;
    color: #cbd5e1;
}

.hero-note {
    margin-top: 1.8rem;
    font-size: 0.78rem;
    color: #94a3b8;
}

/* ============================================================
   FEATURE CARDS
   ============================================================ */

.feature-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 1.3rem;
    min-height: 125px;
    box-shadow: 0 4px 15px rgba(15,23,42,0.035);
}

.feature-icon {
    font-size: 1.4rem;
    margin-bottom: 0.7rem;
}

.feature-title {
    font-size: 0.88rem;
    font-weight: 700;
    color: #1e293b;
}

.feature-text {
    font-size: 0.74rem;
    color: #64748b;
    margin-top: 0.3rem;
}

/* ============================================================
   SECTION
   ============================================================ */

.section-title {
    font-size: 1.55rem;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.5px;
}

.section-subtitle {
    color: #64748b;
    font-size: 0.88rem;
    margin-top: 0.3rem;
    margin-bottom: 1.5rem;
}

/* ============================================================
   INPUT CARDS
   ============================================================ */

.input-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 1.5rem;
    min-height: 175px;
    box-shadow: 0 5px 18px rgba(15,23,42,0.04);
    transition: 0.2s;
}

.input-icon {
    width: 45px;
    height: 45px;
    border-radius: 13px;
    background: #eff6ff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    margin-bottom: 1rem;
}

.input-name {
    font-size: 0.78rem;
    color: #64748b;
    font-weight: 500;
}

.input-value {
    font-size: 1.35rem;
    font-weight: 800;
    color: #0f172a;
    margin-top: 0.2rem;
}

.input-unit {
    font-size: 0.75rem;
    color: #94a3b8;
}

.active-card {
    border: 1px solid #2563eb;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.08);
}

/* ============================================================
   RESULT
   ============================================================ */

.result-hero {
    background: linear-gradient(135deg, #0f172a, #172554);
    color: white;
    border-radius: 25px;
    padding: 3rem;
    text-align: center;
    margin-bottom: 1.3rem;
}

.result-label {
    color: #93c5fd;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 1.5px;
}

.result-value {
    font-size: 4rem;
    font-weight: 800;
    letter-spacing: -2px;
    margin: 0.4rem 0;
}

.result-caption {
    color: #94a3b8;
    font-size: 0.78rem;
}

.result-stable {
    display: inline-block;
    margin-top: 1rem;
    padding: 0.55rem 1.1rem;
    border-radius: 100px;
    background: rgba(34,197,94,0.12);
    border: 1px solid rgba(74,222,128,0.25);
    color: #86efac;
    font-size: 0.82rem;
    font-weight: 700;
}

.result-warning {
    display: inline-block;
    margin-top: 1rem;
    padding: 0.55rem 1.1rem;
    border-radius: 100px;
    background: rgba(245,158,11,0.12);
    border: 1px solid rgba(251,191,36,0.25);
    color: #fcd34d;
    font-size: 0.82rem;
    font-weight: 700;
}

.result-critical {
    display: inline-block;
    margin-top: 1rem;
    padding: 0.55rem 1.1rem;
    border-radius: 100px;
    background: rgba(239,68,68,0.12);
    border: 1px solid rgba(248,113,113,0.25);
    color: #fca5a5;
    font-size: 0.82rem;
    font-weight: 700;
}

/* ============================================================
   INFO CARDS
   ============================================================ */

.info-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 1.4rem;
    box-shadow: 0 4px 15px rgba(15,23,42,0.03);
}

.info-label {
    color: #64748b;
    font-size: 0.75rem;
}

.info-value {
    color: #0f172a;
    font-size: 1.15rem;
    font-weight: 700;
    margin-top: 0.2rem;
}

/* ============================================================
   BUTTON
   ============================================================ */

.stButton > button {
    border-radius: 11px;
    height: 2.8rem;
    font-weight: 600;
    border: 1px solid #d0d5dd;
    background: white;
    color: #344054;
}

.stButton > button:hover {
    border-color: #2563eb;
    color: #2563eb;
}

.primary-btn .stButton > button {
    background: #2563eb;
    border: none;
    color: white;
}

/* Footer */

.footer {
    text-align: center;
    margin-top: 3rem;
    color: #94a3b8;
    font-size: 0.72rem;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HOME PAGE
# ============================================================

if st.session_state.page == "home":

    st.markdown("""
    <div class="hero">

        <div class="hero-small">
            POWER SYSTEM • MACHINE LEARNING • SCREENING TOOL
        </div>

        <div class="hero-title">
            Voltage Stability<br>
            <span>Surrogate Model</span>
        </div>

        <div class="hero-description">
            Estimasi cepat kondisi kestabilan tegangan sistem distribusi
            berdasarkan parameter operasi dan integrasi Distributed Generation
            menggunakan machine learning.
        </div>

        <div class="hero-note">
            IEEE 33-Bus Distribution System · FVSI Maximum Prediction
        </div>

    </div>
    """, unsafe_allow_html=True)

    # Feature cards
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Voltage Stability</div>
            <div class="feature-text">
                Evaluasi kondisi kestabilan tegangan berdasarkan FVSI Maximum.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">◈</div>
            <div class="feature-title">Machine Learning</div>
            <div class="feature-text">
                Surrogate model memberikan estimasi cepat dari skenario input.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">◉</div>
            <div class="feature-title">Fast Screening</div>
            <div class="feature-text">
                Digunakan sebagai screening awal sebelum analisis sistem tenaga.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="primary-btn">', unsafe_allow_html=True)

    if st.button("Mulai Analisis  →", use_container_width=True):
        st.session_state.page = "input"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
        Surrogate Model Kestabilan Tegangan · Machine Learning Based Screening Tool
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# INPUT PAGE
# ============================================================

elif st.session_state.page == "input":

    st.markdown(
        '<div class="section-title">Input Skenario</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Klik parameter yang ingin diubah. Nilai input akan muncul setelah kartu dipilih.'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # CARD 1
    # --------------------------------------------------------

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(f"""
        <div class="input-card">
            <div class="input-icon">⚡</div>
            <div class="input-name">LOAD SCALING</div>
            <div class="input-value">
                {st.session_state.load_scaling:.2f}
            </div>
            <div class="input-unit">Per-unit load multiplier</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Ubah Load Scaling", key="load_btn", use_container_width=True):
            st.session_state.active_input = "load"
            st.rerun()

    # --------------------------------------------------------
    # CARD 2
    # --------------------------------------------------------

    with c2:

        st.markdown(f"""
        <div class="input-card">
            <div class="input-icon">☀</div>
            <div class="input-name">KAPASITAS PLTS</div>
            <div class="input-value">
                {st.session_state.plts:.0f}
            </div>
            <div class="input-unit">kW</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Ubah Kapasitas PLTS", key="plts_btn", use_container_width=True):
            st.session_state.active_input = "plts"
            st.rerun()

    # --------------------------------------------------------
    # CARD 3
    # --------------------------------------------------------

    with c3:

        st.markdown(f"""
        <div class="input-card">
            <div class="input-icon">◒</div>
            <div class="input-name">KAPASITAS PLTB</div>
            <div class="input-value">
                {st.session_state.pltb:.0f}
            </div>
            <div class="input-unit">kW</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Ubah Kapasitas PLTB", key="pltb_btn", use_container_width=True):
            st.session_state.active_input = "pltb"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # CARD 4
    # --------------------------------------------------------

    c4, c5, c6 = st.columns(3)

    with c4:

        st.markdown(f"""
        <div class="input-card">
            <div class="input-icon">◉</div>
            <div class="input-name">LOKASI BUS PLTS</div>
            <div class="input-value">
                {st.session_state.bus_plts}
            </div>
            <div class="input-unit">Bus IEEE 33</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Ubah Bus PLTS", key="bus_plts_btn", use_container_width=True):
            st.session_state.active_input = "bus_plts"
            st.rerun()

    with c5:

        st.markdown(f"""
        <div class="input-card">
            <div class="input-icon">◉</div>
            <div class="input-name">LOKASI BUS PLTB</div>
            <div class="input-value">
                {st.session_state.bus_pltb}
            </div>
            <div class="input-unit">Bus IEEE 33</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Ubah Bus PLTB", key="bus_pltb_btn", use_container_width=True):
            st.session_state.active_input = "bus_pltb"
            st.rerun()

    with c6:

        total_dg = st.session_state.plts + st.session_state.pltb

        st.markdown(f"""
        <div class="input-card">
            <div class="input-icon">Σ</div>
            <div class="input-name">TOTAL DISTRIBUTED GENERATION</div>
            <div class="input-value">
                {total_dg:.0f}
            </div>
            <div class="input-unit">kW · automatically calculated</div>
        </div>
        """, unsafe_allow_html=True)

    # ========================================================
    # ACTIVE INPUT
    # ========================================================

    if st.session_state.active_input is not None:

        st.markdown("<br>", unsafe_allow_html=True)

        active = st.session_state.active_input

        if active == "load":

            st.info("Masukkan nilai Load Scaling")

            new_value = st.number_input(
                "Load Scaling",
                min_value=0.10,
                max_value=2.00,
                value=float(st.session_state.load_scaling),
                step=0.01,
                format="%.2f",
                key="input_load"
            )

            if st.button("Simpan Load Scaling", use_container_width=True):
                st.session_state.load_scaling = new_value
                st.session_state.active_input = None
                st.rerun()

        elif active == "plts":

            st.info("Masukkan kapasitas PLTS")

            new_value = st.number_input(
                "Kapasitas PLTS (kW)",
                min_value=0.0,
                max_value=1000.0,
                value=float(st.session_state.plts),
                step=10.0,
                key="input_plts"
            )

            if st.button("Simpan Kapasitas PLTS", use_container_width=True):
                st.session_state.plts = new_value
                st.session_state.active_input = None
                st.rerun()

        elif active == "pltb":

            st.info("Masukkan kapasitas PLTB")

            new_value = st.number_input(
                "Kapasitas PLTB (kW)",
                min_value=0.0,
                max_value=1000.0,
                value=float(st.session_state.pltb),
                step=10.0,
                key="input_pltb"
            )

            if st.button("Simpan Kapasitas PLTB", use_container_width=True):
                st.session_state.pltb = new_value
                st.session_state.active_input = None
                st.rerun()

        elif active == "bus_plts":

            st.info("Masukkan nomor bus tempat PLTS terhubung")

            new_value = st.number_input(
                "Bus PLTS",
                min_value=1,
                max_value=33,
                value=int(st.session_state.bus_plts),
                step=1,
                key="input_bus_plts"
            )

            if st.button("Simpan Bus PLTS", use_container_width=True):
                st.session_state.bus_plts = new_value
                st.session_state.active_input = None
                st.rerun()

        elif active == "bus_pltb":

            st.info("Masukkan nomor bus tempat PLTB terhubung")

            new_value = st.number_input(
                "Bus PLTB",
                min_value=1,
                max_value=33,
                value=int(st.session_state.bus_pltb),
                step=1,
                key="input_bus_pltb"
            )

            if st.button("Simpan Bus PLTB", use_container_width=True):
                st.session_state.bus_pltb = new_value
                st.session_state.active_input = None
                st.rerun()

    # ========================================================
    # ANALYSIS BUTTON
    # ========================================================

    st.markdown("<br>", unsafe_allow_html=True)

    total_dg = st.session_state.plts + st.session_state.pltb

    st.markdown(
        f"""
        <div class="info-card">
            <div class="info-label">SCENARIO SUMMARY</div>
            <div class="info-value">
                Load {st.session_state.load_scaling:.2f}
                &nbsp; · &nbsp;
                DG {total_dg:.0f} kW
                &nbsp; · &nbsp;
                PLTS Bus {st.session_state.bus_plts}
                &nbsp; · &nbsp;
                PLTB Bus {st.session_state.bus_pltb}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="primary-btn">', unsafe_allow_html=True)

    if st.button(
        "Jalankan Analisis Prediksi  →",
        use_container_width=True
    ):

        if model is None:
            st.error(
                "Model 'model_stabilitas.pkl' tidak ditemukan."
            )

        else:

            input_df = pd.DataFrame(
                [[
                    st.session_state.load_scaling,
                    st.session_state.plts,
                    st.session_state.pltb,
                    total_dg,
                    st.session_state.bus_plts,
                    st.session_state.bus_pltb
                ]],
                columns=[
                    "Load Scaling",
                    "PLTS",
                    "PLTB",
                    "Total DG",
                    "Lokasi PLTS",
                    "Lokasi PLTB"
                ]
            )

            hasil_pred = model.predict(input_df)[0]

            if hasil_pred < 0.90:
                status = "AMAN (STABIL)"
                status_class = "result-stable"

            elif hasil_pred < 1.00:
                status = "WARNING (WASPADA)"
                status_class = "result-warning"

            else:
                status = "KRITIS (TIDAK STABIL)"
                status_class = "result-critical"

            st.session_state.result = {
                "fvsi": hasil_pred,
                "status": status,
                "status_class": status_class
            }

            st.session_state.page = "result"

            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("← Kembali ke Beranda"):
        st.session_state.page = "home"
        st.rerun()


# ============================================================
# RESULT PAGE
# ============================================================

elif st.session_state.page == "result":

    result = st.session_state.result

    st.markdown(
        '<div class="section-title">Analysis Result</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Estimasi kondisi kestabilan sistem berdasarkan skenario yang telah dipilih.'
        '</div>',
        unsafe_allow_html=True
    )

    # ========================================================
    # MAIN RESULT
    # ========================================================

    st.markdown(
        f"""
        <div class="result-hero">

            <div class="result-label">
                ESTIMATED FVSI MAX
            </div>

            <div class="result-value">
                {result["fvsi"]:.6f}
            </div>

            <div class="result-caption">
                Fast screening prediction
            </div>

            <div class="{result["status_class"]}">
                ✓ &nbsp; {result["status"]}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # SCENARIO RESULT
    # ========================================================

    total_dg = st.session_state.plts + st.session_state.pltb

    c1, c2, c3, c4 = st.columns(4)

    data = [
        ("Load Scaling", f'{st.session_state.load_scaling:.2f}'),
        ("Total DG", f'{total_dg:.0f} kW'),
        ("PLTS", f'{st.session_state.plts:.0f} kW'),
        ("PLTB", f'{st.session_state.pltb:.0f} kW')
    ]

    for col, (label, value) in zip(
        [c1, c2, c3, c4],
        data
    ):

        with col:

            st.markdown(
                f"""
                <div class="info-card">

                    <div class="info-label">
                        {label.upper()}
                    </div>

                    <div class="info-value">
                        {value}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            f"""
            <div class="info-card">

                <div class="info-label">
                    LOKASI DISTRIBUTED GENERATION
                </div>

                <br>

                <div class="info-value">
                    PLTS → Bus {st.session_state.bus_plts}
                </div>

                <div class="info-value">
                    PLTB → Bus {st.session_state.bus_pltb}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            f"""
            <div class="info-card">

                <div class="info-label">
                    MODEL OUTPUT
                </div>

                <br>

                <div class="info-value">
                    FVSI Maximum
                </div>

                <div style="
                    color:#2563eb;
                    font-size:1.25rem;
                    font-weight:800;
                    margin-top:0.3rem;
                ">
                    {result["fvsi"]:.6f}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    # ========================================================
    # INTERPRETATION
    # ========================================================

    st.markdown("<br>", unsafe_allow_html=True)

    if result["fvsi"] < 0.90:

        st.success(
            f"Sistem diprediksi **STABIL** dengan FVSI Maximum "
            f"sebesar **{result['fvsi']:.6f}**."
        )

    elif result["fvsi"] < 1.00:

        st.warning(
            f"Sistem berada pada kondisi **WASPADA** dengan FVSI Maximum "
            f"sebesar **{result['fvsi']:.6f}**."
        )

    else:

        st.error(
            f"Sistem berada pada kondisi **KRITIS** dengan FVSI Maximum "
            f"sebesar **{result['fvsi']:.6f}**."
        )

    # ========================================================
    # DISCLAIMER
    # ========================================================

    st.markdown("""
    <div class="info-card">

        <div class="info-label">
            MODEL APPLICATION
        </div>

        <br>

        <div style="
            color:#475467;
            font-size:0.82rem;
            line-height:1.7;
        ">

        Surrogate model digunakan sebagai <b>fast screening tool</b>
        untuk mengestimasi kondisi kestabilan tegangan berdasarkan
        pola data hasil simulasi yang digunakan dalam pembentukan
        model machine learning.

        Model ini tidak dimaksudkan untuk menggantikan simulasi
        <b>DIgSILENT PowerFactory</b>. Simulasi sistem tenaga tetap
        digunakan sebagai acuan analisis yang lebih rinci.

        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "← Ubah Skenario",
            use_container_width=True
        ):
            st.session_state.page = "input"
            st.session_state.result = None
            st.rerun()

    with c2:

        if st.button(
            "⌂ Kembali ke Beranda",
            use_container_width=True
        ):
            st.session_state.page = "home"
            st.session_state.result = None
            st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    Voltage Stability Surrogate Model · IEEE 33-Bus Distribution System
</div>
""", unsafe_allow_html=True)
