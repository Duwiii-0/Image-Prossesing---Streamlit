import numpy as np

from image_processing.image_enhancement import (
    apply_brightness_contrast,
    apply_gaussian_blur as apply_enhancement_blur,
    apply_sharpening,
    apply_histogram_equalization
)

from image_processing.geometric_transformation import (
    apply_rotation,
    apply_translation,
    apply_scaling,
    apply_center_crop,
    apply_ratio_crop,
)

from image_processing.image_restoration import (
    apply_gaussian_blur as apply_restoration_gaussian,
    apply_median_filter,
    apply_salt_pepper_removal,
)

from image_processing.binary_edge_processing import (
    apply_thresholding,
    apply_adaptive_thresholding,
    apply_edge_detection,
    apply_morphology,
)

from image_processing.image_segmentation import (
    apply_global_threshold,
    apply_adaptive_threshold as apply_seg_adaptive_threshold,
    apply_otsu_threshold,
    apply_canny_edge,
    apply_sobel_edge,
    apply_laplacian_edge,
    apply_simple_region_growing,
    apply_kmeans_segmentation,
    apply_contour_segmentation,
    apply_watershed,
)


def apply_geometric_only(
    base_image,
    angle=0,
    translate_x=0,
    translate_y=0,
    scale=1.0,
    crop_ratio=1.0,
    interpolation="Bilinear",
    crop_target_ratio=None,
    crop_scale=1.0,
    crop_x_offset=0,
    crop_y_offset=0
):
    """Geometric transformation saja"""
    if base_image is None or not isinstance(base_image, np.ndarray):
        return None
    
    img = base_image.copy()
    
    img = apply_rotation(img, angle=angle)
    img = apply_translation(img, tx=translate_x, ty=translate_y)
    
    if scale != 1.0:
        img = apply_scaling(img, scale=scale)
    
    if crop_target_ratio is not None or crop_scale < 1.0 or crop_x_offset != 0 or crop_y_offset != 0:
        # If target ratio is None (Original), calculate it dynamically based on CURRENT rotated image
        current_target_ratio = crop_target_ratio
        if current_target_ratio is None:
            curr_h, curr_w = img.shape[:2]
            current_target_ratio = curr_w / curr_h
            
        img = apply_ratio_crop(
            img,
            target_ratio=current_target_ratio,
            scale=crop_scale,
            x_offset=crop_x_offset,
            y_offset=crop_y_offset
        )
    
    if crop_ratio < 1.0:
        img = apply_center_crop(img, crop_ratio=crop_ratio)
    
    return img


