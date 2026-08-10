# AETHER

**Atmospheric Engineering Through High-Energy Removal**

AETHER is an open research program testing whether AI and robotics-accelerated infrastructure could make atmospheric carbon removal a managed public system. The central 100 GtCO2/year case is an extreme feasibility boundary, not a deployment promise, investment forecast, or prediction of AI progress.

The institutional thesis is straightforward: useful industrial activity can operate inside a measured net carbon budget. A public carbon utility would set an atmospheric operating range, meter net use, price permitted loading, procure durable removal and storage, verify results, carry liability, and return public value where the system produces a surplus. CO2 is a stock-and-flow variable to manage, not a moral category.

- Website: [aetherclimate.com](https://aetherclimate.com)
- Repository: [RedLynx101/aether-climate-reversal](https://github.com/RedLynx101/aether-climate-reversal)
- Principal author and project originator: Noah Hicks

## Current status

This is a conditional working paper and research scaffold. It has not been externally peer reviewed, and it is not publication-ready climate science.

Five submission gates currently pass, five remain partial, and two fail. The failing gates are publication-grade climate modeling and species-level emissions inputs. Clean-power delivery, storage/MRV/lifecycle treatment, robotics field productivity, adversarial specialist review, and final submission formatting remain partial.

AETHER is legitimate to share as a falsifiable engineering and governance proposal. It should not be represented as a validated climate solution or evidence that 100 GtCO2/year is likely.

## Start here

- `manuscript/proposal/AETHER_Conditional_Feasibility_Proposal.pdf` - concise designed proposal.
- `manuscript/paper/aether_scientific_paper.md` - canonical full working paper.
- `manuscript/submission/AETHER_Atmospheric_Engineering_Through_High_Energy_Removal_v0.45.pdf` - current review PDF.
- `manuscript/review/aether_review_readiness.md` - evidence classes and unresolved gates.
- `docs/REVIEW_GUIDE.md` - how to challenge a claim or contribute evidence.
- `docs/PUBLIC_RESEARCH_ROADMAP.md` - research priorities that could change the headline.
- `research/source-notes/ai-scenario-benchmarks.md` - comparison with AI 2027, AI 2040, and Situational Awareness.
- `analysis/tables/aether_independent_calculation_audit.csv` - independent arithmetic and consistency checks.

## What is in the repository

- `analysis/scenario-models/` contains the Python model suite.
- `analysis/tables/` and `analysis/figures/` contain generated, inspectable outputs.
- `data/parameters/` contains structured parameter and evidence registers.
- `research/` contains assumptions, source notes, literature review, parameter notes, and open questions.
- `references/` contains the source register and BibTeX bibliography.
- `manuscript/` contains the proposal, working paper, review notes, and current submission artifacts.
- `website/` contains the production Next.js site deployed through Vercel.

The earlier abundance memo remains under `reference-material/` as provenance, not evidence. Its course-specific working files are intentionally excluded from the public research record.

## Reproduce and review

Install [uv](https://docs.astral.sh/uv/) and Node.js 24, then run:

```text
uv sync --locked
uv run python -m unittest discover -s tests
uv run python scripts/check_public_release.py
uv run python scripts/audit_aether_calculations.py
uv run python scripts/check_source_register.py

cd website
npm ci
npm run lint
npm test
```

Model scripts are executable directly from the repository root. Each writes its named tables under `analysis/tables/`; corresponding PowerShell figure scripts write to `analysis/figures/`. The exact artifact and document workflow is described in `docs/reproducibility.md`.

## Research boundaries

AETHER asks whether enough clean power, machinery, air-contact capacity, materials, storage, measurement, capital, and governance could be assembled under a strong automation premise. Its outputs remain conditional on their stated inputs.

The project does not assume that software capability automatically becomes reliable field robotics. It does not treat gross capture as durable or creditable removal. It does not assume that cheap removal excuses unlimited emissions. A passing component model does not imply that the integrated system passes.

Deliberate planetary-scale atmospheric management qualifies as a low form of terraforming. That framing raises the governance burden on Earth. Descendant atmosphere-processing and autonomous-construction systems might eventually support work on other celestial bodies, but the current models do not establish off-world feasibility.

## Contributing

Scientific criticism is a contribution. Open a structured review issue, reproduce a model, replace a weak parameter, add a missing constraint, or submit a narrow pull request. Read `CONTRIBUTING.md`, `SECURITY.md`, and `CODE_OF_CONDUCT.md` first.

Code is licensed under Apache-2.0. Original research prose, documentation, tables, and figures are licensed under CC BY 4.0. AETHER was originated and is principally authored by Noah Hicks. See `LICENSING.md`, `NOTICE`, `AUTHORS.md`, and `CITATION.cff`.
