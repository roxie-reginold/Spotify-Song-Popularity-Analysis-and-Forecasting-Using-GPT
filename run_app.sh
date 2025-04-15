#!/bin/bash
# Simple script to run the Spotify Recommendation App

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Activated virtual environment..."
else
    echo "No virtual environment found. Consider creating one with: python -m venv venv"
fi

# Start the backend server in the background
echo "Starting backend server on port 8006..."
python llm_endpoint.py &
BACKEND_PID=$!

# Wait for backend to initialize
sleep 3

# Start the Streamlit frontend
echo "Starting Streamlit frontend..."
streamlit run app.py

# When Streamlit is closed, clean up the backend process
echo "Cleaning up..."
kill $BACKEND_PID
