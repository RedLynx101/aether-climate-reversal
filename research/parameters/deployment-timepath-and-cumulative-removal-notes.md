# Deployment Timepath and Cumulative Removal Notes

Last updated: 2026-06-09

This layer closes one of the obvious gaps in the working paper: endpoint capacity is not enough. AETHER has to say how annual deployment grows, when it crosses useful thresholds, how much durable removal accumulates, and whether net climate value survives residual emissions and rebound.

The model lives in 'analysis/scenario-models/aether_deployment_timepath_model.py'. The generated tables are:

- 'analysis/tables/aether_deployment_timepath_annual.csv'
- 'analysis/tables/aether_deployment_timepath_summary.csv'
- 'analysis/tables/aether_deployment_gate_crossings.csv'

The figure is 'analysis/figures/deployment_timepath_capacity_and_cumulative.png'.

## Current Read

- The linear 2046 reference reaches 66.7 GtCO2/year gross and 56.6 GtCO2/year durable credited removal in 2046, with cumulative durable credit of 367 GtCO2 by 2046.
- The abundance acceleration case reaches 57.0 GtCO2/year gross by 2040 and accumulates 2,017 GtCO2 durable credit by 2060, but this depends on very aggressive clean-energy, robot, storage, and learning assumptions.
- The energy-delayed case reaches only 18.3 GtCO2/year gross in 2046. That is the point of the scenario: AI and robotics optimism is not enough if power-system buildout is late.
- The rebound-failure case can build large gross capacity but records only -2.1 GtCO2/year net after residual emissions and rebound in 2046. Physical throughput is not the same as climate success.

## Use in the Paper

Use this layer to keep the argument honest. A 100 GtCO2/year endpoint sounds decisive, but what matters scientifically is the trajectory: cumulative durable credit, annual residual emissions, rebound or delayed abatement, and the time at which the system starts producing net-negative climate value.

The model is still hand-set. It needs regional energy buildout, storage-basin constraints, pathway-specific lifecycle assessment, construction-material supply chains, MRV failure rates, and correlated uncertainty before it can support publication-grade forecasts.

