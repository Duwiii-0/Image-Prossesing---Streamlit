import streamlit as st
import numpy as np
from image_processing.image_enhancement import apply_histogram_equalization
from utils.preview_helper import get_preview_image
from utils.ui_helpers import render_image_preview


def render_image_enhancement_page():
    if st.session_state.original_image is None:
        st.markdown("""
        <div class="custom-info-box">
            <strong>Notice:</strong> Please upload an image via the Image Management menu before applying any enhancements.
        </div>
        """, unsafe_allow_html=True)
        return
    
    if st.session_state.processed_image is None:
        st.session_state.processed_image = st.session_state.original_image.copy()

    st.markdown("Select a tool below to apply modifications to your image.")
    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "Brightness & Contrast", 
        "Histogram Equalization", 
        "Sharpening", 
        "Smoothing (Blur)"
    ])

    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        col_sl1, col_sl2 = st.columns(2)
        with col_sl1:
            brightness_val = st.slider(
                "Brightness", -150, 150,
                value=st.session_state.brightness,
                key="brightness_slider_temp"
            )
            if brightness_val != st.session_state.brightness:
                st.session_state.brightness = brightness_val
                st.rerun()
        with col_sl2:
            contrast_val = st.slider(
                "Contrast", -100, 100,
                value=st.session_state.contrast,
                key="contrast_slider_temp"
            )
            if contrast_val != st.session_state.contrast:
                st.session_state.contrast = contrast_val
                st.rerun()

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("This operation automatically adjusts the image contrast by evenly distributing the intensity values across the histogram.")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Apply Histogram Equalization", type="primary"):
            st.session_state.processed_image = apply_histogram_equalization(
                st.session_state.processed_image
            )
            st.rerun()

    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("Enhance the edges and details of the image using a convolution kernel matrix.")
        st.markdown("<br>", unsafe_allow_html=True)
        sharpening_val = st.slider(
            "Sharpening Strength", 0, 100,
            value=st.session_state.sharpening,
            key="sharpening_slider_temp"
        )
        if sharpening_val != st.session_state.sharpening:
            st.session_state.sharpening = sharpening_val
            st.rerun()

    with tab4:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("Smooth the image and reduce noise using a Gaussian filter.")
        st.markdown("<br>", unsafe_allow_html=True)
        blur_val = st.slider(
            "Kernel Size (Gaussian)", 1, 15, step=2,
            value=st.session_state.blur_size,
            key="blur_slider_temp"
        )
        if blur_val != st.session_state.blur_size:
            st.session_state.blur_size = blur_val
            st.rerun()

    # Preview image using helper
    preview_image = get_preview_image()

    st.markdown("<hr style='margin: 2.5rem 0;' />", unsafe_allow_html=True)
    st.markdown("### Image Preview")

    render_image_preview(st.session_state.original_image, preview_image)