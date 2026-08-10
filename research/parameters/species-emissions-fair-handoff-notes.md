# Species-Emissions FAIR Handoff Notes

Last updated: 2026-08-09

This layer turns the FAIR forcing diagnostic into a concrete publication gate. It does not claim that AETHER now has a full species-emissions FAIR run. It lists the species and forcing families that must replace aggregate forcing placeholders before the paper treats temperature paths as publication-grade.

## Generated Artifacts

- `analysis/scenario-models/aether_species_emissions_handoff_model.py`
- `analysis/tables/aether_species_emissions_handoff_pathways.csv`
- `analysis/tables/aether_species_emissions_requirement_matrix.csv`
- `analysis/tables/aether_species_emissions_summary.csv`
- `analysis/tables/aether_species_emissions_publication_gates.csv`
- `analysis/figures/species_emissions_handoff_gap_matrix.png`

## Current Result

The handoff matrix tracks 16 species or forcing families across 28800 annual scenario-family rows. It marks 0 usable-screen families, 4 provisional proxies, 7 aggregate placeholders, and 5 missing families. The readiness score is 0.31, with 10 P0 blocking families. The publication-gate table has 7 fail rows and 3 partial rows.

The next climate-modeling step is therefore specific: replace aggregate non-CO2 and aerosol forcing with CH4, N2O, halogenated gases, ozone precursors, SO2, black carbon, organic carbon, nitrate/ammonia precursors, land-use forcing, lifecycle species traces, historical spin-up, ZEC, and uncertainty ensembles.

