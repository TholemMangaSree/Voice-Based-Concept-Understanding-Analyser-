# test_setup.py
print("Checking installations...")

try:
    import whisper
    import torch
    from sentence_transformers import SentenceTransformer
    import os
    
    print("✅ PyTorch version:", torch.__version__)
    print("✅ Whisper loaded successfully!")
    print("✅ Sentence-Transformers loaded successfully!")
    
    # Check if system can find FFmpeg
    ffmpeg_check = os.system("ffmpeg -version > nul 2>&1")
    if ffmpeg_check == 0:
        print("✅ FFmpeg is fully accessible by Python!")
    else:
        print("❌ FFmpeg path issue inside Python environment.")

    print("\n🎉 CONGRATULATIONS! Environment is 100% ready for the project!")

except ImportError as e:
    print(f"❌ Setup incomplete. Missing module: {e}")