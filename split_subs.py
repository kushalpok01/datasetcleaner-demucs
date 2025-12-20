import webvtt
import os

def str_to_seconds(t):
    parts = t.split(":")
    if len(parts) == 4:
        t = ":".join(parts[:3]) + "." + parts[3]
    h, m, s = map(float, t.replace(',', '.').split(":"))
    return h * 3600 + m * 60 + s

def seconds_to_str(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"

def is_in_range(start, end, t):
    return str_to_seconds(start) <= t < str_to_seconds(end)

def split_sentences(text):
    """
    Split text by danda (।) but keep danda at end of each sentence.
    Remove empty splits.
    """
    parts = []
    buf = ""
    for ch in text:
        buf += ch
        if ch == '।':
            parts.append(buf.strip())
            buf = ""
    # Add leftover if any (sentence without danda)
    if buf.strip():
        parts.append(buf.strip())
    return parts

chunks = [
("00:00:00", "00:40:01"),
("00:40:01", "01:00:40"),
("01:00:40", "02:00:00"),
("02:00:00", "03:00:32"),
("03:00:32", "04:29:41"),
]

captions = list(webvtt.read('subtitles.vtt'))
os.makedirs('transcripts', exist_ok=True)

for idx, (chunk_start, chunk_end) in enumerate(chunks):
    chunk_captions = [c for c in captions if is_in_range(chunk_start, chunk_end, str_to_seconds(c.start))]
    filename = f"chunk_{idx:03d}.txt"

    with open(os.path.join("transcripts", filename), "w", encoding="utf-8") as f:
        for caption in chunk_captions:
            start_sec = str_to_seconds(caption.start)
            end_sec = str_to_seconds(caption.end)
            duration = end_sec - start_sec

            sentences = split_sentences(caption.text)

            if not sentences:
                continue

            seg_duration = duration / len(sentences)

            for i, sentence in enumerate(sentences):
                seg_start = start_sec + i * seg_duration
                seg_end = seg_start + seg_duration
                seg_start_ts = seconds_to_str(seg_start)
                seg_end_ts = seconds_to_str(seg_end)
                f.write(f"[{seg_start_ts} --> {seg_end_ts}] {sentence.strip()}\n\n")

    print(f"✅ Saved: transcripts/{filename}")
