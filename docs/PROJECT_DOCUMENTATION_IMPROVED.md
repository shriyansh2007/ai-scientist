# Autonomous AI Scientist: Hypothesis Hivemind Prototype

**Technical Project Report · Initial Prototype · Materials Science**

  -----------------------------------------------------------------------
  Field                               Details
  ----------------------------------- -----------------------------------
  Project focus                       AI-assisted scientific hypothesis
                                      generation and diversity assessment

  Language                            Python

  Model services                      Google Gemini API and
                                      `gemini-embedding-001`

  Status                              Initial working prototype; research
                                      and engineering extensions remain
  -----------------------------------------------------------------------

> **Scope statement:** This project is an independent prototype inspired
> by research on autonomous AI scientists and the hypothesis-hivemind
> problem. It is not an official implementation of the paper, a
> reproduction of its experiments, or a validated autonomous scientific
> discovery system.

------------------------------------------------------------------------

## Abstract

This project explores a small, inspectable workflow for AI-assisted
scientific hypothesis generation in materials science. It uses a hosted
large language model (LLM) to generate structured candidate hypotheses
and provide preliminary critiques. It also uses text embeddings to
calculate pairwise semantic similarity and a separate LLM prompt to
compare pairs of hypotheses by their proposed mechanisms, interventions,
and predictions.

The current implementation contains four principal capabilities:
**structured hypothesis generation, LLM-based scientific criticism,
embedding-based similarity analysis, and mechanism-focused pairwise
review**. Outputs are saved to JSON files so they can be inspected and
reused.

The prototype demonstrates that these components run and produce
structured outputs. It does not yet retrieve scientific literature,
verify novelty, conduct real experiments, update beliefs from
experimental feedback, or coordinate all components in a persistent
autonomous research loop. The next stage is to add evidence-grounded
review, controlled testing, persistent memory, and systematic
evaluation.

## 1. Motivation and research question

Scientific hypothesis generation is not only a text-generation task.
Useful research support also requires testable claims, explicit
assumptions, potential falsification tests, and a way to compare
competing explanations.

A particular challenge is **hypothesis diversity**: several outputs can
differ in wording while proposing essentially the same scientific idea.
Conversely, hypotheses that share vocabulary may still propose different
mechanisms or interventions. This prototype therefore explores two
complementary questions:

1.  Can an LLM generate multiple structured, testable candidate
    hypotheses for a materials-science question?
2.  Can semantic similarity and mechanism-focused review help identify
    which candidates may overlap and which may warrant separate
    consideration?

These are exploratory engineering questions. The prototype does not
claim that its outputs are novel, correct, or scientifically important.

## 2. Goals and non-goals

### Implemented goals

-   Connect a Python project to a hosted Gemini text-generation model.
-   Generate one structured hypothesis and multiple candidate
    hypotheses.
-   Ask an LLM critic to review testability, falsifiability, mechanism
    quality, and experimental feasibility.
-   Generate vector embeddings for hypothesis text.
-   Calculate pairwise cosine similarity and flag pairs above a
    configurable threshold.
-   Ask an LLM reviewer to compare pairs by mechanism, material or
    intervention, and predicted outcomes.
-   Save intermediate outputs as JSON for inspection.

### Not implemented yet

-   Scientific literature search and retrieval-augmented generation
    (RAG).
-   Source-grounded claim verification or citation checking.
-   Reliable novelty assessment against the literature.
-   Real laboratory experimentation or a validated materials-science
    simulator.
-   Persistent research memory or experiment history in a database.
-   Formal Bayesian belief updates from new evidence.
-   An end-to-end orchestrator that runs repeated research cycles.
-   Benchmarking against expert judgments or reproducing the original
    paper's evaluation.

## 3. System architecture

### 3.1 Current component flow

``` mermaid
flowchart TD
    A[Gemini API connection test] --> B[Single-hypothesis generation]
    A --> C[Generate multiple hypotheses]
    C --> D[hypotheses.json]
    D --> E[LLM scientific critic]
    D --> F[Embedding similarity checker]
    D --> G[Mechanism-based pair reviewer]
    E --> H[critic_results.json]
    F --> I[diversity_results.json]
    G --> J[diversity_critic_results.json]
```

The scripts are currently run separately. The diagram describes the
current workflow, not a fully automated orchestration service. The
critic and diversity reviewers are LLM-based assessments, not
independent experimental validators.

