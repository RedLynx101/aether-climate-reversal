# Clean-Energy Additionality and Market Design Notes

Last updated: 2026-06-09

This note adds the v0.28 clean-energy additionality screen. The earlier power-system model translated AETHER electricity demand into capacity, land, storage, and firm-power requirements. This layer asks a different question: if clean energy keeps getting cheaper and keeps scaling, how much of that clean buildout is actually delivered to AETHER as additional power rather than being blocked by grid queues, consumed by competing loads, or displaced from ordinary decarbonization?

Implementation: `analysis/scenario-models/aether_clean_energy_additionality_model.py`

Outputs:

- `analysis/tables/aether_clean_energy_additionality_cases.csv`
- `analysis/tables/aether_clean_energy_market_pull_comparators.csv`
- `analysis/tables/aether_clean_energy_policy_friction_matrix.csv`
- `analysis/tables/aether_clean_energy_additionality_summary.csv`
- `analysis/figures/clean_energy_additionality_gate.png`

## Current Read

| Scenario | Added clean generation | Additional AETHER power | Share of target | Result |
| --- | --- | --- | --- | --- |
| Status quo friction | 38,898 TWh/y | 2,995 TWh/y | 3% | fails |
| Market-unlocked buildout | 87,077 TWh/y | 19,429 TWh/y | 21% | fails |
| Dedicated AETHER buildout | 158,685 TWh/y | 68,552 TWh/y | 75% | fails |
| Abundance clean-power push | 202,291 TWh/y | 122,512 TWh/y | 134% | passes |
| Nonadditional grid pull | 87,077 TWh/y | 6,857 TWh/y | 7% | fails |

The market-unlocked case is not enough by itself. With annual clean additions growing 15% for 20 years, a 75% delivery factor, a 35% AETHER allocation after competing loads, and 85% additionality, the model gives about 19,429 TWh/year of additional AETHER clean power. That is about 21% of the 3 GJ/tCO2 balanced power gate.

The dedicated AETHER case gets closer but still misses the gate: about 68,552 TWh/year, or 75% of the target. Only the upper-tail abundance clean-power push passes the screen, at about 122,512 TWh/year, or 134% of the 3 GJ/tCO2 gate.

The nonadditional-grid case shows the failure boundary. It has the same nominal clean-energy expansion as the market-unlocked case, but weak additionality leaves only about 7% of the target as true additional AETHER clean power. That is not a clean climate-reversal program; it is a load-shifting program with a carbon-removal story attached.

## Comparators

| Comparator | TWh/y | Share of target |
| --- | --- | --- |
| 2025 global electricity growth | 850.0 | 0.93% |
| 2025 solar generation growth | 600.0 | 0.65% |
| IEA 2030 data-centre demand | 950.0 | 1.04% |
| Current global nuclear generation | 2,617.5 | 2.86% |
| IEA cost-effective geothermal 2050 case | 6,000.0 | 6.55% |
| Microsoft/Constellation Crane PPA | 6.8 | 0.01% |
| Google/Kairos advanced nuclear agreement | 4.1 | 0.00% |
| Helion/Microsoft fusion PPA | 0.4 | 0.00% |

Data centers matter because they are already pulling clean firm power forward, not because they solve the AETHER energy problem. IEA's projected 2030 data-centre demand is about 950 TWh/year, about 1.0% of the 3 GJ/tCO2 AETHER power gate. Current global nuclear generation and IEA's cost-effective 2050 geothermal case are also useful comparators: about 2.9% and 6.5% of the AETHER target, respectively.

## Interpretation

The pro-AETHER point is that clean energy no longer has to be imagined as purely regulatory charity. IRENA's cost data, Texas's wind and solar scale, California's high clean share, and data-center firm-power deals all show real market pull. The anti-hype point is that AETHER cannot count generic clean-energy growth as its own energy supply. It needs delivered, additional, low-carbon power matched to removal operations, storage geology, transmission, water, materials, and public consent.

The next model should replace these scalar filters with regional dispatch, hourly matching, interconnection queues, transmission corridors, storage duration, curtailment, marginal emissions, and colocation with geologic storage or mineral resources.

