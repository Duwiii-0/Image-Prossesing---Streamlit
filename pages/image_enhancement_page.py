import streamlit as st
import numpy as np
from PIL import Image
from utils.state_manager import reset_enhancement_state
from utils.preview_helper import get_preview_image
from utils.ui_helpers import render_image_preview, render_section_header

# Gunakan session state untuk timestamp reset
def reset_enhancement():
    reset_enhancement_state()
    if 'reset_counter' not in st.session_state:
        st.session_state.reset_counter = 0
    st.session_state.reset_counter += 1
    st.rerun()

def render_image_enhancement_page():
    # Inisialisasi reset counter
    if 'reset_counter' not in st.session_state:
        st.session_state.reset_counter = 0
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Brightness", 
        "Equalize", 
        "Sharpen", 
        "Blur"
    ])

    with tab1:
        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        
        # Brightness - key pakai counter agar force refresh saat reset
        def on_brightness_change():
            st.session_state.brightness = st.session_state[f"_brightness_{st.session_state.reset_counter}"]
        
        st.slider(
            "Brightness", -150, 150,
            value=st.session_state.brightness,
            key=f"_brightness_{st.session_state.reset_counter}",
            on_change=on_brightness_change
        )
        
        # Contrast
        def on_contrast_change():
            st.session_state.contrast = st.session_state[f"_contrast_{st.session_state.reset_counter}"]
        
        st.slider(
            "Contrast", -100, 100,
            value=st.session_state.contrast,
            key=f"_contrast_{st.session_state.reset_counter}",
            on_change=on_contrast_change
        )

    with tab2:
        st.markdown("<p style='font-size: 0.8rem;'>Histogram equalization improves contrast by spreading out intensity values.</p>", unsafe_allow_html=True)
        
        if st.button("Apply Equalization", type="primary", use_container_width=True):
            st.session_state.histogram_equalization_enabled = True
            st.rerun()
        
        if st.session_state.histogram_equalization_enabled:
            st.success("Equalization applied")
        else:
            st.info("Click 'Apply Equalization' to enhance contrast")

    with tab3:
        def on_sharpening_change():
            st.session_state.sharpening = st.session_state[f"_sharpening_{st.session_state.reset_counter}"]
        
        st.slider(
            "Strength", 0, 100,
            value=st.session_state.sharpening,
            key=f"_sharpening_{st.session_state.reset_counter}",
            on_change=on_sharpening_change
        )

    with tab4:
        def on_blur_change():
            st.session_state.blur_size = st.session_state[f"_blur_{st.session_state.reset_counter}"]
        
        st.slider(
            "Kernel Size", 1, 15, step=2,
            value=st.session_state.blur_size,
            key=f"_blur_{st.session_state.reset_counter}",
            on_change=on_blur_change
        )

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("Reset Enhancement", use_container_width=True):
        reset_enhancement()