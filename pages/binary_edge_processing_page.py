import streamlit as st
from utils.state_manager import reset_binary_edge_state
from utils.constants import (
    THRESHOLD_METHODS, ADAPTIVE_METHODS, EDGE_METHODS, 
    SOBEL_DIRECTIONS, MORPH_OPERATIONS
)

def reset_binary_edge():
    reset_binary_edge_state()
    st.session_state.thresh_mode = "None"
    if 'reset_counter' not in st.session_state:
        st.session_state.reset_counter = 0
    st.session_state.reset_counter += 1
    st.rerun()

def render_binary_edge_processing_page():
    if 'reset_counter' not in st.session_state:
        st.session_state.reset_counter = 0
    
    tab1, tab2, tab3 = st.tabs(["Threshold", "Edge", "Morph"])

    # ========== TAB 1: THRESHOLD ==========
    with tab1:
        if 'thresh_mode' not in st.session_state:
            st.session_state.thresh_mode = "None"
        
        def on_thresh_mode_change():
            selected = st.session_state[f"thresh_mode_widget_{st.session_state.reset_counter}"]
            st.session_state.thresh_mode = selected
            if selected == "None":
                st.session_state.threshold_enabled = False
            else:
                st.session_state.threshold_enabled = True
                if selected == "Simple":
                    st.session_state.threshold_type = "simple"
                elif selected == "Adaptive":
                    st.session_state.threshold_type = "adaptive"
        
        threshold_mode = st.selectbox(
            "Mode", ["None", "Simple", "Adaptive"],
            index=["None", "Simple", "Adaptive"].index(st.session_state.thresh_mode),
            key=f"thresh_mode_widget_{st.session_state.reset_counter}",
            on_change=on_thresh_mode_change
        )
        
        if st.session_state.thresh_mode == "Simple":
            def on_thresh_val_change():
                st.session_state.binary_threshold_value = st.session_state[f"th_val_widget_{st.session_state.reset_counter}"]
            
            st.slider(
                "Value", 0, 255,
                value=st.session_state.binary_threshold_value,
                key=f"th_val_widget_{st.session_state.reset_counter}",
                on_change=on_thresh_val_change
            )
            
            def on_thresh_method_change():
                st.session_state.binary_threshold_method = st.session_state[f"th_method_widget_{st.session_state.reset_counter}"]
            
            st.selectbox(
                "Method", THRESHOLD_METHODS,
                index=THRESHOLD_METHODS.index(st.session_state.binary_threshold_method),
                key=f"th_method_widget_{st.session_state.reset_counter}",
                on_change=on_thresh_method_change
            )
        
        elif st.session_state.thresh_mode == "Adaptive":
            def on_adaptive_method_change():
                st.session_state.binary_adaptive_method = st.session_state[f"ad_method_widget_{st.session_state.reset_counter}"]
            
            st.selectbox(
                "Method", ADAPTIVE_METHODS,
                index=ADAPTIVE_METHODS.index(st.session_state.binary_adaptive_method),
                key=f"ad_method_widget_{st.session_state.reset_counter}",
                on_change=on_adaptive_method_change
            )
            
            def on_adaptive_block_change():
                st.session_state.binary_adaptive_block = st.session_state[f"ad_block_widget_{st.session_state.reset_counter}"]
            
            st.slider(
                "Block", 3, 31, step=2,
                value=st.session_state.binary_adaptive_block,
                key=f"ad_block_widget_{st.session_state.reset_counter}",
                on_change=on_adaptive_block_change
            )
            
            def on_adaptive_c_change():
                st.session_state.binary_adaptive_c = st.session_state[f"ad_c_widget_{st.session_state.reset_counter}"]
            
            st.slider(
                "C", 0, 20,
                value=st.session_state.binary_adaptive_c,
                key=f"ad_c_widget_{st.session_state.reset_counter}",
                on_change=on_adaptive_c_change
            )

    # ========== TAB 2: EDGE ==========
    with tab2:
        edge_methods_with_none = ["None"] + EDGE_METHODS
        current_method = st.session_state.edge_method
        if current_method not in edge_methods_with_none:
            current_method = "Canny"
        idx = edge_methods_with_none.index(current_method) if current_method in edge_methods_with_none else 1
        
        def on_edge_method_change():
            selected = st.session_state[f"edge_method_widget_{st.session_state.reset_counter}"]
            st.session_state.edge_method = selected
            if selected == "None":
                st.session_state.edge_enabled = False
            else:
                st.session_state.edge_enabled = True
        
        method = st.selectbox(
            "Method", edge_methods_with_none,
            index=idx,
            key=f"edge_method_widget_{st.session_state.reset_counter}",
            on_change=on_edge_method_change
        )
        
        if method != "None":
            if method == "Canny":
                def on_edge_low_change():
                    st.session_state.edge_low = st.session_state[f"edge_low_widget_{st.session_state.reset_counter}"]
                
                st.slider(
                    "Low", 0, 255,
                    value=st.session_state.edge_low,
                    key=f"edge_low_widget_{st.session_state.reset_counter}",
                    on_change=on_edge_low_change
                )
                
                def on_edge_high_change():
                    st.session_state.edge_high = st.session_state[f"edge_high_widget_{st.session_state.reset_counter}"]
                
                st.slider(
                    "High", 0, 255,
                    value=st.session_state.edge_high,
                    key=f"edge_high_widget_{st.session_state.reset_counter}",
                    on_change=on_edge_high_change
                )
            
            elif method == "Sobel":
                def on_sobel_dir_change():
                    st.session_state.edge_sobel_direction = st.session_state[f"sobel_dir_widget_{st.session_state.reset_counter}"]
                
                st.radio(
                    "Dir", SOBEL_DIRECTIONS,
                    index=SOBEL_DIRECTIONS.index(st.session_state.edge_sobel_direction),
                    key=f"sobel_dir_widget_{st.session_state.reset_counter}",
                    on_change=on_sobel_dir_change,
                    horizontal=True
                )
                
                def on_edge_kernel_change():
                    st.session_state.edge_kernel = st.session_state[f"edge_kernel_widget_{st.session_state.reset_counter}"]
                
                st.slider(
                    "Kernel", 1, 7, step=2,
                    value=st.session_state.edge_kernel,
                    key=f"edge_kernel_widget_{st.session_state.reset_counter}",
                    on_change=on_edge_kernel_change
                )
            
            elif method in ["Laplacian", "LoG"]:
                def on_edge_kernel_change():
                    st.session_state.edge_kernel = st.session_state[f"edge_kernel_widget_{st.session_state.reset_counter}"]
                
                st.slider(
                    "Kernel", 1, 7, step=2,
                    value=st.session_state.edge_kernel,
                    key=f"edge_kernel_widget_{st.session_state.reset_counter}",
                    on_change=on_edge_kernel_change
                )
            
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
        
        def on_morph_op_change():
            selected = st.session_state[f"morph_op_widget_{st.session_state.reset_counter}"]
            st.session_state.morph_operation = selected
            if selected == "None":
                st.session_state.morph_enabled = False
            else:
                st.session_state.morph_enabled = True
        
        op = st.selectbox(
            "Operation", morph_ops_with_none,
            index=idx,
            key=f"morph_op_widget_{st.session_state.reset_counter}",
            on_change=on_morph_op_change
        )
        
        if op != "None":
            def on_morph_kernel_change():
                st.session_state.morph_kernel = st.session_state[f"morph_kernel_widget_{st.session_state.reset_counter}"]
            
            st.slider(
                "Kernel", 3, 15, step=2,
                value=st.session_state.morph_kernel,
                key=f"morph_kernel_widget_{st.session_state.reset_counter}",
                on_change=on_morph_kernel_change
            )
            
            def on_morph_iter_change():
                st.session_state.morph_iterations = st.session_state[f"morph_iter_widget_{st.session_state.reset_counter}"]
            
            st.slider(
                "Iter", 1, 5,
                value=st.session_state.morph_iterations,
                key=f"morph_iter_widget_{st.session_state.reset_counter}",
                on_change=on_morph_iter_change
            )
        else:
            st.info("Morphology disabled.")

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("Reset Binary & Edge", use_container_width=True):
        reset_binary_edge()