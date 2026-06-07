import streamlit as st
import io
from PIL import Image

def load_css():
    """Load custom CSS from style.css file and inject Tailwind CSS"""
    # 1. Jalankan pembacaan file css bawaan yang lama
    try:
        # Inject Tailwind CSS Play CDN
        st.markdown('<script src="https://cdn.tailwindcss.com"></script>', unsafe_allow_html=True)
        
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            
        # Inject custom transitions
        st.markdown("""
        <style>
            /* Custom Transitions */
            .stApp * {
                transition: background-color 0.15s ease-in-out, border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
            }
            
            /* Ensure Tailwind classes don't conflict with Streamlit padding where not wanted */
            .tw-container {
                all: initial;
                font-family: 'Inter', sans-serif;
            }
        </style>
        """, unsafe_allow_html=True)
    except:
        pass

    # 2. INJECT CSS DISINI
    st.markdown("""
    <style>
    /* 1. Hancurkan atribut width angka (width="436") secara paksa */
    .e1y9jy7j2, .st-emotion-cache-p75nl5 {
        width: 100% !important;
        min-width: 100% !important; /* Memaksa mengabaikan properti width angka */
        max-width: 100% !important;
        display: flex !important;
        justify-content: center !important; /* Dorong isinya ke tengah */
        align-items: center !important;
        flex-grow: 1 !important;
    }

    /* 2. Pastikan container pembungkus luarnya juga ikut melebar penuh */
    div[data-testid="column"]:nth-child(1) .element-container,
    div[data-testid="column"]:nth-child(1) [data-testid="stElementContainer"] {
        width: 100% !important;
        min-width: 100% !important;
        display: flex !important;
        justify-content: center !important;
    }

    /* 3. Paksa gambar (tag <img>) yang ada di dalam class itu berada di center */
    .e1y9jy7j2 img, .st-emotion-cache-p75nl5 img {
        display: block !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    </style>
    """, unsafe_allow_html=True)

def render_tailwind_card(title, content, icon=""):
    """Example of a custom component using Tailwind CSS classes - Minimalist Version"""
    st.markdown(f"""
    <div class="p-5 max-w-sm mx-auto bg-slate-900 rounded border border-slate-800 hover:border-blue-600 transition-all duration-200">
      <div>
        <div class="text-sm font-bold uppercase tracking-wider text-slate-500 mb-1">{title}</div>
        <p class="text-slate-300 text-sm leading-relaxed">{content}</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

def render_section_header(title, description=None, icon=None):
    """Render a styled section header with optional description (No Emoji)"""
    html = f"""
    <div style="margin-bottom: 1.5rem; padding-bottom: 0.5rem; border-bottom: 1px solid #23272E;">
        <h3 style="margin-bottom: 0.25rem; font-weight: 600; color: #F8FAFC;">{title}</h3>
        {f'<p style="margin-bottom: 0; color: #64748B; font-size: 0.85rem;">{description}</p>' if description else ''}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_image_preview(image_left, image_right, title_left="REFERENCE", title_right="OUTPUT"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="image-preview-card">
            <div class="image-preview-badge">{title_left}</div>
        """, unsafe_allow_html=True)
        st.image(image_left, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="image-preview-card">
            <div class="image-preview-badge" style="color: #0071E3;">{title_right}</div>
        """, unsafe_allow_html=True)
        st.image(image_right, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

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

