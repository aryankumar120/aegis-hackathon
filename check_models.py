import requests
import os
from dotenv import load_dotenv

# Load API key from your .env file
load_dotenv()

api_key = os.environ.get("GROQ_API_KEY")

# If you don't have the 'requests' library, install it with:
# pip3 install requests
if not api_key:
    print("Error: GROQ_API_KEY not found. Please check your .env file.")
else:
    url = "https://api.groq.com/openai/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an exception for bad status codes
        models = response.json()
        
        print("✅ Successfully fetched available models:\n")
        for model in models['data']:
            print(f"- {model['id']}")
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")