import tekore as tk

conf = tk.config_from_file("conf.txt")
token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)


spotify = tk.Spotify(token)
spotify.playlist_follow(playlist_id="4eGUqz708EdfM4bkNaYsL6")
playlist = spotify.followed_playlists(limit=1).items[0]
track = spotify.playlist_items(playlist.id, limit=1).items[0].track
name = f'"{track.name}" from {playlist.name}'

if track.episode:
    print(f'Cannot analyse episodes!\nGot {name}.')
elif track.track and track.is_local:
    print(f'Cannot analyse local tracks!\nGot {name}.')
else:
    print(f'Analysing {name}...\n')
    analysis = spotify.track_audio_features(track.id)
    print(repr(analysis))