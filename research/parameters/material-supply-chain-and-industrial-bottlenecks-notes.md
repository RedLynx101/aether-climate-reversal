# Material Supply Chain and Industrial Bottleneck Notes

Last updated: 2026-06-09

This note adds a material and industrial supply-chain screen to AETHER. It does not claim to be a complete bill of materials. It asks a narrower question: once the paper has enough energy, robots, storage, and cost arithmetic on the page, which material flows still look capable of breaking the optimistic case?

Implementation:

- `analysis/scenario-models/aether_material_supply_chain_model.py`
- `analysis/tables/aether_material_supply_chain_inputs.csv`
- `analysis/tables/aether_material_supply_chain_requirements.csv`
- `analysis/tables/aether_material_supply_chain_summary.csv`
- `analysis/figures/material_supply_chain_pressure.png`

## Current Read

The result is asymmetric. Ordinary structural mass is big, but it is not the most obvious physical impossibility. The moderate all-air contactor-frame case uses about 18.9 Mt/year of steel over a 20-year buildout, or about 1.0% of current crude steel production. The 3 GJ/tCO2 balanced clean-power case is more material-intensive: the current proxy uses about 68.8 Mt/year of steel and 2.8 Mt/year of copper over 20 years. The copper proxy is about 10.2% of the rounded refined-copper market proxy.

The more dangerous case is reactive media. Chatterjee and Huang's critique of very large DAC deployment reports NaOH makeup rates of 0.17-0.29 t per tCO2 in the DAC1 case, scaled from Realmonte et al.'s deep-mitigation DAC deployment assumptions. At 100 GtCO2/year, that would mean about 17,000-29,000 Mt/year of NaOH-equivalent reactive media. That is several times current global cement production. AETHER cannot use that as its base chemistry.

The optimized interpretation is stricter: the 40 GtCO2/year DACCS branch needs media losses pushed down by orders of magnitude. Even a 0.5% replacement-media case is about 200 Mt/year, and a 2% case is about 800 Mt/year. That may be industrially imaginable only if the media are cheap, benign, recyclable, low-carbon, and supported by automated manufacturing and recovery loops.

| Screen item | Annual material demand | Comparator share | Evidence class |
|---|---:|---:|---|
| Legacy NaOH 0.17 t/t | 17,000 Mt/y | 425% of world cement production proxy | source-backed critique scaled to AETHER target |
| Legacy NaOH 0.29 t/t | 29,000 Mt/y | 725% of world cement production proxy | source-backed critique scaled to AETHER target |
| DACCS media 0.5%/t | 200 Mt/y | 5% of world cement production proxy | scenario assumption informed by DAC material-risk literature |
| DACCS media 2.0%/t | 800 Mt/y | 20% of world cement production proxy | scenario assumption informed by DAC material-risk literature |
| Power copper | 3 Mt/y | 10.2% of world refined copper production proxy | scenario assumption with IEA critical-minerals context |
| Power steel | 69 Mt/y | 3.6% of world crude steel production | scenario assumption with source-backed global comparator |
| All-air contactor steel | 19 Mt/y | 1% of world crude steel production | scenario assumption with source-backed global comparator |
| Pipeline steel | 3 Mt/y | 0.1% of world crude steel production | scenario placeholder with source-backed global comparator |

## Research Consequence

The paper should treat material supply as a gate, not a footnote. The next version needs pathway-specific bills of materials: sorbents, solvents, membranes, catalysts, electrolyte, steel, cement, copper, aluminum, plastics, pumps, fans, compressors, heat exchangers, drilling materials, pipelines, sensors, and replacement media. It also needs embodied emissions and supply-chain competition with ordinary electrification, AI data centers, housing, transmission, and industrial decarbonization.

