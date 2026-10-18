
import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

# Load the hypotheses generated in the previous step.
with open("hypotheses.json", "r", encoding="utf-8") as file:
    hypotheses = json.load(file)

evaluations = []

for hypothesis in hypotheses:
    print(f"\nEvaluating {hypothesis['id']}...")

    prompt = f"""
You are a skeptical scientific reviewer specializing in
materials science.

Review the following proposed hypothesis.

HYPOTHESIS:
{json.dumps(hypothesis, indent=2)}

Evaluate it critically. Do not assume the hypothesis is true.
Do not invent scientific citations or experimental results.
Distinguish plausible reasoning from verified evidence.
If no literature evidence was supplied, explicitly say so.

Return one JSON object with exactly these fields:
- hypothesis_id: the supplied hypothesis ID
- testability: integer from 1 to 5
- falsifiability: integer from 1 to 5
- mechanism_quality: integer from 1 to 5
- experimental_feasibility: integer from 1 to 5
- evidence_status: "supported", "limited", or "not_provided"
- strengths: list of strings
- concerns: list of strings
- missing_evidence: list of strings
- suggested_improvement: string

Scoring:
1 = very weak
2 = weak
3 = moderate
4 = strong
5 = very strong

Use "not_provided" for evidence_status when no relevant
scientific sources or experimental data were supplied.
Scores are preliminary reviewer judgments, not probabilities.
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    evaluation = json.loads(response.text)

    # Ensure the evaluation belongs to the correct hypothesis.
    if evaluation.get("hypothesis_id") != hypothesis["id"]:
        raise ValueError(
            f"Incorrect hypothesis ID for {hypothesis['id']}"
        )

    # Check required fields.
    required_fields = {
        "hypothesis_id",
        "testability",
        "falsifiability",
        "mechanism_quality",
        "experimental_feasibility",
        "evidence_status",
        "strengths",
        "concerns",
        "missing_evidence",
        "suggested_improvement"
    }

    missing = required_fields - evaluation.keys()
    if missing:
        raise ValueError(
            f"{hypothesis['id']} evaluation missing: {missing}"
        )

    # Validate the numeric scores.
    score_fields = [
        "testability",
        "falsifiability",
        "mechanism_quality",
        "experimental_feasibility"
    ]

    for field in score_fields:
        score = evaluation[field]

        if type(score) is not int or not 1 <= score <= 5:
            raise ValueError(
                f"Invalid {field} score for {hypothesis['id']}"
            )

    if evaluation["evidence_status"] not in {
        "supported", "limited", "not_provided"
    }:
        raise ValueError(
            f"Invalid evidence status for {hypothesis['id']}"
        )

    for field in ["strengths", "concerns", "missing_evidence"]:
        if not isinstance(evaluation[field], list):
            raise ValueError(
                f"{field} must be a list for {hypothesis['id']}"
            )

    evaluations.append(evaluation)

    print("Testability:", evaluation["testability"], "/ 5")
    print("Falsifiability:", evaluation["falsifiability"], "/ 5")
    print("Mechanism quality:", evaluation["mechanism_quality"], "/ 5")
    print(
        "Experimental feasibility:",
        evaluation["experimental_feasibility"],
        "/ 5"
    )
    print("Evidence status:", evaluation["evidence_status"])
    print("Main concerns:", evaluation["concerns"])

# Save the evaluations separately from the original hypotheses.
with open("critic_results.json", "w", encoding="utf-8") as file:
    json.dump(evaluations, file, indent=2, ensure_ascii=False)

print("\nSaved evaluations to critic_results.json")
