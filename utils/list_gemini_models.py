import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure API key
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("No GOOGLE_API_KEY found in environment variables!")
    exit(1)

# Configure the Gemini API
genai.configure(api_key=api_key)

# List available models
try:
    print("Listing available Gemini models...")
    models = genai.list_models()
    
    for model in models:
        if "gemini" in model.name.lower():
            print(f"Model name: {model.name}")
            print(f"  - Display name: {model.display_name}")
            print(f"  - Description: {model.description}")
            print(f"  - Supported generation methods: {model.supported_generation_methods}")
            print("-" * 50)
            
except Exception as e:
    print(f"Error listing models: {e}")
