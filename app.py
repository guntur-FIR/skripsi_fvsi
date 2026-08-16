import streamlit as st
import pandas as pd
import joblib

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================

st.set_page_config(
    page_title="Surrogate Model | Stabilitas Tegangan",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #f6f8fb;
}

/* Hilangkan sidebar */
section[data-testid="stSidebar"] {
    display: none;
}

/* Container utama */
.block-container {
    max-width: 1180px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

/* Header */
.main-header {
    text-align: center;
    margin-bottom: 2.2rem;
}

.main-title {
    font-size: 2.35rem;
    font-weight: 700;
    color: #172033;
    letter-spacing: -0.8px;
    margin-bottom: 0.4rem;
}

.main-subtitle {
    font-size: 0.98rem;
    color: #667085;
    font-weight: 400;
}

/* Section title */
.section-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #172033;
    margin-top: 1.2rem;
    margin-bottom: 0.3rem;
}

.section-description {
    color: #667085;
    font-size: 0.88rem;
    margin-bottom: 1.2rem;
}

/* Card */
.input-card {
    background: white;
    border: 1px solid #e4e7ec;
    border-radius: 16px;
    padding: 1.4rem 1.5rem 1.1rem 1.5rem;
    box-shadow: 0 2px 8px rgba(16, 24, 40, 0.04);
}

/* Input label */
label {
    font-weight: 500 !important;
    color: #344054 !important;
}

/* Button */
.stButton > button {
    width: 100%;
    height: 3rem;
    border-radius: 10px;
    border: none;
    background: #1d4ed8;
    color: white;
    font-size: 0.95rem;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: #1e40af;
    color: white;
    transform: translateY(-1px);
}

/* KPI cards */
.kpi-card {
    background: white;
    border: 1px solid #e4e7ec;
    border-radius: 16px;
    padding: 1.35rem 1.5rem;
    min-height: 135px;
    box-shadow: 0 2px 8px rgba(16, 24, 40, 0.04);
}

.kpi-label {
    color: #667085;
    font-size: 0.82rem;
    font-weight: 500;
    margin-bottom: 0.55rem;
}

.kpi-value {
    color: #172033;
    font-size: 1.65rem;
    font-weight: 700;
    letter-spacing: -0.5px;
}

.kpi-small {
    color: #667085;
    font-size: 0.78rem;
    margin-top: 0.35rem;
}

/* Status cards */
.status-stable {
    background: #ecfdf3;
    border: 1px solid #abefc6;
    color: #067647;
}

.status-warning {
    background: #fffaeb;
    border: 1px solid #fedf89;
    color: #b54708;
}

.status-critical {
    background: #fef3f2;
    border: 1px solid #fecdca;
    color: #b42318;
}

.status-card {
    border-radius: 16px;
    padding: 1.35rem 1.5rem;
    min-height: 135px;
}

.status-label {
    font-size: 0.82rem;
    font-weight: 500;
    margin-bottom: 0.55rem;
}

.status-value {
    font-size: 1.45rem;
    font-weight: 700;
}

/* Info box */
.info-box {
    background: #f8fafc;
    border: 1px solid #e4e7ec;
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    color: #475467;
    font-size: 0.82rem;
    line-height: 1.6;
}

/* Footer */
.footer {
    text-align: center;
    color: #98a2b3;
    font-size: 0.75rem;
    margin-top: 2.5rem;
    padding-top: 1rem;
    border-top: 1px solid #eaecf0;
}

</style>
""", unsafe_allow_html=True)


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
# HEADER
# ============================================================

st.markdown("""
<div class="main-header">

    <div class="main-title">
        ⚡ Surrogate Model Kestabilan Tegangan
    </div>

    <div class="main-subtitle">
        Sistem Pendukung Keputusan Berbasis Machine Learning
        untuk Estimasi FVSI Maximum pada Sistem Distribusi
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# MODEL ERROR
# ============================================================

if model is None:

    st.error(
        "File model 'model_stabilitas.pkl' tidak dapat dimuat. "
        "Pastikan file model berada pada repository yang sama dengan aplikasi."
    )

