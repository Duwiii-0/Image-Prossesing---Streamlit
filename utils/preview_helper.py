import streamlit as st
from image_processing.apply_all_operations import apply_all_operations

def get_base_params():
    """Return dictionary of all parameters from session_state"""
    return {
        # Enhancement
        'brightness': st.session_state.brightness,
        'contrast': st.session_state.contrast,
        'blur_size': st.session_state.blur_size,
        'sharpening': st.session_state.sharpening,
        
        # Geometric
        'angle': st.session_state.rotation_angle,
        'translate_x': st.session_state.translate_x,
        'translate_y': st.session_state.translate_y,
        'scale': st.session_state.scale_factor,
        'crop_ratio': st.session_state.crop_ratio,
        'interpolation': st.session_state.interpolation_method,
        
        # Restoration
        'restoration_gaussian_kernel': st.session_state.restoration_gaussian_kernel,
        'restoration_median_kernel': st.session_state.restoration_median_kernel,
        'restoration_sp_kernel': st.session_state.restoration_sp_kernel,
        
        # Binary & Edge
        'binary_edge_mode': st.session_state.binary_edge_mode,
        'binary_threshold_value': st.session_state.binary_threshold_value,
        'binary_threshold_method': st.session_state.binary_threshold_method,
        'binary_adaptive_method': st.session_state.binary_adaptive_method,
        'binary_adaptive_block': st.session_state.binary_adaptive_block,
        'binary_adaptive_c': st.session_state.binary_adaptive_c,
        'edge_method': st.session_state.edge_method,
        'edge_low': st.session_state.edge_low,
        'edge_high': st.session_state.edge_high,
        'edge_kernel': st.session_state.edge_kernel,
        'edge_sobel_direction': st.session_state.edge_sobel_direction,
        'edge_log_sigma': st.session_state.edge_log_sigma,
        'morph_operation': st.session_state.morph_operation,
        'morph_kernel': st.session_state.morph_kernel,
        'morph_iterations': st.session_state.morph_iterations,
    }

def get_preview_image(extra_params=None):
    """Get preview image with optional extra parameters override"""
    params = get_base_params()
    if extra_params:
        params.update(extra_params)
    return apply_all_operations(st.session_state.processed_image, **params)