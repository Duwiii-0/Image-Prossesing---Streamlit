import streamlit as st
from utils.constants import *

def init_session_state():
    """Initialize all session state variables"""
    if 'original_image' not in st.session_state:
        st.session_state.original_image = None
    if 'processed_image' not in st.session_state:
        st.session_state.processed_image = None
    
    # Enhancement
    if 'brightness' not in st.session_state:
        st.session_state.brightness = DEFAULT_BRIGHTNESS
    if 'contrast' not in st.session_state:
        st.session_state.contrast = DEFAULT_CONTRAST
    if 'histogram_equalization_enabled' not in st.session_state:
        st.session_state.histogram_equalization_enabled = False
    if 'blur_size' not in st.session_state:
        st.session_state.blur_size = DEFAULT_BLUR_SIZE
    if 'sharpening' not in st.session_state:
        st.session_state.sharpening = DEFAULT_SHARPENING
    
    # Geometric
    if 'rotation_angle' not in st.session_state:
        st.session_state.rotation_angle = DEFAULT_ROTATION_ANGLE
    if 'translate_x' not in st.session_state:
        st.session_state.translate_x = DEFAULT_TRANSLATE_X
    if 'translate_y' not in st.session_state:
        st.session_state.translate_y = DEFAULT_TRANSLATE_Y
    if 'scale_factor' not in st.session_state:
        st.session_state.scale_factor = DEFAULT_SCALE_FACTOR
    if 'crop_ratio' not in st.session_state:
        st.session_state.crop_ratio = DEFAULT_CROP_RATIO
    if 'interpolation_method' not in st.session_state:
        st.session_state.interpolation_method = DEFAULT_INTERPOLATION
    
    # Crop 
    if 'enable_live_crop' not in st.session_state:
        st.session_state.enable_live_crop = False
    if 'crop_target_ratio' not in st.session_state:
        st.session_state.crop_target_ratio = DEFAULT_CROP_TARGET_RATIO
    if 'crop_scale' not in st.session_state:
        st.session_state.crop_scale = DEFAULT_CROP_SCALE
    if 'crop_x_offset' not in st.session_state:
        st.session_state.crop_x_offset = DEFAULT_CROP_X_OFFSET
    if 'crop_y_offset' not in st.session_state:
        st.session_state.crop_y_offset = DEFAULT_CROP_Y_OFFSET
    if 'crop_ratio_selected' not in st.session_state:
        st.session_state.crop_ratio_selected = DEFAULT_CROP_RATIO_SELECTED
    
    # Restoration
    if 'restoration_gaussian_kernel' not in st.session_state:
        st.session_state.restoration_gaussian_kernel = DEFAULT_RESTORATION_GAUSSIAN_KERNEL
    if 'restoration_median_kernel' not in st.session_state:
        st.session_state.restoration_median_kernel = DEFAULT_RESTORATION_MEDIAN_KERNEL
    if 'restoration_sp_kernel' not in st.session_state:
        st.session_state.restoration_sp_kernel = DEFAULT_RESTORATION_SP_KERNEL
    
    # Binary & Edge
    if 'threshold_enabled' not in st.session_state:
        st.session_state.threshold_enabled = False
    if 'edge_enabled' not in st.session_state:
        st.session_state.edge_enabled = False
    if 'morph_enabled' not in st.session_state:
        st.session_state.morph_enabled = False
    if 'threshold_type' not in st.session_state:
        st.session_state.threshold_type = "simple"   
    if 'binary_threshold_value' not in st.session_state:
        st.session_state.binary_threshold_value = DEFAULT_BINARY_THRESHOLD_VALUE
    if 'binary_threshold_method' not in st.session_state:
        st.session_state.binary_threshold_method = DEFAULT_BINARY_THRESHOLD_METHOD
    if 'binary_adaptive_method' not in st.session_state:
        st.session_state.binary_adaptive_method = DEFAULT_BINARY_ADAPTIVE_METHOD
    if 'binary_adaptive_block' not in st.session_state:
        st.session_state.binary_adaptive_block = DEFAULT_BINARY_ADAPTIVE_BLOCK
    if 'binary_adaptive_c' not in st.session_state:
        st.session_state.binary_adaptive_c = DEFAULT_BINARY_ADAPTIVE_C
    if 'edge_method' not in st.session_state:
        st.session_state.edge_method = "None"
    if 'edge_low' not in st.session_state:
        st.session_state.edge_low = DEFAULT_EDGE_LOW
    if 'edge_high' not in st.session_state:
        st.session_state.edge_high = DEFAULT_EDGE_HIGH
    if 'edge_kernel' not in st.session_state:
        st.session_state.edge_kernel = DEFAULT_EDGE_KERNEL
    if 'edge_sobel_direction' not in st.session_state:
        st.session_state.edge_sobel_direction = DEFAULT_EDGE_SOBEL_DIRECTION
    if 'edge_log_sigma' not in st.session_state:
        st.session_state.edge_log_sigma = DEFAULT_EDGE_LOG_SIGMA
    if 'morph_operation' not in st.session_state:
        st.session_state.morph_operation = "None"
    if 'morph_kernel' not in st.session_state:
        st.session_state.morph_kernel = DEFAULT_MORPH_KERNEL
    if 'morph_iterations' not in st.session_state:
        st.session_state.morph_iterations = DEFAULT_MORPH_ITERATIONS

    # Color Processing
    if 'color_processing_state' not in st.session_state:
        st.session_state.color_processing_state = {
            'operation': 'None',
            'grayscale': False,
            'channel_split': False,
            'hue_shift': 0,
            'saturation_scale': 1.0,
            'value_scale': 1.0,
            'invert': False,
            'sepia_intensity': 0.0,
            'posterize_levels': 8,
            'red_shift': 0,
            'green_shift': 0,
            'blue_shift': 0,
        }

    # Segmentation
    if 'segmentation_mode' not in st.session_state:
        st.session_state.segmentation_mode = "none"
    if 'seg_threshold_enabled' not in st.session_state:
        st.session_state.seg_threshold_enabled = False
    if 'seg_edge_enabled' not in st.session_state:
        st.session_state.seg_edge_enabled = False
    if 'seg_region_enabled' not in st.session_state:
        st.session_state.seg_region_enabled = False
    if 'seg_threshold_mode' not in st.session_state:
        st.session_state.seg_threshold_mode = DEFAULT_THRESHOLD_MODE
    if 'seg_threshold_value' not in st.session_state:
        st.session_state.seg_threshold_value = DEFAULT_THRESHOLD_VALUE
    if 'seg_adaptive_method' not in st.session_state:
        st.session_state.seg_adaptive_method = DEFAULT_ADAPTIVE_METHOD
    if 'seg_adaptive_block' not in st.session_state:
        st.session_state.seg_adaptive_block = DEFAULT_ADAPTIVE_BLOCK
    if 'seg_adaptive_c' not in st.session_state:
        st.session_state.seg_adaptive_c = DEFAULT_ADAPTIVE_C
    if 'seg_edge_method' not in st.session_state:
        st.session_state.seg_edge_method = DEFAULT_SEG_EDGE_METHOD
    if 'seg_edge_low' not in st.session_state:
        st.session_state.seg_edge_low = DEFAULT_SEG_EDGE_LOW
    if 'seg_edge_high' not in st.session_state:
        st.session_state.seg_edge_high = DEFAULT_SEG_EDGE_HIGH
    if 'seg_edge_kernel' not in st.session_state:
        st.session_state.seg_edge_kernel = DEFAULT_SEG_EDGE_KERNEL
    if 'seg_sobel_direction' not in st.session_state:
        st.session_state.seg_sobel_direction = DEFAULT_SEG_SOBEL_DIRECTION
    if 'seg_region_method' not in st.session_state:
        st.session_state.seg_region_method = DEFAULT_REGION_METHOD
    if 'seg_region_threshold' not in st.session_state:
        st.session_state.seg_region_threshold = DEFAULT_REGION_THRESHOLD
    if 'seg_kmeans_k' not in st.session_state:
        st.session_state.seg_kmeans_k = DEFAULT_KMEANS_K
    if 'seg_contour_mode' not in st.session_state:
        st.session_state.seg_contour_mode = DEFAULT_CONTOUR_MODE

