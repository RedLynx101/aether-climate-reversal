# AETHER Submission Checklist

Last updated: 2026-08-10

Use this before sending AETHER to a scientist, advisor, or potential collaborator.

## Current Package

- Review manuscript: `manuscript/submission/aether_submission_manuscript.md`
- Package manifest: `manuscript/submission/aether_submission_manifest.md`
- Figure inventory: `analysis/tables/aether_figure_inventory.csv`
- Readiness gates: `analysis/tables/aether_submission_readiness_gates.csv`
- Style audit: `analysis/tables/aether_manuscript_style_audit.csv`

## Gate Summary

| Gate | Status | Current evidence |
| --- | --- | --- |
| S01_citation_coverage | pass | 83 cited keys; 0 missing BibTeX entries |
| S02_figure_resolution | pass | 41 paper figure references; 0 missing files |
| S03_equation_reproducibility | pass | 10 unit checks; 0 failures |
| S04_claim_evidence | pass | 14 claim-evidence rows |
| S05_climate_model_publication_grade | fail | Forcing-driven FAIR diagnostic exists, but species-emissions handoff still blocks publication-grade climate claims. |
| S06_species_emissions_inputs | fail | 7 failing species-emissions gates out of 10 |
| S07_clean_power_delivery | partial | 7 clean-power deliverability summary rows plus regional dispatch screen |
| S08_storage_mrv_lifecycle | partial | Route-level storage, lifecycle, MRV, and credit-integrity screens exist. |
| S09_robotics_field_productivity | partial | Production verification and field-productivity distribution screens exist, but multipliers remain provisional. |
| S10_adversarial_review | partial | 10 falsification-test rows in the adversarial review packet |
| S11_style_and_duplicate_scan | pass | old repeated FAIR phrase count: 0; editorial placeholder hits: 0 |
| S12_submission_format | partial | Generated Markdown submission package exists; final journal format is not selected. |

## Minimum Before Formal Submission

1. Pick the target venue or advisor-facing format.
2. Render citations through the required CSL, Pandoc, or LaTeX pipeline.
3. Add final numbered captions for all paper figures.
4. Replace the climate-response proxy with species-emissions FAIR-class or Earth-system modeling.
5. Upgrade field-productivity, storage, lifecycle, MRV, and regional dispatch assumptions from screens to source-backed distributions.
6. Run adversarial review against the P0 falsification tests and narrow the claim where needed.
