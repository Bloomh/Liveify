import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# export SPOTIPY_CLIENT_ID="" - ran these in the terminal
# export SPOTIPY_CLIENT_SECRET=""

juice_uri = 'spotify:artist:4MCBfE4596Uoi2O4DtmEMz'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

results = spotify.artist_albums(juice_uri, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])