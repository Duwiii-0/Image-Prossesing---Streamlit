import streamlit as st
import numpy as np
import time
import cv2

from utils.ui_helpers import render_section_header
from image_processing.compression import (
    simulate_jpeg_compression,
    uniform_quantization,
    kmeans_quantization,
    huffman_encoding_size,
    huffman_compress_to_bytes,
    rle_compress_to_bytes,
    arithmetic_compress_to_bytes,
    lzw_compress_to_bytes,
    calculate_metrics
)


def _render_metric(label, value, delta=None):
    """Render a single metric row as plain HTML — no grey card background."""
    delta_html = ""
    if delta is not None:
        color = "#4caf50" if delta.startswith("-") else "#f44336"
        delta_html = f' <span style="font-size:0.78rem;color:{color};">{delta}</span>'
    st.markdown(
        f"""
        <div style="padding:4px 0 6px 0; border-bottom:1px solid rgba(128,128,128,0.15); margin-bottom:2px;">
            <div style="font-size:0.72rem; color:#888; text-transform:uppercase; letter-spacing:0.05em;">{label}</div>
            <div style="font-size:1.05rem; font-weight:600; line-height:1.4;">{value}{delta_html}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def _encode_to_png_bytes(image_rgb):
    """Encode RGB numpy array to actual PNG bytes. Returns (bytes, size_in_bytes)."""
    _, buf = cv2.imencode('.png', cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR))
    return buf.tobytes(), len(buf)


def _delta_str(ratio):
    """Return formatted delta string based on size ratio."""
    if ratio < 100:
        return f"-{100 - ratio:.1f}%"
    return f"+{ratio - 100:.1f}%"


def render_image_compression_page():

    # Initialize state
    if "compression_mode" not in st.session_state:
        st.session_state.compression_mode = "Lossy (Visual)"

    mode = st.radio("Compression Type", ["Lossy (Visual)", "Lossless (Analytical)"], horizontal=True)
    st.session_state.compression_mode = mode

    original = st.session_state.original_image
    h, w, c = original.shape
    original_size_bytes = h * w * c

    # ── LOSSY ──────────────────────────────────────────────────────────────────
    if mode == "Lossy (Visual)":
        method = st.selectbox("Method", [
            "JPEG Simulation",
            "Uniform Quantization",
            "Color Quantization (K-Means)"
        ])

        # ── JPEG Simulation ──────────────────────────────────────────────────
        if method == "JPEG Simulation":
            quality = st.slider("JPEG Quality", 1, 100, 50)

            if st.button("Apply Compression", use_container_width=True, type="primary"):
                start = time.time()
                compressed, comp_size, jpeg_bytes = simulate_jpeg_compression(original, quality)
                elapsed = time.time() - start

                st.session_state.processed_image = compressed
                mse, psnr = calculate_metrics(original, compressed)
                ratio = (comp_size / original_size_bytes) * 100

                # Store export — bytes are the exact JPEG that was encoded
                st.session_state.compression_export = {
                    "bytes":    jpeg_bytes,
                    "filename": f"compressed_q{quality}.jpg",
                    "mime":     "image/jpeg",
                    "label":    "⬇️ Export as JPEG",
                }

                st.markdown("**Metrics:**")
                _render_metric("Orig. Size",  f"{original_size_bytes / 1024:.1f} KB")
                _render_metric("Comp. Size",  f"{comp_size / 1024:.1f} KB", _delta_str(ratio))
                _render_metric("Ratio",       f"{ratio:.1f}%")
                _render_metric("PSNR",        f"{psnr:.2f} dB")
                _render_metric("Time",        f"{elapsed:.3f} s")

        # ── Uniform Quantization ─────────────────────────────────────────────
        elif method == "Uniform Quantization":
            levels = st.select_slider(
                "Color Levels per Channel",
                options=[2, 4, 8, 16, 32, 64, 128],
                value=16
            )

            if st.button("Apply Quantization", use_container_width=True, type="primary"):
                start = time.time()
                compressed = uniform_quantization(original, levels)
                elapsed = time.time() - start

                st.session_state.processed_image = compressed
                mse, psnr = calculate_metrics(original, compressed)

                # Encode to PNG — size shown == size downloaded
                png_bytes, comp_size = _encode_to_png_bytes(compressed)
                ratio = (comp_size / original_size_bytes) * 100

                st.session_state.compression_export = {
                    "bytes":    png_bytes,
                    "filename": f"quantized_{levels}levels.png",
                    "mime":     "image/png",
                    "label":    "⬇️ Export as PNG",
                }

                st.markdown("**Metrics:**")
                _render_metric("Orig. Size",  f"{original_size_bytes / 1024:.1f} KB")
                _render_metric("Comp. Size",  f"{comp_size / 1024:.1f} KB", _delta_str(ratio))
                _render_metric("Ratio",       f"{ratio:.1f}%")
                _render_metric("PSNR",        f"{psnr:.2f} dB")
                _render_metric("Time",        f"{elapsed:.3f} s")

        # ── K-Means Quantization ─────────────────────────────────────────────
        elif method == "Color Quantization (K-Means)":
            k_colors = st.slider("Number of Colors (K)", 2, 256, 16)

            if st.button("Apply K-Means", use_container_width=True, type="primary"):
                with st.spinner("Clustering colors..."):
                    start = time.time()
                    compressed = kmeans_quantization(original, k_colors)
                    elapsed = time.time() - start

                    st.session_state.processed_image = compressed
                    mse, psnr = calculate_metrics(original, compressed)

                    # Encode to PNG — size shown == size downloaded
                    png_bytes, comp_size = _encode_to_png_bytes(compressed)
                    ratio = (comp_size / original_size_bytes) * 100

                    st.session_state.compression_export = {
                        "bytes":    png_bytes,
                        "filename": f"kmeans_{k_colors}colors.png",
                        "mime":     "image/png",
                        "label":    "⬇️ Export as PNG",
                    }

                    st.markdown("**Metrics:**")
                    _render_metric("Orig. Size",  f"{original_size_bytes / 1024:.1f} KB")
                    _render_metric("Comp. Size",  f"{comp_size / 1024:.1f} KB", _delta_str(ratio))
                    _render_metric("Ratio",       f"{ratio:.1f}%")
                    _render_metric("PSNR",        f"{psnr:.2f} dB")
                    _render_metric("MSE",         f"{mse:.2f}")
                    _render_metric("Time",        f"{elapsed:.3f} s")

    # ── LOSSLESS ───────────────────────────────────────────────────────────────
    else:
        st.info(
            "Lossless compression does not degrade the image. "
            "The original image remains unchanged. "
            "Data yang ditampilkan sesuai dengan ukuran file yang akan di-export."
        )
        method = st.selectbox("Algorithm", [
            "Huffman Coding",
            "Run-Length Encoding (RLE)",
            "Arithmetic Coding",
            "LZW Simulation"
        ])

        if st.button("Apply Compression", use_container_width=True, type="primary"):
            with st.spinner("Compressing..."):
                start = time.time()

                if method == "Huffman Coding":
                    comp_bytes, comp_size = huffman_compress_to_bytes(original)
                    _, entropy = huffman_encoding_size(original)
                    elapsed = time.time() - start
                    st.caption(f"Image Entropy: {entropy:.3f} bits/pixel")
                    export_cfg = {
                        "bytes":    comp_bytes,
                        "filename": "compressed_huffman.png",
                        "mime":     "image/png",
                        "label":    "⬇️ Export as PNG (Huffman)",
                    }

                elif method == "Run-Length Encoding (RLE)":
                    comp_bytes, comp_size = rle_compress_to_bytes(original)
                    elapsed = time.time() - start
                    export_cfg = {
                        "bytes":    comp_bytes,
                        "filename": "compressed_rle.png",
                        "mime":     "image/png",
                        "label":    "⬇️ Export as PNG (RLE)",
                    }

                elif method == "Arithmetic Coding":
                    comp_bytes, comp_size = arithmetic_compress_to_bytes(original)
                    elapsed = time.time() - start
                    export_cfg = {
                        "bytes":    comp_bytes,
                        "filename": "compressed_arithmetic.png",
                        "mime":     "image/png",
                        "label":    "⬇️ Export as PNG (Arithmetic)",
                    }

                elif method == "LZW Simulation":
                    comp_bytes, comp_size = lzw_compress_to_bytes(original)
                    elapsed = time.time() - start
                    st.caption("Dictionary-based compression via zlib (LZ77, similar to LZW).")
                    export_cfg = {
                        "bytes":    comp_bytes,
                        "filename": "compressed_lzw.png",
                        "mime":     "image/png",
                        "label":    "⬇️ Export as PNG (LZW)",
                    }

                ratio = (comp_size / original_size_bytes) * 100
                st.session_state.compression_export = export_cfg

                st.markdown("**Compression Metrics:**")
                _render_metric("Orig. Size",  f"{original_size_bytes / 1024:.1f} KB")
                _render_metric("Comp. Size",  f"{comp_size / 1024:.1f} KB", _delta_str(ratio))
                _render_metric("Ratio",       f"{ratio:.1f}%")
                _render_metric("Time",        f"{elapsed:.3f} s")

            st.session_state.processed_image = original.copy()

    # ── Persistent export button ───────────────────────────────────────────────
    exp = st.session_state.get("compression_export")
    if exp:
        st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
        st.download_button(
            label=exp["label"],
            data=exp["bytes"],
            file_name=exp["filename"],
            mime=exp["mime"],
            use_container_width=True,
        )

    # ── Reset ──────────────────────────────────────────────────────────────────
    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    if st.button("Reset Compression", use_container_width=True):
        st.session_state.processed_image = st.session_state.original_image.copy()
        st.session_state.pop("compression_export", None)
        st.rerun()
