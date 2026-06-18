import streamlit as st
import pickle
import pandas as pd

st.set_page_config(page_title="Justin Corp — Analisis Kredit", page_icon="🏢", layout="centered")

# ── Toggle Mode ──
_, col_m = st.columns([7, 3])
with col_m:
    mode_gelap = st.toggle("🌙 Mode Gelap", value=True)

if mode_gelap:
    bg        = "#0B0F1A"
    card      = "#141824"
    inp       = "#1A1F2E"
    border    = "#2A3148"
    focus     = "#4A7AFF"
    txt       = "#E8EDF8"
    txt2      = "#7A88A8"
    accent    = "#4A7AFF"
    accentd   = "#2D5FE8"
    hdr       = "#0A1628"
    div       = "#1E2535"
    grn       = "#22C55E"
    grn_bg    = "#071A0F"
    grn_bd    = "#14532D"
    red       = "#EF4444"
    red_bg    = "#1A0707"
    red_bd    = "#450A0A"
else:
    bg        = "#F0F4FC"
    card      = "#FFFFFF"
    inp       = "#F6F9FF"
    border    = "#D0DCEF"
    focus     = "#1A5CDB"
    txt       = "#0D1A3A"
    txt2      = "#4A5C80"
    accent    = "#1A5CDB"
    accentd   = "#0D3FA8"
    hdr       = "#0A2352"
    div       = "#E2EAF6"
    grn       = "#16A34A"
    grn_bg    = "#F0FDF4"
    grn_bd    = "#BBF7D0"
    red       = "#DC2626"
    red_bg    = "#FFF5F5"
    red_bd    = "#FECACA"

# ── CSS (tanpa Google Fonts, tanpa animasi berat) ──
st.markdown(f"""<style>
.stApp {{background:{bg}; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
.stApp *{{color:{txt}}}
.block-container{{padding-top:1.2rem!important;padding-bottom:3rem!important;max-width:700px!important}}

.hdr{{background:{hdr};border-radius:14px;padding:30px 36px;margin-bottom:20px}}
.hdr-badge{{display:inline-block;background:rgba(74,122,255,0.15);color:{accent}!important;
  font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;
  padding:3px 10px;border-radius:20px;margin-bottom:12px;border:1px solid {border}}}
.hdr h1{{color:#fff!important;font-size:24px!important;font-weight:700!important;margin:0 0 5px!important}}
.hdr p{{color:rgba(255,255,255,.5)!important;font-size:13px!important;margin:0!important}}

.slbl{{font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;
  color:{txt2}!important;margin:18px 0 6px}}

[data-baseweb="base-input"]{{background:{inp}!important;border:1px solid {border}!important;border-radius:8px!important}}
[data-baseweb="base-input"]:focus-within{{border-color:{focus}!important;box-shadow:0 0 0 2px rgba(74,122,255,.2)!important}}
[data-baseweb="select"]>div{{background:{inp}!important;border:1px solid {border}!important;border-radius:8px!important}}
input{{color:{txt}!important}}
[data-baseweb="menu"]{{background:{card}!important;border:1px solid {border}!important;border-radius:8px!important}}
[data-baseweb="menu"] li{{color:{txt}!important}}
label[data-testid="stWidgetLabel"] p{{font-size:13px!important;font-weight:500!important;color:{txt2}!important}}

[data-testid="stForm"]{{background:{card}!important;border:1px solid {border}!important;border-radius:12px!important;padding:20px 24px!important}}

div.stButton>button{{background:{accent}!important;border:none!important;border-radius:8px!important;
  width:100%!important;height:46px!important;font-size:14px!important;font-weight:600!important}}
div.stButton>button:hover{{background:{accentd}!important}}
div.stButton>button p,div.stButton>button span{{color:#fff!important;font-weight:600!important}}

[data-testid="stAlert"]{{border-radius:8px!important}}
hr{{border-color:{div}!important;margin:20px 0!important}}

.res-ok{{background:{grn_bg};border:1px solid {grn_bd};border-left:4px solid {grn};
  border-radius:12px;padding:24px 28px;margin-bottom:12px}}
.res-ok .badge{{font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:{grn}!important;margin-bottom:6px}}
.res-ok h2{{color:#fff!important;font-size:19px!important;font-weight:700!important;margin:0 0 14px!important}}
.res-ok .prob{{background:rgba(255,255,255,.06);border-radius:8px;padding:12px 16px;
  display:flex;align-items:center;justify-content:space-between;margin-bottom:12px}}
.res-ok .prob-val{{font-size:22px;font-weight:700;color:{grn}!important}}
.res-ok .prob-lbl{{font-size:13px;color:rgba(255,255,255,.55)!important}}
.res-ok .desc{{font-size:13px;color:rgba(255,255,255,.65)!important;line-height:1.6;margin:0}}

.res-err{{background:{red_bg};border:1px solid {red_bd};border-left:4px solid {red};
  border-radius:12px;padding:24px 28px;margin-bottom:12px}}
.res-err .badge{{font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:{red}!important;margin-bottom:6px}}
.res-err h2{{color:#fff!important;font-size:19px!important;font-weight:700!important;margin:0 0 14px!important}}
.res-err .prob{{background:rgba(255,255,255,.06);border-radius:8px;padding:12px 16px;
  display:flex;align-items:center;justify-content:space-between;margin-bottom:12px}}
.res-err .prob-val{{font-size:22px;font-weight:700;color:{red}!important}}
.res-err .prob-lbl{{font-size:13px;color:rgba(255,255,255,.55)!important}}
.res-err .desc{{font-size:13px;color:rgba(255,255,255,.65)!important;line-height:1.6;margin:0}}

.footer{{text-align:center;padding:16px 0;border-top:1px solid {div};margin-top:24px}}
.footer p{{font-size:12px;color:{txt2}!important;margin:0;letter-spacing:.04em}}
</style>""", unsafe_allow_html=True)

