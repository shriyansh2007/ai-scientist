
import os
import json
from itertools import combinations

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

# Load the existing hypotheses
with open("hypotheses.json", "r", encoding="utf-8") as file:
    hypotheses = json.load(file)

if len(hypotheses) < 2:
    raise ValueError("At least two hypotheses are required.")

results = []

# Examine every unique pair
for h1, h2 in combinations(hypotheses, 2):
    print(f"\nComparing {h1['id']} and {h2['id']}...")

    prompt = f"""
You are reviewing diversity among scientific hypotheses
in materials science.

Compare these two candidate hypotheses.

HYPOTHESIS A:
{json.dumps(h1, indent=2)}

HYPOTHESIS B:
{json.dumps(h2, indent=2)}

Assess the hypotheses using their scientific content, not
just differences in wording.

Return valid JSON with exactly these fields:
- hypothesis_1_id: ID of hypothesis A
- hypothesis_2_id: ID of hypothesis B
- mechanism_difference: string
- material_or_intervention_difference: string
- prediction_difference: string
- diversity_assessment: one of
  "distinct", "partially_overlapping", "highly_overlapping"
- reasoning: string
- recommended_action: one of
  "retain_both", "review_manually", "revise_one"

Guidelines:
- Different wording alone does not establish diversity.
- Different materials do not automatically mean different
  scientific mechanisms.
- Consider whether the proposed mechanisms and predictions
  can be distinguished experimentally.
- Do not invent citations or claim experimental validation.
- If information is insufficient, say so.
- These are preliminary judgments, not verified findings.
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
        config={"response_mime_type": "application/json"}
    )

    evaluation = json.loads(response.text)

    expected_fields = {
        "hypothesis_1_id",
        "hypothesis_2_id",
        "mechanism_difference",
        "material_or_intervention_difference",
        "prediction_difference",
        "diversity_assessment",
        "reasoning",
        "recommended_action"
    }

    missing = expected_fields - evaluation.keys()
    if missing:
        raise ValueError(
            f"Missing fields for {h1['id']} vs {h2['id']}: {missing}"
        )

    if evaluation["hypothesis_1_id"] != h1["id"]:
        raise ValueError("Incorrect first hypothesis ID.")

    if evaluation["hypothesis_2_id"] != h2["id"]:
        raise ValueError("Incorrect second hypothesis ID.")

    if evaluation["diversity_assessment"] not in {
        "distinct",
        "partially_overlapping",
        "highly_overlapping"
    }:
        raise ValueError("Invalid diversity assessment.")

    if evaluation["recommended_action"] not in {
        "retain_both",
        "review_manually",
        "revise_one"
    }:
        raise ValueError("Invalid recommended action.")

    results.append(evaluation)

    print("Assessment:", evaluation["diversity_assessment"])
    print("Reasoning:", evaluation["reasoning"])
    print("Recommended action:", evaluation["recommended_action"])

# Save all pairwise reviews
with open(
    "diversity_critic_results.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(results, file, indent=2, ensure_ascii=False)

print("\nSaved results to diversity_critic_results.json")
