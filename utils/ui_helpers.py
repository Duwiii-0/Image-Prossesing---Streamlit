import streamlit as st
import io
from PIL import Image

def load_css():
    """Load custom CSS from style.css file"""
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            
        # Inject custom transitions
        st.markdown("""
        <style>
            /* Custom Transitions */
            .stApp * {
                transition: background-color 0.15s ease-in-out, border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
            }
        </style>
        """, unsafe_allow_html=True)
    except:
        pass

def render_section_header(title, description=None, icon=None):
    """Render a styled section header with optional icon and description"""
    icon_html = f'<div class="section-icon">{icon}</div>' if icon else ''
    
    html = f"""
    <div class="section-header">
        {icon_html}
        <div>
            <h3 style="margin-bottom: 0;">{title}</h3>
            {f'<p style="margin-bottom: 0; margin-top: 0.25rem;">{description}</p>' if description else ''}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_image_preview(image_left, image_right, title_left="Original Reference", title_right="Modified Output"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="image-preview-card">
            <div class="image-preview-badge">{title_left}</div>
        </div>
        """, unsafe_allow_html=True)
        st.image(image_left, use_container_width=True)
    with col2:
        st.markdown(f"""
        <div class="image-preview-card">
            <div class="image-preview-badge" style="background: rgba(99, 102, 241, 0.8); border-color: rgba(99, 102, 241, 1);">{title_right}</div>
        </div>
        """, unsafe_allow_html=True)
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
        width='stretch',
        type="primary"
    )

def render_reset_and_save_buttons(reset_callback=None, image_to_save=None):
    """Render reset and save buttons in two columns"""
    col_btn1, col_btn2, col_spacer = st.columns([1.2, 2, 5.8])
    
    with col_btn1:
        if st.button("Reset", width='stretch'):
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

