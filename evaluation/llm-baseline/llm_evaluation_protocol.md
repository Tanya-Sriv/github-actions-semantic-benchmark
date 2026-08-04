# Frozen LLM-Baseline Evaluation Protocol

## Objective

Evaluate whether general-purpose language models detect schema-valid GitHub Actions operational-semantic faults represented by the benchmark, under a controlled protocol comparable to baseline-differenced static-tool evaluation.

## Research question

How often do evaluated language models identify the injected operational-semantic fault when given only the workflow configuration and a neutral statement of intended behavior, without access to the mutant oracle, fault-class label, baseline diff, repository, web, or external tools?

## Case sets

1. **Public benchmark set:** 18 released mutants and their five logical clean baselines (six baseline workflow files because B005 contains two interacting workflows).
2. **Fresh contamination-control set:** 6–9 unpublished mutants authored and frozen after this protocol, withheld from public access until all model calls and hashes are recorded.

Public and unpublished results must be reported separately and together. The unpublished set does not prove absence of contamination in the public set; it supplies an unreleased comparison condition.

## Models

Evaluate three models from at least two providers. Record exact API model IDs, provider, API endpoint/version, execution timestamp, region when exposed, generation settings, and any provider-reported model/version metadata. Do not substitute a model after results are inspected without labeling the replacement as a separate experiment.

## Input condition

Each request contains:

- the frozen prompt template;
- a neutral intended-behavior statement;
- one workflow file, or both interacting files for a cross-workflow case;
- file names and fenced YAML content.

Each request excludes:

- mutant ID and baseline ID;
- fault class and mutation operator;
- oracle, expected violation, target path, and ground-truth rationale;
- baseline-mutant diff in the primary condition;
- benchmark title, DOI, repository URL, and model-accessible web links.

## Prompt

The exact prompt is stored in `prompt_template.txt`. It must not be changed after production responses are viewed. A pilot may use an excluded dummy case before freezing.

## Trial structure

- Three independent trials per model and case.
- Fresh stateless API request for every trial.
- No conversation continuation, memory, browsing, tools, code execution, retrieval, or repository access.
- Provider seed is recorded when supported but is not assumed to guarantee determinism.
- Temperature is set to 0 or the provider's closest supported deterministic setting. Unsupported settings are omitted and documented.
- Maximum output tokens: 1,200 unless a provider requires a different ceiling, which must be documented.

## Baseline differencing

Every logical clean baseline is evaluated under the same model, prompt, intended-behavior statement, and trial count. A mutant response can count as a detection only if its matched fault is not present as an equivalent finding in the corresponding clean-baseline responses under the predefined differencing rule.

A baseline-equivalent finding is one that alleges the same violated relationship and operational consequence in the clean case. Generic advice present in both conditions is removed.

## Finding-to-oracle matching rule

A response matches the oracle only when it:

1. identifies the mutated construct or the affected operational relationship with enough specificity to locate the issue;
2. describes the same failure mechanism as the frozen oracle;
3. states a plausible operational consequence consistent with that oracle; and
4. goes beyond generic advice or restating the intended behavior.

Partial matches are recorded separately and do not count as primary true positives. A response may contain multiple findings; only the oracle-matching finding is scored for mutant detection, while unsupported additional findings contribute to false-positive analysis.

## Blind scoring

Responses are randomized and stripped of provider, model, trial, and case-status indicators before independent scoring. The rater receives the response, workflow input, intended behavior, and a concise oracle-matching rubric, but not the author judgment. For the primary blind assessment, the rater may receive the oracle statement keyed by an anonymous case code; this reveals the criterion but not whether the response is from a baseline or mutant.

Disagreements are listed individually and adjudicated after independent ratings are locked. Report plain agreement and Cohen's kappa for nominal decisions. If an ordinal match scale is used (No / Partial / Full), report weighted kappa.

## Primary and sensitivity metrics

For each model and mutant:

- **Any-trial detection:** at least 1 of 3 baseline-differenced trials is a full match.
- **Majority detection (primary):** at least 2 of 3 trials are full matches.
- **Stable detection:** all 3 trials are full matches.

Also report:

- clean-baseline false-positive rate;
- unsupported-finding rate per response;
- trial-to-trial consistency;
- detection by fault class and semantic depth;
- public versus unpublished-set results;
- refusals, empty responses, API failures, and reruns.

## Failed requests and reruns

Retry only transport errors, provider 5xx errors, timeouts, and explicit rate-limit errors. Do not retry a valid refusal, empty substantive answer, or poor-quality response. Retried requests retain the same case/model/trial identifier and log every attempt. The first successful API response is canonical.

## Contamination analysis

Record:

- public benchmark release date;
- model deployment/model-card date where documented;
- provider statements about training cutoffs only when officially documented;
- whether the model had browsing, retrieval, or tools disabled;
- performance difference between public and unpublished sets.

Do not claim that a training cutoff proves non-exposure. Treat contamination as unresolved for public cases and as reduced, not eliminated, for unpublished cases.

## Reproducibility and release

Publish verbatim prompts, prepared workflow inputs, model IDs, timestamps, generation settings, raw responses, blinded scoring records, adjudication log, scripts, and aggregate outputs. Remove API keys and review provider metadata for sensitive identifiers. Preserve hashes of all frozen pre-execution files and unpublished cases.
