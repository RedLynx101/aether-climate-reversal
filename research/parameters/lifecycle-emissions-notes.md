# Lifecycle Emissions Notes

Last updated: 2026-06-09

This note documents the first explicit lifecycle-emissions screen for AETHER. The existing storage-lifecycle model applies route-level durability and lifecycle haircuts. The v0.27 model makes a narrower calculation: what happens when operational energy emissions and placeholder non-power LCA burdens are made explicit by pathway?

Implementation: `analysis/scenario-models/aether_lifecycle_emissions_model.py`

Outputs:

- `analysis/tables/aether_lifecycle_emissions_assumptions.csv`
- `analysis/tables/aether_lifecycle_emissions_by_pathway.csv`
- `analysis/tables/aether_lifecycle_emissions_summary.csv`
- `analysis/figures/lifecycle_emissions_net_credit_sensitivity.png`

## Current Read

| Power case | Lifecycle emissions | Durable after LCA | Creditable after LCA+MRV | Gross for 100 creditable |
| --- | --- | --- | --- | --- |
| 5 kgCO2/MWh | 11.0 Gt/y | 85.2 Gt/y | 66.3 Gt/y | 151 Gt/y |
| 25 kgCO2/MWh | 12.3 Gt/y | 83.9 Gt/y | 65.3 Gt/y | 153 Gt/y |
| 100 kgCO2/MWh | 17.2 Gt/y | 79.1 Gt/y | 61.3 Gt/y | 163 Gt/y |
| 250 kgCO2/MWh | 26.9 Gt/y | 69.5 Gt/y | 53.4 Gt/y | 187 Gt/y |

At 25 kgCO2/MWh, the 100 GtCO2/year gross portfolio produces about 12.3 GtCO2e/year of lifecycle emissions under the placeholder assumptions. It credits about 83.9 GtCO2/year after 100-year retention and about 65.3 GtCO2/year after MRV buffers. To credit 100 GtCO2/year at the same pathway mix, the model needs about 153 GtCO2/year gross removal.

The largest lifecycle-emissions contributors in the 25 kgCO2/MWh case are:

| Pathway | Gross | LCA emissions | Creditable after LCA+MRV |
| --- | --- | --- | --- |
| DACCS with geologic storage | 40.0 Gt/y | 3.7 Gt/y | 33.5 Gt/y |
| Enhanced weathering and surficial mineralization | 20.0 Gt/y | 2.8 Gt/y | 11.5 Gt/y |
| Ocean alkalinity enhancement | 15.0 Gt/y | 2.2 Gt/y | 7.1 Gt/y |
| BECCS | 10.0 Gt/y | 1.9 Gt/y | 6.9 Gt/y |
| Direct ocean capture and electrochemical mCDR | 4.0 Gt/y | 0.8 Gt/y | 2.6 Gt/y |

## Interpretation

The result is not that AETHER is impossible. It is that "clean energy" cannot be a slogan. The power must be genuinely low-carbon after firming, storage, transmission, curtailment, backup, and opportunity cost are counted. The non-power lifecycle terms are also not optional. Construction, sorbent/media replacement, mining, transport, storage, MRV, sensors, decommissioning, and waste streams all eat into the gross target.

This layer remains a placeholder. A publication-grade paper needs pathway-specific LCA datasets, regional embodied-emissions factors, recycling assumptions, energy-emissions traces, and uncertainty distributions. Until then, AETHER should report gross removal, durable after LCA, and creditable after LCA+MRV as different quantities.

