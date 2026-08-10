# AETHER Modeling Plan

Project title: AETHER: Atmospheric Engineering Through High-Energy Removal

## Model 1: Carbon Stock-Flow

Goal: estimate atmospheric CO2 change under emissions and removal scenarios.

Inputs:

- Annual anthropogenic CO2 emissions.
- Annual durable removals.
- Conventional land sink assumptions.
- Carbon-cycle rebound or airborne fraction assumptions.
- Target atmospheric CO2 range.

Outputs:

- Net emissions.
- Approximate ppm trajectory.
- Time to peak, stabilization, and drawdown.
- Sensitivity to rebound and removal durability.

Notes:

- The simple conversion `1 ppm atmospheric CO2 ~= 7.8 GtCO2 in air` is useful but incomplete because oceans and land exchange carbon with the atmosphere.
- The model should show both a simple mass-balance view and a more cautious rebound-adjusted view.

Current implementation: `analysis/scenario-models/aether_carbon_cycle_model.py`, with outputs in `analysis/tables/aether_carbon_cycle_pathways.csv`, `analysis/tables/aether_carbon_cycle_summary.csv`, and `analysis/figures/carbon_cycle_atmospheric_co2_pathways.png`.

Current upgrade: analysis/scenario-models/aether_state_dependent_carbon_model.py now stress-tests removal effectiveness across fixed, optimistic, conservative, and asymmetry-stress cases. Next upgrade: replace both reduced-form screens with a FAIR-class or Earth-system-model workflow that handles endogenous carbon-cycle feedbacks, temperature response, ocean chemistry, and removal/emission asymmetry.

## Model 2: Removal Pathway Cost Curves

Goal: compare cost decline and scale-up pathways for durable carbon removal.

Candidate pathways:

- Direct air capture with geologic storage.
- Bioenergy with carbon capture and storage.
- Biochar and bio-oil storage.
- Enhanced rock weathering.
- Mineralization.
- Ocean alkalinity enhancement.
- Direct ocean capture.
- Point-source capture for residual industrial emissions.

Inputs:

- Current cost per tonne.
- Learning rate.
- Deployment growth rate.
- Energy intensity.
- Capital intensity.
- Storage and monitoring cost.
- Maximum plausible scale.

Outputs:

- Cost per tonne over time.
- Total annual removal capacity.
- Energy demand.
- Capital requirement.
- Constraint flags.

## Model 3: Robotics and Automation Scaling

Goal: test whether robotics and AI could materially reduce the cost and speed constraints of carbon-removal infrastructure.

Inputs:

- Robot unit cost.
- Useful life.
- Hours operated per year.
- Maintenance cost.
- Task productivity.
- Energy use.
- Human supervision ratio.
- Manufacturing ramp rate.
- Learning rate.

Outputs:

- Effective hourly robot labor cost.
- Infrastructure buildout acceleration.
- Sensitivity to robot reliability and maintenance.
- Scenario curves for robot fleet size and productive capacity.

Important caution:

Humanoid robots are only one automation category. The research should also model specialized machinery: autonomous mining equipment, drilling rigs, construction robots, industrial manipulators, inspection drones, sensor networks, and automated factories.

## Model 4: Energy System Coupling

Goal: estimate whether carbon removal competes with or complements clean-energy expansion.

Inputs:

- Clean electricity buildout.
- Capacity factor by technology.
- Storage and transmission constraints.
- Energy intensity of removal pathways.
- Heat versus electricity requirements.
- Curtailment and surplus-energy availability.

Outputs:

- Energy demand for removal.
- Share of clean generation consumed by removal.
- Break-even points where removal becomes energy-feasible.
- Sensitivity to energy price and clean-energy growth.

## Model 5: Storage State and Durability

Goal: compare storage pathways by density, durability, leakage risk, monitoring need, and conversion cost.

Storage forms:

- Gaseous CO2.
- Liquid CO2.
- Supercritical CO2.
- Geologic storage.
- Mineral carbonate.
- Biochar.
- Bio-oil.
- Solid carbon.
- Biomass and soil carbon.
- Ocean bicarbonate/carbonate forms.

Outputs:

- Storage capacity by pathway.
- Expected permanence.
- Monitoring and liability burden.
- Energy and material conversion costs.
- Failure modes.

## Model Outputs For The Paper

The paper should show:

- Removal capacity curves over time.
- Cost-per-tonne decline scenarios.
- Clean-energy requirement bands.
- Robot fleet and unit-cost sensitivity.
- Storage-capacity bottleneck charts.
- Atmospheric CO2 trajectories under conservative, base, and aggressive assumptions.

## Model 6: Learning, Scale, and Rebound

Goal: estimate how fast costs can fall and when rebound effects erase net-negative outcomes.

Inputs:

- Current engineered-removal capacity.
- Target removal capacity.
- Initial cost per tonne.
- Learning rate per cumulative capacity doubling.
- Energy price and energy intensity.
- Storage and MRV floors.
- Rebound or delayed-abatement fraction.
- Plant scale and capex scaling exponent.

Outputs:

- Capacity doublings required to reach 100 GtCO2/year.
- Learned cost per tonne under 10-40% learning rates.
- Bounded cost after energy, storage, and MRV floors.
- Plant count and relative unit capex by hub size.
- Net removal after Jevons-style rebound.

Current implementation: `analysis/scenario-models/aether_transition_model.py`.

## Model 7: Robot Fleet Requirements

Goal: separate useful robotics optimism from vague humanoid hype.

Inputs:

- Robots per MtCO2/year removal capacity.
- Buildout horizon.
- Current global industrial robot installation baseline.
- Figure Robotics production-rate leads, treated as unresolved scenario calibration.

Outputs:

