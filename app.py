import streamlit as st
import pickle
import pandas as pd

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(page_title="Simulasi Skor Kredit", page_icon="💳", layout="centered")

# ==========================================
# 1. FITUR TOMBOL & CSS CUSTOM MODE
# ==========================================
header_container = st.container()
with header_container:
    col_t, col_m = st.columns([7, 3])
    with col_m:
        mode_gelap = st.toggle("🌙 Mode Gelap", value=True)

if mode_gelap:
    css_custom = """
        <style>
        .stApp { background-color: #0E1117; }
        .stApp, .stApp p, .stApp span, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 { color: #FAFAFA !important; }
        
        [data-baseweb="base-input"], [data-baseweb="select"] > div { 
            background-color: #262730 !important; 
            border: 1px solid #444444 !important; 
            border-radius: 6px !important; 
        }
        input, [data-baseweb="menu"] li { color: #FAFAFA !important; }
        [data-baseweb="menu"] { background-color: #262730 !important; }
        
        /* PERBAIKAN TOMBOL DARK MODE */
        div.stButton > button, div.stButton > button:hover, div.stButton > button:active { 
            background-color: #FF4B4B !important; 
            border: 1px solid #FF4B4B !important; 
            border-radius: 8px !important; 
            width: 100% !important; 
        }
        div.stButton > button p, div.stButton > button span { 
            color: #FFFFFF !important; 
            font-weight: bold !important; 
        }
        </style>
    """
