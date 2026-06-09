import streamlit as st
import cv2
import numpy as np
from PIL import Image
from image_processing.geometric_transformation import get_crop_dimensions
from utils.state_manager import reset_geometric_state, reset_crop_state
from utils.constants import RATIO_OPTIONS

def reset_geometric():
    reset_geometric_state()
    reset_crop_state()
    if 'reset_counter' not in st.session_state:
        st.session_state.reset_counter = 0
    st.session_state.reset_counter += 1
    st.session_state.processed_image = st.session_state.original_image.copy()
    st.rerun()

def render_geometric_transformation_page():
    if 'reset_counter' not in st.session_state:
        st.session_state.reset_counter = 0
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Rotate", "Flip", "Trans", "Scale", "Crop"])

    # Get rotated image without any crop constraints for calculating dimensions
    from utils.preview_helper import get_preview_image
    before_image_for_crop = get_preview_image(extra_params={'crop_target_ratio': None, 'crop_scale': 1.0, 'crop_x_offset': 0, 'crop_y_offset': 0})
    h, w = before_image_for_crop.shape[:2]
    original_ratio = w / h

    # TAB 1: ROTATE
    with tab1:
        def on_rotate_change():
            st.session_state.rotation_angle = st.session_state[f"_rotate_{st.session_state.reset_counter}"]
        
        st.slider(
            "Angle", 0, 360,
            value=st.session_state.rotation_angle,
            key=f"_rotate_{st.session_state.reset_counter}",
            on_change=on_rotate_change
        )

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
        def on_trans_x_change():
            st.session_state.translate_x = st.session_state[f"_trans_x_{st.session_state.reset_counter}"]
        
        st.slider(
            "Shift X", -500, 500,
            value=st.session_state.translate_x,
            key=f"_trans_x_{st.session_state.reset_counter}",
            on_change=on_trans_x_change
        )
        
        def on_trans_y_change():
            st.session_state.translate_y = st.session_state[f"_trans_y_{st.session_state.reset_counter}"]
        
        st.slider(
            "Shift Y", -500, 500,
            value=st.session_state.translate_y,
            key=f"_trans_y_{st.session_state.reset_counter}",
            on_change=on_trans_y_change
        )

    # TAB 4: SCALING 
    with tab4:
        def on_scale_change():
            st.session_state.scale_factor = st.session_state[f"_scale_{st.session_state.reset_counter}"]
        
        st.slider(
            "Scale", 0.1, 3.0, step=0.05,
            value=st.session_state.scale_factor,
            key=f"_scale_{st.session_state.reset_counter}",
            on_change=on_scale_change
        )

    # TAB 5: CROP 
    with tab5:
        def on_ratio_change():
            selected = st.session_state[f"crop_ratio_select_{st.session_state.reset_counter}"]
            st.session_state.crop_ratio_selected = selected
            st.session_state.crop_target_ratio = RATIO_OPTIONS[selected]
            st.session_state.crop_scale = 1.0
            st.session_state.crop_x_offset = 0
            st.session_state.crop_y_offset = 0
        
        selected_ratio = st.selectbox(
            "Ratio", list(RATIO_OPTIONS.keys()),
            index=list(RATIO_OPTIONS.keys()).index(st.session_state.crop_ratio_selected),
            key=f"crop_ratio_select_{st.session_state.reset_counter}",
            on_change=on_ratio_change
        )
        if selected_ratio != st.session_state.crop_ratio_selected:
            st.session_state.crop_ratio_selected = selected_ratio
            st.session_state.crop_target_ratio = RATIO_OPTIONS[selected_ratio]
            st.session_state.crop_scale = 1.0
            st.session_state.crop_x_offset = 0
            st.session_state.crop_y_offset = 0
        
        def on_crop_zoom_change():
            st.session_state.crop_scale = st.session_state[f"_crop_zoom_{st.session_state.reset_counter}"]
        
        st.slider(
            "Zoom", 0.3, 1.0, step=0.01,
            value=st.session_state.crop_scale,
            key=f"_crop_zoom_{st.session_state.reset_counter}",
            on_change=on_crop_zoom_change
        )
        
        current_target_ratio = st.session_state.crop_target_ratio if st.session_state.crop_target_ratio is not None else original_ratio
        base_crop_w, base_crop_h = get_crop_dimensions(w, h, current_target_ratio)
        
        crop_w = int(base_crop_w * st.session_state.crop_scale)
        crop_h = int(base_crop_h * st.session_state.crop_scale)
        
        max_x = max(w - crop_w, 0)
        max_y = max(h - crop_h, 0)
        
        slider_max_x = max_x if max_x > 0 else 1
        def on_crop_x_change():
            st.session_state.crop_x_offset = st.session_state[f"_crop_x_{st.session_state.reset_counter}"]
        
        st.slider(
            "X", 0, slider_max_x,
            value=min(st.session_state.crop_x_offset, max_x),
            disabled=(max_x == 0),
            key=f"_crop_x_{st.session_state.reset_counter}",
            on_change=on_crop_x_change
        )
        
        slider_max_y = max_y if max_y > 0 else 1
        def on_crop_y_change():
            st.session_state.crop_y_offset = st.session_state[f"_crop_y_{st.session_state.reset_counter}"]
        
        st.slider(
            "Y", 0, slider_max_y,
            value=min(st.session_state.crop_y_offset, max_y),
            disabled=(max_y == 0),
            key=f"_crop_y_{st.session_state.reset_counter}",
            on_change=on_crop_y_change
        )

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("Reset Geometric", use_container_width=True):
        reset_geometric()