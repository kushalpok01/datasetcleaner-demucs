#!/usr/bin/env python3
"""
YouTube → .wav + .txt + .srt
- Uses system ffmpeg (already in PATH)
- Skips download if .wav already exists
- Converts any existing audio file to .wav (once)
"""

import sys
import shutil
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
from youtube_transcript_api.formatters import TextFormatter, SRTFormatter


# ----------------------------------------------------------------------
# 0. Verify ffmpeg/ffprobe are available
# ----------------------------------------------------------------------
def _verify_ffmpeg():
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise RuntimeError(
            "ffmpeg/ffprobe not found in PATH. "
            "Add the folder containing ffmpeg.exe to your system PATH and restart VS Code."
        )
    print(f"ffmpeg found: {shutil.which('ffmpeg')}")
    print(f"ffprobe found: {shutil.which('ffprobe')}")

_verify_ffmpeg()


# ----------------------------------------------------------------------
# 1. Extract video ID
# ----------------------------------------------------------------------
def get_video_id(url: str) -> str:
    parsed = urlparse(url)
    if parsed.hostname in ("youtu.be",):
        return parsed.path[1:]
    if parsed.hostname in ("youtube.com", "www.youtube.com"):
        if parsed.path == "/watch":
            return parse_qs(parsed.query)["v"][0]
        if parsed.path.startswith("/embed/"):
            return parsed.path.split("/")[2]
        if parsed.path.startswith("/v/"):
            return parsed.path.split("/")[2]
    raise ValueError("Invalid YouTube URL")


# ----------------------------------------------------------------------
# 2. Download / convert to WAV (skip if .wav exists)
# ----------------------------------------------------------------------
def download_wav(url: str, out_dir: str = "downloads") -> str | None:
    video_id = get_video_id(url)
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    final_wav = out_path / f"{video_id}.wav"

    # 1. If .wav already exists → done
    if final_wav.exists():
        print(f"WAV already exists → {final_wav}")
        return str(final_wav)

    # 2. Look for any existing audio file (from previous runs)
    existing_audio = None
    for ext in (".m4a", ".webm", ".opus", ".mp4", ".mkv"):
        candidate = out_path / f"{video_id}{ext}"
        if candidate.exists():
            existing_audio = candidate
            break

    if existing_audio:
        print(f"Found existing audio: {existing_audio}")
        print(f"Converting to WAV → {final_wav}")
        
        # Use ffmpeg directly for conversion
        import subprocess
        try:
            subprocess.run([
                "ffmpeg", "-i", str(existing_audio),
                "-acodec", "pcm_s16le", "-ar", "44100",
                str(final_wav)
            ], check=True, capture_output=True)
            
            print(f"WAV created → {final_wav}")
            # Optional: remove old file
            try:
                existing_audio.unlink()
            except Exception:
                pass
            return str(final_wav)
        except subprocess.CalledProcessError as e:
            print(f"Conversion failed: {e}")

    # 3. No existing file → normal download + convert
    print(f"Downloading from YouTube and converting → {final_wav}")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(out_path / f"{video_id}.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
        }],
        "quiet": False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        if final_wav.exists():
            print(f"WAV saved → {final_wav}")
            return str(final_wav)
    except Exception as e:
        print(f"Download failed: {e}")
    return None


# ----------------------------------------------------------------------
# 3. Download transcript
# ----------------------------------------------------------------------
def download_transcript(url: str, out_dir: str = "downloads", langs=["ne", "np"]) -> tuple[str | None, str | None]:
    video_id = get_video_id(url)
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    txt_path = out_path / f"{video_id}.txt"
    srt_path = out_path / f"{video_id}.srt"

    print(f"Fetching transcript for {video_id} …")
    try:
        ytt = YouTubeTranscriptApi()
        tlist = ytt.list(video_id)

        t = None
        try:
            t = tlist.find_transcript(langs)
            print(f"Using manual transcript ({t.language_code})")
        except NoTranscriptFound:
            try:
                t = tlist.find_generated_transcript(langs)
                print(f"Using auto-generated transcript ({t.language_code})")
            except NoTranscriptFound:
                t = next(iter(tlist), None)
                if t:
                    print(f"Using available transcript ({t.language_code})")

        if not t:
            print("No transcript available.")
            return None, None

        data = t.fetch()

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(TextFormatter().format_transcript(data))
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(SRTFormatter().format_transcript(data))

        print(f"Transcript → {txt_path} | {srt_path}")
        return str(txt_path), str(srt_path)

    except TranscriptsDisabled:
        print("Transcripts disabled.")
    except Exception as e:
        print(f"Transcript error: {e}")
    return None, None


# ----------------------------------------------------------------------
# 4. Main
# ----------------------------------------------------------------------
def main():
    if len(sys.argv) != 2:
        print("Usage: python yt_downloader.py <YouTube_URL>")
        sys.exit(1)

    url = sys.argv[1].strip()
    try:
        wav = download_wav(url)
        txt, srt = download_transcript(url)

        print("\n=== DONE ===")
        print(f"WAV : {wav or 'Failed'}")
        print(f"TXT : {txt or 'N/A'}")
        print(f"SRT : {srt or 'N/A'}")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()