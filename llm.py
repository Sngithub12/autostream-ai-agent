from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_text(prompt: str) -> str:
    response = client.models.generate_content(
        model="models/gemini-2.0-flash",   
        contents=prompt
    )
    return response.text