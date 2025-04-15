#!/usr/bin/env python3
"""
Script to create a CSV file with genre information for Spotify songs using our genre fetching functionality.
This processes the data in batches to handle large datasets efficiently.
"""
import pandas as pd
import time
from tqdm import tqdm  # For progress tracking
from fetch_genre import get_genre

# Configuration
INPUT_FILE = "Most Streamed Spotify Songs 2024.csv"  # Input CSV file with Spotify data
OUTPUT_FILE = "Spotify_Songs_With_Genres.csv"       # Output CSV file with added genre data
CHUNK_SIZE = 100                                   # Number of songs to process at once
MAX_SONGS = 500                                    # Maximum number of songs to process (set to None for all)
SLEEP_TIME = 0.5                                   # Seconds to wait between API calls to avoid rate limits

# Function to fetch genres for a given row
def fetch_genre_for_row(row):
    """
    Process a single row to get genre information
    """
    try:
        track = row['Track']
        artist = row['Artist'] 
        
        # Get the genre and convert to comma-separated string
        genres = get_genre(track, artist)
        
        # Handle different return types from get_genre
        if isinstance(genres, set):
            return ', '.join(genres) if genres else "Unknown"
        elif isinstance(genres, str):
            return genres
        else:
            return "Error: Unexpected genre format"
    except Exception as e:
        print(f"Error processing {row['Track']} by {row['Artist']}: {e}")
        return "Error"

# Main processing function
def process_spotify_data():
    """
    Main function to process the Spotify dataset and add genre information
    """
    try:
        # Check if the file exists
        try:
            # Just load the first few rows to check if file exists and see column names
            test_df = pd.read_csv(INPUT_FILE, nrows=5)
            print(f"Successfully loaded {INPUT_FILE}. Sample columns: {list(test_df.columns)}")
        except FileNotFoundError:
            print(f"Error: Could not find the input file '{INPUT_FILE}'")
            return
        except Exception as e:
            print(f"Error reading the input file: {e}")
            return
        
        # Process the file in chunks
        print(f"Starting to process {INPUT_FILE} in chunks of {CHUNK_SIZE} songs...")
        
        # Track total songs processed
        total_processed = 0
        
        # Reader for the chunks
        reader = pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE)
        
        # Process each chunk
        for i, chunk in enumerate(reader):
            print(f"\nProcessing chunk {i+1}...")
            
            # Verify required columns exist
            required_columns = ['Track', 'Artist']
            missing_columns = [col for col in required_columns if col not in chunk.columns]
            
            if missing_columns:
                print(f"Error: Missing required columns: {missing_columns}")
                print(f"Available columns: {list(chunk.columns)}")
                return
            
            # Only keep needed columns to reduce memory usage
            df_chunk = chunk[['Track', 'Artist']].copy()
            
            # Make sure we have no missing values in critical columns
            df_chunk = df_chunk.dropna(subset=['Track', 'Artist'])
            
            # Process each row to fetch genre information (with progress bar)
            print("Fetching genres for songs in this chunk...")
            
            # Use tqdm for a progress bar
            genres = []
            for _, row in tqdm(df_chunk.iterrows(), total=len(df_chunk)):
                genre = fetch_genre_for_row(row)
                genres.append(genre)
                time.sleep(SLEEP_TIME)  # Prevent rate limiting
                
            # Add genres to the dataframe
            df_chunk['Genres'] = genres
            
            # Write to CSV
            mode = 'w' if i == 0 else 'a'
            header = True if i == 0 else False
            df_chunk.to_csv(OUTPUT_FILE, mode=mode, header=header, index=False)
            
            # Update total processed
            total_processed += len(df_chunk)
            print(f"Added genres for {len(df_chunk)} songs. Total processed: {total_processed}")
            
            # Check if we've reached the maximum number of songs to process
            if MAX_SONGS and total_processed >= MAX_SONGS:
                print(f"Reached maximum limit of {MAX_SONGS} songs.")
                break
        
        print(f"\nProcessing complete! Genre data saved to {OUTPUT_FILE}")
        print(f"Total songs processed: {total_processed}")
            
    except Exception as e:
        print(f"An error occurred during processing: {e}")

# Run the script
if __name__ == "__main__":
    print("Starting Spotify genre data processing...")
    process_spotify_data()