- Implied AETHER robot fleet.
- Annual robot production over a 20-year buildout.
- Multiples of 2024 global industrial robot installations.
- Multiples of an annualized 250/month single-company Figure lead.

Current implementation: `analysis/scenario-models/aether_transition_model.py` and `research/parameters/robotics-scaling-notes.md`.




## Model 8: Pathway Portfolio

Goal: prevent the 100 GtCO2/year target from hiding behind a single magic pathway.

Outputs:

- Portfolio allocation across DACCS, enhanced weathering, ocean alkalinity, BECCS, biochar, afforestation/reforestation, and direct ocean/electrochemical CDR.
- Weighted cost, energy, average power, central assessment gap, and bottleneck list.
- Figure comparing optimized allocation against central assessed potential ranges.

Current implementation: `analysis/scenario-models/aether_pathway_portfolio_model.py`, with outputs in `analysis/tables/aether_pathway_portfolio_allocation.csv`, `analysis/tables/aether_pathway_portfolio_summary.csv`, and `analysis/figures/pathway_portfolio_100gt.png`.

## Model 9: Integrated Feasibility Frontier

Goal: evaluate whether the 100 GtCO2/year target survives simultaneous constraints rather than isolated optimism.

Inputs:

- Energy intensity by scenario.
- Clean-electricity addition growth and AETHER allocation share.
- Robot production growth, service life, and robots per MtCO2/year capacity.
- Storage terminal capacity and storage ramp speed.
- Initial and floor cost per tonne with learning.
- Annual budget.
- 2046 residual emissions and rebound fraction.

Outputs:

- Scenario-level feasibility screen.
- 2026-2046 capacity path.
- Binding constraint by year.
- Integrated resource adequacy ratios.
- Net removal after emissions and rebound.

Current implementation: `analysis/scenario-models/aether_integrated_feasibility_model.py`.

## Model 10: Storage Lifecycle and Regionalization

Goal: separate gross captured CO2 from lifecycle-adjusted durable credited removal.

Inputs:

- Pathway portfolio allocation.
- Storage route and regional resource proxy.
- Injection or processing terminal capacity.
- Per-route storage energy penalty.
- Lifecycle penalty fraction.
- Annual leakage, reversal, or durability-risk rate.
- Monitoring duration.
- One-Mt/year injection well-equivalent assumption or ten-Mt/year processing hub proxy.

Outputs:

- Gross allocation by pathway.
- Lifecycle-adjusted removal.
- 100-year durable credited removal.
- Gross-to-net multiplier by route.
- Additional storage energy penalty.
- Injection well or processing-hub deployment burden.

Current implementation: `analysis/scenario-models/aether_storage_lifecycle_model.py`.

## Model 11: Uncertainty and Sensitivity

Goal: test whether the AETHER feasibility claim survives coupled uncertainty rather than isolated scenario optimism.

Inputs:

- Full-system energy intensity.
- Clean-generation addition growth, AETHER allocation share, and deliverability.
- Robot-production growth, AETHER robot allocation share, and robots per MtCO2/year capacity.
- Terminal storage throughput.
- Delivered cost per tonne and annual budget.
- Gross overbuild and execution realization.
- 100-year lifecycle/durability credit fraction.
- Residual emissions and rebound or delayed-abatement fraction.

Outputs:

- Probability-like screen for gross 100 GtCO2/year capacity.
- Probability-like screen for durable credited 100 GtCO2/year removal.
- Probability-like screen for positive net climate reversal after residual emissions and rebound.
- P10/P50/P90 bands for gross capacity, durable credited removal, and net climate result.
- Bottleneck shares across energy, robot supply, storage, budget, and execution.
- First-order sensitivity correlations.

Current implementation: `analysis/scenario-models/aether_uncertainty_sensitivity_model.py`.

Caution: this is not a forecast. The current distributions are explicit AETHER assumptions. The next version should replace them with sourced distributions, correlated scenarios, expert elicitation, and stronger uncertainty methods.




## Model 12: Cost Stack and Automation Leverage

Goal: separate whole-system $/tCO2 assumptions into the cost buckets AI, robotics, energy abundance, and learning curves can actually affect.

Inputs:

- Capture and splitting energy intensity.
- Clean-electricity price.
- Plant/contactors capex amortization.
- Sorbent and material replacement.
- Compression, transport, and storage cost.
- MRV, insurance, and liability cost.
- Robot operations and maintenance cost.
- Finance, permitting, and overhead.
- Carbon and oxygen product-handling cost when CO2 is split.
- Robot unit cost, utilization, lifetime, maintenance, energy use, and supervision overhead.

Outputs:

- Delivered cost stack by scenario.
- Annual cost at 100 GtCO2/year gross removal.
- Annual cost after gross overbuild needed to credit 100 GtCO2/year durable removal under the current lifecycle ratio.
- Cost-reduction factors relative to a current DAC-like stack.
- Direct robot-hour cost scenarios.
- Visual separation between automatable cost buckets and hard floors.

Current implementation: `analysis/scenario-models/aether_cost_stack_model.py`.

Caution: this is still a scenario model. The next version needs sourced distributions for each cost bucket and should connect component costs to pathway-specific technologies.



## Model 13: Parameter Evidence Database

Goal: keep model assumptions from silently becoming factual claims.

Inputs:

- Source-register keys.
- Model-generated outputs.
- Scenario assumptions.
- Provisional leads.
- Evidence grades.
- Next actions for weak assumptions.

Outputs:

- `data/parameters/aether_parameter_evidence.csv`
- `analysis/tables/aether_parameter_evidence_summary.csv`

Rule: parameters with `C` or `D` evidence grades can drive scenarios but should not be stated as established facts in the manuscript.










## Model 14: Pathway Source-Range Screen

