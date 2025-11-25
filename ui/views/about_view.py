import streamlit as st
from ui.components import show_page_header, show_developer_card

def show_about():
    """About page"""
    show_page_header("ℹ️ About This Project", "A little bit about me and the code")
    
    # Me!
    show_developer_card()
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="stats-card">
                <h3>🔬 Tech Stack</h3>
                <ul style="list-style: none; padding: 0;">
                    <li style="padding: 0.5rem 0;">🐍 <b>Python</b> - Because it's awesome</li>
                    <li style="padding: 0.5rem 0;">🧠 <b>TensorFlow</b> - For the heavy lifting</li>
                    <li style="padding: 0.5rem 0;">👁️ <b>OpenCV</b> - To see you better</li>
                    <li style="padding: 0.5rem 0;">🎨 <b>Streamlit</b> - For this UI</li>
                    <li style="padding: 0.5rem 0;">📊 <b>Plotly</b> - Pretty charts</li>
                    <li style="padding: 0.5rem 0;">💾 <b>SQLite</b> - Keeping track of things</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="stats-card">
                <h3>✨ What it does</h3>
                <ul style="list-style: none; padding: 0;">
                    <li style="padding: 0.5rem 0;">📸 <b>Images</b> - Upload and analyze</li>
                    <li style="padding: 0.5rem 0;">📹 <b>Webcam</b> - Real-time magic</li>
                    <li style="padding: 0.5rem 0;">🎯 <b>7 Emotions</b> - Happy, Sad, Angry, etc.</li>
                    <li style="padding: 0.5rem 0;">📊 <b>Stats</b> - See your history</li>
                    <li style="padding: 0.5rem 0;">🎨 <b>UI</b> - Dark mode & glassmorphism</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    # CNN Info
    st.markdown("---")
    st.markdown("""
        <div class="info-card">
            <h3>🧠 How it works (The nerdy stuff)</h3>
            <p>
                I built a <b>Convolutional Neural Network (CNN)</b> that looks at your face and guesses how you're feeling.
                It pays attention to:
            </p>
            <ul>
                <li><b>Eyes:</b> Are they wide open? (Surprise!)</li>
                <li><b>Mouth:</b> Is it curved up or down? (Happy/Sad)</li>
                <li><b>Eyebrows:</b> Are they furrowed? (Angry)</li>
            </ul>
            <p>
                I used <b>batch normalization</b> and <b>dropout</b> to make sure it doesn't just memorize the training data.
                It's not perfect, but it tries its best!
            </p>
        </div>
    """, unsafe_allow_html=True)
