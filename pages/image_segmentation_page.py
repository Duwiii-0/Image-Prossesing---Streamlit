import streamlit as st
import numpy as np
from PIL import Image
from utils.preview_helper import get_preview_image
from utils.state_manager import reset_segmentation_state
from utils.ui_helpers import render_image_preview, render_reset_and_save_buttons, render_section_header
from utils.constants import (
    SEG_THRESHOLD_METHODS, SEG_EDGE_METHODS, SEG_REGION_METHODS, SEG_ADAPTIVE_METHODS
)


def render_image_segmentation_page():
    render_section_header(
        title="Image Segmentation",
        description="Segment images using threshold-based, edge-based, and region-based methods.",
        icon="✂️"
    )
    
    # Upload File
    uploaded_file = st.file_uploader(
        "Select an Image (JPG, PNG, BMP)",
        type=["jpg", "png", "jpeg", "bmp"],
        key="image_segmentation_uploader"
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

    if 'segmentation_mode' not in st.session_state:
        st.session_state.segmentation_mode = "none"

    tab1, tab2, tab3 = st.tabs([
        "Threshold-based", 
        "Edge-based", 
        "Region-based"
    ])

    # Gambar sebelum segmentation (tanpa efek)
    before_image = get_preview_image(extra_params={'segmentation_mode': 'none'})

    # ==================== TAB 1: THRESHOLD-BASED ====================
    with tab1:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        st.markdown("""
        <p><strong>Threshold-based Segmentation</strong> - Separates objects from background based on intensity values.</p>
        <p style="font-size: 0.85rem; color: #64748B;"><em>Best for images with high contrast between objects and background.</em></p>
        """, unsafe_allow_html=True)
        
        sub_tab1, sub_tab2, sub_tab3 = st.tabs(["Global Threshold", "Adaptive Threshold", "Otsu Threshold"])
        
        # SUB-TAB 1: Global Threshold
        with sub_tab1:
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            
            threshold_val = st.slider(
                "Threshold Value", 0, 255,
                value=st.session_state.seg_threshold_value,
                key="seg_threshold_val_temp"
            )
            if threshold_val != st.session_state.seg_threshold_value:
                st.session_state.seg_threshold_value = threshold_val
                st.rerun()
            
            after_image = get_preview_image(extra_params={
                'segmentation_mode': 'threshold_global',
                'seg_threshold_value': st.session_state.seg_threshold_value
            })

            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

            col_btn = st.columns([1, 1, 1])[1]
            with col_btn:
                if st.button("Apply Global Threshold", type="primary", use_container_width=True):
                    st.session_state.segmentation_mode = "threshold_global"
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)
            render_image_preview(before_image, after_image)
        
        # SUB-TAB 2: Adaptive Threshold
        with sub_tab2:
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            
            adaptive_method = st.selectbox(
                "Adaptive Method",
                SEG_ADAPTIVE_METHODS,
                index=0 if st.session_state.seg_adaptive_method == "mean" else 1,
                key="seg_adaptive_method_temp"
            )
            if adaptive_method != st.session_state.seg_adaptive_method:
                st.session_state.seg_adaptive_method = adaptive_method
                st.rerun()
            
            col1, col2 = st.columns(2)
            with col1:
                block_size = st.slider(
                    "Block Size", 3, 31, step=2,
                    value=st.session_state.seg_adaptive_block,
                    key="seg_adaptive_block_temp"
                )
                if block_size != st.session_state.seg_adaptive_block:
                    st.session_state.seg_adaptive_block = block_size
                    st.rerun()
            with col2:
                c_val = st.slider(
                    "Constant C", 0, 20,
                    value=st.session_state.seg_adaptive_c,
                    key="seg_adaptive_c_temp"
                )
                if c_val != st.session_state.seg_adaptive_c:
                    st.session_state.seg_adaptive_c = c_val
                    st.rerun()
            
            after_image = get_preview_image(extra_params={
                'segmentation_mode': 'threshold_adaptive',
                'seg_adaptive_method': st.session_state.seg_adaptive_method,
                'seg_adaptive_block': st.session_state.seg_adaptive_block,
                'seg_adaptive_c': st.session_state.seg_adaptive_c
            })

            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

            col_btn = st.columns([1, 1, 1])[1]
            with col_btn:
                if st.button("Apply Adaptive Threshold", type="primary", use_container_width=True):
                    st.session_state.segmentation_mode = "threshold_adaptive"
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)
            render_image_preview(before_image, after_image)
        
        # SUB-TAB 3: Otsu Threshold
        with sub_tab3:
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            st.markdown("""
            <p><strong>Otsu's Method</strong> - Automatically determines optimal threshold value.</p>
            <p style="font-size: 0.85rem; color: #64748B;"><em>Best for bimodal histograms where objects and background have distinct intensity peaks.</em></p>
            """, unsafe_allow_html=True)
            
            after_image = get_preview_image(extra_params={
                'segmentation_mode': 'threshold_otsu'
            })

            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

            col_btn = st.columns([1, 1, 1])[1]
            with col_btn:
                if st.button("Apply Otsu Threshold", type="primary", use_container_width=True):
                    st.session_state.segmentation_mode = "threshold_otsu"
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)
            render_image_preview(before_image, after_image)

    # ==================== TAB 2: EDGE-BASED ====================
    with tab2:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        st.markdown("""
        <p><strong>Edge-based Segmentation</strong> - Detects boundaries where image intensity changes sharply.</p>
        <p style="font-size: 0.85rem; color: #64748B;"><em>Best for shape recognition, object boundaries, and structural analysis.</em></p>
        """, unsafe_allow_html=True)
        
        edge_method = st.selectbox(
            "Edge Detection Method",
            SEG_EDGE_METHODS,
            index=SEG_EDGE_METHODS.index(st.session_state.seg_edge_method),
            key="seg_edge_method_temp"
        )
        if edge_method != st.session_state.seg_edge_method:
            st.session_state.seg_edge_method = edge_method
            st.rerun()
        
        # Canny parameters
        if st.session_state.seg_edge_method == "Canny":
            col1, col2 = st.columns(2)
            with col1:
                low_val = st.slider("Low Threshold", 0, 255, value=st.session_state.seg_edge_low, key="seg_edge_low_temp")
                if low_val != st.session_state.seg_edge_low:
                    st.session_state.seg_edge_low = low_val
                    st.rerun()
            with col2:
                high_val = st.slider("High Threshold", 0, 255, value=st.session_state.seg_edge_high, key="seg_edge_high_temp")
                if high_val != st.session_state.seg_edge_high:
                    st.session_state.seg_edge_high = high_val
                    st.rerun()
        
        # Sobel parameters
        elif st.session_state.seg_edge_method == "Sobel":
            col1, col2 = st.columns(2)
            with col1:
                kernel_val = st.slider("Kernel Size", 1, 7, step=2, value=st.session_state.seg_edge_kernel, key="seg_edge_kernel_temp")
                if kernel_val != st.session_state.seg_edge_kernel:
                    st.session_state.seg_edge_kernel = kernel_val
                    st.rerun()
            with col2:
                sobel_dir = st.selectbox(
                    "Direction",
                    ["both", "x", "y"],
                    index=["both", "x", "y"].index(st.session_state.seg_sobel_direction),
                    key="seg_sobel_dir_temp"
                )
                if sobel_dir != st.session_state.seg_sobel_direction:
                    st.session_state.seg_sobel_direction = sobel_dir
                    st.rerun()
        
        # Laplacian parameters
        else:
            kernel_val = st.slider("Kernel Size", 1, 7, step=2, value=st.session_state.seg_edge_kernel, key="seg_edge_kernel_lap_temp")
            if kernel_val != st.session_state.seg_edge_kernel:
                st.session_state.seg_edge_kernel = kernel_val
                st.rerun()
        
        # Determine which edge mode to use
        edge_mode_map = {
            "Canny": "edge_canny",
            "Sobel": "edge_sobel",
            "Laplacian": "edge_laplacian"
        }
        
        after_image = get_preview_image(extra_params={
            'segmentation_mode': edge_mode_map[st.session_state.seg_edge_method],
            'seg_edge_low': st.session_state.seg_edge_low,
            'seg_edge_high': st.session_state.seg_edge_high,
            'seg_edge_kernel': st.session_state.seg_edge_kernel,
            'seg_sobel_direction': st.session_state.seg_sobel_direction
        })

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        col_btn = st.columns([1, 1, 1])[1]
        with col_btn:
            if st.button("Apply Edge Detection", type="primary", use_container_width=True):
                st.session_state.segmentation_mode = edge_mode_map[st.session_state.seg_edge_method]
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
        render_image_preview(before_image, after_image)

    # ==================== TAB 3: REGION-BASED ====================
    with tab3:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        st.markdown("""
        <p><strong>Region-based Segmentation</strong> - Groups pixels with similar properties into regions.</p>
        <p style="font-size: 0.85rem; color: #64748B;"><em>Best for complex images where thresholding alone is insufficient.</em></p>
        """, unsafe_allow_html=True)
        
        region_method = st.selectbox(
            "Region Method",
            SEG_REGION_METHODS,
            index=SEG_REGION_METHODS.index(st.session_state.seg_region_method),
            key="seg_region_method_temp"
        )
        if region_method != st.session_state.seg_region_method:
            st.session_state.seg_region_method = region_method
            st.rerun()
        
        # Region Growing parameters
        if st.session_state.seg_region_method == "Region Growing":
            threshold_val = st.slider(
                "Intensity Threshold", 0, 50,
                value=st.session_state.seg_region_threshold,
                key="seg_region_threshold_temp"
            )
            if threshold_val != st.session_state.seg_region_threshold:
                st.session_state.seg_region_threshold = threshold_val
                st.rerun()
            st.caption("Lower values = stricter region growing. Higher values = more inclusive.")
        
        # K-Means parameters
        elif st.session_state.seg_region_method == "K-Means":
            k_val = st.slider(
                "Number of Clusters (K)", 2, 8,
                value=st.session_state.seg_kmeans_k,
                key="seg_kmeans_k_temp"
            )
            if k_val != st.session_state.seg_kmeans_k:
                st.session_state.seg_kmeans_k = k_val
                st.rerun()
            st.caption("More clusters = more detailed color segmentation.")
        
        # Contour parameters
        elif st.session_state.seg_region_method == "Contour":
            contour_mode = st.selectbox(
                "Contour Mode",
                ["external", "all"],
                index=0 if st.session_state.seg_contour_mode == "external" else 1,
                key="seg_contour_mode_temp"
            )
            if contour_mode != st.session_state.seg_contour_mode:
                st.session_state.seg_contour_mode = contour_mode
                st.rerun()
            st.caption("External = only outer boundaries. All = all contours including inner holes.")
        
        # Watershed - no parameters
        else:
            st.info("Watershed algorithm automatically segments overlapping objects.")
        
        # Determine which region mode to use
        region_mode_map = {
            "Region Growing": "region_growing",
            "K-Means": "kmeans",
            "Contour": "contour",
            "Watershed": "watershed"
        }
        
        after_image = get_preview_image(extra_params={
            'segmentation_mode': region_mode_map[st.session_state.seg_region_method],
            'seg_region_threshold': st.session_state.seg_region_threshold,
            'seg_kmeans_k': st.session_state.seg_kmeans_k,
            'seg_contour_mode': st.session_state.seg_contour_mode
        })

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        col_btn = st.columns([1, 1, 1])[1]
        with col_btn:
            if st.button("Apply Region Segmentation", type="primary", use_container_width=True):
                st.session_state.segmentation_mode = region_mode_map[st.session_state.seg_region_method]
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
        render_image_preview(before_image, after_image)

    st.markdown("<hr/>", unsafe_allow_html=True)
    
    # Reset and Save buttons - FIX: tambah st.rerun() di reset_callback
    def reset_segmentation():
        reset_segmentation_state()
        st.rerun()
    
    preview_image = get_preview_image()
    render_reset_and_save_buttons(
        reset_callback=reset_segmentation,
        image_to_save=preview_image
    )