def reset_enhancement_state():
    """Reset only enhancement state to defaults"""
    st.session_state.brightness = DEFAULT_BRIGHTNESS
    st.session_state.contrast = DEFAULT_CONTRAST
    st.session_state.histogram_equalization_enabled = False
    st.session_state.blur_size = DEFAULT_BLUR_SIZE
    st.session_state.sharpening = DEFAULT_SHARPENING

def reset_geometric_state():
    """Reset only geometric state to defaults"""
    st.session_state.rotation_angle = DEFAULT_ROTATION_ANGLE
    st.session_state.translate_x = DEFAULT_TRANSLATE_X
    st.session_state.translate_y = DEFAULT_TRANSLATE_Y
    st.session_state.scale_factor = DEFAULT_SCALE_FACTOR
    st.session_state.crop_ratio = DEFAULT_CROP_RATIO
    st.session_state.interpolation_method = DEFAULT_INTERPOLATION

def reset_crop_state():
    """Reset only crop state to defaults"""
    st.session_state.enable_live_crop = False
    st.session_state.crop_target_ratio = DEFAULT_CROP_TARGET_RATIO
    st.session_state.crop_scale = DEFAULT_CROP_SCALE
    st.session_state.crop_x_offset = DEFAULT_CROP_X_OFFSET
    st.session_state.crop_y_offset = DEFAULT_CROP_Y_OFFSET
    st.session_state.crop_ratio_selected = DEFAULT_CROP_RATIO_SELECTED

