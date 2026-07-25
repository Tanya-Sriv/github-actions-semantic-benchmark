# 4. Evidence and Adjudication

## Preserve for every run

- repository URL;
- branch;
- commit SHA;
- workflow file SHA-256;
- GitHub run ID;
- event;
- runner operating system;
- Python version where applicable;
- action versions;
- job and step conclusions;
- start and end timestamps;
- raw logs;
- artifact metadata;
- final adjudication.

## CE08 evidence

Use:

- `templates/ce08_run_metadata.yml`
- `templates/ce08_adjudication.yml`

## CE11 evidence

Use:

- `templates/ce11_trial_metadata.yml`
- `templates/ce11_adjudication.yml`

## Evidence integrity

Do not edit raw logs.

Any derived summary must identify:

- source run ID;
- source file;
- extraction script or manual method;
- reviewer;
- review date.

## Interpretation rule

Separate:

1. Observation
2. Interpretation
3. Limitation

Do not turn an inconclusive or contradicted result into a positive finding.
