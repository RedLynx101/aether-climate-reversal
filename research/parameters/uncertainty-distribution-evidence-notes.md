# Uncertainty Distribution Evidence Notes

Last updated: 2026-06-09

This note documents the v0.26 uncertainty distribution-evidence registry. The purpose is narrow: make the current Monte Carlo assumptions auditable before anyone treats the sampled probabilities as calibrated.

Implementation: `analysis/scenario-models/aether_uncertainty_distribution_evidence_model.py`

Outputs:

- `analysis/tables/aether_uncertainty_distribution_registry.csv`
- `analysis/tables/aether_uncertainty_distribution_upgrade_priorities.csv`
- `analysis/tables/aether_uncertainty_correlation_hypotheses.csv`
- `analysis/figures/uncertainty_distribution_evidence_gaps.png`

## Current Read

The registry maps 15 Monte Carlo input parameters. 11 are priority-1 upgrades, and 6 remain D-grade scenario or provisional inputs. The correlation table records 5 first-pass correlation families. The most urgent inputs include Annual clean-addition growth; Full-system energy intensity; Clean-energy deliverability; Delivered cost; 100-year durable credit fraction; Rebound or delayed-abatement fraction.

| Priority band | Count | Parameters | Next upgrade |
| --- | --- | --- | --- |
| high_priority_source_distribution | 7 | clean_addition_growth_rate;energy_gj_tco2;clean_deliverability_fraction;cost_usd_tco2;durability_fraction_100y;rebound_fraction_of_gross;storage_terminal_gtco2_y | Fit source-backed pathway or sector distributions and replace triangular ranges. |
| high_priority_assumption_correlation | 4 | aether_clean_share;execution_realization_fraction;robot_output_growth_rate;robots_per_mtco2_y_capacity | Run adversarial sensitivity, expert elicitation, and correlated scenario families before using probabilities rhetorically. |
| medium_priority_program_design | 4 | gross_overbuild_factor;residual_emissions_2046_gtco2_y;aether_robot_share;annual_budget_trillion_usd | Tie these variables to explicit governance, funding, and portfolio design branches. |
| lower_priority_documentation | 0 |  | Keep source notes current and promote to distributions when the surrounding model matures. |

## Correlation Hypotheses

| Correlation family | Parameters | Direction | Needed test |
| --- | --- | --- | --- |
| clean_power_coupling | clean_addition_growth_rate;aether_clean_share;clean_deliverability_fraction;energy_gj_tco2 | mixed | Regional power-system scenarios with interconnection, transmission, firming, and opportunity-cost accounting. |
| automation_coupling | robot_output_growth_rate;aether_robot_share;robots_per_mtco2_y_capacity;cost_usd_tco2;execution_realization_fraction | positive for capacity, negative for cost | Task-level robotics productivity model with manufacturing ramp and useful autonomous work-hour distributions. |
| storage_mrv_coupling | storage_terminal_gtco2_y;durability_fraction_100y;gross_overbuild_factor;execution_realization_fraction | mixed | Basin-level and pathway-level storage throughput, MRV, leakage, reversal, liability, and permit-duration distributions. |
| policy_rebound_coupling | rebound_fraction_of_gross;residual_emissions_2046_gtco2_y;annual_budget_trillion_usd;aether_clean_share | mixed | Policy scenarios for carbon pricing, citizen-owned commons, credit rules, and restrictions on dangerous emissions. |
| energy_cost_coupling | energy_gj_tco2;cost_usd_tco2;clean_addition_growth_rate;clean_deliverability_fraction | positive cost coupling, negative abundance coupling | Cost-stack model with regional electricity prices, capacity factors, firming cost, storage duration, and learning curves. |

## Interpretation

The prior uncertainty model is useful because it makes failure modes visible, but its triangular distributions are still hand-set. This registry prevents those ranges from hiding inside code. Each input now carries source keys, an evidence grade, a distribution status, a paper-use rule, and a next evidence task.

The highest-risk inputs are not just technical. Robot productivity, AETHER clean-power allocation, execution realization, rebound, storage terminal throughput, and delivered cost all combine technical feasibility with governance and market allocation. If those variables are sampled independently, the model can miss clustered success and clustered failure. The next version should replace this registry with sourced distributions, expert elicitation, and correlated scenario families.

