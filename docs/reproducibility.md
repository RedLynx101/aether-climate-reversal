# AETHER reproducibility

Last updated: 2026-08-10

The repository is self-contained. Public reproduction does not depend on a private dispatcher, personal filesystem path, or external notes directory.

## Environment

- Python 3.11 or later
- [uv](https://docs.astral.sh/uv/)
- Node.js 24 for the website
- Windows PowerShell for the current figure scripts and Microsoft Word PDF fallback

From the repository root:

```text
uv sync --locked
uv run python -m unittest discover -s tests
uv run python scripts/check_public_release.py
uv run python scripts/audit_aether_calculations.py
uv run python scripts/check_source_register.py
```

## Models and tables

Every Python model under `analysis/scenario-models/` resolves the repository from its own file location and writes named CSV outputs under `analysis/tables/`. Run the model that owns the changed output, for example:

```text
uv run python analysis/scenario-models/aether_scenario_model.py
uv run python analysis/scenario-models/aether_transition_model.py
uv run python analysis/scenario-models/aether_integrated_feasibility_model.py
uv run python analysis/scenario-models/aether_fair_forcing_execution_model.py
uv run python analysis/scenario-models/aether_feasibility_synthesis_model.py
```

Model ownership and output names are documented in `analysis/README.md` and the corresponding note under `research/parameters/`. A changed model must regenerate its tables before review.

## Figures

PowerShell figure scripts read from `analysis/tables/` and write to `analysis/figures/`. Run the matching script after its input table changes:

```text
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/make_aether_feasibility_scorecard_figure.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/make_aether_integrated_figures.ps1
```

Generated figures must be inspected at full resolution for clipped text, unreadable legends, overlapping marks, and stale source labels.

## Manuscript and proposal

The Markdown paper is canonical. Regenerate the review package and documents with:

```text
uv run python scripts/build_aether_submission_package.py
uv run --with python-docx --with pillow python scripts/build_aether_word_manuscript.py
uv run --with python-docx --with pillow --with pymupdf python scripts/build_aether_proposal_docx.py
```

The proposal builder uses `docx2pdf` when available and otherwise invokes the trusted Windows system PowerShell path. Both document builders reject image references that resolve outside the repository's approved figure directories.

After any document change, render every DOCX and PDF page to images and inspect every page for clipping, overlap, broken tables, dangling headings, orphaned captions, missing figures, and font substitution.

## Website

```text
cd website
npm ci
npm run lint
npm test
npm audit --omit=dev --audit-level=high
```

The only supported website target is native Next.js on Vercel. Domain redirects are implemented in `website/proxy.ts` and verified by the runtime test.

## Interpretation

Reproducible output does not make an assumption true. Reviewers should distinguish source-backed inputs, derived calculations, scenario assumptions, governance hypotheses, and unresolved questions. A model change is complete only when its source note, generated outputs, manuscript claim, and readiness gate agree.
