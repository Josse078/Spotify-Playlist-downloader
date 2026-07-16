import os
import yt_dlp
from spotify_scraper import SpotifyClient  

def get_playlist_tracks_free(playlist_url):
    """Fetches playlist metadata and tracks completely keyless using spotifyscraper."""
    print("Extracting tracklist anonymously...")
    
    try:
        client = SpotifyClient()
        playlist = client.get_playlist(playlist_url)
        
        # Access properties directly from the custom Playlist object
        playlist_name = playlist.name
        tracks = []
        
        # Loop through PlaylistTrack items
        for entry in playlist.tracks:
            # Safely extract the inner track object
            track = entry.track
            if track:
                track_name = track.name
                # Extract the name from each artist object in the list
                artists = ", ".join(artist.name for artist in track.artists)
                
                if track_name and artists:
                    tracks.append(f"{track_name} by {artists}")
                elif track_name:
                    tracks.append(track_name)
                    
        return playlist_name, tracks
    except Exception as e:
        raise RuntimeError(f"Could not read playlist. Make sure it is PUBLIC. Error: {e}")

def get_first_youtube_link(search_query):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch1:{search_query}", download=False)
            if 'entries' in info and len(info['entries']) > 0:
                return info['entries'][0]['url']
        except Exception as e:
            print(f"  ↳ Search failed for '{search_query}': {e}")
    return None

def download_video(video_url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

def main():
    user_input = input("Enter PUBLIC Spotify Playlist URL: ").strip()
    if not user_input:
        print("Input cannot be empty.")
        return
        
    try:
        playlist_name, track_list = get_playlist_tracks_free(user_input)
    except Exception as e:
        print(e)
        return

    print(f"\nFound Playlist: '{playlist_name}'")
    result_path = os.path.join("Result", playlist_name)
    os.makedirs(result_path, exist_ok=True)
    
    print(f"Tracks found: {len(track_list)}\n" + "-"*40)
    
    for idx, track in enumerate(track_list, start=1):
        print(f"[{idx}/{len(track_list)}] Searching: {track}")
        link = get_first_youtube_link(track)
        
        if not link:
            print("  ↳ Skipping: No results.")
            continue
            
        try:
            download_video(link, result_path)
            print(f'  ↳ Success!')
        except Exception as e:
            print(f"  ↳ Download Error: {e}")

if __name__ == '__main__':
    main()