import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="", client_secret="", redirect_uri="http://127.0.0.1:5000/input", scope=scope, cache_path="cache.txt"))

juice_uri = 'spotify:artist:4MCBfE4596Uoi2O4DtmEMz'

artists = [sp.artist(juice_uri), sp.artist_related_artists(juice_uri)]
print(sp.artist(juice_uri)['name'])
for i in sp.artist_related_artists(juice_uri):
    print(i)
# print(sp.artist_related_artists(juice_uri)['name'])
# for idx, item in enumerate(artists):
    # print(item['name'])

# results = sp.current_user_saved_tracks()
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])

# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
# from spotipy.oauth2 import SpotifyImplicitGrant

# scope = "user-library-read"
# print(sp)

# results = sp.current_user_saved_tracks()
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])