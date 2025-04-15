# Spotify Recommendation App - Project Structure

This document outlines the clean project structure after organization.

## Core Application Files

- `app.py` - Streamlit frontend for the recommendation system
- `llm_endpoint.py` - Flask backend server with Gemini AI integration
- `spotify_utils.py` - Spotify API utilities for track lookups and album art
- `.env` - Environment variables and configuration

## Analysis & Data

- `analysis/` - Folder containing data analysis materials
  - `notebooks/` - Jupyter notebooks with Spotify data analysis
  - `data/` - Raw datasets used for analysis

## Training Data 

- `data/training/` - Training datasets for fine-tuning recommendation models

## Utilities

- `utils/` - Helper scripts and utilities

## Removed/Archived Files

The following test/utility files were identified as not essential for the core application:

- `list_gemini_models.py` - Test script for listing available Gemini models
- `convert_notebook.py` - Utility for notebook conversion

## Running the Application

1. Start the backend server: `python llm_endpoint.py`
2. Start the Streamlit app: `streamlit run app.py`
