import streamlit as st
import pickle
import pandas as pd

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(page_title="Justin Corp — Analisis Kredit", page_icon="🏢", layout="centered")

# ==========================================
# 1. FITUR TOMBOL & CSS CUSTOM MODE
# ==========================================
header_container = st.container()
with header_container:
    col_t, col_m = st.columns([7, 3])
    with col_m:
        mode_gelap = st.toggle("🌙 Mode Gelap", value=True)

if mode_gelap:
    bg_app        = "#0B0F1A"
    bg_surface    = "#141824"
    bg_card       = "#1A1F2E"
    bg_input      = "#1F2535"
    border_color  = "#2E3650"
    border_focus  = "#4A7AFF"
    text_primary  = "#E8EDF8"
    text_secondary= "#8A95B0"
    text_muted    = "#5A647A"
    accent_main   = "#4A7AFF"
    accent_dark   = "#2D5FE8"
    accent_light  = "#6B95FF"
    header_bg     = "#0D1929"
    divider       = "#252B3B"
    badge_bg      = "#1E2D50"
    badge_text    = "#6B95FF"
else:
    bg_app        = "#F2F5FC"
    bg_surface    = "#FFFFFF"
    bg_card       = "#FFFFFF"
    bg_input      = "#F8FAFF"
    border_color  = "#D1DCEF"
    border_focus  = "#1A5CDB"
    text_primary  = "#0D1A3A"
    text_secondary= "#4A5C80"
    text_muted    = "#8A9AB8"
    accent_main   = "#1A5CDB"
    accent_dark   = "#0D3FA8"
    accent_light  = "#4A7AFF"
    header_bg     = "#0A2352"
    divider       = "#E2EAF6"
    badge_bg      = "#E8EFFE"
    badge_text    = "#1A5CDB"

