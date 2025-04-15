#!/usr/bin/env python3
"""
Spotify Song Popularity Analysis

This script analyzes Spotify song popularity data using a streamlined dataset
that includes essential metrics and genre information.

Data source: Spotify streaming data with genre enrichment
"""

# All necessary imports
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setting for better visualizations
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)

INPUT_DATASET = 'Spotify_Analysis_Ready.csv'

# Load the streamlined dataset
print("Loading streamlined dataset...")
df = pd.read_csv(INPUT_DATASET)

# Display basic information about the dataset
print("Dataset overview:")
print(f"Total songs: {len(df)}")
print(f"Columns: {', '.join(df.columns.tolist())}")

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset information:")
print(df.info())

print("\nDescriptive statistics for numeric columns:")
print(df.describe())

# Analyze popularity metrics
print("\n=== Popularity Analysis ===")

# Top artists by playlist reach
artist_reach = df.groupby('Artist')['Spotify Playlist Reach'].sum().sort_values(ascending=False)
print("\nTop 10 Artists by Playlist Reach:")
print(artist_reach.head(10))

# Most streamed songs (by playlist count as a proxy)
most_playlisted_songs = df.nlargest(5, 'Spotify Playlist Count')
print("\nTop 5 Most Playlisted Songs:")
print(most_playlisted_songs[['Track', 'Artist', 'Spotify Playlist Count']])

# Most popular songs by Spotify Popularity
most_popular_songs = df.nlargest(5, 'Spotify Popularity')
print("\nTop 5 Most Popular Songs by Spotify Popularity:")
print(most_popular_songs[['Track', 'Artist', 'Spotify Popularity', 'Genres']])

# Genre analysis
print("\n=== Genre Analysis ===")

# Extract and count genres
def extract_genres(genre_string):
    """Extract individual genres from comma-separated genre strings"""
    if pd.isna(genre_string) or genre_string == 'Unknown':
        return []
    
    # Handle different possible formats in the CSV
    try:
        # Remove any quotes and split by comma
        clean_string = genre_string.replace('"', '')
        genres = [g.strip() for g in clean_string.split(',') if g.strip()]
        return genres
    except Exception:
        # Fallback for any parsing issues
        return []

# Create a list of all genres
all_genres = []
for genres_str in df['Genres'].dropna():
    try:
        genres = extract_genres(genres_str)
        all_genres.extend(genres)
    except (IndexError, AttributeError):
        # Handle possible format issues in genre strings
        continue

# Count genre frequency
genre_counts = pd.Series(all_genres).value_counts()

print("\nTop 10 Most Common Genres:")
print(genre_counts.head(10))

# Calculate average popularity by genre
print("\nAverage Popularity by Top Genres:")

genre_popularity = {}
genre_songs = {}

# Iterate through each song and its genres
for _, row in df.iterrows():
    if pd.notna(row['Genres']) and row['Genres'] != 'Unknown' and pd.notna(row['Spotify Popularity']):
        try:
            genres_list = extract_genres(row['Genres'])
            for genre in genres_list:
                if genre not in genre_popularity:
                    genre_popularity[genre] = 0
                    genre_songs[genre] = 0
                genre_popularity[genre] += row['Spotify Popularity']
                genre_songs[genre] += 1
        except (IndexError, AttributeError):
            continue

# Calculate averages
genre_avg_popularity = {genre: genre_popularity[genre] / genre_songs[genre] 
                       for genre in genre_popularity if genre_songs[genre] > 0}

# Convert to Series and sort
genre_avg_popularity = pd.Series(genre_avg_popularity).sort_values(ascending=False)

# Filter to only include genres with at least 3 songs for more reliable data
popular_genres = genre_avg_popularity[pd.Series(genre_songs) >= 3]

print(popular_genres.head(10))

