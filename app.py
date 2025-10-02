import streamlit as st
import time
from agents import intake_agent, vision_agent, analysis_agent, orchestrator
import os

# Page config for beauty
st.set_page_config(
    page_title="Urban Air Quality Monitor",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
    <style>
    .main-header {font-size: 3rem; color: #10B981; text-align: center; margin-bottom: 2rem;}
    .feature-card {background: linear-gradient(135deg, #10B981, #059669); color: white; padding: 1.5rem; border-radius: 10px; text-align: center;}
    .loading {text-align: center; font-size: 1.2rem; color: #10B981;}
    .status-bar {background: #E5E7EB; padding: 0.5rem; border-radius: 5px; margin: 0.5rem 0;}
    .alert {background: #FEF3C7; padding: 1rem; border-radius: 5px; border-left: 4px solid #F59E0B;}
    </style>
""", unsafe_allow_html=True)

# Sidebar for API key (secure input)
st.sidebar.title("🔧 Settings")
groq_key = st.sidebar.text_input("Groq API Key", type="password", value=os.getenv("GROQ_API_KEY", ""))
if not groq_key:
    st.sidebar.warning("Enter your Groq API key to proceed.")
    st.stop()

# Main header
st.markdown('<h1 class="main-header">🌿 Real-Time Urban Air Quality Monitor</h1>', unsafe_allow_html=True)
st.markdown("Monitor pollution, forecast impacts, and optimize resources with AI agents powered by Groq.")

# Tabs for features (beautiful navigation)
tab1, tab2, tab3 = st.tabs(["📝 Text Query", "🎤 Voice Report", "🖼️ Image Upload"])

def process_input(input_data, modality):
    """Unified processing with loading."""
    with st.spinner("🤖 Agents activating... Processing input."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Intake (10%)
        status_text.markdown('<div class="status-bar">Intake Agent: Transcribing/Analyzing...</div>', unsafe_allow_html=True)
        processed_input = intake_agent(input_data, modality)
        progress_bar.progress(10)
        time.sleep(0.5)  # Simulate latency
        
        vision_desc = ""
        if modality == "image":
            # Step 2: Vision (30%)
            status_text.markdown('<div class="status-bar">Vision Agent: Extracting visual data...</div>', unsafe_allow_html=True)
            vision_desc = vision_agent(input_data)
            progress_bar.progress(40)
            time.sleep(0.5)
        elif modality == "text" or modality == "voice":
            progress_bar.progress(10)  # Skip vision for non-image
        
        # Step 3: Analysis (60%)
        status_text.markdown('<div class="status-bar">Analysis Agent: Forecasting impacts with MCP...</div>', unsafe_allow_html=True)
        analysis = analysis_agent(processed_input)
        progress_bar.progress(70)
        time.sleep(0.5)
        
        # Step 4: Orchestrate (100%)
        status_text.markdown('<div class="status-bar">Orchestrator: Generating recommendations...</div>', unsafe_allow_html=True)
        final_response = orchestrator(processed_input, vision_desc, analysis)
        progress_bar.progress(100)
        time.sleep(0.5)
        
        status_text.empty()
        return final_response

# Tab 1: Text Query
with tab1:
    st.markdown('<div class="feature-card">Enter a text description of air quality concerns.</div>', unsafe_allow_html=True)
    text_input = st.text_area("Describe the issue (e.g., 'Heavy smog in downtown today')", height=100)
    if st.button("🚀 Analyze Text", type="primary", use_container_width=True):
        if text_input:
            with st.spinner("🌫️ Analyzing..."):
                result = process_input(text_input, "text")
            st.success("✅ Analysis Complete!")
            st.markdown(f"### 🌿 Recommendations\n{result}")
            if "high pollution" in result.lower():
                st.markdown('<div class="alert">⚠️ Alert: High pollution detected! Reduce outdoor activities.</div>', unsafe_allow_html=True)

# Tab 2: Voice Report
with tab2:
    st.markdown('<div class="feature-card">Record a voice report on observed pollution.</div>', unsafe_allow_html=True)
    audio_input = st.audio_input("Record your voice report", key="voice")
    if st.button("🎙️ Transcribe & Analyze", type="primary", use_container_width=True) and audio_input:
        # Save temp file
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_input.getvalue())
        with st.spinner("🔊 Listening..."):
            result = process_input("temp_audio.wav", "voice")
        os.remove("temp_audio.wav")  # Cleanup
        st.success("✅ Voice Analysis Complete!")
        st.markdown(f"### 🌿 Recommendations\n{result}")

# Tab 3: Image Upload
with tab3:
    st.markdown('<div class="feature-card">Upload a photo of the environment (e.g., city skyline with smog).</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if st.button("👁️ Analyze Image", type="primary", use_container_width=True) and uploaded_file:
        # Save temp file
        with open("temp_image.jpg", "wb") as f:
            f.write(uploaded_file.getvalue())
        with st.spinner("📸 Scanning..."):
            result = process_input("temp_image.jpg", "image")
        os.remove("temp_image.jpg")  # Cleanup
        st.success("✅ Image Analysis Complete!")
        st.markdown(f"### 🌿 Recommendations\n{result}")

# Footer
st.markdown("---")