Goal: prevent the 100 GtCO2/year portfolio from hiding outside the assessed ranges for individual CDR pathways.

Inputs:

- IPCC AR6 WGIII Table TS.7 pathway cost, potential, maturity, risk, and tradeoff ranges.
- National Academies ocean CDR research and scale-up cautions.
- Current AETHER portfolio allocation.

Outputs:

- `data/parameters/aether_cdr_pathway_source_ranges.csv`
- `analysis/tables/aether_pathway_source_gap_analysis.csv`
- `analysis/figures/pathway_source_ranges_vs_aether.png`

Rule: an allocation at the upper edge of an assessed range is allowed as a stress test, but the paper must label it as an upper-tail dependency rather than a central forecast.






## Model 15: Robotics Evidence and Task Productivity

Goal: replace vague robotics optimism with source-backed unit-cost, factory-capacity, fleet-scale, duty-cycle, and useful-work assumptions.

Inputs:

- IFR industrial robot installation and stock statistics.
- Company-reported deployed robot fleets and humanoid factory capacities.
- Vendor product pages for low-end humanoid price and runtime anchors.
- AETHER robot-fleet proxy assumptions.
- Task-family productivity placeholders.

Outputs:

- `data/parameters/aether_robotics_evidence.csv`
- `analysis/tables/aether_robotics_scale_comparison.csv`
- `analysis/tables/aether_robotics_task_ladder.csv`
- `analysis/figures/robotics_scale_anchors_vs_aether.png`

Rule: robot unit price is not a substitute for useful autonomous work. Future versions should model task-hours, reliability, maintenance, downtime, supervision, replacement, and environment-specific productivity.
















## Model 16: Conversion and Storage-State Ledger

Goal: make physical conversion arithmetic auditable instead of scattered across prose.

Inputs:

- CO2, carbon, O2, and MgCO3 stoichiometry.
- CO2 gas, supercritical CO2, graphite-like carbon, liquid oxygen, and magnesite-equivalent densities.
- CO2 splitting thermodynamic floor.
- Current natural graphite production and resource comparators.
- Split-fraction sensitivity from 0% to 100%.

Outputs:

- `data/parameters/aether_conversion_constants.csv`
- `analysis/scenario-models/aether_conversion_storage_ledger_model.py`
- `analysis/tables/aether_conversion_state_ledger.csv`
- `analysis/tables/aether_splitting_fraction_sensitivity.csv`
- `analysis/figures/conversion_storage_ledger_100gt.png`

Rule: compact storage volume is not the same as feasible storage. Solid carbon is compact but energy-expensive; mineral carbonate is durable but material- and kinetics-constrained; gas CO2 is physically too bulky; supercritical geologic storage is dense but governed by geology, injection rates, monitoring, pressure, liability, and public acceptance.

























## Model 17: Technology Acceleration and Order-of-Magnitude Frontier

Goal: translate the AI/robotics abundance premise into cost-bucket reduction requirements.

Inputs:

- Current DAC-like, AETHER automation-push, moonshot modular, full-splitting, and deep-abundance cost stacks.
- Bucket-level cost components.
- U.S. total R&D and global energy R&D comparators.
- Illustrative $100B/year, $300B/year, and $1T/year AETHER RD&D program budgets.

Outputs:

- `analysis/scenario-models/aether_technology_acceleration_model.py`
- `analysis/tables/aether_cost_improvement_frontier.csv`
- `analysis/tables/aether_cost_bucket_reduction_factors.csv`
- `analysis/tables/aether_trillion_rd_program_comparators.csv`
- `analysis/figures/technology_acceleration_frontier.png`
- `research/parameters/technology-acceleration-and-order-of-magnitude-notes.md`

Rule: a cost reduction is only credible if the model identifies which bucket moves and why. AI and robotics can accelerate science, manufacturing, construction, monitoring, logistics, and maintenance, but they do not delete thermodynamic, storage, MRV, liability, or governance floors.















## Model 18: Power-System Buildout and Firm Energy

Goal: translate AETHER electricity demand into installed clean-power capacity, annual buildout rates, firm-power requirements, land proxies, and short-duration flexibility proxies.

Inputs:

- AETHER electricity demand cases.
- Solar, wind, nuclear, and geothermal capacity factors.
- Gross-generation penalties for balanced and VRE-heavy portfolios.
- Solar land-use proxy.
- Current nuclear and geothermal scale comparators.
- Utility-scale battery cost and deployment anchors.

Outputs:

- `analysis/scenario-models/aether_power_system_buildout_model.py`
- `analysis/tables/aether_power_supply_cases.csv`
- `analysis/tables/aether_power_system_tech_assumptions.csv`
- `analysis/tables/aether_clean_power_portfolio_requirements.csv`
- `analysis/tables/aether_clean_power_portfolio_summary.csv`
- `analysis/figures/clean_energy_capacity_requirements_100gt.png`
- `research/parameters/power-system-buildout-and-firm-energy-notes.md`

Rule: total TWh is not enough. AETHER feasibility requires installed capacity, capacity factors, storage/flexibility, transmission, siting, and firm clean power to work simultaneously.

















## Model 19: Air-Contactor, Sorbent, and Plant-Scale Hardware

Goal: turn atmospheric concentration into physical hardware scale.

Inputs:

- Atmospheric CO2 ppm.
- CO2 mass per cubic meter of air.
- Capture fraction.
- Face velocity.
- Pressure drop and fan efficiency.
- Operating uptime.
- Current DAC facility capacity comparators.
- Sorbent working capacity, cycle time, uptime, and lifetime.

Outputs:

- `analysis/scenario-models/aether_air_contactor_scale_model.py`
- `analysis/tables/aether_air_contactor_scale.csv`
- `analysis/tables/aether_sorbent_inventory_scale.csv`
- `analysis/tables/aether_air_contactor_scale_summary.csv`
- `analysis/figures/air_contactor_physical_scale_100gt.png`
- `research/parameters/air-contactor-and-sorbent-scale-notes.md`

