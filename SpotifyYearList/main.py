from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

year_of_songs = input("Which year do you want to travel to? (YYYY-MM-DD): ")

response = requests.get("https://www.billboard.com/charts/hot-100/" + year_of_songs)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
song_names = soup.select("li ul li h3")
songs = [song.getText().strip() for song in song_names]
print(songs)


scope = "playlist-modify-private"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        redirect_uri="http://example.com",
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
        show_dialog=True,
        cache_path="***",
        username="***",
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = year_of_songs.split("-")[0]
for song in songs:
    result = sp.search(q=f"track: {song} year: {year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"Song {song} doesn't exist in Spotify.")

playlist = sp.user_playlist_create(user=user_id, name=f"{year_of_songs} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
