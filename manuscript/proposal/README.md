# AETHER proposal materials

`aether_proposal_source.md` is the v0.46 proposal text. It is a concise conditional-research proposal that aligns with the current paper, technical supplement, and correction notice.

`AETHER_Conditional_Feasibility_Proposal.pdf` and `.docx` are historical/superseded proposal artifacts. Keep them for provenance, but do not treat their long-form figures, model outputs, or readiness language as current evidence. The current publication package is in `../submission/`:

- `AETHER_v0.46_working_paper.pdf`
- `AETHER_v0.46_technical_supplement.pdf`
- `current-publication.json`

The proposal does not claim external review, field validation, an approved deployment, or a climate forecast. Its current quantitative center is the generic 1 MtCO2/year matched regional analytical benchmark, not the historical 100 GtCO2/year stress-test narrative.

The source can be rendered through the repository publication workflow after:

```powershell
uv sync --locked --group publication
uv run python scripts/build_current_publication.py --check
```