Rule: energy demand alone is insufficient. DAC at AETHER scale must move enough air across enough active surface with low pressure drop, high availability, manageable sorbent replacement, and credible factory throughput.



















## Model 20: Feasibility Gate Synthesis

Goal: turn the model suite into a scientist-readable decision frame.

Inputs:

- Carbon-cycle outcomes.
- Pathway portfolio potential.
- Power-system capacity requirements.
- Air-contactor and sorbent scale.
- Storage lifecycle and durable credit.
- Cost-stack and technology-acceleration frontier.
- Robotics evidence and integrated feasibility screens.
- Uncertainty and rebound/governance screens.

Outputs:

- `analysis/scenario-models/aether_feasibility_synthesis_model.py`
- `analysis/tables/aether_feasibility_gate_scorecard.csv`
- `analysis/tables/aether_research_program_milestones.csv`
- `analysis/tables/aether_presentation_key_numbers.csv`
- `analysis/figures/feasibility_gate_scorecard.png`
- `research/parameters/feasibility-gate-scorecard-notes.md`

Rule: AETHER should be presented as a conditional infrastructure research program with go/no-go gates, not as a forecast that assumes every optimistic assumption becomes true.









































## Model 21: Manuscript Evidence and Review Readiness

Goal: keep manuscript claims aligned with their evidence class before the paper is shared with scientists.

Inputs:

- Source-backed anchors.
- Derived model outputs.
- Scenario assumptions.
- Provisional technology leads.
- Governance hypotheses.
- Reviewer-facing upgrade requirements.

Outputs:

- `analysis/scenario-models/aether_manuscript_evidence_model.py`
- `analysis/tables/aether_manuscript_claim_evidence_matrix.csv`
- `manuscript/review/aether_review_readiness.md`

Rule: an optimistic AETHER scenario may be useful, but the paper should never let a scenario assumption read like a source-backed fact.


































## Model 22: Prior Art and Contribution Boundary

Goal: prevent AETHER from overclaiming novelty and make its actual contribution legible to scientific reviewers.

Outputs:

- `analysis/scenario-models/aether_prior_art_positioning_model.py`
- `analysis/tables/aether_prior_art_positioning_matrix.csv`
- `manuscript/review/aether_prior_art_positioning.md`

Rule: AETHER should claim a coupled feasibility-boundary contribution, not first invention of CDR, DAC, automation, AI materials discovery, or atmospheric commons governance.

























## Model 23: Deployment Timepaths

Goal: make AETHER's timing claims explicit. Endpoint capacity is insufficient; the paper needs annual trajectories, cumulative durable credit, residual emissions, rebound, and net climate value.

Inputs:

- Capacity ramp form and target year.
- Capture/storage energy intensity.
- Dedicated clean-generation additions and AETHER allocation share.
- Robot production growth, service life, and robots per MtCO2/year capacity.
- Storage ramp, annual budget, learning rate, cost floor, and durable-credit fraction.
- Residual emissions path and rebound or delayed-abatement fraction.

Outputs:

- Annual gross removal, durable credit, energy, cost, residual emissions, rebound, and net value.
- Cumulative gross removal, durable credit, net value, energy, and cost.
- First-year threshold crossings for 10, 50, and 100 GtCO2/year gross removal; 100 GtCO2/year durable credit; and positive net removal.

Current implementation: `analysis/scenario-models/aether_deployment_timepath_model.py`.

## Model 24: Regional Storage and Injection Corridors

Goal: replace a single geologic-storage bucket with a first regional throughput screen.

Inputs:

- Geologic-storage target from the storage-lifecycle layer.
- U.S. storage-resource anchor from USGS Circular 1386.
- Scenario placeholder regions for non-U.S. storage until basin datasets are added.
- Assigned injection by region.
- Pressure-management multiplier.
- Injection-well productivity case.
- Corridor size proxy.
- Regulatory basis and source keys.

Outputs:

- Regional allocation table.
- Injection-well and corridor requirements under productivity cases.
- U.S. Class VI permit-equivalent well count for U.S.-assigned rows.
- Capacity-years at assigned throughput.
- Evidence-class separation between source-backed capacity anchors and scenario placeholders.

Current implementation: `analysis/scenario-models/aether_regional_storage_injection_model.py`.

## Model 25: Equation Ledger and Reproducibility

Goal: make the main equations and unit transformations auditable before the paper is shared outside the repo.

Inputs:

- Source-backed constants and bookkeeping conventions.
- Scenario targets from the current model suite.
- Stoichiometry, energy conversion, storage-volume, durability, injection, robot-cost, learning-curve, rebound, and contactor-area formulas.

Outputs:

- `analysis/scenario-models/aether_equation_ledger_model.py`
- `analysis/tables/aether_model_equation_ledger.csv`
- `analysis/tables/aether_dimensioned_unit_checks.csv`
- `manuscript/appendices/aether_model_equations_and_reproducibility.md`
- `docs/reproducibility.md`

Rule: every headline model claim should trace to a source-backed anchor, a derived equation, or a named model output. If a claim cannot be traced, it should be treated as a research question rather than a result.

## Model 26: Material and Industrial Supply Chain

Goal: keep AETHER from treating energy, robots, and storage as sufficient. The model screens structural materials, reactive media, power-system metals, pipeline steel, and global production comparators.

Inputs:

- Global steel production comparator.
- Global cement production comparator.
- Refined-copper market proxy.
- Air-contactor face-area outputs from the physical scale model.
- 3 GJ/tCO2 balanced clean-power capacity output.
- Reactive-media replacement rates for legacy and optimized DAC cases.
- Pipeline-corridor steel proxy for the geologic-storage branch.

