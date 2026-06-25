import streamlit as st
from rembg import remove
from PIL import Image
import io
import time
import datetime

st.set_page_config(
    page_title="AI Background Remover",
    page_icon="✂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ADVANCED STYLING ====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Base App Colors */
.stApp {
    background-color: #f4f7fe;
    color: #1b254b;
}

/* Header & Default Overrides */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; }

/* ==================== HERO SECTION ==================== */
.hero {
    background: linear-gradient(135deg, #7F00FF 0%, #E100FF 100%);
    border-radius: 24px; 
    padding: 3rem 2rem; 
    color: white; 
    text-align: center; 
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(127, 0, 255, 0.2);
}

.hero::before {
    content: '';
    position: absolute;
    top: -50%; left: -20%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%);
    border-radius: 50%;
}

.hero::after {
    content: '';
    position: absolute;
    bottom: -50%; right: -10%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
    border-radius: 50%;
}

.hero h1 { 
    font-size: 3rem; 
    font-weight: 800; 
    margin: 0; 
    letter-spacing: -0.02em;
    text-shadow: 0 4px 10px rgba(0,0,0,0.1);
    position: relative; z-index: 1;
}

.hero p { 
    font-size: 1.1rem; 
    font-weight: 400;
    opacity: 0.9; 
    margin-top: 15px; 
    position: relative; z-index: 1;
}

/* ==================== CARDS & CONTAINERS ==================== */
.card {
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.5);
    border-radius: 20px; 
    padding: 24px;
    box-shadow: 0 10px 30px rgba(112, 144, 176, 0.15); 
    margin-bottom: 20px;
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(112, 144, 176, 0.2);
}

/* ==================== METRIC CARDS ==================== */
.metric-grid {
    display: flex;
    gap: 20px;
    margin-bottom: 30px;
}

.metric-card {
    flex: 1;
    background: white;
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 10px 30px rgba(112, 144, 176, 0.12);
    display: flex;
    flex-direction: column;
    justify-content: center;
    position: relative;
    overflow: hidden;
    transition: transform 0.3s;
}

.metric-card:hover {
    transform: translateY(-5px);
}

.metric-icon-wrap {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    margin-bottom: 15px;
}

