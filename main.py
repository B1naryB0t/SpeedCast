import os
import feedparser
import requests
import ffmpeg
from tqdm import tqdm

# === CONFIGURABLE OPTIONS ===
OUT_DIR = "Downloads"  # can be relative or absolute
NUM_EPISODES = 5       # number of episodes to download per feed
SPEED = 2.5            # playback speed multiplier
FEEDS_FILE = "feeds.txt"

# === Ensure output folder exists ===
os.makedirs(OUT_DIR, exist_ok=True)

def sanitize_filename(name):
    return ''.join(c if c.isalnum() or c in (' ', '_') else '_' for c in name).strip().replace(' ', '_')

# Download audio from a URL to a file
def download_audio(url, output_path):
    response = requests.get(url, stream=True)
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

# Use ffmpeg-python to speed up audio with pitch preserved.
def process_audio(input_file, output_file, speed=SPEED):
    if speed <= 2.0:
        atempo_filters = [speed]
    else:
        # Split speed into multiple <2.0 filters (e.g. 2.5 => 1.58 * 1.58)
        root = round(speed ** 0.5, 2)
        atempo_filters = [root, root]

    stream = ffmpeg.input(input_file)
    for tempo in atempo_filters:
        stream = ffmpeg.filter(stream, 'atempo', tempo)
    stream = ffmpeg.output(stream, output_file, format='mp3')
    ffmpeg.run(stream, overwrite_output=True, quiet=True)

# Download and process podcast episodes from a feed.
def process_feed(feed_url):
    feed = feedparser.parse(feed_url)
    podcast_title = sanitize_filename(feed.feed.title)

    for entry in tqdm(feed.entries[:NUM_EPISODES], desc=podcast_title):
        # Find the audio link
        audio_url = next((l.href for l in entry.links if "audio" in l.type), None)
        if not audio_url:
            continue

        title = sanitize_filename(entry.title)
        base_filename = f"{podcast_title}_{title[:40]}"
        input_path = os.path.join(OUT_DIR, f"{base_filename}_orig.mp3")
        output_path = os.path.join(OUT_DIR, f"{base_filename}_x{SPEED}.mp3")

        if os.path.exists(output_path):
            continue  # Already processed

        print(f"Downloading: {entry.title}")
        download_audio(audio_url, input_path)

        print(f"Processing at {SPEED}x speed...")
        process_audio(input_path, output_path, SPEED)

        os.remove(input_path)  # Clean up original file

def main():
    if not os.path.exists(FEEDS_FILE):
        print(f"Missing '{FEEDS_FILE}'. Add some podcast RSS URLs (one per line).")
        return

    with open(FEEDS_FILE) as f:
        feed_urls = [line.strip() for line in f if line.strip()]

    for url in feed_urls:
        process_feed(url)

if __name__ == "__main__":
    main()
