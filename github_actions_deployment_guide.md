# Deploying Your Spotify Recommendation App with GitHub Actions

This guide explains how to use the GitHub Actions workflows to automatically deploy your Spotify recommendation application when you push changes to your repository.

## Setup Overview

I've created three key files for your GitHub Actions deployment:

1. `.github/workflows/backend-deploy.yml` - Deploys your Flask backend to Render
2. `.github/workflows/frontend-deploy.yml` - Deploys your Streamlit frontend to Streamlit Cloud
3. `.streamlit/config.toml` - Configuration for your Streamlit app with Spotify-themed styling

## Prerequisites

Before these workflows will work, you need to:

1. Create accounts on:
   - [Render](https://render.com/)
   - [Streamlit Cloud](https://streamlit.io/cloud)

2. Deploy manually first:
   - Deploy your backend API to Render initially (use the Dockerfile provided)
   - Deploy your app to Streamlit Cloud manually the first time

3. Get API credentials:
   - Get your Render service ID and API key
   - Get your Streamlit app ID and deployment token

## Setting Up GitHub Secrets

Add the following secrets to your GitHub repository:

1. Go to your repository → Settings → Secrets and variables → Actions → New repository secret

2. Add these secrets:
   - `RENDER_SERVICE_ID` - Found in your Render dashboard URL
   - `RENDER_API_KEY` - Generated in your Render account settings
   - `STREAMLIT_APP_ID` - Found in your Streamlit dashboard
   - `STREAMLIT_DEPLOY_TOKEN` - Create a deployment token in Streamlit settings

## How the GitHub Actions Work

### Backend Deployment

When you push changes to any of these files:
- `llm_endpoint.py`
- `requirements.txt`
- `Dockerfile`
- `spotify_utils.py`

The backend workflow will:
1. Trigger a new deployment on Render
2. Wait for the deployment to complete
3. Report the deployment status

### Frontend Deployment

When you push changes to any of these files:
- `app.py`
- `spotify_utils.py`
- `requirements.txt`
- `.streamlit/*` files

The frontend workflow will:
1. Set up Python environment
2. Trigger a redeployment on Streamlit Cloud
3. Report the deployment status

## Testing Your GitHub Actions

After setting up the secrets:

1. Make a small change to `app.py` or `llm_endpoint.py`
2. Commit and push to your repository
3. Go to the "Actions" tab in your GitHub repository
4. Watch your workflows run

## Environment Variables

Remember that you still need to configure environment variables in both platforms:

### Render Environment Variables:
- `GEMINI_API_KEY`
- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`
- `FLASK_DEBUG` (set to False for production)

### Streamlit Cloud Secrets:
Create a secrets section with:
```toml
BACKEND_URL = "https://your-render-backend-url/recommend"
SPOTIFY_CLIENT_ID = "your-spotify-client-id"
SPOTIFY_CLIENT_SECRET = "your-spotify-client-secret"
```

## Troubleshooting

If your workflows fail:

1. Check the logs in the GitHub Actions tab
2. Verify your secrets are correctly set
3. Ensure you've done the initial manual deployments
4. Check that your Render and Streamlit accounts have the correct permissions

## Maintenance

- Monitor your workflows in the GitHub Actions tab
- Check Render and Streamlit dashboards for service health
- Update your GitHub secrets if your API keys change
