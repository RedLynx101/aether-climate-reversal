# Storage Lifecycle and Regionalization Notes

Last updated: 2026-06-09

This note documents the first storage-lifecycle filter for AETHER. Earlier model layers showed that a 100 GtCO2/year portfolio can be made to pass an integrated energy/robot/storage/budget screen under aggressive assumptions. That is not enough. A tonne captured at the contactor is not automatically a durable net tonne.

Implementation: `analysis/scenario-models/aether_storage_lifecycle_model.py`

Outputs:

- `analysis/tables/aether_storage_lifecycle_routes.csv`
- `analysis/tables/aether_storage_lifecycle_summary.csv`
- `analysis/figures/storage_lifecycle_net_durable_100y.png`
- `analysis/figures/storage_injection_processing_burden.png`

## Source Anchors

USGS Circular 1386 estimates about 3,000 GtCO2 of mean technically accessible geologic storage resource in the United States, with large regional concentration in coastal plains and the Gulf Coast. That supports the claim that storage resource is large, but not the claim that injection at 100 GtCO2/year is easy.

IPCC AR6 WGIII Chapter 6 gives the broader frame: theoretical global geologic storage potential is about 10,000 GtCO2, usable storage is lower than theoretical, desirable reservoirs need suitable depth/thickness/permeability, pressure can limit injection even when resource is large, and well-managed geologic storage has very low estimated leakage rates.

The USGS Anderson review is the caution note. Storage volumes large enough to matter for atmospheric CO2 are much larger than volumes injected so far. Pressure management, induced seismicity, property rights, liability, and cost are not side issues.

## Current Model Read

The model applies explicit lifecycle and durability haircuts to the v0.5 pathway portfolio. These haircuts are AETHER assumptions, not external facts. They represent embodied emissions, transport, mining, brine handling, feedstock accounting, monitoring error, reversal risk, and leakage or durability uncertainty.

Under the current assumptions, the 100 GtCO2/year gross portfolio credits materially less than 100 GtCO2/year on a 100-year durable basis. The portfolio therefore needs buffer capacity, lower lifecycle emissions, a more durable pathway mix, or stronger MRV before the paper can call the gross target a net durable target.

The injection-burden figure is intentionally rough. It uses one MtCO2/year well equivalents for geologic routes and ten MtCO2/year processing hubs for non-geologic routes. Real injection rates are reservoir-specific. The point is scale discipline: 40 GtCO2/year of DACCS is not just "some storage." It is tens of thousands of Mt-scale well equivalents or a smaller number of very large engineered hubs with pressure management, monitoring, pore-space rights, and public legitimacy.

## How To Use This Layer

The paper should report both gross removal and durable credited removal. Gross tonnes matter for industrial sizing. Durable credited tonnes matter for climate accounting. AETHER fails if those are casually treated as identical.