css_custom = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* ── Global Reset ── */
    .stApp {{
        background-color: {bg_app};
        font-family: 'Inter', sans-serif;
    }}
    .stApp, .stApp p, .stApp span, .stApp label,
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    .stApp div, .stApp section {{
        color: {text_primary} !important;
    }}

    /* ── Hilangkan padding atas bawaan streamlit ── */
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 4rem !important;
        max-width: 720px !important;
    }}

    /* ── Header Korporat ── */
    .corp-header {{
        background: {header_bg};
        border-radius: 16px;
        padding: 36px 40px 30px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }}
    .corp-header::before {{
        content: '';
        position: absolute;
        top: -60px; right: -60px;
        width: 200px; height: 200px;
        border-radius: 50%;
        background: rgba(74, 122, 255, 0.08);
        pointer-events: none;
    }}
    .corp-header::after {{
        content: '';
        position: absolute;
        bottom: -40px; left: 30px;
        width: 140px; height: 140px;
        border-radius: 50%;
        background: rgba(74, 122, 255, 0.05);
        pointer-events: none;
    }}
    .corp-badge {{
        display: inline-block;
        background: {badge_bg};
        color: {badge_text} !important;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 4px 12px;
        border-radius: 20px;
        margin-bottom: 14px;
        border: 1px solid {border_color};
    }}
    .corp-title {{
        color: #FFFFFF !important;
        font-size: 26px !important;
        font-weight: 700 !important;
        margin: 0 0 6px 0 !important;
        letter-spacing: -0.3px;
    }}
    .corp-subtitle {{
        color: rgba(255,255,255,0.55) !important;
        font-size: 14px !important;
        font-weight: 400 !important;
        margin: 0 !important;
    }}

    /* ── Section Label ── */
    .section-label {{
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: {text_muted} !important;
        margin-bottom: 8px;
        margin-top: 20px;
    }}

    /* ── Card Form ── */
    .form-card {{
        background: {bg_card};
        border: 1px solid {border_color};
        border-radius: 14px;
        padding: 28px 32px;
        margin-bottom: 20px;
    }}
    .form-card-title {{
        font-size: 13px;
        font-weight: 600;
        color: {text_secondary} !important;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 20px;
        padding-bottom: 14px;
        border-bottom: 1px solid {divider};
    }}

    /* ── Input Fields ── */
    [data-baseweb="base-input"] {{
        background-color: {bg_input} !important;
        border: 1px solid {border_color} !important;
        border-radius: 10px !important;
        transition: border-color 0.2s, box-shadow 0.2s;
    }}
    [data-baseweb="base-input"]:focus-within {{
        border-color: {border_focus} !important;
        box-shadow: 0 0 0 3px rgba(74,122,255,0.15) !important;
    }}
    [data-baseweb="select"] > div {{
        background-color: {bg_input} !important;
        border: 1px solid {border_color} !important;
        border-radius: 10px !important;
    }}
    input {{
        color: {text_primary} !important;
        font-family: 'Inter', sans-serif !important;
    }}
    [data-baseweb="menu"] {{
        background-color: {bg_card} !important;
        border: 1px solid {border_color} !important;
        border-radius: 10px !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2) !important;
    }}
    [data-baseweb="menu"] li {{
        color: {text_primary} !important;
        font-family: 'Inter', sans-serif !important;
    }}
    [data-baseweb="menu"] li:hover {{
        background-color: {bg_input} !important;
    }}

    /* ── Label Input ── */
    label[data-testid="stWidgetLabel"] p {{
        font-size: 13px !important;
        font-weight: 500 !important;
        color: {text_secondary} !important;
        margin-bottom: 4px !important;
    }}

    /* ── Tombol Submit ── */
    div.stButton > button {{
        background: linear-gradient(135deg, {accent_main} 0%, {accent_dark} 100%) !important;
        border: none !important;
        border-radius: 10px !important;
        width: 100% !important;
        height: 48px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 4px 14px rgba(26,92,219,0.35) !important;
        transition: opacity 0.2s, transform 0.1s !important;
    }}
    div.stButton > button:hover {{
        opacity: 0.9 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(26,92,219,0.45) !important;
    }}
    div.stButton > button:active {{
        transform: translateY(0) !important;
    }}
    div.stButton > button p,
    div.stButton > button span {{
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }}

    /* ── Toggle ── */
    [data-testid="stToggle"] label span {{
        font-size: 13px !important;
        color: {text_secondary} !important;
    }}

    /* ── Info Box ── */
    [data-testid="stAlert"] {{
        background: {badge_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 10px !important;
        border-left: 3px solid {accent_main} !important;
    }}
    [data-testid="stAlert"] p {{
        color: {text_secondary} !important;
        font-size: 13px !important;
    }}

    /* ── Success / Error / Warning Alert ── */
    .stSuccess, .stError, .stWarning {{
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif !important;
    }}

    /* ── Selectbox ── */
    [data-testid="stSelectbox"] label p {{
        font-size: 13px !important;
        font-weight: 500 !important;
        color: {text_secondary} !important;
    }}

    /* ── Divider ── */
    hr {{
        border-color: {divider} !important;
        margin: 24px 0 !important;
    }}

    /* ── Caption / Teks kecil ── */
    .stCaption, [data-testid="stCaption"] {{
        font-size: 12px !important;
        color: {text_muted} !important;
    }}

    /* ── Form Submit ── */
    [data-testid="stForm"] {{
        background: {bg_card} !important;
        border: 1px solid {border_color} !important;
        border-radius: 14px !important;
        padding: 24px 28px !important;
    }}
    </style>
"""
st.markdown(css_custom, unsafe_allow_html=True)

# ==========================================
# 2. KONFIGURASI MODEL & FITUR TIM
# ==========================================
@st.cache_resource
def load_model(nama_file):
    with open(nama_file, 'rb') as file:
        return pickle.load(file)

pilihan_model = {
    'Decision Tree': 'final_pipeline_dt.pkl',
    'Logistic Regression': 'final_pipeline_lr.pkl',
    'XGBoost': 'final_pipeline_xgb.pkl'
}

fitur_model = {
    'Decision Tree': ['Usia', 'Jenis_Kelamin', 'Lama_Bekerja', 'Pendapatan_Tahunan', 'Skor_Kredit', 'Jumlah_Pinjaman', 'Pendidikan'],
    'Logistic Regression': ['Usia', 'Jenis_Kelamin', 'Jumlah_Tanggungan', 'Pendapatan_Tahunan', 'Skor_Kredit', 'Jumlah_Pinjaman', 'Rasio_Pinjaman', 'Kategori_Skor', 'Pekerjaan'],
    'XGBoost': ['Jenis_Kelamin', 'Jumlah_Tanggungan', 'Skor_Kredit', 'Jumlah_Pinjaman', 'Kategori_Skor', '_cat']
}

# ==========================================
# 3. HEADER KORPORAT
# ==========================================
st.markdown(f"""
<div class="corp-header">
    <div class="corp-badge">🏢 Justin Corp. — Credit Analytics</div>
    <h1 class="corp-title">Sistem Analisis Skor Kredit</h1>
    <p class="corp-subtitle">Prediksi status default debitur menggunakan pemodelan Machine Learning terintegrasi</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 4. PILIH MODEL
# ==========================================
st.markdown('<p class="section-label">Konfigurasi Model</p>', unsafe_allow_html=True)
model_dipilih = st.selectbox(
    "🤖 Algoritma Prediksi",
    list(pilihan_model.keys()),
    help="Pilih algoritma yang ingin digunakan untuk analisis risiko kredit."
)
fitur_aktif = fitur_model[model_dipilih]

try:
    model_aktif = load_model(pilihan_model[model_dipilih])
except FileNotFoundError:
    st.error(f"⚠️ File model `{pilihan_model[model_dipilih]}` tidak ditemukan. Pastikan file berada di direktori yang sama.")
    st.stop()

# ==========================================
# 5. FORM INPUT DINAMIS
# ==========================================
st.markdown('<p class="section-label" style="margin-top:24px;">Data Debitur</p>', unsafe_allow_html=True)

input_data = {}

with st.form("form_kredit"):
    st.caption(f"Parameter input untuk model **{model_dipilih}** — isi semua kolom yang tersedia")
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        if 'Usia' in fitur_aktif:
            input_data['Usia'] = st.number_input("Usia", min_value=0, value=30, help="Rentang 21–65 tahun")
        if 'Jenis_Kelamin' in fitur_aktif:
            jk_input = st.selectbox("Jenis Kelamin", ["Laki-Laki", "Perempuan"])
            input_data['Jenis_Kelamin'] = 1 if jk_input == "Laki-Laki" else 0
        if 'Lama_Bekerja' in fitur_aktif:
            input_data['Lama_Bekerja'] = st.number_input("Lama Bekerja (tahun)", min_value=0, value=5, help="Rentang 1–35 tahun")
        if 'Jumlah_Tanggungan' in fitur_aktif:
            input_data['Jumlah_Tanggungan'] = st.number_input("Jumlah Tanggungan", min_value=0, value=1, help="Rentang 1–6")
        if 'Pendapatan_Tahunan' in fitur_aktif:
            input_data['Pendapatan_Tahunan'] = st.number_input("Pendapatan Tahunan (juta Rp)", min_value=0, value=100, help="Rentang 70–626 juta")
        if 'Pendidikan' in fitur_aktif:
            input_data['Pendidikan'] = st.selectbox("Pendidikan Terakhir", ["SMP", "SMA", "S1-Setara"])

    with col2:
        if 'Jumlah_Pinjaman' in fitur_aktif:
            input_data['Jumlah_Pinjaman'] = st.number_input("Jumlah Pinjaman (juta Rp)", min_value=0, value=300, help="Rentang 209–2074 juta")
        if 'Skor_Kredit' in fitur_aktif:
            input_data['Skor_Kredit'] = st.number_input("Skor Kredit", min_value=0, value=650, help="Rentang 350–850")
        if 'Kategori_Skor' in fitur_aktif:
            input_data['Kategori_Skor'] = st.selectbox("Kategori Skor Kredit", ["Risky", "Sub-Prime", "Prime"])
        if 'Pekerjaan' in fitur_aktif:
            input_data['Pekerjaan'] = st.selectbox("Pekerjaan", ["Pak Ogah", "Tukang Sayur", "Starling", "Jamu Keliling", "Tukang Bubur"])
        if '_cat' in fitur_aktif:
            input_data['_cat'] = st.selectbox("Kategori (_cat)", ["01", "02", "03"])

    if 'Rasio_Pinjaman' in fitur_aktif:
        st.info("💡 **Rasio Pinjaman** dihitung otomatis oleh sistem berdasarkan Jumlah Pinjaman ÷ Pendapatan Tahunan.")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    submitted = st.form_submit_button("🔍  Analisis Kelayakan Risiko Kredit", type="primary")

# ==========================================
# 6. LOGIKA VALIDASI & PREDIKSI
# ==========================================
if submitted:
    pesan_error = []

    if 'Usia' in fitur_aktif and not (21 <= input_data['Usia'] <= 65):
        pesan_error.append("**Usia** harus berada di antara 21 hingga 65 tahun.")
    if 'Lama_Bekerja' in fitur_aktif and not (1 <= input_data['Lama_Bekerja'] <= 35):
        pesan_error.append("**Lama Bekerja** harus berada di antara 1 hingga 35 tahun.")
    if 'Jumlah_Tanggungan' in fitur_aktif and not (1 <= input_data['Jumlah_Tanggungan'] <= 6):
        pesan_error.append("**Jumlah Tanggungan** harus berada di antara 1 hingga 6.")
    if 'Pendapatan_Tahunan' in fitur_aktif and not (70 <= input_data['Pendapatan_Tahunan'] <= 626):
        pesan_error.append("**Pendapatan Tahunan** harus di rentang 70 hingga 626 juta.")
    if 'Jumlah_Pinjaman' in fitur_aktif and not (209 <= input_data['Jumlah_Pinjaman'] <= 2074):
        pesan_error.append("**Jumlah Pinjaman** harus di rentang 209 hingga 2074 juta.")
    if 'Skor_Kredit' in fitur_aktif and not (350 <= input_data['Skor_Kredit'] <= 850):
        pesan_error.append("**Skor Kredit** harus berada di antara 350 hingga 850.")

    if len(pesan_error) > 0:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.error("⚠️ **Validasi gagal.** Perbaiki data berikut sebelum melanjutkan:", icon=None)
        for error in pesan_error:
            st.warning(f"› {error}")
    else:
        if 'Rasio_Pinjaman' in fitur_aktif:
            input_data['Rasio_Pinjaman'] = input_data['Jumlah_Pinjaman'] / input_data['Pendapatan_Tahunan']

        df_prediksi = pd.DataFrame([input_data])[fitur_aktif]

        try:
            hasil_prediksi = model_aktif.predict(df_prediksi)[0]
            probabilitas = model_aktif.predict_proba(df_prediksi)[0]

            skor_lancar = probabilitas[0] * 100
            skor_default = probabilitas[1] * 100

            st.markdown("---")
            st.markdown(f'<p class="section-label">Hasil Analisis — {model_dipilih}</p>', unsafe_allow_html=True)

            if hasil_prediksi == 0:
                # ── HASIL: TIDAK DEFAULT ──
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #0A2E1A 0%, #0D3520 100%);
                    border: 1px solid #1A6B3A;
                    border-left: 4px solid #22C55E;
                    border-radius: 14px;
                    padding: 28px 32px;
                    margin-bottom: 16px;
                ">
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom:14px;">
                        <div style="
                            width:44px; height:44px; border-radius:50%;
                            background:#14532D; display:flex;
                            align-items:center; justify-content:center;
                            font-size:20px;
                        ">✅</div>
                        <div>
                            <p style="margin:0; font-size:11px; font-weight:600; letter-spacing:0.1em;
                                text-transform:uppercase; color:#4ADE80 !important;">Keputusan Sistem</p>
                            <p style="margin:0; font-size:20px; font-weight:700; color:#FFFFFF !important;">
                                Risiko Rendah — Tidak Default</p>
                        </div>
                    </div>
                    <div style="
                        background:rgba(255,255,255,0.05); border-radius:10px;
                        padding:16px 20px; margin-bottom:16px;
                        display:flex; align-items:center; justify-content:space-between;
                    ">
                        <span style="font-size:13px; color:rgba(255,255,255,0.6) !important;">
                            Tingkat keyakinan sistem (Tidak Default)
                        </span>
                        <span style="font-size:24px; font-weight:700; color:#4ADE80 !important;">
                            {skor_lancar:.1f}%
                        </span>
                    </div>
                    <p style="margin:0; font-size:14px; color:rgba(255,255,255,0.7) !important; line-height:1.6;">
                        Parameter debitur menunjukkan kemampuan bayar yang memadai. 
                        Sistem merekomendasikan <strong style="color:#4ADE80 !important;">Persetujuan (Approve)</strong> atas pengajuan ini.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()

            else:
                # ── HASIL: DEFAULT ──
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #2A0A0A 0%, #350D0D 100%);
                    border: 1px solid #6B1A1A;
                    border-left: 4px solid #EF4444;
                    border-radius: 14px;
                    padding: 28px 32px;
                    margin-bottom: 16px;
                ">
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom:14px;">
                        <div style="
                            width:44px; height:44px; border-radius:50%;
                            background:#450A0A; display:flex;
                            align-items:center; justify-content:center;
                            font-size:20px;
                        ">🚨</div>
                        <div>
                            <p style="margin:0; font-size:11px; font-weight:600; letter-spacing:0.1em;
                                text-transform:uppercase; color:#F87171 !important;">Keputusan Sistem</p>
                            <p style="margin:0; font-size:20px; font-weight:700; color:#FFFFFF !important;">
                                Risiko Tinggi — Berpotensi Default</p>
                        </div>
                    </div>
                    <div style="
                        background:rgba(255,255,255,0.05); border-radius:10px;
                        padding:16px 20px; margin-bottom:16px;
                        display:flex; align-items:center; justify-content:space-between;
                    ">
                        <span style="font-size:13px; color:rgba(255,255,255,0.6) !important;">
                            Tingkat keyakinan gagal bayar (Default)
                        </span>
                        <span style="font-size:24px; font-weight:700; color:#F87171 !important;">
                            {skor_default:.1f}%
                        </span>
                    </div>
                    <p style="margin:0; font-size:14px; color:rgba(255,255,255,0.7) !important; line-height:1.6;">
                        Model mendeteksi indikasi potensi gagal bayar berdasarkan pembobotan data masukan. 
                        Sistem merekomendasikan <strong style="color:#F87171 !important;">Penolakan (Reject)</strong> atas pengajuan ini.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                st.snow()

        except Exception as e:
            st.error("Terjadi kesalahan saat memproses model. Pastikan tipe data sesuai dengan yang dilatih.")
            st.caption(f"Detail error: {e}")

# ==========================================
# 7. FOOTER
# ==========================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align:center; padding: 20px 0; border-top: 1px solid {'#1E2535' if mode_gelap else '#E2EAF6'};">
    <p style="font-size:12px; color:{'#3A4560' if mode_gelap else '#A0B0CC'} !important; margin:0; letter-spacing:0.04em;">
        JUSTIN CORP. &nbsp;·&nbsp; Credit Risk Analytics Platform &nbsp;·&nbsp; Made with ❤️
    </p>
</div>
""", unsafe_allow_html=True)
