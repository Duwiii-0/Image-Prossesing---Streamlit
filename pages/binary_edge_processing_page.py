import streamlit as st
from utils.preview_helper import get_preview_image
from utils.ui_helpers import render_image_preview
from utils.constants import (
    THRESHOLD_METHODS, ADAPTIVE_METHODS, EDGE_METHODS, 
    SOBEL_DIRECTIONS, MORPH_OPERATIONS
)


def render_binary_edge_processing_page():
    if st.session_state.original_image is None:
        st.markdown("""
        <div class="custom-info-box">
            <strong>Notice:</strong> Please upload an image via the Image Management menu before applying any enhancements.
        </div>
        """, unsafe_allow_html=True)
        return
    
    if st.session_state.processed_image is None:
        st.session_state.processed_image = st.session_state.original_image.copy()

    st.markdown("Binary & Edge Processing - Thresholding, Edge Detection, and Morphological Operations.")
    st.markdown("<br>", unsafe_allow_html=True)

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
        st.markdown("""
        **Thresholding** - Converts image to black and white based on intensity level.
        
        Best for separating objects from high-contrast backgrounds. Ideal for document scanning and text extraction.
        """)
        
        sub_tab1, sub_tab2 = st.tabs(["Simple Threshold", "Adaptive Threshold"])
        
        with sub_tab1:
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

            st.markdown("<br>", unsafe_allow_html=True)

            col_btn = st.columns([1, 1, 1])[1]  
            with col_btn:
                if st.button("Apply Simple Threshold", type="primary", use_container_width=True):
                    st.session_state.binary_edge_mode = "threshold"
                    st.rerun()

            st.markdown("<hr style='margin: 2rem 0;' />", unsafe_allow_html=True)
            st.markdown("### Image Preview")
            
            render_image_preview(before_image, after_image)
        
        with sub_tab2:
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

            st.markdown("<br>", unsafe_allow_html=True)

            col_btn = st.columns([1, 1, 1])[1]
            with col_btn:
                if st.button("Apply Adaptive Threshold", type="primary", use_container_width=True):
                    st.session_state.binary_edge_mode = "adaptive_threshold"
                    st.rerun()

            st.markdown("<hr style='margin: 2rem 0;' />", unsafe_allow_html=True)
            st.markdown("### Image Preview")
            
            render_image_preview(before_image, after_image)

    # TAB 2: EDGE DETECTION 
    with tab2:
        st.markdown("""
        **Edge Detection** - Identifies boundaries where image intensity changes sharply.
        
        Best for shape recognition, object detection, and creating sketch-like effects.
        """)
        
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

        st.markdown("<br>", unsafe_allow_html=True)

        col_btn = st.columns([1, 1, 1])[1]
        with col_btn:
            if st.button("Apply Edge Detection", type="primary", use_container_width=True):
                st.session_state.binary_edge_mode = "edge"
                st.rerun()

        st.markdown("<hr style='margin: 2rem 0;' />", unsafe_allow_html=True)
        st.markdown("### Image Preview")
        
        render_image_preview(before_image, after_image)

    # TAB 3: MORPHOLOGY 
    with tab3:
        st.markdown("""
        **Morphology** - Modifies object shapes using erosion and dilation.
        
        Erosion shrinks objects and removes small noise. Dilation expands objects and fills small holes.
        """)
        
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

        st.markdown("<br>", unsafe_allow_html=True)

        col_btn = st.columns([1, 1, 1])[1]
        with col_btn:
            if st.button("Apply Morphology", type="primary", use_container_width=True):
                st.session_state.binary_edge_mode = "morphology"
                st.rerun()

        st.markdown("<hr style='margin: 2rem 0;' />", unsafe_allow_html=True)
        st.markdown("### Image Preview")
        
        render_image_preview(before_image, after_image)