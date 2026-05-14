import streamlit as st
import cv2
from image_processing.geometric_transformation import apply_ratio_crop, get_crop_dimensions
from utils.preview_helper import get_preview_image
from utils.ui_helpers import render_image_preview
from utils.constants import RATIO_OPTIONS


def render_geometric_transformation_page():
    if st.session_state.original_image is None:
        st.markdown("""
        <div class="custom-info-box">
            <strong>Notice:</strong> Please upload an image via the Image Management menu before applying any transformations.
        </div>
        """, unsafe_allow_html=True)
        return
    
    if st.session_state.processed_image is None:
        st.session_state.processed_image = st.session_state.original_image.copy()

    st.markdown("Apply geometric transformations to your image.")
    st.markdown("<br>", unsafe_allow_html=True)

    # Inisialisasi state untuk crop
    if 'crop_ratio_selected' not in st.session_state:
        st.session_state.crop_ratio_selected = "Original"
    if 'crop_scale' not in st.session_state:
        st.session_state.crop_scale = 1.0
    if 'crop_x_offset' not in st.session_state:
        st.session_state.crop_x_offset = 0
    if 'crop_y_offset' not in st.session_state:
        st.session_state.crop_y_offset = 0
    if 'temp_crop_image' not in st.session_state:
        st.session_state.temp_crop_image = None

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Rotate", "Flip", "Translation", "Scaling", "Crop"])

    # TAB 1: ROTATE
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        
        rotation_val = st.slider(
            "Rotation Angle", 0, 360,
            value=st.session_state.rotation_angle,
            key="rotation_slider_temp"
        )
        if rotation_val != st.session_state.rotation_angle:
            st.session_state.rotation_angle = rotation_val
            st.rerun()

    # TAB 2: FLIP 
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("Flip the image horizontally or vertically. Click the button to apply the flip.")
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_flip1, col_flip2, flip_spacer = st.columns([2, 2, 6]) 

        with col_flip1:
            if st.button("↔ Flip Horizontal", type="primary", use_container_width=True):
                st.session_state.processed_image = cv2.flip(st.session_state.processed_image, 1)
                st.rerun()

        with col_flip2:
            if st.button("↕ Flip Vertical", type="primary", use_container_width=True):
                st.session_state.processed_image = cv2.flip(st.session_state.processed_image, 0)
                st.rerun()

    # TAB 3: TRANSLATION 
    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("Shift the image position along the X and Y axes. Positive values move right/down, negative values move left/up.")
        st.markdown("<br>", unsafe_allow_html=True)
        
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

    # TAB 4: SCALING 
    with tab4:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("Resize the image by adjusting the scale factor. Values below 1.0 shrink the image, above 1.0 enlarge it.")
        st.markdown("<br>", unsafe_allow_html=True)
        
        scale_val = st.slider(
            "Scale Factor", 0.1, 3.0, step=0.05,
            value=st.session_state.scale_factor,
            key="scale_temp"
        )
        if scale_val != st.session_state.scale_factor:
            st.session_state.scale_factor = scale_val
            st.rerun()

    # Before image for crop (tanpa crop)
    before_image_for_crop = get_preview_image(extra_params={'crop_ratio': 1.0})

    # TAB 5: CROP 
    with tab5:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("Select an aspect ratio and adjust the cropping area by moving the frame. The image will be cropped to the selected ratio.")
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_dropdown = st.columns([1, 3])[0]
        with col_dropdown:
            selected_ratio = st.selectbox(
                "Aspect Ratio",
                list(RATIO_OPTIONS.keys()),
                index=list(RATIO_OPTIONS.keys()).index(st.session_state.crop_ratio_selected),
                key="crop_ratio_select"
            )
        
        if selected_ratio != st.session_state.crop_ratio_selected:
            st.session_state.crop_ratio_selected = selected_ratio
            st.session_state.crop_scale = 1.0
            if selected_ratio != "Original" and before_image_for_crop is not None:
                target_ratio = RATIO_OPTIONS[selected_ratio]
                h, w = before_image_for_crop.shape[:2]
                base_crop_w, base_crop_h = get_crop_dimensions(w, h, target_ratio)
                st.session_state.crop_x_offset = (w - base_crop_w) // 2
                st.session_state.crop_y_offset = (h - base_crop_h) // 2
            else:
                st.session_state.crop_x_offset = 0
                st.session_state.crop_y_offset = 0
            st.rerun()
        
        if selected_ratio != "Original" and before_image_for_crop is not None:
            target_ratio = RATIO_OPTIONS[selected_ratio]
            
            # Hitung dimensi crop berdasarkan rasio dengan skala
            h, w = before_image_for_crop.shape[:2]
            
            # SCALE RATIO - slider untuk memperkecil frame crop
            st.markdown("<br>", unsafe_allow_html=True)
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
                base_crop_w, base_crop_h = get_crop_dimensions(w, h, target_ratio)
                new_crop_w = int(base_crop_w * scale_val)
                new_crop_h = int(base_crop_h * scale_val)
                st.session_state.crop_x_offset = (w - new_crop_w) // 2
                st.session_state.crop_y_offset = (h - new_crop_h) // 2
                st.rerun()
            
            # Hitung dimensi crop target (sebelum skala)
            base_crop_w, base_crop_h = get_crop_dimensions(w, h, target_ratio)
            
            # Terapkan skala ke dimensi crop
            crop_w = int(base_crop_w * st.session_state.crop_scale)
            crop_h = int(base_crop_h * st.session_state.crop_scale)
            
            # Pastikan crop tidak melebihi dimensi gambar
            crop_w = min(crop_w, w)
            crop_h = min(crop_h, h)
            
            st.caption(f"Target crop dimension: {crop_w} x {crop_h} pixels (scale: {st.session_state.crop_scale:.0%})")
            
            # Hitung max offset
            max_x_offset = w - crop_w
            max_y_offset = h - crop_h
            
            # Validasi offset agar tidak melebihi max
            if st.session_state.crop_x_offset > max_x_offset:
                st.session_state.crop_x_offset = max(max_x_offset // 2, 0)
            if st.session_state.crop_y_offset > max_y_offset:
                st.session_state.crop_y_offset = max(max_y_offset // 2, 0)
            
            # SLIDER MOVE HORIZONTAL DAN VERTICAL 
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
                    st.session_state.crop_x_offset = 0
                    st.caption("Horizontal: centered (no space to move)")
            
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
                    st.session_state.crop_y_offset = 0
                    st.caption("Vertical: centered (no space to move)")
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Crop area preview (red box):**")

            # Tombol Apply Crop
            col_btn_left, col_btn_center, col_btn_right = st.columns([1, 1, 1])
            with col_btn_center:
                if st.button("Apply Crop", type="primary", use_container_width=True):
                    result = apply_ratio_crop(
                        before_image_for_crop,
                        target_ratio=target_ratio,
                        scale=st.session_state.crop_scale,
                        x_offset=st.session_state.crop_x_offset,
                        y_offset=st.session_state.crop_y_offset
                    )
                    st.session_state.processed_image = result
                    # Reset state
                    st.session_state.crop_ratio_selected = "Original"
                    st.session_state.crop_scale = 1.0
                    st.session_state.crop_x_offset = 0
                    st.session_state.crop_y_offset = 0
                    st.rerun()

            # Preview area crop (visualisasi dengan rectangle)
            if before_image_for_crop is not None:
                # Buat salinan gambar untuk visualisasi
                preview_with_box = before_image_for_crop.copy()
                
                # Gambar kotak crop (merah) - menggunakan opencv
                pt1 = (st.session_state.crop_x_offset, st.session_state.crop_y_offset)
                pt2 = (st.session_state.crop_x_offset + crop_w, st.session_state.crop_y_offset + crop_h)
                cv2.rectangle(preview_with_box, pt1, pt2, (255, 0, 0), 3)
                
                # Buat kolom dengan lebar lebih kecil
                col_preview_left, col_preview_center, col_preview_right = st.columns([1, 2, 1])
                with col_preview_center:
                    st.image(preview_with_box, use_container_width=True)
            
        elif before_image_for_crop is not None and selected_ratio == "Original":
            st.info("Select an aspect ratio above to crop your image.")

    # Preview image (geometric + enhancement) - hanya tampil jika crop tidak aktif
    is_crop_active = st.session_state.crop_ratio_selected != "Original"
    
    if not is_crop_active:
        preview_image = get_preview_image()

        st.markdown("<hr style='margin: 2.5rem 0;' />", unsafe_allow_html=True)
        st.markdown("### Image Preview")

        render_image_preview(st.session_state.original_image, preview_image)