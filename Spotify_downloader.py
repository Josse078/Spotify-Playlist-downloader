import requests
import base64
import yt_dlp
from moviepy.editor import *
import os
from dotenv import load_dotenv  

load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

if not CLIENT_ID or not CLIENT_SECRET:
    raise EnvironmentError("Missing Spotify API credentials in environment variables.")

def get_playlist_name(playlist_id, token):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['name']

def get_access_token(client_id, client_secret):
    auth_string = f'{client_id}:{client_secret}'
    b64_auth_string = base64.b64encode(auth_string.encode()).decode()
    headers = {"Authorization": f'Basic {b64_auth_string}'}
    data = {'grant_type': 'client_credentials'}
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    response.raise_for_status()
    return response.json()['access_token']

def get_playlist_tracks(playlist_id, access_token):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {"Authorization": f"Bearer {access_token}"}
    tracks = []
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if 'items' not in data:
            raise KeyError(f"'items' key not found in API response: {data}")
        for item in data['items']:
            track = item['track']
            if track:
                track_name = track['name']
                artist_names = ", ".join(artist['name'] for artist in track['artists'])
                tracks.append(f"{track_name} by {artist_names}")
        url = data.get('next')
    return tracks

def get_first_youtube_link(search_query):
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(f"ytsearch1:{search_query}", download=False)
        return info['entries'][0]['webpage_url']

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

def extract_playlist_id(input_string):
    if not input_string:
        raise ValueError("Input cannot be empty.")
    if 'open.spotify.com/playlist/' in input_string:
        playlist_id = input_string.split('playlist/')[1].split('?')[0]
    else:
        playlist_id = input_string.strip().split('?')[0]
    if not playlist_id or len(playlist_id) != 22:
        raise ValueError("Invalid playlist ID format")
    return playlist_id

def main():
    user_input = input("Enter the Spotify Playlist URL or ID: ")
    playlist_id = extract_playlist_id(user_input)
    token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    name = get_playlist_name(playlist_id, token)
    result_path = os.path.join("Result", name)
    os.makedirs(result_path, exist_ok=True)
    track_list = get_playlist_tracks(playlist_id, token)
    for idx, track in enumerate(track_list, start=1):
        link = get_first_youtube_link(track)
        try:
            download_video(link, result_path)
            print(f'Downloaded: {track}')
        except Exception as e:
            print(f"Error downloading {track}: {e}")
        print(f'{idx}. {track} : {link}')

if __name__ == '__main__':
    main()
