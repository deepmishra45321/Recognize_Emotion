import streamlit as st
from PIL import Image
from ui.components import show_page_header, show_emotion_card, create_emotion_bar_chart, create_emotion_pie_chart

def show_image_detection():
    """Page for uploading images"""
    show_page_header("📸 Image Emotion Detection", "Upload an image to detect facial emotions")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Upload Image")
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['jpg', 'jpeg', 'png'],
            help="Upload an image containing faces"
        )
        
        if uploaded_file is not None:
            # Show the image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            
            # The magic button
            if st.button("🔍 Detect Emotions", use_container_width=True):
                with st.spinner("🎭 Analyzing emotions..."):
                    # Get predictions
                    preds = st.session_state.predictor.predict_from_image(image)
                    
                    if preds:
                        # Save to DB so we can see stats later
                        emotions = [p['dominant_emotion'] for p in preds]
                        stats = st.session_state.predictor.get_emotion_statistics(preds)
                        
                        st.session_state.db_manager.save_detection_history(
                            st.session_state.user_id,
                            stats['total_faces'],
                            emotions,
                            stats['average_confidence']
                        )
                        
                        # Save to session state so it doesn't disappear on reload
                        st.session_state.predictions = preds
                        st.session_state.annotated_image = st.session_state.predictor.annotate_image(
                            image, preds
                        )
                        
                        st.success(f"✓ Found {len(preds)} face(s)!")
                    else:
                        st.warning("⚠ Couldn't find any faces. Maybe try a clearer photo?")
    
    with col2:
        if 'predictions' in st.session_state and st.session_state.predictions:
            st.markdown("### Detection Results")
            
            # Show the cool annotated image
            st.image(
                st.session_state.annotated_image,
                caption="Emotion Detection Results",
                use_container_width=True
            )
            
            # Details for each face
            for i, p in enumerate(st.session_state.predictions):
                # Using expander to keep it clean
                with st.expander(f"👤 Face {i+1}: {p['dominant_emotion']} ({p['confidence']:.1f}%)", expanded=True):
                    show_emotion_card(p['dominant_emotion'], p['confidence'])
                    
                    # Bar chart looks better here
                    st.plotly_chart(
                        create_emotion_bar_chart(p['all_emotions']),
                        use_container_width=True
                    )


def show_webcam_detection():
    """Page for webcam stuff"""
    show_page_header("📹 Live Webcam Detection", "Detect emotions in real-time from your webcam")
    
    # Help section because webcams are finicky
    with st.expander("⚠️ Camera Not Working? Click Here", expanded=False):
        st.markdown("""
            <div class="info-card">
                <h4>🔧 Troubleshooting</h4>
                <p>Webcams can be tricky in browsers. Here are some tips:</p>
                <ul>
                    <li><b>Permissions:</b> Did you click "Allow"?</li>
                    <li><b>HTTPS:</b> Some browsers block cameras on http://localhost</li>
                    <li><b>Other Apps:</b> Close Zoom/Teams!</li>
                    <li><b>Browser:</b> Chrome usually works best.</li>
                </ul>
                <p><b>Fallback:</b> Use the upload option below if nothing works.</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Instructions
    st.markdown("""
        <div class="info-card">
            <h3>📷 How to Use</h3>
            <ol>
                <li>Enable camera below</li>
                <li>Allow permissions</li>
                <li>Smile! (or frown)</li>
                <li>Click "Take Photo"</li>
                <li>Click "Analyze"</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📸 Camera Feed")
        
        # Toggle between webcam and upload (fallback)
        mode = st.radio(
            "Mode:",
            ["📹 Webcam", "📁 Upload"],
            help="Switch if webcam is broken"
        )
        
        if mode == "📹 Webcam":
            try:
                cam_img = st.camera_input("Take a photo")
                
                if cam_img is not None:
                    image = Image.open(cam_img)
                    
                    if st.button("🎭 Analyze Emotion", use_container_width=True, key="webcam_analyze"):
                        with st.spinner("🔍 Crunching numbers..."):
                            preds = st.session_state.predictor.predict_from_image(image)
                            
                            if preds:
                                # Save history
                                emotions = [p['dominant_emotion'] for p in preds]
                                stats = st.session_state.predictor.get_emotion_statistics(preds)
                                
                                st.session_state.db_manager.save_detection_history(
                                    st.session_state.user_id,
                                    stats['total_faces'],
                                    emotions,
                                    stats['average_confidence']
                                )
                                
                                st.session_state.webcam_predictions = preds
                                st.session_state.webcam_annotated = st.session_state.predictor.annotate_image(
                                    image, preds
                                )
                                
                                st.success(f"✓ Found {len(preds)} face(s)!")
                            else:
                                st.warning("⚠ No faces found. Try better lighting?")
                else:
                    st.info("👆 Waiting for photo...")
                    
            except Exception as e:
                st.error(f"Camera Error: {e}")
        
        else:  # Upload fallback
            st.markdown("#### 📁 Upload Selfie")
            uploaded = st.file_uploader("Choose photo", type=['jpg', 'png'], key="webcam_upload")
            
            if uploaded is not None:
                image = Image.open(uploaded)
                st.image(image, caption="Your Selfie", use_container_width=True)
                
                if st.button("🎭 Analyze", use_container_width=True, key="upload_analyze"):
                    with st.spinner("🔍 Analyzing..."):
                        preds = st.session_state.predictor.predict_from_image(image)
                        
                        if preds:
                            # Save history
                            emotions = [p['dominant_emotion'] for p in preds]
                            stats = st.session_state.predictor.get_emotion_statistics(preds)
                            
                            st.session_state.db_manager.save_detection_history(
                                st.session_state.user_id,
                                stats['total_faces'],
                                emotions,
                                stats['average_confidence']
                            )
                            
                            st.session_state.webcam_predictions = preds
                            st.session_state.webcam_annotated = st.session_state.predictor.annotate_image(
                                image, preds
                            )
                            
                            st.success(f"✓ Found {len(preds)} face(s)!")
                        else:
                            st.warning("⚠ No faces found.")
    
    with col2:
        if 'webcam_predictions' in st.session_state and st.session_state.webcam_predictions:
            st.markdown("### 🎯 Results")
            
            st.image(
                st.session_state.webcam_annotated,
                caption="Detected Emotions",
                use_container_width=True
            )
            
            for p in st.session_state.webcam_predictions:
                show_emotion_card(p['dominant_emotion'], p['confidence'])
                
                st.plotly_chart(
                    create_emotion_pie_chart(p['all_emotions']),
                    use_container_width=True
                )
        else:
            st.markdown("""
                <div class="info-card" style="text-align: center; padding: 3rem;">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">📸</div>
                    <h3>Waiting for input...</h3>
                    <p>Take a photo to see the magic happen!</p>
                </div>
            """, unsafe_allow_html=True)
