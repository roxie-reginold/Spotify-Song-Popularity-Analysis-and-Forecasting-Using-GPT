import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import google.generativeai as genai
# from https://community.spotify.com/t5/Spotify-for-Developers/retrieving-genre-of-track-in-metadata/td-p/5495626 

# Load environment variables from .env file
load_dotenv()

# Set up Gemini AI with API key
gemini_api_key = os.getenv('GEMINI_API_KEY')
if gemini_api_key:
    os.environ['GOOGLE_API_KEY'] = gemini_api_key  # Required by the Google API
    genai.configure(api_key=gemini_api_key)

# Authentication using environment variables
auth_manager = SpotifyOAuth(client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
                            redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
                            scope=os.getenv("SPOTIFY_SCOPE"))

sp = spotipy.Spotify(auth_manager=auth_manager)


# Function to get genres using Gemini AI
def get_genre_from_gemini(track_name, artist_name):
    """
    Use Gemini AI to get genre information for a song when Spotify API returns no results
    """
    try:
        # Initialize the Gemini model
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        # Create a prompt asking about the song's genre
        prompt = f"""I need to know the music genres for the song '{track_name}' by {artist_name}.
        Please provide 2-4 music genres that accurately categorize this song.
        Format your response as a simple comma-separated list of genres only, with no explanations or additional text.
        Example: 'pop, dance-pop, electropop'"""
        
        # Generate response
        response = model.generate_content(prompt)
        
        # Process the response to get a set of genres
        genres_text = response.text.strip().lower()
        
        # Split by commas and clean up each genre
        genres_list = [genre.strip() for genre in genres_text.split(',')]
        
        # Remove any empty strings and return as a set
        return set(genre for genre in genres_list if genre)
        
    except Exception as e:
        print(f"Error getting genres from Gemini: {e}")
        return set()  # Return empty set if there's an error

#function to retrieve song's artist genre
def get_genre(track_name, artist_name):
    """
    Get genre information for a song, first trying Spotify API and falling back to Gemini AI if needed
    """
    try:
        # First try to get genres from Spotify API
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
            
            # If Spotify returned no genres, fall back to Gemini
            if not unique_genres and gemini_api_key:
                print(f"No genres found in Spotify for {track_name} by {artist_name}, trying Gemini AI...")
                return get_genre_from_gemini(track_name, artist_name)
                
            return unique_genres
        else:
            # If track not found in Spotify, try Gemini
            if gemini_api_key:
                print("Song not found in Spotify, trying Gemini AI...")
                return get_genre_from_gemini(track_name, artist_name)
            return "Song not found"
    except Exception as e:
        print(f"Error in Spotify genre lookup: {e}")
        # Try Gemini as a fallback if there's an error with Spotify
        if gemini_api_key:
            print("Falling back to Gemini AI due to Spotify API error")
            return get_genre_from_gemini(track_name, artist_name)
        return f"Error: {e}"


# Example usage
# track_name = "Shape of You"
# artist_name = "Ed Sheeran"
# genres = get_genre(track_name, artist_name)
# print(genres)



    