import streamlit as st
from utils.state_manager import reset_segmentation_state
from utils.constants import (
    SEG_THRESHOLD_METHODS, SEG_EDGE_METHODS, SEG_REGION_METHODS, SEG_ADAPTIVE_METHODS
)

def render_image_segmentation_page():
    tab1, tab2, tab3 = st.tabs(["Threshold", "Edge", "Region"])

    # ==================== TAB 1: THRESHOLD ====================
    with tab1:
        # Gunakan seg_threshold_mode, dengan opsi None
        thresh_options = SEG_THRESHOLD_METHODS  # ["None","Global","Adaptive","Otsu"]
        current_thresh = st.session_state.seg_threshold_mode
        idx_thresh = thresh_options.index(current_thresh) if current_thresh in thresh_options else 0

        threshold_method = st.selectbox("Method", thresh_options, index=idx_thresh, key="seg_threshold_select")
        if threshold_method != st.session_state.seg_threshold_mode:
            st.session_state.seg_threshold_mode = threshold_method
            # Aktifkan/nonaktifkan threshold segmentation
            st.session_state.seg_threshold_enabled = (threshold_method != "None")
            st.rerun()

        if threshold_method == "Global":
            threshold_val = st.slider("Threshold Value", 0, 255,
                                      value=st.session_state.seg_threshold_value,
                                      key="seg_threshold_val_slider")
            if threshold_val != st.session_state.seg_threshold_value:
                st.session_state.seg_threshold_value = threshold_val
                st.rerun()
        elif threshold_method == "Adaptive":
            adaptive_method = st.selectbox("Adaptive Method", SEG_ADAPTIVE_METHODS,
                                           index=0 if st.session_state.seg_adaptive_method == "mean" else 1,
                                           key="seg_adaptive_method_select")
            if adaptive_method != st.session_state.seg_adaptive_method:
                st.session_state.seg_adaptive_method = adaptive_method
                st.rerun()
            block_size = st.slider("Block Size", 3, 31, step=2,
                                   value=st.session_state.seg_adaptive_block,
                                   key="seg_adaptive_block_slider")
            if block_size != st.session_state.seg_adaptive_block:
                st.session_state.seg_adaptive_block = block_size
                st.rerun()
            c_val = st.slider("C", 0, 20, value=st.session_state.seg_adaptive_c,
                              key="seg_adaptive_c_slider")
            if c_val != st.session_state.seg_adaptive_c:
                st.session_state.seg_adaptive_c = c_val
                st.rerun()
        elif threshold_method == "Otsu":
            st.info("Otsu's method determines threshold automatically.")

    # ==================== TAB 2: EDGE ====================
    with tab2:
        edge_options = ["None"] + SEG_EDGE_METHODS
        current_edge = st.session_state.seg_edge_method
        if current_edge not in edge_options:
            current_edge = "None"
        idx_edge = edge_options.index(current_edge)

        edge_method = st.selectbox("Method", edge_options, index=idx_edge, key="seg_edge_method_select")
        if edge_method != st.session_state.seg_edge_method:
            st.session_state.seg_edge_method = edge_method
            st.session_state.seg_edge_enabled = (edge_method != "None")
            st.rerun()

        if edge_method != "None":
            if edge_method == "Canny":
                low_val = st.slider("Low", 0, 255, value=st.session_state.seg_edge_low, key="seg_edge_low_slider")
                if low_val != st.session_state.seg_edge_low:
                    st.session_state.seg_edge_low = low_val
                    st.rerun()
                high_val = st.slider("High", 0, 255, value=st.session_state.seg_edge_high, key="seg_edge_high_slider")
                if high_val != st.session_state.seg_edge_high:
                    st.session_state.seg_edge_high = high_val
                    st.rerun()
            elif edge_method == "Sobel":
                kernel_val = st.slider("Kernel", 1, 7, step=2, value=st.session_state.seg_edge_kernel, key="seg_edge_kernel_slider")
                if kernel_val != st.session_state.seg_edge_kernel:
                    st.session_state.seg_edge_kernel = kernel_val
                    st.rerun()
                sobel_dir = st.selectbox("Direction", ["both", "x", "y"],
                                         index=["both","x","y"].index(st.session_state.seg_sobel_direction),
                                         key="seg_sobel_dir_select")
                if sobel_dir != st.session_state.seg_sobel_direction:
                    st.session_state.seg_sobel_direction = sobel_dir
                    st.rerun()
            elif edge_method == "Laplacian":
                kernel_val = st.slider("Kernel", 1, 7, step=2, value=st.session_state.seg_edge_kernel, key="seg_edge_kernel_slider")
                if kernel_val != st.session_state.seg_edge_kernel:
                    st.session_state.seg_edge_kernel = kernel_val
                    st.rerun()

    # ==================== TAB 3: REGION ====================
    with tab3:
        region_options = ["None"] + SEG_REGION_METHODS
        current_region = st.session_state.seg_region_method
        if current_region not in region_options:
            current_region = "None"
        idx_region = region_options.index(current_region)

        region_method = st.selectbox("Method", region_options, index=idx_region, key="seg_region_method_select")
        if region_method != st.session_state.seg_region_method:
            st.session_state.seg_region_method = region_method
            st.session_state.seg_region_enabled = (region_method != "None")
            st.rerun()

        if region_method != "None":
            if region_method == "Region Growing":
                threshold_val = st.slider("Threshold", 0, 50, value=st.session_state.seg_region_threshold, key="seg_region_threshold_slider")
                if threshold_val != st.session_state.seg_region_threshold:
                    st.session_state.seg_region_threshold = threshold_val
                    st.rerun()
            elif region_method == "K-Means":
                k_val = st.slider("K", 2, 8, value=st.session_state.seg_kmeans_k, key="seg_kmeans_k_slider")
                if k_val != st.session_state.seg_kmeans_k:
                    st.session_state.seg_kmeans_k = k_val
                    st.rerun()
            elif region_method == "Contour":
                contour_mode = st.selectbox("Mode", ["external", "all"],
                                            index=0 if st.session_state.seg_contour_mode == "external" else 1,
                                            key="seg_contour_mode_select")
                if contour_mode != st.session_state.seg_contour_mode:
                    st.session_state.seg_contour_mode = contour_mode
                    st.rerun()
            # Watershed tidak punya parameter

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("Reset Segmentation", use_container_width=True):
        reset_segmentation_state()
        st.rerun()