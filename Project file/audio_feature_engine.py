import wave
import numpy as np
import os

def extract_audio_features(file_path):
    if not os.path.exists(file_path):
        return {"error": f"File {file_path} not found."}
        
    with wave.open(file_path, 'rb') as audio_file:
        num_channels = audio_file.getnchannels()
        sample_width = audio_file.getsampwidth()
        frame_rate = audio_file.getframerate()
        num_frames = audio_file.getnframes()
        
        duration = num_frames / float(frame_rate)
        
        # Read raw frames into a numpy array to analyze the signal
        raw_data = audio_file.readframes(num_frames)
        dtype = np.int16 if sample_width == 2 else np.uint8
        audio_signal = np.frombuffer(raw_data, dtype=dtype)
        
    # Calculate Silence Percentage
    abs_signal = np.abs(audio_signal)
    max_val = np.max(abs_signal) if np.max(abs_signal) > 0 else 1
    normalized_signal = abs_signal / max_val
    
    silence_threshold = 0.03
    silent_frames = np.sum(normalized_signal < silence_threshold)
    silence_percentage = (silent_frames / len(normalized_signal)) * 100
    
    # Calculate Audio Quality Score out of 100
    mean_volume = np.mean(normalized_signal)
    if mean_volume < 0.01 or silence_percentage > 90:
        clarity_score = 10.0
    else:
        variance = np.var(normalized_signal)
        clarity_score = min(100.0, max(0.0, (variance * 400) + 50))
        
    return {
        "duration_seconds": round(duration, 2),
        "channels": "Stereo" if num_channels == 2 else "Mono",
        "sample_rate_hz": frame_rate,
        "silence_percentage": round(silence_percentage, 1),
        "audio_quality_score": round(clarity_score, 1)
    }

if __name__ == "__main__":
    # 1. Put your actual audio file name here (can be .mp3 or .ogg)
    input_audio_file = "ruthvispeech.mp3" 
    
    # 2. This auto-converts it to a temporary .wav file using FFmpeg
    wav_target = "temp_test_properties.wav"
    print(f"--- Converting {input_audio_file} to WAV for analysis ---")
    
    # Run a quick system command to convert the audio cleanly
    conversion_status = os.system(f'ffmpeg -y -i "{input_audio_file}" -ar 16000 -ac 1 "{wav_target}" >nul 2>&1')
    
    if conversion_status == 0 and os.path.exists(wav_target):
        # 3. Extract metrics
        features = extract_audio_features(wav_target)
        print("\n--- EXTRACTED AUDIO FEATURES ---")
        for key, value in features.items():
            print(f"{key}: {value}")
            
        # Clean up the temporary file
        os.remove(wav_target)
    else:
        print(f"\nError: Could not find or convert '{input_audio_file}'.")
        print("Please check that the file name matches your folder exactly!")