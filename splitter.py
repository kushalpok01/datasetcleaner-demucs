import os
from pydub import AudioSegment
import pysrt

# ---------------- CONFIG ----------------
AUDIO_FILE = "input.wav"
SRT_FILE = "subtitles.srt"
OUTPUT_DIR = "clips"
# ----------------------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load audio
audio = AudioSegment.from_file(AUDIO_FILE)

# Load subtitles
subs = pysrt.open(SRT_FILE, encoding="utf-8")

for i, sub in enumerate(subs, start=1):
    start_ms = sub.start.ordinal      # milliseconds
    end_ms = sub.end.ordinal

    # Extract audio segment
    clip = audio[start_ms:end_ms]

    # Clean subtitle text for filename
    safe_text = "".join(
        c for c in sub.text if c.isalnum() or c in " _-"
    ).strip().replace(" ", "_")[:40]

    # Filenames
    audio_filename = f"chunk_{i:03d}.wav"
    text_filename = f"chunk_{i:03d}.txt"

    audio_path = os.path.join(OUTPUT_DIR, audio_filename)
    text_path = os.path.join(OUTPUT_DIR, text_filename)

    # Export audio
    clip.export(audio_path, format="wav")

    # Save subtitle text
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(sub.text)

    print(f"Saved: {audio_filename}")

print("Audio split completed!")
