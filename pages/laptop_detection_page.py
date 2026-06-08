import streamlit as st
import numpy as np
from PIL import Image
import os
import time

# Lazy load Keras Classification Model
@st.cache_resource
def load_keras_model():
    """Load the custom trained MobileNetV2 classification model"""
    try:
        import tensorflow as tf
        model_path = "CNN/laptop_classifier.keras"
        if os.path.exists(model_path):
            model = tf.keras.models.load_model(model_path)
            return model
        return None
    except Exception as e:
        return f"Error loading model: {str(e)}"

def render_laptop_detection_page():
    # Initialize session state
    if 'ai_uploaded_image' not in st.session_state:
        st.session_state.ai_uploaded_image = None
    if 'ai_class_result' not in st.session_state:
        st.session_state.ai_class_result = None

    # Two Column Layout
    col_stage, col_inspector = st.columns([3, 1], gap="small")

    # Right side: Inspector Panel
    with col_inspector:
        st.markdown('<span class="section-label">Import Asset</span>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload Image",
            type=["jpg", "jpeg", "png", "bmp"],
            label_visibility="collapsed",
            key="ai_uploader"
        )

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            img_array = np.array(image)
            if st.session_state.ai_uploaded_image is None or not np.array_equal(st.session_state.ai_uploaded_image, img_array):
                st.session_state.ai_uploaded_image = img_array
                st.session_state.ai_class_result = "pending"

        st.markdown('<span class="section-label">Model Info</span>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background: rgba(0,0,0,0.02); border: 1px solid rgba(0,0,0,0.06); padding: 10px; border-radius: 8px; font-size: 0.8rem; color: #515154;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="font-weight: 600;">Base Model:</span>
                <span>MobileNetV2</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="font-weight: 600;">Method:</span>
                <span>Transfer Learning</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="font-weight: 600;">Accuracy:</span>
                <span style="color: #34C759; font-weight: 700;">94.0%</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="font-weight: 600;">Classes:</span>
                <span>Laptop / Not Laptop</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Left side: Main Stage
    with col_stage:
        if st.session_state.ai_uploaded_image is None:
            st.markdown("""
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 65vh; color: #86868B; background: #E5E5EA; padding: 3rem; border-radius: 12px;">
                <div style="font-size: 3.5rem; margin-bottom: 1.5rem; opacity: 0.4;">🧠</div>
                <div style="font-size: 1.35rem; font-weight: 600; color: #1D1D1F; margin-bottom: 0.5rem;">CNN Classifier Ready</div>
                <div style="font-size: 0.85rem; max-width: 380px; text-align: center; line-height: 1.4;">
                    Upload gambar di panel kanan untuk mendeteksi apakah gambar tersebut laptop atau bukan.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            img_np = st.session_state.ai_uploaded_image
            keras_model = load_keras_model()

            if keras_model is None:
                st.error("Model file 'CNN/laptop_classifier.keras' tidak ditemukan. Silakan train model terlebih dahulu.")
            elif isinstance(keras_model, str):
                st.error(f"Error: {keras_model}")
            else:
                if st.session_state.ai_class_result == "pending":
                    with st.spinner("Mengklasifikasi gambar..."):
                        import tensorflow as tf
                        img_pil = Image.fromarray(img_np)
                        img_resized = img_pil.resize((128, 128))
                        img_array = tf.keras.utils.img_to_array(img_resized)
                        img_array = np.expand_dims(img_array, axis=0)

                        start_time = time.time()
                        predictions = keras_model.predict(img_array, verbose=0)
                        latency = (time.time() - start_time) * 1000

                        probabilities = predictions[0]
                        predicted_class_idx = np.argmax(probabilities)
                        class_names = ["laptop", "not_laptop"]

                        st.session_state.ai_class_result = {
                            "class": class_names[predicted_class_idx],
                            "prob_laptop": probabilities[0] * 100,
                            "prob_not_laptop": probabilities[1] * 100,
                            "latency": latency
                        }

                c_res = st.session_state.ai_class_result
                if c_res and isinstance(c_res, dict):
                    col_img, col_metrics = st.columns([1, 1], gap="medium")

                    with col_img:
                        st.image(img_np, caption="Input Image", width="stretch")

                    with col_metrics:
                        is_laptop = c_res["class"] == "laptop"
                        theme_color = "#34C759" if is_laptop else "#FF3B30"
                        theme_bg = "rgba(52, 199, 89, 0.08)" if is_laptop else "rgba(255, 59, 48, 0.08)"
                        theme_border = "rgba(52, 199, 89, 0.2)" if is_laptop else "rgba(255, 59, 48, 0.2)"
                        badge_icon = "💻" if is_laptop else "🚫"
                        display_title = "LAPTOP" if is_laptop else "BUKAN LAPTOP"

                        st.markdown(f"""
                        <div style="background: {theme_bg}; border: 1px solid {theme_border}; border-radius: 12px; padding: 20px; text-align: center; margin-bottom: 1.5rem;">
                            <div style="font-size: 2.5rem; margin-bottom: 5px;">{badge_icon}</div>
                            <div style="font-size: 1.8rem; font-weight: 800; color: {theme_color}; margin: 5px 0;">{display_title}</div>
                            <div style="font-size: 1.1rem; font-weight: 600; color: #1D1D1F;">Confidence: {max(c_res["prob_laptop"], c_res["prob_not_laptop"]):.2f}%</div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown(f"💻 **Laptop** — {c_res['prob_laptop']:.2f}%")
                        st.progress(float(c_res["prob_laptop"] / 100.0))
                        st.markdown(f"🚫 **Non Laptop** — {c_res['prob_not_laptop']:.2f}%")
                        st.progress(float(c_res["prob_not_laptop"] / 100.0))

                        st.caption(f"Inference latency: {c_res['latency']:.1f} ms")

            # Reset button
            st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
            if st.button("Reset", use_container_width=True):
                st.session_state.ai_uploaded_image = None
                st.session_state.ai_class_result = None
                st.rerun()