# Visualization functions
def create_visualizations():
    """Create visualizations for the Spotify data analysis"""
    try:
        print("\n=== Creating Visualizations ===")
        
        # Create a directory for visualizations if it doesn't exist
        os.makedirs('visualizations', exist_ok=True)
        
        # 1. Popularity Distribution
        plt.figure(figsize=(10, 6))
        sns.histplot(df['Spotify Popularity'].dropna(), kde=True, bins=20)
        plt.title('Distribution of Spotify Song Popularity')
        plt.xlabel('Popularity Score')
        plt.ylabel('Number of Songs')
        plt.savefig('visualizations/popularity_distribution.png')
        plt.close()
        print("Created: popularity_distribution.png")
        
        # 2. Top Genres Bar Chart (top 10)
        if len(genre_counts) > 0:
            plt.figure(figsize=(12, 8))
            genre_counts.head(10).plot(kind='bar')
            plt.title('Top 10 Most Common Genres')
            plt.xlabel('Genre')
            plt.ylabel('Number of Songs')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig('visualizations/top_genres.png')
            plt.close()
            print("Created: top_genres.png")
        
        # 3. Genre Popularity Comparison
        if len(popular_genres) > 0:
            plt.figure(figsize=(12, 8))
            popular_genres.head(10).plot(kind='bar')
            plt.title('Average Popularity Score by Genre')
            plt.xlabel('Genre')
            plt.ylabel('Average Popularity Score')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig('visualizations/genre_popularity.png')
            plt.close()
            print("Created: genre_popularity.png")
        
        # 4. Playlist Count vs. Popularity Scatter Plot
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='Spotify Playlist Count', y='Spotify Popularity', 
                        hue='All Time Rank', size='Track Score',
                        sizes=(20, 200), alpha=0.7, data=df.head(100))
        plt.title('Relationship Between Playlist Count and Popularity (Top 100 Songs)')
        plt.xlabel('Number of Playlists')
        plt.ylabel('Popularity Score')
        plt.legend(title='Rank', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig('visualizations/playlist_vs_popularity.png')
        plt.close()
        print("Created: playlist_vs_popularity.png")
        
        # 5. Top 20 Songs by Rank
        try:
            top_20 = df.head(20)
            plt.figure(figsize=(14, 10))
            sns.barplot(x='Spotify Popularity', y='Track', data=top_20)
            plt.title('Top 20 Songs and Their Popularity')
            plt.xlabel('Popularity Score')
            plt.ylabel('')
            plt.tight_layout()
            plt.savefig('visualizations/top20_songs.png')
            plt.close()
            print("Created: top20_songs.png")
        except Exception as e:
            print(f"Error creating top 20 visualization: {e}")
        
        print("Visualizations created successfully in the 'visualizations' directory")
        
    except Exception as e:
        print(f"Error creating visualizations: {e}")

# Run the visualizations
create_visualizations()

# Final insights summary
print("\n=== Summary of Insights ===")
print("1. Top Artists: The dataset shows that certain artists dominate in playlist reach")
if len(genre_counts) > 0:
    print(f"2. Popular Genres: {', '.join(genre_counts.index[:3])} are the most common genres")
if len(popular_genres) > 0:
    print(f"3. Highest Average Popularity: {popular_genres.index[0]} with score of {popular_genres.iloc[0]:.2f}")
print("4. Top Songs: The most popular songs maintain high playlist counts and popularity scores")
print("\nFull analysis complete. Check the 'visualizations' directory for visual insights.")

# Set up the Gemini API with key from environment variables
try:
    # First try with the GEMINI_API_KEY environment variable
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if gemini_api_key:
        # Set the environment variable that the Google API is looking for
        os.environ['GOOGLE_API_KEY'] = gemini_api_key
        genai.configure(api_key=gemini_api_key)
        
        # Get top genre for analysis
        top_genre = genre_counts.index[0] if not genre_counts.empty else 'pop'
        
        # Using Google's Gemini API for genre-based recommendations
        print(f"\nGenerating song recommendation for {top_genre} genre using Gemini AI...")
        # Use a valid Gemini model from our available models list
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        prompt = f"""Based on the current popularity of the {top_genre} genre, recommend a song released in 2024 in this format:
        Song: [Song Name]
        Artist: [Artist Name]
        Why it's trending: [Brief explanation]
        
        Be specific about why this song is trending in the {top_genre} genre."""
        
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 150,
                "temperature": 0.7
            }
        )
        
        print("\nGemini AI Genre-Based Recommendation:")
        print(response.text)
    else:
        print("\nGemini API Key not found in environment variables.")
        print("Please set GEMINI_API_KEY in your .env file.")
        
except Exception as e:
    print(f"\nError generating recommendation with Gemini: {e}")
    print("You may need to check your Gemini API key in the .env file.")

