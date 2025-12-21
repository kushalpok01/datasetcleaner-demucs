import subprocess
import os
from pathlib import Path
import sys


CHUNKS_DIR = Path(".") 
OUTPUT_DIR = Path("clean_audio")
OUTPUT_DIR.mkdir(exist_ok=True)

chunks = sorted(CHUNKS_DIR.glob("chunk_*.mp3"))

if not chunks:
    print("No chunks found!")
    sys.exit(1)

for chunk in chunks:
    print(f"Processing: {chunk.name}")


    cmd = [
        sys.executable, "-m", "demucs",
        "--two-stems", "vocals",
        str(chunk)
    ]
    subprocess.run(cmd, check=True)

    demucs_output = Path("separated/htdemucs") / chunk.stem / "vocals.wav"

    if not demucs_output.exists():
        print(f"Missing output for {chunk.name}, skipping...")
        continue

    final_output = OUTPUT_DIR / f"{chunk.stem}_cleaned.wav"
    os.replace(demucs_output, final_output)

    print(f"Saved clean audio: {final_output}")

print("All chunks have been processed successfully!")
