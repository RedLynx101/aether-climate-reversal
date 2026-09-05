# AETHER current publication package

The current v0.46 public-review package is:

- `AETHER_v0.46_working_paper.pdf`
- `AETHER_v0.46_technical_supplement.pdf`
- `current-publication.json`

The Markdown sources are in `../paper/`. The paper is conditional research, internally revised but not externally peer reviewed, field validated, or engineering certified.

The v0.45 DOCX/PDF, earlier generated manuscript files, and their manifests are historical artifacts. They are retained for provenance only and are superseded by this package. Do not use them as current evidence.

To check the package from the repository root:

```powershell
uv sync --locked --group publication
uv run python scripts/reproduce_research.py --check
uv run python scripts/export_public_evidence.py --check
uv run python scripts/build_current_publication.py --check
```

Those checks test reproducibility and package consistency, not scientific adequacy or deployment readiness.
