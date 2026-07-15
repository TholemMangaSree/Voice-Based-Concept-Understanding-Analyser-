import whisper
import os
import streamlit as st

# Cache the model so it only loads ONCE into your computer's memory
@st.cache_resource
def load_whisper_model():
    print("Loading Whisper model into memory...")
    return whisper.load_model("base")

model = load_whisper_model()

def transcribe_audio(audio_path):
    if not os.path.exists(audio_path):
        return f"❌ Error: The file '{audio_path}' could not be found."
        
    supported_extensions = ('.mp3', '.wav', '.ogg', '.m4a', '.flac')
    if not audio_path.lower().endswith(supported_extensions):
        return "❌ Error: Unsupported audio format."

    try:
        # Includes the custom prompt to ensure it catches filler words like "um" and "uh"
        result = model.transcribe(
            audio_path, 
            fp16=False, 
            initial_prompt="Um, uh, well, you know, like, hmm, ah, so I am speaking."
        )
        return result["text"].strip()
    except Exception as e:
        return f"❌ Error during transcription: {str(e)}"