import streamlit as st
import cv2
import numpy as np
from PIL import Image
from image_processing.geometric_transformation import get_crop_dimensions
from utils.preview_helper import get_preview_image
from utils.ui_helpers import render_image_preview, render_reset_and_save_buttons, render_section_header
from utils.constants import RATIO_OPTIONS


def render_geometric_transformation_page():
    render_section_header(
        title="Geometric Transformation",
        description="Rotate, flip, scale, and crop your image.",
        icon="📐"
    )
    
    # Upload File
    uploaded_file = st.file_uploader(
        "Select an Image (JPG, PNG, BMP)",
        type=["jpg", "png", "jpeg", "bmp"],
        key="geometric_transformation_uploader"
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

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Rotate", "Flip", "Translation", "Scaling", "Crop"])

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
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        
        rotation_val = st.slider(
            "Rotation Angle", 0, 360,
            value=st.session_state.rotation_angle,
            key="rotation_slider_temp"
        )
        if rotation_val != st.session_state.rotation_angle:
            st.session_state.rotation_angle = rotation_val
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        preview_image = get_preview_image()
        render_image_preview(st.session_state.original_image, preview_image)

    # TAB 2: FLIP 
    with tab2:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        st.markdown("<p>Flip the image horizontally or vertically. Click the button to apply the flip.</p>", unsafe_allow_html=True)
        
        col_flip1, col_flip2, flip_spacer = st.columns([2, 2, 6]) 

        with col_flip1:
            if st.button("↔ Flip Horizontal", type="primary", use_container_width=True):
                st.session_state.processed_image = cv2.flip(st.session_state.processed_image, 1)
                st.rerun()

        with col_flip2:
            if st.button("↕ Flip Vertical", type="primary", use_container_width=True):
                st.session_state.processed_image = cv2.flip(st.session_state.processed_image, 0)
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        preview_image = get_preview_image()
        render_image_preview(st.session_state.original_image, preview_image)

    # TAB 3: TRANSLATION 
    with tab3:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        st.markdown("<p>Shift the image position along the X and Y axes. Positive values move right/down, negative values move left/up.</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            trans_x_val = st.slider(
                "Shift X", -500, 500,
                value=st.session_state.translate_x,
                key="trans_x_temp"
            )
            if trans_x_val != st.session_state.translate_x:
                st.session_state.translate_x = trans_x_val
                st.rerun()
        with col2:
            trans_y_val = st.slider(
                "Shift Y", -500, 500,
                value=st.session_state.translate_y,
                key="trans_y_temp"
            )
            if trans_y_val != st.session_state.translate_y:
                st.session_state.translate_y = trans_y_val
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        preview_image = get_preview_image()
        render_image_preview(st.session_state.original_image, preview_image)

    # TAB 4: SCALING 
    with tab4:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        st.markdown("<p>Resize the image by adjusting the scale factor. Values below 1.0 shrink the image, above 1.0 enlarge it.</p>", unsafe_allow_html=True)
        
        scale_val = st.slider(
            "Scale Factor", 0.1, 3.0, step=0.05,
            value=st.session_state.scale_factor,
            key="scale_temp"
        )
        if scale_val != st.session_state.scale_factor:
            st.session_state.scale_factor = scale_val
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        preview_image = get_preview_image()
        render_image_preview(st.session_state.original_image, preview_image)

    # TAB 5: CROP 
    with tab5:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        st.markdown("<p>Select an aspect ratio and adjust the cropping area by moving the frame.</p>", unsafe_allow_html=True)
        
        col_dropdown = st.columns([1, 3])[0]
        with col_dropdown:
            selected_ratio = st.selectbox(
                "Aspect Ratio",
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
        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        scale_val = st.slider(
            "Crop Scale (Zoom Out)", 
            0.3, 1.0, 
            step=0.01,
            value=st.session_state.crop_scale,
            key="crop_scale_slider",
            help="Reduce crop frame to expand visible area"
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
        
        st.caption(f"Target crop dimension: {crop_w} x {crop_h} pixels (scale: {st.session_state.crop_scale:.0%})")
        
        max_x_offset = w - crop_w
        max_y_offset = h - crop_h
        
        if st.session_state.crop_x_offset > max_x_offset:
            st.session_state.crop_x_offset = max(max_x_offset // 2, 0)
        if st.session_state.crop_y_offset > max_y_offset:
            st.session_state.crop_y_offset = max(max_y_offset // 2, 0)
        
        col_slider_x, col_slider_y = st.columns(2)
        
        with col_slider_x:
            if max_x_offset > 0:
                x_offset = st.slider(
                    "Move Horizontal (X)", 
                    0, max_x_offset,
                    value=min(st.session_state.crop_x_offset, max_x_offset),
                    key="crop_x_slider"
                )
                if x_offset != st.session_state.crop_x_offset:
                    st.session_state.crop_x_offset = x_offset
                    st.rerun()
            else:
                st.caption("Horizontal: centered")
        
        with col_slider_y:
            if max_y_offset > 0:
                y_offset = st.slider(
                    "Move Vertical (Y)", 
                    0, max_y_offset,
                    value=min(st.session_state.crop_y_offset, max_y_offset),
                    key="crop_y_slider"
                )
                if y_offset != st.session_state.crop_y_offset:
                    st.session_state.crop_y_offset = y_offset
                    st.rerun()
            else:
                st.caption("Vertical: centered")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Crop Preview")
        
        # Preview with red box
        preview_with_box = before_image_for_crop.copy()
        
        if len(preview_with_box.shape) == 2:
            preview_with_box = cv2.cvtColor(preview_with_box, cv2.COLOR_GRAY2RGB)
        elif preview_with_box.shape[2] == 1:
            preview_with_box = cv2.cvtColor(preview_with_box, cv2.COLOR_GRAY2RGB)
        elif preview_with_box.shape[2] == 4:
            preview_with_box = cv2.cvtColor(preview_with_box, cv2.COLOR_RGBA2RGB)
        
        cropped_result = preview_with_box[
            st.session_state.crop_y_offset:st.session_state.crop_y_offset + crop_h,
            st.session_state.crop_x_offset:st.session_state.crop_x_offset + crop_w
        ].copy()
        
        pt1 = (st.session_state.crop_x_offset, st.session_state.crop_y_offset)
        pt2 = (st.session_state.crop_x_offset + crop_w, st.session_state.crop_y_offset + crop_h)
        
        cv2.rectangle(preview_with_box, pt1, pt2, (0, 0, 0), 2)       
        cv2.rectangle(preview_with_box, pt1, pt2, (255, 60, 60), 3)   
        
        render_image_preview(
            preview_with_box, 
            cropped_result,
            title_left="Crop area preview (red box)",
            title_right="Cropped Result"
        )

    st.markdown("<hr/>", unsafe_allow_html=True)
    
    # Reset and Save buttons
    preview_image = get_preview_image()
    render_reset_and_save_buttons(
        reset_callback=lambda: None,
        image_to_save=preview_image
    )