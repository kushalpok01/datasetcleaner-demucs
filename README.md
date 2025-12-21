# Demucs Audio Cleaner

Extract clean vocals from audio files using Demucs with a simple Python script.

## Requirements

- Python 3.10 (recommended)
- FFmpeg installed and added to PATH
- YT-DLP added to PATH
- Demucs

## Setup

```bash
python -m venv demucs-env
demucs-env\Scripts\activate

pip install demucs soundfile "numpy<2"

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

python clean.py

