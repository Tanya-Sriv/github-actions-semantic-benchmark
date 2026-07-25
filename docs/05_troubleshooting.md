# 5. Troubleshooting

## Workflow does not appear

Confirm:

- the workflow file is under `.github/workflows/`;
- the branch was pushed;
- the YAML contains `workflow_dispatch`;
- GitHub Actions is enabled for the repository.

## CE08 artifact does not appear

This may be the actual experimental result.

Check the upload-step outcome and logs before treating it as a setup error.

## CE11 runs finish before overlap

The workflows include `sleep 90`. Trigger the second workflow within 10 seconds.

## Branch contains the wrong workflow

Run:

```bash
python scripts/verify_branch_contents.py
```

Then compare the active workflow files with the relevant `experiments/` source folder.

## Recreate branches

Delete local branches and rerun the branch script only after committing any work that must be retained.
