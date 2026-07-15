# transcribe.py
import whisper
import time

print("Loading Whisper model (this might take a minute)...")
# Using the 'base' model for a good balance of speed and accurate text
model = whisper.load_model("base")

# Pointing exactly to your audio file
audio_file_name = "ruthvispeech.ogg" 

print(f"Transcribing '{audio_file_name}'...")
start_time = time.time()

# Run the transcription. fp16=False forces CPU usage cleanly
result = model.transcribe(audio_file_name, fp16=False)

end_time = time.time()

print("\n--- Transcription Result ---")
print(result["text"])
print("----------------------------")
print(f"Done in {end_time - start_time:.2f} seconds!")