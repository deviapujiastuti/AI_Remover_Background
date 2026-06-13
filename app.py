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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
}
[data-testid="stSidebar"] * { color: white !important; }
.card {
    background: white; border-radius: 16px; padding: 24px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin-bottom: 20px;
}
.hero {
    background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 60%, #e94560 100%);
    border-radius: 20px; padding: 50px 40px; color: white; text-align: center; margin-bottom: 30px;
}
.hero h1 { font-size: 2.8rem; font-weight: 700; margin: 0; }
.hero p  { font-size: 1.1rem; opacity: 0.85; margin-top: 10px; }
.metric-card {
    background: linear-gradient(135deg, #1a1a2e, #0f3460);
    border-radius: 14px; padding: 20px; color: white; text-align: center;
}
.metric-card .value { font-size: 2rem; font-weight: 700; color: #e94560; }
.metric-card .label { font-size: 0.85rem; opacity: 0.8; margin-top: 4px; }
.stButton > button {
    background: linear-gradient(135deg, #e94560, #0f3460) !important;
    color: white !important; border: none !important; border-radius: 10px !important;
    font-weight: 600 !important; width: 100%;
}
.result-box {
    background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
    border-left: 4px solid #4caf50; border-radius: 10px; padding: 16px 20px; margin: 10px 0;
}
.info-box {
    background: linear-gradient(135deg, #e3f2fd, #ede7f6);
    border-left: 4px solid #1a73e8; border-radius: 10px; padding: 16px 20px; margin: 10px 0;
}
.tag {
    display: inline-block; background: #e8eaf6; color: #3949ab;
    border-radius: 20px; padding: 4px 14px; font-size: 13px; font-weight: 600; margin: 4px;
}
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []
if "total_processed" not in st.session_state:
    st.session_state.total_processed = 0
if "total_time" not in st.session_state:
    st.session_state.total_time = 0.0

with st.sidebar:
    st.markdown("## ✂️ Background Remover")
    st.markdown("---")
    page = st.radio("Navigasi", ["🏠  Beranda", "🖼️  Hapus Background", "📊  Dashboard"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**👩‍💻 Mahasiswa**")
    st.markdown("Devia Puji Astuti")
    st.markdown("2311531005")
    st.markdown("Informatika 23")
    st.markdown("---")
    st.markdown("**🤖 Model:** U2-Net via `rembg`")
    st.markdown(" Stack: Python · Streamlit · PIL")

# ── BERANDA ──
if page == "🏠  Beranda":
    st.markdown("""
    <div class="hero">
        <h1>✂️ AI Background Remover</h1>
        <p>Hapus latar belakang gambar secara otomatis menggunakan kecerdasan buatan.<br>
        Didukung model deep learning <strong>U2-Net</strong> — cepat, akurat, tanpa edit manual.</p>
    </div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card"><div class="value">U2-Net</div><div class="label">Model AI yang digunakan</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><div class="value">PNG</div><div class="label">Format output transparan</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><div class="value">~3 dtk</div><div class="label">Rata-rata waktu proses</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📌 Tentang Aplikasi")
    st.markdown("""<div class="card">
        Aplikasi ini merupakan implementasi dari proyek <b>Image Processing</b> yang menggunakan model deep learning
        <b>U2-Net</b> untuk melakukan segmentasi otomatis antara objek utama (foreground) dan latar belakang (background).
        Output berupa gambar <b>PNG transparan</b> siap digunakan untuk keperluan desain grafis dan katalog produk.
    </div>""", unsafe_allow_html=True)

    st.markdown("### 🚀 Cara Menggunakan")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="card" style="text-align:center"><div style="font-size:2.5rem">📁</div><b>1. Upload Gambar</b><p style="font-size:13px;color:#666;margin-top:8px">Upload foto JPG atau PNG</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card" style="text-align:center"><div style="font-size:2.5rem">🤖</div><b>2. Proses AI</b><p style="font-size:13px;color:#666;margin-top:8px">Model U2-Net memproses gambar</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="card" style="text-align:center"><div style="font-size:2.5rem">⬇️</div><b>3. Download</b><p style="font-size:13px;color:#666;margin-top:8px">Download PNG transparan</p></div>', unsafe_allow_html=True)

    st.markdown("""
    <span class="tag">Python 3.8+</span><span class="tag">rembg</span>
    <span class="tag">U2-Net</span><span class="tag">Pillow</span>
    <span class="tag">Streamlit</span><span class="tag">ONNX Runtime</span>
    """, unsafe_allow_html=True)

# ── HAPUS BACKGROUND ──
elif page == "🖼️  Hapus Background":
    st.markdown("## 🖼️ Hapus Background Gambar")
    uploaded_file = st.file_uploader("Pilih gambar (JPG / PNG)", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        input_image = Image.open(uploaded_file)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📷 Gambar Asli")
            st.image(input_image, use_column_width=True)
            st.markdown(f"""<div class="info-box">
                 <b>Nama file:</b> {uploaded_file.name}<br>
                 <b>Resolusi:</b> {input_image.width} × {input_image.height} px<br>
                 <b>Mode warna:</b> {input_image.mode}
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("#### ✨ Hasil Deteksi")
            placeholder = st.empty()
            placeholder.info("Klik tombol **Proses Sekarang** untuk memulai.")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Proses Sekarang — Hapus Background"):
            with st.spinner("🤖 Model U2-Net sedang memproses..."):
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
                placeholder.image(output_image, use_column_width=True)
                st.markdown(f"""<div class="result-box">
                    ✅ <b>Background berhasil dihapus!</b><br>
                     <b>Waktu inferensi:</b> {elapsed} detik<br>
                     <b>Format output:</b> PNG transparan<br>
                     <b>Model:</b> U2-Net via rembg
                </div>""", unsafe_allow_html=True)

            buf = io.BytesIO()
            output_image.save(buf, format="PNG")
            st.download_button("⬇️ Download Hasil PNG", data=buf.getvalue(),
                file_name=f"bg_removed_{uploaded_file.name.split('.')[0]}.png", mime="image/png")
    else:
        st.markdown('<div class="card" style="text-align:center;padding:40px"><div style="font-size:4rem">📂</div><p style="color:#888">Belum ada gambar yang diupload.</p></div>', unsafe_allow_html=True)

# ── DASHBOARD ──
elif page == "📊  Dashboard":
    st.markdown("## 📊 Dashboard Statistik")
    total = st.session_state.total_processed
    avg_t = round(st.session_state.total_time / total, 2) if total > 0 else 0
    total_t = round(st.session_state.total_time, 2)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="value">{total}</div><div class="label">Total Gambar Diproses</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="value">{avg_t}s</div><div class="label">Rata-rata Waktu Inferensi</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="value">{total_t}s</div><div class="label">Total Waktu Proses</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><div class="value">~95%</div><div class="label">Akurasi Model U2-Net</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📋 Riwayat Pengujian")
    if st.session_state.history:
        st.markdown("| No | Nama File | Resolusi | Waktu | Jam |\n|----|-----------|----------|-------|-----|")
        for h in st.session_state.history:
            st.markdown(f"| {h['no']} | {h['nama']} | {h['resolusi']} | {h['waktu']}s | {h['timestamp']} |")
    else:
        st.markdown('<div class="card" style="text-align:center;padding:30px"><div style="font-size:3rem">📭</div><p style="color:#888">Belum ada data. Proses gambar dulu di halaman Hapus Background.</p></div>', unsafe_allow_html=True)

    st.markdown("### ℹ️ Informasi Model")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><b>🤖 Model AI</b><br><span class="tag">U2-Net</span><br><br>U2-Net adalah arsitektur deep learning berbasis nested U-structure untuk segmentasi salient object secara akurat.</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><b>📦 Library</b><br><span class="tag">rembg</span> <span class="tag">Pillow</span> <span class="tag">ONNX Runtime</span><br><br>Library rembg mengimplementasikan U2-Net dalam format ONNX, berjalan tanpa GPU khusus.</div>', unsafe_allow_html=True)
