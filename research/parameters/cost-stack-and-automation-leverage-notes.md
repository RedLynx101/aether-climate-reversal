# Cost Stack and Automation Leverage Notes

Last updated: 2026-06-09

This note documents the first AETHER cost-stack model. Earlier versions used whole-system cost assumptions like $84/tCO2 or $35/tCO2. That was useful for feasibility screens, but too coarse. This layer asks which cost buckets have to fall, which buckets AI/robotics can plausibly attack, and which floors remain even under extreme automation.

Implementation: `analysis/scenario-models/aether_cost_stack_model.py

Outputs:

- `analysis/tables/aether_cost_stack_components.csv
- `analysis/tables/aether_cost_stack_scenarios.csv
- `analysis/tables/aether_robot_labor_costs.csv
- `analysis/tables/aether_cost_reduction_requirements.csv
- `analysis/figures/cost_stack_by_scenario.png
- `analysis/figures/robot_hour_cost_scenarios.png

## Current Read

The current DAC-like scenario is about $606/tCO2, or $60.6 trillion/year at 100 GtCO2/year. The AETHER automation-push scenario is about $86/tCO2, or $8.6 trillion/year at 100 GtCO2/year and $10.1 trillion/year if the v0.7 gross-to-durable multiplier is used to credit 100 GtCO2/year. That is a 7.0 x reduction from the current DAC-like stack, but still civilization-scale spending.

The moonshot modular case is about $40/tCO2. The deep-abundance floor is about $24/tCO2. These cases are not predictions. They are boundary conditions showing that the cost target requires simultaneous compression in energy, plant capex, materials, storage, MRV, operations, and finance.

The full-splitting default remains unattractive at about $217/tCO2 even with advanced capture. Splitting makes storage compact, but it pushes the energy and product-handling cost stack back up. It should stay a specialized pathway unless there is a strong industrial reason to make solid carbon or oxygen handling valuable.

## Component Stack

| Scenario | Energy | Plant/contactors | Materials | Storage/logistics | MRV/liability | Robot O&M | Finance/overhead | Carbon/O2 handling | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Current DAC-like | $156 | $170 | $80 | $35 | $15 | $65 | $85 | $0 | $606 |
| AETHER automation push | $20 | $24 | $10 | $14 | $5 | $4 | $9 | $0 | $86 |
| Moonshot modular | $8 | $10 | $5 | $8 | $3 | $2 | $4 | $0 | $40 |
| Full splitting default | $116 | $20 | $8 | $8 | $5 | $5 | $10 | $45 | $217 |
| Deep abundance floor | $4 | $6 | $3 | $5 | $2 | $2 | $3 | $0 | $24 |

## Robot Hour Costs

| Robot case | Unit cost | Utilization | Lifetime | Direct robot-hour cost |
|---|---:|---:|---:|---:|
| Early humanoid / field robot | $200,000 | 4,000 h/y | 5 y | $25.14/h |
| Industrial scale robot | $100,000 | 5,500 h/y | 7 y | $7.88/h |
| AETHER factory robot | $50,000 | 6,500 h/y | 8 y | $3.28/h |
| Deep abundance robot | $25,000 | 7,500 h/y | 10 y | $1.12/h |

The robot result matters but should not be overread. Direct robot-hour cost can fall from about $25.14/hour to about $1.12/hour under aggressive assumptions. That can reduce construction, operations, inspection, and maintenance costs. It does not erase energy, storage, sorbents, MRV, insurance, or finance. AETHER fails if robot optimism is used as a substitute for the rest of the cost stack.

