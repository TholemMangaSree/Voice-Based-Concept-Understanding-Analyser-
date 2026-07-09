import streamlit as st
import os

from speech_to_text import transcribe_audio
from semantic_similarity import similarity
from feedback import generate_feedback
from audio_features import analyze_audio
from report_generator import create_report
from filler_detection import detect_fillers
from fluency import evaluate_fluency

st.title("🎤 Voice-Based Concept Understanding Analyser")

uploaded_file = st.file_uploader(
    "Upload an audio file",
    type=["wav", "mp3", "m4a", "ogg"]
)

if uploaded_file is not None:

    # Create uploads folder
    os.makedirs("uploads", exist_ok=True)

    # Save uploaded file
    audio_path = os.path.join("uploads", uploaded_file.name)

    with open(audio_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ Audio uploaded successfully!")
    st.audio(uploaded_file)
    st.write("**Filename:**", uploaded_file.name)

    # Speech to Text
    st.subheader("📝 Transcribed Text")
    transcript = transcribe_audio(audio_path)
    st.write(transcript)
     
    # Reference Text
    reference_text = "hi,this is the test for my AI project"

    st.subheader("📖 Reference Text")
    st.write(reference_text)

    # Similarity Score
    score = similarity(transcript, reference_text)

    st.subheader("📊 Semantic Similarity Score")
    st.progress(score)
    st.write(f"Similarity:{score*100:.2f}%")

    # Feedback
    feedback = generate_feedback(score)

    st.subheader("💬 Feedback")
    st.success(feedback)

    # Audio Analysis
    analysis = analyze_audio(audio_path)

    st.subheader("🎵 Audio Analysis")

    st.write("**Duration:**", analysis["duration"], "seconds")
    st.write("**Average RMS:**", analysis["average_rms"])
    st.write("**Pause Ratio:**", analysis["pause_ratio"])
    st.subheader("📈 Waveform")
    st.image(analysis["waveform"], caption="Audio Waveform")
    
    # Filler Detection
    fillers = detect_fillers(transcript)
    
    # Fluency Evaluation
    fluency_score, fluency_grade = evaluate_fluency(
        analysis["pause_ratio"],
        analysis["average_rms"],
        fillers["total_fillers"]
    )

    # Filler Word Analysis
    st.subheader(" Filler Word Analysis")
    if fillers["total_fillers"] == 0:
        st.success("No filler words detected.Your speech is clear.")
    else:
        st.write(f"Total filler words:{fillers['total_fillers']}")
    st.write("**Total Filler Words:**", fillers["total_fillers"])

    for word, count in fillers["details"].items():
        if count > 0:
            st.write(f".{word}: {count}")

    # Speech Fluency Analysis
    st.subheader(" Speech Fluency Analysis")
    st.write("**Fluency Score:**", fluency_score, "/100")
    st.success(fluency_grade)
    
   

    # Create PDF report
    pdf_file = create_report(
        transcript,
        reference_text,
        score,
        feedback,
        analysis,
        fluency_score,
        fluency_grade,
        fillers
    )

    # Download button
    with open(pdf_file, "rb") as file:
        st.download_button(
            label="📄 Download PDF Report",
            data=file,
            file_name="Voice_Report.pdf",
            mime="application/pdf"
        )   