# AETHER reproducibility

Last updated: 2026-09-05

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

The portable current-publication check also needs the locked publication group:

```text
uv sync --locked --group publication
uv run --group publication python scripts/build_current_publication.py --check
uv run --group publication python scripts/export_public_evidence.py --check
```

For an end-to-end, non-destructive regression check, run:

```text
uv run python scripts/reproduce_research.py --check
```

This command copies the repository to a temporary directory, regenerates the
declared core table pipeline there, and compares that result with the checked-in
outputs. It never writes under the working tree. A matching output only shows
that the declared calculations are deterministic; it does not validate scenario
assumptions, source interpretation, or physical feasibility.

For UTF-8 CSV and JSON outputs only, the check normalizes LF versus CRLF before
comparison so a Git checkout policy cannot create a false platform failure. It
does not normalize values, headers, ordering, encoding markers, or other
whitespace. Local `.env*` files and build caches such as `.next` are excluded
from the isolated copy.

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

`docs/MODEL_DEPENDENCIES.md` is the executable-order and compatibility
contract. In particular, the existing integrated feasibility model is labeled
`partially_coupled_screening`: it does not ingest compatible regional,
lifecycle, MRV, or field-productivity outputs, and results from those separate
scenario families must not be added together.

## Figures

PowerShell figure scripts read from `analysis/tables/` and write to `analysis/figures/`. Run the matching script after its input table changes:

```text
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/make_aether_feasibility_scorecard_figure.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/make_aether_integrated_figures.ps1
```

Generated figures must be inspected at full resolution for clipped text, unreadable legends, overlapping marks, and stale source labels.

## Manuscript and proposal

The compact Markdown paper and technical supplement are canonical. The supported
publication builder is portable and verifies the committed current artifacts:

```text
uv run --group publication python scripts/build_current_publication.py
uv run --group publication python scripts/build_current_publication.py --check
```

`build_aether_submission_package.py`, `build_aether_word_manuscript.py`, and
`render_aether_bibliography.py` are retained only for v0.45 historical recovery
and fail closed without `--legacy-v0-45-rebuild --legacy-output-dir PATH`, where
`PATH` is a separate complete AETHER checkout. They must not be used to
regenerate current paper, metadata, or evidence artifacts.

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