Outputs:

- `analysis/scenario-models/aether_material_supply_chain_model.py`
- `analysis/tables/aether_material_supply_chain_inputs.csv`
- `analysis/tables/aether_material_supply_chain_requirements.csv`
- `analysis/tables/aether_material_supply_chain_summary.csv`
- `analysis/figures/material_supply_chain_pressure.png`
- `research/parameters/material-supply-chain-and-industrial-bottlenecks-notes.md`

Rule: ordinary structural mass can be modeled as an industrial allocation, but high-makeup reactive media and copper/grid hardware are gating constraints until source-backed bills of materials and recycling loops are built.

## Model 27: MRV and Credit Integrity

Goal: prevent AETHER from treating gross captured tonnes as creditable climate value. The model distinguishes gross removal, lifecycle-durable credit, MRV-filtered creditable removal, liability cost, and gross overbuild required for 100 GtCO2/year creditable removal.

Inputs:

- Current AETHER pathway portfolio allocation.
- Current storage-lifecycle durable-credit table.
- Provisional pathway-specific measurement, method, reversal, leakage, invalidation, and liability-cost buffers.
- Regulatory and quality anchors from EPA Class VI/Subpart RR, EU CRCF, Oxford durable-storage principles, State of CDR, and National Academies ocean CDR research framing.

Outputs:

- `analysis/scenario-models/aether_mrv_credit_integrity_model.py`
- `analysis/tables/aether_mrv_credit_integrity_assumptions.csv`
- `analysis/tables/aether_mrv_credit_integrity_by_pathway.csv`
- `analysis/tables/aether_mrv_credit_integrity_summary.csv`
- `analysis/figures/mrv_credit_integrity_overbuild.png`
- `research/parameters/mrv-and-credit-integrity-notes.md`

Rule: if a tonne cannot survive measurement, attribution, durability, reversal, invalidation, and liability accounting, it should not be used as a creditable AETHER tonne.

## Model 28: Climate Response Proxy

Goal: connect AETHER atmospheric CO2 paths to a first forcing and temperature-response screen without pretending to run a full climate model.

Inputs:

- Reduced-form atmospheric CO2 ppm paths from `aether_carbon_cycle_model.py`.
- IPCC AR6 WGI CO2-doubling effective radiative forcing anchor.
- IPCC AR6 TCR/ECS context for transparent temperature scaling.
- A publication-upgrade target based on FAIR or an Earth-system model.

Outputs:

- `analysis/scenario-models/aether_climate_response_model.py`
- `analysis/tables/aether_climate_response_pathways.csv`
- `analysis/tables/aether_climate_response_summary.csv`
- `analysis/figures/climate_response_temperature_proxy.png`
- `research/parameters/climate-response-and-temperature-proxy-notes.md`

Rule: this model is a CO2-only proxy. It is allowed for internal screening and manuscript caveats; it is not allowed as a final warming forecast. Publication-grade claims need FAIR or Earth-system modeling with non-CO2 forcing, aerosols, ocean heat uptake, zero-emissions commitment, ocean chemistry, lifecycle emissions, and regional impacts.

## Model 29: Uncertainty Distribution Evidence Registry

Goal: make the uncertainty model auditable before treating any Monte Carlo share as a probability claim.

Inputs:

- `analysis/tables/aether_uncertainty_assumptions.csv`
- Current source-register keys for energy, clean power, robotics, storage, cost, MRV, rebound, and governance.
- Reviewer-facing evidence classes: source-informed range, scenario assumption, provisional technology lead, derived screen, and governance hypothesis.

Outputs:

- `analysis/scenario-models/aether_uncertainty_distribution_evidence_model.py`
- `analysis/tables/aether_uncertainty_distribution_registry.csv`
- `analysis/tables/aether_uncertainty_distribution_upgrade_priorities.csv`
- `analysis/tables/aether_uncertainty_correlation_hypotheses.csv`
- `analysis/figures/uncertainty_distribution_evidence_gaps.png`
- `research/parameters/uncertainty-distribution-evidence-notes.md`

Rule: this layer improves traceability, not calibration. It is allowed to say which assumptions are weak, provisional, or correlated. It is not allowed to report the Monte Carlo shares as publication-grade probabilities until the distributions are source-backed or elicited and the correlation structure is implemented.

## Model 30: Lifecycle Emissions Screen

Goal: stop the paper from treating gross removal as net climate value when energy emissions, embodied emissions, media replacement, transport, storage, decommissioning, retention, and MRV buffers all matter.

Inputs:

- `analysis/tables/aether_pathway_portfolio_allocation.csv`
- `analysis/tables/aether_storage_lifecycle_routes.csv`
- `analysis/tables/aether_mrv_credit_integrity_by_pathway.csv`
- Power-emissions cases at 5, 25, 100, and 250 kgCO2/MWh.
- Pathway placeholder non-power LCA terms for construction, media replacement, transport/storage, and decommissioning.

Outputs:

- `analysis/scenario-models/aether_lifecycle_emissions_model.py`
- `analysis/tables/aether_lifecycle_emissions_assumptions.csv`
- `analysis/tables/aether_lifecycle_emissions_by_pathway.csv`
- `analysis/tables/aether_lifecycle_emissions_summary.csv`
- `analysis/figures/lifecycle_emissions_net_credit_sensitivity.png`
- `research/parameters/lifecycle-emissions-notes.md`

Rule: these are placeholder LCA assumptions. They are allowed for screening, but publication-grade net-removal claims need pathway-specific LCA datasets, regional embodied-emissions factors, energy-emissions traces, recycling and replacement schedules, decommissioning, and uncertainty distributions.

