import streamlit as st
from utils.state_manager import reset_segmentation_state
from utils.constants import (
    SEG_THRESHOLD_METHODS, SEG_EDGE_METHODS, SEG_REGION_METHODS, SEG_ADAPTIVE_METHODS
)

def reset_segmentation():
    reset_segmentation_state()
    if 'reset_counter' not in st.session_state:
        st.session_state.reset_counter = 0
    st.session_state.reset_counter += 1
    st.rerun()

def render_image_segmentation_page():
    if 'reset_counter' not in st.session_state:
        st.session_state.reset_counter = 0
    
    tab1, tab2, tab3 = st.tabs(["Threshold", "Edge", "Region"])

    # ==================== TAB 1: THRESHOLD ====================
    with tab1:
        thresh_options = SEG_THRESHOLD_METHODS
        current_thresh = st.session_state.seg_threshold_mode
        idx_thresh = thresh_options.index(current_thresh) if current_thresh in thresh_options else 0

        def on_thresh_method_change():
            selected = st.session_state[f"seg_threshold_select_{st.session_state.reset_counter}"]
            st.session_state.seg_threshold_mode = selected
            st.session_state.seg_threshold_enabled = (selected != "None")

        threshold_method = st.selectbox(
            "Method", thresh_options, index=idx_thresh,
            key=f"seg_threshold_select_{st.session_state.reset_counter}",
            on_change=on_thresh_method_change
        )

        if threshold_method == "Global":
            def on_thresh_val_change():
                st.session_state.seg_threshold_value = st.session_state[f"seg_threshold_val_slider_{st.session_state.reset_counter}"]
            
            st.slider(
                "Threshold Value", 0, 255,
                value=st.session_state.seg_threshold_value,
                key=f"seg_threshold_val_slider_{st.session_state.reset_counter}",
                on_change=on_thresh_val_change
            )
        
        elif threshold_method == "Adaptive":
            def on_adaptive_method_change():
                st.session_state.seg_adaptive_method = st.session_state[f"seg_adaptive_method_select_{st.session_state.reset_counter}"]
            
            st.selectbox(
                "Adaptive Method", SEG_ADAPTIVE_METHODS,
                index=0 if st.session_state.seg_adaptive_method == "mean" else 1,
                key=f"seg_adaptive_method_select_{st.session_state.reset_counter}",
                on_change=on_adaptive_method_change
            )
            
            def on_adaptive_block_change():
                st.session_state.seg_adaptive_block = st.session_state[f"seg_adaptive_block_slider_{st.session_state.reset_counter}"]
            
            st.slider(
                "Block Size", 3, 31, step=2,
                value=st.session_state.seg_adaptive_block,
                key=f"seg_adaptive_block_slider_{st.session_state.reset_counter}",
                on_change=on_adaptive_block_change
            )
            
            def on_adaptive_c_change():
                st.session_state.seg_adaptive_c = st.session_state[f"seg_adaptive_c_slider_{st.session_state.reset_counter}"]
            
            st.slider(
                "C", 0, 20,
                value=st.session_state.seg_adaptive_c,
                key=f"seg_adaptive_c_slider_{st.session_state.reset_counter}",
                on_change=on_adaptive_c_change
            )
        
        elif threshold_method == "Otsu":
            st.info("Otsu's method determines threshold automatically.")

    # ==================== TAB 2: EDGE ====================
    with tab2:
        edge_options = ["None"] + SEG_EDGE_METHODS
        current_edge = st.session_state.seg_edge_method
        if current_edge not in edge_options:
            current_edge = "None"
        idx_edge = edge_options.index(current_edge)

        def on_edge_method_change():
            selected = st.session_state[f"seg_edge_method_select_{st.session_state.reset_counter}"]
            st.session_state.seg_edge_method = selected
            st.session_state.seg_edge_enabled = (selected != "None")

        edge_method = st.selectbox(
            "Method", edge_options, index=idx_edge,
            key=f"seg_edge_method_select_{st.session_state.reset_counter}",
            on_change=on_edge_method_change
        )

        if edge_method != "None":
            if edge_method == "Canny":
                def on_edge_low_change():
                    st.session_state.seg_edge_low = st.session_state[f"seg_edge_low_slider_{st.session_state.reset_counter}"]
                
                st.slider(
                    "Low", 0, 255,
                    value=st.session_state.seg_edge_low,
                    key=f"seg_edge_low_slider_{st.session_state.reset_counter}",
                    on_change=on_edge_low_change
                )
                
                def on_edge_high_change():
                    st.session_state.seg_edge_high = st.session_state[f"seg_edge_high_slider_{st.session_state.reset_counter}"]
                
                st.slider(
                    "High", 0, 255,
                    value=st.session_state.seg_edge_high,
                    key=f"seg_edge_high_slider_{st.session_state.reset_counter}",
                    on_change=on_edge_high_change
                )
            
            elif edge_method == "Sobel":
                def on_edge_kernel_change():
                    st.session_state.seg_edge_kernel = st.session_state[f"seg_edge_kernel_slider_{st.session_state.reset_counter}"]
                
                st.slider(
                    "Kernel", 1, 7, step=2,
                    value=st.session_state.seg_edge_kernel,
                    key=f"seg_edge_kernel_slider_{st.session_state.reset_counter}",
                    on_change=on_edge_kernel_change
                )
                
                def on_sobel_dir_change():
                    st.session_state.seg_sobel_direction = st.session_state[f"seg_sobel_dir_select_{st.session_state.reset_counter}"]
                
                st.selectbox(
                    "Direction", ["both", "x", "y"],
                    index=["both","x","y"].index(st.session_state.seg_sobel_direction),
                    key=f"seg_sobel_dir_select_{st.session_state.reset_counter}",
                    on_change=on_sobel_dir_change
                )
            
            elif edge_method == "Laplacian":
                def on_edge_kernel_change():
                    st.session_state.seg_edge_kernel = st.session_state[f"seg_edge_kernel_slider_{st.session_state.reset_counter}"]
                
                st.slider(
                    "Kernel", 1, 7, step=2,
                    value=st.session_state.seg_edge_kernel,
                    key=f"seg_edge_kernel_slider_{st.session_state.reset_counter}",
                    on_change=on_edge_kernel_change
                )

    # ==================== TAB 3: REGION ====================
    with tab3:
        region_options = ["None"] + SEG_REGION_METHODS
        current_region = st.session_state.seg_region_method
        if current_region not in region_options:
            current_region = "None"
        idx_region = region_options.index(current_region)

        def on_region_method_change():
            selected = st.session_state[f"seg_region_method_select_{st.session_state.reset_counter}"]
            st.session_state.seg_region_method = selected
            st.session_state.seg_region_enabled = (selected != "None")

        region_method = st.selectbox(
            "Method", region_options, index=idx_region,
            key=f"seg_region_method_select_{st.session_state.reset_counter}",
            on_change=on_region_method_change
        )

        if region_method != "None":
            if region_method == "Region Growing":
                def on_region_threshold_change():
                    st.session_state.seg_region_threshold = st.session_state[f"seg_region_threshold_slider_{st.session_state.reset_counter}"]
                
                st.slider(
                    "Threshold", 0, 50,
                    value=st.session_state.seg_region_threshold,
                    key=f"seg_region_threshold_slider_{st.session_state.reset_counter}",
                    on_change=on_region_threshold_change
                )
            
            elif region_method == "K-Means":
                def on_kmeans_k_change():
                    st.session_state.seg_kmeans_k = st.session_state[f"seg_kmeans_k_slider_{st.session_state.reset_counter}"]
                
                st.slider(
                    "K", 2, 8,
                    value=st.session_state.seg_kmeans_k,
                    key=f"seg_kmeans_k_slider_{st.session_state.reset_counter}",
                    on_change=on_kmeans_k_change
                )
            
            elif region_method == "Contour":
                def on_contour_mode_change():
                    st.session_state.seg_contour_mode = st.session_state[f"seg_contour_mode_select_{st.session_state.reset_counter}"]
                
                st.selectbox(
                    "Mode", ["external", "all"],
                    index=0 if st.session_state.seg_contour_mode == "external" else 1,
                    key=f"seg_contour_mode_select_{st.session_state.reset_counter}",
                    on_change=on_contour_mode_change
                )
            # Watershed tidak punya parameter

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("Reset Segmentation", use_container_width=True):
        reset_segmentation()