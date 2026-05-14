import streamlit as st
from utils.preview_helper import get_preview_image
from utils.ui_helpers import render_image_preview


def render_image_restoration_page():
    if st.session_state.original_image is None:
        st.markdown("""
        <div class="custom-info-box">
            <strong>Notice:</strong> Please upload an image via the Image Management menu before applying any enhancements.
        </div>
        """, unsafe_allow_html=True)
        return
    
    if st.session_state.processed_image is None:
        st.session_state.processed_image = st.session_state.original_image.copy()

    st.markdown("Restore and reduce noise in your image using spatial filtering techniques.")
    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "Gaussian Blur", 
        "Median Filter", 
        "Noise Removal (Salt & Pepper)"
    ])

    with tab1:
        st.markdown("""
        **Gaussian Blur** - Smooths image using weighted average of neighboring pixels.
        
        *Best for reducing Gaussian noise. Blurs edges but creates smooth results.*
        """)
        
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
        st.markdown("""
        **Median Filter** - Replaces each pixel with the median value of its neighbors.
        
        *Excellent for salt & pepper noise. Preserves edges better than Gaussian blur.*
        """)
        
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
        st.markdown("""
        **Salt & Pepper Noise Removal** - Specialized median filter for random white/black dots.
        
        *Specifically targets impulse noise. Most effective method for this noise type.*
        """)
        
        kernel_size = st.slider(
            "Kernel Size", 
            1, 15, step=2,
            value=st.session_state.restoration_sp_kernel,
            key="sp_kernel_temp"
        )
        if kernel_size != st.session_state.restoration_sp_kernel:
            st.session_state.restoration_sp_kernel = kernel_size
            st.rerun()
    
    st.markdown("<hr style='margin: 2rem 0;' />", unsafe_allow_html=True)
    st.markdown("### Image Preview")

    # Preview image using helper
    preview_image = get_preview_image()

    render_image_preview(st.session_state.original_image, preview_image)