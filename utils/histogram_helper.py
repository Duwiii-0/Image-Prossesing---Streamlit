import cv2
import numpy as np
import matplotlib.pyplot as plt

def get_grayscale(image):
    if image is None:
        return None
    if len(image.shape) == 3:
        return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return image.copy()

def compute_histogram(image):
    gray = get_grayscale(image)
    if gray is None:
        return None
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    return hist.flatten()

def create_histogram_figure(hist, title="Histogram", color='#1D1D1F'):
    if hist is None:
        return None
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(range(256), hist, width=1.0, color=color, alpha=0.7)
    ax.set_xlim(0, 255)
    ax.set_title(title, fontsize=10)
    ax.set_xlabel("Intensity", fontsize=8)
    ax.set_ylabel("Pixel Count", fontsize=8)
    ax.tick_params(axis='both', labelsize=7)
    plt.tight_layout()
    return fig

def create_comparison_figure(hist_original, hist_processed):
    if hist_original is None or hist_processed is None:
        return None
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3))
    ax1.bar(range(256), hist_original, width=1.0, color='#1D1D1F', alpha=0.7)
    ax1.set_xlim(0, 255)
    ax1.set_title("Original Image", fontsize=10)
    ax1.set_xlabel("Intensity", fontsize=8)
    ax1.set_ylabel("Pixel Count", fontsize=8)
    
    ax2.bar(range(256), hist_processed, width=1.0, color='#0071E3', alpha=0.7)
    ax2.set_xlim(0, 255)
    ax2.set_title("Processed Image (Live)", fontsize=10)
    ax2.set_xlabel("Intensity", fontsize=8)
    ax2.set_ylabel("Pixel Count", fontsize=8)
    
    for ax in (ax1, ax2):
        ax.tick_params(axis='both', labelsize=7)
    plt.tight_layout()
    return fig