def apply_all_operations(
    base_image,
    brightness=0,
    contrast=0,
    histogram_equalization_enabled=False,
    blur_size=1,
    sharpening=0,
    angle=0,
    translate_x=0,
    translate_y=0,
    scale=1.0,
    crop_ratio=1.0,
    interpolation="Bilinear",
    restoration_gaussian_kernel=1,
    restoration_median_kernel=1,
    restoration_sp_kernel=1,
    crop_target_ratio=None,
    crop_scale=1.0,
    crop_x_offset=0,
    crop_y_offset=0,
    threshold_enabled=False,
    edge_enabled=False,
    morph_enabled=False,
    threshold_type="simple",
    binary_edge_mode="none",
    binary_threshold_value=127,
    binary_threshold_method="Binary",
    binary_adaptive_method="Mean",
    binary_adaptive_block=11,
    binary_adaptive_c=2,
    edge_method="Canny",
    edge_low=50,
    edge_high=150,
    edge_kernel=3,
    edge_sobel_direction="Both",
    edge_log_sigma=1.0,
    morph_operation="Erosion",
    morph_kernel=3,
    morph_iterations=1,
    color_grayscale=False,
    color_hue_shift=0,
    color_saturation_scale=1.0,
    color_value_scale=1.0,
    color_invert=False,
    color_sepia_intensity=0.0,
    color_posterize_levels=4,
    color_red_shift=0,
    color_green_shift=0,
    color_blue_shift=0,
    segmentation_mode="none",  
    seg_threshold_enabled=False,
    seg_threshold_mode="None",
    seg_threshold_value=127,
    seg_adaptive_method="mean",
    seg_adaptive_block=11,
    seg_adaptive_c=2,
    seg_edge_enabled=False,
    seg_edge_method="None",
    seg_edge_low=50,
    seg_edge_high=150,
    seg_edge_kernel=3,
    seg_sobel_direction="both",
    seg_region_enabled=False,
    seg_region_method="None",
    seg_region_threshold=10,
    seg_kmeans_k=3,
    seg_contour_mode="external",
):
    """
    Full pipeline: Restoration -> Geometric -> Enhancement -> Segmentation -> Binary & Edge
    """
    if base_image is None or not isinstance(base_image, np.ndarray):
        return None
    
    img = base_image.copy()
    
    # STEP 1: IMAGE RESTORATION
    if restoration_gaussian_kernel > 1:
        img = apply_restoration_gaussian(img, kernel_size=restoration_gaussian_kernel)
    
    if restoration_median_kernel > 1:
        img = apply_median_filter(img, kernel_size=restoration_median_kernel)
    
    if restoration_sp_kernel > 1:
        img = apply_salt_pepper_removal(img, kernel_size=restoration_sp_kernel)
    
    # STEP 2: GEOMETRIC TRANSFORMATION 
    img = apply_geometric_only(
        img,
        angle=angle,
        translate_x=translate_x,
        translate_y=translate_y,
        scale=scale,
        crop_ratio=crop_ratio,
        interpolation=interpolation,
        crop_target_ratio=crop_target_ratio,
        crop_scale=crop_scale,
        crop_x_offset=crop_x_offset,
        crop_y_offset=crop_y_offset
    )
    
    if img is None:
        return base_image
    
    # STEP 3: ENHANCEMENT 
    img = apply_brightness_contrast(img, brightness=brightness, contrast=contrast)

    if histogram_equalization_enabled:
        img = apply_histogram_equalization(img)
    
    if blur_size > 1:
        img = apply_enhancement_blur(img, blur_size=blur_size)
    
    if sharpening > 0:
        img = apply_sharpening(img, strength=sharpening)

    # STEP 3.5: COLOR PROCESSING
    # Grayscale
    if color_grayscale:
        from image_processing.color_processing import apply_rgb_to_grayscale
        img = apply_rgb_to_grayscale(img)
        if len(img.shape) == 2:
            img = np.stack([img] * 3, axis=2)
    
    # HSV Adjustment
    if color_hue_shift != 0 or color_saturation_scale != 1.0 or color_value_scale != 1.0:
        from image_processing.color_processing import apply_hsv_adjustment
        img = apply_hsv_adjustment(img, color_hue_shift, color_saturation_scale, color_value_scale)
    
    # Invert
    if color_invert:
        from image_processing.color_processing import apply_invert_colors
        img = apply_invert_colors(img)
    
    # Sepia
    if color_sepia_intensity > 0:
        from image_processing.color_processing import apply_sepia_effect
        img = apply_sepia_effect(img, color_sepia_intensity)
    
    # Posterize
    if color_posterize_levels < 8:
        from image_processing.color_processing import apply_posterize
        img = apply_posterize(img, color_posterize_levels)
    
    # Color Balance
    if color_red_shift != 0 or color_green_shift != 0 or color_blue_shift != 0:
        from image_processing.color_processing import apply_color_balance
        img = apply_color_balance(img, color_red_shift, color_green_shift, color_blue_shift)
    
    # STEP 4: IMAGE SEGMENTATION (PIPELINE)
    # 4a. Threshold-based segmentation
    if seg_threshold_enabled:
        if seg_threshold_mode == "Global":
            img = apply_global_threshold(img, threshold_value=seg_threshold_value)
        elif seg_threshold_mode == "Adaptive":
            img = apply_seg_adaptive_threshold(img, method=seg_adaptive_method, block_size=seg_adaptive_block, c=seg_adaptive_c)
        elif seg_threshold_mode == "Otsu":
            img = apply_otsu_threshold(img)

    # 4b. Edge-based segmentation
    if seg_edge_enabled:
        if seg_edge_method == "Canny":
            img = apply_canny_edge(img, low_threshold=seg_edge_low, high_threshold=seg_edge_high)
        elif seg_edge_method == "Sobel":
            img = apply_sobel_edge(img, kernel_size=seg_edge_kernel, direction=seg_sobel_direction)
        elif seg_edge_method == "Laplacian":
            img = apply_laplacian_edge(img, kernel_size=seg_edge_kernel)

    # 4c. Region-based segmentation
    if seg_region_enabled:
        if seg_region_method == "Region Growing":
            img = apply_simple_region_growing(img, threshold=seg_region_threshold)
        elif seg_region_method == "K-Means":
            img = apply_kmeans_segmentation(img, k=seg_kmeans_k)
        elif seg_region_method == "Contour":
            img = apply_contour_segmentation(img, mode=seg_contour_mode)
        elif seg_region_method == "Watershed":
            img = apply_watershed(img)

    # Convert binary image (2D) to 3 channel (jika perlu)
    if len(img.shape) == 2:
        img = np.stack([img] * 3, axis=2)
    
    # STEP 5: BINARY & EDGE PROCESSING (PIPELINE)
    # Terapkan threshold terlebih dahulu jika diaktifkan
    if threshold_enabled:
        if threshold_type == "simple":
            img = apply_thresholding(
                img,
                threshold_value=binary_threshold_value,
                method=binary_threshold_method
            )
        else:  # adaptive
            img = apply_adaptive_thresholding(
                img,
                method=binary_adaptive_method,
                block_size=binary_adaptive_block,
                C=binary_adaptive_c
            )
    # Kemudian edge detection jika diaktifkan
    if edge_enabled:
        img = apply_edge_detection(
            img,
            method=edge_method,
            low_threshold=edge_low,
            high_threshold=edge_high,
            kernel_size=edge_kernel,
            sobel_direction=edge_sobel_direction,
            log_sigma=edge_log_sigma
        )
    # Terakhir morphology jika diaktifkan
    if morph_enabled:
        img = apply_morphology(
            img,
            operation=morph_operation,
            kernel_size=morph_kernel,
            iterations=morph_iterations
        )
    
    return img