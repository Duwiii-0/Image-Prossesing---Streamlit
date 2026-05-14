import streamlit as st
import pandas as pd
import numpy as np
import cv2
from PIL import Image
import io

from pages.image_enhancement_page import render_image_enhancement_page
from pages.geometric_transformation_page import render_geometric_transformation_page
from pages.image_restoration_page import render_image_restoration_page
from pages.binary_edge_processing_page import render_binary_edge_processing_page

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

# --- SIDEBAR (NAVIGATION ONLY) ---
with st.sidebar:
    st.markdown('<div class="sidebar-title">Mini Photoshop</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Digital Image Processing</div>', unsafe_allow_html=True)
    
    menu = st.radio(
        "Navigasi",
        ["Image Management", "Image Enhancement", "Geometric Transformation", "Image Restoration", "Binary & Edge Processing"],
        label_visibility="collapsed"
    )

# --- MAIN CONTENT ---
st.title(menu)

# 1. IMAGE MANAGEMENT PAGE
if menu == "Image Management":
    st.markdown("Upload local images to begin editing or export your modified assets.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Upload File component
    uploaded_file = st.file_uploader("Select an Image (JPG, PNG, BMP)", type=["jpg", "png", "jpeg", "bmp"])
    
    if uploaded_file is not None:
        # Read image as PIL
        image = Image.open(uploaded_file).convert('RGB')
        image_np = np.array(image)
        
        st.session_state.original_image = image_np.copy()
        st.session_state.processed_image = image_np.copy()
        
        # Reset semua state ke default
        reset_all_state()
            
    if st.session_state.processed_image is not None:
        
        # Render final image using preview helper
        final_image = get_preview_image()

        if final_image is None:
            st.error("Image processing failed")
            st.stop()

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Render reset and save buttons
        render_reset_and_save_buttons(
            reset_callback=lambda: reset_all_state(),
            image_to_save=final_image
        )
            
        st.markdown("<hr style='margin: 2rem 0; border: none; border-top: 1px solid #E2E8F0;' />", unsafe_allow_html=True)
        
        # Display Preview
        render_image_preview(st.session_state.original_image, final_image)

# 2. IMAGE ENHANCEMENT PAGE
elif menu == "Image Enhancement":
    render_image_enhancement_page()

# 3. GEOMETRIC TRANSFORMATION PAGE
elif menu == "Geometric Transformation":
    render_geometric_transformation_page()

# 4. IMAGE RESTORATION PAGE
elif menu == "Image Restoration":
    render_image_restoration_page()

# 5. BINARY & EDGE PROCESSING PAGE
elif menu == "Binary & Edge Processing":
    render_binary_edge_processing_page()