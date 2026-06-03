import streamlit as st
import numpy as np
from PIL import Image
from image_processing.image_enhancement import apply_histogram_equalization
from utils.state_manager import reset_enhancement_state
from utils.preview_helper import get_preview_image
from utils.ui_helpers import render_image_preview, render_reset_and_save_buttons, render_section_header

def render_image_enhancement_page():
    render_section_header(
        title="Image Enhancement",
        description="Adjust brightness, contrast, and apply filters to improve visual quality.",
        icon="🎨"
    )
    
    # Upload File
    uploaded_file = st.file_uploader(
        "Select an Image (JPG, PNG, BMP)",
        type=["jpg", "png", "jpeg", "bmp"],
        key="image_enhancement_uploader"
    )
    
    if uploaded_file is not None:
        # Read image
        image = Image.open(uploaded_file).convert('RGB')
        image_np = np.array(image)
        
        st.session_state.original_image = image_np.copy()
        st.session_state.processed_image = image_np.copy()
    
    if st.session_state.original_image is None:
        st.markdown("""
        <div style="background: rgba(99, 102, 241, 0.1); border: 1px dashed rgba(99, 102, 241, 0.4); padding: 2rem; text-align: center; border-radius: 12px; margin-top: 1rem;">
            <span style="font-size: 2rem;">📸</span>
            <p style="color: #94A3B8; margin-top: 0.5rem; font-weight: 500;">Please upload an image to begin.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    if st.session_state.processed_image is None:
        st.session_state.processed_image = st.session_state.original_image.copy()

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "Brightness & Contrast", 
        "Histogram Equalization", 
        "Sharpening", 
        "Smoothing (Blur)"
    ])

    with tab1:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
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
        st.markdown('</div>', unsafe_allow_html=True)
        
        # preview_image = get_preview_image()
        # render_image_preview(st.session_state.original_image, preview_image)

    with tab2:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        st.markdown("<p>This operation automatically adjusts the image contrast by evenly distributing the intensity values across the histogram.</p>", unsafe_allow_html=True)
        if st.button("Apply Histogram Equalization", type="primary"):
            st.session_state.processed_image = apply_histogram_equalization(
                st.session_state.processed_image
            )
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # preview_image = get_preview_image()
        # render_image_preview(st.session_state.original_image, preview_image)

    with tab3:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        st.markdown("<p>Enhance the edges and details of the image using a convolution kernel matrix.</p>", unsafe_allow_html=True)
        sharpening_val = st.slider(
            "Sharpening Strength", 0, 100,
            value=st.session_state.sharpening,
            key="sharpening_slider_temp"
        )
        if sharpening_val != st.session_state.sharpening:
            st.session_state.sharpening = sharpening_val
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # preview_image = get_preview_image()
        # render_image_preview(st.session_state.original_image, preview_image)

    with tab4:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        st.markdown("<p>Smooth the image and reduce noise using a Gaussian filter.</p>", unsafe_allow_html=True)
        blur_val = st.slider(
            "Kernel Size (Gaussian)", 1, 15, step=2,
            value=st.session_state.blur_size,
            key="blur_slider_temp"
        )
        if blur_val != st.session_state.blur_size:
            st.session_state.blur_size = blur_val
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # preview_image = get_preview_image()
        # render_image_preview(st.session_state.original_image, preview_image)


    st.markdown("<hr/>", unsafe_allow_html=True)
    
    # Reset and Save buttons
    preview_image = get_preview_image()
    render_image_preview(st.session_state.original_image, preview_image)
    render_reset_and_save_buttons(
        reset_callback=lambda: reset_enhancement_state(), 
        image_to_save=preview_image
    )