else:
    css_custom = """
        <style>
        .stApp { background-color: #F4F6F9; }
        .stApp, .stApp p, .stApp span, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 { color: #1A1A1A !important; }
        
        [data-baseweb="base-input"], [data-baseweb="select"] > div { 
            background-color: #FFFFFF !important; 
            border: 1px solid #DEDEDE !important; 
            border-radius: 6px !important; 
        }
        input, [data-baseweb="menu"] li, [data-baseweb="select"] div { color: #1A1A1A !important; }
        [data-baseweb="menu"] { background-color: #FFFFFF !important; }
        
        /* PERBAIKAN TOMBOL LIGHT MODE - Memaksa warna putih pada teks tombol */
        div.stButton > button, div.stButton > button:hover, div.stButton > button:active { 
            background-color: #FF4B4B !important; 
            border: 1px solid #FF4B4B !important; 
            border-radius: 8px !important; 
            width: 100% !important; 
        }
        div.stButton > button p, div.stButton > button span { 
            color: #FFFFFF !important; 
            font-weight: bold !important; 
        }
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
# 3. KONTEN HALAMAN & FORM DINAMIS
# ==========================================
st.title("💳 Simulasi Skor Kredit")
st.write("Prediksi *Status Default* menggunakan model *Machine Learning*.")

model_dipilih = st.selectbox("🤖 Pilih Algoritma Model:", list(pilihan_model.keys()))
fitur_aktif = fitur_model[model_dipilih]

try:
    model_aktif = load_model(pilihan_model[model_dipilih])
except FileNotFoundError:
    st.error(f"File '{pilihan_model[model_dipilih]}' tidak ditemukan. Pastikan file ada di folder yang sama.")
    st.stop()

st.markdown("<br>", unsafe_allow_html=True)
input_data = {}

with st.form("form_kredit"):
    st.subheader(f"Parameter Input ({model_dipilih})")
    st.caption("Masukkan angka sesuai dengan ketentuan rentang yang valid.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'Usia' in fitur_aktif:
            input_data['Usia'] = st.number_input("Usia (Rentang 21 - 65 Tahun)", value=30)
        if 'Jenis_Kelamin' in fitur_aktif:
            jk_input = st.selectbox("Jenis Kelamin", ["Laki-Laki", "Perempuan"])
            input_data['Jenis_Kelamin'] = 1 if jk_input == "Laki-Laki" else 0
        if 'Lama_Bekerja' in fitur_aktif:
            input_data['Lama_Bekerja'] = st.number_input("Lama Bekerja (Rentang 1 - 35 Tahun)", value=5)
        if 'Jumlah_Tanggungan' in fitur_aktif:
            input_data['Jumlah_Tanggungan'] = st.number_input("Jumlah Tanggungan (Rentang 1 - 6)", value=1)
        if 'Pendapatan_Tahunan' in fitur_aktif:
            input_data['Pendapatan_Tahunan'] = st.number_input("Pendapatan Tahunan (70 - 626 Juta Rp)", value=100)
        if 'Pendidikan' in fitur_aktif:
            input_data['Pendidikan'] = st.selectbox("Pendidikan", ["SMP", "SMA", "S1-Setara"])

    with col2:
        if 'Jumlah_Pinjaman' in fitur_aktif:
            input_data['Jumlah_Pinjaman'] = st.number_input("Jumlah Pinjaman (209 - 2074 Juta Rp)", value=300)
        if 'Skor_Kredit' in fitur_aktif:
            input_data['Skor_Kredit'] = st.number_input("Skor Kredit (Rentang 350 - 850)", value=650)
        if 'Kategori_Skor' in fitur_aktif:
            input_data['Kategori_Skor'] = st.selectbox("Kategori Skor", ["Risky", "Sub-Prime", "Prime"])
        if 'Pekerjaan' in fitur_aktif:
            input_data['Pekerjaan'] = st.selectbox("Pekerjaan", ["Pak Ogah", "Tukang Sayur", "Starling", "Jamu Keliling", "Tukang Bubur"])
        if '_cat' in fitur_aktif:
            input_data['_cat'] = st.selectbox("Kategori (_cat)", ["01", "02", "03"])

    if 'Rasio_Pinjaman' in fitur_aktif:
        st.info("💡 **Rasio Pinjaman** akan dihitung otomatis oleh sistem (Jumlah Pinjaman / Pendapatan Tahunan).")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Penambahan type="primary" agar Streamlit mengenali ini sebagai tombol utama
    submitted = st.form_submit_button("Analisis Kelayakan Risiko", type="primary")

# ==========================================
# 4. LOGIKA VALIDASI & PREDIKSI
# ==========================================
if submitted:
    pesan_error = []
    
    if 'Usia' in fitur_aktif and not (21 <= input_data['Usia'] <= 65):
        pesan_error.append("❌ **Usia** harus berada di antara 21 hingga 65.")
    if 'Lama_Bekerja' in fitur_aktif and not (1 <= input_data['Lama_Bekerja'] <= 35):
        pesan_error.append("❌ **Lama Bekerja** harus berada di antara 1 hingga 35.")
    if 'Jumlah_Tanggungan' in fitur_aktif and not (1 <= input_data['Jumlah_Tanggungan'] <= 6):
        pesan_error.append("❌ **Jumlah Tanggungan** harus berada di antara 1 hingga 6.")
    if 'Pendapatan_Tahunan' in fitur_aktif and not (70 <= input_data['Pendapatan_Tahunan'] <= 626):
        pesan_error.append("❌ **Pendapatan Tahunan** harus berada di rentang 70 hingga 626 juta.")
    if 'Jumlah_Pinjaman' in fitur_aktif and not (209 <= input_data['Jumlah_Pinjaman'] <= 2074):
        pesan_error.append("❌ **Jumlah Pinjaman** harus berada di rentang 209 hingga 2074 juta.")
    if 'Skor_Kredit' in fitur_aktif and not (350 <= input_data['Skor_Kredit'] <= 850):
        pesan_error.append("❌ **Skor Kredit** harus berada di antara 350 hingga 850.")

    if len(pesan_error) > 0:
        st.error("⚠️ **Validasi Gagal! Perbaiki data berikut sebelum melakukan analisis:**")
        for error in pesan_error:
            st.warning(error)
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
            st.subheader(f"Hasil Analisis - {model_dipilih}")
            
            with st.container():
                if hasil_prediksi == 0:
                    st.success(f"✅ **Risiko Rendah** - Prediksi: TIDAK DEFAULT")
                    st.info(f"📊 **Skor Keyakinan (Tidak Default):** {skor_lancar:.1f}%")
                    st.write("Parameter debitur menunjukkan kemampuan bayar yang baik. Layak diberikan persetujuan (Approve).")
                    st.balloons()
                else:
                    st.error(f"🚨 **Risiko Tinggi** - Prediksi: DEFAULT")
                    st.warning(f"📊 **Skor Keyakinan Gagal Bayar (Default):** {skor_default:.1f}%")
                    st.write("Model mendeteksi potensi gagal bayar berdasarkan pembobotan data. Direkomendasikan untuk menolak pengajuan (Reject).")
                    st.markdown("<h1 style='text-align: center; font-size: 80px;'>😢</h1>", unsafe_allow_html=True)
                    st.snow()
                    
        except Exception as e:
            st.error("Terjadi kesalahan saat memproses model. Pastikan tipe data sesuai dengan yang dilatih.")
            st.write(f"Detail error: {e}")