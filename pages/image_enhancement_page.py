import streamlit as st
import numpy as np
from PIL import Image
from image_processing.image_enhancement import apply_histogram_equalization
from utils.state_manager import reset_enhancement_state
from utils.preview_helper import get_preview_image
from utils.ui_helpers import render_image_preview, render_reset_and_save_buttons, render_section_header

def render_image_enhancement_page():
    tab1, tab2, tab3, tab4 = st.tabs([
        "Brightness", 
        "Equalize", 
        "Sharpen", 
        "Blur"
    ])

    with tab1:
        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        brightness_val = st.slider(
            "Brightness", -150, 150,
            value=st.session_state.brightness,
            key="brightness_slider_temp"
        )
        if brightness_val != st.session_state.brightness:
            st.session_state.brightness = brightness_val
            st.rerun()
        
        contrast_val = st.slider(
            "Contrast", -100, 100,
            value=st.session_state.contrast,
            key="contrast_slider_temp"
        )
        if contrast_val != st.session_state.contrast:
            st.session_state.contrast = contrast_val
            st.rerun()

    with tab2:
        st.markdown("<p style='font-size: 0.8rem;'>Histogram equalization improves contrast by spreading out intensity values.</p>", unsafe_allow_html=True)
        
        if st.button("Apply Equalization", type="primary", use_container_width=True):
            st.session_state.histogram_equalization_enabled = True
            st.rerun()
        
        # Tampilkan status (opsional, tapi membantu)
        if st.session_state.histogram_equalization_enabled:
            st.success("Equalization applied")
        else:
            st.info("Equalization not applied")

    with tab3:
        sharpening_val = st.slider(
            "Strength", 0, 100,
            value=st.session_state.sharpening,
            key="sharpening_slider_temp"
        )
        if sharpening_val != st.session_state.sharpening:
            st.session_state.sharpening = sharpening_val
            st.rerun()

    with tab4:
        blur_val = st.slider(
            "Kernel Size", 1, 15, step=2,
            value=st.session_state.blur_size,
            key="blur_slider_temp"
        )
        if blur_val != st.session_state.blur_size:
            st.session_state.blur_size = blur_val
            st.rerun()

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("Reset Enhancement", use_container_width=True):
        reset_enhancement_state()
        st.rerun()
