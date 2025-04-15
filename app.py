import streamlit as st
import requests
import json
import re
from dotenv import load_dotenv
from spotify_utils import get_spotify_track_link

# Load environment variables
load_dotenv()

# Configure backend endpoint URL
# Hardcode to port 8006 to match our running backend
BACKEND_URL = "http://localhost:8006/recommend"

# Print the backend URL for debugging
print(f"Backend URL: {BACKEND_URL}")

# Page configuration
st.set_page_config(
    page_title="Spotify Song Recommendation",
    page_icon="🎵",
    layout="wide"
)

# App header with styling
st.title("🎵 Spotify Song Recommendation System")
st.markdown("""
<style>
.stApp {
    background-color: #1E1E1E;
    color: #FFFFFF;
}
.css-1d391kg, .css-1wbqy5l {
    background-color: #2C2C2C;
}
</style>
""", unsafe_allow_html=True)

st.write("Discover new music based on your preferences using our AI-powered recommendation engine.")

# Sidebar for additional options - more minimal
with st.sidebar:
    st.header("About")
    st.info(
        "This app uses AI to provide personalized song recommendations based on your preferences."
    )
    
    st.subheader("Example Queries")
    st.markdown("- *I enjoy tracks with high energy and danceable beats*")
    st.markdown("- *Songs similar to 'Blinding Lights' by The Weeknd*")
    st.markdown("- *Looking for acoustic folk with female vocals*")

# Main content area - using full width now
with st.container():
    # Input section
    st.subheader("What kind of music are you looking for?")
    user_input = st.text_area(
        "Describe your music preferences or a song you enjoy:",
        height=100,
        placeholder="E.g., I like upbeat pop songs with female vocals similar to Taylor Swift"
    )
    
    # Recommendation button
    if st.button("Get Recommendation", type="primary"):
        if user_input:
            with st.spinner("Generating recommendations..."): 
                try:
                    # Prepare payload and headers
                    payload = {"user_input": user_input}
                    headers = {"Content-Type": "application/json"}
                    
                    # Make the POST request to the recommendation endpoint - without displaying debug info
                    try:
                        response = requests.post(BACKEND_URL, json=payload, headers=headers, timeout=10)
                        
                        if response.status_code == 200:
                            data = response.json()
                            recommendation_text = data.get("recommendation", "No recommendation found.")
                            
                            # Parse the recommendation text to extract song, artist, and explanation
                            song_name = None
                            artist_name = None
                            explanation = None
                                                    # Try to extract structured data from the recommendation text without showing errors
                            try:
                                import re
                                # Look for Song: and Artist: patterns
                                song_match = re.search(r'Song:\s*"?([^"\n]+)"?', recommendation_text)
                                artist_match = re.search(r'Artist:\s*([^\n]+)', recommendation_text)
                                explanation_match = re.search(r'Explanation:\s*([^\n].+(?:\n.+)*)', recommendation_text, re.DOTALL)
                                
                                if song_match:
                                    song_name = song_match.group(1).strip()
                                if artist_match:
                                    artist_name = artist_match.group(1).strip()
                                if explanation_match:
                                    explanation = explanation_match.group(1).strip()
                                else:
                                    # If no Explanation: pattern, take everything after Artist: as explanation
                                    parts = recommendation_text.split("Artist:")
                                    if len(parts) > 1:
                                        remaining = parts[1].split("\n", 1)
                                        if len(remaining) > 1:
                                            explanation = remaining[1].strip()
                            except Exception:
                                # Silent error handling without warnings
                                explanation = recommendation_text
                            
                            # Display the recommendation in an appealing format without extra messages
                            
                            # Parse the recommendation to extract song and artist info
                            song_name = None
                            artist_name = None
                            explanation = None
                            
                            # Extract song and artist using regex patterns
                            song_match = re.search(r'Song:\s*([^\n]+)', recommendation_text)
                            artist_match = re.search(r'Artist:\s*([^\n]+)', recommendation_text)
                            explanation_match = re.search(r'Explanation:\s*([^\n].+(?:\n.+)*)', recommendation_text, re.DOTALL)
                            
                            if song_match:
                                song_name = song_match.group(1).strip()
                            if artist_match:
                                artist_name = artist_match.group(1).strip()
                            if explanation_match:
                                explanation = explanation_match.group(1).strip()
                            
                            # Try to get Spotify link if we have song and artist information
                            spotify_data = None
                            if song_name and artist_name:
                                spotify_data = get_spotify_track_link(song_name, artist_name)
                                if not spotify_data.get('success'):
                                    # Try with just the song name if artist search fails
                                    spotify_data = get_spotify_track_link(song_name)
                            
                            # Create the recommendation display
                            if spotify_data and spotify_data.get('success'):
                                # Display with Spotify data including album art
                                col1, col2 = st.columns([1, 3])
                                
                                with col1:
                                    # Display album art from Spotify
                                    st.image(spotify_data['album_cover_url'], width=150)
                                
                                with col2:
                                    # Display song info with Spotify link
                                    st.markdown(f"""
                                    <div style='background-color:#2C2C2C; padding:20px; border-radius:10px;'>
                                        <h2 style='color:#1DB954; margin-bottom:10px;'>{spotify_data['track_name']}</h2>
                                        <h3 style='color:#CCCCCC; margin-bottom:20px;'>by {spotify_data['artist_name']}</h3>
                                        <p><a href='{spotify_data['track_url']}' target='_blank' style='color:#1DB954;'>Listen on Spotify</a></p>
                                        <div style='height:2px; background-color:#333333; margin:15px 0;'></div>
                                        <p style='color:#FFFFFF;'>{explanation if explanation else 'No explanation available.'}</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    # Display album info
                                    st.caption(f"Album: {spotify_data['album_name']}")
                            else:
                                # Fallback to just showing the recommendation text without Spotify data
                                st.markdown(f"""
                                <div style='background-color:#2C2C2C; padding:20px; border-radius:10px;'>
                                    <p style='color:#FFFFFF; white-space: pre-wrap;'>{recommendation_text}</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                if spotify_data and not spotify_data.get('success'):
                                    st.caption(f"Note: {spotify_data.get('error')}")
                    except requests.exceptions.ConnectionError as e:
                        st.error(f"Connection error: {e}")
                        raise
                    
                    # Only show error for non-200 status codes
                    if response.status_code != 200:
                        st.error(f"Error: {response.status_code} - {response.text}")
                        
                    # Removed the 'Get Another Recommendation' button to avoid extra UI elements
                except requests.exceptions.ConnectionError:
                    st.error("Connection Error: Unable to connect to the recommendation server. Please make sure the backend server is running.")
                    st.info("If running locally, start the backend with: `python llm_endpoint.py`")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter your music preferences to get recommendations.")

# Removed the 'Top Spotify Songs' table section

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Powered by Spotify API and Gemini AI</div>", 
    unsafe_allow_html=True
)
