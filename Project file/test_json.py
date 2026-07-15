# test_json.py
import json
from datetime import datetime

# 1. Create a dictionary containing your pipeline's metadata
data_to_save = {
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "audio_file": "ruthvispeech.mp3",
    "transcript": "Hello, this is a test for my AI project.",
    "detected_intent": "Unknown Intent",
    "confidence_score": 0.1500
}

# 2. Save it securely to a physical .json file
output_filename = "transcript_data.json"

with open(output_filename, "w", encoding="utf-8") as json_file:
    # 'indent=4' makes the file easy for humans to read!
    json.dump(data_to_save, json_file, indent=4, ensure_ascii=False)

print(f"🎉 Success! Structured data saved completely to '{output_filename}'")