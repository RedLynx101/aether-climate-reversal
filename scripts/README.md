# AETHER scripts

Scripts are small, repository-relative entry points for models, figures, validation, and publication artifacts.

## Validation

- `check_public_release.py` rejects known private paths, legacy release material, obsolete website dependencies, and missing public-project controls.
- `audit_aether_calculations.py` independently recomputes headline arithmetic and consistency checks.
- `check_source_register.py` validates source-register structure and status fields.
- `render_aether_bibliography.py` regenerates the readable bibliography from the cited source keys.

## Documents

- `build_aether_submission_package.py` builds the Markdown review package and readiness ledgers.
- `build_aether_word_manuscript.py` creates the current Word review copy.
- `build_aether_proposal_docx.py` creates the concise proposal DOCX and PDF.
- `export_aether_proposal_pdf.ps1` performs the Microsoft Word PDF export used by the proposal fallback.

Document builders accept only repository-contained figure paths. Run them from the repository root and visually inspect every regenerated page.

## Figures

Files named `make_aether_*_figure.ps1` read generated CSVs from `analysis/tables/` and write PNGs to `analysis/figures/`. They resolve the repository from `$PSScriptRoot`; no personal filesystem configuration is required.

See `docs/reproducibility.md` for commands and the required validation sequence.
