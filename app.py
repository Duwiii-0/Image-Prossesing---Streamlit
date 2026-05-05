import streamlit as st
import pandas as pd
import numpy as np
import cv2
from PIL import Image
import io

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Mini Photoshop",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CUSTOM CSS FOR UI/UX PRO MAX ---
st.markdown("""
<style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Typography & Background */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background-color: #F8FAFC;
        color: #0F172A;
    }
    
    /* Clean Layout Padding */
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
        max-width: 1200px;
    }

    /* Buttons */
    .stButton>button {
        background-color: #FFFFFF;
        color: #0F172A;
        border: 1px solid #CBD5E1;
        border-radius: 6px;
        font-weight: 500;
        font-size: 0.875rem;
        padding: 0.5rem 1rem;
        transition: all 0.2s ease;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    .stButton>button:hover {
        border-color: #94A3B8;
        background-color: #F1F5F9;
        transform: translateY(-1px);
    }
    .stButton>button:active {
        transform: translateY(0);
        background-color: #E2E8F0;
    }
    
    /* Primary CTA Button override */
    .stButton>button[kind="primary"] {
        background-color: #0F172A;
        color: #FFFFFF;
        border: 1px solid #0F172A;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .stButton>button[kind="primary"]:hover {
        background-color: #1E293B;
        border-color: #1E293B;
        color: #FFFFFF;
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
    
    .sidebar-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #0F172A;
        margin-bottom: 0.5rem;
        letter-spacing: -0.025em;
    }
    .sidebar-subtitle {
        font-size: 0.875rem;
        color: #64748B;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        border-bottom: 1px solid #E2E8F0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 0;
        gap: 1rem;
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
        font-weight: 500;
        color: #64748B;
    }
    .stTabs [aria-selected="true"] {
        color: #0F172A;
        border-bottom: 2px solid #0F172A;
    }
    
    /* Upload Component Styling */
    [data-testid="stFileUploadDropzone"] {
        background-color: #FFFFFF;
        border: 1px dashed #CBD5E1;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    [data-testid="stFileUploadDropzone"]:hover {
        border-color: #94A3B8;
        background-color: #F8FAFC;
    }

    /* Cards / Containers */
    .css-1r6slb0 {
        background-color: #FFFFFF;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        padding: 1.5rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    }
    
    /* Callouts / Info Boxes */
    .custom-info-box {
        background-color: #EFF6FF;
        border-left: 4px solid #3B82F6;
        padding: 1rem 1.5rem;
        border-radius: 4px;
        color: #1E3A8A;
        font-size: 0.9rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    /* Typography */
    h1 {
        font-size: 2.25rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em !important;
        color: #0F172A !important;
        margin-bottom: 0.5rem !important;
    }
    h2 {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        letter-spacing: -0.025em !important;
        color: #0F172A !important;
    }
    h3 {
        font-size: 1.125rem !important;
        font-weight: 600 !important;
        color: #1E293B !important;
    }
    p {
        color: #475569;
        font-size: 0.95rem;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'original_image' not in st.session_state:
    st.session_state.original_image = None
if 'processed_image' not in st.session_state:
    st.session_state.processed_image = None
if 'brightness' not in st.session_state:
    st.session_state.brightness = 0
if 'contrast' not in st.session_state:
    st.session_state.contrast = 0

# --- SIDEBAR (NAVIGATION ONLY) ---
with st.sidebar:
    st.markdown('<div class="sidebar-title">Mini Photoshop</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Digital Image Processing</div>', unsafe_allow_html=True)
    
    menu = st.radio(
        "Navigasi",
        ["Image Management", "Image Enhancement"],
        label_visibility="collapsed"
    )

# --- MAIN CONTENT AREA ---
st.title(menu)

# 1. IMAGE MANAGEMENT PAGE
if menu == "Image Management":
    st.markdown("Upload local images to begin editing or export your modified assets.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Upload File component
    uploaded_file = st.file_uploader("Select an Image (JPG, PNG, BMP)", type=["jpg", "png", "jpeg", "bmp"])
    
    if uploaded_file is not None:
        # Read image as PIL
        image = Image.open(uploaded_file).convert('RGB')
        image_np = np.array(image)
        
        # If a new file is uploaded
        if st.session_state.original_image is None or not np.array_equal(st.session_state.original_image, image_np):
            st.session_state.original_image = image_np.copy()
            st.session_state.processed_image = image_np.copy()
            # Reset states
            st.session_state.brightness = 0
            st.session_state.contrast = 0
            
    # Show Reset and Save if image is loaded
    if st.session_state.original_image is not None and st.session_state.processed_image is not None:
        
        st.markdown("<br>", unsafe_allow_html=True)
        col_btn1, col_btn2, col_spacer = st.columns([2, 2, 6])
        with col_btn1:
            if st.button("Reset to Original", use_container_width=True):
                st.session_state.processed_image = st.session_state.original_image.copy()
                st.session_state.brightness = 0
                st.session_state.contrast = 0
        
        with col_btn2:
            result_pil = Image.fromarray(st.session_state.processed_image)
            buf = io.BytesIO()
            result_pil.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.download_button(
                label="Save Edited Image",
                data=byte_im,
                file_name="edited_image.png",
                mime="image/png",
                use_container_width=True,
                type="primary"
            )
            
        st.markdown("<hr style='margin: 2rem 0; border: none; border-top: 1px solid #E2E8F0;' />", unsafe_allow_html=True)
        
        # Display Preview
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Original Image")
            st.image(st.session_state.original_image, use_column_width=True)
            
        with col2:
            st.markdown("### Current Image")
            st.image(st.session_state.processed_image, use_column_width=True)


# 2. IMAGE ENHANCEMENT PAGE
elif menu == "Image Enhancement":
    if st.session_state.processed_image is not None:
        st.markdown("Select a tool below to apply modifications to your image.")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Use Tabs to organize the operations in the main area
        tab1, tab2, tab3, tab4 = st.tabs([
            "Brightness & Contrast", 
            "Histogram Equalization", 
            "Sharpening", 
            "Smoothing (Blur)"
        ])
        
        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            col_sl1, col_sl2 = st.columns(2)
            with col_sl1:
                brightness = st.slider("Brightness", -100, 100, st.session_state.brightness, key='slider_bright')
            with col_sl2:
                contrast = st.slider("Contrast", -100, 100, st.session_state.contrast, key='slider_contr')
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Apply Brightness & Contrast", type="primary"):
                img = st.session_state.processed_image.copy()
                
                # Apply Contrast
                if contrast != 0:
                    f = 131 * (contrast + 127) / (127 * (131 - contrast))
                    alpha_c = f
                    gamma_c = 127 * (1 - f)
                    img = cv2.addWeighted(img, alpha_c, img, 0, gamma_c)
                
                # Apply Brightness
                if brightness != 0:
                    bright_arr = np.empty_like(img)
                    bright_arr.fill(abs(brightness))
                    
                    if brightness > 0:
                        img = cv2.add(img, bright_arr)
                    else:
                        img = cv2.subtract(img, bright_arr)
                        
                st.session_state.processed_image = img
                st.session_state.brightness = brightness
                st.session_state.contrast = contrast
                st.rerun()

        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("This operation automatically adjusts the image contrast by evenly distributing the intensity values across the histogram.")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Apply Histogram Equalization", type="primary"):
                img = st.session_state.processed_image.copy()
                if len(img.shape) == 3:
                    # RGB -> YUV
                    img_yuv = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
                    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
                    img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
                else:
                    img = cv2.equalizeHist(img)
                st.session_state.processed_image = img
                st.rerun()

        with tab3:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("Enhance the edges and details of the image using a convolution kernel matrix.")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Apply Sharpening", type="primary"):
                img = st.session_state.processed_image.copy()
                kernel = np.array([[-1,-1,-1], 
                                   [-1, 9,-1], 
                                   [-1,-1,-1]])
                img = cv2.filter2D(img, -1, kernel)
                st.session_state.processed_image = img
                st.rerun()

        with tab4:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("Smooth the image and reduce noise using a Gaussian filter.")
            blur_size = st.slider("Kernel Size (Gaussian)", 1, 15, 3, step=2)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Apply Smoothing", type="primary"):
                img = st.session_state.processed_image.copy()
                img = cv2.GaussianBlur(img, (blur_size, blur_size), 0)
                st.session_state.processed_image = img
                st.rerun()
                
        st.markdown("<hr style='margin: 2.5rem 0; border: none; border-top: 1px solid #E2E8F0;' />", unsafe_allow_html=True)
        
        # Live Preview at the bottom
        st.markdown("### Image Preview")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div style='color: #64748B; margin-bottom: 0.5rem; font-size: 0.875rem;'>Original Reference</div>", unsafe_allow_html=True)
            st.image(st.session_state.original_image, use_column_width=True)
            
        with col2:
            st.markdown("<div style='color: #0F172A; font-weight: 500; margin-bottom: 0.5rem; font-size: 0.875rem;'>Modified Output</div>", unsafe_allow_html=True)
            st.image(st.session_state.processed_image, use_column_width=True)
            
    else:
        st.markdown("""
        <div class="custom-info-box">
            <strong>Notice:</strong> Please upload an image via the Image Management menu before applying any enhancements.
        </div>
        """, unsafe_allow_html=True)
