import streamlit as st
import numpy as np
from PIL import Image
from utils.preview_helper import get_preview_image
from utils.ui_helpers import render_image_preview, render_reset_and_save_buttons, render_section_header
from utils.constants import (
    THRESHOLD_METHODS, ADAPTIVE_METHODS, EDGE_METHODS, 
    SOBEL_DIRECTIONS, MORPH_OPERATIONS
)


def render_binary_edge_processing_page():
    render_section_header(
        title="Binary & Edge Processing",
        description="Thresholding, Edge Detection, and Morphological Operations.",
        icon="⬛"
    )
    
    # Upload File
    uploaded_file = st.file_uploader(
        "Select an Image (JPG, PNG, BMP)",
        type=["jpg", "png", "jpeg", "bmp"],
        key="binary_edge_processing_uploader"
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

    if 'binary_edge_mode' not in st.session_state:
        st.session_state.binary_edge_mode = "none"

    tab1, tab2, tab3 = st.tabs([
        "Thresholding", 
        "Edge Detection", 
        "Morphology"
    ])

    before_image = get_preview_image(extra_params={'binary_edge_mode': 'none'})

    # TAB 1: THRESHOLDING 
    with tab1:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        st.markdown("""
        <p><strong>Thresholding</strong> - Converts image to black and white based on intensity level.</p>
        <p style="font-size: 0.85rem; color: #64748B;"><em>Best for separating objects from high-contrast backgrounds. Ideal for document scanning and text extraction.</em></p>
        """, unsafe_allow_html=True)
        
        sub_tab1, sub_tab2 = st.tabs(["Simple Threshold", "Adaptive Threshold"])
        
        with sub_tab1:
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            threshold_val = st.slider(
                "Threshold Value", 0, 255,
                value=st.session_state.binary_threshold_value,
                key="threshold_val_temp"
            )
            if threshold_val != st.session_state.binary_threshold_value:
                st.session_state.binary_threshold_value = threshold_val
                st.rerun()
            
            method_val = st.selectbox(
                "Threshold Method",
                THRESHOLD_METHODS,
                index=0 if st.session_state.binary_threshold_method == "Binary" else 1,
                key="threshold_method_temp"
            )
            if method_val != st.session_state.binary_threshold_method:
                st.session_state.binary_threshold_method = method_val
                st.rerun()
            
            after_image = get_preview_image(extra_params={
                'binary_edge_mode': 'threshold',
                'binary_threshold_value': st.session_state.binary_threshold_value,
                'binary_threshold_method': st.session_state.binary_threshold_method
            })

            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

            col_btn = st.columns([1, 1, 1])[1]  
            with col_btn:
                if st.button("Apply Simple Threshold", type="primary", use_container_width=True):
                    st.session_state.binary_edge_mode = "threshold"
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)
            render_image_preview(before_image, after_image)
        
        with sub_tab2:
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            adaptive_method = st.selectbox(
                "Adaptive Method",
                ADAPTIVE_METHODS,
                index=0 if st.session_state.binary_adaptive_method == "Mean" else 1,
                key="adaptive_method_temp"
            )
            if adaptive_method != st.session_state.binary_adaptive_method:
                st.session_state.binary_adaptive_method = adaptive_method
                st.rerun()
            
            block_size = st.slider(
                "Block Size", 3, 31, step=2,
                value=st.session_state.binary_adaptive_block,
                key="adaptive_block_temp"
            )
            if block_size != st.session_state.binary_adaptive_block:
                st.session_state.binary_adaptive_block = block_size
                st.rerun()
            
            c_val = st.slider(
                "Constant C", 0, 20,
                value=st.session_state.binary_adaptive_c,
                key="adaptive_c_temp"
            )
            if c_val != st.session_state.binary_adaptive_c:
                st.session_state.binary_adaptive_c = c_val
                st.rerun()
            
            after_image = get_preview_image(extra_params={
                'binary_edge_mode': 'adaptive_threshold',
                'binary_adaptive_method': st.session_state.binary_adaptive_method,
                'binary_adaptive_block': st.session_state.binary_adaptive_block,
                'binary_adaptive_c': st.session_state.binary_adaptive_c
            })

            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

            col_btn = st.columns([1, 1, 1])[1]
            with col_btn:
                if st.button("Apply Adaptive Threshold", type="primary", use_container_width=True):
                    st.session_state.binary_edge_mode = "adaptive_threshold"
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)
            render_image_preview(before_image, after_image)

    # TAB 2: EDGE DETECTION 
    with tab2:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        st.markdown("""
        <p><strong>Edge Detection</strong> - Identifies boundaries where image intensity changes sharply.</p>
        <p style="font-size: 0.85rem; color: #64748B;"><em>Best for shape recognition, object detection, and creating sketch-like effects.</em></p>
        """, unsafe_allow_html=True)
        
        edge_method = st.selectbox(
            "Edge Detection Method",
            EDGE_METHODS,
            index=EDGE_METHODS.index(st.session_state.edge_method),
            key="edge_method_temp"
        )
        if edge_method != st.session_state.edge_method:
            st.session_state.edge_method = edge_method
            st.rerun()
        
        if st.session_state.edge_method == "Canny":
            low_val = st.slider("Low Threshold", 0, 255, value=st.session_state.edge_low, key="edge_low_temp")
            if low_val != st.session_state.edge_low:
                st.session_state.edge_low = low_val
                st.rerun()
            high_val = st.slider("High Threshold", 0, 255, value=st.session_state.edge_high, key="edge_high_temp")
            if high_val != st.session_state.edge_high:
                st.session_state.edge_high = high_val
                st.rerun()
        
        if st.session_state.edge_method == "Sobel":
            sobel_dir = st.radio(
                "Direction",
                SOBEL_DIRECTIONS,
                index=SOBEL_DIRECTIONS.index(st.session_state.edge_sobel_direction),
                key="sobel_dir_temp",
                horizontal=True
            )
            if sobel_dir != st.session_state.edge_sobel_direction:
                st.session_state.edge_sobel_direction = sobel_dir
                st.rerun()
            
            kernel_val = st.slider("Kernel Size", 1, 7, step=2, value=st.session_state.edge_kernel, key="edge_kernel_temp")
            if kernel_val != st.session_state.edge_kernel:
                st.session_state.edge_kernel = kernel_val
                st.rerun()
        
        if st.session_state.edge_method == "LoG":
            sigma_val = st.slider("Sigma (Blur Strength)", 0.5, 5.0, step=0.5, value=st.session_state.edge_log_sigma, key="log_sigma_temp")
            if sigma_val != st.session_state.edge_log_sigma:
                st.session_state.edge_log_sigma = sigma_val
                st.rerun()
            
            kernel_val = st.slider("Kernel Size", 1, 7, step=2, value=st.session_state.edge_kernel, key="edge_kernel_log_temp")
            if kernel_val != st.session_state.edge_kernel:
                st.session_state.edge_kernel = kernel_val
                st.rerun()
        
        if st.session_state.edge_method in ["Laplacian"]:
            kernel_val = st.slider("Kernel Size", 1, 7, step=2, value=st.session_state.edge_kernel, key="edge_kernel_lap_temp")
            if kernel_val != st.session_state.edge_kernel:
                st.session_state.edge_kernel = kernel_val
                st.rerun()
        
        after_image = get_preview_image(extra_params={
            'binary_edge_mode': 'edge',
            'edge_method': st.session_state.edge_method,
            'edge_low': st.session_state.edge_low,
            'edge_high': st.session_state.edge_high,
            'edge_kernel': st.session_state.edge_kernel,
            'edge_sobel_direction': st.session_state.edge_sobel_direction,
            'edge_log_sigma': st.session_state.edge_log_sigma
        })

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        col_btn = st.columns([1, 1, 1])[1]
        with col_btn:
            if st.button("Apply Edge Detection", type="primary", use_container_width=True):
                st.session_state.binary_edge_mode = "edge"
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
        render_image_preview(before_image, after_image)

    # TAB 3: MORPHOLOGY 
    with tab3:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        st.markdown("""
        <p><strong>Morphology</strong> - Modifies object shapes using erosion and dilation.</p>
        <p style="font-size: 0.85rem; color: #64748B;"><em>Erosion shrinks objects and removes small noise. Dilation expands objects and fills small holes.</em></p>
        """, unsafe_allow_html=True)
        
        morph_op = st.selectbox(
            "Operation",
            MORPH_OPERATIONS,
            index=0 if st.session_state.morph_operation == "Erosion" else 1,
            key="morph_op_temp"
        )
        if morph_op != st.session_state.morph_operation:
            st.session_state.morph_operation = morph_op
            st.rerun()
        
        kernel_size = st.slider(
            "Kernel Size", 3, 15, step=2,
            value=st.session_state.morph_kernel,
            key="morph_kernel_temp"
        )
        if kernel_size != st.session_state.morph_kernel:
            st.session_state.morph_kernel = kernel_size
            st.rerun()
        
        iterations = st.slider(
            "Iterations", 1, 5,
            value=st.session_state.morph_iterations,
            key="morph_iter_temp"
        )
        if iterations != st.session_state.morph_iterations:
            st.session_state.morph_iterations = iterations
            st.rerun()
        
        after_image = get_preview_image(extra_params={
            'binary_edge_mode': 'morphology',
            'morph_operation': st.session_state.morph_operation,
            'morph_kernel': st.session_state.morph_kernel,
            'morph_iterations': st.session_state.morph_iterations
        })

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        col_btn = st.columns([1, 1, 1])[1]
        with col_btn:
            if st.button("Apply Morphology", type="primary", use_container_width=True):
                st.session_state.binary_edge_mode = "morphology"
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
        render_image_preview(before_image, after_image)