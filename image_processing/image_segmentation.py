import cv2
import numpy as np


# ==================== THRESHOLD-BASED SEGMENTATION ====================

def apply_global_threshold(img, threshold_value=127, max_value=255):
    """
    Global threshold segmentation - Memisahkan objek dari background berdasarkan nilai intensitas
    
    Args:
        img: input image (numpy array)
        threshold_value: nilai threshold (0-255)
        max_value: nilai maksimum untuk piksel yang memenuhi threshold
    
    Returns:
        image hasil threshold (binary)
    """
    # Convert ke grayscale dulu
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img.copy()
    
    # Apply binary threshold
    _, binary = cv2.threshold(gray, threshold_value, max_value, cv2.THRESH_BINARY)
    
    return binary


def apply_adaptive_threshold(img, method='mean', block_size=11, c=2):
    """
    Adaptive threshold - Threshold berbeda untuk setiap region gambar
    
    Args:
        img: input image (numpy array)
        method: 'mean' atau 'gaussian'
        block_size: ukuran blok untuk perhitungan (harus ganjil, min 3)
        c: konstanta yang dikurangi dari mean atau weighted mean
    
    Returns:
        image hasil adaptive threshold
    """
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img.copy()
    
    if block_size < 3:
        block_size = 3
    if block_size % 2 == 0:
        block_size += 1
    
    if method == 'mean':
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                        cv2.THRESH_BINARY, block_size, c)
    else:
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                        cv2.THRESH_BINARY, block_size, c)
    
    return binary


def apply_otsu_threshold(img):
    """
    Otsu's threshold - Menentukan threshold optimal secara otomatis
    
    Args:
        img: input image (numpy array)
    
    Returns:
        image hasil Otsu threshold
    """
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img.copy()
    
    # Otsu's thresholding
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return binary


# ==================== EDGE-BASED SEGMENTATION ====================

def apply_canny_edge(img, low_threshold=50, high_threshold=150):
    """
    Canny Edge Detection - Algoritma edge detection multi-tahap
    
    Args:
        img: input image (numpy array)
        low_threshold: threshold rendah
        high_threshold: threshold tinggi
    
    Returns:
        image hasil edge detection (binary)
    """
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img.copy()
    
    # Apply Gaussian blur untuk mengurangi noise
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    
    # Canny edge detection
    edges = cv2.Canny(blurred, low_threshold, high_threshold)
    
    return edges


def apply_sobel_edge(img, kernel_size=3, direction='both'):
    """
    Sobel Edge Detection - Menggunakan turunan pertama untuk mendeteksi edge
    
    Args:
        img: input image (numpy array)
        kernel_size: ukuran kernel Sobel (1, 3, 5, 7)
        direction: 'x', 'y', atau 'both'
    
    Returns:
        image hasil edge detection
    """
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img.copy()
    
    # Pastikan kernel_size ganjil dan minimal 1
    if kernel_size < 1:
        kernel_size = 1
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    if direction == 'x':
        sobel = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=kernel_size)
    elif direction == 'y':
        sobel = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=kernel_size)
    else:  # both
        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=kernel_size)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=kernel_size)
        sobel = np.sqrt(sobel_x**2 + sobel_y**2)
    
    # Normalize ke 0-255
    sobel = np.uint8(np.clip(sobel, 0, 255))
    
    return sobel


def apply_laplacian_edge(img, kernel_size=3):
    """
    Laplacian Edge Detection - Menggunakan turunan kedua untuk mendeteksi edge
    
    Args:
        img: input image (numpy array)
        kernel_size: ukuran kernel (1, 3, 5, 7)
    
    Returns:
        image hasil edge detection
    """
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img.copy()
    
    if kernel_size < 1:
        kernel_size = 1
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    laplacian = cv2.Laplacian(gray, cv2.CV_64F, ksize=kernel_size)
    laplacian = np.uint8(np.clip(np.abs(laplacian), 0, 255))
    
    return laplacian


# ==================== REGION-BASED SEGMENTATION ====================

def apply_simple_region_growing(img, seed_point=None, threshold=10):
    """
    Region Growing sederhana - Mengembangkan region dari seed point berdasarkan kesamaan intensitas
    
    Args:
        img: input image (numpy array)
        seed_point: titik seed (x, y) - jika None, pilih titik tengah
        threshold: toleransi perbedaan intensitas
    
    Returns:
        binary image hasil region growing
    """
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img.copy()
    
    h, w = gray.shape
    
    # Jika seed point tidak ditentukan, pilih titik tengah
    if seed_point is None:
        seed_point = (w // 2, h // 2)
    
    # Pastikan seed point dalam batas gambar
    seed_x = max(0, min(seed_point[0], w-1))
    seed_y = max(0, min(seed_point[1], h-1))
    
    # Inisialisasi
    visited = np.zeros((h, w), dtype=bool)
    region = np.zeros((h, w), dtype=np.uint8)
    seed_value = int(gray[seed_y, seed_x])
    
    # Stack untuk BFS
    stack = [(seed_x, seed_y)]
    visited[seed_y, seed_x] = True
    
    # Direction: 4-connectivity
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while stack:
        x, y = stack.pop()
        
        # Cek apakah piksel ini termasuk dalam region
        if abs(int(gray[y, x]) - seed_value) <= threshold:
            region[y, x] = 255
            
            # Cek tetangga
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and not visited[ny, nx]:
                    visited[ny, nx] = True
                    stack.append((nx, ny))
    
    return region


def apply_watershed(img, marker_style='auto'):
    """
    Watershed algorithm - Segmentasi berbasis marker
    
    Args:
        img: input image (numpy array)
        marker_style: 'auto' atau 'distance'
    
    Returns:
        segmented image dengan label berbeda untuk setiap region
    """
    if len(img.shape) == 3:
        img_rgb = img.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img.copy()
        img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    
    # Thresholding untuk mendapatkan objek
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Noise removal
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    
    # Sure background area
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    
    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    
    # Marker labelling
    _, markers = cv2.connectedComponents(sure_fg)
    
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers + 1
    markers[unknown == 255] = 0
    
    # Apply watershed
    markers = cv2.watershed(img_rgb, markers)
    
    # Create output segmentation mask
    segments = np.zeros_like(gray)
    segments[markers > 1] = 255
    
    return segments


def apply_contour_segmentation(img, mode='external'):
    """
    Segmentasi berdasarkan contour detection
    
    Args:
        img: input image (numpy array)
        mode: 'external' (hanya contour luar) atau 'all' (semua contour)
    
    Returns:
        image dengan contours yang digambar
    """
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img.copy()
    
    # Binary threshold
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    # Find contours
    if mode == 'external':
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create output image
    output = np.zeros_like(gray)
    cv2.drawContours(output, contours, -1, 255, 1)
    
    return output


def apply_kmeans_segmentation(img, k=3):
    """
    K-Means clustering untuk segmentasi warna
    
    Args:
        img: input image (numpy array)
        k: jumlah cluster
    
    Returns:
        image hasil segmentasi dengan K-Means
    """
    # Reshape image ke 2D array
    data = img.reshape((-1, 3))
    data = np.float32(data)
    
    # Kriteria K-Means
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    
    # Apply K-Means
    _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    # Convert back to uint8
    centers = np.uint8(centers)
    
    # Reshape hasil
    segmented = centers[labels.flatten()]
    segmented = segmented.reshape(img.shape)
    
    return segmented