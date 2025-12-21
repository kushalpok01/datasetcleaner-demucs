import subprocess
import os

chunks = [
("00:00:00", "00:40:01"), #chunk000
("00:40:01", "01:00:40"), #chunk001
("01:00:40", "02:00:00"), #chunk002
("02:00:00", "03:00:32"), #chunk003
("03:00:32", "04:06:23"), #chunk004
("04:06:23", "05:09:36"), #chunk005
]

input_audio = "cleanedaudio.wav"
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
    print(f"Saved: {out_file}")
