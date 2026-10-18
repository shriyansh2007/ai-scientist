
import os
import json
import math

from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Connect to the API
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

# 2. Load our generated hypotheses
with open("hypotheses.json", "r", encoding="utf-8") as file:
    hypotheses = json.load(file)

if len(hypotheses) < 2:
    raise ValueError("At least two hypotheses are required.")

# 3. Represent each hypothesis using its claim and mechanism
texts = []

for hypothesis in hypotheses:
    text = (
        f"Claim: {hypothesis['claim']}\n"
        f"Mechanism: {hypothesis['mechanism']}"
    )
    texts.append(text)

# 4. Generate embeddings
response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=texts,
    config=types.EmbedContentConfig(
        task_type="SEMANTIC_SIMILARITY"
    )
)

embeddings = [
    item.values for item in response.embeddings
]

# 5. Calculate cosine similarity
def cosine_similarity(vector_a, vector_b):
    dot_product = sum(
        a * b for a, b in zip(vector_a, vector_b)
    )

    norm_a = math.sqrt(sum(a * a for a in vector_a))
    norm_b = math.sqrt(sum(b * b for b in vector_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


# 6. Compare every unique pair
results = []

# This is a provisional threshold, not a scientific rule.
similarity_threshold = 0.80

for i in range(len(hypotheses)):
    for j in range(i + 1, len(hypotheses)):
        similarity = cosine_similarity(
            embeddings[i],
            embeddings[j]
        )

        result = {
            "hypothesis_1": hypotheses[i]["id"],
            "hypothesis_2": hypotheses[j]["id"],
            "cosine_similarity": round(similarity, 4),
            "potentially_redundant": (
                similarity >= similarity_threshold
            )
        }

        results.append(result)

        print(
            f"{result['hypothesis_1']} vs "
            f"{result['hypothesis_2']}: "
            f"{result['cosine_similarity']}"
        )

        if result["potentially_redundant"]:
            print("  Warning: potentially similar hypotheses")
        else:
            print("  No similarity warning at this threshold")

# 7. Save the results
output = {
    "embedding_model": "gemini-embedding-001",
    "similarity_threshold": similarity_threshold,
    "pairwise_comparisons": results
}

with open(
    "diversity_results.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(output, file, indent=2, ensure_ascii=False)

print("\nSaved results to diversity_results.json")