else:

    # ========================================================
    # INPUT SCENARIO
    # ========================================================

    st.markdown(
        '<div class="section-title">Input Skenario Sistem</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Masukkan parameter operasi dan penetrasi Distributed Generation '
        'untuk melakukan estimasi kondisi kestabilan tegangan.'
        '</div>',
        unsafe_allow_html=True
    )

    with st.form("scenario_form"):

        st.markdown('<div class="input-card">', unsafe_allow_html=True)

        # Baris pertama
        col1, col2, col3 = st.columns(3)

        with col1:
            w_load_scaling = st.number_input(
                "Load Scaling",
                min_value=0.10,
                max_value=2.00,
                value=1.00,
                step=0.01,
                format="%.2f",
                help="Faktor pengali beban sistem."
            )

        with col2:
            w_plts = st.number_input(
                "Kapasitas PLTS (kW)",
                min_value=0.0,
                max_value=1000.0,
                value=100.0,
                step=10.0,
                format="%.1f",
                help="Kapasitas pembangkit PLTS."
            )

        with col3:
            w_pltb = st.number_input(
                "Kapasitas PLTB (kW)",
                min_value=0.0,
                max_value=1000.0,
                value=100.0,
                step=10.0,
                format="%.1f",
                help="Kapasitas pembangkit PLTB."
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Baris kedua
        col4, col5, col6 = st.columns(3)

        with col4:
            w_lok_plts = st.number_input(
                "Lokasi Bus PLTS",
                min_value=1,
                max_value=33,
                value=15,
                step=1,
                help="Nomor bus tempat PLTS terhubung."
            )

        with col5:
            w_lok_pltb = st.number_input(
                "Lokasi Bus PLTB",
                min_value=1,
                max_value=33,
                value=20,
                step=1,
                help="Nomor bus tempat PLTB terhubung."
            )

        with col6:

            w_total_dg = w_plts + w_pltb

            st.markdown(
                f"""
                <div style="
                    margin-top: 1.8rem;
                    padding: 0.72rem 1rem;
                    border-radius: 10px;
                    background: #f2f4f7;
                    border: 1px solid #eaecf0;
                ">
                    <div style="
                        font-size: 0.78rem;
                        color: #667085;
                        margin-bottom: 0.15rem;
                    ">
                        Total Distributed Generation
                    </div>

                    <div style="
                        font-size: 1.15rem;
                        font-weight: 700;
                        color: #172033;
                    ">
                        {w_total_dg:,.1f} kW
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        submitted = st.form_submit_button(
            "🚀  Jalankan Analisis Prediksi"
        )

        st.markdown('</div>', unsafe_allow_html=True)


    # ========================================================
    # PREDICTION
    # ========================================================

    if submitted:

        # Membuat dataframe sesuai urutan feature model
        input_df = pd.DataFrame(
            [[
                w_load_scaling,
                w_plts,
                w_pltb,
                w_total_dg,
                w_lok_plts,
                w_lok_pltb
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

        # Prediksi
        try:

            hasil_pred = model.predict(input_df)[0]

            # ====================================================
            # STATUS
            # ====================================================

            if hasil_pred < 0.90:

                status = "AMAN (STABIL)"
                status_class = "status-stable"
                status_description = "Kondisi sistem berada pada kategori stabil."

            elif hasil_pred < 1.00:

                status = "WARNING (WASPADA)"
                status_class = "status-warning"
                status_description = "Kondisi sistem perlu mendapatkan perhatian."

            else:

                status = "KRITIS (TIDAK STABIL)"
                status_class = "status-critical"
                status_description = "Kondisi sistem berada pada kategori kritis."

            # ====================================================
            # RESULT HEADER
            # ====================================================

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(
                '<div class="section-title">Hasil Prediksi Sistem</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="section-description">'
                'Hasil estimasi surrogate model berdasarkan skenario input yang diberikan.'
                '</div>',
                unsafe_allow_html=True
            )

            # ====================================================
            # KPI
            # ====================================================

            col1, col2, col3 = st.columns(3)

            with col1:

                st.markdown(
                    f"""
                    <div class="kpi-card">

                        <div class="kpi-label">
                            ESTIMASI FVSI MAX
                        </div>

                        <div class="kpi-value">
                            {hasil_pred:.6f}
                        </div>

                        <div class="kpi-small">
                            Predicted output
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:

                st.markdown(
                    f"""
                    <div class="status-card {status_class}">

                        <div class="status-label">
                            STATUS SISTEM
                        </div>

                        <div class="status-value">
                            {status}
                        </div>

                        <div style="
                            font-size: 0.78rem;
                            margin-top: 0.35rem;
                        ">
                            {status_description}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col3:

                st.markdown(
                    f"""
                    <div class="kpi-card">

                        <div class="kpi-label">
                            TOTAL DISTRIBUTED GENERATION
                        </div>

                        <div class="kpi-value">
                            {w_total_dg:,.1f} kW
                        </div>

                        <div class="kpi-small">
                            PLTS {w_plts:,.1f} kW + PLTB {w_pltb:,.1f} kW
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # ====================================================
            # SCENARIO SUMMARY
            # ====================================================

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(
                '<div class="section-title">Ringkasan Skenario</div>',
                unsafe_allow_html=True
            )

            summary_col1, summary_col2 = st.columns(2)

            with summary_col1:

                st.markdown(
                    f"""
                    <div class="info-box">

                    <b>Parameter Sistem</b><br><br>

                    Load Scaling :
                    <b>{w_load_scaling:.2f}</b><br>

                    Total DG :
                    <b>{w_total_dg:,.1f} kW</b><br>

                    Kapasitas PLTS :
                    <b>{w_plts:,.1f} kW</b><br>

                    Kapasitas PLTB :
                    <b>{w_pltb:,.1f} kW</b>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with summary_col2:

                st.markdown(
                    f"""
                    <div class="info-box">

                    <b>Lokasi Distributed Generation</b><br><br>

                    Bus PLTS :
                    <b>{w_lok_plts}</b><br>

                    Bus PLTB :
                    <b>{w_lok_pltb}</b><br><br>

                    <b>Output Model</b><br>

                    FVSI Maximum :
                    <b>{hasil_pred:.6f}</b>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # ====================================================
            # INTERPRETATION
            # ====================================================

            st.markdown("<br>", unsafe_allow_html=True)

            if hasil_pred < 0.90:

                st.success(
                    f"✓ Sistem diprediksi **STABIL** dengan nilai FVSI Max "
                    f"sebesar **{hasil_pred:.6f}**."
                )

            elif hasil_pred < 1.00:

                st.warning(
                    f"⚠ Sistem berada pada kondisi **WASPADA** dengan nilai "
                    f"FVSI Max sebesar **{hasil_pred:.6f}**."
                )

            else:

                st.error(
                    f"✕ Sistem berada pada kondisi **KRITIS** dengan nilai "
                    f"FVSI Max sebesar **{hasil_pred:.6f}**."
                )


            # ====================================================
            # DISCLAIMER
            # ====================================================

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(
                """
                <div class="info-box">

                <b>Catatan penggunaan model</b><br>

                Surrogate model digunakan sebagai <b>screening tool</b>
                untuk memberikan estimasi cepat kondisi kestabilan tegangan
                berdasarkan pola data simulasi yang telah digunakan dalam
                pembentukan model machine learning.

                Hasil prediksi tidak dimaksudkan untuk menggantikan
                simulasi sistem tenaga menggunakan <b>DIgSILENT PowerFactory</b>.
                Analisis lebih lanjut dapat dilakukan melalui simulasi
                untuk memperoleh hasil yang lebih rinci.

                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception as e:

            st.error(
                "Terjadi kesalahan saat melakukan prediksi. "
                "Pastikan urutan dan nama fitur input sesuai dengan model."
            )

            st.code(str(e))


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Surrogate Model Kestabilan Tegangan · Machine Learning Based Screening Tool
    </div>
    """,
    unsafe_allow_html=True
)
