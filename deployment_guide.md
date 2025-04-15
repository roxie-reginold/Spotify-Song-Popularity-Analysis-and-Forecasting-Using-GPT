# Spotify Recommendation App - Deployment Guide

This guide provides step-by-step instructions for deploying your Spotify recommendation app. We'll use Render for the backend API and Streamlit Cloud for the frontend.

## Prerequisites

- GitHub account
- [Render account](https://render.com/) (free tier available)
- [Streamlit Cloud account](https://streamlit.io/cloud) (free tier available)
- Spotify Developer and Google Gemini API credentials

## Part 1: Deploy the Backend API to Render

1. **Push your code to GitHub**
   - Ensure your repository is up-to-date on GitHub

2. **Sign up for Render**
   - Create an account at [render.com](https://render.com/)

3. **Create a new Web Service**
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository
   - Configure the service:
     - Name: `spotify-recommendation-api`
     - Runtime: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn llm_endpoint:app`
     - Select the Free plan

4. **Set Environment Variables**
   - In Render dashboard, go to your web service
   - Click on "Environment" tab
   - Add the following variables:
     - `GEMINI_API_KEY`: Your Google Gemini API key
     - `SPOTIFY_CLIENT_ID`: Your Spotify Client ID
     - `SPOTIFY_CLIENT_SECRET`: Your Spotify Client Secret
     - `FLASK_DEBUG`: `False` (for production)

5. **Deploy the Service**
   - Render will automatically deploy your service
   - Note the URL of your service (e.g., `https://spotify-recommendation-api.onrender.com`)
   - Test the endpoint by visiting `https://your-render-url/` in your browser

## Part 2: Deploy the Frontend to Streamlit Cloud

1. **Sign up for Streamlit Cloud**
   - Create an account at [streamlit.io/cloud](https://streamlit.io/cloud)

2. **Deploy Your App**
   - Click "New app"
   - Connect your GitHub repository
   - Configure the app:
     - Repository: Select your GitHub repository
     - Branch: `main`
     - Main file path: `app.py`
     - Advanced settings: 
       - Python version: 3.9

3. **Set Environment Variables**
   - In your Streamlit app settings, go to "Secrets"
   - Add the following variables in TOML format:
   ```toml
   BACKEND_URL = "https://your-render-url/recommend"
   SPOTIFY_CLIENT_ID = "your-spotify-client-id"
   SPOTIFY_CLIENT_SECRET = "your-spotify-client-secret"
   ```

4. **Deploy the App**
   - Streamlit Cloud will automatically deploy your app
   - Click "Save" and "Deploy"
   - Wait for the deployment to complete
   - Your app will be available at a URL like `https://your-app-name.streamlit.app`

## Testing the Deployed Application

1. Visit your Streamlit app URL
2. Enter a music preference
3. Click "Get Recommendation"
4. You should see a recommendation with Spotify integration

## Troubleshooting

- **CORS Issues**: Ensure the CORS configuration in `llm_endpoint.py` is correct
- **Connection Errors**: Verify the `BACKEND_URL` is correctly set in Streamlit
- **API Key Issues**: Double-check all API keys and credentials
- **Deployment Fails**: Check the logs in Render or Streamlit Cloud for errors

## Monitoring and Maintenance

- **Render Dashboard**: Monitor your backend API usage and logs
- **Streamlit Cloud**: Check app analytics and performance
- **API Limits**: Be aware of free tier limits on both platforms

## Cost Considerations

- Render's free tier includes 750 hours of service per month
- Streamlit Cloud offers free public apps with some limitations
- Both Gemini AI and Spotify API have usage limitations on free tiers
