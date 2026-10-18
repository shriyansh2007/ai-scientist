# Autonomous AI Scientist --- Hypothesis Hivemind Prototype

An early-stage research prototype exploring AI-assisted scientific
hypothesis generation and diversity assessment in materials science.

> **Status:** Initial prototype. This project is inspired by research on
> autonomous AI scientists and the hypothesis-hivemind problem. It is
> not a reproduction of the paper's experiments, a validated scientific
> discovery system, or a fully autonomous AI scientist.

## Overview

Scientific discovery can benefit from generating multiple candidate
explanations, critically reviewing them, and checking whether they are
meaningfully different. This project implements an initial workflow
around those ideas using a hosted large language model (LLM) and text
embeddings.

The current prototype can:

1.  Connect to the Google Gemini API.
2.  Generate a structured scientific hypothesis.
3.  Generate multiple candidate hypotheses in materials science.
4.  Ask an LLM-based critic to assess testability, falsifiability,
    mechanism quality, and experimental feasibility.
5.  Calculate pairwise cosine similarity between hypothesis embeddings.
6.  Ask an LLM-based reviewer to compare pairs of hypotheses by their
    proposed mechanisms, interventions, and predictions.
7.  Save intermediate results as JSON files for inspection and reuse.

## Current workflow

``` text
Gemini API connection
        |
        v
Generate one hypothesis / generate multiple hypotheses
        |
        v
hypotheses.json
        |
        +----------------------+
        |                      |
        v                      v
LLM scientific critic     Embedding similarity
        |                      |
        v                      v
critic_results.json       diversity_results.json

hypotheses.json
        |
        v
Mechanism-based pairwise reviewer
        |
        v
diversity_critic_results.json
```

The scripts are currently run separately. They have not yet been
integrated into a single autonomous research loop.

## Repository components

  -----------------------------------------------------------------------
  File                                Purpose
  ----------------------------------- -----------------------------------
  `test_model.py`                     Checks that the Gemini
                                      text-generation API connection
                                      works.

  `hypothesis_test.py`                Generates one structured hypothesis
                                      and parses the JSON response.

  `multi_hypothesis.py`               Generates three hypotheses and
                                      saves them to `hypotheses.json`.

  `critic.py`                         Reviews each hypothesis and records
                                      preliminary scores and concerns in
                                      `critic_results.json`.

  `test_embedding.py`                 Checks the embedding API and prints
                                      embedding dimensions.

  `diversity.py`                      Creates embeddings and calculates
                                      pairwise cosine similarity, saving
                                      `diversity_results.json`.

  `diversity_critic.py`               Compares pairs of hypotheses using
                                      an LLM-based mechanism reviewer,
                                      saving
                                      `diversity_critic_results.json`.

  `.env`                              Local API-key configuration. **Do
                                      not commit this file.**

  `.gitignore`                        Should exclude secrets, virtual
                                      environments, and generated Python
                                      cache files.
  -----------------------------------------------------------------------

The file list reflects the scripts implemented in the current prototype.
Generated JSON files are outputs, not source code.

## Technology

-   Python
-   Google GenAI Python SDK (`google-genai`)
-   Google Gemini API for text generation
-   `gemini-embedding-001` for embeddings
-   `python-dotenv` for local environment variables
-   Python standard library modules including `json`, `os`, `math`, and
    `itertools`

The project uses a hosted API, so it does not require a local GPU. API
access, model availability, quotas, and pricing depend on the Google
account and current service terms.

## Setup

### 1. Requirements

-   Windows, macOS, or Linux
-   Python version compatible with the installed `google-genai` SDK
-   A Google Gemini API key
-   Internet access for API calls

### 2. Clone the repository

``` bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_REPOSITORY_FOLDER>
```

Replace the placeholders with the actual repository URL and folder name.

### 3. Create and activate a virtual environment

**Windows PowerShell**

``` powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

``` bash
python -m pip install --upgrade pip
python -m pip install google-genai python-dotenv
```

### 5. Configure the API key

Create a local `.env` file in the project root:

``` dotenv
GEMINI_API_KEY=your_api_key_here
```

Replace the example value with your own key. Never put a real API key in
source code, screenshots, documentation, or a public repository.

Ensure `.gitignore` includes:

``` gitignore
.env
.venv/
__pycache__/
*.pyc
```

### 6. Run the scripts

Run the scripts from the project root with the virtual environment
activated:

``` powershell
python test_model.py
python hypothesis_test.py
python multi_hypothesis.py
python critic.py
python test_embedding.py
python diversity.py
python diversity_critic.py
```

Run `multi_hypothesis.py` before `critic.py`, `diversity.py`, or
`diversity_critic.py`, because those scripts use `hypotheses.json`. The
test scripts can be run independently. Each script may make one or more
API requests.

## Outputs

  -----------------------------------------------------------------------
  Output file                         Contents
  ----------------------------------- -----------------------------------
  `hypotheses.json`                   Generated candidate hypotheses,
                                      including fields such as claim,
                                      mechanism, prediction, assumptions,
                                      and falsification test.

  `critic_results.json`               Preliminary LLM reviewer scores,
                                      concerns, and missing evidence for
                                      each hypothesis.

  `diversity_results.json`            Pairwise cosine similarity values
                                      and flags based on the configured
                                      threshold.

  `diversity_critic_results.json`     LLM-generated comparisons of pairs
                                      of hypotheses and suggested review
                                      actions.
  -----------------------------------------------------------------------

The exact fields depend on the current script versions. Inspect the
generated JSON files to see the actual output.

## Interpreting the results responsibly

-   **Generated hypotheses are candidates, not established scientific
    facts.**
-   Critic scores are preliminary LLM judgments; they are not calibrated
    probabilities or objective measurements.
-   `evidence_status: not_provided` means that relevant literature or
    experimental evidence was not supplied to the critic.
-   Cosine similarity measures similarity in embedding space. It does
    not prove that two hypotheses are scientifically equivalent or
    redundant.
-   The similarity threshold in `diversity.py` is a provisional
    heuristic and needs calibration.
-   The mechanism-based reviewer is also an LLM judgment. Using the same
    model family for generation and review can produce correlated
    biases.
-   A toy simulation, if added later, would validate only the
    assumptions encoded in that simulation---not the behavior of a real
    material.

## Current limitations

1.  No literature retrieval or citation-grounded evidence verification
    yet.
2.  No real laboratory experiment or validated materials-science
    simulator.
3.  No persistent database or shared evidence memory yet.
4.  No automatic belief updating across research cycles.
5.  No single orchestrator that runs all components end-to-end.
6.  No calibrated method for deciding whether two scientific hypotheses
    are truly distinct.
7.  LLM-generated content may contain scientific errors, formatting
    issues, or unsupported assumptions and must be reviewed.

## Planned next steps

-   Improve schema validation, error handling, and reproducibility.
-   Add literature retrieval and source-grounded evidence review.
-   Improve diversity assessment using mechanism, intervention,
    prediction, and falsification criteria.
-   Add a controlled toy experiment runner with explicit assumptions.
-   Store hypotheses, evidence, and experiment results in SQLite.
-   Build an orchestration loop for generation, review, testing, and
    revision.
-   Add automated tests and example fixtures.
-   Evaluate the system on a documented set of scientific questions.

## Research context and attribution

This is an independent learning and prototyping project inspired by
research discussing autonomous AI scientists and the hypothesis-hivemind
problem, including work associated with Professor Mausam at IIT Delhi.
It is not an official implementation, endorsement, or reproduction of
the original research. Please consult and cite the original paper
directly in any formal report, and add its exact title, author list, and
DOI/arXiv identifier here after verifying them from the paper itself.


## Disclaimer

This repository is for research exploration and educational purposes. It
does not establish scientific validity, replace expert review, or
provide experimentally verified materials-science claims. Verify all
important claims against reliable sources and experimental data.