# ==========================================
# KONFIGURASI MODEL & FITUR
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
# HEADER
# ==========================================
st.markdown(f"""
<div class="hdr">
  <div class="hdr-badge">🏢 Justin Corp. · Credit Analytics</div>
  <h1>Sistem Analisis Skor Kredit</h1>
  <p>Prediksi status default debitur menggunakan pemodelan Machine Learning terintegrasi</p>
</div>""", unsafe_allow_html=True)

# ==========================================
# PILIH MODEL
# ==========================================
st.markdown('<p class="slbl">Konfigurasi Model</p>', unsafe_allow_html=True)
model_dipilih = st.selectbox("🤖 Algoritma Prediksi", list(pilihan_model.keys()),
    help="Pilih algoritma untuk analisis risiko kredit.")
fitur_aktif = fitur_model[model_dipilih]

try:
    model_aktif = load_model(pilihan_model[model_dipilih])
except FileNotFoundError:
    st.error(f"⚠️ File model `{pilihan_model[model_dipilih]}` tidak ditemukan.")
    st.stop()

# ==========================================
# FORM INPUT
# ==========================================
st.markdown('<p class="slbl" style="margin-top:20px">Data Debitur</p>', unsafe_allow_html=True)
input_data = {}

with st.form("form_kredit"):
    st.caption(f"Parameter input untuk model **{model_dipilih}**")
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        if 'Usia' in fitur_aktif:
            input_data['Usia'] = st.number_input("Usia (21–65 tahun)", value=30)
        if 'Jenis_Kelamin' in fitur_aktif:
            jk = st.selectbox("Jenis Kelamin", ["Laki-Laki", "Perempuan"])
            input_data['Jenis_Kelamin'] = 1 if jk == "Laki-Laki" else 0
        if 'Lama_Bekerja' in fitur_aktif:
            input_data['Lama_Bekerja'] = st.number_input("Lama Bekerja (1–35 tahun)", value=5)
        if 'Jumlah_Tanggungan' in fitur_aktif:
            input_data['Jumlah_Tanggungan'] = st.number_input("Jumlah Tanggungan (1–6)", value=1)
        if 'Pendapatan_Tahunan' in fitur_aktif:
            input_data['Pendapatan_Tahunan'] = st.number_input("Pendapatan Tahunan (juta Rp)", value=100)
        if 'Pendidikan' in fitur_aktif:
            input_data['Pendidikan'] = st.selectbox("Pendidikan Terakhir", ["SMP", "SMA", "S1-Setara"])

    with col2:
        if 'Jumlah_Pinjaman' in fitur_aktif:
            input_data['Jumlah_Pinjaman'] = st.number_input("Jumlah Pinjaman (juta Rp)", value=300)
        if 'Skor_Kredit' in fitur_aktif:
            input_data['Skor_Kredit'] = st.number_input("Skor Kredit (350–850)", value=650)
        if 'Kategori_Skor' in fitur_aktif:
            input_data['Kategori_Skor'] = st.selectbox("Kategori Skor", ["Risky", "Sub-Prime", "Prime"])
        if 'Pekerjaan' in fitur_aktif:
            input_data['Pekerjaan'] = st.selectbox("Pekerjaan", ["Pak Ogah", "Tukang Sayur", "Starling", "Jamu Keliling", "Tukang Bubur"])
        if '_cat' in fitur_aktif:
            input_data['_cat'] = st.selectbox("Kategori (_cat)", ["01", "02", "03"])

    if 'Rasio_Pinjaman' in fitur_aktif:
        st.info("💡 **Rasio Pinjaman** dihitung otomatis: Jumlah Pinjaman ÷ Pendapatan Tahunan.")

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    submitted = st.form_submit_button("🔍  Analisis Kelayakan Risiko Kredit", type="primary")

