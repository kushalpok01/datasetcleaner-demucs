import subprocess
import whisper
import os

# === CONFIGURATION ===
youtube_url = "https://www.youtube.com/watch?v=p-yTCgYGNqY"
audio_dir = "audio"
transcript_dir = "transcripts"
audio_filename = os.path.join(audio_dir, "full_audio.mp3")

# === CUSTOM CHUNKS ===
timestamps = [
("00:00:00", "00:40:01"),
("00:40:01", "01:00:40"),
("01:00:40", "02:00:00"),
("02:00:00", "03:00:32"),
("03:00:32", "04:29:41"),
]

# === CREATE FOLDERS ===
os.makedirs(audio_dir, exist_ok=True)
os.makedirs(transcript_dir, exist_ok=True)

# === DOWNLOAD AUDIO ===
print("📥 Downloading audio from YouTube...")

subprocess.run([
    "C:/yt-dlp/yt-dlp.exe", "-f", "bestaudio", "-x", "--audio-format", "mp3",
    "-o", audio_filename, youtube_url
])



# === CALCULATE DURATIONS ===
def time_to_seconds(t):
    h, m, s = map(int, t.split(":"))
    return h * 3600 + m * 60 + s

chunks = []
for i in range(len(timestamps)):
    start = timestamps[i][0]
    end = timestamps[i][1]
    start_sec = time_to_seconds(start)
    end_sec = time_to_seconds(end)
    duration = end_sec - start_sec
    chunks.append((start, str(duration)))

# === SPLIT AUDIO ===
print("✂️  Splitting audio...")
for i, (start, duration) in enumerate(chunks):
    output_file = os.path.join(audio_dir, f"chunk_{i:03d}.mp3")
    subprocess.run([
        "ffmpeg", "-i", audio_filename,
        "-ss", start,
        "-t", duration,
        "-c", "copy",
        output_file
    ])
    print(f"✅ Created: {output_file}")


# === TRANSCRIBE USING WHISPER ===
print("🧠 Transcribing chunks...")
model = whisper.load_model("base")  # you can change to "medium" or "large"

for i in range(len(chunks)):
    audio_path = os.path.join(audio_dir, f"chunk_{i:03d}.mp3")
    print(f"🎧 Transcribing {audio_path}...")
    result = model.transcribe(audio_path, language="ne")
    output_txt = os.path.join(transcript_dir, f"chunk_{i:03d}.txt")
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(result["text"])
    print(f"📝 Saved: {output_txt}")

print("✅ All done! Transcripts are in the 'transcripts/' folder.")