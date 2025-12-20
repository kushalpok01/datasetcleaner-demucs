import subprocess
import os

chunks = [
("00:00:00", "02:30:01"),
("02:30:01", "05:09:36"),
]

input_audio = "audio.mp3"
os.makedirs("audio_chunks", exist_ok=True)

for idx, (start, end) in enumerate(chunks):
    out_file = f"audio_chunks/chunk_{idx:03d}.wav"

    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_audio,
        "-ss", start,
        "-to", end,
        "-c", "copy",
        out_file
    ]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ Saved: {out_file}")
