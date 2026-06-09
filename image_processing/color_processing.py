import cv2
import numpy as np


def apply_rgb_to_grayscale(img):
    """
    Konversi RGB ke Grayscale
    
    Args:
        img: input image (RGB)
    
    Returns:
        image grayscale
    """
    if len(img.shape) == 2:
        return img.copy()
    
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def apply_channel_split(img):
    """
    Split channels RGB menjadi terpisah
    
    Args:
        img: input image (RGB)
    
    Returns:
        tuple of (R, G, B) channels
    """
    if len(img.shape) == 2:
        # If grayscale, return same image for all channels
        return img.copy(), img.copy(), img.copy()
    
    b, g, r = cv2.split(img)
    return r, g, b


def apply_hsv_adjustment(img, hue_shift=0, saturation_scale=1.0, value_scale=1.0):
    """
    Adjust Hue, Saturation, Value dalam HSV color space
    
    Args:
        img: input image (RGB)
        hue_shift: pergeseran hue (-180 sampai 180)
        saturation_scale: skala saturasi (0.0 sampai 2.0)
        value_scale: skala brightness (0.0 sampai 2.0)
    
    Returns:
        image dengan HSV adjustment
    """
    if len(img.shape) == 2:
        # For grayscale, hanya bisa adjust brightness
        result = img.copy().astype(np.float32)
        result = result * value_scale
        return np.clip(result, 0, 255).astype(np.uint8)
    
    # Konversi RGB ke HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV).astype(np.float32)
    
    # Adjust Hue (wrap around 0-180)
    if hue_shift != 0:
        hsv[:, :, 0] = (hsv[:, :, 0] + hue_shift) % 180
    
    # Adjust Saturation
    if saturation_scale != 1.0:
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation_scale, 0, 255)
    
    # Adjust Value (brightness)
    if value_scale != 1.0:
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * value_scale, 0, 255)
    
    # Konversi kembali ke RGB
    hsv = hsv.astype(np.uint8)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)


def apply_invert_colors(img):
    """
    Invert warna (negative image)
    
    Args:
        img: input image
    
    Returns:
        image dengan warna terbalik
    """
    return cv2.bitwise_not(img)


def apply_sepia_effect(img, intensity=1.0):
    """
    Apply sepia effect
    
    Args:
        img: input image
        intensity: intensitas sepia (0.0 - 1.0)
    
    Returns:
        image dengan efek sepia
    """
    if len(img.shape) == 2:
        # Convert grayscale to BGR first
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    
    # Sepia kernel
    sepia_kernel = np.array([[0.272, 0.534, 0.131],
                             [0.349, 0.686, 0.168],
                             [0.393, 0.769, 0.189]])
    
    sepia = cv2.transform(img, sepia_kernel)
    sepia = np.clip(sepia, 0, 255).astype(np.uint8)
    
    # Blend dengan original
    result = cv2.addWeighted(img, 1 - intensity, sepia, intensity, 0)
    return result


def apply_posterize(img, levels=4):
    """
    Posterize effect - mengurangi jumlah warna
    
    Args:
        img: input image
        levels: jumlah level warna per channel (2-8)
    
    Returns:
        image dengan efek posterize
    """
    # Jika levels 8, tidak ada perubahan 
    if levels >= 8:
        return img.copy()
    
    if levels < 2:
        levels = 2
    
    # Quantize ke jumlah levels
    levels_range = 256 / levels
    result = (img.astype(np.float32) // levels_range) * levels_range
    result = np.clip(result, 0, 255).astype(np.uint8)
    return result


def apply_color_balance(img, red_shift=0, green_shift=0, blue_shift=0):
    """
    Adjust color balance dengan mengubah channel individual
    
    Args:
        img: input image
        red_shift: pergeseran red channel (-100 sampai 100)
        green_shift: pergeseran green channel (-100 sampai 100)
        blue_shift: pergeseran blue channel (-100 sampai 100)
    
    Returns:
        image dengan color balance adjustment
    """
    if len(img.shape) == 2:
        return img.copy()
    
    result = img.copy().astype(np.float32)
    
    # Split channels
    r, g, b = cv2.split(result)
    
    # Apply shifts
    r = np.clip(r + red_shift, 0, 255)
    g = np.clip(g + green_shift, 0, 255)
    b = np.clip(b + blue_shift, 0, 255)
    
    # Merge back
    result = cv2.merge([b, g, r])
    return result.astype(np.uint8)


def get_channel_histogram(img, channel=None):
    """
    Get histogram untuk satu atau semua channels
    
    Args:
        img: input image
        channel: None (all) atau 0 (R), 1 (G), 2 (B) untuk RGB
    
    Returns:
        histogram data
    """
    if len(img.shape) == 2:
        # Grayscale
        hist = cv2.calcHist([img], [0], None, [256], [0, 256])
        return {'grayscale': hist}
    
    if channel is None:
        # All channels
        hist_r = cv2.calcHist([img], [0], None, [256], [0, 256])
        hist_g = cv2.calcHist([img], [1], None, [256], [0, 256])
        hist_b = cv2.calcHist([img], [2], None, [256], [0, 256])
        return {'R': hist_r, 'G': hist_g, 'B': hist_b}
    else:
        hist = cv2.calcHist([img], [channel], None, [256], [0, 256])
        return hist
