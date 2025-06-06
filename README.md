# Podcast Speed Downloader

This is a lightweight Python script that:

- Automatically downloads podcast episodes from one or more RSS feeds
- Speeds them up to a specified playback rate (e.g., 2.5x)
- Preserves audio pitch
- Saves the processed episodes as MP3s

Perfect for people who want to maximize efficiency.

---

## Features

- Batch downloads latest episodes from multiple feeds
- Converts audio to faster speed while preserving pitch
- Saves output as `.mp3` files in a configurable directory

---

## Requirements

Install Python packages in your virtual environment:

```bash
pip install feedparser requests ffmpeg-python tqdm
```

---

## Instructions

1. Clone or download this project
2. Create a feeds.txt file with one RSS feed URL per line.
3. Adjust settings in main.py
4. Run the script
```bash
   python main.py
```
By default, the standard speedup wiil be 2.5x, it will download 5 newest episodes per feed, and downloads will be placed in a local directory Downlods/
