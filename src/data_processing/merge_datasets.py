#!/usr/bin/env python3
"""
Script to merge the simplified dataset with genre information
"""
import pandas as pd

# Configuration
ESSENTIAL_DATA_FILE = "Spotify_Essential_Data.csv"
GENRES_DATA_FILE = "Spotify_Songs_With_Genres.csv"
OUTPUT_FILE = "Spotify_Analysis_Ready.csv"

def merge_datasets():
    """
    Merge the essential data with genre information
    """
    try:
        # Load the datasets
        print(f"Loading essential data from {ESSENTIAL_DATA_FILE}...")
        essential_df = pd.read_csv(ESSENTIAL_DATA_FILE)
        
        print(f"Loading genre data from {GENRES_DATA_FILE}...")
        genres_df = pd.read_csv(GENRES_DATA_FILE)
        
        # Check the datasets
        print(f"Essential dataset: {len(essential_df)} rows, {len(essential_df.columns)} columns")
        print(f"Genres dataset: {len(genres_df)} rows, {len(genres_df.columns)} columns")
        
        # Merge the datasets on Track and Artist
        print("Merging datasets...")
        merged_df = pd.merge(
            essential_df, 
            genres_df[['Track', 'Artist', 'Genres']], 
            on=['Track', 'Artist'], 
            how='left'
        )
        
        # Fill any missing genres
        merged_df['Genres'] = merged_df['Genres'].fillna('Unknown')
        
        # Save the merged dataset
        merged_df.to_csv(OUTPUT_FILE, index=False)
        
        # Calculate statistics
        total_songs = len(merged_df)
        songs_with_genres = (merged_df['Genres'] != 'Unknown').sum()
        genre_coverage_pct = (songs_with_genres / total_songs) * 100
        
        print(f"\nSuccessfully merged datasets!")
        print(f"Total songs: {total_songs}")
        print(f"Songs with genre information: {songs_with_genres} ({genre_coverage_pct:.2f}%)")
        print(f"Analysis-ready data saved to {OUTPUT_FILE}")
        
        # Display sample
        print("\nSample of the merged data (first 5 rows):")
        print(merged_df.head())
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    merge_datasets()
