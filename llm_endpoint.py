#!/usr/bin/env python3
"""
LLM Endpoint for Spotify Song Recommendation System

This server provides an API endpoint that connects to the fine-tuned Gemini model
for Spotify song recommendations. It receives user queries and returns personalized
song recommendations based on the fine-tuned model's responses.
"""

import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Set up Vertex AI model configuration
PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION")
MODEL_ID = os.getenv("MODEL_ID")

# Get the endpoint URL from .env file
MODEL_ENDPOINT_URL = os.getenv("MODEL_ENDPOINT_URL")
if not MODEL_ENDPOINT_URL:
    raise ValueError("MODEL_ENDPOINT_URL not set in .env file")

if not (PROJECT_ID and LOCATION and MODEL_ID):
    raise ValueError("PROJECT_ID, LOCATION, and MODEL_ID environment variables must be set for Vertex AI.")

# Request parameters
REQUEST_PARAMS = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "maxOutputTokens": 300,
}

def query_gemini(user_input):
    """
    Query the Gemini 2.0 Flash model with user input to get song recommendations
    
    Args:
        user_input (str): User's music preference or query
        
    Returns:
        str: The song recommendation with explanation
    """
    import json
    import random
    import time
    import google.generativeai as genai
    
    try:
        # Log request parameters for debugging
        print(f"User query: {user_input}")
        print(f"API Key: {GEMINI_API_KEY[:5]}...")
        
        # Generation parameters
        generation_config = {
            "temperature": REQUEST_PARAMS["temperature"],
            "max_output_tokens": REQUEST_PARAMS["maxOutputTokens"],
            "top_k": REQUEST_PARAMS["top_k"],
            "top_p": REQUEST_PARAMS["top_p"]
        }
        
        print(f"Generation config: {json.dumps(generation_config, indent=2)}")
        
        # Configure the Gemini API with your API key
        print("Setting up Gemini client...")
        genai.configure(api_key=GEMINI_API_KEY)
        
        # List available models to confirm Gemini 2.0 Flash is available
        print("Available models:")
        for model in genai.list_models():
            if "gemini-2.0-flash" in model.name:
                print(f"- {model.name} ✓")
            else:
                print(f"- {model.name}")
        
        # Add a cache buster with random number and timestamp to prevent caching
        cache_buster = f"{random.randint(1, 100000)}_{int(time.time())}"
        
        # Customize the prompt to get better song recommendations in a specific format
        enhanced_prompt = f"""
        You are a music recommendation system that specializes in Spotify songs.
        Based on the following music preference, recommend a relevant song with artist name and explanation.
        
        User preference: {user_input}
        
        Session ID: {cache_buster}
        
        IMPORTANT: Each time you're asked, give a DIFFERENT song recommendation. 
        Vary your responses even for identical queries.
        
        EXTREMELY IMPORTANT: You must respond in EXACTLY this format with these exact line breaks:
        
        Okay, based on your preference, I recommend:
        
        Song: [Song Name]
        
        Artist: [Artist Name]
        
        Explanation: [Detailed explanation of why this song matches their preference]
        
        DO NOT combine Song and Artist on the same line. Each must be on its own line.
        DO NOT change this format in any way.
        """
        
        # Initialize Gemini 2.0 Flash model
        model = genai.GenerativeModel('gemini-2.0-flash-001')
        
        print("Sending request to Gemini 2.0 Flash API...")
        
        # Generate content using the model with higher temperature for more variety
        response = model.generate_content(
            enhanced_prompt,
            generation_config=genai.types.GenerationConfig(
                # Use a slightly higher temperature to encourage diverse results
                temperature=max(REQUEST_PARAMS["temperature"], 0.8),  # Ensure minimum temperature of 0.8 for variety
                max_output_tokens=REQUEST_PARAMS["maxOutputTokens"],
                top_k=REQUEST_PARAMS["top_k"],
                top_p=REQUEST_PARAMS["top_p"]
            )
        )
        
        print(f"Received response: {response}")
        
        # Process the response
        print(f"Response type: {type(response)}")
        print(f"Response: {response}")
        
        # Extract text content from the response
        try:
            if hasattr(response, 'text'):
                # Get the text directly from the response
                recommendation = response.text.strip()
                print(f"Response text: {recommendation}")
                return recommendation
            elif hasattr(response, 'parts'):
                # Extract text from parts
                text_parts = []
                for part in response.parts:
                    if hasattr(part, 'text') and part.text:
                        text_parts.append(part.text)
                if text_parts:
                    recommendation = '\n'.join(text_parts)
                    return recommendation
            elif hasattr(response, 'candidates'):
                # Try to get content from candidates
                candidates = response.candidates
                if candidates and len(candidates) > 0:
                    first_candidate = candidates[0]
                    if hasattr(first_candidate, 'content'):
                        content = first_candidate.content
                        if hasattr(content, 'parts'):
                            text_parts = []
                            for part in content.parts:
                                if hasattr(part, 'text') and part.text:
                                    text_parts.append(part.text)
                            if text_parts:
                                return '\n'.join(text_parts)
            
            # If we couldn't extract text through any of the methods above
            return str(response)
        except Exception as e:
            print(f"Error processing response: {e}")
            return f"Error extracting recommendation: {str(e)}. Please try again."
    
    except Exception as e:
        import traceback
        print(f"Error details: {traceback.format_exc()}")
        raise Exception(f"Gemini API error: {str(e)}")

@app.route('/recommend', methods=['POST'])
def recommend():
    """
    API endpoint to get song recommendations based on user input
    
    Expects JSON with format: {"user_input": "user's query string"}
    Returns JSON with format: {"recommendation": "recommendation text"}
    """
    try:
        # Get request data
        data = request.get_json()
        user_input = data.get("user_input")
        
        # Validate input
        if not user_input:
            return jsonify({"error": "Missing 'user_input' in request"}), 400

        # Query the Gemini model for a recommendation
        recommendation = query_gemini(user_input)
        return jsonify({"recommendation": recommendation}), 200
    
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.environ.get("PORT", 8006))  # Changed to port 8006 to avoid conflicts
    
    # Run the app
    print(f"Starting Spotify Recommendation server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=True)
