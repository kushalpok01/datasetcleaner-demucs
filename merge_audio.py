from pydub import AudioSegment
import os

INPUT_DIR = "audio_chunks"   # folder with split audios
OUTPUT_FILE = "merged_audio.wav"

combined = AudioSegment.empty()

# Sort files to keep correct order
files = sorted(f for f in os.listdir(INPUT_DIR) if f.endswith((".wav", ".mp3")))

for file in files:
    audio = AudioSegment.from_file(os.path.join(INPUT_DIR, file))
    combined += audio

combined.export(OUTPUT_FILE, format="wav")
print(f"✅ Merged audio saved as: {OUTPUT_FILE}")
