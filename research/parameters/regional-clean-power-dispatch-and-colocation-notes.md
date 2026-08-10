# Regional Clean-Power Dispatch and Colocation Notes

Last updated: 2026-06-10

This note upgrades the v0.35 clean-power deliverability gate into a first regional dispatch and colocation screen. It is still not a full power-market model. It is a disciplined intermediate step between annual clean-energy arithmetic and an 8760-hour regional dispatch model.

The generated artifacts are:

- `analysis/scenario-models/aether_regional_power_dispatch_model.py`
- `analysis/tables/aether_regional_power_region_assumptions.csv`
- `analysis/tables/aether_regional_power_dispatch_cases.csv`
- `analysis/tables/aether_regional_power_dispatch_by_region.csv`
- `analysis/tables/aether_regional_power_hourly_sample.csv`
- `analysis/tables/aether_regional_power_colocation_scorecard.csv`
- `analysis/tables/aether_regional_power_dispatch_summary.csv`
- `analysis/figures/regional_power_dispatch_gate.png`

Current read: the 100 GtCO2/year, 3 GJ/tCO2 clean-power gate remains about 91,667 TWh/year after the current delivery and firming penalty. The market regional reference supports about 15.5 GtCO2/year; dedicated AETHER corridors support about 47.9; a firm colocated backbone reaches about 64.3. Only the upper-tail AI energy-abundance dispatch case clears the 100 GtCO2/year screen, supporting about 122.0 GtCO2/year. Across 7 regional archetypes, 1 of 5 cases clear 100 GtCO2/year and 2 clear 50 GtCO2/year.

These regional values are not forecasts. The point is narrower and more useful: annual clean TWh is no longer enough as proof. AETHER needs delivered, additional, low-carbon industrial power that can serve high-uptime removal loads in places where storage geology, transmission corridors, firm clean supply, heat, water, and public-consent constraints fit together.

The next upgrade is an 8760-hour model with real regional resource traces, interconnection queue data, regional marginal emissions, storage duration, industrial heat, water constraints, and pathway-specific colocation requirements.

