import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Please set GEMINI_API_KEY in your .env file.")

# Configure the Gemini API
genai.configure(api_key=API_KEY)

# Optional: Function to get a Gemini model
def get_model(model_name="gemini-1.5-flash"):
    return genai.GenerativeModel(model_name=model_name)
