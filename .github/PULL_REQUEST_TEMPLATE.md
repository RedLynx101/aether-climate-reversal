## What changed

Describe the narrow change and the artifact, claim, parameter, model, or website behavior it affects.

## Evidence and consequences

- Source or rationale for each changed parameter:
- Evidence class: observation, derivation, assumption, scenario, or speculation:
- Feasibility gates or headline claims affected:
- Third-party material or license considerations:

## Validation

- [ ] `uv run python -m unittest discover -s tests`
- [ ] `uv run python scripts/check_public_release.py`
- [ ] `uv run python scripts/audit_aether_calculations.py`
- [ ] Generated tables, figures, and manuscripts were rebuilt when their inputs changed.
- [ ] Changed DOCX/PDF/PNG artifacts were visually inspected for clipping, overlap, dangling headings, and broken captions.
- [ ] `cd website && npm ci && npm run lint && npm test` was run when the website changed.
