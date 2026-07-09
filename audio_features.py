import librosa
import numpy as np
import matplotlib.pyplot as plt


def analyze_audio(audio_path):
    # Load audio
    y, sr = librosa.load(audio_path, sr=None)

    # Duration
    duration = librosa.get_duration(y=y, sr=sr)

    # RMS Energy
    rms = librosa.feature.rms(y=y)[0]
    avg_rms = np.mean(rms)

    # Simple pause detection
    threshold = 0.01
    pause_samples = np.sum(np.abs(y) < threshold)
    pause_ratio = pause_samples / len(y)

    # Waveform
    plt.figure(figsize=(10, 3))
    plt.plot(y)
    plt.title("Audio Waveform")
    plt.xlabel("Samples")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.savefig("waveform.png")
    plt.close()

    return {
        "duration": round(duration, 2),
        "average_rms": round(float(avg_rms), 4),
        "pause_ratio": round(float(pause_ratio), 4),
        "waveform": "waveform.png"
    }


# Test the file directly
if __name__ == "__main__":
    audio_file = "uploads/testsaudio.wav"   # Replace with your audio file
    result = analyze_audio(audio_file)

    print("Audio Analysis")
    print("----------------")
    print("Duration:", result["duration"], "seconds")
    print("Average RMS:", result["average_rms"])
    print("Pause Ratio:", result["pause_ratio"])
    print("Waveform saved as:", result["waveform"])