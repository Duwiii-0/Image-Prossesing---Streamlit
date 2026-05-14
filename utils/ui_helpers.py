import streamlit as st
import io
from PIL import Image

def load_css():
    """Load custom CSS from style.css file"""
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

def render_image_preview(image_left, image_right, title_left="Original Reference", title_right="Modified Output"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**{title_left}**")
        st.image(image_left, use_container_width=True)
    with col2:
        st.markdown(f"**{title_right}**")
        st.image(image_right, use_container_width=True)

def create_download_button(image, filename="edited_image.png", button_text="Save Edited Image"):
    """Create download button for image"""
    result_pil = Image.fromarray(image)
    buf = io.BytesIO()
    result_pil.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.download_button(
        label=button_text,
        data=byte_im,
        file_name=filename,
        mime="image/png",
        use_container_width=True,
        type="primary"
    )

def render_reset_and_save_buttons(reset_callback=None, image_to_save=None):
    """Render reset and save buttons in two columns"""
    col_btn1, col_btn2, col_spacer = st.columns([2, 2, 6])
    
    with col_btn1:
        if st.button("Reset to Original", use_container_width=True):
            # Reset processed_image ke original_image
            if st.session_state.original_image is not None:
                st.session_state.processed_image = st.session_state.original_image.copy()
            if reset_callback:
                reset_callback()
            st.rerun()
    
    with col_btn2:
        # Gunakan image_to_save jika ada, fallback ke processed_image
        img_to_save = image_to_save if image_to_save is not None else st.session_state.processed_image
        if img_to_save is not None:
            create_download_button(img_to_save)

