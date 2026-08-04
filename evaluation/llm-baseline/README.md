# GitHub Actions LLM Baseline — Frozen Pre-Execution Package

This package defines the LLM-baseline experiment for the GitHub Actions Semantic Benchmark before any model responses are inspected.

## Status

- Protocol, prompt, case structure, logging format, scoring rubric, and summary rules are frozen here.
- API keys, exact model IDs, raw responses, scoring decisions, and unpublished contamination-control cases are intentionally absent.
- The package is designed to be copied into the root of `github-actions-semantic-benchmark` or run with `--repo-root` pointing to that repository.

## Primary design

- Mutant-only workflow input; no oracle or fault-class leakage.
- The same prompt is used on clean baselines and mutants.
- Three independent trials per case and model.
- Fresh stateless request for every trial; no browsing, tools, repository access, or conversation history.
- Exact raw requests and responses are retained.
- Findings are scored only after baseline differencing and blinded review.
- Primary model-level result: majority detection (at least 2 of 3 trials).
- Sensitivity results: any-trial and stable 3-of-3 detection.

## Files

- `llm_evaluation_protocol.md` — frozen experimental protocol.
- `prompt_template.txt` — exact user prompt template.
- `case_manifest.json` — 5 logical baselines and 18 public mutants; intended-behavior text is loaded from oracle files at preparation time but oracle-only fields are stripped from model input.
- `run_llm_baseline.py` — validates cases, prepares prompts, and calls configured providers.
- `providers.example.yaml` — provider/model configuration template.
- `prepare_cases.py` — resolves repository paths and creates immutable prepared case inputs.
- `validate_package.py` — checks configuration, paths, hashes, and leakage safeguards.
- `freeze_hashes.py` — writes SHA-256 hashes for all pre-execution files.
- `scoring_blinded.csv` — blank blind-scoring sheet.
- `oracle_key_private.csv` — private mapping template; do not send to raters.
- `summarize_results.py` — creates aggregate detection and false-positive tables from completed scoring.
- `results_llm_baseline.csv` — empty output schema.
- `requirements.txt` — Python dependencies.

## Recommended sequence

1. Copy this folder into or next to the benchmark repository.
2. Fill `providers.yaml` from `providers.example.yaml`; use exact API model identifiers on the execution date.
3. Run `python prepare_cases.py --repo-root /path/to/github-actions-semantic-benchmark`.
4. Add and freeze 6–9 unpublished mutants under `unpublished_cases/` before model execution.
5. Run `python validate_package.py --repo-root ...`.
6. Run `python freeze_hashes.py` and commit/tag the package before any production calls.
7. Run a dummy provider or excluded pilot case only; do not alter the frozen prompt after viewing benchmark responses.
8. Execute model calls.
9. Generate the blinded scoring sheet and have the independent rater score without model identity or baseline/mutant status.
10. Run `summarize_results.py` after adjudication.

## Security

Never commit API keys. The scripts read keys from environment variables named in `providers.yaml`. Raw responses may contain provider request IDs and usage metadata; review before public release. The private oracle key must not be sent to the rater.

## Important limitation

The public v1.0.1 benchmark may have been available before some evaluated models were trained or deployed. The protocol therefore requires a fresh unpublished contamination-control set and reports public and unpublished results separately.
