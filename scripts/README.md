# AETHER scripts

Scripts are small, repository-relative entry points for models, figures, validation, and publication artifacts.

## Validation

- `check_public_release.py` rejects known private paths, legacy release material, obsolete website dependencies, and missing public-project controls.
- `audit_aether_calculations.py` independently recomputes headline arithmetic and consistency checks.
- `check_source_register.py` validates source-register structure and status fields.
- `build_current_publication.py` is the supported portable current-publication builder and `--check` validator.
- `export_public_evidence.py --check` verifies the source-linked public evidence payload and figures.
- `audit_aether_calculations.py` checks accounting identities and explicitly records review-required evidence boundaries; it does not validate scenario inputs.

## Documents

- `build_aether_submission_package.py`, `build_aether_word_manuscript.py`, and `render_aether_bibliography.py` are retired v0.45 historical builders. They fail closed unless invoked with both `--legacy-v0-45-rebuild` and `--legacy-output-dir PATH`, where `PATH` is a separate complete AETHER checkout; do not use them for current publication work.
- `build_aether_proposal_docx.py` creates the concise proposal DOCX and PDF.
- `export_aether_proposal_pdf.ps1` performs the Microsoft Word PDF export used by the proposal fallback.

Document builders accept only repository-contained figure paths. Run them from the repository root and visually inspect every regenerated page.

## Figures

Files named `make_aether_*_figure.ps1` read generated CSVs from `analysis/tables/` and write PNGs to `analysis/figures/`. They resolve the repository from `$PSScriptRoot`; no personal filesystem configuration is required.

See `docs/reproducibility.md` and `docs/MODEL_DEPENDENCIES.md` for supported generation order, isolated reproduction, and validation.
