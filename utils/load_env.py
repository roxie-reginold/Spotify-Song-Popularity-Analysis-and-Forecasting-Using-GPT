import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Print confirmation that environment variables are loaded
print("Environment variables loaded from .env file")

# Check if essential variables are set
spotify_vars = ["SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET", 
                "SPOTIFY_REDIRECT_URI", "SPOTIFY_SCOPE"]
openai_var = "GEMINI_API_KEY"

# Display status of required variables
for var in spotify_vars:
    if os.getenv(var):
        print(f"✓ {var} is set")
    else:
        print(f"✗ {var} is missing or empty")

if os.getenv(openai_var):
    print(f"✓ {openai_var} is set")
else:
    print(f"✗ {openai_var} is missing or empty")
