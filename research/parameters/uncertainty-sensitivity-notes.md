# Uncertainty and Sensitivity Notes

Last updated: 2026-06-09

This note documents the first Monte Carlo uncertainty screen for AETHER. It should be treated as model triage, not a forecast. The distributions are explicit AETHER assumptions designed to answer a narrower question: when the main constraints vary together, which assumptions most strongly decide whether 100 GtCO2/year survives as durable climate reversal?

Implementation: `analysis/scenario-models/aether_uncertainty_sensitivity_model.py`

Outputs:

- `analysis/tables/aether_uncertainty_assumptions.csv`
- `analysis/tables/aether_uncertainty_samples.csv`
- `analysis/tables/aether_uncertainty_summary.csv`
- `analysis/tables/aether_uncertainty_bottlenecks.csv`
- `analysis/tables/aether_uncertainty_sensitivity.csv`
- `analysis/figures/uncertainty_success_probabilities.png`
- `analysis/figures/uncertainty_sensitivity_tornado.png`

## Current Read

The current v0.8 screen gives 0.8% probability of reaching at least 100 GtCO2/year gross capacity, but only 0.1% probability of crediting at least 100 GtCO2/year after lifecycle and 100-year durability haircuts. The probability of any positive net climate reversal after residual emissions and rebound is 56.0%. The stricter probability of net removal at least as large as current annual anthropogenic emissions is 1.5%.

The median durable credited removal is 30.8 GtCO2/year, with a P10-P90 range of 14.1-57.9 GtCO2/year. The median net result after residual emissions and rebound is 2.0 GtCO2/year, with a P10-P90 range of -12.6-23.0 GtCO2/year.

Among samples that fail the 100 GtCO2/year durable-credit target, the leading binding constraint is currently clean energy, binding in 67.4% of failed durable samples. That is not a permanent conclusion. It is a pointer to where the next model should become more physical.

## Sensitivity Screen

| Parameter | Correlation with net climate result | Interpretation |
|---|---:|---|
| Annual clean-addition growth | 0.48 | Growth rate for annual global clean-generation additions through 2046. |
| Residual emissions in 2046 | -0.44 | Positive emissions remaining when the AETHER system reaches industrial scale. |
| Rebound or delayed-abatement fraction | -0.37 | Extra emissions or delayed abatement induced by cheap removal. |
| Full-system energy intensity | -0.28 | Lower values make the clean-energy constraint less binding. |
| AETHER share of new clean generation | 0.27 | Share of new clean generation that can be allocated to AETHER after other demand claims. |
| 100-year durable credit fraction | 0.16 | Fraction of gross captured CO2 credited after lifecycle and 100-year durability haircuts. |

## Interpretation

This layer makes the plausibility claim more disciplined. AETHER should not be sold as "works if AI gets good." In the current model, AI and robotics help only if they improve several coupled distributions: clean-energy construction, storage throughput, delivered cost, robot-mediated deployment, lifecycle durability, and rebound control. If one layer remains mediocre, the model often fails even when the others improve.

The next upgrade should replace these hand-set triangular distributions with sourced distributions, scenario families, or expert elicitation. A publication-grade version should also handle correlations explicitly: cheap robots may lower cost and raise clean-energy buildout together, but social opposition could reduce storage and execution at the same time.

