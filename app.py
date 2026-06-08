import streamlit as st
import numpy as np
import cv2
from PIL import Image
import io

from pages.image_enhancement_page import render_image_enhancement_page
from pages.geometric_transformation_page import render_geometric_transformation_page
from pages.image_restoration_page import render_image_restoration_page
from pages.binary_edge_processing_page import render_binary_edge_processing_page
from pages.color_processing_page import render_color_processing_page
from pages.image_segmentation_page import render_image_segmentation_page
from pages.image_compression_page import render_image_compression_page
from pages.laptop_detection_page import render_laptop_detection_page

from utils.state_manager import init_session_state, reset_all_state
from utils.ui_helpers import load_css
from utils.preview_helper import get_preview_image

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Studio Pro",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load custom CSS (Injects Tailwind & Custom Styles)
load_css()

# Initialize all session state
init_session_state()

# Navigation state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Image Enhancement"

def set_page(page_name):
    st.session_state.current_page = page_name

# --- SIDEBAR (NAVIGATION ONLY) ---
with st.sidebar:
    st.markdown('<div class="sidebar-title">Studio Pro</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Professional Imaging</div>', unsafe_allow_html=True)
    st.markdown('<span class="section-label">Tools</span>', unsafe_allow_html=True)
    
    nav_items = [
        ("Image Enhancement", ""),
        ("Geometric Transformation", ""),
        ("Image Restoration", ""),
        ("Binary & Edge Processing", ""),
        ("Color Processing", ""),
        ("Image Segmentation", ""),
        ("Image Compression", ""),
        ("Laptop AI Studio", "")
    ]
    
    for page_name, icon in nav_items:
        is_active = st.session_state.current_page == page_name
        if st.button(page_name, key=f"nav_{page_name}", use_container_width=True, type="primary" if is_active else "secondary"):
            set_page(page_name)
            st.rerun()

# --- TOP BAR ---
st.markdown(f"""
<div class="top-bar">
    <div style="font-weight: 700; font-size: 0.9rem; color: #1D1D1F; margin-right: 2rem;">Studio Pro v2</div>
    <div style="color: #86868B; font-size: 0.8rem; border-left: 1px solid rgba(0,0,0,0.1); padding-left: 1.5rem;">
        Editing: <span style="color: #1D1D1F; font-weight: 500;">{st.session_state.current_page}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- MAIN LAYOUT ---
if st.session_state.current_page == "Laptop AI Studio":
    render_laptop_detection_page()
    st.stop()

col_stage, col_inspector = st.columns([3, 1], gap="small")

# 1. MIDDLE PART (STAGE)
with col_stage:
    if st.session_state.original_image is None:
        st.markdown("""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 80vh; color: #86868B; background: #E5E5EA; padding: 3rem; border-radius: 12px; margin-top: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 1.5rem; opacity: 0.3;">🖼️</div>
            <div style="font-size: 1.25rem; font-weight: 600; color: #1D1D1F; margin-bottom: 0.5rem;">No Image Selected</div>
            <div style="font-size: 0.85rem; max-width: 300px; text-align: center;">Upload an image from the inspector panel on the right to begin.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Output Preview
        preview_image = get_preview_image()
        st.image(preview_image, use_container_width=False)

        # Convert original image to base64 for floating thumbnail
        import base64
        h, w = st.session_state.original_image.shape[:2]
        img_pil = Image.fromarray(st.session_state.original_image)
        buf = io.BytesIO()
        img_pil.save(buf, format="PNG")
        b64_img = base64.b64encode(buf.getvalue()).decode("utf-8")
        
        # Floating Reference Image over the bottom left of the preview
        st.markdown(f"""
        <div style="position: relative; height: 0px; z-index: 1000;">
            <div style="position: absolute; bottom: 0px; left: 0px;
                        background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(10px);
                        padding: 12px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); 
                        width: 240px; border: 1px solid rgba(0,0,0,0.05);">
                <div style="font-size: 0.75rem; color: #86868B; margin-bottom: 6px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">Original Asset</div>
                <img src="data:image/png;base64,{b64_img}" style="width: 100%; border-radius: 8px; border: 1px solid rgba(0,0,0,0.1);">
                <div style="font-size: 0.75rem; color: #1D1D1F; margin-top: 6px; text-align: center; font-weight: 500;">{w} × {h} px</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 2. RIGHT BAR (INSPECTOR)
with col_inspector:
    # 0. IMPORT ASSET
    st.markdown('<span class="section-label">Import Asset</span>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png", "bmp"], label_visibility="collapsed", key="main_uploader_final")
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        if image.mode == 'RGBA': image = image.convert('RGB')
        img_array = np.array(image)
        if st.session_state.original_image is None or not np.array_equal(st.session_state.original_image, img_array):
            st.session_state.original_image = img_array
            st.session_state.processed_image = img_array.copy()
            st.rerun()

    if st.session_state.original_image is not None:
        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        
        # 1. WORKSPACE (RESET)
        st.markdown('<span class="section-label">Workspace</span>', unsafe_allow_html=True)
        if st.button("Reset All Settings", use_container_width=True, key="reset_all_global"):
            reset_all_state()
            st.session_state.processed_image = st.session_state.original_image.copy()
            st.rerun()
            
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)



        # 3. TOOL SETTINGS (CONTROLS ONLY)
        st.markdown('<span class="section-label">Tool Settings</span>', unsafe_allow_html=True)
        if st.session_state.current_page == "Image Enhancement":
            render_image_enhancement_page()
        elif st.session_state.current_page == "Geometric Transformation":
            render_geometric_transformation_page()
        elif st.session_state.current_page == "Image Restoration":
            render_image_restoration_page()
        elif st.session_state.current_page == "Binary & Edge Processing":
            render_binary_edge_processing_page()
        elif st.session_state.current_page == "Color Processing":
            render_color_processing_page()
        elif st.session_state.current_page == "Image Segmentation":
            render_image_segmentation_page()
        elif st.session_state.current_page == "Image Compression":
            render_image_compression_page()
        
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

        # 4. EXPORT
        st.markdown('<span class="section-label">Export</span>', unsafe_allow_html=True)
        export_format = st.selectbox("Format", ["PNG", "JPEG", "BMP"], key="export_fmt_final")
        export_name = st.text_input("Filename", value="edited_studio", key="export_name_final")
        
        if st.session_state.processed_image is not None:
            res_pil = Image.fromarray(st.session_state.processed_image)
            buf = io.BytesIO()
            if export_format == "PNG":
                res_pil.save(buf, format="PNG")
                mime, ext = "image/png", "png"
            elif export_format == "JPEG":
                if res_pil.mode == 'RGBA': res_pil = res_pil.convert('RGB')
                res_pil.save(buf, format="JPEG", quality=95)
                mime, ext = "image/jpeg", "jpg"
            else:
                res_pil.save(buf, format="BMP")
                mime, ext = "image/bmp", "bmp"
                
            st.download_button(
                label=f"Download {export_format}",
                data=buf.getvalue(),
                file_name=f"{export_name}.{ext}",
                mime=mime,
                type="primary",
                use_container_width=True,
                key="download_btn_final"
            )
        else:
            st.info("No processed image to export.")
    else:
        st.info("Upload an image to start")
