import streamlit as st
import numpy as np
from PIL import Image
from utils.state_manager import reset_restoration_state

def reset_restoration():
    reset_restoration_state()
    if 'reset_counter' not in st.session_state:
        st.session_state.reset_counter = 0
    st.session_state.reset_counter += 1
    st.rerun()

def render_image_restoration_page():
    if 'reset_counter' not in st.session_state:
        st.session_state.reset_counter = 0
    
    tab1, tab2, tab3 = st.tabs([
        "Gaussian", 
        "Median", 
        "Noise"
    ])

    with tab1:
        def on_gaussian_change():
            st.session_state.restoration_gaussian_kernel = st.session_state[f"_gaussian_{st.session_state.reset_counter}"]
        
        st.slider(
            "Kernel Size", 1, 15, step=2,
            value=st.session_state.restoration_gaussian_kernel,
            key=f"_gaussian_{st.session_state.reset_counter}",
            on_change=on_gaussian_change
        )

    with tab2:
        def on_median_change():
            st.session_state.restoration_median_kernel = st.session_state[f"_median_{st.session_state.reset_counter}"]
        
        st.slider(
            "Kernel Size", 1, 15, step=2,
            value=st.session_state.restoration_median_kernel,
            key=f"_median_{st.session_state.reset_counter}",
            on_change=on_median_change
        )

    with tab3:
        def on_sp_change():
            st.session_state.restoration_sp_kernel = st.session_state[f"_sp_{st.session_state.reset_counter}"]
        
        st.slider(
            "Kernel Size", 1, 15, step=2,
            value=st.session_state.restoration_sp_kernel,
            key=f"_sp_{st.session_state.reset_counter}",
            on_change=on_sp_change
        )

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("Reset Restoration", use_container_width=True):
        reset_restoration()