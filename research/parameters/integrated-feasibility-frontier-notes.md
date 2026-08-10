# Integrated Feasibility Frontier Notes

Last updated: 2026-06-09

This note documents the first integrated AETHER feasibility screen. Earlier models treated energy, robots, cost, rebound, pathway allocation, and carbon-cycle response mostly as separate modules. That was useful, but it left a gap: a 100 GtCO2/year system can fail because any one physical layer does not arrive on time.

Implementation: `analysis/scenario-models/aether_integrated_feasibility_model.py`

Outputs:

- `analysis/tables/aether_integrated_feasibility_scenarios.csv`
- `analysis/tables/aether_integrated_feasibility_timepaths.csv`
- `analysis/tables/aether_integrated_feasibility_bottlenecks.csv`
- `analysis/figures/integrated_feasibility_screen_2046.png`
- `analysis/figures/integrated_capacity_paths_2026_2046.png`

## What the Screen Does

For each scenario, the model estimates a 2026-2046 capacity path. Actual removal capacity in a given year is the minimum of:

- the planned linear target toward 100 GtCO2/year;
- clean electricity available to AETHER;
- robot supply in service for AETHER;
- storage capacity available by that year;
- annual budget capacity at the learned cost per tonne.

It then calculates net removal after remaining emissions and Jevons-style rebound or delayed abatement.

## Current Scenario Read

The reference extrapolation fails. It does not have enough clean energy, robot capacity, storage, or budget to approach 100 GtCO2/year.

The fast-learning but energy-constrained case still fails the full target. Learning and automation help, but the clean-energy allocation is too small and storage arrives too slowly.

The AETHER portfolio push is the first case that passes the 100 GtCO2/year screen. It is not a forecast. It assumes the current v0.5 pathway portfolio energy intensity, aggressive clean-energy growth, a very large share of new clean generation dedicated to removal, enough robot manufacturing, a storage system built to about 105 GtCO2/year, annual spending near $9T, strong emissions decline, and rebound held to 15%.

The moonshot low-energy case passes with more headroom because energy intensity falls to 1.35 GJ/tCO2 and the annual cost floor falls to about $35/tCO2.

The high-rebound case shows why physical success is not enough. The buildout can mostly work while cheap removal still destroys most of the climate benefit if it induces emissions or delayed abatement.

## Interpretation

This model is a feasibility screen, not a prediction. Its job is to identify which assumptions have to be true at the same time. The important result is that no single optimistic assumption carries the project. AETHER needs simultaneous progress in energy, storage, cost, robots, emissions decline, and governance. AI and robotics matter because they can accelerate several of those layers, but they do not substitute for them.