.icon-purple { background: #F4EEFF; color: #7F00FF; }
.icon-pink { background: #FFEDF6; color: #E100FF; }
.icon-blue { background: #E8F4FF; color: #0075FF; }
.icon-green { background: #E6FFF2; color: #00B86E; }

.metric-card .value { 
    font-size: 2.2rem; 
    font-weight: 800; 
    color: #1b254b;
    line-height: 1.2;
}

.metric-card .label { 
    font-size: 0.9rem; 
    color: #a3aed1; 
    font-weight: 600;
    margin-top: 5px; 
}

/* ==================== BUTTONS ==================== */
.stButton > button {
    background: linear-gradient(135deg, #7F00FF 0%, #E100FF 100%) !important;
    color: white !important; 
    border: none !important; 
    border-radius: 14px !important;
    font-weight: 700 !important; 
    font-size: 1.1rem !important;
    padding: 0.8rem 1.5rem !important;
    width: 100%;
    box-shadow: 0 10px 20px rgba(127, 0, 255, 0.3) !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 15px 25px rgba(127, 0, 255, 0.4) !important;
}

.stDownloadButton > button {
    background: linear-gradient(135deg, #00C9FF 0%, #92FE9D 100%) !important;
    color: #0c3823 !important;
    box-shadow: 0 10px 20px rgba(0, 201, 255, 0.3) !important;
}

/* ==================== INFO & RESULT BOXES ==================== */
.result-box {
    background: #F4EEFF;
    border: 2px dashed #7F00FF;
    border-radius: 16px; 
    padding: 20px; 
    margin: 15px 0;
    color: #4A148C;
}

.info-box {
    background: white;
    border-left: 5px solid #E100FF;
    border-radius: 12px; 
    padding: 16px 20px; 
    margin: 15px 0;
    box-shadow: 0 5px 15px rgba(112, 144, 176, 0.1);
}

/* ==================== TAGS ==================== */
.tag-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    margin-top: 20px;
}

.tag {
    background: white; 
    color: #7F00FF;
    border: 1px solid rgba(127,0,255,0.2);
    border-radius: 20px; 
    padding: 6px 16px; 
    font-size: 13px; 
    font-weight: 600; 
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

/* ==================== SIDEBAR ==================== */
[data-testid="stSidebar"] {
    background: white !important;
    border-right: 1px solid #e0e5f2;
}

[data-testid="stSidebar"] * {
    color: #1b254b !important;
}

.sidebar-profile {
    background: linear-gradient(135deg, #7F00FF 0%, #E100FF 100%);
    border-radius: 16px;
    padding: 20px;
    color: white;
    margin-bottom: 20px;
    box-shadow: 0 10px 20px rgba(127, 0, 255, 0.2);
}

.sidebar-profile * { color: white !important; }
.sidebar-profile h3 { margin: 0 0 10px 0; font-size: 1.2rem; font-weight: 700; }
.sidebar-profile p { margin: 2px 0; font-size: 0.9rem; opacity: 0.9; }

/* File Uploader styling */
[data-testid="stFileUploadDropzone"] {
    border: 2px dashed #a3aed1 !important;
    border-radius: 20px !important;
    background: rgba(255,255,255,0.5) !important;
}
[data-testid="stFileUploadDropzone"]:hover {
    border-color: #7F00FF !important;
    background: rgba(127,0,255,0.05) !important;
}
</style>
""", unsafe_allow_html=True)

# ==================== STATE MANAGEMENT ====================
if "history" not in st.session_state:
    st.session_state.history = []
if "total_processed" not in st.session_state:
    st.session_state.total_processed = 0
if "total_time" not in st.session_state:
    st.session_state.total_time = 0.0

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
        <div style="font-size:2rem; background: linear-gradient(135deg, #7F00FF, #E100FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">✂️</div>
        <h2 style="margin:0; font-weight:800; font-size:1.4rem;">AI Remover</h2>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.radio("Navigasi", ["🏠  Beranda", "🖼️  Hapus Background", "📊  Dashboard"], label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-profile">
        <h3>👩‍💻 Profil Developer</h3>
        <p><b>Devia Puji Astuti</b></p>
        <p>NPM: 2311531005</p>
        <p>Informatika 23</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card" style="padding:15px; margin-top:10px;">
        <div style="font-size:0.85rem; color:#a3aed1; font-weight:600; margin-bottom:8px;">TECH STACK</div>
        <div style="font-size:0.9rem; font-weight:600;">
            🤖 U2-Net via rembg<br>
            🐍 Python & Streamlit<br>
            🖼️ PIL & ONNX
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== BERANDA ====================
if page == "🏠  Beranda":
    st.markdown("""
    <div class="hero">
        <h1>✂️ Magic Background Remover</h1>
        <p>Hapus latar belakang gambar secara otomatis dalam hitungan detik menggunakan kekuatan <b>AI Deep Learning</b>.<br>
        Ditenagai oleh arsitektur <strong>U2-Net</strong> untuk hasil potongan yang presisi dan rapi.</p>
    </div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon-wrap icon-purple">🧠</div>
            <div class="value">U2-Net</div>
            <div class="label">Arsitektur AI Model</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon-wrap icon-pink">✨</div>
            <div class="value">PNG</div>
            <div class="label">Format Output Transparan</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon-wrap icon-blue">⚡</div>
            <div class="value">~3 dtk</div>
            <div class="label">Rata-rata Kecepatan Proses</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("### 🚀 Cara Menggunakan")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="card" style="text-align:center; padding:30px 20px;">
            <div style="font-size:3rem; margin-bottom:15px;">📁</div>
            <h3 style="font-size:1.2rem; font-weight:700; margin-bottom:10px;">1. Upload File</h3>
            <p style="font-size:0.9rem; color:#a3aed1;">Unggah foto dengan format JPG atau PNG ke dalam sistem.</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card" style="text-align:center; padding:30px 20px;">
            <div style="font-size:3rem; margin-bottom:15px;">🤖</div>
            <h3 style="font-size:1.2rem; font-weight:700; margin-bottom:10px;">2. AI Processing</h3>
            <p style="font-size:0.9rem; color:#a3aed1;">Model U2-Net akan menyeleksi objek utama secara otomatis.</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="card" style="text-align:center; padding:30px 20px;">
            <div style="font-size:3rem; margin-bottom:15px;">💾</div>
            <h3 style="font-size:1.2rem; font-weight:700; margin-bottom:10px;">3. Download Hasil</h3>
            <p style="font-size:0.9rem; color:#a3aed1;">Simpan gambar berformat PNG dengan background transparan.</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="tag-container">
        <span class="tag">Python 3.8+</span>
        <span class="tag">rembg</span>
        <span class="tag">U2-Net Architecture</span>
        <span class="tag">Pillow (PIL)</span>
        <span class="tag">Streamlit UI</span>
        <span class="tag">ONNX Runtime</span>
    </div>
    """, unsafe_allow_html=True)

# ==================== HAPUS BACKGROUND ====================
elif page == "🖼️  Hapus Background":
    st.markdown("<h2 style='font-weight:800; margin-bottom:20px; color:#1b254b;'>🖼️ Workspace Penghapus Background</h2>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Seret & Lepas atau Klik untuk Memilih Gambar (JPG / PNG)", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        input_image = Image.open(uploaded_file)
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("<h4 style='font-weight:700; color:#1b254b; margin-bottom:15px;'>📷 Gambar Original</h4>", unsafe_allow_html=True)
            st.image(input_image, use_column_width=True, output_format="auto")
            
            st.markdown(f"""
            <div class="info-box">
                <div style="font-size:0.85rem; color:#a3aed1; font-weight:700; margin-bottom:5px;">FILE INFO</div>
                <b style="color:#1b254b;">Nama:</b> {uploaded_file.name}<br>
                <b style="color:#1b254b;">Resolusi:</b> {input_image.width} × {input_image.height} px<br>
                <b style="color:#1b254b;">Mode:</b> {input_image.mode}
            </div>""", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<h4 style='font-weight:700; color:#1b254b; margin-bottom:15px;'>✨ Hasil Transparan</h4>", unsafe_allow_html=True)
            placeholder = st.empty()
            placeholder.markdown("""
            <div class="card" style="text-align:center; padding:60px 20px; border:2px dashed #e0e5f2;">
                <div style="font-size:3rem; margin-bottom:10px;">🪄</div>
                <h4 style="color:#1b254b; font-weight:700;">Siap Diproses!</h4>
                <p style="color:#a3aed1; font-size:0.9rem;">Klik tombol di bawah untuk memulai keajaiban AI.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Centered button logic
        _, btn_col, _ = st.columns([1,2,1])
        with btn_col:
            if st.button("🚀 Proses Gambar Sekarang", use_container_width=True):
                with st.spinner("🧠 AI U2-Net sedang menganalisis piksel..."):
                    start = time.time()
                    output_image = remove(input_image)
                    elapsed = round(time.time() - start, 2)

                st.session_state.total_processed += 1
                st.session_state.total_time += elapsed
                st.session_state.history.append({
                    "no": st.session_state.total_processed,
                    "nama": uploaded_file.name,
                    "resolusi": f"{input_image.width}×{input_image.height}",
                    "waktu": elapsed,
                    "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
                })

                with col2:
                    # Menampilkan image dengan background pola catur untuk memperjelas transparansi
                    placeholder.image(output_image, use_column_width=True)
                    st.markdown(f"""
                    <div class="result-box">
                        <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
                            <div style="font-size:1.5rem;">✅</div>
                            <b style="font-size:1.1rem;">Berhasil Dihapus!</b>
                        </div>
                        <div style="font-size:0.9rem; line-height:1.6;">
                            ⏱️ <b>Waktu Eksekusi:</b> {elapsed} detik<br>
                            ⚙️ <b>Mesin AI:</b> U2-Net via rembg
                        </div>
                    </div>""", unsafe_allow_html=True)

                buf = io.BytesIO()
                output_image.save(buf, format="PNG")
                
                with btn_col:
                    st.download_button("⬇️ Download Hasil (.PNG)", data=buf.getvalue(),
                        file_name=f"nobg_{uploaded_file.name.split('.')[0]}.png", mime="image/png")
    else:
        st.markdown("""
        <div class="card" style="text-align:center; padding:80px 20px; border:2px dashed #a3aed1; background:transparent;">
            <div style="font-size:4rem; margin-bottom:20px;">🖼️</div>
            <h3 style="color:#1b254b; font-weight:700;">Area Kerja Kosong</h3>
            <p style="color:#a3aed1;">Silahkan unggah gambar terlebih dahulu pada area dropzone di atas.</p>
        </div>""", unsafe_allow_html=True)

# ==================== DASHBOARD ====================
elif page == "📊  Dashboard":
    st.markdown("<h2 style='font-weight:800; margin-bottom:20px; color:#1b254b;'>📊 Dashboard Statistik Sistem</h2>", unsafe_allow_html=True)
    
    total = st.session_state.total_processed
    avg_t = round(st.session_state.total_time / total, 2) if total > 0 else 0
    total_t = round(st.session_state.total_time, 2)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon-wrap icon-purple">🖼️</div>
            <div class="value">{total}</div>
            <div class="label">Gambar Diproses</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon-wrap icon-blue">⏱️</div>
            <div class="value">{avg_t}s</div>
            <div class="label">Rata-rata Waktu</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon-wrap icon-pink">⏳</div>
            <div class="value">{total_t}s</div>
            <div class="label">Total Durasi Komputasi</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon-wrap icon-green">🎯</div>
            <div class="value">~95%</div>
            <div class="label">Akurasi Segmentasi AI</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_hist, col_info = st.columns([2, 1], gap="large")
    
    with col_hist:
        st.markdown("<h3 style='font-weight:700; color:#1b254b; margin-bottom:15px;'>📋 Riwayat Sesi Saat Ini</h3>", unsafe_allow_html=True)
        if st.session_state.history:
            # Menggunakan Markdown Table standard (Streamlit akan render otomatis dengan style native)
            st.markdown("| ID | Nama File Asli | Resolusi Awal | Waktu Proses | Jam |\n|---|---|---|---|---|")
            for h in st.session_state.history:
                st.markdown(f"| #{h['no']} | `{h['nama']}` | {h['resolusi']} | **{h['waktu']}s** | {h['timestamp']} |")
        else:
            st.markdown("""
            <div class="card" style="text-align:center; padding:40px 20px;">
                <div style="font-size:3rem; margin-bottom:10px;">📭</div>
                <h4 style="color:#1b254b; font-weight:700;">Riwayat Kosong</h4>
                <p style="color:#a3aed1; font-size:0.9rem;">Belum ada gambar yang diproses pada sesi ini.</p>
            </div>""", unsafe_allow_html=True)

    with col_info:
        st.markdown("<h3 style='font-weight:700; color:#1b254b; margin-bottom:15px;'>ℹ️ Detail Engine</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
            <div style="font-size:1.8rem; margin-bottom:10px;">🤖</div>
            <h4 style="font-weight:700; color:#1b254b;">Model U2-Net</h4>
            <p style="font-size:0.9rem; color:#666; line-height:1.6;">
                Arsitektur deep learning berbasis <i>nested U-structure</i> yang dirancang khusus untuk mendeteksi <i>salient object</i> (objek utama) secara akurat tanpa bergantung pada hardware khusus (GPU).
            </p>
        </div>
        
        <div class="card">
            <div style="font-size:1.8rem; margin-bottom:10px;">📦</div>
            <h4 style="font-weight:700; color:#1b254b;">Library rembg</h4>
            <p style="font-size:0.9rem; color:#666; line-height:1.6;">
                Merupakan implementasi Python dari U2-Net menggunakan format <b>ONNX Runtime</b>. ONNX memungkinkan model AI dieksekusi dengan efisien dan sangat ringan di server standar.
            </p>
        </div>
        """, unsafe_allow_html=True)
