# Upwork Proposal Safety Gates

A dependency-free, offline gate for **draft-only** proposal material. It combines job eligibility, proposal completeness, public-proof, and duplicate checks before a human or authorized platform workflow considers submission.

It never authenticates, sends a proposal, contacts a client, uses a browser, or makes network requests.

## Run

```bash
python3 gate.py job.json draft.md claims.json seen.json
```

`READY` means only that the supplied sanitized inputs passed local checks. Reconcile current platform access, allowance, duplicate history, job recency, and client credibility before any submission.

## Test

```bash
python3 -m unittest -v
```

No private data, credentials, customer data, or target URLs should be included in fixtures or examples.

## Contract delivery acceptance pack

`acceptance_pack.py SCOPE_FILE` generates a handoff checklist from explicit scope lines only. It is offline and does not infer client requirements.
