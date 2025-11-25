import streamlit as st
import time
from data.db_handler import DatabaseManager

def show_login_page():
    """Simple login page"""
    st.markdown("""
        <div style="text-align: center; padding: 3rem 0;">
            <h1 style="font-size: 4rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                🎭 Facial Emotion Recognition
            </h1>
            <p style="font-size: 1.5rem; color: #666; margin-top: 1rem;">
                AI-Powered Emotion Detection System
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div class="info-card" style="text-align: center;">
                <h2>👋 Welcome!</h2>
                <p>Please enter your name to get started</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input(
                "Your Name",
                placeholder="Enter your name...",
                help="Just so we know what to call you!"
            )
            
            email = st.text_input(
                "Email (Optional)",
                placeholder="your.email@example.com",
                help="We won't spam you, promise."
            )
            
            submit = st.form_submit_button("🚀 Start Detecting Emotions", use_container_width=True)
            
            if submit and username:
                # Need to make sure DB is ready
                if 'db_manager' not in st.session_state:
                     st.session_state.db_manager = DatabaseManager()

                # Create user if they don't exist
                uid = st.session_state.db_manager.create_user(username, email if email else None)
                
                if uid:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_id = uid
                    st.session_state.show_welcome = True
                    
                    # Update timestamp
                    st.session_state.db_manager.update_last_login(uid)
                    
                    st.success(f"✓ Welcome, {username}!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Oops, something went wrong. Try again?")
            elif submit:
                st.warning("Hey, we need a name first!")