## Model 31: Clean-Power Additionality and Market Design

Goal: prevent the paper from counting generic clean-energy growth as AETHER supply. AETHER power must be delivered, additional, low-carbon on the margin, and available after competing loads.

Inputs:

- `analysis/tables/aether_clean_power_portfolio_summary.csv`
- Current clean-energy growth anchors.
- Delivery factors for interconnection, transmission, siting, and permitting.
- AETHER allocation fractions after ordinary electrification, data centers, industrial heat, desalination, hydrogen, synthetic fuels, and fossil displacement make their claims.
- Additionality fractions for whether AETHER power is truly new rather than displaced from other decarbonization uses.
- Market-pull comparators for data centers, nuclear, geothermal, and fusion.

Outputs:

- `analysis/scenario-models/aether_clean_energy_additionality_model.py`
- `analysis/tables/aether_clean_energy_additionality_cases.csv`
- `analysis/tables/aether_clean_energy_market_pull_comparators.csv`
- `analysis/tables/aether_clean_energy_policy_friction_matrix.csv`
- `analysis/tables/aether_clean_energy_additionality_summary.csv`
- `analysis/figures/clean_energy_additionality_gate.png`
- `research/parameters/clean-energy-additionality-and-market-design-notes.md`

Rule: a tonne is not clean just because it used electricity from a grid with some clean generation. The power accounting must show delivered additional clean supply or explicitly label the case as a failure boundary.

## Model 24: Dynamic Climate Emulator

Goal: move beyond a static CO2-only temperature proxy without pretending to run a publication-grade climate model.

Inputs:

- Reduced-form atmospheric CO2 ppm paths from `analysis/tables/aether_carbon_cycle_pathways.csv`.
- AR6 CO2-doubling forcing anchor of 3.93 W/m2.
- ECS = 3.0 deg C and TCR about 1.8 deg C calibration target.
- Scenario non-CO2 positive forcing paths.
- Scenario aerosol forcing paths.

Outputs:

- Annual CO2 forcing, non-CO2 forcing, aerosol forcing, total forcing, surface-temperature anomaly, deep-ocean temperature index, and ocean heat uptake.
- Summary comparison of AETHER scenarios against same-forcing no-AETHER baselines.
- Forcing-assumption table and calibration table.
- Figure showing selected temperature paths.

Current implementation:

- `analysis/scenario-models/aether_climate_emulator_model.py`
- `analysis/tables/aether_climate_emulator_pathways.csv`
- `analysis/tables/aether_climate_emulator_summary.csv`
- `analysis/tables/aether_climate_emulator_forcing_assumptions.csv`
- `analysis/tables/aether_climate_emulator_calibration.csv`
- `analysis/figures/climate_emulator_temperature_paths.png`

Limit: this is a screening emulator only. Publication-grade claims still require FAIR-class or Earth-system modeling.

## Model 25: Robotics Productivity and Autonomy Economics

Goal: replace generic robot-count optimism with useful task-hours, robot classes, duty cycle, maintenance, supervision, replacement flow, and task-family bottlenecks.

Inputs:

- Target AETHER operating capacity of 100,000 MtCO2/year.
- Average 20-year buildout rate of 5,000 MtCO2/year new capacity.
- Scenario useful task-hours per MtCO2/year operating capacity.
- Scenario useful task-hours per MtCO2/year new capacity added.
- Robot class assumptions for factory robots, logistics robots, humanoid/generalist robots, autonomous construction equipment, drilling/subsurface robotics, MRV drones/sensor networks, and robotic lab workcells.
- Unit cost, useful hours per year, lifetime, maintenance fraction, energy use, supervision ratio, and integration overhead.

Outputs:

- Delivered cost per useful robot-hour by class and scenario.
- Useful task-hour demand by AETHER task family.
- Required robot stock, replacement flow, buildout flow, annual operating cost, and capex stock by task family.
- Scenario summary compared with current global industrial robot installations and frontier humanoid production cadences.
- Figure showing useful task-hour stacks by scenario.

Current implementation:

- `analysis/scenario-models/aether_robotics_productivity_model.py`
- `analysis/tables/aether_robotics_productivity_class_costs.csv`
- `analysis/tables/aether_robotics_task_demand.csv`
- `analysis/tables/aether_robotics_productivity_by_task.csv`
- `analysis/tables/aether_robotics_productivity_summary.csv`
- `analysis/figures/robotics_productivity_capacity_stack.png`

Limit: the useful task-hour intensities and supervision ratios are still scenario assumptions. Publication-grade use requires source-backed task-level productivity distributions.

## Model 26: State-Dependent Removal Effectiveness

Goal: avoid letting the paper depend on one fixed removal-effectiveness multiplier when discussing climate reversal and overshoot recovery.

Inputs:

- Reduced-form atmospheric CO2 pathways from `analysis/tables/aether_carbon_cycle_pathways.csv`.
- Joos impulse-response coefficients already used by the carbon-cycle screen.
- Four removal-effectiveness cases: fixed 0.96, optimistic active management, conservative state-dependent response, and asymmetry stress.
- Scenario penalties for drawdown depth, low-ppm management conditions, and cumulative removals relative to positive emissions.

Outputs:

- `analysis/tables/aether_removal_effectiveness_cases.csv`
- `analysis/tables/aether_state_dependent_carbon_pathways.csv`
- `analysis/tables/aether_state_dependent_carbon_summary.csv`
- `analysis/figures/state_dependent_carbon_removal_effectiveness.png`

Limit: this is a screening layer only. The multipliers are scenario assumptions, not fitted climate-model outputs. Publication-grade use requires FAIR-class or Earth-system modeling with explicit land/ocean response, temperature dynamics, non-CO2 forcing, aerosols, ocean heat uptake, lifecycle emissions, and regional impacts.

