# Cost Curve Model Spec

## Objective

Estimate how cost per tonne and annual capacity could change for major carbon-removal pathways.

## Core Variables

- `pathway`
- `year`
- `capacity_gtco2_per_year`
- `cost_usd_per_tco2`
- `learning_rate`
- `cumulative_capacity_gtco2`
- `energy_mwh_per_tco2`
- `capex_usd_per_tco2_year`
- `opex_usd_per_tco2`
- `storage_cost_usd_per_tco2`
- `mrv_cost_usd_per_tco2`

## First Version

Use simple learning curves:

`cost_t = initial_cost * (cumulative_capacity_t / initial_capacity) ^ learning_exponent`

Then stress-test across low/base/high learning rates.

## Required Caveats

- Learning curves do not remove material constraints.
- Cheap capture is not enough if storage, MRV, or energy is bottlenecked.
- Pathways have different durability and verification quality.

