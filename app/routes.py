from app import app
from flask import render_template, flash, redirect, request, session
from app.forms import Input, LoginForm
from spot import Spot
import tekore as tk
from tekore import model

"""
export SPOTIFY_CLIENT_ID=""
export SPOTIFY_CLIENT_SECRET=""
export SPOTIFY_REDIRECT_URI="http://localhost:5000/callback"
"""

# conf = tk.config_from_environment()
# tk.config_to_file(file_path="conf.ini", conf)
conf = tk.config_from_file(file_path="conf.txt", section='DEFAULT', return_refresh=False)
cred = tk.Credentials(*conf)
spotify = tk.Spotify()

users = {}

@app.route('/')
def main():
    user = session.get('user', None)
    song = None
    in_link = '<a href="/login">login</a>'
    out_link = '<a href="/logout">logout</a>'
    if user is None:
        page = f'User ID: {user}<br>You can {in_link} or {out_link}.'
    if user is not None:
        token = users[user]
        input_link = '<a href="/input">input</a>'
        page = f'User ID: {user}<br>You can {in_link} or {out_link}. Now that you\'re logged in, head to {input_link}'
        if token.is_expiring:
            token = cred.refresh(token)
            users[user] = token

        try:
            with spotify.token_as(users[user]):
                song = spotify.playback_currently_playing()

            page += f'<br>Now playing: {song.item.name}'
            print(type(song.item.album.images))
        except Exception:
            page += '<br>Error in retrieving now playing!'

    return render_template('home.html', user=user, song=song, title="Welcome to Liveify!")

@app.route('/login', methods=['GET'])
def login():
    auth_url = cred.user_authorisation_url(scope=tk.scope.every)
    return redirect(auth_url, 307)

@app.route('/logout', methods=['GET'])
def logout():
    uid = session.pop('user', None)
    if uid is not None:
        users.pop(uid, None)
    return redirect('/', 307)

    return app

@app.route('/callback', methods=['GET'])
def login_callback():
    code = request.args.get('code', None)

    token = cred.request_user_token(code)
    with spotify.token_as(token):
        info = spotify.current_user()

    session['user'] = info.id
    users[info.id] = token

    return redirect('/', 307)

@app.route('/index')
def index():
    return render_template('index.html', title='Success!')

# @app.route('/login')
# def login():
#     form = LoginForm()
#     return render_template('login.html', title='Sign In', form=form)

@app.route('/input', methods=['GET', 'POST'])
def input():
    form = Input()
    if form.validate_on_submit():
        try:
            # print(float(form.mood.data), float(form.danceability.data), float(form.energy.data))
            if not 0<= float(form.mood.data) <= 1.0 or not 0<=float(form.danceability.data)<=1 or not 0<=float(form.energy.data)<=1:
                flash('Please make sure your inputs are correct')
                return redirect('/input')
            # flash('Name: {}, Mood: {}'.format(form.username.data, form.mood.data))

            user = session.get('user', None)
            token = users[user]
            if token.is_expiring:
                token = cred.refresh(token)
                users[user] = token
            with spotify.token_as(users[user]):
            #     # tracks = spotify.current_user_top_tracks(limit=10)
            #     # for track in tracks.items:
            #     #     print(track.name)
            #     top_artists_name = [] #name used to avoid duplicates
            #     top_artists_uri = [] #uniform resource indicator to connect direct with spotify api

            #     ranges = ['short_term', 'medium_term', 'long_term'] #4 weeks, 6 months, all time
            #     for r in ranges:
            #         print(r)
            #         top_artists_all_data = spotify.current_user_top_artists(limit=50, time_range=r) #get their top artists
            #         top_artists_data = top_artists_all_data.items
            #         for artist_data in top_artists_data:
            #             if artist_data.name not in top_artists_name:
            #                 top_artists_name.append(artist_data.name)
            #                 top_artists_uri.append(artist_data.uri)
                
            #     followed_artists_all_data = spotify.followed_artists(limit=50)
            #     print("bruh")

            # print(top_artists_name)
                s = Spot(form.username.data, form.mood.data, spotify)
                s.grab_songs(float(form.mood.data), float(form.danceability.data), float(form.energy.data))
                # s.do_stuff()
            return redirect('/index')
        except:
            flash('Please input your username and a mood from 0 to 1')
            return redirect('/input')
    flash('Please input a mood from 0 to 1')
    return render_template('input.html', title='Create Your Concert!', form=form)

# @app.route('/verify')
# def verify():
