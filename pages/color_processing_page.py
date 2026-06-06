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

    # Reset color processing state if not present
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
    
    tab1, tab2, tab3, tab4 = st.tabs(["Basic", "HSV", "FX", "Balance"])
    
    with tab1:
        if st.button("Convert to Grayscale", key="btn_grayscale", use_container_width=True):
            st.session_state.color_processing_state['grayscale'] = True
            st.session_state.color_processing_state['channel_split'] = False
            st.rerun()
        
        if st.button("Show RGB Channels", key="btn_channel_split", use_container_width=True):
            st.session_state.color_processing_state['channel_split'] = True
            st.session_state.color_processing_state['grayscale'] = False
            st.rerun()

    with tab2:
        hue_shift = st.slider("Hue", -180, 180, st.session_state.color_processing_state['hue_shift'], key="hue_shift_slider")
        if hue_shift != st.session_state.color_processing_state['hue_shift']:
            st.session_state.color_processing_state['hue_shift'] = hue_shift
            st.rerun()
        
        saturation = st.slider("Sat", 0.0, 2.0, st.session_state.color_processing_state['saturation_scale'], 0.1, key="saturation_slider")
        if saturation != st.session_state.color_processing_state['saturation_scale']:
            st.session_state.color_processing_state['saturation_scale'] = saturation
            st.rerun()
        
        brightness = st.slider("Val", 0.0, 2.0, st.session_state.color_processing_state['value_scale'], 0.1, key="brightness_slider")
        if brightness != st.session_state.color_processing_state['value_scale']:
            st.session_state.color_processing_state['value_scale'] = brightness
            st.rerun()
    
    with tab3:
        if st.button("Invert Colors", key="btn_invert", use_container_width=True):
            st.session_state.color_processing_state['invert'] = not st.session_state.color_processing_state['invert']
            st.rerun()
        
        sepia_intensity = st.slider("Sepia", 0.0, 1.0, st.session_state.color_processing_state['sepia_intensity'], 0.1, key="sepia_slider")
        if sepia_intensity != st.session_state.color_processing_state['sepia_intensity']:
            st.session_state.color_processing_state['sepia_intensity'] = sepia_intensity
            st.rerun()
        
        posterize_levels = st.slider("Levels", 2, 8, st.session_state.color_processing_state['posterize_levels'], key="posterize_slider")
        if posterize_levels != st.session_state.color_processing_state['posterize_levels']:
            st.session_state.color_processing_state['posterize_levels'] = posterize_levels
            st.rerun()
    
    with tab4:
        red_shift = st.slider("Red", -100, 100, st.session_state.color_processing_state['red_shift'], key="red_shift_slider")
        if red_shift != st.session_state.color_processing_state['red_shift']:
            st.session_state.color_processing_state['red_shift'] = red_shift
            st.rerun()
        
        green_shift = st.slider("Green", -100, 100, st.session_state.color_processing_state['green_shift'], key="green_shift_slider")
        if green_shift != st.session_state.color_processing_state['green_shift']:
            st.session_state.color_processing_state['green_shift'] = green_shift
            st.rerun()
        
        blue_shift = st.slider("Blue", -100, 100, st.session_state.color_processing_state['blue_shift'], key="blue_shift_slider")
        if blue_shift != st.session_state.color_processing_state['blue_shift']:
            st.session_state.color_processing_state['blue_shift'] = blue_shift
            st.rerun()

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("Reset Color", use_container_width=True):
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
        st.session_state.processed_image = st.session_state.original_image.copy()
        st.rerun()

    # Apply all color processing
    processed = st.session_state.original_image.copy()
    
    if st.session_state.color_processing_state['grayscale']:
        processed = apply_rgb_to_grayscale(processed)
        if len(processed.shape) == 2:
            processed = np.stack([processed] * 3, axis=2)
    
    hue = st.session_state.color_processing_state['hue_shift']
    sat = st.session_state.color_processing_state['saturation_scale']
    bright = st.session_state.color_processing_state['value_scale']
    if hue != 0 or sat != 1.0 or bright != 1.0:
        processed = apply_hsv_adjustment(processed, hue, sat, bright)
    
    if st.session_state.color_processing_state['invert']:
        processed = apply_invert_colors(processed)
    
    sepia_int = st.session_state.color_processing_state['sepia_intensity']
    if sepia_int > 0:
        processed = apply_sepia_effect(processed, sepia_int)
    
    if st.session_state.color_processing_state['posterize_levels'] != 8:
        processed = apply_posterize(processed, st.session_state.color_processing_state['posterize_levels'])
    
    r_shift = st.session_state.color_processing_state['red_shift']
    g_shift = st.session_state.color_processing_state['green_shift']
    b_shift = st.session_state.color_processing_state['blue_shift']
    if r_shift != 0 or g_shift != 0 or b_shift != 0:
        processed = apply_color_balance(processed, r_shift, g_shift, b_shift)
    
    st.session_state.processed_image = processed
