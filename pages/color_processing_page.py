import streamlit as st
from utils.state_manager import reset_color_processing_state

def reset_color_processing():
    reset_color_processing_state()
    if 'reset_counter' not in st.session_state:
        st.session_state.reset_counter = 0
    st.session_state.reset_counter += 1
    st.rerun()

def render_color_processing_page():
    if 'reset_counter' not in st.session_state:
        st.session_state.reset_counter = 0
    
    if 'color_processing_state' not in st.session_state:
        st.session_state.color_processing_state = {
            'grayscale': False,
            'hue_shift': 0,
            'saturation_scale': 1.0,
            'value_scale': 1.0,
            'invert': False,
            'sepia_intensity': 0.0,
            'posterize_levels': 8,
            'red_shift': 0,
            'green_shift': 0,
            'blue_shift': 0,
        }
    
    tab1, tab2, tab3, tab4 = st.tabs(["Basic", "HSV", "FX", "Balance"])
    
    # ==================== TAB 1: BASIC ====================
    with tab1:
        def on_grayscale_change():
            st.session_state.color_processing_state['grayscale'] = not st.session_state.color_processing_state['grayscale']
        
        st.button(
            "Convert to Grayscale",
            key=f"btn_grayscale_{st.session_state.reset_counter}",
            on_click=on_grayscale_change,
            use_container_width=True
        )
        
        if st.session_state.color_processing_state.get('grayscale', False):
            st.success("✓ Grayscale active")
        else:
            st.info("Click to convert to grayscale")
    
    # ==================== TAB 2: HSV ====================
    with tab2:
        def on_hue_change():
            st.session_state.color_processing_state['hue_shift'] = st.session_state[f"hue_slider_{st.session_state.reset_counter}"]
        
        st.slider(
            "Hue", -180, 180,
            value=st.session_state.color_processing_state.get('hue_shift', 0),
            key=f"hue_slider_{st.session_state.reset_counter}",
            on_change=on_hue_change
        )
        
        def on_saturation_change():
            st.session_state.color_processing_state['saturation_scale'] = st.session_state[f"saturation_slider_{st.session_state.reset_counter}"]
        
        st.slider(
            "Saturation", 0.0, 2.0, step=0.1,
            value=st.session_state.color_processing_state.get('saturation_scale', 1.0),
            key=f"saturation_slider_{st.session_state.reset_counter}",
            on_change=on_saturation_change
        )
        
        def on_value_change():
            st.session_state.color_processing_state['value_scale'] = st.session_state[f"value_slider_{st.session_state.reset_counter}"]
        
        st.slider(
            "Value", 0.0, 2.0, step=0.1,
            value=st.session_state.color_processing_state.get('value_scale', 1.0),
            key=f"value_slider_{st.session_state.reset_counter}",
            on_change=on_value_change
        )
    
    # ==================== TAB 3: FX ====================
    with tab3:
        def on_invert_change():
            st.session_state.color_processing_state['invert'] = not st.session_state.color_processing_state['invert']
        
        st.button(
            "Invert Colors",
            key=f"btn_invert_{st.session_state.reset_counter}",
            on_click=on_invert_change,
            use_container_width=True
        )
        
        if st.session_state.color_processing_state.get('invert', False):
            st.success("✓ Invert active")
        else:
            st.info("Click to invert colors")
        
        def on_sepia_change():
            st.session_state.color_processing_state['sepia_intensity'] = st.session_state[f"sepia_slider_{st.session_state.reset_counter}"]
        
        st.slider(
            "Sepia", 0.0, 1.0, step=0.1,
            value=st.session_state.color_processing_state.get('sepia_intensity', 0.0),
            key=f"sepia_slider_{st.session_state.reset_counter}",
            on_change=on_sepia_change
        )
        
        def on_posterize_change():
            st.session_state.color_processing_state['posterize_levels'] = st.session_state[f"posterize_slider_{st.session_state.reset_counter}"]
        
        st.slider(
            "Posterize Levels", 2, 8,
            value=st.session_state.color_processing_state.get('posterize_levels', 8),
            key=f"posterize_slider_{st.session_state.reset_counter}",
            on_change=on_posterize_change
        )
    
    # ==================== TAB 4: COLOR BALANCE ====================
    with tab4:
        def on_red_change():
            st.session_state.color_processing_state['red_shift'] = st.session_state[f"red_slider_{st.session_state.reset_counter}"]
        
        st.slider(
            "Red", -100, 100,
            value=st.session_state.color_processing_state.get('red_shift', 0),
            key=f"red_slider_{st.session_state.reset_counter}",
            on_change=on_red_change
        )
        
        def on_green_change():
            st.session_state.color_processing_state['green_shift'] = st.session_state[f"green_slider_{st.session_state.reset_counter}"]
        
        st.slider(
            "Green", -100, 100,
            value=st.session_state.color_processing_state.get('green_shift', 0),
            key=f"green_slider_{st.session_state.reset_counter}",
            on_change=on_green_change
        )
        
        def on_blue_change():
            st.session_state.color_processing_state['blue_shift'] = st.session_state[f"blue_slider_{st.session_state.reset_counter}"]
        
        st.slider(
            "Blue", -100, 100,
            value=st.session_state.color_processing_state.get('blue_shift', 0),
            key=f"blue_slider_{st.session_state.reset_counter}",
            on_change=on_blue_change
        )

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("Reset Color", use_container_width=True):
        reset_color_processing()