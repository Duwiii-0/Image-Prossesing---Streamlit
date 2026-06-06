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

from utils.state_manager import init_session_state, reset_all_state
from utils.ui_helpers import load_css, render_reset_and_save_buttons, render_image_preview
from utils.preview_helper import get_preview_image

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Mini Photoshop",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load custom CSS
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
        ("Image Segmentation", "")
    ]
    
    # Navigation Buttons
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
# We use two main columns: Stage (Center) and Inspector (Right)
col_stage, col_inspector = st.columns([3, 1], gap="small")

with col_stage:
    if st.session_state.original_image is None:
        # Empty State for Stage
        st.markdown("""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; color: #86868B; background: #EEEEF0; padding: 3rem;">
            <div style="font-size: 3rem; margin-bottom: 1.5rem; opacity: 0.3;">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                    <circle cx="8.5" cy="8.5" r="1.5"></circle>
                    <polyline points="21 15 16 10 5 21"></polyline>
                </svg>
            </div>
            <div style="font-size: 1.25rem; font-weight: 600; color: #1D1D1F; margin-bottom: 0.5rem;">No Image Selected</div>
            <div style="font-size: 0.85rem; max-width: 300px; text-align: center;">Upload an image from the inspector panel on the right to begin editing.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # --- IMAGE PREVIEW IN STAGE (SINGLE OUTPUT ONLY) ---
        preview_image = get_preview_image()
        # Create a "focus" layout with padding columns to shrink the image
        col_p1, col_focus, col_p2 = st.columns([1, 2, 1])
        with col_focus:
            st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
            st.image(preview_image, use_container_width=True)

with col_inspector:
    # 0. IMAGE UPLOAD SECTION
    st.markdown('<span class="section-label">Import Asset</span>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png", "bmp"], label_visibility="collapsed")
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        if image.mode == 'RGBA': image = image.convert('RGB')
        img_array = np.array(image)
        if st.session_state.original_image is None or not np.array_equal(st.session_state.original_image, img_array):
            st.session_state.original_image = img_array
            st.session_state.processed_image = img_array.copy()
            st.rerun()

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # 1. PAGE-SPECIFIC CONTROLS (NOW IN INSPECTOR)
    if st.session_state.original_image is not None:
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
        
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # 2. GLOBAL EXPORT SECTION
    st.markdown('<span class="section-label">Export</span>', unsafe_allow_html=True)
    if st.session_state.processed_image is not None:
        export_format = st.selectbox("Format", ["PNG", "JPEG", "BMP"], key="global_export_fmt")
        export_name = st.text_input("Filename", value="edited_studio", key="global_export_name")
        
        # Prepare image for download
        res_pil = Image.fromarray(st.session_state.processed_image)
        buf = io.BytesIO()
        
        if export_format == "PNG":
            res_pil.save(buf, format="PNG")
            mime = "image/png"
            ext = "png"
        elif export_format == "JPEG":
            if res_pil.mode == 'RGBA': res_pil = res_pil.convert('RGB')
            res_pil.save(buf, format="JPEG", quality=95)
            mime = "image/jpeg"
            ext = "jpg"
        else:
            res_pil.save(buf, format="BMP")
            mime = "image/bmp"
            ext = "bmp"
            
        st.download_button(
            label=f"Download {export_format}",
            data=buf.getvalue(),
            file_name=f"{export_name}.{ext}",
            mime=mime,
            type="primary",
            use_container_width=True
        )
    else:
        st.info("Upload image to enable export")

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # 3. SESSION CONTROL
    st.markdown('<span class="section-label">Workspace</span>', unsafe_allow_html=True)
    if st.button("Reset All Settings", use_container_width=True):
        reset_all_state()
        if st.session_state.original_image is not None:
            st.session_state.processed_image = st.session_state.original_image.copy()
        st.rerun()

    if st.session_state.original_image is not None:
        h, w = st.session_state.original_image.shape[:2]
        st.markdown(f"""
        <div style="margin-top: 1rem; padding: 16px; background: #F5F5F7; border-radius: 8px; border: 1px solid rgba(0,0,0,0.03);">
            <div style="font-size: 0.65rem; color: #86868B; font-weight: 700; text-transform: uppercase; margin-bottom: 8px;">Metadata</div>
            <div style="font-size: 0.9rem; font-weight: 600;">{w} × {h} px</div>
            <div style="font-size: 0.75rem; color: #86868B; margin-top: 4px;">Color Space: RGB</div>
        </div>
        """, unsafe_allow_html=True)