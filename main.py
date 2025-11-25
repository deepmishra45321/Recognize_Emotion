"""
Facial Emotion Recognition App
------------------------------
Main entry point.
Run this file to start the app: `streamlit run main.py`

By: Deepak Mishra
"""

import streamlit as st
import time
import sys
import os

# Fix path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# My custom stuff
from ui.styles import get_custom_css
from ui.components import show_welcome_animation
from core.emotion_detector import EmotionPredictor
from core.image_processor import ImagePreprocessor
from data.db_handler import DatabaseManager

# The pages
from ui.views.auth_view import show_login_page
from ui.views.detection_view import show_image_detection, show_webcam_detection
from ui.views.stats_view import show_statistics
from ui.views.about_view import show_about


# Config
st.set_page_config(
    page_title="Emotion Detector | AI Project",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)


def init_session():
    """Sets up all the session variables we need"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
        
    # Lazy load the heavy stuff
    if 'db_manager' not in st.session_state:
        st.session_state.db_manager = DatabaseManager()
    if 'predictor' not in st.session_state:
        with st.spinner("🔄 Waking up the AI..."):
            st.session_state.predictor = EmotionPredictor()
    if 'preprocessor' not in st.session_state:
        st.session_state.preprocessor = ImagePreprocessor()
        
    if 'show_welcome' not in st.session_state:
        st.session_state.show_welcome = True


def main():
    """The main loop"""
    init_session()
    
    # Make it look pretty
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    # Login check
    if not st.session_state.logged_in:
        show_login_page()
        return
    
    # Animation on first load
    if st.session_state.show_welcome:
        show_welcome_animation(st.session_state.username)
        st.session_state.show_welcome = False
        time.sleep(2)
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"""
            <div style="text-align: center; padding: 2rem 0;">
                <div style="font-size: 3rem;">👤</div>
                <h2>{st.session_state.username}</h2>
                <p style="opacity: 0.8;">Dashboard</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        page = st.radio(
            "Go to:",
            ["📸 Image Detection", "📹 Webcam Detection", "📊 Statistics", "ℹ️ About"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            # Reset everything
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.user_id = None
            st.session_state.show_welcome = True
            st.rerun()
    
    # Router
    if page == "📸 Image Detection":
        show_image_detection()
    elif page == "📹 Webcam Detection":
        show_webcam_detection()
    elif page == "📊 Statistics":
        show_statistics()
    elif page == "ℹ️ About":
        show_about()
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #666;">
            <p>🎭 Facial Emotion Recognition | <b>Deepak Mishra</b></p>
            <p style="font-size: 0.9rem; opacity: 0.8;">B.Tech AI & ML | 2025</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
