#https://medium.com/@mohithsubbarao/moodtape-using-spotify-api-to-create-mood-generated-playlists-6e1244c70892
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import sys, random, re

client_id = ""
client_secret = ""

redirect_uri = "http://127.0.0.1:5000/input" #"https://localhost:9009/"

scope = "user-library-read user-top-read playlist-modify-public user-follow-read" #sets what we can access

# print(sys.argv) #arguments are taken from the command line prompt (should be changed in the actual project lol)
# if len(sys.argv)>2:
#     username = sys.argv[1]
#     mood = float(sys.argv[2])
# else:
#     print("Usage: %s username" % (sys.argv[0],))
#     sys.exit()

username = "henry"
mood = 0.7

token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
print("hello")
print(token)

if token:

    #authenticating spotipy

    def authenticate_spotify():
        print("connecting to Spotify")
        sp = spotipy.Spotify(auth=token)
        return sp

# print(authenticate_spotify())

def aggregate_top_artists(sp):
    print("getting top artists")
    top_artists_name = [] #name used to avoid duplicates
    top_artists_uri = [] #uniform resource indicator to connect direct with spotify api

    ranges = ['short_term', 'medium_term', 'long_term'] #4 weeks, 6 months, all time
    for r in ranges:
        top_artists_all_data = sp.current_user_top_artists(limit=50, time_range=r) #get their top artists
        top_artists_data = top_artists_all_data['items']
        for artist_data in top_artists_data:
            if artist_data['name'] not in top_artists_name:
                top_artists_name.append(artist_data['name'])
                top_artists_uri.append(artist_data['uri'])
            # print(r, artist_data['name']) 
    
    followed_artists_all_data = sp.current_user_followed_artists(limit=50) 
    followed_artists_data = (followed_artists_all_data['artists'])
    for artist_data in followed_artists_data['items']:
        if artist_data['name'] not in top_artists_name:
            top_artists_name.append(artist_data['name'])
            top_artists_uri.append(artist_data['uri'])
    return top_artists_uri

def aggregate_top_tracks(sp, top_artists_uri):
    print("getting top tracks")
    top_tracks_uri = []
    for artist in top_artists_uri:
        try:
            top_tracks_all_data = sp.artist_top_tracks(artist) #get the artist's top tracks - if we were to do all of their tracks, we would have to accomodate for live performances and commentary pieces (using the "liveness" and "speechiness" attributes)
            top_tracks_data = top_tracks_all_data['tracks']
            for track_data in top_tracks_data:
                top_tracks_uri.append(track_data['uri'])
        except: #prevents some weird http error
            continue
    return top_tracks_uri
        
def select_tracks(sp, top_tracks_uri):
    print("selecting tracks")
    selected_tracks_uri = []
    random.shuffle(top_tracks_uri)
    for tracks in list(top_tracks_uri): #list(group(top_tracks_uri, 50))
        tracks_all_data = sp.audio_features(tracks)
        for track_data in tracks_all_data:
            try:
                # if mood < 0.15 and track_data['valence']<0.15:
                #     selected_tracks_uri.append(track_data["uri"])
                # elif 0.15 <= mood < 0.25 and 0.15 <= track_data['valence']<0.25:
                #     selected_tracks_uri.append(track_data["uri"])
                # elif 0.25 <= mood < 0.50 and 0.25 <= track_data['valence']<0.50:
                #     selected_tracks_uri.append(track_data["uri"])
                # elif 0.50 <= mood < 0.75 and 0.50 <= track_data['valence']<0.75:
                #     selected_tracks_uri.append(track_data["uri"])
                # elif 0.75 <= mood < 0.90 and 0.75 <= track_data['valence']<0.90:
                #     selected_tracks_uri.append(track_data["uri"])
                # elif 0.85 <= mood and 0.85 <= track_data['valence']:
                #     selected_tracks_uri.append(track_data["uri"])
                # if abs(track_data['valence']-mood) <= 0.10:
                if track_data['liveness']>0.8:
                    selected_tracks_uri.append(track_data["uri"])
                    # print(track_data["uri"], track_data['valence'])
            except TypeError as te:
                continue
    return selected_tracks_uri

def create_playlist(sp, selected_tracks_uri):
    print("creating playlist")
    user_all_data = sp.current_user()
    user_id = user_all_data['id']

    playlist_all_data = sp.user_playlist_create(user_id, "joe mama's tunes" + str(mood))
    playlist_id = playlist_all_data['id']

    random.shuffle(selected_tracks_uri)
    sp.user_playlist_add_tracks(user_id, playlist_id, selected_tracks_uri[:30]) #can do up to 100 tracks before spotify gets angry and throws an error

print("h")
s = authenticate_spotify()
print("h")
create_playlist(s, select_tracks(s, aggregate_top_tracks(s, aggregate_top_artists(s))))