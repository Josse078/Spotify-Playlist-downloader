🎵 Anonymous Spotify Playlist Downloader
A lightweight, modern, and zero-configuration Python script to download songs from any public Spotify playlist directly as high-quality .mp3 audio files.

Unlike traditional downloaders that rely on the heavily restricted Spotify Developer API, this tool employs an anonymous, keyless scraping architecture. You do not need a Spotify Premium subscription, developer credentials, or a .env file to run it.

✨ Features
100% Free & Keyless: No SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET required.

Bypasses Premium Restrictions: Works flawlessly without a Spotify Premium account.

Automatic Matching: Extracts song metadata from Spotify and matches it automatically with the best audio sources on YouTube.

High-Quality Audio: Extracts clean, 192kbps .mp3 audio using optimized FFmpeg pipelines.

Smart Directory Structuring: Automatically reads your playlist's name and organizes tracks into a neatly labeled folder.

Search Optimization: Employs metadata-only matching techniques (extract_flat) for lightning-fast search processing.

📽️ Project Demonstration
See the script in action below:

https://github.com/user-attachments/assets/demo

💡 Tip: If you are hosting this project on GitHub, you can drag and drop your screen recording file directly into this section of the Markdown file to display an embedded video player.

🧠 How It Works (The Core Logic)
The script bridges two independent web architectures together without requiring developer access keys. It follows a clean 4-step pipeline:

Plaintext
[ Spotify URL ] ➔ 1. Scrape Metadata ➔ 2. Metadata Text Search ➔ 3. Stream Audio ➔ [ Local .mp3 ]
1. Keyless Metadata Scraping
When you provide a public Spotify URL, the script initializes a SpotifyClient which securely targets Spotify's public front-end interfaces. Because the playlist is public, it fetches the underlying JSON data object containing the playlist name and a list of all tracks. It then isolates the exact song title and contributing artists for every track, mapping them into standard string format strings like "Magnolia by Magnolia Celebration".

2. Flat Search Engine Mapping
Instead of downloading heavy web pages, the script pushes the string query to yt-dlp with the instruction ytsearch1: combined with extract_flat: True. This instructs the program to extract only the bare metadata wrapper from the first search result on YouTube, instantly returning the target URL without wasting network bandwidth on the actual video page layout.

3. Dynamic Stream Demuxing
Once the best matching URL is identified, yt-dlp requests the target stream from YouTube's media delivery servers. The script explicitly filters for 'format': 'bestaudio/best', which tells the network pipeline to ignore the heavy video stream data entirely and stream only the raw, isolated compressed audio track.

4. FFmpeg Post-Processing Transcoding
As chunks of the audio stream are received, the script passes the temporary download stream directly down to FFmpeg via a Python post-processor layer. FFmpeg handles the container conversion, decoding the stream and formatting it into a clean, standalone 192kbps .mp3 output file. The file is saved within an automatically created folder named after your playlist (Result/[Playlist Name]/).

🛠️ Prerequisites
Before executing the script, ensure you have the following installed on your system:

Python 3.8+

FFmpeg: Required by yt-dlp to convert video streams into standalone .mp3 audio.

macOS (via Homebrew): brew install ffmpeg

Windows (via Chocolatey): choco install ffmpeg

Linux (Ubuntu/Debian): sudo apt update && sudo apt install ffmpeg

🚀 Installation & Setup
Save the Script:
Save the script as Spotify_downloader.py inside your desired working directory.

Set Up a Virtual Environment (Recommended):

Bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
Install Dependencies:
Install the necessary modern packages using pip:

Bash
pip install spotify-scraper yt-dlp
📖 Usage Instructions
Ensure your target Spotify playlist is set to Public.

Copy the full playlist link from your browser or Spotify app (e.g., [https://open.spotify.com/playlist/](https://open.spotify.com/playlist/)...).

Run the script:

Bash
python Spotify_downloader.py
Paste the URL when prompted and press Enter.
