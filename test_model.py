
import os
from dotenv import load_dotenv
from google import genai

# Load the API key from the .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "API key not found. Check your .env file."
    )

# Create a client that communicates with Gemini
client = genai.Client(api_key=api_key)

# Send a simple request to the model
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Explain ionic conductivity in a solid-state electrolyte in two simple sentences."
)

# Display the model's answer
print(response.text)