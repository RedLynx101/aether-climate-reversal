# FAIR Forcing-Execution Notes

Last updated: 2026-06-10

This layer runs the FAIR package locally. It is a real FAIR 2.2.4 execution, but it is not yet a full species-emissions FAIR study. The model uses AETHER's existing CO2 forcing, aggregate non-CO2 forcing, and aggregate aerosol forcing paths from the FAIR-readiness handoff deck, initializes the temperature state from the screening emulator, and then runs FAIR's temperature response engine under three diagnostic climate configurations.

## Generated Artifacts

- `analysis/scenario-models/aether_fair_forcing_execution_model.py`
- `analysis/tables/aether_fair_forcing_temperature_paths.csv`
- `analysis/tables/aether_fair_forcing_summary.csv`
- `analysis/tables/aether_fair_forcing_config.csv`
- `analysis/tables/aether_fair_forcing_delta_vs_emulator.csv`
- `analysis/figures/fair_forcing_execution_comparison.png`

## Current Result

Using the central diagnostic configuration, the delayed non-CO2 plus aerosol-unmasking stress case reaches 4.14 C in 2100 without AETHER and 2.92 C with AETHER plus 58% rebound. AETHER plus net-zero 2050 and active full-forcing management reaches 1.15 C in 2100.

These numbers should be read as a package-executed forcing diagnostic. They are more serious than the homegrown emulator alone, but they still inherit the aggregate forcing inputs. The next publication-grade step is species-level emissions and concentrations for CH4, N2O, aerosol precursors, land-use forcing, lifecycle emissions, and uncertainty ensembles.

