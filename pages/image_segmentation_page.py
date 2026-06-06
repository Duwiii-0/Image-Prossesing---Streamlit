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
    tab1, tab2, tab3 = st.tabs([
        "Threshold", 
        "Edge", 
        "Region"
    ])

    # ==================== TAB 1: THRESHOLD-BASED ====================
    with tab1:
        sub_tab1, sub_tab2, sub_tab3 = st.tabs(["Global", "Adaptive", "Otsu"])
        
        # SUB-TAB 1: Global Threshold
        with sub_tab1:
            threshold_val = st.slider(
                "Value", 0, 255,
                value=st.session_state.seg_threshold_value,
                key="seg_threshold_val_temp"
            )
            if threshold_val != st.session_state.seg_threshold_value:
                st.session_state.seg_threshold_value = threshold_val
                st.rerun()
            
            if st.button("Apply Global", type="primary", use_container_width=True):
                st.session_state.segmentation_mode = "threshold_global"
                st.rerun()
        
        # SUB-TAB 2: Adaptive Threshold
        with sub_tab2:
            adaptive_method = st.selectbox(
                "Method",
                SEG_ADAPTIVE_METHODS,
                index=0 if st.session_state.seg_adaptive_method == "mean" else 1,
                key="seg_adaptive_method_temp"
            )
            if adaptive_method != st.session_state.seg_adaptive_method:
                st.session_state.seg_adaptive_method = adaptive_method
                st.rerun()
            
            block_size = st.slider(
                "Block", 3, 31, step=2,
                value=st.session_state.seg_adaptive_block,
                key="seg_adaptive_block_temp"
            )
            if block_size != st.session_state.seg_adaptive_block:
                st.session_state.seg_adaptive_block = block_size
                st.rerun()
            
            c_val = st.slider(
                "C", 0, 20,
                value=st.session_state.seg_adaptive_c,
                key="seg_adaptive_c_temp"
            )
            if c_val != st.session_state.seg_adaptive_c:
                st.session_state.seg_adaptive_c = c_val
                st.rerun()
            
            if st.button("Apply Adaptive", type="primary", use_container_width=True):
                st.session_state.segmentation_mode = "threshold_adaptive"
                st.rerun()
        
        # SUB-TAB 3: Otsu Threshold
        with sub_tab3:
            if st.button("Apply Otsu", type="primary", use_container_width=True):
                st.session_state.segmentation_mode = "threshold_otsu"
                st.rerun()

    # ==================== TAB 2: EDGE-BASED ====================
    with tab2:
        edge_method = st.selectbox(
            "Method",
            SEG_EDGE_METHODS,
            index=SEG_EDGE_METHODS.index(st.session_state.seg_edge_method),
            key="seg_edge_method_temp"
        )
        if edge_method != st.session_state.seg_edge_method:
            st.session_state.seg_edge_method = edge_method
            st.rerun()
        
        # Canny parameters
        if st.session_state.seg_edge_method == "Canny":
            low_val = st.slider("Low", 0, 255, value=st.session_state.edge_low, key="seg_edge_low_temp")
            if low_val != st.session_state.edge_low:
                st.session_state.edge_low = low_val
                st.rerun()
            high_val = st.slider("High", 0, 255, value=st.session_state.edge_high, key="seg_edge_high_temp")
            if high_val != st.session_state.edge_high:
                st.session_state.edge_high = high_val
                st.rerun()
        
        # Sobel parameters
        elif st.session_state.seg_edge_method == "Sobel":
            kernel_val = st.slider("Kernel", 1, 7, step=2, value=st.session_state.seg_edge_kernel, key="seg_edge_kernel_temp")
            if kernel_val != st.session_state.seg_edge_kernel:
                st.session_state.seg_edge_kernel = kernel_val
                st.rerun()
            sobel_dir = st.selectbox(
                "Dir",
                ["both", "x", "y"],
                index=["both", "x", "y"].index(st.session_state.seg_sobel_direction),
                key="seg_sobel_dir_temp"
            )
            if sobel_dir != st.session_state.seg_sobel_direction:
                st.session_state.seg_sobel_direction = sobel_dir
                st.rerun()
        
        # Laplacian parameters
        else:
            kernel_val = st.slider("Kernel", 1, 7, step=2, value=st.session_state.seg_edge_kernel, key="seg_edge_kernel_lap_temp")
            if kernel_val != st.session_state.seg_edge_kernel:
                st.session_state.seg_edge_kernel = kernel_val
                st.rerun()
        
        edge_mode_map = {
            "Canny": "edge_canny",
            "Sobel": "edge_sobel",
            "Laplacian": "edge_laplacian"
        }
        
        if st.button("Apply Edge", type="primary", use_container_width=True):
            st.session_state.segmentation_mode = edge_mode_map[st.session_state.seg_edge_method]
            st.rerun()

    # ==================== TAB 3: REGION-BASED ====================
    with tab3:
        region_method = st.selectbox(
            "Method",
            SEG_REGION_METHODS,
            index=SEG_REGION_METHODS.index(st.session_state.seg_region_method),
            key="seg_region_method_temp"
        )
        if region_method != st.session_state.seg_region_method:
            st.session_state.seg_region_method = region_method
            st.rerun()
        
        if st.session_state.seg_region_method == "Region Growing":
            threshold_val = st.slider(
                "Threshold", 0, 50,
                value=st.session_state.seg_region_threshold,
                key="seg_region_threshold_temp"
            )
            if threshold_val != st.session_state.seg_region_threshold:
                st.session_state.seg_region_threshold = threshold_val
                st.rerun()
        
        elif st.session_state.seg_region_method == "K-Means":
            k_val = st.slider(
                "K", 2, 8,
                value=st.session_state.seg_kmeans_k,
                key="seg_kmeans_k_temp"
            )
            if k_val != st.session_state.seg_kmeans_k:
                st.session_state.seg_kmeans_k = k_val
                st.rerun()
        
        elif st.session_state.seg_region_method == "Contour":
            contour_mode = st.selectbox(
                "Mode",
                ["external", "all"],
                index=0 if st.session_state.seg_contour_mode == "external" else 1,
                key="seg_contour_mode_temp"
            )
            if contour_mode != st.session_state.seg_contour_mode:
                st.session_state.seg_contour_mode = contour_mode
                st.rerun()
        
        region_mode_map = {
            "Region Growing": "region_growing",
            "K-Means": "kmeans",
            "Contour": "contour",
            "Watershed": "watershed"
        }
        
        if st.button("Apply Region", type="primary", use_container_width=True):
            st.session_state.segmentation_mode = region_mode_map[st.session_state.seg_region_method]
            st.rerun()

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("Reset Segmentation", use_container_width=True):
        reset_segmentation_state()
        st.rerun()
