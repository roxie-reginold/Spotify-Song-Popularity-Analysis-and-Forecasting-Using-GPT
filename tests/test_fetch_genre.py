#!/usr/bin/env python3
"""
Test script for checking if fetch_genre.py is working correctly
"""
from fetch_genre import get_genre

def test_genre_fetching():
    """Test the genre fetching with various popular songs that should have genre information"""
    test_cases = [
        ("Shape of You", "Ed Sheeran"),
        ("Blinding Lights", "The Weeknd"),
        ("Someone You Loved", "Lewis Capaldi"),
        ("As It Was", "Harry Styles"),
        ("Espresso", "Sabrina Carpenter")
    ]
    
    print("Testing genre fetching functionality...")
    print("-" * 50)
    
    for track, artist in test_cases:
        print(f"\nAttempting to fetch genres for '{track}' by {artist}:")
        try:
            genres = get_genre(track, artist)
            if genres and isinstance(genres, set) and len(genres) > 0:
                print(f"SUCCESS: Found {len(genres)} genres: {', '.join(genres)}")
            else:
                print(f"WARNING: No genres found (empty set): {genres}")
        except Exception as e:
            print(f"ERROR: Failed to fetch genres: {e}")
    
    print("\nAdditional debug information:")
    print("-" * 50)
    # Print Spotify authentication information (without secrets)
    import os
    print(f"SPOTIFY_CLIENT_ID set: {'Yes' if os.getenv('SPOTIFY_CLIENT_ID') else 'No'}")
    print(f"SPOTIFY_CLIENT_SECRET set: {'Yes' if os.getenv('SPOTIFY_CLIENT_SECRET') else 'No'}")
    print(f"SPOTIFY_REDIRECT_URI: {os.getenv('SPOTIFY_REDIRECT_URI')}")
    print(f"SPOTIFY_SCOPE: {os.getenv('SPOTIFY_SCOPE')}")

if __name__ == "__main__":
    test_genre_fetching()
