import streamlit as st
import os

# Import the optimized logic files we just worked on
from speech_to_text import transcribe_audio
from semantic_similarity import similarity
from feedback import generate_feedback
from audio_features import analyze_audio
from report_generator import create_report
from filler_detection import detect_fillers
from fluency import evaluate_fluency

# Page Layout Configuration
st.set_page_config(page_title="Voice-Based Concept Analyser", page_icon="🎤", layout="centered")

st.title("🎤 Voice-Based Concept Understanding Analyser")
st.write("Upload your audio response to analyze concept accuracy, fluency, and speech disfluencies.")

# 1. Target Reference Text Input
st.subheader("📋 Target Concept Definition")
reference_text = st.text_area(
    "Enter the target reference text or answer key to compare against:",
    value="hi, this is the test for my AI project"
)

# 2. Audio File Uploader
st.subheader("🎵 Upload Audio Response")
uploaded_file = st.file_uploader(
    "Upload an audio file",
    type=["wav", "mp3", "m4a", "ogg"]
)

if uploaded_file is not None:
    # Create an uploads folder to safely process the file locally
    os.makedirs("uploads", exist_ok=True)
    audio_path = os.path.join("uploads", uploaded_file.name)

    with open(audio_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ Audio uploaded successfully!")
    st.audio(uploaded_file)

    # Simple loading spinner to process calculations cleanly
    with st.spinner("Analyzing audio characteristics and transcribing text..."):
        
        # Run calculations using your teammate's backend functions
        transcript = transcribe_audio(audio_path)
        analysis = analyze_audio(audio_path)
        fillers = detect_fillers(transcript)
        
        # Run comparison scoring
        score = similarity(transcript, reference_text)
        feedback = generate_feedback(score)
        
        fluency_score, fluency_grade = evaluate_fluency(
            analysis["pause_ratio"],
            analysis["average_rms"],
            fillers["total_fillers"]
        )

    st.markdown("---")

    # Display Section 1: Transcripts & Similarity Metrics
    st.subheader("📝 Text Analysis & Understanding")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Your Spoken Transcript:**")
        st.info(transcript)
    with col2:
        st.markdown("**Target Reference Text:**")
        st.code(reference_text, wrap_lines=True)
        
    st.metric(label="Conceptual Similarity Score", value=f"{score * 100:.1f}%")
    st.markdown(f"**Evaluation Feedback:** {feedback}")

    st.markdown("---")

    # Display Section 2: Audio Characteristics & Fluency Layout
    st.subheader("📊 Speech Fluency Metrics")
    
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("Duration", f"{analysis['duration']}s")
    m_col2.metric("Pause Ratio", f"{analysis['pause_ratio'] * 100:.1f}%")
    m_col3.metric("Fluency Score", f"{fluency_score}/100")
    
    st.markdown(f"**Fluency Classification:** {fluency_grade}")
    
    # Automatically display the audio waveform plot
    if os.path.exists(analysis["waveform"]):
        st.image(analysis["waveform"], caption="Audio Amplitude Waveform Map", use_container_width=True)

    st.markdown("---")

    # Display Section 3: Filler Word Highlights
    st.subheader("🔀 Filler Word Breakdown")
    if fillers["total_fillers"] == 0:
        st.success("✨ Excellent! No standard filler words detected in your speech.")
    else:
        st.warning(f"Detected **{fillers['total_fillers']}** total filler words.")
        # Loop through and display counts for each filler word used
        f_details = [f"• **{word}**: {count} times" for word, count in fillers["details"].items() if count > 0]
        st.markdown("\n".join(f_details))

    st.markdown("---")

    # Display Section 4: PDF Document Generation and Exporter
    st.subheader("📥 Export Final Evaluation")
    try:
        # Create the report PDF using report_generator.py
        create_report(
            transcript, reference_text, score, feedback, 
            analysis, fluency_score, fluency_grade, fillers
        )
        
        if os.path.exists("report.pdf"):
            with open("report.pdf", "rb") as pdf_file:
                st.download_button(
                    label="Download Report as PDF",
                    data=pdf_file,
                    file_name="Voice_Concept_Analysis_Report.pdf",
                    mime="application/pdf"
                )
    except Exception as e:
        st.error(f"Could not generate PDF download bundle: {e}")