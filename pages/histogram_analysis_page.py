import streamlit as st
import matplotlib.pyplot as plt
import io
from utils.histogram_helper import compute_histogram
from utils.preview_helper import get_preview_image

@st.dialog("Histogram Analysis Comparison", width="large")
def render_histogram_analysis_popup():
    # --- CSS SAKTI: FORCE HEIGHT AUTO DAN BLOCK DI SEMUA LAYER ---
    st.markdown("""
    <style>
    div[data-testid="stDialog"] > div:first-child {
        width: 80vw !important;
        max-width: 950px !important;
        min-width: 700px !important;
        left: 0 !important;
        right: 0 !important;
        
        margin: -50px auto 0 auto !important; 
        
        background-color: #1E1E24 !important; 
        border-radius: 12px !important;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5) !important;
        display: block !important;
        height: auto !important;
        min-height: unset !important;
        max-height: none !important;
    }

    /* Layer Internal Dialog */
    div[role="dialog"] {
        background: transparent !important;
        border: none !important;
        display: block !important;
        height: auto !important;
        min-height: unset !important;
    }
    
    div[role="dialog"] [data-testid="stVerticalBlock"] {
        display: block !important;
        height: auto !important;
        min-height: unset !important;
        gap: 0px !important;
        padding: 0px 10px 10px 0px !important; 
    }

    /* Rapatkan Judul Utama internal */
    div[data-testid="stDialog"] h2 {
        color: #ffffff !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        margin-top: 0px !important;  
        margin-bottom: 0px !important; 
    }
    
    /* Container subtitle internal */
    div[data-testid="stDialog"] div[data-testid="stMarkdownContainer"] {
        margin-top: -4px !important; 
    }

    /* Tombol close (X) */
    div[data-testid="stDialog"] button[p-aria-label="Close"] svg {
        fill: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Subtitle deskripsi teks atas
    st.markdown("<div style='font-size: 0.85rem; color: #A4A4AA; margin-bottom: 20px;'>Compare pixel intensity distribution between Original Baseline and Processed Pipeline.</div>", unsafe_allow_html=True)

    # 1. Hitung data histogram secara aman
    orig_hist = None
    if st.session_state.original_image is not None:
        orig_hist = compute_histogram(st.session_state.original_image)
        
    proc_image = get_preview_image()
    proc_hist = None
    if proc_image is not None:
        proc_hist = compute_histogram(proc_image)

    # 2. GENERATE GRAFIK MATPLOTLIB DENGAN UKURAN PAS
    # Grafik Kiri (Before)
    if orig_hist is not None:
        fig1, ax1 = plt.subplots(figsize=(4.5, 2.5))
        ax1.bar(range(256), orig_hist, width=1.0, color='#1D1D1F', alpha=0.8)
        ax1.set_xlim(0, 255)
        ax1.set_title("Original Histogram (Before)", fontsize=9, fontweight='bold')
        ax1.grid(True, linestyle='--', alpha=0.2)
        plt.tight_layout()
        
        buf1 = io.BytesIO()
        plt.savefig(buf1, format='png', dpi=150)
        buf1.seek(0)
        st.session_state.hist_img_before = buf1.getvalue()
        plt.close(fig1)

    # Grafik Kanan (After)
    if proc_hist is not None:
        fig2, ax2 = plt.subplots(figsize=(4.5, 2.5))
        ax2.bar(range(256), proc_hist, width=1.0, color='#0071E3', alpha=0.8)
        ax2.set_xlim(0, 255)
        ax2.set_title("Processed Histogram (After)", fontsize=9, fontweight='bold')
        ax2.grid(True, linestyle='--', alpha=0.2)
        plt.tight_layout()
        
        buf2 = io.BytesIO()
        plt.savefig(buf2, format='png', dpi=150)
        buf2.seek(0)
        st.session_state.hist_img_after = buf2.getvalue()
        plt.close(fig2)

    # --- 3. DISPLAY BERDAMPINGAN MENGGUNAKAN FLEXBOX ---
    import base64
    b64_before = base64.b64encode(st.session_state.hist_img_before).decode('utf-8') if orig_hist is not None else ""
    b64_after = base64.b64encode(st.session_state.hist_img_after).decode('utf-8') if proc_hist is not None else ""

    st.markdown(f"""
    <div style="display: flex; flex-direction: row; justify-content: space-between; align-items: center; width: 100%; gap: 15px; margin-top: 5px;">
        <div style="flex: 1; width: 50%; background: #ffffff; border-radius: 8px; padding: 5px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
            {f'<img src="data:image/png;base64,{b64_before}" style="width: 100%; height: auto; display: block;">' if b64_before else '<p style="text-align:center;font-size:0.8rem;color:#86868B;">Original Asset Missing</p>'}
        </div>
        <div style="flex: 1; width: 50%; background: #ffffff; border-radius: 8px; padding: 5px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
            {f'<img src="data:image/png;base64,{b64_after}" style="width: 100%; height: auto; display: block;">' if b64_after else '<p style="text-align:center;font-size:0.8rem;color:#86868B;">Processed Asset Missing</p>'}
        </div>
    </div>
    """, unsafe_allow_html=True)