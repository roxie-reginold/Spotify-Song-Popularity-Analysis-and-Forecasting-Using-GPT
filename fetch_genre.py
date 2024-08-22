import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# from https://community.spotify.com/t5/Spotify-for-Developers/retrieving-genre-of-track-in-metadata/td-p/5495626 
#load secrets

with open('secrets.json') as f:
    creds = json.load(f)


#authentication
auth_manager = SpotifyOAuth(client_id=creds["spotify_client_id"],
                            client_secret=creds["spotify_client_secret"],
                            redirect_uri=creds["spotify_redirect_uri"],
                            scope=creds["spotify_scope"])

sp = spotipy.Spotify(auth_manager=auth_manager)


#funtion to retrive song's artist genre
def get_genre(track_name, artist_name):
    results = sp.search(q=f'{track_name} {artist_name}', limit=1)
    track_id = None
    artist_ids = []
    for idx, track in enumerate(results['tracks']['items']):
        print(f'Result {idx}: {track["name"]}, {track["artists"][0]["name"]}')
        track_id = track['id']
        break
    if track_id:
        track_info = sp.track(track_id)
        
        # Retrieve artist IDs from the track
        artist_ids = [artist["id"] for artist in track_info["artists"]]
        
        # Fetch artists' data using the collected artist IDs
        artists_data = sp.artists(artist_ids)
        
        # Aggregate genres from all artists
        genres = []
        for artist in artists_data["artists"]:
            genres += artist["genres"]
        
        # Remove duplicates and convert to a set
        unique_genres = set(genres)
        
        return unique_genres
    else:
        return "Song not found"


# Example usage
# track_name = "Shape of You"
# artist_name = "Ed Sheeran"
# genres = get_genre(track_name, artist_name)
# print(genres)



    