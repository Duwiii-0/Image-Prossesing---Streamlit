import streamlit as st
import cv2
import numpy as np
from PIL import Image
from streamlit_cropper import st_cropper
from image_processing.geometric_transformation import get_crop_dimensions
from utils.state_manager import reset_geometric_state, reset_crop_state
from utils.constants import RATIO_OPTIONS
from utils.preview_helper import get_preview_image

def reset_geometric():
    reset_geometric_state()
    reset_crop_state()
    if 'reset_counter' not in st.session_state:
        st.session_state.reset_counter = 0
    st.session_state.reset_counter += 1
    st.session_state.enable_live_crop = False
    st.session_state.crop_ratio_selected = "Original"
    st.session_state.crop_target_ratio = None
    st.session_state.processed_image = st.session_state.original_image.copy()
    st.rerun()

def render_geometric_transformation_page():
    if 'reset_counter' not in st.session_state:
        st.session_state.reset_counter = 0
        
    rc = st.session_state.reset_counter
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Rotate", "Flip", "Trans", "Scale", "Crop"])

    from image_processing.apply_all_operations import apply_all_operations
    from utils.preview_helper import get_base_params
    
    params = get_base_params()
    params.update({
        'angle': 0, 'translate_x': 0, 'translate_y': 0, 'scale': 1.0,
        'crop_target_ratio': None, 'crop_scale': 1.0, 'crop_x_offset': 0, 'crop_y_offset': 0
    })
    
    if st.session_state.original_image is not None:
        before_image_for_crop = st.session_state.original_image.copy()
    else:
        before_image_for_crop = np.zeros((300, 300, 3), dtype=np.uint8)

    h, w = before_image_for_crop.shape[:2]
    original_ratio = w / h

    # TAB 1: ROTATE
    with tab1:
        def on_rotate_change():
            st.session_state.rotation_angle = st.session_state[f"_rotate_{rc}"]
        
        st.slider(
            "Angle", 0, 360,
            value=st.session_state.rotation_angle,
            key=f"_rotate_{rc}",
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
            st.session_state.translate_x = st.session_state[f"_trans_x_{rc}"]
        
        st.slider(
            "Shift X", -500, 500,
            value=st.session_state.translate_x,
            key=f"_trans_x_{rc}",
            on_change=on_trans_x_change
        )
        
        def on_trans_y_change():
            st.session_state.translate_y = st.session_state[f"_trans_y_{rc}"]
        
        st.slider(
            "Shift Y", -500, 500,
            value=st.session_state.translate_y,
            key=f"_trans_y_{rc}",
            on_change=on_trans_y_change
        )

    # TAB 4: SCALING 
    with tab4:
        def on_scale_change():
            st.session_state.scale_factor = st.session_state[f"_scale_{rc}"]
        
        st.slider(
            "Scale", 0.1, 3.0, step=0.05,
            value=st.session_state.scale_factor,
            key=f"_scale_{rc}",
            on_change=on_scale_change
        )

    # TAB 5: CROP
        with tab5:
            enable_crop = st.checkbox(
                "Aktifkan Crop", 
                value=st.session_state.enable_live_crop, 
                key=f"enable_live_crop_{rc}"
            )
            
            if enable_crop != st.session_state.enable_live_crop:
                st.session_state.enable_live_crop = enable_crop
                if not enable_crop:
                    reset_crop_state()
                st.rerun()
        
            if st.session_state.enable_live_crop:
                # 1. Dropdown & Logic Ratio
                def on_ratio_change():
                    selected = st.session_state[f"crop_ratio_select_{rc}"]
                    st.session_state.crop_ratio_selected = selected
                    st.session_state.crop_target_ratio = RATIO_OPTIONS[selected] if RATIO_OPTIONS[selected] is not None else original_ratio
                    st.session_state.crop_scale = 1.0
                    st.session_state.crop_x_offset = 0
                    st.session_state.crop_y_offset = 0
                
                selected_ratio = st.selectbox(
                    "Ratio", list(RATIO_OPTIONS.keys()),
                    index=list(RATIO_OPTIONS.keys()).index(st.session_state.crop_ratio_selected),
                    key=f"crop_ratio_select_{rc}",
                    on_change=on_ratio_change
                )
                
                if selected_ratio != st.session_state.crop_ratio_selected:
                    st.session_state.crop_ratio_selected = selected_ratio
                    st.session_state.crop_target_ratio = RATIO_OPTIONS[selected_ratio] if RATIO_OPTIONS[selected_ratio] is not None else original_ratio
                    st.session_state.crop_scale = 1.0
                    st.session_state.crop_x_offset = 0
                    st.session_state.crop_y_offset = 0
                    st.rerun()

                # 2. Format aspek ratio
                target_aspect = st.session_state.crop_target_ratio
                if target_aspect is None: target_aspect = (int(w), int(h))
                elif isinstance(target_aspect, (int, float)):
                    if abs(target_aspect - 1.0) < 0.01: target_aspect = (1, 1)
                    elif abs(target_aspect - 1.33) < 0.05: target_aspect = (4, 3)
                    elif abs(target_aspect - 1.77) < 0.05: target_aspect = (16, 9)
                    else: target_aspect = (int(target_aspect * 100), 100)
                else: target_aspect = tuple(target_aspect)

                # 3. RENDER CROPPER
                cropper_params = {'crop_target_ratio': None, 'crop_scale': 1.0, 'crop_x_offset': 0, 'crop_y_offset': 0}
                img_for_cropper = get_preview_image(extra_params=cropper_params)
                pil_img_original = Image.fromarray(img_for_cropper)
                orig_w, orig_h = pil_img_original.size

                max_width = 320
                pil_img_display = pil_img_original.copy()
                pil_img_display.thumbnail((max_width, max_width), Image.Resampling.LANCZOS)
                disp_w, disp_h = pil_img_display.size
                
                scale_factor_x = orig_w / disp_w
                scale_factor_y = orig_h / disp_h

                cropper_key = f"cropper_canvas_{rc}_{st.session_state.crop_ratio_selected}"
                box_coords = st_cropper(
                    pil_img_display, realtime_update=True, box_color='#0071E3',
                    aspect_ratio=target_aspect, return_type='box', key=cropper_key
                )

                # 4. DETEKSI LIVE DRAG & ZOOM
                if box_coords:
                    new_x = int(box_coords['left'] * scale_factor_x)
                    new_y = int(box_coords['top'] * scale_factor_y)
                    new_w = int(box_coords['width'] * scale_factor_x)

                    new_x = max(0, min(new_x, orig_w))
                    new_y = max(0, min(new_y, orig_h))
                    
                    current_target_ratio = st.session_state.crop_target_ratio if st.session_state.crop_target_ratio is not None else original_ratio
                    base_crop_w, _ = get_crop_dimensions(w, h, current_target_ratio)
                    new_scale = max(0.1, min(round(new_w / base_crop_w, 2), 1.0))

                    if (abs(new_x - st.session_state.crop_x_offset) > 2 or 
                        abs(new_y - st.session_state.crop_y_offset) > 2 or 
                        abs(new_scale - st.session_state.crop_scale) > 0.02):
                        
                        st.session_state.crop_x_offset = new_x
                        st.session_state.crop_y_offset = new_y
                        st.session_state.crop_scale = new_scale
                        st.rerun()

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("Reset Geometric", use_container_width=True):
        reset_geometric()

