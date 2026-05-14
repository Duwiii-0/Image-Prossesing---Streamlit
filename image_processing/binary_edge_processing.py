import cv2
import numpy as np


def apply_thresholding(img, threshold_value=127, max_value=255, method="Binary"):
    """
    Thresholding untuk menghasilkan citra biner
    
    Args:
        img: input image (numpy array)
        threshold_value: nilai ambang (0-255)
        max_value: nilai maksimum (biasanya 255)
        method: metode thresholding ("Binary", "Binary Inverse")
    
    Returns:
        image hasil thresholding (grayscale/biner)
    """
    # Konversi ke grayscale jika perlu
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img.copy()
    
    method_map = {
        "Binary": cv2.THRESH_BINARY,
        "Binary Inverse": cv2.THRESH_BINARY_INV,
    }
    
    thresh_method = method_map.get(method, cv2.THRESH_BINARY)
    _, result = cv2.threshold(gray, threshold_value, max_value, thresh_method)
    
    return result


def apply_adaptive_thresholding(img, max_value=255, method="Mean", block_size=11, C=2):
    """
    Adaptive Thresholding - threshold berbeda untuk setiap region
    
    Args:
        img: input image
        max_value: nilai maksimum
        method: "Mean" atau "Gaussian"
        block_size: ukuran blok (harus ganjil, min 3)
        C: konstanta yang dikurangkan dari mean
    
    Returns:
        image hasil adaptive thresholding
    """
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img.copy()
    
    if block_size % 2 == 0:
        block_size += 1
    if block_size < 3:
        block_size = 3
    
    method_map = {
        "Mean": cv2.ADAPTIVE_THRESH_MEAN_C,
        "Gaussian": cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    }
    
    adaptive_method = method_map.get(method, cv2.ADAPTIVE_THRESH_MEAN_C)
    result = cv2.adaptiveThreshold(gray, max_value, adaptive_method, cv2.THRESH_BINARY, block_size, C)
    
    return result


def apply_edge_detection(img, method="Canny", low_threshold=50, high_threshold=150, kernel_size=3, sobel_direction="Both", log_sigma=1.0):
    """
    Edge Detection dengan berbagai metode
    
    Args:
        img: input image
        method: "Canny", "Sobel", "Prewitt", "Roberts", "Laplacian", "LoG"
        low_threshold: threshold rendah (untuk Canny)
        high_threshold: threshold tinggi (untuk Canny)
        kernel_size: ukuran kernel (untuk Sobel, Laplacian)
        sobel_direction: "X", "Y", atau "Both" (untuk Sobel)
        log_sigma: sigma untuk Gaussian blur pada LoG
    
    Returns:
        image hasil edge detection
    """
    # Konversi ke grayscale
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img.copy()
    
    if method == "Canny":
        edges = cv2.Canny(gray, low_threshold, high_threshold)
    
    elif method == "Sobel":
        # Sobel X dan Y dengan direction option
        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=kernel_size)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=kernel_size)
        
        if sobel_direction == "X":
            edges = np.abs(sobel_x)
        elif sobel_direction == "Y":
            edges = np.abs(sobel_y)
        else:  # Both
            edges = np.sqrt(sobel_x**2 + sobel_y**2)
        
        edges = np.clip(edges, 0, 255).astype(np.uint8)
    
    elif method == "Prewitt":
        # Prewitt kernels
        kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
        kernel_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=np.float32)
        
        gray_float = gray.astype(np.float32)
        
        prewitt_x = cv2.filter2D(gray_float, -1, kernel_x)
        prewitt_y = cv2.filter2D(gray_float, -1, kernel_y)
        
        edges = np.sqrt(prewitt_x.astype(np.float64)**2 + prewitt_y.astype(np.float64)**2)
        edges = np.clip(edges, 0, 255).astype(np.uint8)
    
    elif method == "Roberts":
        # Roberts Cross kernels
        kernel_x = np.array([[1, 0], [0, -1]], dtype=np.float32)
        kernel_y = np.array([[0, 1], [-1, 0]], dtype=np.float32)
        
        gray_float = gray.astype(np.float32)
        
        roberts_x = cv2.filter2D(gray_float, -1, kernel_x)
        roberts_y = cv2.filter2D(gray_float, -1, kernel_y)
        
        edges = np.sqrt(roberts_x.astype(np.float64)**2 + roberts_y.astype(np.float64)**2)
        edges = np.clip(edges, 0, 255).astype(np.uint8)
    
    elif method == "Laplacian":
        edges = cv2.Laplacian(gray, cv2.CV_64F, ksize=kernel_size)
        edges = np.clip(np.abs(edges), 0, 255).astype(np.uint8)
    
    elif method == "LoG" or method == "Laplacian of Gaussian":
        # Laplacian of Gaussian - Gaussian blur dengan sigma tertentu
        blurred = cv2.GaussianBlur(gray, (0, 0), sigmaX=log_sigma, sigmaY=log_sigma)
        edges = cv2.Laplacian(blurred, cv2.CV_64F, ksize=kernel_size)
        edges = np.clip(np.abs(edges), 0, 255).astype(np.uint8)
    
    else:
        edges = cv2.Canny(gray, low_threshold, high_threshold)
    
    return edges


def apply_morphology(img, operation="Erosion", kernel_size=3, iterations=1):
    """
    Operasi morfologi: Erosion dan Dilation
    
    Args:
        img: input image (grayscale atau biner)
        operation: "Erosion" atau "Dilation"
        kernel_size: ukuran structuring element (3, 5, 7, dst)
        iterations: jumlah iterasi
    
    Returns:
        image hasil operasi morfologi
    """
    # Konversi ke grayscale jika perlu
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img.copy()
    
    # Buat kernel (structuring element)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    
    if operation == "Erosion":
        result = cv2.erode(gray, kernel, iterations=iterations)
    elif operation == "Dilation":
        result = cv2.dilate(gray, kernel, iterations=iterations)
    else:
        result = gray
    
    return result   