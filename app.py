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
    st.markdown('<div class="sidebar-title">✨ Mini Photoshop</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Digital Image Processing</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="nav-item-container">', unsafe_allow_html=True)
    
    nav_items = [
        ("Image Enhancement", "🎨"),
        ("Geometric Transformation", "📐"),
        ("Image Restoration", "🩹"),
        ("Binary & Edge Processing", "⬛"),
        ("Color Processing", "🌈"),
        ("Image Segmentation", "✂️")
    ]
    
    for page_name, icon in nav_items:
        is_active = st.session_state.current_page == page_name
        active_class = "active" if is_active else ""
        
        # We use a native button inside a container to get click events
        # Streamlit's native button is styled to look like our custom nav via CSS
        if st.button(f"{icon}  {page_name}", key=f"nav_{page_name}", use_container_width=True):
            set_page(page_name)
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Active Image Badge
    if st.session_state.original_image is not None:
        h, w = st.session_state.original_image.shape[:2]
        st.markdown(f"""
        <div style="margin-top: 2rem; padding: 1rem; background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 8px;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; font-weight: 600; margin-bottom: 0.25rem;">Active Image</div>
            <div style="font-size: 0.9rem; color: #F1F5F9; font-weight: 500;">{w} × {h} px</div>
        </div>
        """, unsafe_allow_html=True)

# --- MAIN CONTENT ---
menu = st.session_state.current_page
icon_map = {name: icon for name, icon in nav_items}
st.title(f"{icon_map[menu]} {menu}")

# 1. IMAGE ENHANCEMENT PAGE
if menu == "Image Enhancement":
    render_image_enhancement_page()

# 2. GEOMETRIC TRANSFORMATION PAGE
elif menu == "Geometric Transformation":
    render_geometric_transformation_page()

# 3. IMAGE RESTORATION PAGE
elif menu == "Image Restoration":
    render_image_restoration_page()

# 4. BINARY & EDGE PROCESSING PAGE
elif menu == "Binary & Edge Processing":
    render_binary_edge_processing_page()

# 5. COLOR PROCESSING PAGE
elif menu == "Color Processing":
    render_color_processing_page()

# 6. IMAGE SEGMENTATION PAGE
elif menu == "Image Segmentation":
    render_image_segmentation_page()