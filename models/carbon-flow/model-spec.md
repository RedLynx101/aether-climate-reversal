# Carbon Flow Model Spec

## Objective

Estimate how atmospheric CO2 changes under different emissions and durable-removal scenarios.

## Core Variables

- `year`
- `gross_emissions_gtco2`
- `durable_removals_gtco2`
- `non_durable_removals_gtco2`
- `net_emissions_gtco2`
- `airborne_fraction`
- `carbon_cycle_rebound_factor`
- `atmospheric_co2_ppm`

## First Version

Start with a simple annual time-step model:

`net_emissions = gross_emissions - durable_removals`

Then translate net emissions to approximate ppm change using a documented conversion, with a warning that this is not a full carbon-cycle model.

## Later Version

Add:

- Ocean and land rebound behavior.
- Separate durability classes.
- Non-CO2 forcing notes.
- Delayed climate response.
- Uncertainty bands.

