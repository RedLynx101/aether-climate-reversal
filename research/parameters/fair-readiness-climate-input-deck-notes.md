# FAIR-Readiness Climate Input Deck Notes

Last updated: 2026-06-10

This layer is a bridge from AETHER's current screening climate models to a real FAIR-class or Earth-system workflow. It does not claim to run FAIR. It does something narrower and useful: it joins the annual emissions/removal pulse variables from the state-dependent carbon screen to the annual forcing and temperature variables from the dynamic climate emulator.

## Generated Artifacts

- `analysis/scenario-models/aether_fair_readiness_model.py`
- `analysis/tables/aether_fair_readiness_input_deck.csv`
- `analysis/tables/aether_fair_readiness_summary.csv`
- `analysis/tables/aether_fair_readiness_gap_matrix.csv`
- `analysis/tables/aether_fair_readiness_run_manifest.csv`
- `analysis/figures/fair_readiness_climate_input_deck.png`

## Current Result

The joined input deck has 1800 annual rows and 17 climate-variable families in the gap matrix. The current readiness score is 0.40 on a 0-1 screening scale. That score should not be treated as scientific confidence. It is a bookkeeping signal that the deck has CO2 concentration, CO2 forcing, annual proxy CO2 emissions/removals, and a two-box temperature response, but still lacks the species-level inputs and calibrated uncertainty treatment needed for publication-grade climate claims.

In the delayed non-CO2 plus aerosol-unmasking stress case, no-AETHER constant emissions reaches about 3.24 C in 2100. AETHER with 58% rebound reaches about 2.38 C. AETHER plus net-zero 2050 and active full-forcing management reaches about 1.10 C in the screening emulator.

## Publication Rule

Use this deck as a handoff scaffold. Do not cite it as a FAIR result. The paper can say that AETHER now has a FAIR-ready data structure and a gap matrix for the next climate-modeling stage. It cannot say that FAIR has confirmed the temperature pathways.

## P0 Gaps

The current matrix still has 11 P0 gaps that are not usable screens. The most important are species-level CH4 and N2O trajectories, aerosol precursor emissions, lifecycle emissions as annual traces, zero-emissions commitment, carbon-cycle asymmetry calibration, uncertainty ensembles, and historical spin-up.

