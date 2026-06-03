import numpy as np

from image_processing.image_enhancement import (
    apply_brightness_contrast,
    apply_gaussian_blur as apply_enhancement_blur,
    apply_sharpening,
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
    
    if crop_target_ratio is not None:
        img = apply_ratio_crop(
            img,
            target_ratio=crop_target_ratio,
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
    segmentation_mode="none",  
    seg_threshold_value=127,
    seg_adaptive_method="mean",
    seg_adaptive_block=11,
    seg_adaptive_c=2,
    seg_edge_low=50,
    seg_edge_high=150,
    seg_edge_kernel=3,
    seg_sobel_direction="both",
    seg_region_threshold=10,
    seg_kmeans_k=3,
    seg_contour_mode="external"
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
    
    if blur_size > 1:
        img = apply_enhancement_blur(img, blur_size=blur_size)
    
    if sharpening > 0:
        img = apply_sharpening(img, strength=sharpening)
    
    # STEP 4: IMAGE SEGMENTATION
    if segmentation_mode == "threshold_global":
        img = apply_global_threshold(img, threshold_value=seg_threshold_value)
    elif segmentation_mode == "threshold_adaptive":
        img = apply_seg_adaptive_threshold(img, method=seg_adaptive_method, block_size=seg_adaptive_block, c=seg_adaptive_c)
    elif segmentation_mode == "threshold_otsu":
        img = apply_otsu_threshold(img)
    elif segmentation_mode == "edge_canny":
        img = apply_canny_edge(img, low_threshold=seg_edge_low, high_threshold=seg_edge_high)
    elif segmentation_mode == "edge_sobel":
        img = apply_sobel_edge(img, kernel_size=seg_edge_kernel, direction=seg_sobel_direction)
    elif segmentation_mode == "edge_laplacian":
        img = apply_laplacian_edge(img, kernel_size=seg_edge_kernel)
    elif segmentation_mode == "region_growing":
        img = apply_simple_region_growing(img, threshold=seg_region_threshold)
    elif segmentation_mode == "kmeans":
        img = apply_kmeans_segmentation(img, k=seg_kmeans_k)
    elif segmentation_mode == "contour":
        img = apply_contour_segmentation(img, mode=seg_contour_mode)
    elif segmentation_mode == "watershed":
        img = apply_watershed(img)
    
    # Convert binary image (2D) to 3 channel
    if len(img.shape) == 2:
        img = np.stack([img] * 3, axis=2)
    
    # STEP 5: BINARY & EDGE PROCESSING 
    if binary_edge_mode == "threshold":
        img = apply_thresholding(
            img,
            threshold_value=binary_threshold_value,
            method=binary_threshold_method
        )
    elif binary_edge_mode == "adaptive_threshold":
        img = apply_adaptive_thresholding(
            img,
            method=binary_adaptive_method,
            block_size=binary_adaptive_block,
            C=binary_adaptive_c
        )
    elif binary_edge_mode == "edge":
        img = apply_edge_detection(
            img,
            method=edge_method,
            low_threshold=edge_low,
            high_threshold=edge_high,
            kernel_size=edge_kernel,
            sobel_direction=edge_sobel_direction,
            log_sigma=edge_log_sigma
        )
    elif binary_edge_mode == "morphology":
        img = apply_morphology(
            img,
            operation=morph_operation,
            kernel_size=morph_kernel,
            iterations=morph_iterations
        )
    
    return img