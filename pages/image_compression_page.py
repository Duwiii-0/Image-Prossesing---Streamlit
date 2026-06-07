import streamlit as st
import numpy as np
import time

from utils.ui_helpers import render_section_header, render_reset_and_save_buttons
from image_processing.compression import (
    simulate_jpeg_compression,
    uniform_quantization,
    kmeans_quantization,
    run_length_encoding_size,
    huffman_encoding_size,
    arithmetic_encoding_size,
    calculate_metrics
)

def render_image_compression_page():
    
    # Initialize compression state
    if "compression_mode" not in st.session_state:
        st.session_state.compression_mode = "Lossy (Visual)"
    
    mode = st.radio("Compression Type", ["Lossy (Visual)", "Lossless (Analytical)"], horizontal=True)
    st.session_state.compression_mode = mode

    original = st.session_state.original_image
    h, w, c = original.shape
    original_size_bytes = h * w * c
    
    if mode == "Lossy (Visual)":
        method = st.selectbox("Method", ["JPEG Simulation", "Uniform Quantization", "Color Quantization (K-Means)"])
        
        # Parameters
        if method == "JPEG Simulation":
            quality = st.slider("JPEG Quality", 1, 100, 50)
            
            if st.button("Apply Compression", use_container_width=True, type="primary"):
                start_time = time.time()
                compressed, comp_size = simulate_jpeg_compression(original, quality)
                process_time = time.time() - start_time
                
                st.session_state.processed_image = compressed
                
                # Metrics
                mse, psnr = calculate_metrics(original, compressed)
                ratio = (comp_size / original_size_bytes) * 100
                
                st.markdown(f"**Metrics:**")
                cols = st.columns(4)
                cols[0].metric("Orig. Size", f"{original_size_bytes / 1024:.1f} KB")
                cols[1].metric("Comp. Size", f"{comp_size / 1024:.1f} KB", f"-{100-ratio:.1f}%")
                cols[2].metric("PSNR", f"{psnr:.2f} dB")
                cols[3].metric("Time", f"{process_time:.3f} s")
                
        elif method == "Uniform Quantization":
            levels = st.select_slider("Color Levels per Channel", options=[2, 4, 8, 16, 32, 64, 128], value=16)
            if st.button("Apply Quantization", use_container_width=True, type="primary"):
                start_time = time.time()
                compressed = uniform_quantization(original, levels)
                process_time = time.time() - start_time
                
                st.session_state.processed_image = compressed
                mse, psnr = calculate_metrics(original, compressed)
                
                # Rough size estimate based on bits per channel
                bpc = int(np.log2(levels))
                comp_size = (h * w * 3 * bpc) / 8
                ratio = (comp_size / original_size_bytes) * 100
                
                st.markdown(f"**Metrics:**")
                cols = st.columns(4)
                cols[0].metric("Orig. Size", f"{original_size_bytes / 1024:.1f} KB")
                cols[1].metric("Est. Size", f"{comp_size / 1024:.1f} KB", f"-{100-ratio:.1f}%")
                cols[2].metric("PSNR", f"{psnr:.2f} dB")
                cols[3].metric("Time", f"{process_time:.3f} s")

        elif method == "Color Quantization (K-Means)":
            k_colors = st.slider("Number of Colors (K)", 2, 256, 16)
            if st.button("Apply K-Means", use_container_width=True, type="primary"):
                with st.spinner("Clustering colors..."):
                    start_time = time.time()
                    compressed = kmeans_quantization(original, k_colors)
                    process_time = time.time() - start_time
                    
                    st.session_state.processed_image = compressed
                    mse, psnr = calculate_metrics(original, compressed)
                    
                    st.markdown(f"**Metrics:**")
                    cols = st.columns(3)
                    cols[0].metric("PSNR", f"{psnr:.2f} dB")
                    cols[1].metric("MSE", f"{mse:.2f}")
                    cols[2].metric("Time", f"{process_time:.3f} s")

    else:
        # Lossless Analytical Mode
        st.info("Lossless compression does not degrade the image. The original image remains unchanged. The metrics below estimate the encoded data size.")
        method = st.selectbox("Algorithm", ["Huffman Coding", "Run-Length Encoding (RLE)", "Arithmetic Coding", "LZW Simulation"])
        
        if st.button("Analyze Compression", use_container_width=True, type="primary"):
            start_time = time.time()
            comp_size = original_size_bytes
            
            if method == "Huffman Coding":
                comp_size, entropy = huffman_encoding_size(original)
                st.caption(f"Calculated Image Entropy: {entropy:.3f} bits/pixel")
            elif method == "Run-Length Encoding (RLE)":
                comp_size = run_length_encoding_size(original)
            elif method == "Arithmetic Coding":
                comp_size = arithmetic_encoding_size(original)
            elif method == "LZW Simulation":
                # LZW is dictionary based, often achieves around 50-70% on continuous tone images
                # A true LZW on a 1080p image is very slow in Python.
                # We use a heuristic estimate bounded by Huffman but slightly worse for noise.
                _, entropy = huffman_encoding_size(original)
                comp_size = int((len(original.flatten()) * entropy * 1.1) / 8)
                st.caption("Using heuristic dictionary size estimation based on entropy.")
                
            process_time = time.time() - start_time
            ratio = (comp_size / original_size_bytes) * 100
            
            st.markdown(f"**Compression Metrics:**")
            cols = st.columns(4)
            cols[0].metric("Orig. Size", f"{original_size_bytes / 1024:.1f} KB")
            cols[1].metric("Comp. Size", f"{comp_size / 1024:.1f} KB", f"-{100-ratio:.1f}%")
            cols[2].metric("Ratio", f"{ratio:.1f}%")
            cols[3].metric("Time", f"{process_time:.3f} s")
            
            # Re-assign processed image to original so no visual change occurs
            st.session_state.processed_image = original.copy()

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    render_reset_and_save_buttons()
