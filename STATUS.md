# AETHER current state

Last updated: 2026-08-10

## Release posture

The repository is prepared as a public working-research project. Its history is intentionally flattened to one public-release root so obsolete private workflow material and personal commit metadata are not part of the public record.

The public site is deployed at `https://aetherclimate.com`. `https://aetherclimate.org` permanently redirects to the `.com` domain with path and query preservation. The site presents the possibility and public-infrastructure thesis; the paper and repository remain authoritative for evidence and caveats.

## Security and privacy

- No credentials, private keys, API tokens, or strong secret matches are tracked.
- Machine-specific paths, private workflow notes, course/submission material, and prompt archives have been removed.
- Document image inputs are constrained to approved repository directories.
- The Word-to-PDF fallback resolves the Windows system PowerShell executable without ambient search-path lookup.
- The unused secondary website toolchain has been removed; production and development now use the same Next.js/Vercel target.
- CI checks Python syntax, security regressions, the public-release tree, arithmetic consistency, website lint, website runtime behavior, and production dependency advisories.

## Scientific readiness

The generated submission ledger contains twelve gates:

- **Pass (5):** citation coverage, figure resolution, equation reproducibility, claim/evidence mapping, and duplicate/style screening.
- **Partial (5):** clean-power delivery, storage/MRV/lifecycle treatment, robotics field productivity, adversarial review, and submission formatting.
- **Fail (2):** publication-grade climate modeling and species-level emissions inputs.

The independent calculation audit currently passes all 31 arithmetic and consistency checks. That establishes internal calculation consistency only. It does not validate the assumptions, forecasts, or physical feasibility of the integrated system.

## Current release artifacts

- Proposal: `manuscript/proposal/AETHER_Conditional_Feasibility_Proposal.pdf`
- Working paper source: `manuscript/paper/aether_scientific_paper.md`
- Current review DOCX/PDF: `manuscript/submission/AETHER_Atmospheric_Engineering_Through_High_Energy_Removal_v0.45.*`
- Readiness note: `manuscript/review/aether_review_readiness.md`
- Gate ledger: `analysis/tables/aether_submission_readiness_gates.csv`
- Calculation audit: `analysis/tables/aether_independent_calculation_audit.csv`
- Public website: `website/`

## What still has to be learned

The main research risks are not hidden behind a general disclaimer. AETHER still needs species-level climate inputs and ensembles; regional 8760-hour power modeling; basin-level storage and injection analysis; method-specific lifecycle and MRV evidence; source-backed field-robotics distributions; component-level cost and material models; and external specialist review of the P0 falsification tests.

The honest description remains: stronger than an idea memo, useful for review, and not yet a scientific publication or validated deployment plan.