# ==========================================
# VALIDASI & PREDIKSI
# ==========================================
if submitted:
    errors = []
    if 'Usia' in fitur_aktif and not (21 <= input_data['Usia'] <= 65):
        errors.append("**Usia** harus antara 21–65 tahun.")
    if 'Lama_Bekerja' in fitur_aktif and not (1 <= input_data['Lama_Bekerja'] <= 35):
        errors.append("**Lama Bekerja** harus antara 1–35 tahun.")
    if 'Jumlah_Tanggungan' in fitur_aktif and not (1 <= input_data['Jumlah_Tanggungan'] <= 6):
        errors.append("**Jumlah Tanggungan** harus antara 1–6.")
    if 'Pendapatan_Tahunan' in fitur_aktif and not (70 <= input_data['Pendapatan_Tahunan'] <= 626):
        errors.append("**Pendapatan Tahunan** harus di rentang 70–626 juta.")
    if 'Jumlah_Pinjaman' in fitur_aktif and not (209 <= input_data['Jumlah_Pinjaman'] <= 2074):
        errors.append("**Jumlah Pinjaman** harus di rentang 209–2074 juta.")
    if 'Skor_Kredit' in fitur_aktif and not (350 <= input_data['Skor_Kredit'] <= 850):
        errors.append("**Skor Kredit** harus antara 350–850.")

    if errors:
        st.error("⚠️ **Validasi gagal.** Perbaiki data berikut:")
        for e in errors:
            st.warning(f"› {e}")
    else:
        if 'Rasio_Pinjaman' in fitur_aktif:
            input_data['Rasio_Pinjaman'] = input_data['Jumlah_Pinjaman'] / input_data['Pendapatan_Tahunan']

        df_prediksi = pd.DataFrame([input_data])[fitur_aktif]

        try:
            hasil = model_aktif.predict(df_prediksi)[0]
            prob  = model_aktif.predict_proba(df_prediksi)[0]
            skor_lancar  = prob[0] * 100
            skor_default = prob[1] * 100

            st.markdown("---")
            st.markdown(f'<p class="slbl">Hasil Analisis — {model_dipilih}</p>', unsafe_allow_html=True)

            if hasil == 0:
                st.markdown(f"""
                <div class="res-ok">
                  <p class="badge">✅ Keputusan Sistem</p>
                  <h2>Risiko Rendah — Tidak Default</h2>
                  <div class="prob">
                    <span class="prob-lbl">Keyakinan tidak default</span>
                    <span class="prob-val">{skor_lancar:.1f}%</span>
                  </div>
                  <p class="desc">Parameter debitur menunjukkan kemampuan bayar yang memadai.
                  Sistem merekomendasikan <strong>Persetujuan (Approve)</strong> atas pengajuan ini.</p>
                </div>""", unsafe_allow_html=True)
                st.balloons()
            else:
                st.markdown(f"""
                <div class="res-err">
                  <p class="badge">🚨 Keputusan Sistem</p>
                  <h2>Risiko Tinggi — Berpotensi Default</h2>
                  <div class="prob">
                    <span class="prob-lbl">Keyakinan gagal bayar</span>
                    <span class="prob-val">{skor_default:.1f}%</span>
                  </div>
                  <p class="desc">Model mendeteksi indikasi potensi gagal bayar berdasarkan data masukan.
                  Sistem merekomendasikan <strong>Penolakan (Reject)</strong> atas pengajuan ini.</p>
                </div>""", unsafe_allow_html=True)
                st.snow()

        except Exception as e:
            st.error("Terjadi kesalahan saat memproses model. Pastikan tipe data sesuai.")
            st.caption(f"Detail: {e}")

# ── Footer ──
st.markdown(f"""
<div class="footer">
  <p>JUSTIN CORP. &nbsp;·&nbsp; Credit Risk Analytics &nbsp;·&nbsp; Made with ❤️</p>
</div>""", unsafe_allow_html=True)
