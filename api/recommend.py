import os
import json
import sys
import random
import time

# Add the parent directory to the path so imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import google.generativeai as genai
from flask import Flask, request, jsonify, Response
from dotenv import load_dotenv
from spotify_utils import get_spotify_track_link

# Load environment variables
load_dotenv()

# Get API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Set up Vertex AI model configuration
REQUEST_PARAMS = {
    'temperature': 0.8,
    'maxOutputTokens': 1024,
    'top_p': 0.9,
    'top_k': 40,
}

def query_gemini(user_input):
    """
    Query the Gemini 2.0 Flash model with user input to get song recommendations
    
    Args:
        user_input (str): User's music preference or query
        
    Returns:
        str: The song recommendation with explanation
    """
    try:
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
        
        # Extract text content from the response
        try:
            recommendation_text = response.text.strip()
            return recommendation_text
        except Exception as e:
            print(f"Error extracting text from response: {e}")
            return f"Error generating recommendation: {str(e)}"
    
    except Exception as e:
        print(f"Error in query_gemini: {e}")
        return f"Error: {str(e)}"

def handle_request(request):
    """Serverless function handler for Vercel"""
    # Handle OPTIONS requests for CORS
    if request.method == "OPTIONS":
        # Return CORS headers
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Max-Age": "3600"
        }
        return Response("", status=204, headers=headers)
    
    # Handle POST request
    if request.method == "POST":
        try:
            # Get JSON data
            data = request.get_json()
            user_input = data.get("user_input")
            
            # Validate input
            if not user_input:
                return Response(
                    json.dumps({"error": "Missing 'user_input' in request"}),
                    status=400,
                    mimetype="application/json",
                    headers={"Access-Control-Allow-Origin": "*"}
                )

            # Query the Gemini model for a recommendation
            recommendation = query_gemini(user_input)
            
            # Return the result
            return Response(
                json.dumps({"recommendation": recommendation}),
                status=200,
                mimetype="application/json",
                headers={"Access-Control-Allow-Origin": "*"}
            )
        
        except Exception as e:
            print(f"Error processing request: {e}")
            return Response(
                json.dumps({"error": str(e)}),
                status=500,
                mimetype="application/json",
                headers={"Access-Control-Allow-Origin": "*"}
            )
    
    # Handle other HTTP methods
    return Response(
        json.dumps({"error": "Method not allowed"}),
        status=405,
        mimetype="application/json",
        headers={"Access-Control-Allow-Origin": "*"}
    )

# This is the Vercel serverless function handler
def handler(request):
    return handle_request(request)