## Model 33: FAIR-Readiness Climate Input Deck

Goal: create a clean handoff from the current climate screens to a real FAIR-class or Earth-system-model workflow.

Inputs:

- Annual positive emissions, gross removals, effective removals, and direct net CO2 pulses from `analysis/tables/aether_state_dependent_carbon_pathways.csv`.
- Annual CO2 concentration, CO2 forcing, non-CO2 forcing, aerosol forcing, total forcing, surface temperature, deep-ocean index, and ocean heat uptake from `analysis/tables/aether_climate_emulator_pathways.csv`.

Outputs:

- `analysis/tables/aether_fair_readiness_input_deck.csv`
- `analysis/tables/aether_fair_readiness_summary.csv`
- `analysis/tables/aether_fair_readiness_gap_matrix.csv`
- `analysis/tables/aether_fair_readiness_run_manifest.csv`
- `analysis/figures/fair_readiness_climate_input_deck.png`

Publication rule: this is a FAIR-ready scaffold, not a FAIR result. Use it to make the next model run reproducible and to keep temperature claims visibly provisional.

## Model 34: Forcing-Driven FAIR Execution

Goal: move from a FAIR-ready handoff deck to a real package-executed climate-response diagnostic.

Inputs:

- `analysis/tables/aether_fair_readiness_input_deck.csv`
- FAIR 2.2.4 installed under Python 3.11.

Outputs:

- `analysis/scenario-models/aether_fair_forcing_execution_model.py`
- `analysis/tables/aether_fair_forcing_temperature_paths.csv`
- `analysis/tables/aether_fair_forcing_summary.csv`
- `analysis/tables/aether_fair_forcing_config.csv`
- `analysis/tables/aether_fair_forcing_delta_vs_emulator.csv`
- `analysis/figures/fair_forcing_execution_comparison.png`

Publication rule: this is a real FAIR package execution in forcing mode. It is not a full species-emissions FAIR study until CH4, N2O, aerosol precursor, land-use, lifecycle, historical spin-up, ZEC, and uncertainty inputs are added.

## Model 35: Species-Emissions FAIR Handoff

Goal: make the next FAIR or Earth-system upgrade concrete by listing which species and forcing-family inputs must replace aggregate forcing placeholders.

Inputs:

- `analysis/tables/aether_fair_readiness_input_deck.csv`
- `analysis/tables/aether_fair_forcing_summary.csv`

Outputs:

- `analysis/scenario-models/aether_species_emissions_handoff_model.py`
- `analysis/tables/aether_species_emissions_handoff_pathways.csv`
- `analysis/tables/aether_species_emissions_requirement_matrix.csv`
- `analysis/tables/aether_species_emissions_summary.csv`
- `analysis/tables/aether_species_emissions_publication_gates.csv`
- `analysis/figures/species_emissions_handoff_gap_matrix.png`

Publication rule: this model is a blocker map. It should be used to plan the next climate-modeling work, not as a species-emissions result.

## Model 27: Correlated Uncertainty Scenario Families

Goal: replace the implicit independence of the first Monte Carlo screen with explicit scenario families in which related bottlenecks move together.

Inputs:

- `analysis/tables/aether_uncertainty_distribution_registry.csv`
- `analysis/tables/aether_uncertainty_correlation_hypotheses.csv`
- The same clean-energy, robot-supply, storage, budget, execution, durability, emissions, and rebound equations used by the first uncertainty screen.

Outputs:

- `analysis/scenario-models/aether_correlated_uncertainty_model.py`
- `analysis/tables/aether_correlated_uncertainty_scenarios.csv`
- `analysis/tables/aether_correlated_uncertainty_samples.csv`
- `analysis/tables/aether_correlated_uncertainty_summary.csv`
- `analysis/tables/aether_correlated_uncertainty_family_effects.csv`
- `analysis/figures/correlated_uncertainty_success_frontier.png`

Limit: the scenario-family percentages are not calibrated probabilities. They are pass rates under current hand-set ranges and explicit co-movement assumptions. The next upgrade is a formal uncertainty-methods appendix with source-fitted distributions, expert elicitation, adversarial sensitivity review, and covariance assumptions.

## Model 28: Adversarial Review and Falsification Register

Goal: make AETHER reviewable by domain specialists before the paper presents optimistic conclusions too strongly.

Inputs:

- The current model suite, especially the feasibility-gate scorecard, claim-evidence matrix, correlated uncertainty screen, clean-power additionality screen, MRV screen, storage screen, and robotics productivity screen.
- The review-readiness backlog in `manuscript/review/aether_review_readiness.md`.

Outputs:

- `analysis/scenario-models/aether_adversarial_review_model.py`
- `analysis/tables/aether_adversarial_review_panels.csv`
- `analysis/tables/aether_falsification_tests.csv`
- `analysis/tables/aether_scientist_feedback_packet.csv`
- `analysis/tables/aether_adversarial_review_summary.csv`
- `analysis/figures/adversarial_review_risk_register.png`
- `manuscript/review/aether_adversarial_review_plan.md`

Use rule: if a P0 falsification test fails, narrow the manuscript claim. Do not protect the project by keeping the headline and hiding the failed gate in caveats.

## Model 30: P0 Clean-Power Deliverability Gate

Goal: convert F2 from an adversarial review question into a quantified clean-power deliverability screen.

Inputs:

- `analysis/tables/aether_clean_power_portfolio_summary.csv`
- `analysis/tables/aether_clean_energy_additionality_cases.csv`
- IEA, IRENA, NREL, Berkeley Lab, EIA, CEC, nuclear/geothermal, and firm-power source anchors in `references/source-register.md`

Outputs:

