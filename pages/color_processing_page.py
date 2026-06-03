import streamlit as st
import numpy as np
from PIL import Image

from image_processing.color_processing import (
    apply_rgb_to_grayscale,
    apply_channel_split,
    apply_hsv_adjustment,
    apply_invert_colors,
    apply_sepia_effect,
    apply_posterize,
    apply_color_balance,
)
from utils.preview_helper import get_preview_image
from utils.ui_helpers import render_reset_and_save_buttons, render_image_preview


def render_color_processing_page():
    """Render Color Processing page"""

# Reset color processing state
    if 'color_processing_state' not in st.session_state:
        st.session_state.color_processing_state = {
            'operation': 'None',
            'grayscale': False,
            'channel_split': False,
            'hue_shift': 0,
            'saturation_scale': 1.0,
            'value_scale': 1.0,
            'invert': False,
            'sepia_intensity': 0.0,
            'posterize_levels': 4,
            'red_shift': 0,
            'green_shift': 0,
            'blue_shift': 0,
        }
    
    st.markdown("Adjust and manipulate colors in your image.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Upload File
    uploaded_file = st.file_uploader(
        "Select an Image (JPG, PNG, BMP)",
        type=["jpg", "png", "jpeg", "bmp"],
        key="color_processing_uploader"
    )
    
    if uploaded_file is not None:
        # Read image
        image = Image.open(uploaded_file).convert('RGB')
        image_np = np.array(image)
        
        st.session_state.original_image = image_np.copy()
        st.session_state.processed_image = image_np.copy()
    
    if st.session_state.processed_image is not None:
        st.markdown("<hr style='margin: 2rem 0; border: none; border-top: 1px solid #E2E8F0;' />", unsafe_allow_html=True)
        
        # Color Processing Options
        st.subheader("Color Processing Operations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Grayscale Conversion
            st.markdown("**Grayscale Conversion**")
            if st.button("Convert to Grayscale", key="btn_grayscale"):
                st.session_state.color_processing_state['grayscale'] = True
                st.session_state.color_processing_state['channel_split'] = False
        
        with col2:
            # Channel Split
            st.markdown("**Channel Split**")
            if st.button("Show RGB Channels", key="btn_channel_split"):
                st.session_state.color_processing_state['channel_split'] = True
                st.session_state.color_processing_state['grayscale'] = False
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # HSV Adjustment
        st.markdown("**HSV Adjustment**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            hue_shift = st.slider(
                "Hue Shift",
                -180, 180, 0,
                key="hue_shift_slider"
            )
            st.session_state.color_processing_state['hue_shift'] = hue_shift
        
        with col2:
            saturation = st.slider(
                "Saturation",
                0.0, 2.0, 1.0, 0.1,
                key="saturation_slider"
            )
            st.session_state.color_processing_state['saturation_scale'] = saturation
        
        with col3:
            brightness = st.slider(
                "Brightness",
                0.0, 2.0, 1.0, 0.1,
                key="brightness_slider"
            )
            st.session_state.color_processing_state['value_scale'] = brightness
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Special Effects
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Invert Colors**")
            if st.button("Invert", key="btn_invert"):
                st.session_state.color_processing_state['invert'] = not st.session_state.color_processing_state['invert']
        
        with col2:
            st.markdown("**Sepia Effect**")
            sepia_intensity = st.slider(
                "Sepia Intensity",
                0.0, 1.0, 0.0, 0.1,
                key="sepia_slider"
            )
            st.session_state.color_processing_state['sepia_intensity'] = sepia_intensity
        
        with col3:
            st.markdown("**Posterize**")
            posterize_levels = st.slider(
                "Color Levels",
                2, 8, 4,
                key="posterize_slider"
            )
            st.session_state.color_processing_state['posterize_levels'] = posterize_levels
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Color Balance
        st.markdown("**Color Balance**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            red_shift = st.slider(
                "Red Channel",
                -100, 100, 0,
                key="red_shift_slider"
            )
            st.session_state.color_processing_state['red_shift'] = red_shift
        
        with col2:
            green_shift = st.slider(
                "Green Channel",
                -100, 100, 0,
                key="green_shift_slider"
            )
            st.session_state.color_processing_state['green_shift'] = green_shift
        
        with col3:
            blue_shift = st.slider(
                "Blue Channel",
                -100, 100, 0,
                key="blue_shift_slider"
            )
            st.session_state.color_processing_state['blue_shift'] = blue_shift
        
        st.markdown("<hr style='margin: 2rem 0; border: none; border-top: 1px solid #E2E8F0;' />", unsafe_allow_html=True)
        
        # Apply all color processing
        processed = st.session_state.original_image.copy()
        
        # Grayscale
        if st.session_state.color_processing_state['grayscale']:
            processed = apply_rgb_to_grayscale(processed)
            # Convert back to RGB for consistency
            if len(processed.shape) == 2:
                processed = np.stack([processed] * 3, axis=2)
        
        # Channel Split - hanya tampilkan, jangan ubah processed
        if st.session_state.color_processing_state['channel_split']:
            r, g, b = apply_channel_split(processed)
            st.markdown("**RGB Channels**")
            ch_col1, ch_col2, ch_col3 = st.columns(3)
            with ch_col1:
                    st.image(r, caption="Red Channel", use_container_width=True)
            with ch_col2:
                    st.image(g, caption="Green Channel", use_container_width=True)
            with ch_col3:
                    st.image(b, caption="Blue Channel", use_container_width=True)
        hue = st.session_state.color_processing_state['hue_shift']
        sat = st.session_state.color_processing_state['saturation_scale']
        bright = st.session_state.color_processing_state['value_scale']

        if hue != 0 or sat != 1.0 or bright != 1.0:
            processed = apply_hsv_adjustment(processed, hue, sat, bright)
        
        # Invert
        if st.session_state.color_processing_state['invert']:
            processed = apply_invert_colors(processed)
        
        # Sepia
        sepia_int = st.session_state.color_processing_state['sepia_intensity']
        if sepia_int > 0:
            processed = apply_sepia_effect(processed, sepia_int)
        
        # Posterize
        if st.session_state.color_processing_state['posterize_levels'] != 8:
            processed = apply_posterize(processed, st.session_state.color_processing_state['posterize_levels'])
        
        # Color Balance
        r_shift = st.session_state.color_processing_state['red_shift']
        g_shift = st.session_state.color_processing_state['green_shift']
        b_shift = st.session_state.color_processing_state['blue_shift']
        
        if r_shift != 0 or g_shift != 0 or b_shift != 0:
            processed = apply_color_balance(processed, r_shift, g_shift, b_shift)
        
        st.session_state.processed_image = processed
        
        # Get final preview
        final_image = get_preview_image()
        
        if final_image is None:
            st.error("Image processing failed")
            st.stop()
        
        # Reset and Save buttons
        render_reset_and_save_buttons(
            reset_callback=lambda: (
                st.session_state.update({
                    'processed_image': st.session_state.original_image.copy(),
                    'color_processing_state': {
                        'operation': 'None',
                        'grayscale': False,
                        'channel_split': False,
                        'hue_shift': 0,
                        'saturation_scale': 1.0,
                        'value_scale': 1.0,
                        'invert': False,
                        'sepia_intensity': 0.0,
                        'posterize_levels': 4,
                        'red_shift': 0,
                        'green_shift': 0,
                        'blue_shift': 0,
                    }
                })
            ),
            image_to_save=final_image
        )
        
        st.markdown("<hr style='margin: 2rem 0; border: none; border-top: 1px solid #E2E8F0;' />", unsafe_allow_html=True)
        
        # Preview
        render_image_preview(st.session_state.original_image, final_image)
