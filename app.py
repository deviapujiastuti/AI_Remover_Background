import streamlit as st
from rembg import remove
from PIL import Image
import io
import time
import datetime

# Harus menjadi perintah Streamlit pertama
st.set_page_config(
    page_title="AI Background Remover",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== STATE MANAGEMENT ====================
if "welcomed" not in st.session_state:
    st.session_state.welcomed = False
if "history" not in st.session_state:
    st.session_state.history = []
if "total_processed" not in st.session_state:
    st.session_state.total_processed = 0
if "total_time" not in st.session_state:
    st.session_state.total_time = 0.0

# ==================== SPLASH SCREEN ====================
if not st.session_state.welcomed:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stSidebar"] { display: none !important; } /* Sembunyikan sidebar di splash screen */
    
    .stApp {
        background-color: #0b1437;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .splash-container {
        text-align: center;
        font-family: 'Plus Jakarta Sans', sans-serif;
        animation: fadeInOut 3s ease-in-out forwards;
        margin-top: 20vh;
    }
    
    .splash-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #7F00FF 0%, #E100FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
    }
    
    .splash-subtitle {
        color: #a3aed1;
        font-size: 1.2rem;
        font-weight: 400;
    }
    
    @keyframes fadeInOut {
        0% { opacity: 0; transform: scale(0.95); }
        20% { opacity: 1; transform: scale(1); }
        80% { opacity: 1; transform: scale(1); }
        100% { opacity: 0; transform: scale(1.05); }
    }
    </style>
    
    <div class="splash-container">
        <div class="splash-title">AI Background Remover</div>
        <div class="splash-subtitle">Selamat datang! Mempersiapkan workspace Anda...</div>
    </div>
    """, unsafe_allow_html=True)
    
    time.sleep(3) # Tahan selama 3 detik
    st.session_state.welcomed = True
    st.rerun()

# ==================== MAIN APPLICATION ====================
else:
    # ==================== THEME MANAGEMENT ====================
    with st.sidebar:
        st.markdown("""
        <div style="margin-bottom:20px;">
            <h2 style="margin:0; font-weight:800; font-size:1.6rem; color:inherit; font-family:'Plus Jakarta Sans', sans-serif;">
                AI Remover.
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        tema = st.radio("Theme:", ["Light Mode", "Dark Mode"], horizontal=True)

    # Konfigurasi Warna Berdasarkan Tema
    if tema == "Light Mode":
        bg_app = "#f4f7fe"
        text_main = "#1b254b"
        text_muted = "#707ea9"
        card_bg = "rgba(255, 255, 255, 0.85)"
        card_border = "rgba(255, 255, 255, 0.5)"
        sidebar_bg = "#ffffff"
        sidebar_border = "#e0e5f2"
        box_bg = "#ffffff"
        dropzone_bg = "rgba(255, 255, 255, 0.6)"
        highlight = "#F4EEFF"
    else:
        bg_app = "#0b1437"
        text_main = "#ffffff"
        text_muted = "#a3aed1"
        card_bg = "rgba(17, 28, 68, 0.75)"
        card_border = "rgba(255, 255, 255, 0.08)"
        sidebar_bg = "#0b1437"
        sidebar_border = "rgba(255, 255, 255, 0.1)"
        box_bg = "#111c44"
        dropzone_bg = "rgba(17, 28, 68, 0.8)"
        highlight = "rgba(127, 0, 255, 0.2)"

    # ==================== ADVANCED DYNAMIC STYLING ====================
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    * {{ font-family: 'Plus Jakarta Sans', sans-serif; }}

    .stApp {{ background-color: {bg_app} !important; }}
    .text-main, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, p, span, div {{ color: {text_main}; }}
    .text-muted {{ color: {text_muted} !important; }}
    #MainMenu, footer, header {{ visibility: hidden; }}
    .block-container {{ padding-top: 2rem !important; }}

    /* Hero */
    .hero {{
        background: linear-gradient(135deg, #7F00FF 0%, #E100FF 100%);
        border-radius: 24px; padding: 3rem 2rem; text-align: center; margin-bottom: 2rem;
        position: relative; overflow: hidden; box-shadow: 0 20px 40px rgba(127, 0, 255, 0.2);
    }}
    .hero h1, .hero p {{ color: white !important; position: relative; z-index: 1; }}
    .hero h1 {{ font-size: 3rem; font-weight: 800; margin: 0; letter-spacing: -0.02em; }}
    .hero p {{ font-size: 1.1rem; opacity: 0.9; margin-top: 15px; }}

    /* Cards */
    .custom-card {{
        background: {card_bg}; backdrop-filter: blur(10px);
        border: 1px solid {card_border}; border-radius: 20px; 
        padding: 24px; margin-bottom: 20px; transition: all 0.3s ease;
    }}
    .custom-card:hover {{ transform: translateY(-5px); box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1); }}

    /* Metric Cards */
    .metric-card {{
        background: {box_bg}; border-radius: 20px; padding: 24px;
        border: 1px solid {card_border}; display: flex; flex-direction: column; transition: transform 0.3s;
    }}
    .metric-card:hover {{ transform: translateY(-5px); }}
    .metric-card .value {{ font-size: 2.2rem; font-weight: 800; line-height: 1.2; color: {text_main}; }}
    .metric-card .label {{ font-size: 0.9rem; font-weight: 600; margin-top: 5px; color: {text_muted}; }}

    /* Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, #7F00FF 0%, #E100FF 100%) !important;
        color: white !important; border: none !important; border-radius: 12px !important;
        font-weight: 700 !important; padding: 0.8rem 1.5rem !important; width: 100%;
        transition: all 0.3s ease !important;
    }}
    .stButton > button:hover {{ transform: translateY(-3px) !important; box-shadow: 0 10px 20px rgba(127, 0, 255, 0.3) !important; }}
    
    .stDownloadButton > button {{
        background: {box_bg} !important;
        color: {text_main} !important; border: 1px solid {card_border} !important;
    }}

    /* Boxes */
    .result-box {{ background: {highlight}; border-left: 4px solid #7F00FF; border-radius: 12px; padding: 20px; margin: 15px 0; }}
    .info-box {{ background: {box_bg}; border-left: 4px solid #E100FF; border-radius: 12px; padding: 16px 20px; margin: 15px 0; border: 1px solid {card_border}; }}

    /* Sidebar */
    [data-testid="stSidebar"] {{ background: {sidebar_bg} !important; border-right: 1px solid {sidebar_border} !important; }}
    .sidebar-profile {{
        background: linear-gradient(135deg, #7F00FF 0%, #E100FF 100%);
        border-radius: 16px; padding: 20px; margin-bottom: 20px;
    }}
    .sidebar-profile *, .sidebar-profile p, .sidebar-profile h3 {{ color: white !important; }}
    .sidebar-profile h3 {{ margin: 0 0 10px 0; font-size: 1.2rem; font-weight: 700; }}
    .sidebar-profile p {{ margin: 2px 0; font-size: 0.9rem; opacity: 0.9; }}

    /* File Uploader */
    [data-testid="stFileUploadDropzone"] {{ border: 2px dashed {text_muted} !important; border-radius: 20px !important; background: {dropzone_bg} !important; }}
    [data-testid="stFileUploadDropzone"]:hover {{ border-color: #7F00FF !important; }}
    </style>
    """, unsafe_allow_html=True)

    # ==================== NAVIGATION (SIDEBAR) ====================
    with st.sidebar:
        st.markdown("<hr style='margin:10px 0; border-color:rgba(150,150,150,0.2)'>", unsafe_allow_html=True)
        page = st.radio("Navigation", ["Beranda", "Workspace", "Dashboard"], label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="sidebar-profile">
            <h3>Profil Developer</h3>
            <p><b>Devia Puji Astuti</b></p>
            <p>NPM: 2311531005</p>
            <p>Informatika 23</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="custom-card" style="padding:15px; margin-top:10px;">
            <div class="text-muted" style="font-size:0.85rem; font-weight:600; margin-bottom:8px;">TECH STACK</div>
            <div class="text-main" style="font-size:0.9rem; font-weight:600;">
                U2-Net via rembg<br>
                Python & Streamlit<br>
                PIL & ONNX
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ==================== BERANDA ====================
    if page == "Beranda":
        st.markdown("""
        <div class="hero">
            <h1>Background Remover</h1>
            <p>Hapus latar belakang gambar secara otomatis dalam hitungan detik menggunakan model Deep Learning.<br>
            Ditenagai oleh arsitektur U2-Net untuk hasil segmentasi yang presisi.</p>
        </div>""", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="metric-card">
                <div class="value">U2-Net</div>
                <div class="label">Arsitektur AI Model</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="metric-card">
                <div class="value">PNG</div>
                <div class="label">Format Output Transparan</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="metric-card">
                <div class="value">~3s</div>
                <div class="label">Rata-rata Kecepatan Proses</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<h3 class='text-main' style='margin-top:30px; font-weight:700;'>Cara Menggunakan</h3>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="custom-card" style="padding:30px 20px;">
                <h1 style="color:#7F00FF; font-size:2.5rem; margin:0 0 10px 0; font-weight:800;">01</h1>
                <h3 class="text-main" style="font-size:1.2rem; font-weight:700; margin-bottom:10px;">Upload File</h3>
                <p class="text-muted" style="font-size:0.9rem;">Unggah foto dengan format JPG atau PNG ke dalam sistem workspace.</p>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="custom-card" style="padding:30px 20px;">
                <h1 style="color:#7F00FF; font-size:2.5rem; margin:0 0 10px 0; font-weight:800;">02</h1>
                <h3 class="text-main" style="font-size:1.2rem; font-weight:700; margin-bottom:10px;">AI Processing</h3>
                <p class="text-muted" style="font-size:0.9rem;">Sistem AI akan mengeksekusi dan memisahkan objek utama dari background.</p>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="custom-card" style="padding:30px 20px;">
                <h1 style="color:#7F00FF; font-size:2.5rem; margin:0 0 10px 0; font-weight:800;">03</h1>
                <h3 class="text-main" style="font-size:1.2rem; font-weight:700; margin-bottom:10px;">Download Hasil</h3>
                <p class="text-muted" style="font-size:0.9rem;">Simpan dan gunakan gambar berformat PNG transparan Anda.</p>
            </div>""", unsafe_allow_html=True)

    # ==================== HAPUS BACKGROUND (WORKSPACE) ====================
    elif page == "Workspace":
        st.markdown("<h2 class='text-main' style='font-weight:800; margin-bottom:20px;'>Workspace Area</h2>", unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Upload Gambar (JPG / PNG)", type=["jpg", "jpeg", "png"])

        if uploaded_file:
            input_image = Image.open(uploaded_file)
            col1, col2 = st.columns(2, gap="large")
            
            with col1:
                st.markdown("<h4 class='text-main' style='font-weight:700; margin-bottom:15px;'>Gambar Original</h4>", unsafe_allow_html=True)
                st.image(input_image, use_column_width=True, output_format="auto")
                
                st.markdown(f"""
                <div class="info-box">
                    <div class="text-muted" style="font-size:0.85rem; font-weight:700; margin-bottom:5px;">FILE INFO</div>
                    <b class="text-main">Nama File:</b> <span class="text-main">{uploaded_file.name}</span><br>
                    <b class="text-main">Resolusi:</b> <span class="text-main">{input_image.width} × {input_image.height} px</span><br>
                    <b class="text-main">Warna:</b> <span class="text-main">{input_image.mode}</span>
                </div>""", unsafe_allow_html=True)
                
            with col2:
                st.markdown("<h4 class='text-main' style='font-weight:700; margin-bottom:15px;'>Hasil Transparan</h4>", unsafe_allow_html=True)
                placeholder = st.empty()
                placeholder.markdown(f"""
                <div class="custom-card" style="text-align:center; padding:60px 20px; border:2px dashed {text_muted};">
                    <h4 class="text-main" style="font-weight:700; margin-bottom:10px;">Gambar Siap Diproses</h4>
                    <p class="text-muted" style="font-size:0.9rem;">Klik tombol proses di bawah ini.</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            
            _, btn_col, _ = st.columns([1,2,1])
            with btn_col:
                if st.button("Proses Gambar Sekarang", use_container_width=True):
                    with st.spinner("AI sedang menganalisis gambar..."):
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
                        st.markdown(f"""
                        <div class="result-box">
                            <b style="font-size:1.1rem;" class="text-main">Proses Selesai!</b>
                            <div class="text-main" style="font-size:0.9rem; margin-top:8px;">
                                Waktu Eksekusi: {elapsed} detik<br>
                                Resolusi Output: Sama dengan original
                            </div>
                        </div>""", unsafe_allow_html=True)

                    buf = io.BytesIO()
                    output_image.save(buf, format="PNG")
                    
                    with btn_col:
                        st.download_button("Download Hasil (.PNG)", data=buf.getvalue(),
                            file_name=f"nobg_{uploaded_file.name.split('.')[0]}.png", mime="image/png")
        else:
            st.markdown(f"""
            <div class="custom-card" style="text-align:center; padding:80px 20px; border:2px dashed {text_muted}; background:transparent;">
                <h3 class="text-main" style="font-weight:700; margin-bottom:10px;">Area Kerja Kosong</h3>
                <p class="text-muted">Silahkan unggah gambar terlebih dahulu pada uploader di atas.</p>
            </div>""", unsafe_allow_html=True)

    # ==================== DASHBOARD ====================
    elif page == "Dashboard":
        st.markdown("<h2 class='text-main' style='font-weight:800; margin-bottom:20px;'>Dashboard Statistik</h2>", unsafe_allow_html=True)
        
        total = st.session_state.total_processed
        avg_t = round(st.session_state.total_time / total, 2) if total > 0 else 0
        total_t = round(st.session_state.total_time, 2)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="value">{total}</div>
                <div class="label">Gambar Diproses</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="value">{avg_t}s</div>
                <div class="label">Rata-rata Waktu</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="value">{total_t}s</div>
                <div class="label">Total Durasi Proses</div>
            </div>""", unsafe_allow_html=True)
        with col4:
            st.markdown("""
            <div class="metric-card">
                <div class="value">~95%</div>
                <div class="label">Estimasi Akurasi AI</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        col_hist, col_info = st.columns([2, 1], gap="large")
        
        with col_hist:
            st.markdown("<h3 class='text-main' style='font-weight:700; margin-bottom:15px;'>Riwayat Sesi Saat Ini</h3>", unsafe_allow_html=True)
            if st.session_state.history:
                st.markdown("| ID | Nama File | Resolusi | Durasi | Waktu |\n|---|---|---|---|---|")
                for h in st.session_state.history:
                    st.markdown(f"| {h['no']} | `{h['nama']}` | {h['resolusi']} | **{h['waktu']}s** | {h['timestamp']} |")
            else:
                st.markdown(f"""
                <div class="custom-card" style="text-align:center; padding:40px 20px;">
                    <h4 class="text-main" style="font-weight:700; margin-bottom:10px;">Riwayat Masih Kosong</h4>
                    <p class="text-muted" style="font-size:0.9rem;">Belum ada gambar yang diproses pada sesi ini.</p>
                </div>""", unsafe_allow_html=True)

        with col_info:
            st.markdown("<h3 class='text-main' style='font-weight:700; margin-bottom:15px;'>Informasi Sistem</h3>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="custom-card">
                <h4 class="text-main" style="font-weight:700; margin-bottom:10px;">Model U2-Net</h4>
                <p class="text-muted" style="font-size:0.9rem; line-height:1.6;">
                    Arsitektur deep learning berbasis <i>nested U-structure</i> yang dirancang untuk mendeteksi <i>salient object</i> secara presisi tanpa bergantung hardware GPU berat.
                </p>
            </div>
            
            <div class="custom-card">
                <h4 class="text-main" style="font-weight:700; margin-bottom:10px;">Format ONNX Runtime</h4>
                <p class="text-muted" style="font-size:0.9rem; line-height:1.6;">
                    Implementasi standar AI yang memungkinkan model dieksekusi secara optimal, efisien, dan ringan pada server standar.
                </p>
            </div>
            """, unsafe_allow_html=True)
