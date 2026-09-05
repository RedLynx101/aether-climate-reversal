# AETHER

**Atmospheric Engineering Through High-Energy Removal**

AETHER is an open conditional-research program on accountable atmospheric carbon management. Its central proposition is practical rather than moral: useful industrial activity could be paired with measurement of atmospheric loading, prevention of avoidable emissions, durable removal where needed, and long-tail liability that does not vanish when an operator does.

Direct air capture is one possible service tool, not the project's preferred answer in every case. Prevention, process change, concentrated-source capture, and durable atmospheric removal should be compared under the same physical, lifecycle, measurement, and liability boundary.

## Current status: v0.46

This is conditional research, not external peer review, field validation, engineering certification, a deployment recommendation, or a climate forecast.

The current quantitative center is a reproducible generic approximately 1 MtCO2/year liquid-solvent-DAC-plus-geologic-storage benchmark. It compares ordinary operations with automation assistance under the same physical contract. In the analytical mechanism test, a stated uptime assumption changes gross capture from 850,000 to 900,000 tCO2/year; it does not show that automation can create missing clean power, process heat, or storage.

The earlier 100 GtCO2/year material is retained as a stress-test and constraint inventory. It is not a feasibility finding. The corrected synthetic representative-day dispatch diagnostic no longer has a 100 GtCO2/year case after cyclic storage is enforced. The first RCMIP/Joos absolute carbon-output method is quarantined after an implausible zero-future-emissions diagnostic; it supports no ppm, temperature, target-date, or validated-climate claim. The integrated screen is partially coupled, and Monte Carlo shares are not probabilities.

## Start here

- [Current working paper](manuscript/submission/AETHER_v0.46_working_paper.pdf)
- [Current technical supplement](manuscript/submission/AETHER_v0.46_technical_supplement.pdf)
- [Current publication manifest](manuscript/submission/current-publication.json)
- [Current Markdown paper source](manuscript/paper/aether_scientific_paper.md)
- [Correction and replacement notice](docs/CORRECTIONS_v0.46.md)
- [Regional reference benchmark](docs/REGIONAL_REFERENCE.md)
- [Review readiness](manuscript/review/aether_review_readiness.md)
- [Public research roadmap](docs/PUBLIC_RESEARCH_ROADMAP.md)

The older proposal PDF/DOCX, v0.45 submission files, historical manuscript packages, and prior generated artifacts are retained for provenance only. They are superseded and are not current evidence.

## Reproduce and review

From the repository root, install [uv](https://docs.astral.sh/uv/) and run:

```powershell
uv sync --locked --group publication
uv run python -m unittest discover -s tests
uv run python scripts/reproduce_research.py --check
uv run python scripts/export_public_evidence.py --check
uv run python scripts/build_current_publication.py --check
uv run python scripts/audit_aether_calculations.py
uv run python scripts/check_public_release.py
uv run python scripts/check_source_register.py
```

These commands check reproducibility and package consistency. They do not establish that assumptions are correct or that a modeled system is deployable. No deployment or live-site verification is claimed here.

## Research boundaries

AETHER separates gross capture, retained carbon, signed net-after-lifecycle accounting, risk-adjusted credits, and net climate outcome. Only credits floor at zero; a negative net-after-lifecycle result remains a visible burden. Electricity, useful heat, and chemical energy are distinct inputs.

Approximately 280 ppm is a preindustrial reference range and long-horizon investigational restoration aspiration, not an established optimum, safe setpoint, or date. Deliberate atmospheric management is a limited literal form of terraforming, which raises the governance standard. Related technology might one day matter for closed habitats or other celestial bodies; this repository makes no readiness or transferability claim beyond Earth.

## Contributing and attribution

Useful contributions reproduce a bounded result, replace a weak input, add a constraint, or challenge a specific claim. Start with `CONTRIBUTING.md`, `docs/REVIEW_GUIDE.md`, and the review-readiness note.

Noah Hicks originated and principally authored AETHER. Code is Apache-2.0; original research prose, documentation, tables, and figures are CC BY 4.0. See `AUTHORS.md`, `CITATION.cff`, `LICENSING.md`, and `NOTICE`.
