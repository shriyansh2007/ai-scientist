
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
You are a scientific hypothesis generator specializing in
materials science.

Research question:
What factors could influence lithium-ion conductivity
in solid-state electrolytes?

Generate exactly THREE distinct, testable hypotheses.

Requirements:
1. Each hypothesis must propose a different scientific mechanism.
2. Each must make a measurable prediction.
3. Each must include assumptions.
4. Each must include a falsification test.
5. Do not invent experimental results or citations.
6. Treat all hypotheses as candidates, not established facts.

Return a JSON object with one key, "hypotheses".
Its value must be a list of exactly three objects.

Each object must contain:
- claim
- mechanism
- prediction
- assumptions (a list of strings)
- falsification_test
"""

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=prompt,
    config={
        "response_mime_type": "application/json"
    }
)

data = json.loads(response.text)
hypotheses = data["hypotheses"]

# Check that the model returned exactly three hypotheses.
if len(hypotheses) != 3:
    raise ValueError(
        f"Expected 3 hypotheses, got {len(hypotheses)}"
    )

required_fields = {
    "claim",
    "mechanism",
    "prediction",
    "assumptions",
    "falsification_test"
}

for i, hypothesis in enumerate(hypotheses, start=1):
    missing = required_fields - hypothesis.keys()

    if missing:
        raise ValueError(
            f"Hypothesis {i} is missing fields: {missing}"
        )

    hypothesis["id"] = f"H-{i:03d}"

print("\n=== GENERATED HYPOTHESES ===")

for hypothesis in hypotheses:
    print(f"\n{hypothesis['id']}: {hypothesis['claim']}")
    print("Mechanism:", hypothesis["mechanism"])
    print("Prediction:", hypothesis["prediction"])
    print("Assumptions:", hypothesis["assumptions"])
    print("Falsification test:", hypothesis["falsification_test"])

# Save the hypotheses so we can use them in later steps.
with open("hypotheses.json", "w", encoding="utf-8") as file:
    json.dump(hypotheses, file, indent=2, ensure_ascii=False)

print("\nSaved hypotheses to hypotheses.json")
