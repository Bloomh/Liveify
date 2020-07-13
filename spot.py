#DELETE CACHE.TXT EVERY TIME THAT YOU REMOVE ACCESS FROM THE APP
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import sys, random, re
from flask import flash, redirect
import tekore as tk
import random

class Spot():
    def __init__(self, username, mood, spotify):#username
        # self.username = username
        self.username = username
        self.mood = float(mood)
        # with open("auth.txt", "r") as f: #reading in the application authorization from the text file auth.txt
        #     lines = f.readlines()
        #     self.client_id = lines[0].strip()
        #     self.client_secret = lines[1].strip() 
        # self.redirect_uri = "http://127.0.0.1:5000/input"
        # self.scope = "user-library-read user-top-read playlist-modify-public user-follow-read"
        # print("b")
        # self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=self.scope))
        self.sp = spotify
        # token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
        # self.sp = spotipy.Spotify(auth=token)
        # self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id, client_secret=self.client_secret, redirect_uri="http://127.0.0.1:5000/input", scope=self.scope)) #, cache_path="cache.txt"
        # print(self.sp) 

        # results = self.sp.current_user_saved_tracks()
        # self.token = util.prompt_for_user_token(self.username, scope, client_id, client_secret, redirect_uri)
        # print("d") 
        # self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri, scope=self.scope, cache_path="cache.txt")) #, username="3blklgk1eghstajpic90ni2wr"
        # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri, scope=self.scope, cache_path="cache.txt")) #, username="3blklgk1eghstajpic90ni2wr"
        # results = sp.current_user_saved_tracks()
        # print(sp)
        # print("b")
        # self.token = util.prompt_for_user_token(self.username, self.scope, self.client_id, self.client_secret, self.redirect_uri, cache_path="new.txt")
        # print("hi")

        # self.sp = spotipy.Spotify(auth=self.token)

        # print("sp:", sp)
        # if self.token: #authenticating spotipy
        #     def authenticate_spotify(self):
        #         print("connecting to Spotify")
        #         sp = spotipy.Spotify(auth=self.token)
        #         return sp

    # def ask_auth(self):

    def aggregate_top_artists(self, sp):
        print("getting top artists")
        # flash("getting top artists")
        top_artists_name = [] #name used to avoid duplicates
        top_artists_id = [] #uniform resource indicator to connect direct with spotify api

        ranges = ['short_term', 'medium_term', 'long_term'] #4 weeks, 6 months, all time
        for r in ranges:
            # print(r)
            top_artists_all_data = sp.current_user_top_artists(limit=50, time_range=r) #get their top artists
            top_artists_data = top_artists_all_data.items
            for artist_data in top_artists_data:
                if artist_data.name not in top_artists_name:
                    top_artists_name.append(artist_data.name)
                    top_artists_id.append(artist_data.id)
                # print(r, artist_data['name']) 

        # print("b")
        followed_artists_all_data = sp.followed_artists(limit=50) 
        # print("a")
        # # followed_artists_data = followed_artists_all_data.items
        # print("e")
        for artist_data in followed_artists_all_data.items:
            if artist_data.name not in top_artists_name:
                top_artists_name.append(artist_data.name)
                top_artists_id.append(artist_data.id)
                # print(sp.artist(artist_data.id))
                # print(sp.artist(artist_data.id))
                # print(artist_data.id)
                # print(artist_data.uri)
        print(len(top_artists_id))
        # for i in top_artists_uri:
        #     print(i)
        # print("here")
        # print(top_artists_uri)
        # print(top_artists_uri)
        return top_artists_id
        #works!
    
    def aggregate_top_tracks(self, sp, top_artists_id):
        print("getting top tracks")
        # flash("getting top tracks")
        top_tracks_id = []
        # print(sp.artists(top_artists_uri))
        # print("h")
        for art in top_artists_id:
            # print(sp)
            # print(art, "1")
            # if art.count("spotify:artist:")>0: #makes sure they are all of the same format
            #     art = art[len("spotify:artist:"):]
            # print(art, "2")
            # print(sp.artist(art))
            try:
                # print("hi")
                top_tracks_data = sp.artist_top_tracks(art, "from_token") #get the artist's top tracks - if we were to do all of their tracks, we would have to accomodate for live performances and commentary pieces (using the "liveness" and "speechiness" attributes)
                # print(top_tracks_data)
                # print("bye")
                # print("hi")
                # top_tracks_data = top_tracks_all_data.tracks
                # print("he")
                for track_data in top_tracks_data:
                    # print("ho")
                    top_tracks_id.append(track_data.id)
                    # print("ha")
            except: #prevents some weird http error
                # print("prevented an error letsgoo")
                continue
        print(len(top_tracks_id))
        return top_tracks_id
        
    def select_tracks(self, sp, top_tracks_id):
        print("selecting tracks")
        # flash("selecting tracks")
        selected_tracks_id = []
        random.shuffle(top_tracks_id)
        # inside = 0
        # success = 0
        for tracks in top_tracks_id: 
            # print("hello)")
            # print("tracks:",tracks)
            # print(tracks, "here")
            try:
                track_data = sp.track_audio_features(tracks)
                # print("track data:", track_data)
                # print("valence:", track_data.valence)
                # print("there")
                # print(tracks_all_data)
                # print("hi")
                # for track_data in tracks_all_data:
                # print("e")
                try:
                    # print(track_data['valence'], self.mood)
                    # print(abs(track_data['valence']-self.mood))
                    # print("1")
                    if abs(track_data.valence-float(self.mood)) <= 0.12:
                        # print("2")
                        # inside += 1
                        selected_tracks_id.append(track_data.id)
                        # print("3")
                        # print(track_data["uri"], track_data['valence'])
                    # success += 1
                except TypeError as te:
                    # print("e")
                    continue
            except:
                continue
        # print("tracks",selected_tracks_uri, "successful:", success, "inside", inside)
        print(len(selected_tracks_id))
        return selected_tracks_id
    
    def create_playlist(self, sp, selected_tracks_id):
        try:
            print("creating playlist")
            # flash("creating playlist")
            print("bruh")
            # print(sp.current_user())
            print("ee")
            user_all_data = sp.current_user()
            print("a")
            user_id = user_all_data.id
            print("b")
            playlist_all_data = sp.playlist_create(user_id, self.username)
            print("c")
            playlist_id = playlist_all_data.id
            print("e")
            random.shuffle(selected_tracks_id)
            print("f")
            print(playlist_id, type(playlist_id))
            print(selected_tracks_id[:50])            
            # print(user_id, playlist_id, selected_tracks_uri[:30])
            sp.playlist_tracks_add(playlist_id, selected_tracks_id[:50])#user_id,  # HTTP Error for POST to {link} returned 400 due to Error parsing JSON.
            print("g")
            flash("Success! Check your spotify account for the playlist")
            return
        except Exception:
            print(Exception)
            print("Something went wrong, please try again")
            flash("Something went wrong, please try again")

    def do_stuff(self):
        if self.sp:
            print("connecting to Spotify")
            # flash("connecting to Spotify")
            s = self.sp
            # print("s", s)
            self.create_playlist(s, self.select_tracks(s, self.aggregate_top_tracks(s, self.aggregate_top_artists(s))))
        else:
            print("No token")
            flash("No token – not authorized")
    
    def grab_songs(self, mood, danceability, energy):
        # print("a") 110ufW2zDSs5ZNadOfkLH7 - liveify
        # print("a") 4eGUqz708EdfM4bkNaYsL6 - live music
        self.sp.playlist_follow(playlist_id="110ufW2zDSs5ZNadOfkLH7")
        # print("b")
        playlist = self.sp.followed_playlists(limit=1).items[0]
        # print("c")
        # print(playlist)
        tracks = []
        r = random.randint(0,8800)
        for i in range(r,r+500): #need to set to the length of the thing
            # print("e")
            try:
                track = self.sp.playlist_items(playlist.id, limit=1, offset=i).items[0].track
                if track.id not in tracks and self.sp.track_audio_features(track.id).liveness>=0.8 and abs(self.sp.track_audio_features(track.id).valence-mood)<=0.30 and abs(self.sp.track_audio_features(track.id).danceability-danceability)<=0.30 and abs(self.sp.track_audio_features(track.id).energy-energy)<=0.30:
                    # print(track.id)
                    # print(len(tracks))
                    tracks.append(track.id)
                    print(len(tracks), i)
                else:
                    print("tried", i)
            except:
                print("boo", i)
                continue
        # for i in self.sp.playlist_items(playlist.id, limit=1, offset=i):
        #     tracks.append(i.track)
        # print("hi")
        print(len(tracks))
        # print("bye")
        self.sp.playlist_unfollow(playlist_id="110ufW2zDSs5ZNadOfkLH7")
        self.create_playlist(self.sp, tracks)
#spotify.playlist_follow(playlist_id="4eGUqz708EdfM4bkNaYsL6")


