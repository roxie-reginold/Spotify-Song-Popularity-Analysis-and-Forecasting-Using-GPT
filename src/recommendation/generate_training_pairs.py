#!/usr/bin/env python3
"""
Generate training pairs for fine-tuning a recommendation model based on Spotify data.
Each pair consists of:
- Input: A description or preference related to a song
- Output: A recommended song with explanation

The pairs are saved in JSONL format.
"""

import pandas as pd
import json
import random
import numpy as np
from collections import defaultdict

# Input file
SPOTIFY_DATA = "Spotify_Essential_Data.csv"
OUTPUT_FILE = "spotify_recommendation_training_pairs.jsonl"

# Number of training pairs to generate
NUM_PAIRS = 500

def generate_training_pairs():
    """Generate diverse training pairs for fine-tuning"""
    print(f"Loading Spotify data from {SPOTIFY_DATA}...")
    df = pd.read_csv(SPOTIFY_DATA)
    
    # Verify the data
    print(f"Loaded {len(df)} songs with {len(df.columns)} attributes")
    
    # Group songs by artists for easier access
    artist_songs = defaultdict(list)
    for _, row in df.iterrows():
        artist_songs[row['Artist']].append(row)
    
    # Get popular artists (have at least 3 songs)
    popular_artists = [artist for artist, songs in artist_songs.items() 
                       if len(songs) >= 3 and isinstance(artist, str)]
    
    print(f"Found {len(popular_artists)} artists with 3+ songs")
    
    # Calculate similarity between songs for better recommendations
    # Normalize numeric columns for better comparison
    numeric_cols = ['Track Score', 'Spotify Playlist Count', 'Spotify Playlist Reach', 'Spotify Popularity']
    df_numeric = df[numeric_cols].copy()
    
    # Replace missing values with median
    for col in numeric_cols:
        df_numeric[col] = df_numeric[col].fillna(df_numeric[col].median())
    
    # Min-max scaling for each column
    for col in numeric_cols:
        df_numeric[col] = (df_numeric[col] - df_numeric[col].min()) / (df_numeric[col].max() - df_numeric[col].min() + 1e-8)
    
    # Store the normalized values back in the dataframe
    for col in numeric_cols:
        df[f"{col}_normalized"] = df_numeric[col]
    
    # Create training pairs
    print(f"Generating {NUM_PAIRS} training pairs...")
    training_pairs = []
    
    # Different types of input patterns
    input_patterns = [
        "by_track",           # "I enjoy the track X by Y"
        "by_artist",          # "I like songs by X"
        "by_popularity",      # "Recommend me a highly popular song"
        "by_playlist_reach",  # "I'm looking for songs with wide playlist reach"
        "combined_criteria",  # "I want a popular song by X with high playlist count"
        "similar_to",         # "Recommend something similar to X by Y"
        "attribute_based",    # "I prefer songs with high track scores"
        "rank_based",         # "I'm interested in top-ranked songs"
    ]
    
    # Create diverse training pairs
    for _ in range(NUM_PAIRS):
        pattern = random.choice(input_patterns)
        
        if pattern == "by_track":
            # Random song as source
            source_song = df.sample(1).iloc[0]
            input_text = f"I enjoy the track '{source_song['Track']}' by {source_song['Artist']}."
            
            # Find a similar song (not by the same artist)
            target_df = df[df['Artist'] != source_song['Artist']]
            if len(target_df) == 0:
                continue
                
            # Calculate similarity based on normalized values
            similarities = []
            for _, candidate in target_df.iterrows():
                similarity_score = 0
                for col in numeric_cols:
                    norm_col = f"{col}_normalized"
                    if pd.notna(source_song[norm_col]) and pd.notna(candidate[norm_col]):
                        similarity_score += (1 - abs(source_song[norm_col] - candidate[norm_col]))
                similarities.append((similarity_score, candidate))
            
            if not similarities:
                continue
                
            # Get the most similar song
            similarities.sort(reverse=True)
            target_song = similarities[0][1]
            
            # Generate explanation
            explanation = f"You might enjoy '{target_song['Track']}' by {target_song['Artist']} because it has similar "
            similar_attributes = []
            
            if abs(source_song['Spotify Popularity'] - target_song['Spotify Popularity']) < 10:
                similar_attributes.append("popularity")
            if abs(source_song['Track Score'] - target_song['Track Score']) < 50:
                similar_attributes.append("track score")
            if abs(source_song['Spotify Playlist Count'] - target_song['Spotify Playlist Count']) < 50000:
                similar_attributes.append("playlist presence")
                
            if not similar_attributes:
                similar_attributes = ["musical attributes"]
                
            explanation += " and ".join(similar_attributes) + "."
            
            output_text = f"Based on your enjoyment of '{source_song['Track']}', I recommend '{target_song['Track']}' by {target_song['Artist']}. {explanation}"
            
        elif pattern == "by_artist":
            # Choose a random popular artist
            source_artist = random.choice(popular_artists)
            input_text = f"I like songs by {source_artist}."
            
            # Find another artist with similar popularity
            artist_avg_popularity = {}
            for artist, songs in artist_songs.items():
                if len(songs) >= 2 and artist != source_artist:
                    popularities = [song['Spotify Popularity'] for song in songs if pd.notna(song['Spotify Popularity'])]
                    if popularities:
                        artist_avg_popularity[artist] = sum(popularities) / len(popularities)
            
            if not artist_avg_popularity:
                continue
                
            # Get the source artist's average popularity
            source_popularities = [song['Spotify Popularity'] for song in artist_songs[source_artist] 
                                  if pd.notna(song['Spotify Popularity'])]
            if not source_popularities:
                continue
                
            source_avg_popularity = sum(source_popularities) / len(source_popularities)
            
            # Find similar artists
            similarities = [(abs(source_avg_popularity - pop), artist) for artist, pop in artist_avg_popularity.items()]
            similarities.sort()
            
            if not similarities:
                continue
                
            target_artist = similarities[0][1]
            
            # Choose a popular song from the target artist
            target_songs = [song for song in artist_songs[target_artist] 
                           if pd.notna(song['Spotify Popularity'])]
            if not target_songs:
                continue
                
            target_songs.sort(key=lambda x: x['Spotify Popularity'], reverse=True)
            target_song = target_songs[0]
            
            output_text = f"Since you like {source_artist}, you might enjoy '{target_song['Track']}' by {target_artist}. This track has similar appeal with a popularity score of {target_song['Spotify Popularity']:.0f}."
            
        elif pattern == "by_popularity":
            # Get request for popular song
            popularity_threshold = random.uniform(70, 90)
            input_text = f"Recommend me a song with a popularity score above {popularity_threshold:.0f}."
            
            # Find popular songs
            popular_songs = df[df['Spotify Popularity'] >= popularity_threshold].copy()
            if len(popular_songs) == 0:
                # If no songs meet the threshold, lower it
                popularity_threshold = random.uniform(60, 70)
                popular_songs = df[df['Spotify Popularity'] >= popularity_threshold].copy()
                if len(popular_songs) == 0:
                    continue
                
            # Select a random popular song
            target_song = popular_songs.sample(1).iloc[0]
            
            output_text = f"I recommend '{target_song['Track']}' by {target_song['Artist']}. It has a high popularity score of {target_song['Spotify Popularity']:.0f} and is ranked {target_song['All Time Rank']} on the chart."
            
        elif pattern == "by_playlist_reach":
            # Get request for songs with wide reach
            reach_threshold = df['Spotify Playlist Reach'].quantile(0.75)
            input_text = "I'm looking for songs with extensive playlist reach that many people are discovering."
            
            # Find songs with high playlist reach
            high_reach_songs = df[df['Spotify Playlist Reach'] >= reach_threshold].copy()
            if len(high_reach_songs) == 0:
                continue
                
            # Select a random song with high reach
            target_song = high_reach_songs.sample(1).iloc[0]
            
            # Format the reach number for easier reading
            reach_formatted = f"{target_song['Spotify Playlist Reach']/1000000:.1f} million"
            
            output_text = f"'{target_song['Track']}' by {target_song['Artist']} has a playlist reach of {reach_formatted} listeners. It's featured in approximately {target_song['Spotify Playlist Count']:.0f} playlists, giving it excellent visibility."
            
        elif pattern == "combined_criteria":
            # Random artist
            artist = random.choice(popular_artists)
            
            # Request with multiple criteria
            input_text = f"I want a popular song by {artist} with high playlist presence."
            
            # Find this artist's songs
            artist_tracks = [song for song in artist_songs[artist]]
            if not artist_tracks:
                continue
                
            # Sort by combination of popularity and playlist count
            scored_tracks = []
            for song in artist_tracks:
                # Skip songs with missing data
                if pd.isna(song['Spotify Popularity']) or pd.isna(song['Spotify Playlist Count']):
                    continue
                    
                popularity_score = float(song['Spotify Popularity'])
                playlist_score = float(song['Spotify Playlist Count'])
                # Normalize playlist count to 0-100 scale approximately
                playlist_score_norm = min(100, playlist_score / 3000)
                combined_score = (popularity_score + playlist_score_norm) / 2
                scored_tracks.append((combined_score, song))
            
            if not scored_tracks:
                continue
                
            # Sort by combined score
            scored_tracks.sort(key=lambda x: x[0], reverse=True)
            target_song = scored_tracks[0][1]
            
            output_text = f"For {artist} fans seeking popular tracks with good playlist presence, '{target_song['Track']}' stands out with a popularity score of {target_song['Spotify Popularity']:.0f} and appears in {target_song['Spotify Playlist Count']:.0f} playlists."
            
        elif pattern == "similar_to":
            # Random song as source
            source_song = df.sample(1).iloc[0]
            input_text = f"Recommend something similar to '{source_song['Track']}' by {source_song['Artist']}."
            
            # Find a similar song by a different artist
            target_df = df[df['Artist'] != source_song['Artist']]
            if len(target_df) == 0:
                continue
            
            # Calculate similarity based on track attributes
            numeric_attrs = ['Spotify Popularity', 'Track Score', 'Spotify Playlist Count']
            available_attrs = [attr for attr in numeric_attrs 
                              if pd.notna(source_song[attr])]
            
            if not available_attrs:
                continue
                
            # Simple similarity calculation
            similarities = []
            for _, row in target_df.iterrows():
                total_diff = 0
                count = 0
                for attr in available_attrs:
                    if pd.notna(row[attr]):
                        # Normalize the difference based on the range of values
                        attr_max = df[attr].max()
                        attr_min = df[attr].min()
                        normalized_diff = abs(float(source_song[attr]) - float(row[attr])) / (attr_max - attr_min)
                        total_diff += normalized_diff
                        count += 1
                
                if count > 0:
                    similarity = 1 - (total_diff / count)
                    similarities.append((similarity, row))
            
            if not similarities:
                continue
                
            # Sort by similarity (first element of each tuple)
            similarities.sort(key=lambda x: x[0], reverse=True)
            target_song = similarities[0][1]
            
            output_text = f"If you like '{source_song['Track']}' by {source_song['Artist']}, check out '{target_song['Track']}' by {target_song['Artist']}. Both tracks have similar characteristics in terms of popularity metrics and playlist presence."
            
        elif pattern == "attribute_based":
            # Choose a random attribute to focus on
            attribute = random.choice(['Track Score', 'Spotify Popularity', 'Spotify Playlist Count'])
            attribute_label = {
                'Track Score': 'track scores',
                'Spotify Popularity': 'popularity ratings',
                'Spotify Playlist Count': 'playlist inclusion'
            }[attribute]
            
            input_text = f"I prefer songs with high {attribute_label}."
            
            # Get top songs by this attribute (removing NaN values first)
            filtered_df = df.dropna(subset=[attribute])
            if len(filtered_df) == 0:
                continue
                
            top_songs = filtered_df.sort_values(by=attribute, ascending=False).head(20)
            if len(top_songs) == 0:
                continue
                
            target_song = top_songs.sample(1).iloc[0]
            
            # Format the attribute value for the explanation
            attribute_value = target_song[attribute]
            if attribute == 'Spotify Playlist Count':
                attribute_display = f"{attribute_value:.0f} playlists"
            elif attribute == 'Track Score':
                attribute_display = f"{attribute_value:.1f}"
            else:
                attribute_display = f"{attribute_value:.0f}/100"
            
            output_text = f"Based on your preference for high {attribute_label}, I recommend '{target_song['Track']}' by {target_song['Artist']}. It has an impressive {attribute_label.split()[0]} of {attribute_display}."
            
        elif pattern == "rank_based":
            input_text = "I'm interested in top-ranked songs on the charts."
            
            try:
                # Get songs ranked in top 50
                # Convert to numeric first and handle errors
                df['Rank_Numeric'] = pd.to_numeric(df['All Time Rank'], errors='coerce')
                top_ranked = df[df['Rank_Numeric'] <= 50].dropna(subset=['Rank_Numeric'])
                if len(top_ranked) == 0:
                    # If no songs in top 50, try top 100
                    top_ranked = df[df['Rank_Numeric'] <= 100].dropna(subset=['Rank_Numeric'])
                    if len(top_ranked) == 0:
                        continue
                    
                target_song = top_ranked.sample(1).iloc[0]
            except Exception:
                # Fallback to simpler approach if there are issues
                try:
                    top_ranked = df.head(50)
                    target_song = top_ranked.sample(1).iloc[0]
                except Exception:
                    continue
            
            output_text = f"'{target_song['Track']}' by {target_song['Artist']} is ranked #{target_song['All Time Rank']} on the charts with a track score of {target_song['Track Score']:.1f}. It's one of the most successful songs in the dataset."
        
        # Append the training pair to our list
        training_pairs.append({
            "input": input_text,
            "output": output_text
        })
    
    # Save the training pairs as JSONL
    print(f"Saving {len(training_pairs)} training pairs to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w') as f:
        for pair in training_pairs:
            f.write(json.dumps(pair) + '\n')
            
    print(f"Training pairs saved successfully to {OUTPUT_FILE}")
    print("\nHere are 5 example training pairs:")
    for i, pair in enumerate(random.sample(training_pairs, min(5, len(training_pairs)))):
        print(f"\nExample {i+1}:")
        print(f"Input: {pair['input']}")
        print(f"Output: {pair['output']}")

if __name__ == "__main__":
    generate_training_pairs()
