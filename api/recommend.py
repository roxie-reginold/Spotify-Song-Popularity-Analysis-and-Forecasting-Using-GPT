import os
import json
import requests
import random
import time
from http.server import BaseHTTPRequestHandler

# Simplified function to query Gemini API directly with HTTP requests
def query_gemini(user_input):
    """Query Gemini API with minimal dependencies"""
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return "Error: Missing API key"
            
        # Add a cache buster with random number and timestamp
        cache_buster = f"{random.randint(1, 100000)}_{int(time.time())}"
        
        # Create prompt
        prompt = f"""
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
        
        # Create request payload for Gemini API
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.8,
                "maxOutputTokens": 1024,
                "topP": 0.9,
                "topK": 40
            }
        }
        
        # Send request to Gemini API
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-001:generateContent?key={api_key}",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        # Check if request was successful
        if response.status_code == 200:
            result = response.json()
            # Extract text from response
            try:
                content = result["candidates"][0]["content"]
                parts = content["parts"]
                recommendation_text = parts[0]["text"].strip()
                return recommendation_text
            except (KeyError, IndexError) as e:
                return f"Error parsing response: {str(e)}"
        else:
            return f"API Error: {response.status_code} - {response.text}"
    
    except Exception as e:
        return f"Error: {str(e)}"

# Vercel serverless handler
class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()
    
    def do_POST(self):
        try:
            # Get content length
            content_length = int(self.headers['Content-Length'])
            # Read and parse request body
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            # Get user input
            user_input = request_data.get('user_input')
            
            # Validate input
            if not user_input:
                self._send_json_response(400, {"error": "Missing 'user_input' in request"})
                return
            
            # Query Gemini
            recommendation = query_gemini(user_input)
            
            # Send response
            self._send_json_response(200, {"recommendation": recommendation})
        
        except Exception as e:
            self._send_json_response(500, {"error": str(e)})
    
    def _send_json_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
