# Clean-Power Deliverability and P0 F2 Gate Notes

Last updated: 2026-06-10

This note upgrades the clean-power question from annual energy arithmetic to a falsification-style deliverability gate. The earlier model asked how much clean electricity could be built. This one asks how much of that electricity can actually count for AETHER after ordinary demand, interconnection, transmission, hourly matching, firm clean supply, and additionality.

The generated artifacts are:

- `analysis/scenario-models/aether_clean_power_deliverability_model.py`
- `analysis/tables/aether_clean_power_deliverability_cases.csv`
- `analysis/tables/aether_clean_power_deliverability_scale_targets.csv`
- `analysis/tables/aether_clean_power_deliverability_constraints.csv`
- `analysis/tables/aether_clean_power_deliverability_summary.csv`
- `analysis/figures/clean_power_deliverability_gate.png`

Current read: the 100 GtCO2/year, 3 GJ/tCO2 delivered clean-power gate is about 91,667 TWh/year after the current 10% delivery and firming penalty. After ordinary demand, grid deliverability, hourly matching, firming, and additionality, the market-unlocked case powers only about 6.4 GtCO2/year. Dedicated AETHER corridors and a firm clean-power backbone cluster near 44.9 and 44.7 GtCO2/year. The upper-tail AI energy-abundance case reaches about 135.6 GtCO2/year and is the only current case that clears the full energy gate; the nonadditional-grid failure case is essentially a rejection case at about 0.3 GtCO2/year.

The useful conclusion is narrow: "clean energy is getting cheap" is not enough. AETHER needs delivered, additional, low-carbon, industrially useful power. If a reviewer breaks that claim under a regional dispatch and interconnection model, the paper should cap feasible removal by delivered clean power instead of keeping the 100 GtCO2/year headline.