- `analysis/scenario-models/aether_clean_power_deliverability_model.py`
- `analysis/tables/aether_clean_power_deliverability_cases.csv`
- `analysis/tables/aether_clean_power_deliverability_scale_targets.csv`
- `analysis/tables/aether_clean_power_deliverability_constraints.csv`
- `analysis/tables/aether_clean_power_deliverability_summary.csv`
- `analysis/figures/clean_power_deliverability_gate.png`
- `research/parameters/clean-power-deliverability-and-f2-gate-notes.md`

Use rule: annual clean-energy growth does not prove AETHER power adequacy. Count delivered additional low-carbon industrial power after ordinary demand, interconnection, transmission, hourly matching, firming, and additionality.

## Model 31: Regional Clean-Power Dispatch and Colocation Screen

Goal: move beyond annual clean-power deliverability into a representative regional dispatch screen.

Inputs:

- `analysis/tables/aether_clean_power_deliverability_cases.csv`
- `analysis/tables/aether_power_supply_cases.csv`
- IEA, IRENA, NREL, Berkeley Lab, EIA, CEC, nuclear, geothermal, storage, and interconnection source anchors in `references/source-register.md`

Outputs:

- `analysis/scenario-models/aether_regional_power_dispatch_model.py`
- `analysis/tables/aether_regional_power_region_assumptions.csv`
- `analysis/tables/aether_regional_power_dispatch_cases.csv`
- `analysis/tables/aether_regional_power_dispatch_by_region.csv`
- `analysis/tables/aether_regional_power_hourly_sample.csv`
- `analysis/tables/aether_regional_power_colocation_scorecard.csv`
- `analysis/tables/aether_regional_power_dispatch_summary.csv`
- `analysis/figures/regional_power_dispatch_gate.png`
- `research/parameters/regional-clean-power-dispatch-and-colocation-notes.md`

Use rule: a regional AETHER power claim needs delivered additional low-carbon power at the right hours and locations. The v0.36 model is a representative-day screen. The publication-grade upgrade is an 8760-hour regional dispatch model with real resource traces, interconnection queues, storage-duration costs, marginal emissions, water/heat constraints, and pathway-specific co-location rules.

## Model 32: Robotics Production Verification and Scale Credibility

Goal: separate robotics production-rate evidence from robotics productivity assumptions.

Inputs:

- `analysis/tables/aether_robotics_productivity_summary.csv`
- IFR 2024 industrial robot installations and operational stock.
- Amazon deployed mobile-robot stock.
- Unitree G1 product-price floor.
- Figure BotQ capacity, Figure 03 production cadence, delivered-stock, yield, and actuator claims.
- Agility RoboFab capacity.
- User-supplied Figure X claims retained as unresolved leads.

Outputs:

- `analysis/scenario-models/aether_robotics_production_verification_model.py`
- `analysis/tables/aether_robotics_production_claims.csv`
- `analysis/tables/aether_robotics_production_scale_comparison.csv`
- `analysis/tables/aether_robotics_production_ramp_paths.csv`
- `analysis/tables/aether_robotics_production_verification_summary.csv`
- `analysis/figures/robotics_production_verification_gate.png`
- `research/parameters/robotics-production-verification-and-scale-credibility-notes.md`

Use rule: source quality must stay visible. Official company production claims can be used as company-primary signals. Social-media leads stay as verification tasks. None of these proves AETHER-grade field productivity until useful autonomous task-hours, uptime, failure recovery, service cost, supervision, and task suitability are measured.

## Model 33: Robotics Field Productivity Distribution

Goal: stress-test the robotics premise after uptime, autonomy success, task-fit, maintenance drag, and supervision drag.

Inputs:

- `analysis/tables/aether_robotics_productivity_by_task.csv`
- Scenario triangular distributions for field uptime, autonomy success, task fit, maintenance factor, and supervision factor.
- Task-family adjustments for plant O&M, logistics, storage-field work, MRV, factory spares, robotic labs, module manufacturing, construction, storage wells, logistics ramp, and MRV initialization.

Outputs:

- `analysis/scenario-models/aether_robotics_field_productivity_distribution_model.py`
- `analysis/tables/aether_robotics_field_productivity_distribution_assumptions.csv`
- `analysis/tables/aether_robotics_field_productivity_distribution_samples.csv`
- `analysis/tables/aether_robotics_field_productivity_distribution_summary.csv`
- `analysis/tables/aether_robotics_field_productivity_bottlenecks.csv`
- `analysis/tables/aether_robotics_field_productivity_summary_metrics.csv`
- `analysis/figures/robotics_field_productivity_distribution_gate.png`

Use rule: this is a stress test, not a calibrated robotics forecast. Publication-grade use requires measured task-family distributions for uptime, autonomy limits, repair cycles, field failure modes, safety-supervision ratios, and productivity per robot-hour.

## Model 36: Submission Package and Manuscript Readiness

Goal: turn the working-paper state into a reproducible review package with figure inventory, submission gates, and style audit.

Inputs:

- `manuscript/paper/aether_scientific_paper.md`
- `analysis/tables/aether_bibliography_coverage.csv`
- `analysis/tables/aether_dimensioned_unit_checks.csv`
- `analysis/tables/aether_species_emissions_publication_gates.csv`

Outputs:

- `scripts/build_aether_submission_package.py`
- `manuscript/submission/aether_submission_manuscript.md`
- `manuscript/submission/aether_submission_manifest.md`
- `manuscript/review/aether_submission_checklist.md`
- `analysis/tables/aether_figure_inventory.csv`
- `analysis/tables/aether_submission_readiness_gates.csv`
- `analysis/tables/aether_manuscript_style_audit.csv`

Publication rule: this model makes the review package reproducible. It does not clear the climate-model, species-emissions, robotics-productivity, storage/MRV/LCA, or target-journal-format gates.
