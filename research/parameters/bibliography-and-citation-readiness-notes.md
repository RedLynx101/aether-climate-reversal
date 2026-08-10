# Bibliography and Citation Readiness Notes

Last updated: 2026-08-09

The generated bibliography layer is a reproducibility upgrade, not a final journal-style citation system. It generates:

- `manuscript/paper/aether_references_rendered.md`
- `analysis/tables/aether_bibliography_coverage.csv`
- `scripts/render_aether_bibliography.py`

The generator reads citation keys from `manuscript/paper/aether_scientific_paper.md` and BibTeX entries from `references/bibtex/sources.bib`. It keeps source keys in the rendered bibliography because AETHER still needs traceability to the source register while the paper is changing quickly.

Current coverage:

- Cited source keys in manuscript: 83
- Missing BibTeX entries: 0

Publication implication: this closes the crude source-key-bullet problem, but not the final citation-format problem. Before submission, render the manuscript with a target journal CSL style or an equivalent Pandoc/LaTeX pipeline, then audit every citation against the source register and the claim-evidence matrix.

