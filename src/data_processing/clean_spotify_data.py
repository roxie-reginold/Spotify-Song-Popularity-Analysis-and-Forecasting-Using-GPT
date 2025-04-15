#!/usr/bin/env python3
"""
Script to clean the Spotify Essential Data CSV file by:
1. Removing duplicate tracks
2. Removing rows with null values
3. Removing rows with non-ASCII characters
"""
import pandas as pd
import re
import os

# Input and output files
INPUT_FILE = "Spotify_Essential_Data.csv"
OUTPUT_FILE = "Spotify_Essential_Data_Clean.csv"

def contains_non_ascii(text):
    """Check if a text contains non-ASCII characters"""
    if not isinstance(text, str):
        return False
    return bool(re.search(r'[^\x00-\x7F]', text))

def clean_spotify_data():
    """Clean the Spotify dataset by removing duplicates, null values, and non-ASCII characters"""
    print(f"Loading dataset from {INPUT_FILE}...")
    
    # Read the CSV file
    df = pd.read_csv(INPUT_FILE)
    
    # Store original row count
    original_count = len(df)
    print(f"Original dataset: {original_count} rows")
    
    # 1. Remove duplicate tracks (keep the first occurrence)
    print("Removing duplicate tracks...")
    df_no_dupes = df.drop_duplicates(subset=['Track'])
    dupes_removed = original_count - len(df_no_dupes)
    print(f"Removed {dupes_removed} duplicate tracks")
    
    # 2. Remove rows with any null values
    print("Removing rows with null values...")
    df_no_nulls = df_no_dupes.dropna()
    nulls_removed = len(df_no_dupes) - len(df_no_nulls)
    print(f"Removed {nulls_removed} rows with null values")
    
    # 3. Remove rows with non-ASCII characters in any column
    print("Removing rows with non-ASCII characters...")
    
    # Create a mask of rows containing non-ASCII characters
    non_ascii_mask = df_no_nulls.applymap(contains_non_ascii).any(axis=1)
    
    # Get rows without non-ASCII characters
    df_clean = df_no_nulls[~non_ascii_mask]
    non_ascii_removed = len(df_no_nulls) - len(df_clean)
    print(f"Removed {non_ascii_removed} rows with non-ASCII characters")
    
    # Save the cleaned dataset
    df_clean.to_csv(OUTPUT_FILE, index=False)
    
    # Print summary
    print("\nCleaning Summary:")
    print(f"Original rows: {original_count}")
    print(f"Rows removed: {original_count - len(df_clean)}")
    print(f"Clean rows: {len(df_clean)}")
    print(f"Clean dataset saved to {OUTPUT_FILE}")
    
    # Create a backup of the original file
    backup_file = f"{os.path.splitext(INPUT_FILE)[0]}_original.csv"
    os.rename(INPUT_FILE, backup_file)
    
    # Rename the cleaned file to the original filename
    os.rename(OUTPUT_FILE, INPUT_FILE)
    
    print(f"\nOriginal file backed up as {backup_file}")
    print(f"Cleaned file is now {INPUT_FILE}")

if __name__ == "__main__":
    clean_spotify_data()