### 3.2 Repository files

  ---------------------------------------------------------------------------------
  File                    Responsibility          Main output
  ----------------------- ----------------------- ---------------------------------
  `test_model.py`         Verify text-generation  Printed response
                          API connectivity        

  `hypothesis_test.py`    Generate one structured Printed JSON-like result
                          candidate hypothesis    

  `multi_hypothesis.py`   Generate three          `hypotheses.json`
                          candidate hypotheses    
                          and assign IDs          

  `critic.py`             Assess each hypothesis  `critic_results.json`
                          and record preliminary  
                          concerns                

  `test_embedding.py`     Verify that the         Embedding dimensions and sample
                          embedding API works     values

  `diversity.py`          Embed claim + mechanism `diversity_results.json`
                          text and calculate      
                          pairwise cosine         
                          similarity              

  `diversity_critic.py`   Compare each hypothesis `diversity_critic_results.json`
                          pair using an LLM       
                          prompt                  

  `.env`                  Store the local API key Must remain untracked

  `.gitignore`            Exclude credentials,    N/A
                          virtual environments,   
                          and cache files         
  ---------------------------------------------------------------------------------

The list describes the scripts used in the current prototype. Confirm
that the same files are present in the public repository before
publishing this report.

## 4. Implementation details

### 4.1 Structured hypothesis generation

`hypothesis_test.py` tests a single structured generation request.
`multi_hypothesis.py` requests three candidates and stores them in
`hypotheses.json`.

A hypothesis object includes fields such as:

-   `id`: a local identifier such as `H-001`.
-   `claim`: the main candidate claim.
-   `mechanism`: a proposed explanation for the effect.
-   `prediction`: an outcome that could be observed if the hypothesis is
    correct.
-   `assumptions`: assumptions or conditions on which the claim depends.
-   `falsification_test`: a proposed test that could count against the
    claim.

The generator's response is model-produced. A well-formed JSON object
does not imply that the scientific content is valid. The generated
candidates should be checked against scientific literature and domain
expertise before being treated as research claims.

### 4.2 LLM-based scientific critic

`critic.py` reviews the hypotheses individually. It requests preliminary
integer scores from 1 to 5 for:

-   **Testability:** whether an observation or experiment could assess
    the claim.
-   **Falsifiability:** whether a plausible result could count against
    it.
-   **Mechanism quality:** whether the proposed explanation is coherent
    and sufficiently specified.
-   **Experimental feasibility:** whether the proposed test appears
    practical.

It also records strengths, concerns, missing evidence, a suggested
improvement, and an evidence-status label. In the observed run, the
critic returned `not_provided` for evidence status because no supporting
papers or experimental data were supplied.

These are subjective LLM judgments. The scores are not calibrated
probabilities, validated measurements, or a substitute for expert
review. The critic can generate incorrect or overconfident scientific
reasoning.

### 4.3 Embedding-based similarity

`test_embedding.py` verified the configured embedding API. The observed
test returned three embeddings, each with 3,072 dimensions.

`diversity.py` creates a text representation from each candidate's claim
and mechanism, embeds those texts using `gemini-embedding-001`, and
calculates cosine similarity for every unique pair.

For vectors (A) and (B):

\[ `\operatorname{cosine}`{=tex}(A,B)=
`\frac{A\cdot B}{\|A\|\,\|B\|}`{=tex} \]

The value measures alignment between the two vectors. Similarity values
closer to 1 indicate stronger similarity in embedding space, but **they
are not probabilities, novelty scores, or proof of scientific
equivalence**.

The current script uses a provisional threshold of `0.80` to flag pairs
for review. This threshold is a heuristic, not a scientifically
calibrated boundary. It should be evaluated against a labeled set of
hypothesis pairs before being used for consequential decisions.

### 4.4 Mechanism-focused pairwise review

`diversity_critic.py` compares each unique pair and asks an LLM to
discuss:

-   How the proposed mechanisms differ.
-   Whether the materials or interventions differ.
-   Whether the predicted outcomes are distinguishable.
-   Whether the pair appears distinct, partially overlapping, or highly
    overlapping.
-   Whether to retain both candidates, review manually, or revise one.

The output is stored in `diversity_critic_results.json`.

This review provides a different perspective from vector similarity, but
it is **not an independent source of truth**. The generation and review
stages use the same Gemini model family and may share biases. Strong
claims in the review must be checked against scientific sources and
experimental evidence.

## 5. Observed prototype run

