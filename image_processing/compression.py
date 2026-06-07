import numpy as np
import cv2
import heapq
from collections import Counter

def simulate_jpeg_compression(image, quality=50):
    """
    Simulates JPEG compression artifacts by applying DCT and Quantization.
    This uses cv2.imencode and cv2.imdecode as a robust way to simulate the exact JPEG pipeline 
    with quality control and get accurate visual artifacts.
    """
    # Menggunakan built-in JPEG encoder OpenCV untuk simulasi artefak yang paling akurat
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    result, encimg = cv2.imencode('.jpg', cv2.cvtColor(image, cv2.COLOR_RGB2BGR), encode_param)
    
    if result:
        decimg = cv2.imdecode(encimg, 1)
        # Calculate theoretical compressed size in bytes
        compressed_size = len(encimg)
        return cv2.cvtColor(decimg, cv2.COLOR_BGR2RGB), compressed_size
    return image, 0

def uniform_quantization(image, levels=4):
    """
    Reduces the color depth of the image uniformly.
    Levels usually are powers of 2. For 4 levels (2 bits), we drop 6 bits.
    """
    factor = 256 // levels
    quantized = (image // factor) * factor + (factor // 2)
    # Clip to uint8
    quantized = np.clip(quantized, 0, 255).astype(np.uint8)
    return quantized

def kmeans_quantization(image, k=8):
    """
    Reduces the total number of unique colors using K-Means clustering.
    """
    Z = image.reshape((-1, 3))
    Z = np.float32(Z)
    
    # Define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv2.kmeans(Z, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((image.shape))
    
    return res2

def run_length_encoding_size(image):
    """
    Simulates Run-Length Encoding. 
    Returns the estimated byte size of the encoded data.
    """
    flattened = image.flatten()
    # Menghitung titik perubahan menggunakan diff
    # +1 karena index differences, lalu ditambahkan index awal dan akhir
    changes = np.where(flattened[:-1] != flattened[1:])[0]
    num_runs = len(changes) + 1
    
    # 1 run biasanya disimpan sebagai pasangan (Value: 1 byte, Count: 2 bytes)
    # Rata-rata 3 bytes per run untuk gambar berwarna
    estimated_size_bytes = num_runs * 3
    return estimated_size_bytes

def huffman_encoding_size(image):
    """
    Simulates Huffman coding by calculating histogram entropy and tree depth.
    Returns estimated byte size.
    """
    flattened = image.flatten()
    # Hitung frekuensi piksel
    counts = np.bincount(flattened, minlength=256)
    probabilities = counts[counts > 0] / len(flattened)
    
    # Hitung Shannon Entropy (Lower bound kompresi Huffman)
    entropy = -np.sum(probabilities * np.log2(probabilities))
    
    # Estimasi ukuran terkompresi (Bits = Total Pixels * Entropy)
    estimated_bits = len(flattened) * entropy
    estimated_bytes = int(estimated_bits / 8)
    
    return estimated_bytes, entropy

def arithmetic_encoding_size(image):
    """
    Arithmetic coding often achieves close to theoretical entropy limit.
    Slightly better than Huffman but computationally heavy. We use a 
    heuristic multiplier of entropy.
    """
    flattened = image.flatten()
    counts = np.bincount(flattened, minlength=256)
    probabilities = counts[counts > 0] / len(flattened)
    
    entropy = -np.sum(probabilities * np.log2(probabilities))
    
    # Arithmetic biasanya mencapai 99% dari entropy ideal, 
    # sedangkan Huffman mungkin sedikit lebih boros karena integer bit length.
    estimated_bits = len(flattened) * (entropy * 0.98) 
    estimated_bytes = int(estimated_bits / 8)
    
    return estimated_bytes

def calculate_metrics(original, compressed):
    """
    Calculates MSE and PSNR.
    """
    mse = np.mean((original.astype(np.float64) - compressed.astype(np.float64)) ** 2)
    if mse == 0:
        psnr = 100 # Identik
    else:
        max_pixel = 255.0
        psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    
    return float(mse), float(psnr)
