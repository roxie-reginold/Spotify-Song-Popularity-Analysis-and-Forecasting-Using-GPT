#!/usr/bin/env python3
"""
Script to create a simplified dataset with only the essential columns for Spotify analysis
"""
import pandas as pd

# Configuration
INPUT_FILE = "Most Streamed Spotify Songs 2024.csv"
OUTPUT_FILE = "Spotify_Essential_Data.csv"

# Columns to keep
ESSENTIAL_COLUMNS = [
    'Track',
    'Album Name',
    'Artist',
    'All Time Rank',
    'Track Score',
    'Spotify Playlist Count',
    'Spotify Playlist Reach',
    'Spotify Popularity'
]

def create_simplified_dataset():
    """
    Extract only the essential columns from the full dataset
    """
    try:
        # Load the full dataset
        print(f"Loading dataset from {INPUT_FILE}...")
        df = pd.read_csv(INPUT_FILE)
        
        # Check if all required columns exist
        missing_columns = [col for col in ESSENTIAL_COLUMNS if col not in df.columns]
        if missing_columns:
            print(f"Error: Missing columns in the dataset: {missing_columns}")
            print(f"Available columns: {df.columns.tolist()}")
            return
        
        # Create the simplified dataset
        simplified_df = df[ESSENTIAL_COLUMNS].copy()
        
        # Handle any missing values
        for col in ESSENTIAL_COLUMNS:
            if simplified_df[col].isna().any():
                print(f"Note: Column '{col}' has {simplified_df[col].isna().sum()} missing values")
        
        # Convert string columns that should be numeric
        numeric_columns = ['Spotify Playlist Count', 'Spotify Playlist Reach']
        for col in numeric_columns:
            if simplified_df[col].dtype == 'object':
                try:
                    # Remove commas and convert to float
                    simplified_df[col] = simplified_df[col].str.replace(',', '').astype(float)
                    print(f"Converted '{col}' to numeric format")
                except Exception as e:
                    print(f"Warning: Could not convert '{col}' to numeric: {e}")
        
        # Save to CSV
        simplified_df.to_csv(OUTPUT_FILE, index=False)
        print(f"Successfully created simplified dataset with {len(simplified_df)} rows and {len(ESSENTIAL_COLUMNS)} columns")
        print(f"Data saved to {OUTPUT_FILE}")
        
        # Display sample of the data
        print("\nSample data (first 5 rows):")
        print(simplified_df.head())
        
    except FileNotFoundError:
        print(f"Error: Input file '{INPUT_FILE}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_simplified_dataset()