The multi-hypothesis generator produced three candidate topics:

  -----------------------------------------------------------------------
  ID                      Candidate topic         Proposed intervention
                                                  or factor
  ----------------------- ----------------------- -----------------------
  H-001                   Lithium-ion transport   Selenium substitution
                          in argyrodite           
                          electrolytes            

  H-002                   Grain-boundary          Tantalum segregation
                          resistance in LLZO      

  H-003                   Lithium-ion diffusion   Tensile strain
                          in LLZO thin films      
  -----------------------------------------------------------------------

These are examples of **model-generated candidates**, not verified
findings. Their scientific validity and novelty have not been
established.

### 5.1 Critic output

The critic returned the following preliminary scores:

  ---------------------------------------------------------------------------------------
  Hypothesis     Testability   Falsifiability    Mechanism   Feasibility Evidence status
                                                   quality               
  ------------ ------------- ---------------- ------------ ------------- ----------------
  H-001                  4/5              5/5          4/5           4/5 `not_provided`

  H-002                  4/5              4/5          2/5           3/5 `not_provided`

  H-003                  4/5              4/5          3/5           2/5 `not_provided`
  ---------------------------------------------------------------------------------------

The critic raised concerns about possible confounding factors,
electrostatic interpretation, phase stability, strain relaxation, and
experimental feasibility. These concerns are useful prompts for
follow-up investigation, but they are not verified scientific
conclusions.

### 5.2 Embedding similarity output

The observed pairwise cosine similarity scores were:

  Pair               Cosine similarity Flagged at threshold 0.80?
  ---------------- ------------------- ----------------------------
  H-001 vs H-002                0.8712 Yes
  H-001 vs H-003                0.9084 Yes
  H-002 vs H-003                0.8729 Yes

All three pairs exceeded the configured threshold and were flagged for
review.

### 5.3 Mechanism-review output

The LLM-based mechanism reviewer classified all three pairs as
`distinct` and recommended `retain_both` for each pair.

The two assessment methods therefore produced different signals:
embedding similarity flagged every pair, while the mechanism reviewer
judged every pair distinct. This is an important prototype observation,
not a failure to be hidden. It shows that semantic similarity and
mechanism-level diversity are different concepts and that neither method
should decide on its own whether a candidate is redundant.

The next evaluation should inspect these pairs manually, compare their
mechanisms and predictions, and establish labeled examples to measure
when each method is useful.

## 6. Setup and execution

### 6.1 Requirements

-   Python version compatible with the installed `google-genai` SDK.
-   A Gemini API key.
-   Internet connectivity for hosted API calls.
-   Windows, macOS, or Linux.

A local GPU is not required because model inference is performed through
hosted APIs.

### 6.2 Create and activate an environment

Windows PowerShell:

``` powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install google-genai python-dotenv
```

macOS or Linux:

``` bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install google-genai python-dotenv
```

### 6.3 Configure the API key

Create a `.env` file in the project root:

``` dotenv
GEMINI_API_KEY=your_api_key_here
```

Do not commit this file or paste the real key into source code,
documentation, screenshots, or public issue trackers. The `.gitignore`
file should include:

``` gitignore
.env
.venv/
__pycache__/
*.pyc
```

If a key is accidentally exposed, revoke or rotate it through the
provider.

### 6.4 Run the scripts

From the repository root, with the virtual environment activated:

``` powershell
python test_model.py
python hypothesis_test.py
python multi_hypothesis.py
python critic.py
python test_embedding.py
python diversity.py
python diversity_critic.py
```

Run `multi_hypothesis.py` before `critic.py`, `diversity.py`, and
`diversity_critic.py`, because those scripts read `hypotheses.json`. API
calls may be subject to provider quotas, account terms, and costs. Model
identifiers and API behavior can change; check the provider's current
documentation if a request fails.

## 7. Output files

  -----------------------------------------------------------------------
  File                                Purpose
  ----------------------------------- -----------------------------------
  `hypotheses.json`                   Structured candidate hypotheses

  `critic_results.json`               Preliminary critic scores,
                                      concerns, and missing evidence

  `diversity_results.json`            Pairwise similarity scores and
                                      threshold flags

  `diversity_critic_results.json`     Pairwise mechanism reviews and
                                      suggested actions
  -----------------------------------------------------------------------

These files are generated outputs. Review them before committing them to
a public repository, particularly if they contain sensitive research
prompts or information.

## 8. Limitations and threats to validity

### Scientific limitations

1.  **No literature retrieval:** the prototype cannot reliably establish
    novelty or whether a claim is already known.
2.  **No experimental feedback:** it does not run laboratory tests or a
    validated materials-science simulator.
