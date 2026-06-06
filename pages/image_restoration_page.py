import streamlit as st
import numpy as np
from PIL import Image
from utils.preview_helper import get_preview_image
from utils.state_manager import reset_restoration_state
from utils.ui_helpers import render_image_preview, render_reset_and_save_buttons, render_section_header


def render_image_restoration_page():
    tab1, tab2, tab3 = st.tabs([
        "Gaussian", 
        "Median", 
        "Noise"
    ])

    with tab1:
        kernel_size = st.slider(
            "Kernel Size", 
            1, 15, step=2,
            value=st.session_state.restoration_gaussian_kernel,
            key="gaussian_kernel_temp"
        )
        if kernel_size != st.session_state.restoration_gaussian_kernel:
            st.session_state.restoration_gaussian_kernel = kernel_size
            st.rerun()

    with tab2:
        kernel_size = st.slider(
            "Kernel Size", 
            1, 15, step=2,
            value=st.session_state.restoration_median_kernel,
            key="median_kernel_temp"
        )
        if kernel_size != st.session_state.restoration_median_kernel:
            st.session_state.restoration_median_kernel = kernel_size
            st.rerun()

    with tab3:
        kernel_size = st.slider(
            "Kernel Size", 
            1, 15, step=2,
            value=st.session_state.restoration_sp_kernel,
            key="sp_kernel_temp"
        )
        if kernel_size != st.session_state.restoration_sp_kernel:
            st.session_state.restoration_sp_kernel = kernel_size
            st.rerun()

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("Reset Restoration", use_container_width=True):
        reset_restoration_state()
        st.rerun()
