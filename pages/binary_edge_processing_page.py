import streamlit as st
from utils.state_manager import reset_binary_edge_state
from utils.constants import (
    THRESHOLD_METHODS, ADAPTIVE_METHODS, EDGE_METHODS, 
    SOBEL_DIRECTIONS, MORPH_OPERATIONS
)

def render_binary_edge_processing_page():
    tab1, tab2, tab3 = st.tabs(["Threshold", "Edge", "Morph"])

    # ========== TAB 1: THRESHOLD ==========
    with tab1:
        if 'thresh_mode' not in st.session_state:
            st.session_state.thresh_mode = "None"
        
        threshold_mode = st.selectbox(
            "Mode", ["None", "Simple", "Adaptive"],
            index=["None", "Simple", "Adaptive"].index(st.session_state.thresh_mode),
            key="thresh_mode_widget"
        )
        if threshold_mode != st.session_state.thresh_mode:
            st.session_state.thresh_mode = threshold_mode
            if threshold_mode == "None":
                st.session_state.threshold_enabled = False
            else:
                st.session_state.threshold_enabled = True
                if threshold_mode == "Simple":
                    st.session_state.threshold_type = "simple"
                elif threshold_mode == "Adaptive":
                    st.session_state.threshold_type = "adaptive"
            st.rerun()
        
        if threshold_mode == "Simple":
            val = st.slider("Value", 0, 255, value=st.session_state.binary_threshold_value, key="th_val_widget")
            if val != st.session_state.binary_threshold_value:
                st.session_state.binary_threshold_value = val
                st.rerun()
            
            method = st.selectbox("Method", THRESHOLD_METHODS, index=THRESHOLD_METHODS.index(st.session_state.binary_threshold_method), key="th_method_widget")
            if method != st.session_state.binary_threshold_method:
                st.session_state.binary_threshold_method = method
                st.rerun()
        
        elif threshold_mode == "Adaptive":
            method = st.selectbox("Method", ADAPTIVE_METHODS, index=ADAPTIVE_METHODS.index(st.session_state.binary_adaptive_method), key="ad_method_widget")
            if method != st.session_state.binary_adaptive_method:
                st.session_state.binary_adaptive_method = method
                st.rerun()
            
            block = st.slider("Block", 3, 31, step=2, value=st.session_state.binary_adaptive_block, key="ad_block_widget")
            if block != st.session_state.binary_adaptive_block:
                st.session_state.binary_adaptive_block = block
                st.rerun()
            
            c = st.slider("C", 0, 20, value=st.session_state.binary_adaptive_c, key="ad_c_widget")
            if c != st.session_state.binary_adaptive_c:
                st.session_state.binary_adaptive_c = c
                st.rerun()

    # ========== TAB 2: EDGE ==========
    with tab2:
        edge_methods_with_none = ["None"] + EDGE_METHODS
        current_method = st.session_state.edge_method
        if current_method not in edge_methods_with_none:
            current_method = "Canny"
        idx = edge_methods_with_none.index(current_method) if current_method in edge_methods_with_none else 1
        
        method = st.selectbox(
            "Method", edge_methods_with_none,
            index=idx,
            key="edge_method_widget"
        )
        if method != st.session_state.edge_method:
            st.session_state.edge_method = method
            if method == "None":
                st.session_state.edge_enabled = False
            else:
                st.session_state.edge_enabled = True
            st.rerun()
        
        if method != "None":
            if method == "Canny":
                low = st.slider("Low", 0, 255, value=st.session_state.edge_low, key="edge_low_widget")
                if low != st.session_state.edge_low:
                    st.session_state.edge_low = low
                    st.rerun()
                high = st.slider("High", 0, 255, value=st.session_state.edge_high, key="edge_high_widget")
                if high != st.session_state.edge_high:
                    st.session_state.edge_high = high
                    st.rerun()
            elif method == "Sobel":
                dir_val = st.radio("Dir", SOBEL_DIRECTIONS, index=SOBEL_DIRECTIONS.index(st.session_state.edge_sobel_direction), key="sobel_dir_widget", horizontal=True)
                if dir_val != st.session_state.edge_sobel_direction:
                    st.session_state.edge_sobel_direction = dir_val
                    st.rerun()
                kernel = st.slider("Kernel", 1, 7, step=2, value=st.session_state.edge_kernel, key="edge_kernel_widget")
                if kernel != st.session_state.edge_kernel:
                    st.session_state.edge_kernel = kernel
                    st.rerun()
            elif method in ["Laplacian", "LoG"]:
                kernel = st.slider("Kernel", 1, 7, step=2, value=st.session_state.edge_kernel, key="edge_kernel_widget")
                if kernel != st.session_state.edge_kernel:
                    st.session_state.edge_kernel = kernel
                    st.rerun()
            else:  # Prewitt, Roberts
                st.info("Kernel size not used for Prewitt/Roberts (fixed 3x3).")
        else:
            st.info("Edge detection disabled.")

    # ========== TAB 3: MORPHOLOGY ==========
    with tab3:
        morph_ops_with_none = ["None"] + MORPH_OPERATIONS
        current_op = st.session_state.morph_operation
        if current_op not in morph_ops_with_none:
            current_op = "Erosion"
        idx = morph_ops_with_none.index(current_op) if current_op in morph_ops_with_none else 1
        
        op = st.selectbox(
            "Operation", morph_ops_with_none,
            index=idx,
            key="morph_op_widget"
        )
        if op != st.session_state.morph_operation:
            st.session_state.morph_operation = op
            if op == "None":
                st.session_state.morph_enabled = False
            else:
                st.session_state.morph_enabled = True
            st.rerun()
        
        if op != "None":
            kernel = st.slider("Kernel", 3, 15, step=2, value=st.session_state.morph_kernel, key="morph_kernel_widget")
            if kernel != st.session_state.morph_kernel:
                st.session_state.morph_kernel = kernel
                st.rerun()
            iters = st.slider("Iter", 1, 5, value=st.session_state.morph_iterations, key="morph_iter_widget")
            if iters != st.session_state.morph_iterations:
                st.session_state.morph_iterations = iters
                st.rerun()
        else:
            st.info("Morphology disabled.")

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("Reset Binary & Edge", use_container_width=True):
        reset_binary_edge_state()
        st.session_state.thresh_mode = "None"
        st.rerun()