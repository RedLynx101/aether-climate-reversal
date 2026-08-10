# AETHER Proposal Document

Final shareable proposal, rewritten from the v0.42 submission manuscript for use in academic contexts.

## Files

- `AETHER_Conditional_Feasibility_Proposal.pdf` - the deliverable.
- `AETHER_Conditional_Feasibility_Proposal.docx` - Word source of the PDF.
- `aether_proposal_source.md` - canonical text. Edit this, not the docx.
- `proposal-skeleton.md` - earlier outline (historical).

## Rebuilding

```
uv run --with python-docx --with docx2pdf --with pymupdf --with pillow python scripts\build_aether_proposal_docx.py
```

Requires Microsoft Word (PDF export uses Word COM via docx2pdf). The build crops the `Source: aether_*.py` footer lines from figures automatically, writes cropped copies to `figcache/`, and renders page previews to `preview/`. Both folders are disposable.

## How this differs from the submission manuscript

- Restructured from a repo changelog into a single integrated argument; all version numbers, file paths, and generated-table inventories removed.
- Cut from ~24k to ~11k words; repeated caveats consolidated.
- Numbers rounded to defensible precision.
- The 350 ppm management-floor throttle is flagged wherever it pins results.
- Company-primary robotics claims quarantined as market signals.
- Monte Carlo outputs framed as screens, not probabilities, and not led with.
- The upper-tail dependency of the pathway portfolio stated as a finding.
- Research roadmap reframed as a funded program with go/no-go gates.
