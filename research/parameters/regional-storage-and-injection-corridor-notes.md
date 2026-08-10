# Regional Storage and Injection Corridor Notes

Last updated: 2026-06-09

This note adds the first regional storage and injection-corridor screen for AETHER. The prior storage-lifecycle layer showed that the 100 GtCO2/year gross portfolio sends about 54 GtCO2/year into geologic storage routes. This layer asks where that throughput might go and how many injection wells or corridors it implies.

Implementation: `analysis/scenario-models/aether_regional_storage_injection_model.py`

Outputs:

- `analysis/tables/aether_regional_storage_allocation.csv`
- `analysis/tables/aether_regional_storage_summary.csv`
- `analysis/tables/aether_injection_corridor_requirements.csv`
- `analysis/figures/regional_storage_injection_corridors.png`

## Source Anchors

USGS Circular 1386 remains the strongest source-backed storage anchor in the current repo. It estimates about 3,000 GtCO2 of mean technically accessible storage resource in U.S. onshore and state-water formations and reports that the U.S. Gulf Coast area represents 59% of national CO2 storage capacity.

NETL's Carbon Storage Atlas V is a broader North American storage-program source. It is useful for the repo because it connects storage-resource mapping to Regional Carbon Sequestration Partnerships and large-scale field projects, not only abstract pore volume.

EPA Class VI guidance is the operational constraint. Class VI wells inject CO2 into deep rock formations, including CO2 captured directly from air, and each U.S. Class VI well needs permitting through site closure. EPA's page emphasizes site characterization, plume and pressure-front modeling, area-of-review/corrective action, construction, monitoring, financial responsibility, emergency/remedial planning, reporting, public participation, and project phases.

## Current Model Read

The current screen assigns 54 GtCO2/year of geologic storage throughput across seven regional corridor archetypes. U.S. capacity is source-backed; non-U.S. capacity rows are scenario placeholders until upgraded with basin-level sources.

At 54 GtCO2/year, the U.S. source-backed 3,000 GtCO2 capacity anchor represents about 55.6 years of capacity if it were all technically and socially usable for AETHER. The full scenario proxy capacity represents about 92.6 years. Those numbers are intentionally not a siting claim. They only say that resource volume is not the first-order impossibility.

The hard part is throughput. At 1 MtCO2/year per injection well after pressure-management multipliers, the current scenario needs about 71,700 pressure-adjusted injection-well equivalents, or about 1,434 fifty-well corridor equivalents. At 0.25 MtCO2/year, that rises to about 286,800 wells. At 2 MtCO2/year, it is still about 35,850 wells. The U.S.-assigned rows alone imply about 32,800 Class VI permit-equivalent wells in the 1 Mt/year case.

## How To Use This Layer

This layer should keep the paper from treating geologic storage as a single global bucket. AETHER needs regional storage corridors, not just storage capacity. The next version should replace the placeholder regional rows with basin-level datasets: capacity, permeability, depth, pressure, brine handling, existing wells, induced-seismicity risk, pore-space ownership, Class VI or equivalent permitting, community consent, and monitoring cost.

