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

def create_download_button(image, filename="edited_image", button_text="Save Edited Image"):
    """Create download button for image with format selection"""
    col1, col2 = st.columns([1, 1])
    
    with col1:
        format_choice = st.selectbox(
            "Format",
            ["PNG", "JPEG", "BMP"],
            key="save_format"
        )
    
    with col2:
        custom_filename = st.text_input(
            "Filename",
            value=filename,
            key="save_filename"
        )
    
    # Prepare image based on format
    result_pil = Image.fromarray(image)
    
    if format_choice == "PNG":
        buf = io.BytesIO()
        result_pil.save(buf, format="PNG")
        byte_im = buf.getvalue()
        mime = "image/png"
        ext = "png"
    
    elif format_choice == "JPEG":
        if result_pil.mode == 'RGBA':
            result_pil = result_pil.convert('RGB')
        buf = io.BytesIO()
        result_pil.save(buf, format="JPEG", quality=95)
        byte_im = buf.getvalue()
        mime = "image/jpeg"
        ext = "jpg"
    
    else:  # BMP
        buf = io.BytesIO()
        result_pil.save(buf, format="BMP")
        byte_im = buf.getvalue()
        mime = "image/bmp"
        ext = "bmp"
    
    # Bersihkan nama file dari ekstensi
    clean_filename = custom_filename.rsplit('.', 1)[0] if '.' in custom_filename else custom_filename
    full_filename = f"{clean_filename}.{ext}"
    
    st.download_button(
        label=button_text,
        data=byte_im,
        file_name=full_filename,
        mime=mime,
        type="primary",
        use_container_width=True
    )

def render_reset_and_save_buttons(reset_callback=None, image_to_save=None):
    """Render reset and save buttons in two columns"""
    
    # Baris untuk Reset dan Tombol Save
    col_reset, col_save = st.columns([1, 3])
    
    with col_reset:
        if st.button("Reset", use_container_width=True):
            if st.session_state.original_image is not None:
                st.session_state.processed_image = st.session_state.original_image.copy()
            if reset_callback:
                reset_callback()
            st.rerun()
    
    with col_save:
        img_to_save = image_to_save if image_to_save is not None else st.session_state.processed_image
        if img_to_save is not None:
            col_fmt, col_name, col_btn = st.columns([1, 2, 1.2])
            
            with col_fmt:
                format_choice = st.selectbox(
                    "Format",
                    ["PNG", "JPEG", "BMP"],
                    key="save_format",
                    label_visibility="collapsed"
                )
            
            with col_name:
                custom_filename = st.text_input(
                    "Filename",
                    value="edited_image",
                    key="save_filename",
                    label_visibility="collapsed",
                    placeholder="filename"
                )
            
            with col_btn:
                result_pil = Image.fromarray(img_to_save)
                
                if format_choice == "PNG":
                    buf = io.BytesIO()
                    result_pil.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    mime = "image/png"
                    ext = "png"
                elif format_choice == "JPEG":
                    if result_pil.mode == 'RGBA':
                        result_pil = result_pil.convert('RGB')
                    buf = io.BytesIO()
                    result_pil.save(buf, format="JPEG", quality=95)
                    byte_im = buf.getvalue()
                    mime = "image/jpeg"
                    ext = "jpg"
                else:
                    buf = io.BytesIO()
                    result_pil.save(buf, format="BMP")
                    byte_im = buf.getvalue()
                    mime = "image/bmp"
                    ext = "bmp"
                
                clean_filename = custom_filename.rsplit('.', 1)[0] if '.' in custom_filename else custom_filename
                full_filename = f"{clean_filename}.{ext}"
                
                st.download_button(
                    label="Save",
                    data=byte_im,
                    file_name=full_filename,
                    mime=mime,
                    type="primary",
                    use_container_width=True
                )

