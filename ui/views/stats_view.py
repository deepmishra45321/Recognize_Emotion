import streamlit as st
from ui.components import show_page_header, show_stats_overview, create_emotion_pie_chart, create_history_chart

def show_statistics():
    """Shows all the cool charts and data"""
    show_page_header("📊 Your Statistics", "See how you've been feeling lately")
    
    # Grab data from DB
    total = st.session_state.db_manager.get_total_detections(st.session_state.user_id)
    stats = st.session_state.db_manager.get_emotion_statistics(st.session_state.user_id)
    history = st.session_state.db_manager.get_user_history(st.session_state.user_id, limit=20)
    
    # Calculate some quick numbers
    if stats:
        # Find the most frequent emotion
        top_emo = max(stats.items(), key=lambda x: x[1]['count'])[0]
        
        # Calculate average confidence
        if history:
            avg_conf = sum(h['confidence'] for h in history) / len(history)
        else:
            avg_conf = 0
    else:
        top_emo = "N/A"
        avg_conf = 0
    
    show_stats_overview(total, top_emo, avg_conf)
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        if stats:
            st.markdown("### 🎭 Emotion Mix")
            counts = {emo: data['count'] for emo, data in stats.items()}
            
            # Pie chart is best for this
            fig = create_emotion_pie_chart(counts)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data yet. Go detect some emotions!")
    
    with col2:
        if history:
            st.markdown("### 📈 Confidence Over Time")
            fig = create_history_chart(history)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Waiting for data...")
    
    # List of recent scans
    if history:
        st.markdown("### 🕐 Recent Activity")
        
        for h in history[:5]:
            with st.expander(f"🎯 {h['time']} - {h['num_faces']} face(s)"):
                st.write(f"**Emotions:** {', '.join(h['emotions'])}")
                st.write(f"**Confidence:** {h['confidence']:.1f}%")
