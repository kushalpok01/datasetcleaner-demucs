import subprocess
import os
import sys

INPUT_AUDIO = "3rdhalf.wav"
OUTPUT_DIR = "clean_audio"

os.makedirs(OUTPUT_DIR, exist_ok=True)

cmd = [
    sys.executable, "-m", "demucs",
    "--two-stems", "vocals",
    "-d", "cuda",
    INPUT_AUDIO
]  

subprocess.run(cmd, check=True)
 
# Demucs output path
demucs_output = "separated/htdemucs/audio/vocals.wav"

final_output = os.path.join(OUTPUT_DIR, "audio_cleaned.wav")
os.replace(demucs_output, final_output)

print(f"✅ Clean speech saved as: {final_output}")
