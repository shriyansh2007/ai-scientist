
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

texts = [
    "Expanding lithium-ion migration pathways may improve ionic conductivity.",
    "Widening lithium-ion transport channels may increase ionic conductivity.",
    "Changing a material's color may improve its optical appearance."
]

response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=texts,
    config=types.EmbedContentConfig(
        task_type="SEMANTIC_SIMILARITY"
    )
)

embeddings = [item.values for item in response.embeddings]

print("Number of sentences:", len(embeddings))
print("Dimensions per embedding:", len(embeddings[0]))
print("Embedding test successful!")
print("First 5 numbers of the first embedding:")
print(embeddings[0][:5])
