import cv2
import numpy as np


def apply_translation(img, tx=0, ty=0):
    h, w = img.shape[:2]

    matrix = np.float32([
        [1, 0, tx],
        [0, 1, ty]
    ])

    return cv2.warpAffine(
        img,
        matrix,
        (w, h),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(229, 229, 234)
    )


def apply_scaling(img, scale=1.0):
    if scale == 1.0:
        return img.copy()

    h, w = img.shape[:2]

    new_w = max(1, int(w * scale))
    new_h = max(1, int(h * scale))

    return cv2.resize(
        img,
        (new_w, new_h),
        interpolation=cv2.INTER_LINEAR
    )


def apply_resize(img, width, height):
    return cv2.resize(
        img,
        (width, height),
        interpolation=cv2.INTER_LINEAR
    )


def apply_rotation(img, angle=0):
    if angle == 0:
        return img.copy()

    h, w = img.shape[:2]
    center = (w / 2, h / 2)

    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    # Calculate absolute cosine and sine of the rotation angle
    abs_cos = abs(matrix[0, 0])
    abs_sin = abs(matrix[0, 1])

    # Calculate the new bounding dimensions of the image
    bound_w = int(h * abs_sin + w * abs_cos)
    bound_h = int(h * abs_cos + w * abs_sin)

    # Adjust the rotation matrix to take into account the translation
    matrix[0, 2] += bound_w / 2 - center[0]
    matrix[1, 2] += bound_h / 2 - center[1]

    return cv2.warpAffine(
        img,
        matrix,
        (bound_w, bound_h),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(229, 229, 234)
    )


def apply_flip(img, horizontal=False, vertical=False):
    if horizontal and vertical:
        return cv2.flip(img, -1)
    elif horizontal:
        return cv2.flip(img, 1)
    elif vertical:
        return cv2.flip(img, 0)

    return img.copy()


def apply_center_crop(img, crop_ratio=1.0):
    if crop_ratio >= 1.0:
        return img.copy()

    h, w = img.shape[:2]

    crop_w = int(w * crop_ratio)
    crop_h = int(h * crop_ratio)

    x = (w - crop_w) // 2
    y = (h - crop_h) // 2

    return img[y:y + crop_h, x:x + crop_w]


def get_crop_dimensions(width, height, target_ratio):
    """
    Hitung dimensi crop berdasarkan target ratio
    
    Args:
        width: lebar gambar asli
        height: tinggi gambar asli
        target_ratio: rasio target (lebar/tinggi)
    
    Returns:
        (crop_width, crop_height): dimensi crop
    """
    img_ratio = width / height
    
    if target_ratio > img_ratio:
        # Target lebih lebar, batasi oleh lebar
        crop_width = width
        crop_height = int(width / target_ratio)
    else:
        # Target lebih tinggi, batasi oleh tinggi
        crop_height = height
        crop_width = int(height * target_ratio)
    
    # Pastikan tidak melebihi batas
    crop_width = min(crop_width, width)
    crop_height = min(crop_height, height)
    
    return crop_width, crop_height


def apply_ratio_crop(img, target_ratio, scale=1.0, x_offset=0, y_offset=0):
    """
    Crop gambar dengan target rasio tertentu dan skala
    
    Args:
        img: input image
        target_ratio: rasio target (lebar/tinggi)
        scale: skala crop (0.3 - 1.0), semakin kecil semakin luas area
        x_offset: offset horizontal dari kiri (0 = paling kiri)
        y_offset: offset vertikal dari atas (0 = paling atas)
    
    Returns:
        image hasil crop
    """
    h, w = img.shape[:2]
    
    # Hitung dimensi crop dasar
    base_crop_w, base_crop_h = get_crop_dimensions(w, h, target_ratio)
    
    # Terapkan skala
    crop_w = int(base_crop_w * scale)
    crop_h = int(base_crop_h * scale)
    
    # Pastikan tidak melebihi batas
    crop_w = min(crop_w, w)
    crop_h = min(crop_h, h)
    
    # Validasi offset
    max_x_offset = w - crop_w
    max_y_offset = h - crop_h
    
    x_offset = max(0, min(x_offset, max_x_offset))
    y_offset = max(0, min(y_offset, max_y_offset))
    
    # Lakukan crop
    result = img[y_offset:y_offset + crop_h, x_offset:x_offset + crop_w].copy()
    
    return result