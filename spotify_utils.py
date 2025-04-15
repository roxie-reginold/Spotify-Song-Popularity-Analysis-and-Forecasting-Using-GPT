import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

def get_spotify_client():
    """
    Create and return an authenticated Spotify client using credentials from environment variables.
    """
    # Authenticate using the Client Credentials flow
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp

def get_spotify_track_link(song_name, artist_name=None):
    """
    Search for a track on Spotify and return its URL.
    
    Args:
        song_name (str): The name of the song to search for
        artist_name (str, optional): The artist name to refine the search
        
    Returns:
        dict: Dictionary containing track URL, album cover image, and track details
    """
    try:
        sp = get_spotify_client()
        
        # Build the search query; if artist_name is provided, include it in the query
        if artist_name:
            query = f"track:{song_name} artist:{artist_name}"
        else:
            query = f"track:{song_name}"

        # Use the Spotify search endpoint, specifying type=track and limiting results to 1 for simplicity
        results = sp.search(q=query, type='track', limit=1)

        # Check if any tracks were returned
        if results and 'tracks' in results and results['tracks']['items']:
            track = results['tracks']['items'][0]
            
            # Get album cover image URL (medium size)
            album_cover_url = track['album']['images'][1]['url'] if track['album']['images'] else None
            
            # Return a dictionary with various useful track details
            return {
                'success': True,
                'track_url': track.get('external_urls', {}).get('spotify', 'No URL available'),
                'album_cover_url': album_cover_url,
                'track_name': track['name'],
                'artist_name': track['artists'][0]['name'] if track['artists'] else 'Unknown',
                'album_name': track['album']['name'],
                'preview_url': track.get('preview_url')
            }
        else:
            return {
                'success': False,
                'error': 'No track found on Spotify'
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': f'Error searching Spotify: {str(e)}'
        }

# Example usage (only runs if the file is executed directly)
if __name__ == "__main__":
    # Example to test the function
    song_name = "Blinding Lights"
    artist_name = "The Weeknd"
    result = get_spotify_track_link(song_name, artist_name)
    
    if result['success']:
        print(f"Found: {result['track_name']} by {result['artist_name']}")
        print(f"Spotify URL: {result['track_url']}")
        print(f"Album Cover: {result['album_cover_url']}")
    else:
        print(f"Error: {result['error']}")
