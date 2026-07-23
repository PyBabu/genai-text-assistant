import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("API Key:", os.getenv("GEMINI_API_KEY")[:10] + "...")

print("\nAvailable Models:\n")

for model in client.models.list():
    print(model.name)

