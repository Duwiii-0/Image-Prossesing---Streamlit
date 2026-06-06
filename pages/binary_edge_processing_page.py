import streamlit as st
import numpy as np
from PIL import Image
from utils.preview_helper import get_preview_image
from utils.state_manager import reset_binary_edge_state
from utils.constants import (
    THRESHOLD_METHODS, ADAPTIVE_METHODS, EDGE_METHODS, 
    SOBEL_DIRECTIONS, MORPH_OPERATIONS
)

def render_binary_edge_processing_page():
    tab1, tab2, tab3 = st.tabs([
        "Threshold", 
        "Edge", 
        "Morph"
    ])

    # TAB 1: THRESHOLDING 
    with tab1:
        sub_tab1, sub_tab2 = st.tabs(["Simple", "Adaptive"])
        
        with sub_tab1:
            threshold_val = st.slider(
                "Value", 0, 255,
                value=st.session_state.binary_threshold_value,
                key="threshold_val_temp"
            )
            if threshold_val != st.session_state.binary_threshold_value:
                st.session_state.binary_threshold_value = threshold_val
                st.rerun()
            
            method_val = st.selectbox(
                "Method",
                THRESHOLD_METHODS,
                index=0 if st.session_state.binary_threshold_method == "Binary" else 1,
                key="threshold_method_temp"
            )
            if method_val != st.session_state.binary_threshold_method:
                st.session_state.binary_threshold_method = method_val
                st.rerun()
            
            if st.button("Apply Simple", type="primary", use_container_width=True):
                st.session_state.binary_edge_mode = "threshold"
                st.rerun()
        
        with sub_tab2:
            adaptive_method = st.selectbox(
                "Method",
                ADAPTIVE_METHODS,
                index=0 if st.session_state.binary_adaptive_method == "Mean" else 1,
                key="adaptive_method_temp"
            )
            if adaptive_method != st.session_state.binary_adaptive_method:
                st.session_state.binary_adaptive_method = adaptive_method
                st.rerun()
            
            block_size = st.slider(
                "Block", 3, 31, step=2,
                value=st.session_state.binary_adaptive_block,
                key="adaptive_block_temp"
            )
            if block_size != st.session_state.binary_adaptive_block:
                st.session_state.binary_adaptive_block = block_size
                st.rerun()
            
            c_val = st.slider(
                "C", 0, 20,
                value=st.session_state.binary_adaptive_c,
                key="adaptive_c_temp"
            )
            if c_val != st.session_state.binary_adaptive_c:
                st.session_state.binary_adaptive_c = c_val
                st.rerun()
            
            if st.button("Apply Adaptive", type="primary", use_container_width=True):
                st.session_state.binary_edge_mode = "adaptive_threshold"
                st.rerun()

    # TAB 2: EDGE DETECTION 
    with tab2:
        edge_method = st.selectbox(
            "Method",
            EDGE_METHODS,
            index=EDGE_METHODS.index(st.session_state.edge_method),
            key="edge_method_temp"
        )
        if edge_method != st.session_state.edge_method:
            st.session_state.edge_method = edge_method
            st.rerun()
        
        if st.session_state.edge_method == "Canny":
            low_val = st.slider("Low", 0, 255, value=st.session_state.edge_low, key="edge_low_temp")
            if low_val != st.session_state.edge_low:
                st.session_state.edge_low = low_val
                st.rerun()
            high_val = st.slider("High", 0, 255, value=st.session_state.edge_high, key="edge_high_temp")
            if high_val != st.session_state.edge_high:
                st.session_state.edge_high = high_val
                st.rerun()
        
        if st.session_state.edge_method == "Sobel":
            sobel_dir = st.radio("Dir", SOBEL_DIRECTIONS, index=SOBEL_DIRECTIONS.index(st.session_state.edge_sobel_direction), key="sobel_dir_temp", horizontal=True)
            if sobel_dir != st.session_state.edge_sobel_direction:
                st.session_state.edge_sobel_direction = sobel_dir
                st.rerun()
            
            kernel_val = st.slider("Kernel", 1, 7, step=2, value=st.session_state.edge_kernel, key="edge_kernel_temp")
            if kernel_val != st.session_state.edge_kernel:
                st.session_state.edge_kernel = kernel_val
                st.rerun()
        
        if st.session_state.edge_method in ["LoG", "Laplacian"]:
            kernel_val = st.slider("Kernel", 1, 7, step=2, value=st.session_state.edge_kernel, key="edge_kernel_log_lap_temp")
            if kernel_val != st.session_state.edge_kernel:
                st.session_state.edge_kernel = kernel_val
                st.rerun()

        if st.button("Apply Edge", type="primary", use_container_width=True):
            st.session_state.binary_edge_mode = "edge"
            st.rerun()

    # TAB 3: MORPHOLOGY 
    with tab3:
        morph_op = st.selectbox("Op", MORPH_OPERATIONS, index=0 if st.session_state.morph_operation == "Erosion" else 1, key="morph_op_temp")
        if morph_op != st.session_state.morph_operation:
            st.session_state.morph_operation = morph_op
            st.rerun()
        
        kernel_size = st.slider("Kernel", 3, 15, step=2, value=st.session_state.morph_kernel, key="morph_kernel_temp")
        if kernel_size != st.session_state.morph_kernel:
            st.session_state.morph_kernel = kernel_size
            st.rerun()
        
        iterations = st.slider("Iter", 1, 5, value=st.session_state.morph_iterations, key="morph_iter_temp")
        if iterations != st.session_state.morph_iterations:
            st.session_state.morph_iterations = iterations
            st.rerun()
        
        if st.button("Apply Morph", type="primary", use_container_width=True):
            st.session_state.binary_edge_mode = "morphology"
            st.rerun()

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("Reset Binary & Edge", use_container_width=True):
        reset_binary_edge_state()
        st.rerun()
