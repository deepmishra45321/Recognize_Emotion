"""
Reusable UI Components for Streamlit
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime


def show_welcome_animation(username):
    """
    Display animated welcome message
    
    Args:
        username: Name of logged-in user
    """
    st.markdown(f"""
        <div class="welcome-container">
            <div class="welcome-title">👋 Welcome, {username}!</div>
            <div class="welcome-subtitle">🎭 Ready to Detect Emotions</div>
            <p style="margin-top: 1rem; font-size: 1.1rem; opacity: 0.8;">
                Let's analyze facial expressions and uncover emotions together
            </p>
        </div>
    """, unsafe_allow_html=True)


def show_page_header(title, subtitle="", icon="🎭"):
    """
    Display page header with icon
    
    Args:
        title: Page title
        subtitle: Optional subtitle
        icon: Emoji icon
    """
    st.markdown(f"""
        <div class="app-header">
            <h1>{icon} {title}</h1>
            {f'<p style="font-size: 1.2rem; color: #666;">{subtitle}</p>' if subtitle else ''}
        </div>
    """, unsafe_allow_html=True)


def show_info_card(title, content, icon="ℹ️"):
    """
    Display information card
    
    Args:
        title: Card title
        content: Card content
        icon: Emoji icon
    """
    st.markdown(f"""
        <div class="info-card">
            <h3>{icon} {title}</h3>
            <p>{content}</p>
        </div>
    """, unsafe_allow_html=True)


def show_emotion_card(emotion, confidence):
    """
    Display emotion result card
    
    Args:
        emotion: Detected emotion
        confidence: Confidence score (0-100)
    """
    # Emotion emojis
    emotion_emojis = {
        'Happy': '😊',
        'Sad': '😢',
        'Angry': '😠',
        'Surprise': '😲',
        'Fear': '😨',
        'Disgust': '🤢',
        'Neutral': '😐'
    }
    
    emoji = emotion_emojis.get(emotion, '😐')
    
    st.markdown(f"""
        <div class="emotion-card">
            <div style="font-size: 4rem; margin-bottom: 1rem;">{emoji}</div>
            <div class="emotion-label">{emotion}</div>
            <div class="confidence-score">Confidence: {confidence:.1f}%</div>
        </div>
    """, unsafe_allow_html=True)


def show_metric_card(label, value, icon="📊"):
    """
    Display metric card
    
    Args:
        label: Metric label
        value: Metric value
        icon: Emoji icon
    """
    st.markdown(f"""
        <div class="metric-container">
            <div style="font-size: 2rem;">{icon}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
    """, unsafe_allow_html=True)


def create_emotion_bar_chart(emotions_dict):
    """
    Create interactive bar chart for emotion probabilities
    
    Args:
        emotions_dict: Dictionary with emotion: probability pairs
        
    Returns:
        Plotly figure
    """
    # Sort emotions by probability
    sorted_emotions = dict(sorted(emotions_dict.items(), key=lambda x: x[1], reverse=True))
    
    # Define colors for each emotion
    color_map = {
        'Happy': '#fda085',
        'Sad': '#3f2b96',
        'Angry': '#ee5a6f',
        'Surprise': '#fddb92',
        'Fear': '#d299c2',
        'Disgust': '#c471f5',
        'Neutral': '#9fa4a8'
    }
    
    emotions = list(sorted_emotions.keys())
    probabilities = list(sorted_emotions.values())
    colors = [color_map.get(e, '#667eea') for e in emotions]
    
    fig = go.Figure(data=[
        go.Bar(
            x=emotions,
            y=probabilities,
            marker=dict(
                color=colors,
                line=dict(color='white', width=2)
            ),
            text=[f'{p:.1f}%' for p in probabilities],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Confidence: %{y:.2f}%<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title={
            'text': '🎭 Emotion Analysis',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Outfit'}
        },
        xaxis_title='Emotions',
        yaxis_title='Confidence (%)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=12),
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
    )
    
    return fig


def create_emotion_pie_chart(emotions_dict):
    """
    Create interactive pie chart for emotion distribution
    
    Args:
        emotions_dict: Dictionary with emotion: probability pairs
        
    Returns:
        Plotly figure
    """
    # Filter out very low probabilities
    filtered_emotions = {k: v for k, v in emotions_dict.items() if v > 1.0}
    
    if not filtered_emotions:
        filtered_emotions = emotions_dict
    
    color_map = {
        'Happy': '#fda085',
        'Sad': '#3f2b96',
        'Angry': '#ee5a6f',
        'Surprise': '#fddb92',
        'Fear': '#d299c2',
        'Disgust': '#c471f5',
        'Neutral': '#9fa4a8'
    }
    
    colors = [color_map.get(e, '#667eea') for e in filtered_emotions.keys()]
    
    fig = go.Figure(data=[
        go.Pie(
            labels=list(filtered_emotions.keys()),
            values=list(filtered_emotions.values()),
            marker=dict(colors=colors, line=dict(color='white', width=2)),
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>%{value:.2f}%<extra></extra>',
            hole=0.4
        )
    ])
    
    fig.update_layout(
        title={
            'text': '🎯 Emotion Distribution',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Outfit'}
        },
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=12),
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
        showlegend=True
    )
    
    return fig


def create_history_chart(history_data):
    """
    Create line chart for detection history
    
    Args:
        history_data: List of history records
        
    Returns:
        Plotly figure
    """
    if not history_data:
        return None
    
    times = [datetime.fromisoformat(h['time']) if isinstance(h['time'], str) else h['time'] 
             for h in history_data]
    confidences = [h['confidence'] for h in history_data]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=times,
        y=confidences,
        mode='lines+markers',
        name='Confidence',
        line=dict(color='#667eea', width=3),
        marker=dict(size=8, color='#764ba2'),
        hovertemplate='<b>Time:</b> %{x}<br><b>Confidence:</b> %{y:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': '📈 Detection History',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Outfit'}
        },
        xaxis_title='Time',
        yaxis_title='Confidence (%)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=12),
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', range=[0, 100])
    )
    
    return fig


def show_developer_card():
    """
    Display developer information card
    """
    import base64
    import os
    
    # Load and encode profile image
    profile_image_path = "assets/deepak_profile.jpg"
    if os.path.exists(profile_image_path):
        with open(profile_image_path, "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode()
            profile_img_html = f'<img src="data:image/jpeg;base64,{img_data}" style="width: 200px; height: 200px; border-radius: 50%; object-fit: cover; border: 5px solid rgba(255,255,255,0.3); box-shadow: 0 10px 30px rgba(0,0,0,0.3); margin-bottom: 1rem;" />'
    else:
        # Fallback to emoji if image not found
        profile_img_html = '<div style="font-size: 4rem; margin-bottom: 1rem;">👨‍💻</div>'
    
    st.markdown(f"""
        <div class="developer-card">
            <div style="text-align: center;">
                {profile_img_html}
                <div class="developer-name">Deepak Mishra</div>
                <div class="developer-title">B.Tech in AI & ML</div>
                <p style="font-size: 1rem; opacity: 0.9; margin: 1rem 0;">
                    Passionate about building intelligent systems that understand human emotions
                    and create meaningful interactions through AI and Deep Learning.
                </p>
                
                <div style="margin-top: 2rem;">
                    <h3 style="margin-bottom: 1rem;">🚀 Project Highlights</h3>
                    <ul style="text-align: left; list-style: none; padding: 0;">
                        <li style="margin: 0.5rem 0;">✨ CNN-based facial emotion recognition</li>
                        <li style="margin: 0.5rem 0;">🎯 Real-time webcam emotion detection</li>
                        <li style="margin: 0.5rem 0;">📊 Advanced emotion analytics & visualization</li>
                        <li style="margin: 0.5rem 0;">💾 User history & statistics tracking</li>
                        <li style="margin: 0.5rem 0;">🎨 Modern, interactive UI with Streamlit</li>
                    </ul>
                </div>
                
                <div style="margin-top: 2rem;">
                    <h3 style="margin-bottom: 1rem;">📬 Connect With Me</h3>
                    <div class="social-links" style="justify-content: center;">
                        <a href="https://www.linkedin.com/in/deepak-mishra-a86623287" target="_blank" class="social-link">
                            💼 LinkedIn
                        </a>
                        <a href="https://github.com/deepmishra45321" target="_blank" class="social-link">
                            💻 GitHub
                        </a>
                        <a href="mailto:deepak.mishra@example.com" class="social-link">
                            📧 Email
                        </a>
                    </div>
                </div>
                
                <div style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.3);">
                    <p style="font-size: 0.9rem; opacity: 0.8;">
                        🎓 Aspiring AI/ML Engineer | 🔬 Research Enthusiast | 🌟 Innovation Driven
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def show_loading_spinner(text="Processing..."):
    """
    Display loading spinner
    
    Args:
        text: Loading text
    """
    st.markdown(f"""
        <div style="text-align: center; padding: 2rem;">
            <div class="loading" style="font-size: 3rem;">⚙️</div>
            <p style="font-size: 1.2rem; color: #667eea; margin-top: 1rem;">{text}</p>
        </div>
    """, unsafe_allow_html=True)


def show_stats_overview(total_detections, most_common_emotion, avg_confidence):
    """
    Display statistics overview
    
    Args:
        total_detections: Total number of detections
        most_common_emotion: Most frequently detected emotion
        avg_confidence: Average confidence score
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        show_metric_card("Total Detections", total_detections, "🔍")
    
    with col2:
        show_metric_card("Most Common", most_common_emotion, "🎭")
    
    with col3:
        show_metric_card("Avg Confidence", f"{avg_confidence:.1f}%", "📊")