def reset_restoration_state():
    """Reset only restoration state to defaults"""
    st.session_state.restoration_gaussian_kernel = DEFAULT_RESTORATION_GAUSSIAN_KERNEL
    st.session_state.restoration_median_kernel = DEFAULT_RESTORATION_MEDIAN_KERNEL
    st.session_state.restoration_sp_kernel = DEFAULT_RESTORATION_SP_KERNEL

def reset_binary_edge_state():
    st.session_state.threshold_enabled = False
    st.session_state.edge_enabled = False
    st.session_state.morph_enabled = False
    st.session_state.threshold_type = "simple"
    st.session_state.binary_threshold_value = DEFAULT_BINARY_THRESHOLD_VALUE
    st.session_state.binary_threshold_method = DEFAULT_BINARY_THRESHOLD_METHOD
    st.session_state.binary_adaptive_method = DEFAULT_BINARY_ADAPTIVE_METHOD
    st.session_state.binary_adaptive_block = DEFAULT_BINARY_ADAPTIVE_BLOCK
    st.session_state.binary_adaptive_c = DEFAULT_BINARY_ADAPTIVE_C
    st.session_state.edge_method = "None"        
    st.session_state.edge_low = DEFAULT_EDGE_LOW
    st.session_state.edge_high = DEFAULT_EDGE_HIGH
    st.session_state.edge_kernel = DEFAULT_EDGE_KERNEL
    st.session_state.edge_sobel_direction = DEFAULT_EDGE_SOBEL_DIRECTION
    st.session_state.edge_log_sigma = DEFAULT_EDGE_LOG_SIGMA
    st.session_state.morph_operation = "None"    
    st.session_state.morph_kernel = DEFAULT_MORPH_KERNEL
    st.session_state.morph_iterations = DEFAULT_MORPH_ITERATIONS

def reset_color_processing_state():
    """Reset only color processing state to defaults"""
    st.session_state.color_processing_state = {
        'grayscale': False,
        'channel_split': False,
        'hue_shift': 0,
        'saturation_scale': 1.0,
        'value_scale': 1.0,
        'invert': False,
        'sepia_intensity': 0.0,
        'posterize_levels': 8,
        'red_shift': 0,
        'green_shift': 0,
        'blue_shift': 0,
    }

def reset_segmentation_state():
    st.session_state.seg_threshold_enabled = False
    st.session_state.seg_edge_enabled = False
    st.session_state.seg_region_enabled = False
    st.session_state.seg_threshold_mode = DEFAULT_THRESHOLD_MODE
    st.session_state.seg_threshold_value = DEFAULT_THRESHOLD_VALUE
    st.session_state.seg_adaptive_method = DEFAULT_ADAPTIVE_METHOD
    st.session_state.seg_adaptive_block = DEFAULT_ADAPTIVE_BLOCK
    st.session_state.seg_adaptive_c = DEFAULT_ADAPTIVE_C
    st.session_state.seg_edge_method = DEFAULT_SEG_EDGE_METHOD
    st.session_state.seg_edge_low = DEFAULT_SEG_EDGE_LOW
    st.session_state.seg_edge_high = DEFAULT_SEG_EDGE_HIGH
    st.session_state.seg_edge_kernel = DEFAULT_SEG_EDGE_KERNEL
    st.session_state.seg_sobel_direction = DEFAULT_SEG_SOBEL_DIRECTION
    st.session_state.seg_region_method = DEFAULT_REGION_METHOD
    st.session_state.seg_region_threshold = DEFAULT_REGION_THRESHOLD
    st.session_state.seg_kmeans_k = DEFAULT_KMEANS_K
    st.session_state.seg_contour_mode = DEFAULT_CONTOUR_MODE

def reset_all_state():
    """Reset all state to defaults (keep images intact)"""
    reset_enhancement_state()
    reset_geometric_state()
    reset_crop_state()
    reset_restoration_state()
    reset_binary_edge_state()
    reset_color_processing_state()
    reset_segmentation_state()