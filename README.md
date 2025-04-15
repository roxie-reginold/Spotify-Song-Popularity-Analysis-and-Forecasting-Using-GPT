# Spotify Song Recommendation System

A powerful AI-driven music recommendation app that uses Gemini 2.0 Flash and the Spotify API to provide personalized song suggestions.

## Features

- **AI-Powered Recommendations**: Uses Google's Gemini 2.0 Flash model to provide intelligent song recommendations
- **Spotify Integration**: Direct links to songs, album artwork, and artist information via the Spotify API
- **Clean Interface**: Modern, user-friendly design for an excellent music discovery experience
- **Consistent Output Format**: Structured recommendations with song, artist, and explanations
- **Variety**: Advanced caching prevention ensures you get different song recommendations each time

## Setup and Installation

### Prerequisites

- Python 3.8+
- Spotify Developer Account and API credentials
- Google Cloud account with Gemini API access

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd Spotify-Song-Popularity-Analysis-and-Forecasting-Using-GPT
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables in `.env`:
   ```
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   GEMINI_API_KEY=your_gemini_api_key
   ```

## Running the Application

You can use the provided shell script to start both the backend and frontend:

```
./run_app.sh
```

Or run them separately:

1. Start the backend server:
   ```
   python llm_endpoint.py
   ```

2. Start the Streamlit frontend (in a separate terminal):
   ```
   streamlit run app.py
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:8501
   ```

## Project Structure

- `app.py` - Streamlit frontend interface
- `llm_endpoint.py` - Flask backend for Gemini AI integration
- `spotify_utils.py` - Utilities for Spotify API interaction
- `utils/` - Helper scripts and utilities
- `analysis/` - Data analysis notebooks and datasets
- `data/` - Dataset files and training data
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (not in repo)

## How It Works

1. User enters their music preferences in the Streamlit frontend
2. Request is sent to the Flask backend
3. Gemini AI generates personalized song recommendations
4. Spotify API provides song details and album artwork
5. Results are displayed in an elegant, user-friendly interface

## Demo

The app provides personalized song recommendations based on user preferences:

- Enter music preferences like "upbeat dance tracks with female vocals"
- Get song recommendations with Spotify links
- View album artwork and detailed explanations of why songs match your preferences

## Credits

- Powered by [Gemini AI](https://ai.google.dev/)
- Music data from [Spotify API](https://developer.spotify.com/documentation/web-api/)

## Quick Start

1. Ensure you have completed the installation steps above
2. Start the application:
   ```bash
   ./run_app.sh
   ```
3. Open your browser to http://localhost:8501
4. Enter your music preferences and discover new songs!

## Environment Variables

Create a `.env` file with the following credentials:

```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8080
SPOTIFY_SCOPE=user-library-read
GEMINI_API_KEY=your_gemini_api_key
```

## Development

If you want to contribute to the project or modify it for your needs:

1. The core files to modify are:
   - `app.py` - Streamlit frontend
   - `llm_endpoint.py` - Flask backend
   - `spotify_utils.py` - Spotify API integration

2. To run tests or utility scripts, use the files in the `utils/` directory

3. For data analysis, check the notebooks in `analysis/notebooks/`

### Generate Training Data

```bash
python src/recommendation/generate_training_pairs.py
```

## Screenshots

![image](https://github.com/user-attachments/assets/9ee40518-d4a9-4c76-9ba5-27a787fcb869)


## Future Enhancements

- **Customizable Playlist Creation**: Save recommendations to Spotify playlists
- **User Preference Learning**: Remember user tastes for better future recommendations
- **Audio Preview**: Listen to song snippets directly in the app
- **Advanced Filtering**: Filter recommendations by tempo, genre, era, etc.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- [Spotify API](https://developer.spotify.com/documentation/web-api/) for music data and integration
- [Google Gemini AI](https://ai.google.dev/) for intelligent recommendation generation
- [Streamlit](https://streamlit.io/) for the interactive frontend