3.  **Domain complexity:** material behavior may depend on phase
    stability, defects, stoichiometry, sample preparation, measurement
    geometry, and other confounders.
4.  **No expert-labeled benchmark:** there is no measured estimate of
    the system's accuracy at identifying redundant hypotheses.
5.  **No uncertainty calibration:** reviewer scores and labels are not
    calibrated against a reference standard.

### Engineering limitations

1.  The scripts are run separately rather than through one orchestrator.
2.  The current workflow does not persist a linked history of
    hypotheses, evidence, and outcomes in a database.
3.  Error handling, retries, logging, and automated tests can be
    improved.
4.  The similarity threshold is provisional and not calibrated.
5.  LLM-based generation and review can share biases, hallucinate
    mechanisms, or express unjustified confidence.
6.  JSON validity and required fields do not guarantee factual or
    scientific correctness.

## 9. Development roadmap

### Phase 1 --- Make the prototype more robust

-   Add consistent schema validation and useful error messages.
-   Add tests for cosine similarity, pair enumeration, and malformed
    model responses.
-   Log model identifiers, timestamps, prompts or prompt versions, and
    run settings.
-   Make outputs reproducible where the API permits and record the
    limits of reproducibility.

### Phase 2 --- Add literature-grounded review

-   Retrieve relevant scientific papers and preserve source metadata.
-   Connect claims in reviews to retrieved evidence.
-   Separate directly supported statements from model interpretation and
    missing evidence.
-   Require manual review before making novelty or scientific-validity
    claims.

### Phase 3 --- Add a controlled experiment runner

-   Start with a small toy model whose assumptions and equations are
    explicit.
-   Define baseline conditions and interventions.
-   Change one variable at a time and record predicted and simulated
    outcomes separately.
-   Label simulation results as synthetic; do not treat them as real
    materials-science evidence.

### Phase 4 --- Add persistent research memory

-   Store hypotheses, reviews, sources, and experiments in SQLite.
-   Link each observation to its hypothesis, conditions, and provenance.
-   Preserve negative results and failed approaches.
-   Track revisions instead of silently overwriting earlier hypotheses.

### Phase 5 --- Build an iterative research loop

-   Coordinate generation, criticism, evidence retrieval, diversity
    checks, and experiment planning.
-   Define explicit criteria for when to revise or continue a
    hypothesis.
-   Update confidence only through a documented evidence-update
    procedure.
-   Keep human oversight for consequential scientific decisions.

### Phase 6 --- Evaluate the system

-   Create a set of hypothesis pairs labeled by trained reviewers or
    domain experts.
-   Measure false-positive and false-negative redundancy flags.
-   Compare embedding-only, mechanism-review-only, and combined
    approaches.
-   Assess whether critiques identify useful confounders and
    falsification tests.
-   Document failures and examples where the model's conclusions were
    incorrect.

## 10. Relationship to the motivating research

This project is inspired by research concerning autonomous AI scientists
and the hypothesis-hivemind problem, including work associated with
Professor Mausam at IIT Delhi. It is an independent learning and
prototyping effort.

The current implementation operationalizes a small subset of related
ideas---multiple candidate hypotheses, critique, and diversity
assessment. It does not implement or reproduce the full empirical study
or the broader research architecture discussed in the paper.

**Before public release, add a verified citation to the exact paper:**
title, complete author list, publication venue or preprint server, year,
and DOI or arXiv identifier. Verify those details from the original
paper rather than guessing them.

## 11. Responsible interpretation

-   Generated hypotheses are candidates for investigation, not
    established facts.
-   Critic scores are preliminary model judgments, not probabilities.
-   Similarity scores are measurements in embedding space, not direct
    novelty measures.
-   LLM mechanism reviews are not independent experimental validation.
-   Any future toy simulation will reflect only the assumptions encoded
    in its model.
-   Claims about real materials should be supported by reliable
    literature, expert review, or appropriate experimental evidence.

## 12. Conclusion

This initial prototype provides a working foundation for AI-assisted
scientific hypothesis generation and diversity screening. It
demonstrates structured candidate generation, preliminary LLM criticism,
embedding-based pairwise similarity, and mechanism-focused pair review.

The observed difference between similarity flags and mechanism-review
judgments highlights a central challenge: textual similarity alone is
insufficient to establish whether scientific ideas overlap. The next
stage is to ground reviews in literature, preserve evidence and
failures, test predictions under controlled assumptions, and evaluate
the system against explicit criteria.

