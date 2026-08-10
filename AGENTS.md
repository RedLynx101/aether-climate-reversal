# Agent Instructions

This repo is AETHER: Atmospheric Engineering Through High-Energy Removal.

It is intended to become a serious academic research project, not a one-off essay. The old label `Climate Reversal Research` is descriptive only; use AETHER as the canonical project title in future docs, proposal drafts, model outputs, and figures.

## Operating Rules

- Preserve the distinction between evidence, assumptions, speculation, and research questions.
- Do not invent numbers, dates, quotes, citations, or claims to make the argument smoother.
- Keep the old abundance memo as reference material. Do not silently promote its claims into the proposal.
- When adding a quantitative claim, add a source note or mark it as `needs source`.
- Prefer primary sources: IPCC, NOAA, Global Carbon Project, IEA, IRENA, DOE, National Academies, peer-reviewed papers, company filings, official company statements, and data portals.
- Use secondary sources only as leads unless they are the best available record of a deleted or ephemeral public statement.
- Be explicit about failure modes: energy bottlenecks, storage leakage, MRV fraud, land and water constraints, ecological harms, permitting, rebound effects, supply chains, financing, and governance.

## Writing Style

Write directly. Use concrete mechanisms and tradeoffs. Avoid generic optimism, doom framing, and polished filler. The tone should be serious enough for academic work but not sterile.

## Citation Discipline

- Add source candidates to `references/source-register.md`.
- Add BibTeX entries to `references/bibtex/sources.bib` only when the source has enough metadata to cite.
- Put source-specific notes in `research/source-notes/`.
- If a claim came from a social post, preserve the original URL, access date, screenshot/archive status, and verification status.

## Modeling Discipline

Future model outputs should be reproducible. Every scenario needs:

- Named assumptions.
- Units.
- Source or rationale for each parameter.
- Sensitivity bounds.
- A note on which omitted variables could change the conclusion.
