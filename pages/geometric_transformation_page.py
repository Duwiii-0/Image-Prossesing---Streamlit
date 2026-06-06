import streamlit as st
import cv2
import numpy as np
from PIL import Image
from image_processing.geometric_transformation import get_crop_dimensions
from utils.state_manager import reset_geometric_state, reset_crop_state
from utils.preview_helper import get_preview_image
from utils.ui_helpers import render_image_preview, render_reset_and_save_buttons, render_section_header
from utils.constants import RATIO_OPTIONS


def render_geometric_transformation_page():
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Rotate", "Flip", "Trans", "Scale", "Crop"])

    # Before image for crop preview (processed_image + apply_all_operations WITHOUT crop)
    before_image_for_crop = get_preview_image(extra_params={'crop_target_ratio': None})
    
    # Calculate original ratio
    h, w = before_image_for_crop.shape[:2]
    original_ratio = w / h
    
    # Initializing crop_target_ratio if None
    if st.session_state.crop_target_ratio is None and st.session_state.crop_ratio_selected == "Original":
        st.session_state.crop_target_ratio = original_ratio

    # TAB 1: ROTATE
    with tab1:
        rotation_val = st.slider(
            "Angle", 0, 360,
            value=st.session_state.rotation_angle,
            key="rotation_slider_temp"
        )
        if rotation_val != st.session_state.rotation_angle:
            st.session_state.rotation_angle = rotation_val
            st.rerun()

    # TAB 2: FLIP 
    with tab2:
        if st.button("↔ Flip Horizontal", type="primary", use_container_width=True):
            st.session_state.processed_image = cv2.flip(st.session_state.processed_image, 1)
            st.rerun()

        if st.button("↕ Flip Vertical", type="primary", use_container_width=True):
            st.session_state.processed_image = cv2.flip(st.session_state.processed_image, 0)
            st.rerun()

    # TAB 3: TRANSLATION 
    with tab3:
        trans_x_val = st.slider(
            "Shift X", -500, 500,
            value=st.session_state.translate_x,
            key="trans_x_temp"
        )
        if trans_x_val != st.session_state.translate_x:
            st.session_state.translate_x = trans_x_val
            st.rerun()
        trans_y_val = st.slider(
            "Shift Y", -500, 500,
            value=st.session_state.translate_y,
            key="trans_y_temp"
        )
        if trans_y_val != st.session_state.translate_y:
            st.session_state.translate_y = trans_y_val
            st.rerun()

    # TAB 4: SCALING 
    with tab4:
        scale_val = st.slider(
            "Scale", 0.1, 3.0, step=0.05,
            value=st.session_state.scale_factor,
            key="scale_temp"
        )
        if scale_val != st.session_state.scale_factor:
            st.session_state.scale_factor = scale_val
            st.rerun()

    # TAB 5: CROP 
    with tab5:
        selected_ratio = st.selectbox(
            "Ratio",
            list(RATIO_OPTIONS.keys()),
            index=list(RATIO_OPTIONS.keys()).index(st.session_state.crop_ratio_selected),
            key="crop_ratio_select"
        )
        
        if selected_ratio != "Original":
            target_ratio = RATIO_OPTIONS[selected_ratio]
        else:
            target_ratio = original_ratio
        
        if selected_ratio != st.session_state.crop_ratio_selected:
            st.session_state.crop_ratio_selected = selected_ratio
            st.session_state.crop_target_ratio = target_ratio
            st.session_state.crop_scale = 1.0
            st.session_state.crop_x_offset = 0
            st.session_state.crop_y_offset = 0
            st.rerun()
        
        # Update crop_target_ratio in every changes
        if st.session_state.crop_target_ratio != target_ratio:
            st.session_state.crop_target_ratio = target_ratio
            st.rerun()
        
        h, w = before_image_for_crop.shape[:2]
        
        # Calculate crop dimensions
        base_crop_w, base_crop_h = get_crop_dimensions(w, h, target_ratio)
        
        # SCALE RATIO slider
        scale_val = st.slider(
            "Zoom", 
            0.3, 1.0, 
            step=0.01,
            value=st.session_state.crop_scale,
            key="crop_scale_slider"
        )
        if scale_val != st.session_state.crop_scale:
            st.session_state.crop_scale = scale_val
            new_crop_w = int(base_crop_w * scale_val)
            new_crop_h = int(base_crop_h * scale_val)
            st.session_state.crop_x_offset = max((w - new_crop_w) // 2, 0)
            st.session_state.crop_y_offset = max((h - new_crop_h) // 2, 0)
            st.rerun()
        
        crop_w = int(base_crop_w * st.session_state.crop_scale)
        crop_h = int(base_crop_h * st.session_state.crop_scale)
        crop_w = min(crop_w, w)
        crop_h = min(crop_h, h)
        
        max_x_offset = w - crop_w
        max_y_offset = h - crop_h
        
        if st.session_state.crop_x_offset > max_x_offset:
            st.session_state.crop_x_offset = max(max_x_offset // 2, 0)
        if st.session_state.crop_y_offset > max_y_offset:
            st.session_state.crop_y_offset = max(max_y_offset // 2, 0)
        
        if max_x_offset > 0:
            x_offset = st.slider(
                "X", 
                0, max_x_offset,
                value=min(st.session_state.crop_x_offset, max_x_offset),
                key="crop_x_slider"
            )
            if x_offset != st.session_state.crop_x_offset:
                st.session_state.crop_x_offset = x_offset
                st.rerun()
        
        if max_y_offset > 0:
            y_offset = st.slider(
                "Y", 
                0, max_y_offset,
                value=min(st.session_state.crop_y_offset, max_y_offset),
                key="crop_y_slider"
            )
            if y_offset != st.session_state.crop_y_offset:
                st.session_state.crop_y_offset = y_offset
                st.rerun()

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("Reset Geometric", use_container_width=True):
        reset_geometric_state()
        reset_crop_state()
        st.session_state.processed_image = st.session_state.original_image.copy()
        st.rerun()
