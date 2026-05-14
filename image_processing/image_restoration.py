import cv2
import numpy as np


def apply_gaussian_blur(img, kernel_size=3, sigma=0):
    """
    Gaussian Blur - Spatial filtering dengan kernel convolution
    
    Args:
        img: input image (numpy array)
        kernel_size: ukuran kernel (1, 3, 5, 7, dst) - 1 berarti tidak ada blur
        sigma: standar deviasi Gaussian (0 = auto dari kernel_size)
    
    Returns:
        image hasil Gaussian blur
    """
    # Jika kernel_size <= 1, kembalikan gambar asli (tidak ada efek)
    if kernel_size <= 1:
        return img.copy()
    
    # Pastikan kernel_size minimal 3 dan ganjil
    if kernel_size < 3 or kernel_size % 2 == 0:
        kernel_size = 3
    
    # Pastikan kernel_size ganjil
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    # cv2.GaussianBlur menggunakan kernel convolution Gaussian
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), sigma)


def apply_median_filter(img, kernel_size=3):
    """
    Median Filter - Spatial filtering non-linear
    
    Args:
        img: input image (numpy array)
        kernel_size: ukuran jendela (1, 3, 5, 7, dst) - 1 berarti tidak ada efek
    
    Returns:
        image hasil median filter
    """
    # Jika kernel_size <= 1, kembalikan gambar asli (tidak ada efek)
    if kernel_size <= 1:
        return img.copy()
    
    # Pastikan kernel_size minimal 3 dan ganjil
    if kernel_size < 3 or kernel_size % 2 == 0:
        kernel_size = 3
    
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    # cv2.medianBlur mengganti setiap piksel dengan nilai median dari tetangganya
    return cv2.medianBlur(img, kernel_size)


def apply_salt_pepper_removal(img, kernel_size=3):
    """
    Noise Removal khusus untuk Salt & Pepper noise
    Menggunakan median filter karena paling efektif untuk tipe noise ini
    
    Args:
        img: input image (numpy array)
        kernel_size: ukuran kernel untuk median filter (1 = tidak ada efek)
    
    Returns:
        image hasil noise removal
    """
    # Jika kernel_size <= 1, kembalikan gambar asli
    if kernel_size <= 1:
        return img.copy()
    
    # Median filter adalah metode terbaik untuk salt & pepper noise
    return apply_median_filter(img, kernel_size)


def add_salt_pepper_noise(img, salt_prob=0.01, pepper_prob=0.01):
    """
    Utility function untuk menambahkan salt & pepper noise ke gambar.
    Digunakan untuk testing atau demonstrasi.
    
    Args:
        img: input image (numpy array)
        salt_prob: probabilitas salt (piksel putih)
        pepper_prob: probabilitas pepper (piksel hitam)
    
    Returns:
        image dengan salt & pepper noise
    """
    img_copy = img.copy()
    h, w = img_copy.shape[:2]
    total_pixels = h * w
    
    # Salt (white) - untuk gambar grayscale atau color
    num_salt = int(total_pixels * salt_prob)
    salt_coords = [np.random.randint(0, i, num_salt) for i in (h, w)]
    
    if len(img_copy.shape) == 2:  # Grayscale
        img_copy[salt_coords[0], salt_coords[1]] = 255
    else:  # Color
        img_copy[salt_coords[0], salt_coords[1]] = [255, 255, 255]
    
    # Pepper (black)
    num_pepper = int(total_pixels * pepper_prob)
    pepper_coords = [np.random.randint(0, i, num_pepper) for i in (h, w)]
    
    if len(img_copy.shape) == 2:  # Grayscale
        img_copy[pepper_coords[0], pepper_coords[1]] = 0
    else:  # Color
        img_copy[pepper_coords[0], pepper_coords[1]] = [0, 0, 0]
    
    return img_copy