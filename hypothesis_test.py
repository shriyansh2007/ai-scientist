
import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

prompt = """
You are assisting a materials-science research project.

Generate one preliminary, testable hypothesis about factors
that may affect ionic conductivity in a solid-state electrolyte.

Do not claim that the hypothesis is established fact.
Do not invent citations or experimental results.

Return a JSON object with exactly these fields:
- claim: a concise hypothesis
- mechanism: a possible scientific explanation
- prediction: an observable predicted outcome
- assumptions: a list of assumptions
- falsification_test: a test whose result could contradict the hypothesis
"""

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=prompt,
    config={
        "response_mime_type": "application/json"
    }
)

# Convert the JSON text into a Python dictionary
hypothesis = json.loads(response.text)

# Display the fields separately
print("\n--- GENERATED HYPOTHESIS ---")
print("Claim:", hypothesis["claim"])
print("Mechanism:", hypothesis["mechanism"])
print("Prediction:", hypothesis["prediction"])
print("Assumptions:", hypothesis["assumptions"])
print("Falsification test:", hypothesis["falsification_test"])