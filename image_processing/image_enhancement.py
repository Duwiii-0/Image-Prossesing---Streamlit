import cv2
import numpy as np

def apply_brightness_contrast(img, brightness=0, contrast=0):
    alpha = (contrast + 100) / 100.0
    beta = brightness
    img_result = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

    return img_result


def apply_histogram_equalization(img):
    img_result = img.copy()
    
    if len(img_result.shape) == 3:
        # For RGB images, convert to YUV and equalize only Y channel
        img_yuv = cv2.cvtColor(img_result, cv2.COLOR_RGB2YUV)
        img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
        img_result = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
    else:
        # For grayscale images
        img_result = cv2.equalizeHist(img_result)
    
    return img_result


def apply_sharpening(img, strength=0):
    if strength <= 0:
        return img.copy()

    # Blur untuk mendapatkan detail
    blurred = cv2.GaussianBlur(img, (0, 0), sigmaX=2.0)

    # Mapping 0–100 -> 0.0–8.0
    # Jadi di nilai kecil pun efek udah terasa.
    amount = strength / 100.0 * 8.0

    # Sharpen
    result = cv2.addWeighted(
        img,
        1.0 + amount,
        blurred,
        -amount,
        0
    )

    return result


def apply_gaussian_blur(img, blur_size=3):
    # Jika blur_size <= 1, tidak perlu blur
    if blur_size <= 1:
        return img.copy()

    # Pastikan ukuran kernel ganjil
    if blur_size % 2 == 0:
        blur_size += 1

    return cv2.GaussianBlur(img, (blur_size, blur_size), 0)