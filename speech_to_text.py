import whisper
import os

print("Loading Whisper model...")
model = whisper.load_model("base")

def transcribe_audio(audio_path):
    """
    Transcribes an audio file to text with error handling.
    Returns the transcript string if successful, or an error message if it fails.
    """
    # 1. Error Handling: Check if the file actually exists
    if not os.path.exists(audio_path):
        return f"❌ Error: The file '{audio_path}' could not be found."
        
    # 2. Pre-processing check: Ensure it's a supported audio format
    supported_extensions = ('.mp3', '.wav', '.ogg', '.m4a', '.flac')
    if not audio_path.lower().endswith(supported_extensions):
        return "❌ Error: Unsupported audio format. Please use MP3, WAV, OGG, M4A, or FLAC."

    # 3. Safe Execution: Wrap the transcription in a try-except block
    try:
        print(f"Processing audio safely: {os.path.basename(audio_path)}...")
       # We add an initial prompt containing filler words to force Whisper to transcribe them
       result = model.transcribe(
           audio_path, 
           fp16=False, 
           initial_prompt="Um, uh, well, you know, like, hmm, ah, so I am speaking."
       )
       return result["text"].strip()
    except Exception as e:
        return f"❌ Error during transcription: {str(e)}"