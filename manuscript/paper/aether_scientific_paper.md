# AETHER: Atmospheric Engineering Through High-Energy Removal

## A Conditional Feasibility Analysis of a 100 GtCO2/year Gross Removal Stress Test in an AI- and Robotics-Accelerated Economy

Author: Noah Hicks  
Prepared: 2026-08-09  
Status: Working paper v0.45 for the AETHER research repository
Project originator and principal author: Noah Hicks  
Copyright (c) 2026 Noah Hicks. Original research content: CC BY 4.0; code: Apache-2.0.  

## Abstract

AETHER asks whether atmospheric CO2 drawdown could become a managed infrastructure problem rather than a loosely promised offset market. This paper evaluates a deliberately strong premise: over the next two decades, AI systems and robotics improve enough to rival large portions of human scientific, engineering, construction, and industrial labor. Under that premise, the limiting question is not whether smarter models can imagine carbon removal. The limiting question is whether enough clean energy, machinery, storage capacity, measurement, capital, and governance can be assembled to remove CO2 at rates large enough to reverse atmospheric accumulation.

The analysis centers on a 100 GtCO2/year gross removal target. That target is about 2.4 times current annual anthropogenic CO2 emissions and about 45 times current global carbon dioxide removal, which is still almost entirely conventional land-based removal. A simple atmosphere-only calculation says 100 GtCO2/year would correspond to 12.8 ppm/year of gross drawdown, or 7.4 ppm/year after offsetting a 42.2 GtCO2/year current-emissions baseline. This is only bookkeeping; carbon-cycle rebound from land and ocean reservoirs would reduce realized atmospheric drawdown.

The physical constraints are severe. At current direct-air-capture energy intensities of roughly 4-10 GJ/tCO2, 100 GtCO2/year would require about 111,000-278,000 TWh/year before any CO2 splitting. A more aggressive 3 GJ/tCO2 pathway would require about 83,333 TWh/year, or 9.5 TW average power. A near-thermodynamic 1 GJ/tCO2 capture case would still require 27,778 TWh/year, or 3.17 TW average power. Splitting all captured CO2 into carbon and oxygen adds an ideal enthalpy burden of about 8.94 GJ/tCO2, raising an advanced 3 GJ/tCO2 capture pathway to about 331,708 TWh/year. This makes full splitting a specialized option, not the default AETHER pathway.

The paper concludes that 100 GtCO2/year is not forbidden by physics, but it is only plausible under a narrow abundance scenario: capture energy must fall toward 1-3 GJ/tCO2, storage must rely mostly on geologic or mineral pathways rather than full CO2 splitting, clean-energy construction must exceed today's record growth by multiples for sustained decades, and costs must fall into the rough range of $10-$50/tCO2 for annual spending to stay within trillion-scale budgets. AI and robotics can matter by compressing R&D cycles, lowering construction and operations labor costs, improving drilling and MRV, and scaling plant manufacturing. They do not remove thermodynamic floors, reactive-media requirements, material supply chains, land and water conflicts, MRV, storage liability, credit invalidation, or the institutional problem of governing finite atmospheric capacity. AETHER should therefore be developed as a staged research program: source-backed parameter models, scenario forecasts, storage-state comparisons, AI/robotics acceleration models, and a proposed public-carbon-utility model in which permitted net atmospheric use is measured, priced, and reconciled against verified durable removal.

## Keywords

carbon dioxide removal; direct air capture; climate reversal; AI automation; robotics; carbon storage; CO2 splitting; atmospheric commons; public trust doctrine; citizen dividends

## 1. Scope and Claim

AETHER stands for Atmospheric Engineering Through High-Energy Removal. The name is intentionally explicit: this is not a claim that climate repair is cheap, automatic, or already available. It is a research program about whether the atmosphere can become a deliberately managed infrastructure variable if energy, automation, and durable storage improve far beyond their present levels.

This working paper uses climate reversal in a narrow sense: sustained net-negative CO2 sufficient to reduce atmospheric CO2 concentration over time. It does not claim to reverse all climate damage. It does not directly solve methane, nitrous oxide, ocean acidification, biodiversity loss, hydrological shifts, heat extremes, or political conflict. AETHER is one part of a broader future technology program for managing human and Earth conditions: climate, oceans, agriculture, infrastructure, health, settlement, and long-run planetary resilience.

The central question is:

> Under a strong 2046 abundance premise, where AI and robotics rival large amounts of human scientific and physical labor, what technical and governance conditions would have to be true for durable CO2 removal at 100 GtCO2/year to be plausible?

The answer is conditional. AETHER becomes physically plausible only if the system converges toward low capture energy, cheap clean power, automated construction, durable storage, adversarial measurement, and a governance structure that makes atmospheric and ocean dumping costly or prohibited. It fails if it depends on current DAC costs, full splitting of all CO2, weak measurement, fossil-powered removal, or carbon credits that are easier to sell than to verify.

<!-- AETHER-PUBLICATION-GATE:paper-accounting:BEGIN -->
### 1.1 Accounting and Assumption Boundaries

The headline 100 GtCO2/year value is a **gross removal stress test**. It is not an optimum, recommendation, deployment promise, central forecast, or claim about what should be built. The purpose of the extreme boundary is to expose which constraints become decisive. A smaller program may be more defensible.

The paper keeps four accounting layers separate:

1. **Gross removal** is CO2 entering a capture or removal process.
2. **Lifecycle-adjusted durable removal** subtracts operational and non-power lifecycle emissions and then applies pathway-specific 100-year retention assumptions.
3. **Creditable removal** applies provisional measurement, method, reversal, leakage, and invalidation buffers to the durable quantity.
4. **Net climate result** subtracts residual positive emissions and any induced emissions or delayed abatement attributed to rebound.

The corresponding accounting identities are `simple net = gross removal - residual emissions - rebound`; `durable after LCA = sum((pathway gross - pathway lifecycle emissions) * 100-year retention)`; and `creditable = sum(durable after LCA * pathway MRV multiplier)`. These are model definitions, not a claim that the inputs have been empirically validated.

Unless a table says otherwise, mass is in metric tonnes. TWh can denote electricity or heat-equivalent energy; those forms are not interchangeable, and average power does not solve capacity factor, dispatch, transmission, or firming. Dollar values combine reported source-year values and scenario assumptions and are not harmonized to constant 2026 dollars, so cross-scenario comparisons are order-of-magnitude screens rather than precise real-cost forecasts. Displayed values are rounded; generated CSVs retain more precision. A gate marked `pass` or `conditional_pass` means only that an internal scenario clears its coded test under stated assumptions. Monte Carlo pass shares use hand-set distributions and are not real-world probabilities.
<!-- AETHER-PUBLICATION-GATE:paper-accounting:END -->



### 1.2 Prior Art and Contribution Boundary

AETHER is not the first carbon dioxide removal roadmap, not the first direct-air-capture cost model, not the first argument that DAC can scale modularly, not the first atmospheric-commons governance proposal, and not the first use of AI for carbon-capture materials discovery. The project is weaker if it pretends otherwise.

The prior work is substantial. National Academies, IPCC, State of CDR, and Roads to Removal establish the CDR research agenda, pathway set, current scale, and regional planning frame [@national_academies_net_reliable_sequestration; @ipcc_ar6_wg3_technical_summary_cdr; @state_of_cdr_2026; @roads_to_removal_2023]. Realmonte et al. model DACCS in deep mitigation pathways, including 30 GtCO2/year capacity cases, and Chatterjee and Huang challenge very large DAC deployment on energy, materials, sorbent, and coproduct grounds [@realmonte_2019_daccs_iam; @chatterjee_huang_2020_unrealistic_dac]. Young et al. show why DACS costs may remain far above optimistic public targets without strong deployment and policy support [@young_2023_dacs_cost_targets]. Keith et al., NASEM, and NETL provide process, contactor, and sorbent-engineering anchors [@keith_2018_process_dac; @national_academies_dac_ch5_2018; @netl_sorbent_dac_2025].

There is also adjacent work directly relevant to the AI and robotics premise. McQueen and Drennan connect warehouse automation to scalable DAC design [@mcqueen_drennan_2024_warehouse_dac]. OpenDAC 2023 gives a machine-learning materials-discovery benchmark for DAC sorbents, and Giro et al. demonstrate AI-powered automated discovery for carbon-capture polymer membranes [@sriram_2023_opendac; @giro_2023_ai_polymer_membranes]. These do not prove that AI scientists and robots can deliver AETHER-scale removal. They prove the narrower point that parts of AETHER's premise are already visible in the literature: automated material discovery, modular industrial automation, DAC process design, and large-scale CDR planning are separate active fields.

The intended contribution is the coupling. AETHER asks what happens if those fields are forced into one 100 GtCO2/year feasibility-boundary model under an explicit 2046 abundance premise. The paper's claim is not "nobody has thought about this." The claim is that the coupled system has to be judged as a coupled system: energy, contactors, sorbents, storage, robot productivity, cost floors, carbon-cycle response, rebound, MRV, and governance all have to clear together. The prior-art positioning matrix in `analysis/tables/aether_prior_art_positioning_matrix.csv` records the current boundary between prior work and AETHER's proposed contribution.
<!-- AETHER-PUBLIC-RELEASE:paper-project:BEGIN -->
The public research record is maintained at https://github.com/RedLynx101/aether-climate-reversal. This paper is one interface to the concept rather than the project boundary; the repository carries the models, generated evidence, review gates, and contribution workflow needed for independent scrutiny.
<!-- AETHER-PUBLIC-RELEASE:paper-project:END -->

## 2. Current State

Atmospheric CO2 is still rising. NOAA's global monthly mean CO2 page reported 428.53 ppm for February 2026, and NOAA's Mauna Loa monthly mean page reported 432.34 ppm for May 2026 [@noaa_gml_global_co2_2026; @noaa_gml_mauna_loa_co2_2026]. The Global Carbon Budget 2025 projects fossil CO2 emissions of 38.1 GtCO2/year in 2025 and total anthropogenic CO2 emissions of about 42.2 GtCO2/year when fossil and land-use emissions are combined [@global_carbon_budget_2025].

Current carbon dioxide removal is not close to the AETHER target. The State of Carbon Dioxide Removal 2026 reports current global CDR at roughly 2.2 GtCO2/year, with almost all of it from conventional land-based methods. Novel CDR is around 2.04 MtCO2/year, or 0.00204 GtCO2/year [@state_of_cdr_2026]. A 100 GtCO2/year AETHER target is therefore about 45 times current total CDR and about 49,000 times current novel CDR.

This gap is the reason AETHER should not be written as a near-term deployment claim. The useful question is instead whether the gap changes under a very strong automation and energy-abundance premise.

## 3. Method

The repository model uses transparent first-order calculations rather than a complex climate model. That is deliberate. The purpose of this version is to expose feasibility boundaries before building a full coupled carbon-cycle and industrial learning model.

The model combines thirty-two blocks:

1. Carbon stock-flow bookkeeping: gross removal, current emissions offset, atmosphere-only ppm equivalents, and reduced-form carbon-cycle time paths.
2. Energy intensity: capture energy in GJ/tCO2, optional CO2 splitting energy, annual TWh, and average TW.
3. Power-system buildout: installed solar, wind, nuclear, geothermal, storage/flexibility, and annual capacity-addition requirements.
4. Air-contactor and plant-scale hardware: air flow, contactor face area, fan pressure drop, plant-equivalent counts, sorbent inventory, and replacement mass.
5. Storage state: supercritical CO2, gas-phase CO2, solid carbon, liquid oxygen, and air-throughput estimates.
6. Storage lifecycle and regionalization: storage route, regional resource proxy, injection/processing burden, lifecycle penalty, leakage or reversal risk, and 100-year durable credited removal.
7. Regional storage and injection corridors: basin-level proxy capacity, source-distance routing, injection wells, pressure-management multiplier, corridor count, and regulatory stage.
8. Cost stack and automation leverage: delivered cost by energy, capex, materials, storage, MRV, robot operations, finance, and carbon/O2 product handling.
9. Robotics assumptions: unit cost, operating hours, lifetime, maintenance, manufacturing growth, and robot capacity per MtCO2/year.
10. Transition dynamics: learning curves, economies of scale, rebound, clean-energy buildout, and carbon-cycle trajectories.
11. Pathway portfolio: method-specific cost, energy, capacity, durability, and bottleneck assumptions.
12. Integrated feasibility frontier: 2026-2046 capacity paths constrained by clean energy, robot supply, storage, budget, rebound, and emissions decline.
13. Deployment timepaths and cumulative removal: annual gross capacity, durable credit, cumulative removal, residual emissions, rebound, and net climate value through 2060.
14. Uncertainty and sensitivity: Monte Carlo sampling across coupled energy, robotics, storage, budget, lifecycle, residual-emissions, rebound, and execution assumptions.
15. Governance branch: commons ownership and public-trust mechanisms as a candidate way to price or prohibit use of atmosphere, oceans, and lakes as sinks.
16. Research-roadmap layer: explicit next models needed before publication-grade claims.
17. Equation and reproducibility ledger: main model equations, unit transformations, unit checks, and traceability from source anchors to model outputs.
18. Material and industrial supply-chain screen: structural steel, cement, reactive media, copper, power-system materials, pipeline steel, and source-backed global production comparators.
19. MRV and credit-integrity filter: measurement uncertainty, method uncertainty, reversal and leakage buffers, credit-invalidation reserves, liability cost, and gross-to-creditable overbuild.
20. Climate-response proxy: CO2 concentration trajectories into CO2 forcing, CO2-only equilibrium warming proxy, and transient-scaled warming proxy.
21. Uncertainty distribution evidence registry: evidence grade, source keys, distribution rationale, correlation family, paper-use rule, and upgrade priority for every Monte Carlo input.
22. Lifecycle emissions screen: pathway-specific placeholder LCA assumptions, clean-power emissions sensitivity, durable removal after LCA, and creditable removal after LCA plus MRV.
23. Clean-power additionality screen: market-led clean-energy growth, transmission/interconnection delivery, competing load claims, and true additionality as a separate power gate.
24. Dynamic climate emulator: CO2 forcing, non-CO2/aerosol forcing policy screens, ocean-lag response, and avoided-temperature comparison.
25. Robotics productivity and autonomy economics: useful task-hours, robot classes, duty cycle, maintenance, supervision, replacement flow, and task-family bottlenecks.
26. State-dependent carbon removal: removal-effectiveness sensitivity across fixed, optimistic, conservative, and asymmetry-stress carbon-cycle response cases.
27. Correlated uncertainty scenario families: aligned-abundance and clustered-failure cases that move clean power, automation, storage/MRV, rebound, and execution assumptions together.
28. Adversarial review and falsification: reviewer-panel risk register, P0 tests, and scientist feedback packet for narrowing or defending claims.
29. Clean-power deliverability: P0 F2 screen for delivered additional power after ordinary demand, interconnection, transmission, hourly matching, firming, and additionality constraints.
30. Regional clean-power dispatch and colocation: representative-day regional archetype screen for hourly matching, storage duration, curtailment, ordinary demand, and co-location constraints.
31. Robotics production verification: source-quality gate for humanoid and industrial robot production claims, annual robot-production requirements, factory-capacity multiples, and scale credibility.
32. Robotics field-productivity distributions: stress test for uptime, autonomy success, task fit, maintenance, supervision, robot stock, annual production flow, and task-family bottlenecks.

### 3.1 Evidence Standard and Claim Classes

The current draft uses four evidence classes. This is important because AETHER combines official climate and energy data, derived physical calculations, scenario models, and provisional technology leads. Those should not be written with the same certainty.

| Claim class | Allowed use in this paper | Example |
|---|---|---|
| Source-backed anchor | State as a current external fact, with citation and date where relevant. | Current emissions, CO2 concentration, current CDR scale, official energy statistics. |
| Derived calculation | State as arithmetic or model output, with the input assumptions visible. | 100 GtCO2/year as ppm arithmetic, annual TWh, contactor area, storage volume, cost at a stated $/tCO2. |
| Scenario assumption | Use to test plausibility, not to claim that the future will follow it. | AI/robotics cost compression, robot adequacy ratios, deep-abundance cost floor, clean-power allocation to AETHER. |
| Provisional lead or governance hypothesis | Treat as a research branch or source lead until independently verified. | Figure Robotics production-rate posts, citizen-owned sink governance, future fusion market pull. |

The claim-evidence matrix in `analysis/tables/aether_manuscript_claim_evidence_matrix.csv` is now the reviewer-facing index for the main claims. Each row gives the claim, evidence class, evidence anchor, artifacts, citation keys, reviewer risk, required upgrade, and manuscript-use rule. This is not bureaucratic overhead. It is how the paper avoids turning an optimistic scenario into an unsupported forecast.

The core physical model lives in `analysis/scenario-models/aether_scenario_model.py`. The transition model lives in `analysis/scenario-models/aether_transition_model.py`. The latest outputs are in:

- `analysis/tables/aether_scenario_summary.csv`
- `analysis/tables/aether_parameter_table.csv`
- `analysis/tables/aether_learning_curve_costs.csv`
- `analysis/tables/aether_jevons_rebound_sensitivity.csv`
- `analysis/tables/aether_economies_of_scale.csv`
- `analysis/tables/aether_robot_fleet_requirements.csv`
- `analysis/tables/aether_robotics_scale_comparison.csv`
- `analysis/tables/aether_robotics_task_ladder.csv`
- `analysis/tables/aether_robotics_productivity_class_costs.csv`
- `analysis/tables/aether_robotics_task_demand.csv`
- `analysis/tables/aether_robotics_productivity_by_task.csv`
- `analysis/tables/aether_robotics_productivity_summary.csv`
- `analysis/tables/aether_robotics_production_claims.csv`
- `analysis/tables/aether_robotics_production_scale_comparison.csv`
- `analysis/tables/aether_robotics_production_ramp_paths.csv`
- `analysis/tables/aether_robotics_production_verification_summary.csv`
- `analysis/tables/aether_robotics_field_productivity_distribution_assumptions.csv`
- `analysis/tables/aether_robotics_field_productivity_distribution_samples.csv`
- `analysis/tables/aether_robotics_field_productivity_distribution_summary.csv`
- `analysis/tables/aether_robotics_field_productivity_bottlenecks.csv`
- `analysis/tables/aether_robotics_field_productivity_summary_metrics.csv`
- `analysis/tables/aether_20y_buildout_pathways.csv`
- `analysis/tables/aether_clean_energy_buildout_sensitivity.csv`
- `analysis/tables/aether_carbon_cycle_pathways.csv`
- `analysis/tables/aether_carbon_cycle_summary.csv`
- `analysis/tables/aether_removal_effectiveness_cases.csv`
- `analysis/tables/aether_state_dependent_carbon_pathways.csv`
- `analysis/tables/aether_state_dependent_carbon_summary.csv`
- `analysis/tables/aether_climate_response_pathways.csv`
- `analysis/tables/aether_climate_response_summary.csv`
- `analysis/tables/aether_pathway_portfolio_allocation.csv`
- `analysis/tables/aether_pathway_portfolio_summary.csv`
- `analysis/tables/aether_pathway_source_gap_analysis.csv`
- `analysis/tables/aether_integrated_feasibility_scenarios.csv`
- `analysis/tables/aether_integrated_feasibility_timepaths.csv`
- `analysis/tables/aether_integrated_feasibility_bottlenecks.csv`
- `analysis/tables/aether_deployment_timepath_annual.csv`
- `analysis/tables/aether_deployment_timepath_summary.csv`
- `analysis/tables/aether_deployment_gate_crossings.csv`
- `analysis/tables/aether_storage_lifecycle_routes.csv`
- `analysis/tables/aether_storage_lifecycle_summary.csv`
- `analysis/tables/aether_regional_storage_allocation.csv`
- `analysis/tables/aether_regional_storage_summary.csv`
- `analysis/tables/aether_model_equation_ledger.csv`
- `analysis/tables/aether_dimensioned_unit_checks.csv`
- `analysis/tables/aether_injection_corridor_requirements.csv`
- `analysis/tables/aether_material_supply_chain_inputs.csv`
- `analysis/tables/aether_material_supply_chain_requirements.csv`
- `analysis/tables/aether_material_supply_chain_summary.csv`
- `analysis/tables/aether_conversion_state_ledger.csv`
- `analysis/tables/aether_splitting_fraction_sensitivity.csv`
- `analysis/tables/aether_uncertainty_assumptions.csv`
- `analysis/tables/aether_uncertainty_samples.csv`
- `analysis/tables/aether_uncertainty_summary.csv`
- `analysis/tables/aether_uncertainty_bottlenecks.csv`
- `analysis/tables/aether_uncertainty_sensitivity.csv`
- `analysis/tables/aether_uncertainty_distribution_registry.csv`
- `analysis/tables/aether_uncertainty_distribution_upgrade_priorities.csv`
- `analysis/tables/aether_uncertainty_correlation_hypotheses.csv`
- `analysis/tables/aether_correlated_uncertainty_scenarios.csv`
- `analysis/tables/aether_correlated_uncertainty_samples.csv`
- `analysis/tables/aether_correlated_uncertainty_summary.csv`
- `analysis/tables/aether_correlated_uncertainty_family_effects.csv`
- `analysis/tables/aether_adversarial_review_panels.csv`
- `analysis/tables/aether_falsification_tests.csv`
- `analysis/tables/aether_scientist_feedback_packet.csv`
- `analysis/tables/aether_adversarial_review_summary.csv`
- `analysis/tables/aether_cost_stack_components.csv`
- `analysis/tables/aether_cost_stack_scenarios.csv`
- `analysis/tables/aether_robot_labor_costs.csv`
- `analysis/tables/aether_cost_reduction_requirements.csv`
- `analysis/tables/aether_cost_improvement_frontier.csv`
- `analysis/tables/aether_cost_bucket_reduction_factors.csv`
- `analysis/tables/aether_trillion_rd_program_comparators.csv`
- `analysis/tables/aether_power_supply_cases.csv`
- `analysis/tables/aether_power_system_tech_assumptions.csv`
- `analysis/tables/aether_clean_power_portfolio_requirements.csv`
- `analysis/tables/aether_clean_power_portfolio_summary.csv`
- `analysis/tables/aether_air_contactor_scale.csv`
- `analysis/tables/aether_sorbent_inventory_scale.csv`
- `analysis/tables/aether_air_contactor_scale_summary.csv`
- `analysis/tables/aether_feasibility_gate_scorecard.csv`
- `analysis/tables/aether_research_program_milestones.csv`
- `analysis/tables/aether_presentation_key_numbers.csv`
- `analysis/tables/aether_parameter_evidence_summary.csv`

The parameter-evidence map is in `data/parameters/aether_parameter_evidence.csv`, with schema notes in `docs/parameter-database-schema.md`.
The equation ledger is in `analysis/tables/aether_model_equation_ledger.csv`, with unit checks in `analysis/tables/aether_dimensioned_unit_checks.csv` and a reproducibility note in `docs/reproducibility.md`. The pathway source-range matrix is in `data/parameters/aether_cdr_pathway_source_ranges.csv`. The robotics evidence map is in `data/parameters/aether_robotics_evidence.csv`. The conversion constants ledger is in `data/parameters/aether_conversion_constants.csv`. Parameter notes are in `research/parameters/aether-parameter-notes.md`, `research/parameters/clean-energy-market-and-firm-power-notes.md`, `research/parameters/robotics-scaling-notes.md`, `research/parameters/pathway-portfolio-notes.md`, `research/parameters/integrated-feasibility-frontier-notes.md`, `research/parameters/storage-lifecycle-and-regionalization-notes.md`, `research/parameters/regional-storage-and-injection-corridor-notes.md`, `research/parameters/conversion-and-storage-state-ledger-notes.md`, `research/parameters/uncertainty-sensitivity-notes.md`, `research/parameters/cost-stack-and-automation-leverage-notes.md`, `research/parameters/parameter-evidence-database-notes.md`, and `research/open-questions/jevons-learning-and-scale-economics.md`.

The current figure set is generated by `scripts/make_aether_figures.ps1` plus specialized figure scripts for rebound, carbon cycle, integrated feasibility, deployment timepaths, storage lifecycle, uncertainty, cost stack, pathway ranges, robotics evidence, the conversion ledger, technology acceleration, power-system buildout, clean-power additionality, lifecycle emissions, the dynamic climate emulator, robotics productivity, state-dependent carbon-removal effectiveness, correlated uncertainty scenario-family screening, and adversarial reviewer-risk screening. The figures were manually inspected after generation.

![AETHER energy demand at 100 GtCO2/year](../../analysis/figures/energy_by_pathway_100gt.png)

![AETHER clean-power capacity requirements](../../analysis/figures/clean_energy_capacity_requirements_100gt.png)

![AETHER air-contactor physical scale](../../analysis/figures/air_contactor_physical_scale_100gt.png)

![Storage-state volumes at 100 GtCO2/year](../../analysis/figures/storage_state_volumes_100gt.png)

![Conversion and storage-state ledger for 100 GtCO2/year](../../analysis/figures/conversion_storage_ledger_100gt.png)

![Jevons and policy rebound sensitivity](../../analysis/figures/jevons_rebound_sensitivity_100gt.png)

![Robot fleet scale for 100 GtCO2/year](../../analysis/figures/robot_fleet_requirements_100gt.png)

![Robotics scale anchors vs AETHER needs](../../analysis/figures/robotics_scale_anchors_vs_aether.png)

![Reduced-form atmospheric CO2 pathways](../../analysis/figures/carbon_cycle_atmospheric_co2_pathways.png)
![State-dependent carbon-removal effectiveness](../../analysis/figures/state_dependent_carbon_removal_effectiveness.png)
![AETHER climate-response temperature proxy](../../analysis/figures/climate_response_temperature_proxy.png)
![AETHER FAIR-readiness climate input deck](../../analysis/figures/fair_readiness_climate_input_deck.png)
![AETHER forcing-driven FAIR execution](../../analysis/figures/fair_forcing_execution_comparison.png)
![AETHER species-emissions FAIR handoff](../../analysis/figures/species_emissions_handoff_gap_matrix.png)

![AETHER pathway portfolio at 100 GtCO2/year](../../analysis/figures/pathway_portfolio_100gt.png)

![AETHER portfolio against assessed CDR pathway ranges](../../analysis/figures/pathway_source_ranges_vs_aether.png)

![Integrated feasibility screen for AETHER](../../analysis/figures/integrated_feasibility_screen_2046.png)

![Integrated capacity paths for AETHER](../../analysis/figures/integrated_capacity_paths_2026_2046.png)
![AETHER deployment timepaths and cumulative durable removal](../../analysis/figures/deployment_timepath_capacity_and_cumulative.png)

![Storage lifecycle durability filter](../../analysis/figures/storage_lifecycle_net_durable_100y.png)

![Storage injection and processing burden](../../analysis/figures/storage_injection_processing_burden.png)
![Regional storage and injection corridors](../../analysis/figures/regional_storage_injection_corridors.png)
![Material and industrial supply-chain pressure](../../analysis/figures/material_supply_chain_pressure.png)
![MRV and credit-integrity filter](../../analysis/figures/mrv_credit_integrity_overbuild.png)
![Lifecycle emissions and creditable removal sensitivity](../../analysis/figures/lifecycle_emissions_net_credit_sensitivity.png)
![Clean-power additionality gate](../../analysis/figures/clean_energy_additionality_gate.png)

![AETHER uncertainty success probabilities](../../analysis/figures/uncertainty_success_probabilities.png)

![AETHER uncertainty sensitivity tornado](../../analysis/figures/uncertainty_sensitivity_tornado.png)
![AETHER uncertainty distribution evidence gaps](../../analysis/figures/uncertainty_distribution_evidence_gaps.png)
![AETHER correlated uncertainty scenario families](../../analysis/figures/correlated_uncertainty_success_frontier.png)
![AETHER adversarial reviewer risk register](../../analysis/figures/adversarial_review_risk_register.png)

![AETHER feasibility gate scorecard](../../analysis/figures/feasibility_gate_scorecard.png)

![AETHER delivered cost stack by scenario](../../analysis/figures/cost_stack_by_scenario.png)

![AETHER technology acceleration frontier](../../analysis/figures/technology_acceleration_frontier.png)

![AETHER robot hour cost scenarios](../../analysis/figures/robot_hour_cost_scenarios.png)

## 4. Core Calculations

### 4.1 Scale of 100 GtCO2/year

Using a simple conversion of 1 ppm atmospheric CO2 to about 7.8 GtCO2, 100 GtCO2/year gross removal corresponds to about 12.8 ppm/year of gross atmosphere-only drawdown. If current total anthropogenic CO2 emissions are treated as 42.2 GtCO2/year, the same gross removal gives 57.8 GtCO2/year net removal, or about 7.4 ppm/year atmosphere-only drawdown.

These numbers are useful but incomplete. They do not include land-ocean rebound. If atmospheric CO2 falls, natural sinks can weaken or reverse relative to the drawdown trajectory. A serious next model must include carbon-cycle feedbacks. The simple calculation is still valuable because it shows the order of magnitude: 100 GtCO2/year is not an offset tweak. It is a system larger than current annual emissions.


### 4.2 Carbon-Cycle Time Paths

The first AETHER draft treated ppm drawdown as atmosphere-only bookkeeping. The current repo now adds a reduced-form carbon-cycle model using the Joos et al. multi-model CO2 impulse-response function [@joos_2013_impulse_response]. This matters because land and ocean reservoirs do not stay passive when atmospheric CO2 changes. IPCC AR6 WGI describes the airborne fraction, carbon-cycle feedbacks, and carbon dioxide removal response as central constraints on future atmospheric CO2 [@ipcc_ar6_wg1_ch5_carbon_cycle]. It also summarizes model experiments in which CO2 removed from the atmosphere is partly offset by land and ocean reservoir response [@ipcc_ar6_wg1_fig_5_32_cdr_pulse]. Zickfeld et al. further show that positive emissions and equivalent removals are not perfectly symmetric in the climate-carbon system [@zickfeld_2021_asymmetry].

The model is still deliberately simple. Annual positive emissions and negative AETHER removals are convolved with the Joos impulse-response function. Durable removals use a 0.96 removal-effectiveness multiplier as a first caution factor, not as a universal constant. Managed AETHER scenarios also use an illustrative 350 ppm floor: once the reduced-form atmospheric path reaches that management range, annual removals throttle instead of blindly continuing at 100 GtCO2/year. This is a control assumption, not a recommended final target.

The time-path result changes the interpretation of the 100 GtCO2/year target. If current emissions continue and AETHER ramps linearly toward 100 GtCO2/year by 2046, the model shows atmospheric CO2 falling later in the century, but not as quickly as the atmosphere-only calculation implies. If emissions reach zero by 2050 while AETHER reaches industrial scale, the modeled system can return the atmosphere to a lower managed range this century and then reduce removal activity. If cheap removal induces rebound or delayed abatement, much of the benefit disappears.

| Scenario | 2046 CO2 | 2050 CO2 | 2100 CO2 | Interpretation |
|---|---:|---:|---:|---|
| No AETHER, constant emissions | 510 ppm | 523 ppm | 656 ppm | Failure case: atmospheric CO2 keeps rising |
| AETHER, constant emissions | 409 ppm | 388 ppm | 350 ppm | Managed AETHER can overcome current emissions, then throttle near the management floor |
| AETHER, 58% rebound | 470 ppm | 469 ppm | 473 ppm | Rebound/delayed abatement can erase much of the annual net-negative effect |
| AETHER plus delayed zero | 387 ppm | 357 ppm | 350 ppm | Large drawdown requires both removal, emissions decline, and an operating floor |
| AETHER plus net-zero 2050 | 372 ppm | 350 ppm | 350 ppm | Strongest current pathway: removal becomes managed climate reversal rather than offset accounting |

The generated values live in `analysis/tables/aether_carbon_cycle_summary.csv`; the pathway figure lives in `analysis/figures/carbon_cycle_atmospheric_co2_pathways.png`. The paper should not overclaim from this model. It is a reduced-form screen for scenario discipline. The later version should use FAIR or an Earth-system-model workflow with explicit temperature response, state-dependent removal effectiveness, ocean chemistry, and lifecycle emissions.

### 4.2.1 Climate Response Proxy

The carbon-cycle section gives concentration paths. The v0.25 model adds a deliberately limited climate-response proxy so the paper can discuss forcing and temperature direction without pretending to run a full climate model. IPCC AR6 WGI Chapter 7 gives the assessed effective radiative forcing for CO2 doubling as 3.93 W/m2 and frames the sensitivity relationship used here [@ipcc_ar6_wg1_ch7_forcing_sensitivity]. The IPCC Technical Summary gives the relevant ECS, TCR, and TCRE context, including the warning that very low and net-negative CO2 pathways remain more uncertain over long horizons [@ipcc_ar6_wg1_ts_tcre_2021]. FAIR is the appropriate next-step model class because it connects emissions, concentrations, forcing, and temperature response with non-CO2 forcing and ocean heat uptake dynamics rather than relying on a static proxy [@fair_v13_smith_2018].

The current proxy uses the AR6 CO2-doubling forcing anchor:

`FCO2 = 3.93 * log2(C / 278)`

It then reports two transparent quantities: a CO2-only equilibrium warming proxy using ECS = 3.0 deg C and a CO2-only transient-scaled warming proxy using TCR = 1.8 deg C. These are not forecasts of total warming. They exclude non-CO2 forcing, aerosols, ocean heat uptake dynamics, ice sheets, regional climate response, ocean chemistry, and full carbon-climate feedbacks.

| Scenario | 2100 ppm | 2100 CO2 ERF | 2100 transient proxy | Avoided vs no AETHER |
| --- | --- | --- | --- | --- |
| No AETHER, constant emissions | 656 | 4.87 W/m2 | 2.23 deg C | 0.00 deg C |
| AETHER, constant emissions | 350 | 1.31 W/m2 | 0.60 deg C | 1.63 deg C |
| AETHER, 58% rebound | 473 | 3.02 W/m2 | 1.38 deg C | 0.85 deg C |
| AETHER plus net-zero 2050 | 350 | 1.31 W/m2 | 0.60 deg C | 1.63 deg C |

The result is a useful discipline layer. Under no-AETHER constant emissions, the CO2-only transient-scaled proxy reaches about 2.23 deg C by 2100. AETHER plus net-zero 2050 reaches about 0.60 deg C in the same proxy, while the 58% rebound case remains near 1.38 deg C. The avoided value is large enough to matter, but the caveat is equally large: this is a CO2-only comparison, not a publication-grade warming projection. The next version should run the same AETHER time paths through FAIR or an Earth-system model before making climate-response claims.

The generated pathway table is `analysis/tables/aether_climate_response_pathways.csv`; the summary table is `analysis/tables/aether_climate_response_summary.csv`; the figure is `analysis/figures/climate_response_temperature_proxy.png`.

### 4.2.2 Dynamic Climate Emulator and Non-CO2 Forcing Screen

The v0.29 repo adds an intermediate climate-emulator layer. This is not FAIR and not an Earth-system model. It is a calibrated two-box screening emulator built to answer a narrower question: how much does AETHER's temperature story change once CO2 forcing is passed through an ocean-lag response and combined with explicit non-CO2 and aerosol forcing scenarios?

The model keeps the AR6 CO2 forcing equation from the proxy section, calibrates a two-box energy-balance response to ECS = 3.000 deg C and achieved TCR about 1.800 deg C, then runs four forcing-policy screens: CO2-only comparison, mitigation with aerosol cleanup, delayed non-CO2 mitigation with aerosol unmasking, and active full-forcing management. The policy paths start from a positive non-CO2 forcing assumption of about +1.20 W/m2 and aerosol cooling of about -0.70 W/m2 in 2026, then move differently by scenario. These are scenario assumptions anchored to the assessed forcing categories, not forecasts.

![AETHER climate emulator temperature paths](../../analysis/figures/climate_emulator_temperature_paths.png)

| Scenario | 2050 temp | 2100 temp | 2026-2100 change | Avoided vs same-forcing no-AETHER |
| --- | --- | --- | --- | --- |
| No AETHER; delayed non-CO2 + aerosol unmasking | 2.32 | 3.24 | 1.63 | 0.00 |
| AETHER with 58% rebound; same forcing stress | 2.11 | 2.38 | 0.76 | 0.86 |
| AETHER + net-zero 2050; mitigation cleanup | 1.34 | 1.20 | -0.42 | 1.74 |
| AETHER + net-zero 2050; full-forcing management | 1.30 | 1.10 | -0.51 | 1.74 |

The result is a useful discipline check. Under the delayed non-CO2 plus aerosol-unmasking stress case, AETHER with a 58% rebound still avoids about 0.86 deg C against the same forcing-policy no-AETHER case by 2100, but the absolute temperature path remains materially higher than a CO2-only graph would suggest. Under net-zero 2050 plus active full-forcing management, the emulator puts 2100 temperature near 1.10 deg C in this screening setup and avoids about 1.74 deg C against the same-policy no-AETHER baseline.

This does not make the temperature claim publication-grade. It makes the paper more honest. AETHER is a CO2-removal program, but climate reversal is not a CO2-only control problem. The next step is a FAIR-class or Earth-system workflow with non-CO2 gas trajectories, aerosol pathways, uncertainty ensembles, lifecycle emissions, zero-emissions commitment, ocean chemistry, and comparison to assessed temperature metrics.

The generated tables are `analysis/tables/aether_climate_emulator_pathways.csv`, `analysis/tables/aether_climate_emulator_summary.csv`, `analysis/tables/aether_climate_emulator_forcing_assumptions.csv`, and `analysis/tables/aether_climate_emulator_calibration.csv`; the figure is `analysis/figures/climate_emulator_temperature_paths.png`.

### 4.2.3 State-Dependent Removal Effectiveness and Overshoot Reversibility

The v0.32 repo adds a state-dependent removal-effectiveness screen. This is not FAIR, and it is not an Earth-system model. It is a more disciplined stress test around the earlier fixed 0.96 multiplier. The scientific reason is straightforward: the atmosphere, land, and ocean do not behave like a passive tank. IPCC AR6 WGI treats carbon-cycle feedbacks and CDR response as core uncertainties [@ipcc_ar6_wg1_ch5_carbon_cycle], and its CDR-pulse experiments show that some removed atmospheric CO2 is offset by land and ocean response [@ipcc_ar6_wg1_fig_5_32_cdr_pulse]. Zickfeld et al. also show that positive emissions and removals are not perfectly symmetric [@zickfeld_2021_asymmetry].

The screen keeps the Joos impulse-response function [@joos_2013_impulse_response] and runs four removal-effectiveness cases: the prior fixed 0.96 screen, an optimistic active-management case, a conservative state-dependent case, and an asymmetry-stress case. The state-dependent cases reduce realized effective removal as atmospheric drawdown deepens, low-ppm management conditions approach, and cumulative removals become large relative to positive emissions. The coefficients are scenario assumptions. Their job is to expose sensitivity, not to replace climate science.

![State-dependent carbon-removal effectiveness](../../analysis/figures/state_dependent_carbon_removal_effectiveness.png)

| Scenario | Fixed 0.96 2100 ppm | Conservative 2100 ppm | Asymmetry stress 2100 ppm | Stress penalty vs fixed |
| --- | --- | --- | --- | --- |
| Net-zero 2050 | 350.0 | 350.0 | 350.0 | 0.0 |
| Constant emissions | 350.0 | 350.0 | 350.0 | 0.0 |
| 58% rebound | 473.3 | 492.4 | 525.9 | 52.7 |

The result is useful because it changes what AETHER has to prove. AETHER cannot only show that 100 GtCO2/year gross removal is mechanically possible. It has to show that the gross system produces enough realized atmospheric drawdown after carbon-cycle response, lifecycle emissions, MRV, and rebound behavior. The state-dependent screen supports the paper's central discipline: climate reversal is plausible only in the joint case where clean energy is additional, emissions decline, removals are durable, rebound is constrained, and the system throttles rather than blindly over-removing near a management floor.

The generated tables are `analysis/tables/aether_removal_effectiveness_cases.csv`, `analysis/tables/aether_state_dependent_carbon_pathways.csv`, and `analysis/tables/aether_state_dependent_carbon_summary.csv`; the figure is `analysis/figures/state_dependent_carbon_removal_effectiveness.png`.

### 4.2.4 FAIR-Readiness Climate Input Deck and Gap Matrix

The v0.39 repo adds a FAIR-readiness climate input deck. This is still not a FAIR run. It is a bridge layer that makes the next climate-modeling step harder to dodge. The deck joins annual positive emissions, gross removals, effective removals, and proxy net CO2 pulses from the state-dependent carbon screen to annual CO2 concentration, CO2 forcing, non-CO2 forcing, aerosol forcing, total forcing, surface temperature, deep-ocean index, and ocean heat uptake from the dynamic climate emulator.

![AETHER FAIR-readiness climate input deck](../../analysis/figures/fair_readiness_climate_input_deck.png)

| Scenario | 2100 temp, C | 2100 ppm | Cumulative proxy net CO2, Gt | Use |
| --- | --- | --- | --- | --- |
| No AETHER stress | 3.24 | 656.1 | 3,165 | baseline stress |
| AETHER 58% rebound stress | 2.38 | 473.3 | 701 | failure-sensitive case |
| AETHER net-zero/full forcing | 1.10 | 350.0 | -1,194 | best governance case |
| AETHER no rebound/full forcing | 1.11 | 350.0 | -1,156 | CO2 removal power case |

The joined deck has 1800 annual rows across the current scenario and forcing-policy combinations. The gap matrix has 17 climate-variable families; 11 P0 families remain outside a usable publication-grade state, and 9 families are still missing or aggregate placeholders. That is the point of the layer. It makes the current climate model more organized without pretending to close the scientific gap.

The immediate consequence is claim discipline. AETHER can now say that the repository has a FAIR-ready handoff scaffold and a named gap matrix. It still cannot say that FAIR confirms the temperature results. That requires species-level CH4 and N2O trajectories, aerosol precursor emissions, annual lifecycle-emissions traces, zero-emissions commitment diagnostics, carbon-cycle asymmetry calibration, uncertainty ensembles, and historical spin-up. FAIR remains the right next model class for this step because it connects emissions, concentrations, forcing, and temperature response in a way the current screening emulator only approximates [@fair_v13_smith_2018].

The generated outputs are `analysis/tables/aether_fair_readiness_input_deck.csv`, `analysis/tables/aether_fair_readiness_summary.csv`, `analysis/tables/aether_fair_readiness_gap_matrix.csv`, `analysis/tables/aether_fair_readiness_run_manifest.csv`, and `analysis/figures/fair_readiness_climate_input_deck.png`.

### 4.2.5 Forcing-Driven FAIR Execution

The v0.40 repo adds the first actual FAIR package run. This is a meaningful step, but it is not the final climate model. The model uses FAIR 2.2.4 in forcing mode, supplies the AETHER CO2 forcing, aggregate non-CO2 forcing, and aggregate aerosol forcing paths from the FAIR-readiness handoff deck, initializes the 2026 temperature state from the screening emulator, and runs three diagnostic thermal-response configurations.

![AETHER forcing-driven FAIR execution](../../analysis/figures/fair_forcing_execution_comparison.png)

| Scenario | FAIR 2100 C | Screen 2100 C | FAIR - screen |
| --- | --- | --- | --- |
| No AETHER stress | 4.14 | 3.24 | 0.90 |
| AETHER 58% rebound stress | 2.92 | 2.38 | 0.54 |
| AETHER net-zero/full forcing | 1.15 | 1.10 | 0.05 |
| AETHER no rebound/full forcing | 1.16 | 1.11 | 0.05 |

The central result is not that the exact temperatures are now final. They are not. The useful result is that AETHER now has a real package-executed climate-response layer. Under the central diagnostic configuration, the delayed non-CO2 plus aerosol-unmasking stress case reaches 4.14 C in 2100 without AETHER and 2.92 C with AETHER plus 58% rebound. AETHER plus net-zero 2050 and active full-forcing management reaches 1.15 C.

This should narrow, not expand, the claim. A forcing-driven FAIR run is more defensible than the homegrown two-box screen, but it still inherits aggregate forcing paths. Publication-grade climate claims still need species-level CH4 and N2O trajectories, aerosol precursor emissions, land-use forcing, lifecycle-emissions traces, historical spin-up, ZEC diagnostics, and uncertainty ensembles. The paper should treat this layer as a real execution bridge between AETHER's industrial feasibility model and a later full FAIR or Earth-system study.

The generated outputs are `analysis/tables/aether_fair_forcing_temperature_paths.csv`, `analysis/tables/aether_fair_forcing_summary.csv`, `analysis/tables/aether_fair_forcing_config.csv`, `analysis/tables/aether_fair_forcing_delta_vs_emulator.csv`, and `analysis/figures/fair_forcing_execution_comparison.png`.

### 4.2.6 Species-Emissions FAIR Handoff and Publication Gate

The repo adds a species-emissions handoff layer. It is not a temperature forecast. It is a blocker map for replacing the aggregate forcing paths used in the forcing-driven FAIR diagnostic with species-level inputs.

![AETHER species-emissions FAIR handoff](../../analysis/figures/species_emissions_handoff_gap_matrix.png)

| Metric | Value |
| --- | --- |
| Species/forcing families | 16 |
| Pathway rows | 28800 |
| Readiness score | 0.31 |
| P0 blocking families | 10 |
| Publication gates failing | 7 |

The result is intentionally restrictive. The handoff matrix tracks 16 species or forcing families across 28800 annual scenario-family rows. Only 0 families are usable screens. 4 are provisional proxies, 7 are aggregate placeholders, and 5 are missing. The score is 0.31, with 10 P0 blocking families. The publication-gate table has 7 fail rows and 3 partial rows.

This keeps the AETHER climate claim disciplined. The forcing-driven FAIR run is useful because it tests the aggregate forcing story through a real package response engine. It is not enough for publication-grade climate reversal claims. A full upgrade needs CH4, N2O, halogenated gases, ozone precursors, SO2, black carbon, organic carbon, nitrate/ammonia precursors, land-use forcing, lifecycle species traces, historical spin-up, zero-emissions-commitment diagnostics, ocean-chemistry treatment for ocean CDR, and uncertainty ensembles.

The generated outputs are `analysis/tables/aether_species_emissions_handoff_pathways.csv`, `analysis/tables/aether_species_emissions_requirement_matrix.csv`, `analysis/tables/aether_species_emissions_summary.csv`, `analysis/tables/aether_species_emissions_publication_gates.csv`, and `analysis/figures/species_emissions_handoff_gap_matrix.png`.

### 4.3 Energy

IPCC AR6 WGIII reports a theoretical minimum energy requirement for separating CO2 from air of about 0.5 GJ/tCO2 and current technology total energy requirements of about 4-10 GJ/tCO2 [@ipcc_ar6_wg3_ch12]. The AETHER model evaluates 1, 3, 8, and 11.94 GJ/tCO2 cases. The 11.94 GJ/tCO2 case is 3 GJ/tCO2 capture plus full CO2 splitting.

NIST lists the standard gas enthalpy of formation of CO2 as -393.51 kJ/mol [@nist_chemistry_webbook_co2]. Reversing the reaction CO2 -> C + O2 gives an ideal enthalpy floor of about 8.94 GJ/tCO2. This is not an engineering energy estimate. It is a lower bound before real electrochemical losses, separations, compression, product handling, and capital costs.

| Scenario | Capture energy | Split fraction | Total energy | Annual energy at 100 GtCO2/year | Average power |
|---|---:|---:|---:|---:|---:|
| Near-thermodynamic capture and storage | 1.0 GJ/tCO2 | 0% | 1.00 GJ/tCO2 | 27,778 TWh/year | 3.17 TW |
| Advanced capture and storage | 3.0 GJ/tCO2 | 0% | 3.00 GJ/tCO2 | 83,333 TWh/year | 9.51 TW |
| Current DAC-like capture and storage | 8.0 GJ/tCO2 | 0% | 8.00 GJ/tCO2 | 222,222 TWh/year | 25.37 TW |
| Advanced capture plus 25% splitting | 3.0 GJ/tCO2 | 25% | 5.24 GJ/tCO2 | 145,427 TWh/year | 16.60 TW |
| Advanced capture plus 100% splitting | 3.0 GJ/tCO2 | 100% | 11.94 GJ/tCO2 | 331,708 TWh/year | 37.87 TW |

The energy conclusion is harsh. Even the near-thermodynamic case requires a dedicated power system measured in terawatts. The advanced 3 GJ/tCO2 storage case requires about 83,333 TWh/year, roughly 98 times the 2025 global electricity-generation increase of over 850 TWh reported by IEA [@iea_global_energy_review_2026]. If built over 20 years in a roughly linear buildout, the 3 GJ/tCO2 case requires adding about 4,167 TWh/year of dedicated clean generation each year, nearly five times the 2025 total global electricity increment and nearly seven times the 2025 solar PV generation increase of about 600 TWh [@iea_global_energy_review_2026].

That does not make the target impossible. It means the abundance assumption must include a major expansion of energy infrastructure, not just better software. AETHER is mainly an energy and storage problem with AI and robotics as accelerants.

### 4.4 Power-System Buildout

Energy demand is not enough. AETHER also has to translate TWh into installed capacity, capacity factors, land, firm supply, storage, and annual construction. The v0.15 power-system screen uses NREL ATB as the source framework for electricity technology parameters [@nrel_atb_2024_electricity], NREL land-use data for utility-scale solar land proxies [@nrel_solar_land_use_2013], NREL's land-based wind and nuclear ATB pages for wind and nuclear capacity-factor anchors [@nrel_atb_land_wind_2024; @nrel_atb_nuclear_2024], IAEA's current nuclear scale data [@iaea_nuclear_status_2025], IEA's geothermal report [@iea_geothermal_future_2024], and IEA Electricity 2026 for storage/flexibility anchors [@iea_electricity_2026].

The main AETHER 3 GJ/tCO2 case needs 83,333 TWh/year delivered to removal. In a balanced clean-power portfolio with a 10% gross generation penalty for curtailment, storage, transmission, and auxiliary losses, that becomes about 91,667 TWh/year of gross clean generation. With the current scenario capacity factors, the required nameplate capacity is about 27.5 TW: roughly 15 TW solar PV, 9 TW wind, 2.3 TW nuclear, and 1.2 TW advanced geothermal.

| Portfolio | Delivered AETHER electricity | Gross generation incl. penalty | Required nameplate | Firm clean capacity | Solar land proxy | Four-hour storage proxy |
|---|---:|---:|---:|---:|---:|---:|
| Near-thermodynamic balanced | 27,778 TWh/y | 30,556 TWh/y | 9.2 TW | 1.2 TW | 151,476 km2 | 2,442 GWh |
| Portfolio/lifecycle balanced | 64,750 TWh/y | 71,225 TWh/y | 21.3 TW | 2.7 TW | 353,091 km2 | 5,691 GWh |
| 3 GJ/tCO2 balanced | 83,333 TWh/y | 91,667 TWh/y | 27.5 TW | 3.5 TW | 454,429 km2 | 7,325 GWh |
| 3 GJ/tCO2 solar-heavy | 83,333 TWh/y | 100,000 TWh/y | 39.0 TW | 1.3 TW | 920,661 km2 | 10,274 GWh |
| Full splitting balanced | 331,708 TWh/y | 364,879 TWh/y | 109.3 TW | 13.9 TW | 1,808,850 km2 | 29,157 GWh |

The balanced 3 GJ/tCO2 case needs about 3.5 TW of firm clean capacity from nuclear and advanced geothermal in this stylized mix. Current operational nuclear capacity is about 377 GW(e), with 64.5 GW(e) under construction at the end of 2024 [@iaea_nuclear_status_2025]. IEA's geothermal report gives a cost-effective 2050 case of about 800 GW producing almost 6,000 TWh/year if technology improves [@iea_geothermal_future_2024]. AETHER therefore needs firm clean power on a scale larger than today's nuclear industry and larger than IEA's cost-effective geothermal deployment case unless capture energy falls much further or the portfolio leans heavily on variable renewables.

The solar-heavy case is instructive. It lowers the firm-power requirement, but it raises nameplate capacity to about 39.0 TW and gives a utility-scale solar land proxy of about 920,661 km2. That land proxy is not a forecast; actual deployment could use rooftops, deserts, agrivoltaics, offshore energy, higher-efficiency modules, or different regional mixes. It does show that a market-led clean-energy path still needs siting, transmission, storage, and public legitimacy at continental scale.

The short-duration storage proxy is deliberately modest: enough four-hour battery-equivalent storage to shift 25% of average VRE output. For the 3 GJ/tCO2 balanced case, that is about 7,325 GWh. At IEA's 2024 utility-scale project-cost anchor of about $150/kWh, this proxy alone is about $1,099B [@iea_electricity_2026]. It is not seasonal storage and not a reliability reserve. It is a floor-level reminder that generation capacity is only one piece of the power-system requirement.

This strengthens the core plausibility filter. AI and robotics can accelerate solar factories, wind manufacturing, nuclear construction, geothermal drilling, battery deployment, transmission inspection, and automated demand response. They cannot make 24% solar capacity factors behave like firm power. The energy system remains the largest coupled bottleneck in the current AETHER model.
### 4.5 Storage State and Conversion Ledger

At 100 GtCO2/year, storage state matters as much as capture technology. Gas-phase CO2 is too bulky for planetary-scale storage. Supercritical geologic storage is far denser. National Academies reports discuss supercritical CO2 storage in deep sedimentary formations and cite an approximate density near 600 kg/m3 [@national_academies_net_reliable_sequestration]. NIST reference-data publications and the NIST Chemistry WebBook provide the fluid-property basis for density calculations across gas, liquid, and supercritical states [@nist_thermophysical_fluids_2009; @nist_cryogenic_fluid_properties].

The current ledger estimates the following annual physical quantities for 100 GtCO2/year:

| State or product | Mass | Volume | Added conversion energy | Interpretation |
|---|---:|---:|---:|---|
| CO2 gas at STP | 100.0 Gt/year | 50,505 km3/year | 0 TWh/year | Not a serious storage state at AETHER scale |
| Supercritical CO2 | 100.0 Gt/year | 166.7 km3/year | 0 TWh/year | Plausible default storage state, subject to geology, injection rates, pressure, monitoring, liability, and public acceptance |
| Solid carbon from full splitting | 27.3 Gt/year | 12.4 km3/year | 248,333 TWh/year | Compact, but requires the 8.94 GJ/tCO2 ideal splitting burden before real losses |
| Liquid O2 coproduct from full splitting | 72.7 Gt/year | 63.7 km3/year | Coupled to splitting | Product handling is unsafe at scale; atmospheric release may be preferable but local oxygen hazards still matter |
| Magnesite-equivalent mineral carbonate | 191.6 Gt/year | 63.9 km3/year | pathway-specific | Durable and dense, but constrained by reactive minerals, grinding, transport, kinetics, water, land disturbance, and local impacts |

This table argues against full CO2 splitting as the default plan. NIST lists the standard gas enthalpy of formation of CO2 as -393.51 kJ/mol; reversing CO2 formation gives an ideal CO2 -> C + O2 floor of about 8.94 GJ/tCO2 [@nist_chemistry_webbook_co2; @nist_chemistry_webbook_co2_calculated]. At 100 GtCO2/year, that splitting energy alone is about 248,333 TWh/year, or 28.3 TW average power, before actual electrochemical losses.

The product scale is also extreme. Full splitting produces about 27.3 Gt/year of solid carbon. OSHA lists natural graphite specific gravity at 2.0-2.25 [@osha_graphite_natural_chemicaldata_2020]. USGS reports 2025 world natural graphite mine production of about 1.8 million tonnes and recoverable world resources above 800 million tonnes [@usgs_graphite_mcs_2026]. The AETHER solid-carbon stream would therefore be about 15,162 times current annual natural graphite production and about 34.1 times reported recoverable natural graphite resources every year. AETHER carbon would be manufactured rather than mined natural graphite, but the comparison shows that solid-carbon handling is an industrial system in its own right.

Mineral carbonate storage avoids the O2 coproduct and can be highly durable. A magnesite-equivalent proxy using magnesium carbonate's molar mass and density gives about 191.6 Gt/year of carbonate product and about 63.9 km3/year of solid volume [@pubchem_magnesium_carbonate_2026]. That is physically denser than supercritical CO2 but shifts the bottleneck into mineral supply, mining, grinding, transport, reaction kinetics, water, land disturbance, and local environmental governance.

The current AETHER conclusion is narrow: most removal should probably use geologic storage, in situ mineralization, ocean-alkalinity pathways where safe, or hybrid storage. Splitting may still matter for special cases: industrial carbon products, high-durability storage, remote systems with stranded energy, or closed-loop processes where oxygen/carbon handling has value. It should not be the base case unless energy becomes extraordinarily cheap and the product-handling system is designed explicitly.
### 4.6 Air Throughput and Plant-Scale Hardware

The concentration problem is not just an energy problem. At NOAA's February 2026 global mean of 428.53 ppm CO2 [@noaa_gml_global_co2_2026], the model estimates about 0.83 grams CO2 per m3 of air before humidity, altitude, temperature, and local circulation effects. That makes air movement a first-order design constraint. NASEM's DAC chapter gives a useful engineering anchor: at 1.5 m/s air velocity and 75% capture, a 1 MtCO2/year contactor needs about 38,000 m2 of cross-sectional area [@national_academies_dac_ch5_2018]. Keith et al. give the related 1 MtCO2/year engineered KOH DAC plant comparator [@keith_2018_process_dac].

| Case | Air flow | Contactor face area | Fan electricity | 1 Mt/y plant equivalents | STRATOS equivalents |
|---|---:|---:|---:|---:|---:|
| 40 Gt/y DACCS, NASEM reference | 2.26 billion m3/s | 1,508 km2 | 3,716 TWh/y | 40,000 | 80,000 |
| 40 Gt/y DACCS, AETHER low-pressure | 1.95 billion m3/s | 651 km2 | 2,248 TWh/y | 40,000 | 80,000 |
| 100 Gt/y all-air, NASEM reference | 5.66 billion m3/s | 3,771 km2 | 9,290 TWh/y | 100,000 | 200,000 |
| 100 Gt/y all-air, AETHER low-pressure | 4.88 billion m3/s | 1,627 km2 | 5,621 TWh/y | 100,000 | 200,000 |
| 100 Gt/y all-air, high-pressure warning | 7.49 billion m3/s | 7,486 km2 | 130,056 TWh/y | 100,000 | 200,000 |

The all-air 100 GtCO2/year stress test is deliberately harsher than the current AETHER portfolio, which allocates 40 GtCO2/year to DACCS and spreads the rest across mineralization, ocean alkalinity, BECCS, biochar, afforestation/reforestation, and direct ocean or electrochemical CDR. Still, even the 40 GtCO2/year DACCS branch implies about 1,508 km2 of NASEM-reference contactor face area and about 80,000 STRATOS-scale facility equivalents. 1PointFive says STRATOS is designed for up to 500,000 tonnes CO2/year when fully operational [@onepointfive_stratos_2026]. Climeworks Mammoth is smaller, at up to 36,000 tons/year nameplate capacity [@climeworks_mammoth_2024]. These are not criticism of either company; they are scale markers. AETHER cannot extrapolate from first commercial plants to climate reversal without a factory-rate model.

The pressure-drop sensitivity is equally important. In the NASEM-reference 100 GtCO2/year case, fan electricity is about 9,290 TWh/year. In the AETHER low-pressure modular case it falls to about 5,621 TWh/year. In the high-pressure warning case, fan electricity alone rises to about 130,056 TWh/year. This is why AI-designed contactors and sorbents matter only if they reduce real pressure drop, fouling, cycle time, thermal load, and maintenance. A better model cannot make a bad contactor cheap.

Solid sorbents add an inventory problem. NASEM reports solid-sorbent total-capacity and lifetime ranges, and NETL's 2025 sorbent DAC report frames current generic sorbent systems as still unoptimized reference cases [@national_academies_dac_ch5_2018; @netl_sorbent_dac_2025]. In the NETL-style reference loading scenario, the 100 GtCO2/year all-air case needs about 150.1 Mt of sorbent inventory and about 75.1 Mt/year replacement. The AETHER improved sorbent case lowers that to about 34.8 Mt inventory and 7.0 Mt/year replacement, but that is a research target rather than a current materials claim.

The conclusion is practical. AETHER needs a contactor and sorbent industrial base, not only cheap energy. Robotics can fabricate modules, inspect fans, replace fouled media, run warehouses, and maintain distributed sites. AI can search materials and control cycles. But the physical system still has to move billions of cubic meters of air per second across active surfaces without wasting the energy budget in pressure drop.
### 4.7 Pathway Portfolio

The 100 GtCO2/year target should not be read as a DAC-only proposal. IPCC AR6 WGIII reports very different cost, potential, maturity, and risk profiles across CDR methods, and the National Academies ocean CDR report treats ocean approaches as important but still research-constrained [@ipcc_ar6_wg3_technical_summary_cdr; @national_academies_ocean_cdr_2021]. The State of CDR also makes the present-scale problem concrete: current CDR is mostly conventional land-based removal, while novel CDR remains tiny relative to the scale implied by climate targets [@state_of_cdr_2026].

The v0.11 source-range layer compares the current AETHER portfolio against those assessed ranges. It does not make the portfolio conservative. It makes the optimism more explicit.

| Pathway | AETHER allocation | Assessed potential | Assessed cost | TRL | Current read |
|---|---:|---:|---:|---:|---|
| DACCS | 40 Gt/y | 5-40 Gt/y | -300; full range -386 | 6 | AETHER uses the top of the IPCC assessed DACCS potential range, so DACCS cannot absorb much model slippage. |
| Enhanced weathering/mineralization | 20 Gt/y | 2-4; full range <1-95 Gt/y | -200; full range -578 | 3-4 | AETHER is five times the central high estimate but still inside the very wide full literature range. |
| Ocean alkalinity enhancement | 15 Gt/y | 1-100 Gt/y | -260 | 1-2 | The allocation is inside the assessed potential range, but the method is low-TRL and must survive marine chemistry, ecology and governance review. |
| BECCS | 10 Gt/y | 0.5-11 Gt/y | -400 | 5-6 | AETHER is close to the upper assessed range; the land, water and biomass-supply penalty is the main reason not to push it harder. |
| Biochar | 6 Gt/y | 0.3-6.6 Gt/y | -345 | 6-7 | AETHER is near the upper assessed range, which is plausible only with large sustainable biomass and high-quality permanence/MRV. |
| Afforestation/reforestation | 5 Gt/y | 0.5-10 Gt/y | -240 | 8-9 | The allocation is inside the assessed range, but it is not a substitute for durable engineered storage. |
| Direct ocean/electrochemical CDR | 4 Gt/y | not resolved as a separate pathway range Gt/y | NASEM: end-to-end CDR roughly -700/tCO2; electrochemical has highest assessed scale-up cost among ocean approaches | research-to-early demonstration | The 4 GtCO2/year allocation is a placeholder until electrochemical ocean CDR has method-specific sourced ranges. |

The source-range comparison changes how the portfolio should be read. DACCS at 40 GtCO2/year uses the top of the IPCC assessed potential range. BECCS at 10 GtCO2/year and biochar at 6 GtCO2/year sit near their upper assessed ranges. Enhanced weathering at 20 GtCO2/year is far above the central assessed range of 2-4 GtCO2/year, although still inside the very wide full literature range. Ocean alkalinity at 15 GtCO2/year is inside the assessed potential range, but the method is low-TRL and depends on marine chemistry, ecological monitoring, permitting, and MRV working at industrial scale. Direct ocean/electrochemical CDR remains the least mature part of the portfolio because the current allocation is not yet backed by a separate method-specific potential range.

The current optimized 100 GtCO2/year allocation therefore should be treated as a stress-test portfolio, not as a forecast: 40 Gt/y DACCS, 20 Gt/y enhanced weathering/mineralization, 15 Gt/y ocean alkalinity, 10 Gt/y BECCS, 6 Gt/y biochar, 5 Gt/y afforestation/reforestation, and 4 Gt/y direct ocean/electrochemical CDR. It totals about $8.4T/year, 56,528 TWh/year, 6.45 TW average power, $84/tCO2 weighted cost, and 2.03 GJ/tCO2 weighted energy in the current model output. The assessed central-potential sum is much lower than 100 GtCO2/year, which means the portfolio requires either upper-tail performance, new pathway capacity, or a future technology layer that is not yet in the source-backed table.

This is one of the strongest feasibility filters in the paper. If AETHER cannot turn a pathway portfolio into a governed industrial system, then 100 GtCO2/year is just a number. If it can, the project becomes less like a single carbon-removal company and more like a global infrastructure program: storage basins, mining and materials systems, ocean monitoring, biomass supply chains, automated construction, and policy institutions all operating under one atmospheric management objective.
### 4.8 Storage Lifecycle and Regionalization

The pathway portfolio is still a gross-removal model. A captured tonne becomes a climate-relevant tonne only after energy supply, transport, storage, monitoring, and permanence are counted. This version therefore adds a storage-lifecycle filter. It is not a full reservoir simulator. It is a discipline layer that asks how much of the 100 GtCO2/year gross portfolio survives when lifecycle penalties and 100-year durability haircuts are applied.

The storage resource headline is encouraging but incomplete. USGS Circular 1386 estimates a mean technically accessible U.S. geologic storage resource near 3,000 GtCO2, with resources assessed at depths of at least 3,000 feet and with large concentration in the coastal plains and Gulf Coast [@usgs_circular_1386_geologic_storage]. IPCC AR6 WGIII gives a broader global frame: theoretical geologic storage potential is around 10,000 GtCO2, usable storage is lower than theoretical, saline aquifers hold most capacity, reservoir quality and distribution matter, and injection can be pressure-limited even where resource is large [@ipcc_ar6_wg3_ch6_ccs_storage]. IPCC also reports very low estimated leakage rates for well-managed geologic sequestration, below 0.001% per year, but that does not remove the engineering problem [@ipcc_ar6_wg3_ch6_ccs_storage]. A USGS review makes the risk point directly: the volumes needed to materially affect atmospheric CO2 are far greater than the volumes injected so far, and pressure management, induced seismicity, liability, and property rights can become binding constraints [@usgs_anderson_storage_risk_liability_2017].

| Pathway | Gross allocation | 100-year durable credit | Lifecycle penalty | 100-year retention | Added storage energy | Deployment burden |
|---|---:|---:|---:|---:|---:|---:|
| DACCS with geologic storage | 40 Gt/y | 37.6 Gt/y | 6% | 100% | 3,889 TWh/y | 40,000 one-Mt/y wells |
| Enhanced weathering and surficial mineralization | 20 Gt/y | 17.6 Gt/y | 12% | 100% | 1,389 TWh/y | 2,000 ten-Mt/y hubs |
| Ocean alkalinity enhancement | 15 Gt/y | 12.1 Gt/y | 15% | 95% | 1,458 TWh/y | 1,500 ten-Mt/y hubs |
| BECCS | 10 Gt/y | 8.0 Gt/y | 20% | 100% | 417 TWh/y | 10,000 one-Mt/y wells |
| Biochar | 6 Gt/y | 4.0 Gt/y | 18% | 82% | 167 TWh/y | 600 ten-Mt/y hubs |
| Afforestation and reforestation | 5 Gt/y | 2.1 Gt/y | 25% | 55% | 69 TWh/y | 500 ten-Mt/y hubs |
| Direct ocean capture and electrochemical mCDR | 4 Gt/y | 3.5 Gt/y | 12% | 100% | 833 TWh/y | 4,000 one-Mt/y wells |

Under these assumptions, the 100 GtCO2/year gross portfolio produces about 84.9 GtCO2/year of 100-year durable credited removal. The shortfall is about 15.1 GtCO2/year. Holding the same pathway mix, AETHER would need about 118 GtCO2/year gross removal to credit 100 GtCO2/year on this lifecycle-adjusted basis. The storage and lifecycle energy penalty adds about 8,222 TWh/year, bringing the portfolio energy screen to about 64,750 TWh/year, or 7.4 TW average.

This changes the language the paper should use. The target cannot simply be "100 GtCO2/year removed." It has to specify whether that means gross captured CO2, stored CO2, lifecycle-adjusted net removal, or 100-year durable credited removal. The difference is not academic. At this scale, a ten-percent lifecycle or durability error is ten gigatonnes per year. AETHER needs explicit buffer capacity, route-specific MRV, and storage contracts that keep liability alive longer than the equipment manufacturer.


### 4.8.1 Regional Storage and Injection Corridors

The previous storage screen still hides a major constraint: storage is regional. AETHER cannot inject CO2 into "global storage capacity." It needs source-to-sink corridors with wells, compression, pipelines or shipping, brine and pressure management, pore-space rights, monitoring, public consent, and a regulator willing to permit the operation.

This version adds a first regional corridor screen for the 54 GtCO2/year geologic-storage component of the current 100 GtCO2/year portfolio. The U.S. capacity rows are anchored to USGS Circular 1386, which estimates about 3,000 GtCO2 of mean technically accessible U.S. geologic storage resource in onshore and state-water formations and reports that the U.S. Gulf Coast area represents 59% of national CO2 storage capacity [@usgs_circular_1386_geologic_storage]. NETL's Carbon Storage Atlas V adds North American storage-resource and Regional Carbon Sequestration Partnership context [@netl_carbon_storage_atlas_v_2015]. The non-U.S. rows are not paper-ready capacity estimates. They are scenario placeholders that keep the model honest until regional basin sources are added.

| Region | Evidence class | Assigned injection | Proxy capacity | Years at assigned rate | 1 Mt/y pressure-adjusted well equivalents |
|---|---|---:|---:|---:|---:|
| U.S. Gulf Coast / Coastal Plains | source-backed U.S. anchor | 16 Gt/y | 1770 Gt | 111 | 22,400 |
| East and South Asia industrial basins | scenario placeholder | 9 Gt/y | 600 Gt | 67 | 13,050 |
| Middle East / North Africa storage provinces | scenario placeholder | 8 Gt/y | 500 Gt | 63 | 9,600 |
| Other U.S. assessed basins | source-backed U.S. anchor | 8 Gt/y | 1230 Gt | 154 | 10,400 |
| North Sea / Northwest Europe | scenario placeholder | 5 Gt/y | 200 Gt | 40 | 6,250 |
| Other global saline-basin corridors | scenario placeholder | 4 Gt/y | 350 Gt | 88 | 5,400 |
| Australia and other high-storage basins | scenario placeholder | 4 Gt/y | 350 Gt | 88 | 4,600 |

The headline is not that AETHER should store 24 GtCO2/year in the United States. The headline is that even a favorable U.S. storage-resource anchor does not remove the injection problem. At the current 54 GtCO2/year geologic target, the source-backed U.S. 3,000 GtCO2 capacity anchor would represent about 55.6 years of capacity if it were all usable for AETHER. But at 1 MtCO2/year per injection well after pressure-management multipliers, the scenario needs about 71,700 pressure-adjusted injection-well equivalents globally. At 0.25 MtCO2/year, the requirement rises to about 286,800 wells. At 2 MtCO2/year, it is still about 35,850 wells.

The U.S. permitting frame makes the scale visible. EPA describes Class VI wells as CO2 injection wells for long-term geologic sequestration, including CO2 captured directly from the atmosphere, and lists requirements for site characterization, plume and pressure-front modeling, area-of-review corrective action, well construction, monitoring, financial responsibility, emergency and remedial response, reporting, and post-injection phases [@epa_class_vi_wells_2026]. EPA's current-projects page says each Class VI well needs an individual well application and permit, with primacy-state caveats and a periodically updated review dashboard [@epa_current_class_vi_projects_2026]. Under this crude allocation, the U.S. rows alone imply about 32,800 Class VI permit-equivalent wells in the 1 Mt/year case.

This is why storage has to become a separate AETHER model rather than a line item. Capacity is necessary but not sufficient. The publication-grade version needs basin-level capacity, permeability, injection-rate distributions, pressure-management cost, brine handling, pipeline and shipping routes, existing-well corrective action, pore-space ownership, induced-seismicity screening, long-term liability, and community consent.

### 4.9 Material and Industrial Supply-Chain Pressure

AETHER cannot stop at energy and robot arithmetic. A removal system this large has to be built out of steel, cement, copper, sorbents, solvents, membranes, catalysts, fans, compressors, heat exchangers, pipelines, drilling equipment, sensors, replacement media, and low-carbon manufacturing capacity. WRI's DAC impacts review makes the basic point directly: DAC plants require materials such as concrete, steel, plastic, aluminum, and copper, and those upstream impacts matter in high scale-up scenarios [@wri_scaling_dac_impacts_2024]. World Steel Association data put 2024 crude steel production at about 1,885 Mt [@worldsteel_figures_2025]. USGS MCS 2025 reports rounded 2024 world cement production of about 4,000 Mt [@usgs_mcs_2025_cement]. IEA's critical-minerals outlook warns that energy-transition mineral demand rises materially under energy-technology deployment, with copper demand growing because grids, electrification, and industrial equipment all pull on the same supply chain [@iea_critical_minerals_outlook_2025].

The first material screen separates three classes. Structural mass is large but potentially manageable if AETHER designs stay modular and light. The 100 GtCO2/year all-air moderate contactor-frame proxy uses about 18.9 Mt/year of steel over a 20-year buildout, about 1.0% of current crude steel production. Power infrastructure is more demanding in this screen: the 3 GJ/tCO2 balanced clean-power case uses about 68.8 Mt/year of steel and 2.8 Mt/year of copper under crude proxy intensities. The copper number is about 10.2% of the rounded refined-copper production proxy, before ordinary electrification, AI data centers, industrial heat, housing, and grid replacement make their claims.

| Screen item | Annual material demand | Comparator share | Evidence class |
|---|---:|---:|---|
| Legacy NaOH 0.17 t/t | 17,000 Mt/y | 425% of world cement production proxy | source-backed critique scaled to AETHER target |
| Legacy NaOH 0.29 t/t | 29,000 Mt/y | 725% of world cement production proxy | source-backed critique scaled to AETHER target |
| DACCS media 0.5%/t | 200 Mt/y | 5% of world cement production proxy | scenario assumption informed by DAC material-risk literature |
| DACCS media 2.0%/t | 800 Mt/y | 20% of world cement production proxy | scenario assumption informed by DAC material-risk literature |
| Power copper | 3 Mt/y | 10.2% of world refined copper production proxy | scenario assumption with IEA critical-minerals context |
| Power steel | 69 Mt/y | 3.6% of world crude steel production | scenario assumption with source-backed global comparator |
| All-air contactor steel | 19 Mt/y | 1% of world crude steel production | scenario assumption with source-backed global comparator |
| Pipeline steel | 3 Mt/y | 0.1% of world crude steel production | scenario placeholder with source-backed global comparator |

The reactive-media result is sharper. Chatterjee and Huang's DAC critique reports NaOH makeup rates of 0.17-0.29 t per tCO2 in one large-deployment DAC case, along with major energy and coproduct burdens [@chatterjee_huang_2020_unrealistic_dac]. Scaled to a 100 GtCO2/year all-air AETHER case, that is 17,000-29,000 Mt/year of NaOH-equivalent reactive media. That is not a rounding error. It is several times current world cement production. AETHER therefore cannot treat legacy high-makeup solvent chemistry as a plausible base case.

The optimistic case is not "materials do not matter." It is that AI-assisted chemistry, closed-loop media recovery, better sorbent lifetime, modular maintenance, and automated recycling push replacement rates down by orders of magnitude. Even then, the 40 GtCO2/year DACCS branch at 0.5% replacement media needs about 200 Mt/year of media, and at 2% it needs about 800 Mt/year. Those flows might be imaginable in a future automated chemical industry, but only if the media are cheap, low-toxicity, recyclable, low-carbon, and not dependent on scarce feedstocks.

This changes the feasibility claim. Structural materials look like a major industrial allocation. Reactive media and copper look like gating constraints. The next AETHER model should stop using pathway-level cost buckets alone and build pathway-specific bills of materials, replacement schedules, recycling loops, embodied emissions, and commodity competition with the rest of the energy transition.

### 4.10 MRV and Credit Integrity Filter

AETHER cannot treat gross captured tonnes, durable tonnes, and creditable tonnes as the same object. A gross tonne is an engineering output. A durable tonne is a physical climate claim after lifecycle and permanence. A creditable tonne is a governance claim: someone is allowed to use that tonne in accounting, finance, regulation, or public legitimacy. That last step needs measurement, reporting, verification, reversal buffers, invalidation rules, and liability.

The v0.24 model adds a provisional credit-integrity filter on top of the existing storage-lifecycle screen. The sources anchor the standard rather than the numeric buffers. EPA Class VI and Subpart RR define a relatively concrete U.S. geologic-storage MRV frame: site characterization, plume and pressure-front modeling, leakage-pathway analysis, monitoring, financial responsibility, mass-balance reporting, and EPA-approved MRV plans [@epa_class_vi_wells_2026; @epa_subpart_rr_mrv_2026]. The EU CRCF creates a certification frame with quality criteria, monitoring and reporting processes, third-party verification, and registry publication [@eu_crcf_2024]. The Oxford principles push offsetting toward durable removals with low reversal risk [@oxford_offsetting_principles_2024]. The National Academies ocean CDR research strategy keeps ocean approaches in a research-gap posture, especially around risks, governance, and responsible deployment [@national_academies_ocean_cdr_2022].

The current stress test starts with the 100 GtCO2/year AETHER pathway portfolio. The existing lifecycle model credits about 84.879 GtCO2/year on a 100-year basis. The MRV model then applies provisional discounts for measurement uncertainty, method uncertainty, reversal or leakage buffers, and credit-invalidation reserves. Under those assumptions, the same portfolio credits only about 66.445 GtCO2/year. To credit 100 GtCO2/year at the same pathway mix, AETHER would need about 150.500 GtCO2/year of gross removal, or roughly 50.500 GtCO2/year above the nominal target.

The generated by-pathway table is analysis/tables/aether_mrv_credit_integrity_by_pathway.csv; the portfolio-level overbuild and cost summary is analysis/tables/aether_mrv_credit_integrity_summary.csv.

| Pathway | Gross Gt/y | 100y durable Gt/y | Creditable Gt/y | Gross per credit | MRV risk class |
| --- | --- | --- | --- | --- | --- |
| DACCS with geologic storage | 40.0 | 37.6 | 34.6 | 1.16x | lower_mrv_risk_high_durability |
| Direct ocean capture and electrochemical mCDR | 4.0 | 3.5 | 2.9 | 1.38x | medium_mrv_risk_low_trl |
| BECCS | 10.0 | 8.0 | 6.8 | 1.47x | medium_mrv_risk |
| Enhanced weathering and surficial mineralization | 20.0 | 17.6 | 11.8 | 1.70x | medium_high_mrv_risk |
| Ocean alkalinity enhancement | 15.0 | 12.1 | 7.1 | 2.11x | high_mrv_risk_low_trl |
| Biochar | 6.0 | 4.0 | 2.5 | 2.45x | medium_high_reversal_risk |
| Afforestation and reforestation | 5.0 | 2.1 | 0.8 | 6.48x | high_reversal_and_counterfactual_risk |

The table is not a forecast. It is a discipline layer. Geologic storage looks stronger because the boundary is more observable. Diffuse land and ocean pathways may still be valuable, but they should not be treated as fungible credit unless the measurement and reversal problem is solved. If AETHER sells gross tonnes as creditable tonnes, it becomes a cleaner-looking offset machine. The serious version needs adversarial MRV, public registries, invalidation rules, liability reserves, and a willingness to reject cheap credits that cannot survive measurement.

### 4.11 Explicit Lifecycle Emissions Screen

The storage-lifecycle and MRV sections already show that gross captured tonnes are not the same as durable or creditable tonnes. The v0.27 lifecycle-emissions screen adds another filter: operational energy emissions and non-power embodied emissions. This matters because a 100 GtCO2/year system can look physically large but still fail its climate purpose if it uses dirty power, high-emissions construction, disposable media, carbon-intensive logistics, or a storage chain that creates large upstream emissions.

The model is intentionally transparent. It uses four electricity-emissions cases: 5, 25, 100, and 250 kgCO2/MWh. It then adds pathway-specific placeholder non-power LCA burdens for construction, media replacement, transport/storage, and decommissioning. In the 25 kgCO2/MWh case, 64,750 TWh/year produces about 1.619 GtCO2e/year of power emissions; the remaining approximately 10.678 GtCO2e/year in the 12.297 Gt total comes from provisional non-power construction, media, transport/storage, and decommissioning terms. The latter dominate this case and require pathway-specific replacement before the result can be treated as an LCA estimate. In the 25 kgCO2/MWh case, 64,750 TWh/year produces about 1.619 GtCO2e/year of power emissions; the remaining approximately 10.678 GtCO2e/year in the 12.297 Gt total comes from provisional non-power construction, media, transport/storage, and decommissioning terms. The latter dominate this case and require pathway-specific replacement before the result can be treated as an LCA estimate. Those terms are not final LCAs. They are the current work queue. WRI's DAC impacts review anchors the need to count DAC materials and local impacts [@wri_scaling_dac_impacts_2024]. The material-supply model anchors steel, cement, and copper comparators [@worldsteel_figures_2025; @usgs_mcs_2025_cement; @iea_critical_minerals_outlook_2025]. The MRV and credit-integrity section then decides how much of the lifecycle-adjusted durable removal should be treated as creditable.

| Power case | Lifecycle emissions | Durable after LCA | Creditable after LCA+MRV | Gross for 100 creditable |
| --- | --- | --- | --- | --- |
| 5 kgCO2/MWh | 11.0 Gt/y | 85.2 Gt/y | 66.3 Gt/y | 151 Gt/y |
| 25 kgCO2/MWh | 12.3 Gt/y | 83.9 Gt/y | 65.3 Gt/y | 153 Gt/y |
| 100 kgCO2/MWh | 17.2 Gt/y | 79.1 Gt/y | 61.3 Gt/y | 163 Gt/y |
| 250 kgCO2/MWh | 26.9 Gt/y | 69.5 Gt/y | 53.4 Gt/y | 187 Gt/y |

The generated lifecycle-emissions outputs are `analysis/tables/aether_lifecycle_emissions_assumptions.csv`, `analysis/tables/aether_lifecycle_emissions_by_pathway.csv`, and `analysis/tables/aether_lifecycle_emissions_summary.csv`; the figure is `analysis/figures/lifecycle_emissions_net_credit_sensitivity.png`.

The 25 kgCO2/MWh case is the useful middle warning. Under the current placeholder assumptions, a 100 GtCO2/year gross portfolio creates about 12.3 GtCO2e/year of lifecycle emissions. It yields about 83.9 GtCO2/year after 100-year retention and about 65.3 GtCO2/year after MRV buffers. To credit 100 GtCO2/year at the same pathway mix, gross removal has to rise to about 153 GtCO2/year.

The 100 and 250 kgCO2/MWh cases are not proposed AETHER designs. They are failure boundaries. They show why "cheap energy" is not enough. The energy has to be additional, low-carbon, deliverable, and not simply displaced from other decarbonization uses. If the removal program pulls from a dirty or opportunity-cost-constrained grid, lifecycle emissions eat into the climate result quickly.

This layer also changes the final paper's reporting standard. AETHER should report at least four quantities for every major scenario: gross captured removal, lifecycle emissions, 100-year durable removal after LCA, and creditable removal after LCA plus MRV. Anything less hides the actual climate accounting.

## 5. Cost and Capital

The cost target is not optional. At 100 GtCO2/year, every $10/tCO2 is $1 trillion/year. A cost that sounds acceptable in a carbon-credit market becomes enormous at AETHER scale.

| Cost per tCO2 | Annual cost at 100 GtCO2/year |
|---:|---:|
| $500/tCO2 | $50 trillion/year |
| $100/tCO2 | $10 trillion/year |
| $50/tCO2 | $5 trillion/year |
| $25/tCO2 | $2.5 trillion/year |
| $10/tCO2 | $1 trillion/year |

The scenario model uses three main cost bands:

| Scenario | Assumed annual operating cost | Capacity capex assumption | Total capacity capex for 100 GtCO2/year |
|---|---:|---:|---:|
| Current DAC-like | $525/tCO2 | $1,200 per tCO2/year | $120 trillion |
| Advanced capture and storage | $90/tCO2 | $400 per tCO2/year | $40 trillion |
| Near-thermodynamic capture and storage | $35/tCO2 | $150 per tCO2/year | $15 trillion |

These are scenario assumptions, not forecasts. They illustrate the cost collapse required. If current DAC-like costs remain the norm, 100 GtCO2/year is not economically plausible. If AI, robotics, energy learning curves, materials discovery, modular plant manufacturing, and storage learning push costs toward $10-$50/tCO2, then the annual cost enters the same rough order as global energy, defense, infrastructure, or health spending rather than the entire world economy.

There is also an energy price floor. At $10/MWh electricity, a 1 GJ/tCO2 capture system has an energy cost floor of about $2.78/tCO2; a 3 GJ/tCO2 system has an $8.33/tCO2 floor; an 8 GJ/tCO2 system has a $22.22/tCO2 floor. Full splitting adds about 2,484 kWh/tCO2, or $24.84/tCO2 at $10/MWh before losses. At $30/MWh, those floors triple. This means very low removal costs require both low energy intensity and cheap clean energy. Robotics can lower labor and construction cost, but it cannot erase the energy bill.


### 5.1 Clean-Energy Markets, Texas, Nuclear, and Fusion

AETHER should take market-driven clean energy seriously. The strongest version of the project does not need to assume that every clean-energy deployment must be forced by detailed regulation. IRENA reports that in 2024 new utility-scale onshore wind averaged $0.034/kWh globally, solar PV averaged $0.043/kWh, and 91% of newly commissioned utility-scale renewable capacity delivered power below the cost of the cheapest new fossil alternative [@irena_power_costs_2024]. IEA reports that global electricity generation increased by more than 850 TWh in 2025, solar PV rose by about 600 TWh, and renewables plus nuclear rose by more than total electricity growth while fossil generation declined [@iea_global_energy_review_2026].

That changes the AETHER policy frame. Cheap clean energy can pull itself into the system when markets are allowed to build and connect it. The role of policy is then less about commanding every megawatt and more about making the market honest and functional: interconnection queues, transmission, siting, reliability, emissions pricing, storage, nuclear licensing, and liability.

Texas and California provide descriptive deployment contrasts, not a controlled causal comparison. EIA reports that Texas led the United States in wind electricity generation in 2024, accounting for about 28% of U.S. wind generation, and was the second-largest solar producer after California [@eia_texas_energy_profile_2024]. The California Energy Commission reports that clean resources accounted for 62% of the state's total system power mix in 2024 [@california_energy_commission_2024_tseg]. These facts show that different market, policy, resource, and grid contexts can all produce substantial clean-energy deployment. They do not, by themselves, establish which state has lower administrative or permitting cost. AETHER should treat interconnection, transmission, siting, reliability, and additionality as measurable regional inputs rather than infer them from two state-level outcomes.

The bottlenecks are not theoretical. Berkeley Lab's `Queued Up: 2025 Edition` documents very large U.S. interconnection queues for generation and storage projects, dominated by solar, storage, and wind [@berkeley_lab_queued_up_2025]. A clean project stuck in an interconnection queue is not usable energy for carbon removal. AETHER therefore needs grid reform as much as it needs better capture chemistry.

Firm clean power is the second market signal. Data centers are already pulling nuclear and advanced firm-power technologies forward. Microsoft and Constellation announced a 20-year agreement to restart TMI Unit 1 as the Crane Clean Energy Center, adding about 835 MW of carbon-free power to the grid [@microsoft_constellation_crane_2024]. Google and Kairos Power announced an agreement for up to 500 MW of advanced nuclear by 2035, with first deployment targeted by 2030 [@google_kairos_2024]. Helion announced a Microsoft fusion PPA targeting at least 50 MW and electricity by 2028, and the Fusion Industry Association reported $2.64B in fusion investment over the prior year [@helion_microsoft_fusion_2023; @fusion_industry_association_2025]. These are not enough to power AETHER by themselves. They are measured in megawatts to low gigawatts while AETHER needs terawatts. But they matter because data-center buyers can create early demand for clean firm power, modular construction, licensing pathways, and financing models that carbon-removal infrastructure can later use.

Data-center growth also competes with AETHER. IEA projects data-centre electricity consumption roughly doubling to about 945-950 TWh by 2030, with renewables as the fastest-growing supply source and nuclear becoming more significant after 2030 in the United States [@iea_energy_ai_2025]. This is small relative to an 83,333 TWh/year advanced AETHER system, but it is large enough to shape near-term power markets, grid queues, nuclear restarts, and firm-power procurement.

The clean-energy buildout sensitivity model starts with the IEA 2025 global electricity-growth increment of 850 TWh/year and asks how much new annual clean generation could be added over 20 years if annual additions keep growing. For the advanced 3 GJ/tCO2 AETHER case, 100 GtCO2/year requires 83,333 TWh/year. If clean-generation additions stayed flat at 850 TWh/year, the world would add only 17,000 TWh/year of new annual generation over 20 years, enough for about 20% of that AETHER energy demand before ordinary demand. At 10% annual growth in clean-generation additions, the cumulative addition reaches about 48,684 TWh/year, or 58% of the advanced AETHER requirement. At 15% annual growth, it reaches about 87,077 TWh/year, enough on paper for the 3 GJ/tCO2 case before other demand consumes the supply.

| Annual growth in clean-generation additions | New annual clean generation after 20 years | Coverage of 3 GJ/tCO2 AETHER energy demand before other demand |
|---:|---:|---:|
| 0% | 17,000 TWh/year | 20% |
| 5% | 28,106 TWh/year | 34% |
| 10% | 48,684 TWh/year | 58% |
| 15% | 87,077 TWh/year | 104% |
| 20% | 158,685 TWh/year | 190% |

This table is optimistic because it assigns the entire clean-energy increment to AETHER. In reality, electrification, AI data centers, industry, desalination, synthetic fuels, and replacement of fossil generation all compete for clean power. The conclusion is still useful: AETHER becomes energy-plausible only if clean-energy additions keep compounding from today's already large base and if AETHER can colocate with cheap clean power, storage, firm generation, and durable storage geology.
### 5.1.1 Clean-Power Additionality and Competing Demand

The clean-energy market argument is necessary but incomplete. Falling renewable costs and market-led deployment make AETHER more plausible, but generic clean-energy growth cannot be counted as AETHER supply. The removal system needs power that is delivered through interconnection and transmission, available after competing loads, low-carbon on the margin, and additional rather than displaced from other decarbonization uses.

The v0.28 additionality screen treats current clean-energy growth as the starting point, then filters it through delivery, AETHER allocation, and true additionality. The source anchors are deliberately mixed: IRENA for cost decline and competitiveness [@irena_power_costs_2024], IEA for recent electricity growth and data-center demand [@iea_global_energy_review_2026; @iea_energy_ai_2025], Berkeley Lab for interconnection queues [@berkeley_lab_queued_up_2025], Texas and California for market-led versus policy-heavy clean-energy comparison [@eia_texas_energy_profile_2024; @california_energy_commission_2024_tseg], and nuclear/fusion/data-center announcements as market-pull signals rather than base-case proof [@microsoft_constellation_crane_2024; @google_kairos_2024; @helion_microsoft_fusion_2023; @fusion_industry_association_2025].

| Scenario | Added clean generation | Additional AETHER power | Share of target | Result |
| --- | --- | --- | --- | --- |
| Status quo friction | 38,898 TWh/y | 2,995 TWh/y | 3% | fails |
| Market-unlocked buildout | 87,077 TWh/y | 19,429 TWh/y | 21% | fails |
| Dedicated AETHER buildout | 158,685 TWh/y | 68,552 TWh/y | 75% | fails |
| Abundance clean-power push | 202,291 TWh/y | 122,512 TWh/y | 134% | passes |
| Nonadditional grid pull | 87,077 TWh/y | 6,857 TWh/y | 7% | fails |

The generated clean-power additionality outputs are `analysis/tables/aether_clean_energy_additionality_cases.csv`, `analysis/tables/aether_clean_energy_market_pull_comparators.csv`, `analysis/tables/aether_clean_energy_policy_friction_matrix.csv`, and `analysis/tables/aether_clean_energy_additionality_summary.csv`; the figure is `analysis/figures/clean_energy_additionality_gate.png`.

The market-unlocked case is a useful warning. It assumes clean-energy additions grow 15% annually from a high 2025 base, delivery improves to 75%, and AETHER claims 35% of delivered clean growth after competing uses. Even then, the true additional AETHER supply is only about 19,429 TWh/year, or 21% of the 3 GJ/tCO2 balanced power gate. The dedicated AETHER case reaches about 75% of the gate. The upper-tail abundance clean-power push is the only case in this screen that passes, and it requires growth, delivery, allocation, and additionality to all stay favorable for two decades.

This is the right discipline for the paper. Texas-style market energy abundance matters because it shows that clean energy can scale when economics, resource quality, and grid access line up. California-style policy pressure matters because it shows clean shares can be pushed high when public institutions keep forcing the issue. Data centers matter because they are already financing clean firm-power deals. But AETHER cannot simply borrow those facts and declare victory. It needs a separate power accounting rule: every modeled tonne should report whether the electricity is additional, deliverable, low-carbon on the margin, and not stolen from ordinary decarbonization.

The nonadditional-grid case makes the failure mode explicit. With the same nominal clean-energy expansion as the market-unlocked case but only 30% additionality, AETHER receives about 7% of the required additional clean power. That scenario should not be reported as climate reversal. It is an energy-accounting failure.

### 5.1.2 P0 Clean-Power Deliverability Gate

The current repo turns clean power into an explicit P0 falsification gate. The question is not whether solar, wind, nuclear, geothermal, storage, and possibly fusion keep improving. The question is whether AETHER can obtain delivered additional low-carbon industrial power after ordinary electrification, data-center demand, fossil replacement, interconnection queues, transmission, siting, hourly matching, firming, and additionality are all counted. This is where the Texas and California comparison matters. Market-led clean-energy growth is real, but a cheap megawatt-hour on a spreadsheet is not the same thing as power delivered to a removal plant with creditable additionality [@irena_power_costs_2024; @eia_texas_energy_profile_2024; @california_energy_commission_2024_tseg; @berkeley_lab_queued_up_2025].

The model starts from the current AETHER balanced gate: 100 GtCO2/year at 3 GJ/tCO2 requires about 91,667 TWh/year after applying a 10% gross-generation adder for delivery and firming. This is an adder to delivered demand, not a 10% loss fraction. It then tests six cases. Each case compounds annual clean-generation additions over 20 years, subtracts ordinary demand claims, and applies explicit factors for AETHER dedication, additionality, interconnection, transmission/siting, hourly matching, and firm clean supply. IEA clean-generation growth, IEA Energy and AI, IRENA costs, Berkeley Lab queues, NREL ATB, IEA Electricity, nuclear/geothermal sources, and company firm-power announcements are used as anchors or market-pull signals, not as proof that the 100 Gt gate is solved [@iea_global_energy_review_2026; @iea_energy_ai_2025; @nrel_atb_2024_electricity; @iea_electricity_2026; @iaea_nuclear_status_2025; @iea_geothermal_future_2024; @google_kairos_2024; @microsoft_constellation_crane_2024; @helion_microsoft_fusion_2023].

![AETHER clean-power deliverability gate](../../analysis/figures/clean_power_deliverability_gate.png)
![AETHER regional clean-power dispatch gate](../../analysis/figures/regional_power_dispatch_gate.png)

| Case | Delivered additional clean TWh/y | Powered scale at 3 GJ/tCO2 | Passes 100 Gt/y |
| --- | --- | --- | --- |
| Status quo friction | 294 | 0.3 | False |
| Market unlocked | 5,858 | 6.4 | False |
| Dedicated AETHER corridors | 41,185 | 44.9 | False |
| Firm clean backbone | 41,002 | 44.7 | False |
| Upper-tail AI energy abundance | 124,305 | 135.6 | True |
| Nonadditional grid failure | 244 | 0.3 | False |

The result is sharper than the earlier annual clean-energy buildout screen. The market-unlocked case powers about 6.4 GtCO2/year at the 3 GJ/tCO2 gate. Dedicated AETHER corridors power about 44.9 GtCO2/year, and a firm clean-power backbone powers about 44.7 GtCO2/year. Only the upper-tail AI energy-abundance case clears the full target, at about 135.6 GtCO2/year. The nonadditional-grid failure case powers only about 0.3 GtCO2/year. In this screen, 1 of 6 cases pass the 100 GtCO2/year power gate and 1 of 6 pass the 50 GtCO2/year gate.

The generated deliverability outputs are `analysis/tables/aether_clean_power_deliverability_cases.csv`, `analysis/tables/aether_clean_power_deliverability_scale_targets.csv`, `analysis/tables/aether_clean_power_deliverability_constraints.csv`, and `analysis/tables/aether_clean_power_deliverability_summary.csv`.

This should be read as a falsification screen, not as a dispatch model. If regional hourly modeling cannot deliver additional low-carbon power at the required scale, AETHER does not get to keep the 100 GtCO2/year headline just because clean energy is cheap in general. The correct response would be to cap feasible removal by delivered clean power, push harder on dedicated firm clean-energy infrastructure, or slow the deployment time path.

### 5.1.3 Regional Clean-Power Dispatch and Colocation Screen

The v0.36 repo adds a first regional dispatch and colocation screen. This is the next filter after the v0.35 clean-power deliverability gate. Annual TWh is still too weak as evidence. A removal plant needs power at the right place, at the right hours, with storage or firm supply, with credible additionality, and with enough co-location value that energy, storage geology, water, heat, transmission, and public consent fit together.

The model uses 7 regional archetypes and a representative 24-hour dispatch day. Each case assigns clean power to regions, subtracts ordinary demand, applies delivery and additionality constraints, then serves a flat AETHER industrial load with regional solar, wind, firm clean power, and storage. The region names are archetypes, not final siting recommendations. Texas/Gulf, California/West, interior wind/geothermal, North Africa/Middle East solar, Australia/Pacific mineral corridors, North Sea/Europe wind, and South America hydro/biomass appear because they make different tradeoffs visible: market-led renewables, storage corridors, firm power, transmission, water/heat limits, and mineral or geologic co-location [@irena_power_costs_2024; @eia_texas_energy_profile_2024; @california_energy_commission_2024_tseg; @berkeley_lab_queued_up_2025; @nrel_atb_2024_electricity; @iea_electricity_2026; @iaea_nuclear_status_2025; @iea_geothermal_future_2024].

![AETHER regional clean-power dispatch gate](../../analysis/figures/regional_power_dispatch_gate.png)

| Case | Target Gt/y | Supported Gt/y | Hourly match | Passes 100 Gt/y |
| --- | --- | --- | --- | --- |
| Market regional reference | 35 | 15.5 | 44% | False |
| Dedicated AETHER corridors | 70 | 47.9 | 68% | False |
| Firm colocated backbone | 85 | 64.3 | 76% | False |
| Upper-tail AI energy abundance | 125 | 122.0 | 98% | True |
| Nonadditional fragmented grid | 50 | 10.2 | 20% | False |

The result is stricter than a clean-energy growth story. The market regional reference supports about 15.5 GtCO2/year. Dedicated AETHER corridors support about 47.9 GtCO2/year. A firm colocated backbone supports about 64.3 GtCO2/year. Only the upper-tail AI energy-abundance dispatch case clears the 100 GtCO2/year screen, supporting about 122.0 GtCO2/year. In this screen, 1 of 5 cases clear 100 GtCO2/year and 2 clear 50 GtCO2/year.

The generated outputs are `analysis/tables/aether_regional_power_region_assumptions.csv`, `analysis/tables/aether_regional_power_dispatch_cases.csv`, `analysis/tables/aether_regional_power_dispatch_by_region.csv`, `analysis/tables/aether_regional_power_hourly_sample.csv`, `analysis/tables/aether_regional_power_colocation_scorecard.csv`, and `analysis/tables/aether_regional_power_dispatch_summary.csv`.

This is still a screen, not an 8760-hour grid model. The next version should replace the synthetic day with real regional resource traces, load shapes, interconnection queues, transmission corridors, storage-duration costs, marginal emissions, industrial heat options, water constraints, and pathway-specific co-location rules. The paper should keep the conclusion narrow: cheap clean energy is favorable for markets, but AETHER only counts power that is delivered, additional, low-carbon, and usable by high-uptime removal infrastructure.

### 5.2 Learning Curves and Economies of Scale

AETHER's optimistic case depends on learning curves and economies of scale. Wright's learning-curve work showed that aircraft production labor fell with cumulative output, and later research stresses that cost reductions can reflect both learning-by-doing and ordinary scale effects rather than a single mechanism [@wright_1936_learning_curve; @thompson_2012_learning_by_doing]. AETHER should model both.

The transition model uses current novel CDR, about 0.00204 GtCO2/year, as the starting point for engineered-removal scale. Moving from there to 100 GtCO2/year requires about 15.6 capacity doublings. If initial engineered-removal cost is $500/tCO2, the raw learning result is highly sensitive to learning rate:

| Learning rate per doubling | Raw learned cost at 100 GtCO2/year | Bounded cost with 3 GJ/tCO2 capture, $10/MWh power, and storage/MRV floor | Annual cost at 100 GtCO2/year |
|---:|---:|---:|---:|
| 10% | $96.83/tCO2 | $96.83/tCO2 | $9.68T/year |
| 15% | $39.74/tCO2 | $39.74/tCO2 | $3.97T/year |
| 20% | $15.45/tCO2 | $20.33/tCO2 | $2.03T/year |
| 25% | $5.65/tCO2 | $20.33/tCO2 | $2.03T/year |
| 30% | $1.93/tCO2 | $20.33/tCO2 | $2.03T/year |

The floor is important. Once manufacturing learning pushes equipment cost below the combined energy, storage, and MRV floor, additional learning does not lower total cost unless energy intensity, power price, storage, or monitoring also improve. This is one reason AETHER should not copy software-style cost expectations into the physical economy. Learning curves matter, but thermodynamics and infrastructure floors eventually dominate.

Plant-level economies of scale also help, but they have limits. At 100 GtCO2/year, a 1 MtCO2/year plant equivalent means 100,000 plants; a 10 MtCO2/year hub means 10,000 hubs; a 25 MtCO2/year hub means 4,000 hubs; and a 100 MtCO2/year mega-hub still means 1,000 hubs. Larger hubs can lower unit capex if capex scales sublinearly with plant size, but they also concentrate land, air-contact, transmission, storage, pipeline, water, safety, and permitting constraints. AETHER's deployment architecture should therefore be neither tiny modular units everywhere nor a few mega-sites. It should be a regional portfolio matched to energy and storage geology.

### 5.3 Jevons Paradox, Rebound, and Induced Emissions

Jevons paradox is the warning that efficiency improvements can increase total resource use when they lower effective cost and expand demand. The rebound literature is contested on how often full backfire occurs, but the warning is central for AETHER [@sorrell_2009_jevons_rebound; @alcott_2005_jevons_paradox]. Cheap removal could make additional carbon-intensive production economically attractive. That is not automatically undesirable: some industrial processes create substantial public value. It does mean that removal capacity and permitted atmospheric use have to share one measured budget. Otherwise new demand can outrun the cleanup capacity that made it attractive.

The transition model treats rebound as induced emissions or delayed abatement equal to a fraction of gross removal. Under simple gross accounting, 100 GtCO2/year minus the 42.2 GtCO2/year current-emissions baseline leaves 57.8 GtCO2/year of headroom, so the gross break-even threshold is 57.8% of gross removal. That number is not the general governance threshold. In the 25 kgCO2/MWh lifecycle case, 100 Gt gross becomes 83.916 Gt durable after LCA, leaving 41.716 Gt of rebound headroom, or 41.7% of gross. After the same case's provisional MRV buffers, 65.270 Gt is creditable, leaving only 23.070 Gt, or 23.1% of gross. Above the threshold for the accounting layer being claimed, AETHER becomes net-positive despite enormous cleanup capacity.

| Accounting layer before rebound | Removal before rebound | Break-even rebound headroom | Break-even rebound as share of 100 Gt gross |
|---|---:|---:|---:|
| Simple gross arithmetic | 100.000 Gt/y | 57.800 Gt/y | 57.8% |
| Durable after LCA, 25 kgCO2/MWh case | 83.916 Gt/y | 41.716 Gt/y | 41.7% |
| Creditable after LCA+MRV, 25 kgCO2/MWh case | 65.270 Gt/y | 23.070 Gt/y | 23.1% |

The original rebound sensitivity table below remains useful as a simple gross-accounting screen. It should not be cited as a lifecycle- or credit-adjusted threshold.

| Rebound or delayed-abatement fraction | Net removal | Simple ppm-equivalent change |
|---:|---:|---:|
| 0% | 57.8 GtCO2/year | 7.41 ppm/year drawdown |
| 10% | 47.8 GtCO2/year | 6.13 ppm/year drawdown |
| 25% | 32.8 GtCO2/year | 4.21 ppm/year drawdown |
| 50% | 7.8 GtCO2/year | 1.00 ppm/year drawdown |
| 57.8% | 0.0 GtCO2/year | break-even |
| 75% | -17.2 GtCO2/year | 2.21 ppm/year accumulation |

This is why AETHER's institutional design is not decorative. Cheap removal changes the economically useful quantity of emissions, so the system needs an atmospheric operating band, a measured net-use budget, sink-use charges, durable-removal procurement, liability, and restrictions on outputs whose local or systemic harms cannot be solved by payment.

## 6. Robotics and AI Acceleration

AETHER's robotics premise is often easy to state badly. The weak version says cheap humanoids will exist, so the project becomes easy. The serious version asks which physical bottlenecks robots can actually move: lab throughput, module manufacturing, construction, drilling, field maintenance, MRV, logistics, and sensor deployment.

The current source-backed anchors are still limited. IFR reports 542,076 industrial robot installations in 2024 and an operational stock of 4,663,698 industrial robots [@ifr_world_robotics_2025]. Amazon reports more than 750,000 deployed mobile robots in its operations network [@amazon_robotics_750k_robots_2024]. Unitree lists a low humanoid price floor, while Figure and Agility have announced humanoid factory-capacity and production-ramp claims [@unitree_g1_product_2026; @figure_botq_2025; @figure_ramping_2026; @agility_robofab_2023]. These are useful signals, but they do not prove field productivity in AETHER conditions.

The robotics productivity model therefore changes the variable. Instead of treating robot count as the main claim, it estimates useful autonomous task-hours by task family, then maps those hours to robot classes with unit cost, useful hours per year, lifetime, maintenance, energy use, supervision ratio, and integration overhead.

![AETHER robotics productivity capacity stack](../../analysis/figures/robotics_productivity_capacity_stack.png)

The high robot-intensity case is the cautionary case. It requires about 1.49 million robots/year in buildout plus replacement flow if the current productivity screen is translated into annual production. The AETHER automation-push case lowers that annual flow to about 233,800 robots/year by moving work into designed environments and increasing useful hours per robot-year. The deep modular abundance case is much smaller, but it is also the least evidenced: it assumes the physical system itself has been redesigned for robots.

### 6.1 Robotics Field Productivity Distribution Stress Test

The v0.38 repo adds a field-productivity distribution screen because robot production count is still too crude. AETHER needs useful autonomous task-hours under real operating conditions. The model discounts the existing task-hour screen by field uptime, autonomy success, task-fit or environment-design suitability, maintenance drag, and safety/supervision drag.

![AETHER robotics field productivity distribution gate](../../analysis/figures/robotics_field_productivity_distribution_gate.png)

| Scenario | P10 production, robots/y | P50 production, robots/y | P90 production, robots/y | P50 stock, M | IFR-count pass share |
| --- | --- | --- | --- | --- | --- |
| High robot intensity | 10,933,533 | 13,220,956 | 16,522,244 | 61.02 | 0% |
| AETHER automation push | 746,069 | 840,142 | 948,342 | 4.53 | 0% |
| Deep modular abundance | 108,497 | 116,483 | 126,009 | 0.70 | 100% |

The automation-push case is the critical middle case. Before field-productivity penalties, it requires about 233,800 robots/year. After the distribution stress test, the median requirement is about 840,142 robots/year, with a P10-P90 range of 746,069 to 948,342. That is about 1.55x current annual industrial robot installations at the median. This does not kill the robotics premise, but it changes what must be proven. The paper needs task-family productivity distributions, not just robot unit costs or factory cadence.

The high robot-intensity case becomes a warning label: median annual production rises to about 13,220,956 robots/year. The deep modular abundance case remains much easier on count, at about 116,483 robots/year median, but it depends on climate-infrastructure work being redesigned around robot-native factories, controlled logistics, automated construction, and dense MRV sensor networks.

The generated outputs are `analysis/tables/aether_robotics_field_productivity_distribution_assumptions.csv`, `analysis/tables/aether_robotics_field_productivity_distribution_samples.csv`, `analysis/tables/aether_robotics_field_productivity_distribution_summary.csv`, `analysis/tables/aether_robotics_field_productivity_bottlenecks.csv`, `analysis/tables/aether_robotics_field_productivity_summary_metrics.csv`, and `analysis/figures/robotics_field_productivity_distribution_gate.png`.

### 6.2 Robotics Production Verification and Scale Credibility Gate

The v0.37 repo added a production verification gate so robotics claims do not outrun their source quality. A production-rate statement is not the same thing as an audited deployment statistic, and neither is the same thing as AETHER-grade field productivity. The model compares independent industrial robotics statistics, company-primary humanoid and warehouse-robot claims, and unresolved social-media leads against the annual robot production flows implied by the AETHER productivity screen.

Figure's official pages are now more useful than the X leads. Figure's BotQ announcement states that its first-generation line would be capable of up to 12,000 humanoids/year, and its 2026 ramping page reports over 350 Figure 03 robots delivered, one robot per hour cycle time, over 80% end-of-line first-pass yield, 99.3% battery-line first-pass yield, and more than 9,000 actuators produced [@figure_botq_2025; @figure_ramping_2026]. These are company-primary claims, not independent audits. Noah's 250-robots-in-one-month X lead remains in the source register as an unresolved lead and should not be written as a paper fact unless archived or independently corroborated.

![AETHER robotics production verification gate](../../analysis/figures/robotics_production_verification_gate.png)

| Scenario | Annual robot production need | Multiple of 2024 IFR installs | Figure BotQ-equivalent lines |
| --- | --- | --- | --- |
| High robot-intensity translation | 1,492,147 | 2.75 | 124.3 |
| AETHER automation push | 233,800 | 0.43 | 19.5 |
| Deep modular abundance | 53,251 | 0.10 | 4.4 |

The count result is sharper than the previous prose. The high robot-intensity case needs about 1,492,147 robots/year, or 2.75x current annual industrial robot installations and 124.3 Figure BotQ first-generation line equivalents. The AETHER automation-push case needs about 233,800 robots/year, below current IFR installations on a count basis but still about 19.5 BotQ-equivalent lines. The deep modular abundance case needs about 53,251 robots/year and is easiest on production count, but it assumes the strongest infrastructure redesign.

This does not prove the robotics premise. It keeps it honest. AETHER does not need the whole world to wait for humanoids if specialized factory, logistics, construction, drilling, inspection, and MRV systems do most of the work. But every robotics-positive scenario must eventually prove useful autonomous task-hours, not just purchase price, production cadence, or a fleet-size press release. The generated outputs are `analysis/tables/aether_robotics_production_claims.csv`, `analysis/tables/aether_robotics_production_scale_comparison.csv`, `analysis/tables/aether_robotics_production_ramp_paths.csv`, `analysis/tables/aether_robotics_production_verification_summary.csv`, and `analysis/figures/robotics_production_verification_gate.png`.

<!-- AETHER-PUBLIC-RELEASE:paper-scenarios:BEGIN -->
### 6.3 External AI Scenario Benchmarks

AETHER's abundance premise is not sourced from any single AI forecast. Three public scenario projects instead define contrasting timing and governance branches.

| Source | Status | Capability timing and acceleration | Physical-world boundary | AETHER use rule |
|---|---|---|---|---|
| Situational Awareness | Argumentative capability and mobilization forecast | AGI around 2027 and superintelligence by the end of the 2020s through compute, algorithmic efficiency, unhobbling, and automated AI research. | AI research can accelerate virtually before robotics; compute and electrical power remain binding. | Use as a fast-capability stress branch, not as a physical-productivity parameter. |
| AI 2027 | Forecast scenario and best guess at publication | Expert-human AI and automated AI R&D in 2027, followed by rapid recursive acceleration. | The authors emphasize timing uncertainty, especially beyond the near-term part of the scenario; software acceleration does not establish robot field throughput. | Use as a short-timeline branch while independently gating power, robots, storage, and governance. |
| AI 2040: Plan A | Normative scenario and policy recommendation with forecast assumptions | Default AI R&D automation in 2030, governed scaling to top-human-expert systems, and superintelligence delayed until 2040. | Physical labor follows cognitive labor and requires robots, automated supply chains, energy, and infrastructure. | Use as a governance-bounded abundance branch, not empirical validation. |
| AETHER | Conditional engineering feasibility screen | A 2046 test premise combining AI scientists, robotic physical labor, dedicated clean energy, durable storage, and measurement. | Power, contactors, materials, storage, MRV, capital, and rebound remain explicit gates. | Treat the external scenarios as timing and coordination branches only. |

Situational Awareness is useful to AETHER precisely because it does not require robotics for its initial AI R&D acceleration and separately identifies industrial power as a constraint [@aschenbrenner_2024_situational_awareness]. AI 2027 provides the fastest detailed branch, but its scenario structure and stated timing uncertainty prevent its use as measured evidence for construction or operations [@kokotajlo_et_al_2025_ai_2027]. AI 2040: Plan A supplies a slower, governance-bounded branch and explicitly places physical abundance downstream of supply-chain-complete automation [@larsen_et_al_2026_ai_2040].

These scenarios widen the plausible timing and governance envelope. They do not source AETHER's engineering parameters. Capture energy, clean-power deliverability, field robot productivity, materials, storage, lifecycle emissions, MRV, and rebound remain independently evidenced or explicitly assumed.
<!-- AETHER-PUBLIC-RELEASE:paper-scenarios:END -->

## 7. What a Reference AETHER Stress-Test System Looks Like

The optimized system is unlikely to be one technology. It is a portfolio with strict accounting.

First, the reference system manages a carbon budget rather than treating all CO2 output as equivalent misconduct. Every emitted tonne creates a physical removal, transport, storage, and verification burden. An industrial process may justify that burden when its social value exceeds the full system cost, but its net atmospheric use still has to be measured and paid for.

Second, the default durable storage pathway should be geologic storage, in situ mineralization, and other low-energy durable storage where geology and social license allow it. Full CO2 splitting should be reserved for cases where solid carbon is worth the added energy burden.

Third, clean energy must be purpose-built and additional. A 100 GtCO2/year system powered by fossil electricity would fail its own purpose. The system needs dedicated clean generation, storage, transmission, heat management, and demand flexibility. Some locations may combine cheap renewables, nuclear, geothermal, waste heat, high-quality storage formations, and access to water or reactive minerals.

Fourth, plant design should favor modular manufacturing and maintainability. A 1 MtCO2/year plant equivalent implies 100,000 plants for 100 GtCO2/year. A 10 MtCO2/year hub implies 10,000 hubs. A 25 MtCO2/year hub implies 4,000 hubs. A 100 MtCO2/year mega-hub implies 1,000 hubs. The likely architecture is not one global machine; it is many regional systems matched to energy, storage, air, water, labor, and community constraints.

Fifth, MRV has to be adversarial. At 100 GtCO2/year, a 1% accounting error is 1 GtCO2/year. That is larger than almost all current novel CDR by several orders of magnitude. Measurement has to include physical monitoring, third-party audits, leakage liability, atmospheric checks, lifecycle energy accounting, and penalties large enough to prevent fake tonnes.

Sixth, governance must treat atmospheric capacity as a finite public service. That is where the public-carbon-utility model belongs.

## 8. Public Carbon Utility and Atmospheric Service Pricing

AETHER proposes a governance path in which the atmosphere's carbon-absorbing capacity is administered as a public service. This is an institutional hypothesis, not a statement of current property law. Citizens, future citizens, and affected communities would hold the relevant interest through a public trust, statutory utility, or comparable commons institution. The operator would set a science-informed atmospheric operating band, authorize a net carbon budget, meter additions and durable removals, charge for permitted net use, and procure the infrastructure needed to maintain the balance.

The public trust doctrine provides one legal analogy in which certain natural resources are preserved for public use, with government acting as trustee [@cornell_public_trust_doctrine]. Atmospheric trust arguments extend that logic to climate and air systems, although the doctrine remains contested and uneven across jurisdictions [@georgetown_atmospheric_trust_2023]. Ostrom's commons work also shows that unmanaged access and private ownership are not the only choices; common-pool resources can sometimes be governed through rules, monitoring, sanctions, and nested institutions [@ostrom_governing_commons_1990]. These precedents do not establish AETHER's legal model. They make it a concrete institutional research question.

The proposed annual account for actor *i* begins with a physical balance:

`net atmospheric use_i = verified CO2 additions_i - retired verified durable removals_i`

For positive net use, a conceptual charge is:

`annual charge_i = net atmospheric use_i × (marginal removal cost + storage/MRV/liability cost + scarcity-and-risk premium)`

This is a design equation, not an estimated tariff. Each term requires legislation, measurement rules, distributional analysis, and empirical cost data. The scarcity-and-risk premium should rise as the atmospheric operating band tightens or as removal and storage capacity become constrained. A negative balance should not automatically create a tradable credit; payment for removal should depend on public procurement rules, additionality, durability, lifecycle emissions, and independent verification.

The operating model has six parts:

- The public operator sets an atmospheric operating band and a permitted net carbon budget rather than an unrestricted right to emit.
- Covered additions and removals are measured by source, pathway, location, durability, and lifecycle effect. Unmeasured tonnes cannot be reconciled away.
- Useful industrial activity can continue inside the budget when its value justifies the full atmospheric-service charge and its local harms satisfy separate law.
- Revenues fund removal, transport, durable storage, MRV, maintenance, liability reserves, affected communities, and—if democratically chosen—citizen dividends.
- Removal providers are paid for net, additional, durable, independently verified tonnes, not nominal capture or avoided emissions relabeled as removal.
- Prices, permissions, and procurement volumes adjust as atmospheric measurements, storage performance, system costs, and public targets change.

This model does not make every output acceptable. Toxic co-pollutants, acute local harms, ecological damage, and other high-risk releases remain subject to prohibitions, performance standards, and liability rather than a carbon fee alone. Carbon pricing cannot substitute for those protections.

The principal failure mode is an underpriced budget that legitimizes more net loading than the physical system can reverse. Other risks include captured regulators, weak measurement, unequal local burdens, governments becoming dependent on use revenue, volatile prices, removal-provider fraud, and cross-border leakage. The institutional model is therefore part of AETHER's feasibility claim, but its legal form, incidence, international coordination, and distributional effects remain open research gates.

## 9. Integrated Feasibility Frontier

The separate models are useful, but AETHER ultimately fails or succeeds as an integrated industrial system. A pathway portfolio can look plausible on paper while the clean-energy buildout is too small. A robot-production curve can look impressive while storage permitting and injection capacity arrive too slowly. A low cost per tonne can still be useless if cheap removal induces enough new emissions or delayed abatement to erase net-negative benefit.

The current repo therefore adds an integrated feasibility screen. It is deliberately simple: for each 2026-2046 scenario, actual removal capacity is the minimum of five constraints: the planned linear path to 100 GtCO2/year, clean electricity available to AETHER, robot supply in service, storage capacity, and annual budget capacity at the learned cost per tonne. The model then subtracts remaining emissions and rebound. This is not a forecast. It is a constraint audit.

| Scenario | Screen result | 2046 capacity | Energy ratio | Robot ratio | Storage ratio | Budget ratio | Net at 100 Gt/y |
|---|---|---:|---:|---:|---:|---:|---:|
| Reference extrapolation | fails or offset-only | 3.1 Gt/y | 0.03x | 0.10x | 0.25x | 0.11x | 17.0 Gt/y |
| Fast learning, energy constrained | fails or offset-only | 19.6 Gt/y | 0.20x | 1.79x | 0.60x | 0.44x | 50.0 Gt/y |
| AETHER portfolio push | passes 100 Gt/y screen | 100.0 Gt/y | 1.16x | 13.70x | 1.05x | 1.07x | 70.0 Gt/y |
| Moonshot low-energy | passes 100 Gt/y screen | 100.0 Gt/y | 1.97x | 54.84x | 1.20x | 1.71x | 90.0 Gt/y |
| High-rebound failure | near miss / rebound failure | 100.0 Gt/y | 1.16x | 13.70x | 1.05x | 1.07x | 5.0 Gt/y |

The reference extrapolation fails for the expected reason: moderate learning and moderate automation do not create enough energy, robots, storage, or budget headroom. The fast-learning case still fails because clean electricity and storage do not scale fast enough. The AETHER portfolio push is the first scenario that passes the 100 GtCO2/year screen, but it requires several strong assumptions to be true at once: the v0.5 pathway portfolio energy intensity near 2.03 GJ/tCO2, about 56,500 TWh/year of AETHER-dedicated clean generation by 2046, storage capacity around 105 GtCO2/year, robot supply sufficient for roughly 50 robots per MtCO2/year of capacity, annual spending near $9T, emissions down to 15 GtCO2/year, and rebound held to 15%. The moonshot low-energy case passes with more headroom because energy intensity falls to 1.35 GJ/tCO2 and the cost floor falls to $35/tCO2.

The high-rebound scenario is the warning case. The physical buildout can mostly work while the atmospheric balance fails. If cheap removal induces more net use than the verified system can offset, AETHER becomes a large settlement mechanism without achieving drawdown. That is why demand response, atmospheric-service pricing, liability, and public governance belong in the technical paper rather than in a later ethics appendix.

The integrated screen changes the plausibility claim. AETHER is not made plausible by any single breakthrough. It is plausible only under coordinated abundance: low-energy capture, clean power, durable storage, automated construction, high-quality MRV, a bounded net atmospheric load, and governance that keeps system use inside verified capacity.
### 9.1 Deployment Timepath and Cumulative Removal

The endpoint screen is not enough. AETHER could look plausible in a table at 100 GtCO2/year and still fail as a climate intervention if it arrives too late, accumulates too little durable credit, or induces net atmospheric use faster than verified capacity grows. The deployment-timepath layer therefore tracks annual gross capacity, durable credited removal, cumulative durable credit, residual emissions, rebound or delayed abatement, annual energy, and annual cost from 2026 through 2060.

The current model evaluates five explicit scenarios: a linear 2046 reference, an S-curve industrialization case, an abundance-acceleration case that reaches scale by 2040, an energy-delayed case, and a rebound-failure case. These are not forecasts. They are stress tests for the claim that AI and robotics can make climate reversal an industrial buildout problem.

| Scenario | Gross removal in 2046 | Durable credit in 2046 | Net after emissions and rebound in 2046 | Cumulative durable credit by 2060 | Main read |
|---|---:|---:|---:|---:|---|
| Linear 2046 reference | 66.7 Gt/y | 56.6 Gt/y | 31.6 Gt/y | 1,527 Gt | Clears gross scale, but durable credit and cumulative timing remain the real climate quantities. |
| Abundance acceleration 2040 | 100.0 Gt/y | 90.0 Gt/y | 78.0 Gt/y | 2,017 Gt | Shows the upside if automation, clean energy, storage, and costs compound together earlier. |
| Energy-delayed buildout | 18.3 Gt/y | 15.5 Gt/y | -5.2 Gt/y | 638 Gt | Demonstrates that robotics optimism does not compensate for late clean power. |
| Rebound failure | 99.7 Gt/y | 85.8 Gt/y | -2.1 Gt/y | 1,742 Gt | Builds hardware while losing much of the climate value to emissions behavior. |

The deployment figure and tables live in 'analysis/figures/deployment_timepath_capacity_and_cumulative.png', 'analysis/tables/aether_deployment_timepath_annual.csv', 'analysis/tables/aether_deployment_timepath_summary.csv', and 'analysis/tables/aether_deployment_gate_crossings.csv'.

The main implication is uncomfortable but useful: AETHER has to be judged on cumulative durable net removal, not just on terminal gross capacity. A late 100 GtCO2/year system is different from an early one. A gross 100 GtCO2/year system is different from a durable credited 100 GtCO2/year system. A physically successful system with high rebound is not climate reversal.

## 10. Uncertainty and Sensitivity Screen

The deterministic scenarios above are useful, but they can make AETHER look cleaner than it is. A single scenario either passes or fails. Real deployment would not be that crisp. Energy intensity, clean-energy growth, robot manufacturing, storage throughput, cost, lifecycle durability, residual emissions, rebound, and execution quality would all move at once. Some of those variables would be correlated. Some would improve because of the same AI/robotics acceleration. Others would fail together because of permitting, supply-chain, political, or public-legitimacy constraints.

The v0.8 repo therefore adds a Monte Carlo screen with 20,000 draws across explicit triangular assumption ranges. Each draw calculates AETHER-deliverable clean energy by 2046, robot-mediated capacity, storage capacity, budget-limited capacity, and program execution capacity. Terminal gross removal is the minimum of those constraints. Durable credited removal is gross capacity times the sampled 100-year lifecycle/durability fraction. Net climate result then subtracts residual positive emissions and Jevons-style rebound or delayed abatement. This is still not a forecast. It is a first uncertainty discipline layer.

| Test | Current Monte Carlo read |
|---|---:|
| Gross capacity at or above 100 GtCO2/year | 0.8% |
| Durable 100-year credit at or above 100 GtCO2/year | 0.1% |
| Positive net climate result after residual emissions and rebound | 56.0% |
| Net removal at least as large as current annual anthropogenic emissions | 1.5% |
| Durable credited removal, median and P10-P90 | 30.8 Gt/y; 14.1-57.9 Gt/y |
| Net after residual emissions and rebound, median and P10-P90 | 2.0 Gt/y; -12.6-23.0 Gt/y |
| Leading bottleneck among durable-target failures | clean energy, 67.4% of failed durable samples |

| Parameter | Correlation with net climate result | Interpretation |
|---|---:|---|
| Annual clean-addition growth | 0.48 | Growth rate for annual global clean-generation additions through 2046. |
| Residual emissions in 2046 | -0.44 | Positive emissions remaining when the AETHER system reaches industrial scale. |
| Rebound or delayed-abatement fraction | -0.37 | Extra emissions or delayed abatement induced by cheap removal. |
| Full-system energy intensity | -0.28 | Lower values make the clean-energy constraint less binding. |
| AETHER share of new clean generation | 0.27 | Share of new clean generation that can be allocated to AETHER after other demand claims. |
| 100-year durable credit fraction | 0.16 | Fraction of gross captured CO2 credited after lifecycle and 100-year durability haircuts. |

The important result is not the exact probability. These are hand-set ranges, not calibrated expert priors. The important result is the shape of failure. Within the coded ranges, AETHER does not usually fail at the first-order mass-and-energy arithmetic layer. It fails because the abundance premise has to arrive as a coupled industrial package. Low energy intensity is not enough if clean power is unavailable. Cheap robots are not enough if each unit supports too little installed capacity or if storage throughput is capped. A low cost per tonne is not enough if induced demand drives net atmospheric use beyond verified capacity. Durable climate reversal requires overbuilding gross capacity, improving lifecycle performance, bounding residual emissions, and operating inside a measured atmospheric budget.
### 10.1 Distribution Evidence and Correlation Gaps

The v0.26 update adds a distribution-evidence registry for the Monte Carlo layer. This does not make the probabilities calibrated. It does something more basic and more necessary: it stops hand-set uncertainty ranges from looking cleaner than they are. Each sampled input now has an evidence grade, source keys, distribution status, distribution rationale, correlation family, paper-use rule, and next evidence task.

The registry currently maps 15 uncertainty inputs. 11 are priority-1 upgrades, and 6 remain D-grade scenario or provisional inputs. The hardest parameters are not merely engineering numbers. Robot productivity, AETHER clean-power allocation, execution realization, rebound, terminal storage throughput, and delivered cost combine technology, institutions, market allocation, and legitimacy.

| Priority band | Count | Parameters | Next upgrade |
| --- | --- | --- | --- |
| high_priority_source_distribution | 7 | clean_addition_growth_rate;energy_gj_tco2;clean_deliverability_fraction;cost_usd_tco2;durability_fraction_100y;rebound_fraction_of_gross;storage_terminal_gtco2_y | Fit source-backed pathway or sector distributions and replace triangular ranges. |
| high_priority_assumption_correlation | 4 | aether_clean_share;execution_realization_fraction;robot_output_growth_rate;robots_per_mtco2_y_capacity | Run adversarial sensitivity, expert elicitation, and correlated scenario families before using probabilities rhetorically. |
| medium_priority_program_design | 4 | gross_overbuild_factor;residual_emissions_2046_gtco2_y;aether_robot_share;annual_budget_trillion_usd | Tie these variables to explicit governance, funding, and portfolio design branches. |
| lower_priority_documentation | 0 |  | Keep source notes current and promote to distributions when the surrounding model matures. |

The correlation table is equally important. Clean-power growth, clean-power allocation, and deliverability should move together. Robot manufacturing, useful robot productivity, cost, and execution quality should move together. Storage throughput, MRV burden, durability, and overbuild should move together. Budget, rebound, residual emissions, and commons governance should move together. Treating them as independent variables is acceptable for a first screen, but not for a serious probability claim.

The next proof standard is therefore clear: replace triangular hand ranges with sourced distributions, expert elicitation, correlated scenario families, and adversarial sensitivity review. Until then, uncertainty outputs are model triage, not forecasts.

### 10.2 Correlated Uncertainty Scenario Families

The v0.33 repo adds a correlated uncertainty screen because independent Monte Carlo sampling is too kind to a system like AETHER. A real 100 GtCO2/year program will not draw clean-power growth, robot productivity, storage throughput, durability, rebound, costs, and execution from separate worlds. The same political, industrial, and physical conditions that make one bottleneck better often move other bottlenecks too. The reverse is also true: storage failure, public resistance, rebound, and execution drag can cluster.

The model keeps the same capacity equations as the first uncertainty screen. It then uses the distribution registry and creates seven scenario families: independent reference, clean-power abundance, automation abundance, storage/MRV failure, policy/rebound failure, full abundance aligned, and full failure clustered. The family shifts are explicit and directional. Favorable families push related variables toward their favorable bounds; failure families push related variables toward adverse bounds. This is not a calibrated joint probability distribution. It is a discipline layer that prevents the paper from implying that all favorable parameters can be mixed freely without a story about why they co-occur.

![AETHER correlated uncertainty scenario families](../../analysis/figures/correlated_uncertainty_success_frontier.png)

| Scenario family | Durable >=100 | Net positive | Strong reversal | Median net Gt/y | Primary binding |
| --- | --- | --- | --- | --- | --- |
| Independent | 0.1% | 56.1% | 1.7% | 2.2 | clean_energy |
| Clean power | 2.4% | 88.9% | 14.4% | 19.8 | storage |
| Automation | 0.6% | 56.9% | 3.1% | 2.7 | clean_energy |
| Storage/MRV failure | 0.0% | 38.5% | 0.1% | -2.9 | clean_energy |
| Policy/rebound failure | 0.0% | 29.6% | 0.0% | -6.2 | clean_energy |
| Full abundance | 57.3% | 100.0% | 88.5% | 72.9 | program_execution |
| Full failure | 0.0% | 0.0% | 0.0% | -23.7 | clean_energy |

The result is a more honest feasibility boundary. AETHER is weakest when rebound, residual emissions, storage/MRV weakness, and execution failure move together. It is strongest only when clean power, automation, cost reduction, storage throughput, durability, budget, and execution are jointly favorable. That does not prove the abundance case; it states the condition the research program has to make technically and institutionally credible.

The generated outputs are `analysis/tables/aether_correlated_uncertainty_scenarios.csv`, `analysis/tables/aether_correlated_uncertainty_samples.csv`, `analysis/tables/aether_correlated_uncertainty_summary.csv`, and `analysis/tables/aether_correlated_uncertainty_family_effects.csv`. The figure is `analysis/figures/correlated_uncertainty_success_frontier.png`.

## 11. Cost Stack and Automation Leverage

The earlier cost section used whole-system numbers because the first question was scale: every $10/tCO2 becomes $1 trillion/year at 100 GtCO2/year. That arithmetic is still the right starting point, but it hides the engineering question. AETHER does not need "costs to fall" in the abstract. It needs specific cost buckets to collapse while other buckets hit real floors.

The v0.9 model separates delivered cost into energy, plant/contactors, sorbents and materials, compression/transport/storage, MRV/insurance/liability, robot operations and maintenance, finance/permitting/overhead, and carbon/O2 product handling. The current DAC-like stack is about $606/tCO2, or $60.6 trillion/year at 100 GtCO2/year. The AETHER automation-push stack is about $86/tCO2, or $8.6 trillion/year at 100 GtCO2/year. If AETHER must overbuild to credit 100 GtCO2/year durable removal at the current storage-lifecycle ratio, that same stack costs about $10.1 trillion/year.

| Scenario | Energy | Plant/contactors | Materials | Storage/logistics | MRV/liability | Robot O&M | Finance/overhead | Carbon/O2 handling | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Current DAC-like | $156 | $170 | $80 | $35 | $15 | $65 | $85 | $0 | $606 |
| AETHER automation push | $20 | $24 | $10 | $14 | $5 | $4 | $9 | $0 | $86 |
| Moonshot modular | $8 | $10 | $5 | $8 | $3 | $2 | $4 | $0 | $40 |
| Full splitting default | $116 | $20 | $8 | $8 | $5 | $5 | $10 | $45 | $217 |
| Deep abundance floor | $4 | $6 | $3 | $5 | $2 | $2 | $3 | $0 | $24 |

The automation-push case is a 7.0 x reduction relative to the current DAC-like stack. That is not one miracle. It requires cheap clean energy, lower energy intensity, modular plant manufacturing, better sorbents, faster construction, cheaper drilling and storage logistics, lower MRV cost, less downtime, and lower finance/permitting friction. AI and robotics can help in many of those places: lab automation can search materials and contactor designs faster; robots can reduce construction and maintenance labor; autonomous inspection can lower monitoring cost; software can coordinate plants, wells, sensors, and spare parts. But the model keeps an explicit floor. Energy, storage, MRV, liability, and product handling do not disappear because the labor input gets cheap.

The robot-hour model makes the same point from the other direction.

| Robot case | Unit cost | Utilization | Lifetime | Direct robot-hour cost |
|---|---:|---:|---:|---:|
| Early humanoid / field robot | $200,000 | 4,000 h/y | 5 y | $25.14/h |
| Industrial scale robot | $100,000 | 5,500 h/y | 7 y | $7.88/h |
| AETHER factory robot | $50,000 | 6,500 h/y | 8 y | $3.28/h |
| Deep abundance robot | $25,000 | 7,500 h/y | 10 y | $1.12/h |

Direct robot-hour cost can plausibly fall by roughly an order of magnitude in an aggressive manufacturing scenario. That matters for AETHER because the project would need mines, wells, factories, pipelines, contactors, sensors, labs, and maintenance crews everywhere. But cheap robot hours are not the same thing as cheap tonnes. If one robot-hour is cheap but each tonne still needs clean power, sorbent replacement, storage monitoring, insurance, and capital, the tonne stays expensive. The useful robotics claim is therefore narrower and stronger: robotics can compress the automatable part of the stack and accelerate deployment. It cannot by itself beat thermodynamics or make shared sinks safe.

The full-splitting case shows the danger of optimizing the wrong variable. Splitting all CO2 into carbon and oxygen makes the stored carbon compact, but the modeled cost rises to about $217/tCO2 because the energy and product-handling burden dominates. The deep-abundance floor reaches about $24/tCO2, or $2.4 trillion/year at 100 GtCO2/year. That is the kind of number that makes AETHER economically imaginable. It is also a warning: reaching it requires the entire industrial stack to work, not just a lower labor bill.
## 12. Technology Acceleration and Order-of-Magnitude Frontier

The abundance premise has to be translated into cost buckets. "AI and robotics get much better" is not enough. AETHER needs to know which parts of the cost stack can plausibly move by a factor of two, ten, or more, and which parts hit energy, storage, MRV, liability, and governance floors.

NCSES estimates that the United States performed about $939.6 billion of R&D in 2023 [@ncses_us_rd_2023]. IEA estimates global public energy R&D at about $55 billion in 2025 and corporate energy R&D at about $160 billion in 2024 [@iea_state_energy_innovation_2026]. A $1 trillion/year AETHER RD&D program would therefore be roughly comparable to all U.S. R&D and about 4.7 times current public plus corporate energy R&D. That is the right scale of comparison. AETHER is not a normal climate-tech startup category. It is closer to a standing industrial-science mobilization.

| Scenario | Delivered cost | Annual cost at 100 GtCO2/year | Reduction vs current | Orders of magnitude |
|---|---:|---:|---:|---:|
| Current DAC-like | $605.6/tCO2 | $60.6T/year | 1.0x | 0.00 |
| AETHER automation push | $85.9/tCO2 | $8.6T/year | 7.0x | 0.85 |
| Moonshot modular | $40.3/tCO2 | $4.0T/year | 15.0x | 1.18 |
| Deep abundance floor | $24.2/tCO2 | $2.4T/year | 25.1x | 1.40 |

The deep-abundance case is about a 25x reduction from the current DAC-like stack, or about 1.4 orders of magnitude. That is aggressive but not magical. The harder part is that even this floor is still about $2.4 trillion/year at 100 GtCO2/year. AETHER needs more than a lower robot wage. It needs the whole delivered-cost frontier to move.

The bucket-level result is more useful than the total. Energy falls only if both energy intensity and clean electricity cost fall. Plant/contactors fall if designs become modular, mass-manufactured, and robot-built. Materials fall if AI-assisted discovery, recycling, and supply chains reduce sorbent and catalyst replacement. Robot O&M can plausibly fall by more than an order of magnitude under mass manufacturing and high utilization. Finance/permitting and MRV/liability do not vanish; they have to be redesigned without making the accounting weaker.

This creates a clean plausibility test. AETHER is plausible only if AI and robotics accelerate the automatable buckets while the hard-floor buckets also improve through energy abundance, storage learning, and governance. If the program produces cheap robots but storage remains bespoke, clean power remains scarce, or MRV remains expensive and fragile, the cost per tonne does not fall far enough.
## 13. Feasibility Gate Scorecard

The model suite now supports a simpler synthesis: AETHER is not a single yes-or-no claim. It is a stack of feasibility gates. If one gate fails, the 100 GtCO2/year target becomes either a smaller offset program, a research agenda, or a failure case. If several gates clear together, the idea becomes a serious climate-reversal infrastructure program.

![AETHER feasibility gate scorecard](../../analysis/figures/feasibility_gate_scorecard.png)

| Gate | Current status | Quantitative anchor | Required next proof |
|---|---|---|---|
| Climate target arithmetic | conditional_pass | Break-even rebound: 57.8% of gross under simple accounting; 41.7% after 25 kg/MWh LCA; 23.1% after LCA+MRV | A policy and market design that keeps removal additional rather than permissive. |
| Carbon-cycle outcome | research_gap | 350 ppm is an imposed management floor; species-level FAIR publication gates still fail | Upgrade the Joos impulse-response screen to FAIR-class or Earth-system modeling. |
| Pathway portfolio potential | upper_tail_dependency | 100 Gt/y portfolio vs 37.5 Gt/y central assessed potential sum and 107.6 Gt/y high assessed sum | Regional cost and potential curves with substitution rules when one pathway under-delivers. |
| Clean power and firm energy | major_bottleneck | 91,667 TWh/y gross clean generation; 27.5 TW nameplate; 3.5 TW firm clean capacity | Regional dispatch, transmission, storage-duration, and colocation model. |
| Air-contactor and factory scale | major_bottleneck | 100 Gt all-air NASEM reference: 3,771 km2 face area; 9,290 TWh/y fan energy; 200,000 STRATOS equivalents | Factory-rate model for contactor modules, sorbent production, replacement logistics, and autonomous maintenance. |
| Durable credited storage | major_bottleneck | 100 Gt/y gross becomes 84.9 Gt/y 100-year durable credit; 117.8 Gt/y gross required for 100 Gt durable credit | Pathway-specific lifecycle assessment and basin-level storage regionalization. |
| Delivered cost frontier | major_bottleneck | AETHER automation push: $86/tCO2 and $8.6T/y; deep-abundance floor: $24/tCO2 | Component-level TEA tied to pathway-specific plant designs and supply chains. |
| Robotics and automation | research_gap | Automation-push P50: 840142 robots/y, 1.55x IFR 2024; 0% pass share | Task-family productivity, duty-cycle, reliability, supervision, maintenance, and replacement distributions. |
| Integrated 2046 feasibility | upper_tail_dependency | A legacy optimistic case passes; it is not integrated with the later field-productivity, species-emissions, and LCA/MRV gates | Integrated scenario model with sourced distributions and correlated assumptions. |
| Uncertainty screen | research_gap | 0.75% gross-100 share; 0.09% durable-100 share; median durable credit 30.8 Gt/y | Expert elicitation, sourced distributions, correlation structure, and adversarial sensitivity review. |
| Governance and rebound | governance_constraint | Break-even rebound falls from 57.8% gross to 41.7% after LCA and 23.1% after LCA+MRV in the 25 kg/MWh case | Operational governance model for atmospheric/ocean sink rights, fees, bans, liability, and citizen ownership. |
The current scorecard is intentionally conservative in language. The strongest pro-AETHER point is that no single first-order calculation rules out a future 100 GtCO2/year system. The strongest anti-hype point is that no single breakthrough makes it happen. AETHER requires clean power, contactor or pathway throughput, durable storage, creditable MRV, cost compression, robot-enabled deployment, rebound control, and governance to work as one coupled system.

The uncertainty screen shows why this should still be presented as a research program. With the current hand-set AETHER distributions, only 0.75% of samples reach 100 GtCO2/year gross capacity and only 0.09% reach 100 GtCO2/year durable credited removal. The median durable credit is 30.8 GtCO2/year. Those numbers are not calibrated probabilities, but they are useful discipline. They say the target lives in the upper tail unless the bottlenecks move together.

### 13.1 Adversarial Review and Falsification Standard

The current repo keeps an adversarial review layer because AETHER should not become a paper that wins only by choosing favorable assumptions. A scientist-presentable version has to say what would break it. The generated register organizes likely specialist attacks across carbon-cycle modeling, power systems, CDR process engineering, storage, robotics, economics, MRV, and governance. The point is not to claim that those attacks are already solved. The point is to make them inspectable.

![AETHER adversarial reviewer risk register](../../analysis/figures/adversarial_review_risk_register.png)

The current register has 8 expert panels, 8 high-risk panels, 5 P0 falsification tests, average reviewer risk 4.62 on a 1-5 scale, and average evidence maturity 1.88 on a 1-5 scale. This is a warning label, but a useful one. A high-risk score is acceptable at this stage only if the paper attaches a decisive test to it. If a P0 test fails, the manuscript should narrow its claim rather than bury the failure under another scenario.

| Reviewer panel | Risk | Evidence maturity | Next decisive artifact |
| --- | --- | --- | --- |
| carbon_cycle_and_climate | 5 | 2 | FAIR-class climate workflow and methods appendix |
| energy_systems_and_power_markets | 5 | 2 | regional dispatch and additionality model |
| cdr_process_and_materials | 5 | 2 | pathway-specific BOM and process TEA |
| storage_and_subsurface | 5 | 2 | basin-level storage and liability model |
| robotics_and_ai_productivity | 4 | 2 | task-family productivity distribution database |
| economics_and_finance | 4 | 2 | component TEA and capital program model |
| mrv_credit_integrity_and_law | 4 | 2 | method-specific MRV and liability model |
| governance_and_rebound | 5 | 1 | governance and rebound-control model |

The P0 tests are the hard gates. FAIR-class or Earth-system modeling has to preserve a meaningful climate-reversal outcome under plausible forcing assumptions. Additional clean power has to be deliverable after hourly matching, interconnection, transmission, and competing demand. Storage has to survive basin-level injection, pressure, leakage, permitting, monitoring, and liability constraints. MRV and lifecycle accounting have to turn gross capture into creditable durable removal without requiring physically impossible overbuild. Rebound and delayed abatement have to stay below the threshold that erases the simple net-negative benefit.

The generated artifacts are `analysis/tables/aether_adversarial_review_panels.csv`, `analysis/tables/aether_falsification_tests.csv`, `analysis/tables/aether_scientist_feedback_packet.csv`, `analysis/tables/aether_adversarial_review_summary.csv`, and `analysis/figures/adversarial_review_risk_register.png`. The companion review note is `manuscript/review/aether_adversarial_review_plan.md`.

## 14. Plausibility Judgment

AETHER is not a forecast. It is a conditional feasibility claim about what could become possible if AI, robotics, energy, storage, and governance improve together instead of separately. The current evidence supports three judgments.

First, the selected first-order screens reveal no immediate conservation-law contradiction. That is weaker than full physical feasibility. Pathway potential, energy delivery, contactor and material throughput, basin-level injectivity, ecology, lifecycle emissions, and governance remain unresolved, so the result supports continued investigation rather than a claim that the system can be built.

Second, current systems do not make it plausible. Present DAC costs, current durable CDR scale, storage permitting, firm clean-power buildout, MRV, and lifecycle accounting are all far short of what the 100 GtCO2/year case needs. Treating today's bottlenecks as already solved would make the proposal weaker, not stronger.

Third, AI and robotics only matter if they move the binding constraints. Useful autonomy would need to speed R&D, plant construction, mining, drilling, monitoring, maintenance, supply chains, and permitting evidence. A large robot count is not itself enough. The relevant metric is delivered durable tonnes per unit of clean energy, capital, land, storage capacity, and public legitimacy.

The serious version of AETHER is therefore a staged research program with go/no-go gates. Its value is not that it predicts 100 GtCO2/year removal. Its value is that it gives academia, industry, and policy a concrete way to test whether climate reversal can become an engineered option before the world needs it under worse conditions.
## 15. Research Roadmap

The next AETHER work should be organized around model layers that can be improved without rewriting the whole project.

1. Carbon-cycle and climate-response model: extend the forcing-driven FAIR run into a full species-emissions FAIR-class or Earth-system-model workflow that includes state-dependent ocean and land response, non-CO2 forcing, aerosols, ocean heat uptake, zero-emissions commitment, temperature, and lifecycle emissions.
2. Energy model: upgrade the current capacity arithmetic into regional solar, wind, nuclear, geothermal, storage, transmission, interconnection, industrial heat, contactor colocation, and dispatch models under conservative, aggressive, and AI-accelerated cases.
3. Capture, pathway, and MRV model: deepen the current pathway portfolio into regional cost curves for DAC, enhanced weathering, biomass-based removal, ocean alkalinity, mineralization, and hybrid systems by energy, water, materials, durability, MRV difficulty, credit invalidation, and liability.
4. Storage-state model: deepen the current conversion ledger into pathway-specific gas, supercritical, liquid, mineral carbonate, solid carbon, dissolved inorganic carbon, and product pathways by volume, mass, safety, leakage, compression, transport, lifecycle emissions, and energy cost.
5. Robotics model: convert the current evidence map into source-backed distributions for unit costs, useful autonomous task-hours, duty cycle, deployment rates, maintenance, spare parts, fleet service, and bottleneck reductions for lab automation, construction robots, field robots, drilling robots, warehouse robots, and humanoids.
6. Cost model: deepen the current cost stack and technology-acceleration frontier into pathway-specific capex, learning curves, energy prices, RD&D throughput, sorbent/material replacement, compression, transport, storage, MRV, insurance, finance cost, permitting, and decommissioning.
7. Parameter database: convert `data/parameters/aether_parameter_evidence.csv` from an evidence map into a source-backed parameter database with distributions, correlations, and versioned source notes.
8. Governance model: compare carbon taxes, cap-and-dividend, public trusts, citizen sink ownership, liability regimes, and strict bans for dangerous outputs.
9. Scenario figures: show atmospheric CO2 trajectories, energy demand, cost sensitivity, storage volume, plant count, robot fleet assumptions, and failure cases.

The paper should eventually show changes over time, not only static endpoints. AETHER's academic contribution will come from making the transition path visible: how many plants, how much power, how many robots, how much storage, how much capital, and how much verified drawdown are needed each year.

## 16. Limitations

AETHER is a conditional feasibility analysis, not a forecast. It asks what would have to be true for 100 GtCO2/year gross removal to become a serious climate-reversal infrastructure program under aggressive AI, robotics, and energy-abundance assumptions.

The carbon-cycle and climate-response treatment is now better than atmosphere-only ppm conversion, but still too simple for final climate claims. The Joos impulse-response model, AR6-anchored forcing proxy, dynamic emulator, FAIR-readiness deck, forcing-driven FAIR execution, and species-emissions handoff are useful for scenario discipline. They do not replace a full species-emissions FAIR or Earth-system treatment of state-dependent land/ocean response, non-CO2 forcing, aerosols, ocean heat uptake, zero-emissions commitment, ocean chemistry, lifecycle species traces, or regional climate effects.

The cost and robot models are deliberately explicit, but still coarse. They show which orders of magnitude matter; they do not yet replace component-level TEA, process simulation, audited factory learning curves, field-productivity measurements, duty-cycle data, service-cost data, or pathway-specific bills of materials.

Storage, MRV, and lifecycle accounting remain major gates. The repo now separates gross captured tonnes, durable tonnes, and creditable tonnes, but method-specific leakage, reversal, monitoring duration, invalidation, liability, and replacement-media loops still need to be sourced and modeled at the pathway and region level.

Robotics assumptions are especially uncertain. Industrial robot deployment statistics are real, but humanoid and general-purpose robot production claims remain noisy. The paper should not rely on social-media claims except as leads, and it should treat company-primary production claims as signals until independent audits or field data exist.

The public-carbon-utility model is an AETHER design hypothesis, not settled law or a demonstrated institution. Treating atmospheric capacity as citizen-held or trust-administered may align incentives, but a weak budget or price could authorize more net loading than the removal system can manage. Legal authority, cross-border coordination, measurement, liability, local pollution controls, revenue allocation, and democratic accountability remain unresolved gates.

Finally, the 100 GtCO2/year target is intentionally extreme. A smaller program may be easier to justify, finance, and govern. The point of the 100 Gt screen is to expose physical and institutional bottlenecks clearly enough that the feasible scale can be argued with evidence instead of slogans.

### 16.1 Planetary Engineering and the Terraforming Boundary

AETHER qualifies as a low form of terraforming in a literal but limited sense: deliberate, planetary-scale alteration of atmospheric composition to maintain a chosen climate state. On Earth, that framing increases the burden of consent, monitoring, reversibility, liability, and international governance. It does not make the planet fully controllable, and it does not imply that carbon removal can reconstruct extinct species, lost ice, displaced communities, or every regional climate state.

Descendant capabilities could have off-world uses. Autonomous construction, atmosphere processing, gas separation, mineralization, closed-loop clean power, and environmental monitoring are plausible components of future habitat engineering on other celestial bodies. The present work does not model Mars, Venus, the Moon, or any other extraterrestrial environment, and it provides no evidence that terrestrial AETHER designs transfer directly. Off-world application remains a speculative research branch outside this paper's feasibility claim.

## 17. Conclusion

AETHER is worth pursuing because the feasibility boundary is not obvious. A 100 GtCO2/year removal system is far beyond today's carbon-removal industry, but it is not a violation of physics. The real constraints are energy, capital, storage, air throughput, materials, measurement, and governance.

The strongest version of the abundance thesis is not that AI solves climate change by thinking harder. It is that AI and robotics might accelerate the physical economy enough to make previously absurd infrastructure scales reachable: faster materials discovery, cheaper plants, automated construction, better drilling, more reliable monitoring, and cleaner energy buildout. Even then, the system only works if capture energy falls toward 1-3 GJ/tCO2, storage avoids unnecessary splitting, clean power grows by sustained multiples of today's record additions, and annual cost falls into a range that civilization can pay without cannibalizing everything else.

AETHER should therefore proceed as a serious research program, not a slogan. The next version should turn this static feasibility analysis into a time-dependent model with citations, figures, and failure cases. The goal is not to make climate reversal sound easy. The goal is to make the necessary machinery visible enough that the idea can be judged scientifically.

## Appendix A: Equation Ledger and Reproducibility

The current manuscript has a dedicated equation ledger rather than relying only on prose. The ledger contains 15 equations and 10 unit checks covering the main transformations in the paper: ppm-equivalent arithmetic, net removal before rebound, energy conversions, average power, CO2 splitting energy, storage-state volume, solid-carbon and oxygen coproduct mass, durable-credit haircuts, injection well equivalents, storage capacity years, robot-hour cost, learning curves, rebound threshold, and air-contactor area.

The full appendix lives in `manuscript/appendices/aether_model_equations_and_reproducibility.md`. The generated tables are `analysis/tables/aether_model_equation_ledger.csv` and `analysis/tables/aether_dimensioned_unit_checks.csv`. The current unit checks all pass, which means the headline unit transformations are explicit and internally consistent. This does not prove the scenario assumptions. It makes the assumptions easier to audit.

The reproducibility rule is simple: a paper claim should trace to a source-backed anchor, a derived equation, or a named model output. If it cannot be traced to one of those, it should stay out of the scientific claim set or be labeled as a research question.

## Appendix B: Submission Package and Review Gates

The v0.45 repo includes a submission package so the paper can be reviewed as a managed research artifact rather than a loose Markdown draft. This does not make AETHER publication-ready. It makes the remaining barriers visible and reproducible.

Generated package artifacts:

- `manuscript/submission/aether_submission_manuscript.md`
- `manuscript/submission/aether_submission_manifest.md`
- `manuscript/submission/README.md`
- `analysis/tables/aether_figure_inventory.csv`
- `analysis/tables/aether_submission_readiness_gates.csv`
- `analysis/tables/aether_manuscript_style_audit.csv`
- `manuscript/review/aether_submission_checklist.md`

The current package inventories 41 paper figures and 41 total PNG figures. The submission-gate table marks 5 gates as pass, 5 as partial, and 2 as fail. The failing gates are not cosmetic: climate response and species-emissions inputs still block publication-grade temperature claims.

| Gate | Status | Current evidence |
| --- | --- | --- |
| S01_citation_coverage | pass | 83 cited keys; 0 missing BibTeX entries |
| S02_figure_resolution | pass | 41 paper figure references; 0 missing files |
| S03_equation_reproducibility | pass | 10 unit checks; 0 failures |
| S04_claim_evidence | pass | 14 claim-evidence rows |
| S05_climate_model_publication_grade | fail | Forcing-driven FAIR diagnostic exists, but species-emissions handoff still blocks publication-grade climate claims. |
| S06_species_emissions_inputs | fail | 7 failing species-emissions gates out of 10 |
| S07_clean_power_delivery | partial | 7 clean-power deliverability summary rows plus regional dispatch screen |
| S08_storage_mrv_lifecycle | partial | Route-level storage, lifecycle, MRV, and credit-integrity screens exist. |
| S09_robotics_field_productivity | partial | Production verification and field-productivity distribution screens exist, but multipliers remain provisional. |
| S10_adversarial_review | partial | 10 falsification-test rows in the adversarial review packet |
| S11_style_and_duplicate_scan | pass | old repeated FAIR phrase count: 0; editorial placeholder hits: 0 |
| S12_submission_format | partial | Generated Markdown submission package exists; final journal format is not selected. |

## Appendix C: Independent Calculation Audit

The independent calculation audit recomputes portfolio, energy, cost, stoichiometry, storage, durability, MRV, lifecycle, rebound, well-count, robotics, unit, and finite-value checks from generated tables. All current checks pass. This establishes internal arithmetic consistency only; it does not validate assumptions or forecasts.
## References

### AETHER Rendered References

Generated from `references/bibtex/sources.bib` and citation keys used in `manuscript/paper/aether_scientific_paper.md`.

- Cited source keys: 83
- BibTeX entries found: 83
- Missing BibTeX entries: 0

Source keys are retained in brackets for traceability to the source register. The next publication step is a target-journal CSL/Pandoc render, not hand-editing this generated list.

- **[agility_robofab_2023]** Agility Robotics. (2023). *Opening RoboFab: World's First Factory for Humanoid Robots*. https://www.agilityrobotics.com/content/opening-robofab-worlds-first-factory-for-humanoid-robots.
- **[alcott_2005_jevons_paradox]** Alcott, Blake. (2005). *Jevons' Paradox*. Ecological Economics. doi:10.1016/j.ecolecon.2005.03.020.
- **[amazon_robotics_750k_robots_2024]** Quinlivan, Joseph. (2024). *How Amazon deploys collaborative robots in its operations to benefit employees and customers*. https://www.aboutamazon.com/news/operations/how-amazon-deploys-robots-in-its-operations-facilities.
- **[aschenbrenner_2024_situational_awareness]** Aschenbrenner, Leopold. (2024). *Situational Awareness: The Decade Ahead*. https://situational-awareness.ai/. Note: Scenario essay; accessed 2026-08-09.
- **[berkeley_lab_queued_up_2025]** Lawrence Berkeley National Laboratory. (2025). *Queued Up: 2025 Edition, Characteristics of Power Plants Seeking Transmission Interconnection As of the End of 2024*. https://eta.lbl.gov/publications/queued-2025-edition-characteristics.
- **[california_energy_commission_2024_tseg]** California Energy Commission. (2025). *2024 Total System Electric Generation*. https://www.energy.ca.gov/data-reports/energy-almanac/california-electricity-data/2024-total-system-electric-generation.
- **[chatterjee_huang_2020_unrealistic_dac]** Chatterjee, Sudipta, and Huang, Kuo-Wei. (2020). *Unrealistic energy and materials requirement for direct air capture in deep mitigation pathways*. Nature Communications. doi:10.1038/s41467-020-17203-7. https://www.nature.com/articles/s41467-020-17203-7.
- **[climeworks_mammoth_2024]** Climeworks. (2024). *Climeworks switches on world's largest direct air capture plant*. https://climeworks.com/press-release/climeworks-switches-on-worlds-largest-direct-air-capture-plant-mammoth.
- **[cornell_public_trust_doctrine]** Legal Information Institute, Cornell Law School. (2026). *Public trust doctrine*. https://www.law.cornell.edu/wex/public_trust_doctrine. Note: Accessed June 9, 2026..
- **[eia_texas_energy_profile_2024]** U.S. Energy Information Administration. (2025). *Texas State Energy Profile and Analysis*. https://www.eia.gov/states/TX/overview. Note: 2024 data. Accessed June 9, 2026..
- **[epa_class_vi_wells_2026]** U.S. Environmental Protection Agency. (2026). *Class VI - Wells used for Geologic Sequestration of Carbon Dioxide*. https://www.epa.gov/uic/class-vi-wells-used-geologic-sequestration-carbon-dioxide. Note: Last updated May 26, 2026. Accessed June 9, 2026..
- **[epa_current_class_vi_projects_2026]** U.S. Environmental Protection Agency. (2026). *Current Class VI Projects under Review at EPA*. https://www.epa.gov/uic/current-class-vi-projects-under-review-epa. Note: Last updated May 26, 2026. Accessed June 9, 2026..
- **[epa_subpart_rr_mrv_2026]** U.S. Environmental Protection Agency. (2026). *Subpart RR: Geologic Sequestration of Carbon Dioxide*. https://www.epa.gov/ghgreporting/subpart-rr-geologic-sequestration-carbon-dioxide. Note: Accessed June 9, 2026..
- **[eu_crcf_2024]** European Commission. (2024). *Carbon Removals and Carbon Farming (CRCF) Regulation*. https://climate.ec.europa.eu/eu-action/carbon-removals-and-carbon-farming/carbon-removals-and-carbon-farming-crcf-regulation_en.
- **[fair_v13_smith_2018]** Smith, Christopher J. et al.. (2018). *FAIR v1.3: a simple emissions-based impulse response and carbon cycle model*. Geoscientific Model Development. doi:10.5194/gmd-11-2273-2018. https://gmd.copernicus.org/articles/11/2273/2018/.
- **[figure_botq_2025]** Figure AI. (2025). *BotQ: A High-Volume Manufacturing Facility for Humanoid Robots*. https://www.figure.ai/news/botq.
- **[figure_ramping_2026]** Figure AI. (2026). *Ramping Figure 03 Production*. https://www.figure.ai/news/ramping-figure-03-production.
- **[fusion_industry_association_2025]** Fusion Industry Association. (2025). *Over $2.5 Billion Invested in Fusion Industry in Past Year*. https://www.fusionindustryassociation.org/over-2-5-billion-invested-in-fusion-industry-in-past-year/.
- **[georgetown_atmospheric_trust_2023]** Georgetown Environmental Law Review. (2023). *Up in the Air: How the Atmospheric Trust Doctrine is Being Used to Fight Climate Change*. https://www.law.georgetown.edu/environmental-law-review/blog/up-in-the-air-how-the-atmospheric-trust-doctrine-is-being-used-to-fight-climate-change/.
- **[giro_2023_ai_polymer_membranes]** Giro, Ronaldo, Hsu, Hsianghan, and Kishimoto, Akihiro et al.. (2023). *AI powered, automated discovery of polymer membranes for carbon capture*. npj Computational Materials. doi:10.1038/s41524-023-01088-3. https://www.nature.com/articles/s41524-023-01088-3.
- **[global_carbon_budget_2025]** Friedlingstein, Pierre et al.. (2026). *Global Carbon Budget 2025*. Earth System Science Data. doi:10.5194/essd-18-3211-2026. https://essd.copernicus.org/articles/18/3211/2026/.
- **[google_kairos_2024]** Google. (2024). *New nuclear clean energy agreement with Kairos Power*. https://blog.google/outreach-initiatives/sustainability/google-kairos-power-nuclear-energy-agreement/.
- **[helion_microsoft_fusion_2023]** Helion Energy. (2023). *Helion announces world's first fusion energy purchase agreement with Microsoft*. https://www.helionenergy.com/articles/helion-announces-worlds-first-fusion-ppa-with-microsoft/.
- **[iaea_nuclear_status_2025]** International Atomic Energy Agency. (2025). *Status and Prospects for Nuclear Power 2025*. https://www.iaea.org/sites/default/files/gc/gov-inf-2025-8-gc69-inf-4.pdf.
- **[iea_critical_minerals_outlook_2025]** International Energy Agency. (2025). *Global Critical Minerals Outlook 2025*. https://www.iea.org/reports/global-critical-minerals-outlook-2025/overview-of-outlook-for-key-minerals.
- **[iea_electricity_2026]** International Energy Agency. (2026). *Electricity 2026*. https://www.iea.org/reports/electricity-2026/flexibility.
- **[iea_energy_ai_2025]** International Energy Agency. (2025). *Energy and AI*. https://www.iea.org/reports/energy-and-ai/executive-summary.
- **[iea_geothermal_future_2024]** International Energy Agency. (2024). *The Future of Geothermal Energy*. https://www.iea.org/reports/the-future-of-geothermal-energy/executive-summary.
- **[iea_global_energy_review_2026]** International Energy Agency. (2026). *Global Energy Review 2026*. https://www.iea.org/reports/global-energy-review-2026/electricity-supply. Note: Licence: CC BY 4.0. Accessed June 9, 2026..
- **[iea_state_energy_innovation_2026]** International Energy Agency. (2026). *The State of Energy Innovation 2026*. https://www.iea.org/reports/the-state-of-energy-innovation-2026/executive-summary.
- **[ifr_world_robotics_2025]** International Federation of Robotics. (2025). *World Robotics 2025 Industrial Robots*. https://ifr.org/worldrobotics/report-2025. Note: Executive summary and press release..
- **[ipcc_ar6_wg1_ch5_carbon_cycle]** Intergovernmental Panel on Climate Change. (2021). *Chapter 5: Global Carbon and Other Biogeochemical Cycles and Feedbacks*. In *Climate Change 2021: The Physical Science Basis. Contribution of Working Group I to the Sixth Assessment Report*. https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-5/.
- **[ipcc_ar6_wg1_ch7_forcing_sensitivity]** Intergovernmental Panel on Climate Change. (2021). *Chapter 7: The Earth's Energy Budget, Climate Feedbacks, and Climate Sensitivity*. In *Climate Change 2021: The Physical Science Basis*. https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-7/.
- **[ipcc_ar6_wg1_fig_5_32_cdr_pulse]** Intergovernmental Panel on Climate Change. (2021). *Figure 5.32: Carbon cycle response to instantaneous carbon dioxide removal from the atmosphere*. https://www.ipcc.ch/report/ar6/wg1/figures/chapter-5/figure-5-32/.
- **[ipcc_ar6_wg1_ts_tcre_2021]** Intergovernmental Panel on Climate Change. (2021). *Technical Summary*. In *Climate Change 2021: The Physical Science Basis*. https://www.ipcc.ch/report/ar6/wg1/chapter/technical-summary/.
- **[ipcc_ar6_wg3_ch12]** Intergovernmental Panel on Climate Change. (2022). *Chapter 12: Cross-sectoral perspectives*. In *Climate Change 2022: Mitigation of Climate Change. Contribution of Working Group III to the Sixth Assessment Report*. https://www.ipcc.ch/report/ar6/wg3/chapter/chapter-12/.
- **[ipcc_ar6_wg3_ch6_ccs_storage]** Intergovernmental Panel on Climate Change. (2022). *Chapter 6: Energy Systems*. In *Climate Change 2022: Mitigation of Climate Change. Contribution of Working Group III to the Sixth Assessment Report*. https://www.ipcc.ch/report/ar6/wg3/chapter/chapter-6/. Note: Section 6.4.2.5 on carbon dioxide capture, utilisation, and storage..
- **[ipcc_ar6_wg3_technical_summary_cdr]** Intergovernmental Panel on Climate Change. (2022). *Technical Summary*. In *Climate Change 2022: Mitigation of Climate Change. Contribution of Working Group III to the Sixth Assessment Report*. https://www.ipcc.ch/report/ar6/wg3/chapter/technical-summary/. Note: Section TS.5.7 and Table TS.7 on carbon dioxide removal..
- **[irena_power_costs_2024]** International Renewable Energy Agency. (2025). *Renewable Power Generation Costs in 2024*. https://www.irena.org/Digital-Report/Renewable-Power-Generation-Costs-in-2024.
- **[joos_2013_impulse_response]** Joos, F. et al.. (2013). *Carbon dioxide and climate impulse response functions for the computation of greenhouse gas metrics: a multi-model analysis*. Atmospheric Chemistry and Physics. doi:10.5194/acp-13-2793-2013. https://acp.copernicus.org/articles/13/2793/2013/.
- **[keith_2018_process_dac]** Keith, David W. et al.. (2018). *A Process for Capturing CO2 from the Atmosphere*. Joule. doi:10.1016/j.joule.2018.05.006. https://www.sciencedirect.com/science/article/pii/S2542435118302253.
- **[kokotajlo_et_al_2025_ai_2027]** Kokotajlo, Daniel et al.. (2025). *AI 2027*. https://ai-2027.com/. Note: Forecast scenario; accessed 2026-08-09.
- **[larsen_et_al_2026_ai_2040]** Larsen, Thomas et al.. (2026). *AI 2040: Plan A*. https://ai-2040.com/. Note: Normative scenario and policy proposal; accessed 2026-08-09.
- **[mcqueen_drennan_2024_warehouse_dac]** McQueen, Noah, and Drennan, David. (2024). *The use of warehouse automation technology for scalable and low-cost direct air capture*. Frontiers in Climate. doi:10.3389/fclim.2024.1415642. https://www.frontiersin.org/journals/climate/articles/10.3389/fclim.2024.1415642/full.
- **[microsoft_constellation_crane_2024]** Constellation Energy. (2024). *Constellation to Launch Crane Clean Energy Center, Restoring Jobs and Carbon-free Power to the Grid*. https://investors.constellationenergy.com/news-releases/news-release-details/constellation-launch-crane-clean-energy-center-restoring-jobs/.
- **[national_academies_dac_ch5_2018]** National Academies of Sciences, Engineering,, and Medicine. (2019). *Negative Emissions Technologies and Reliable Sequestration: A Research Agenda, Chapter 5: Direct Air Capture*. The National Academies Press. doi:10.17226/25259. https://www.ncbi.nlm.nih.gov/books/NBK541435/?report=printable.
- **[national_academies_net_reliable_sequestration]** National Academies of Sciences, Engineering,, and Medicine. (2019). *Negative Emissions Technologies and Reliable Sequestration: A Research Agenda*. The National Academies Press. doi:10.17226/25259. https://www.nationalacademies.org/read/25259/chapter/9.
- **[national_academies_ocean_cdr_2021]** National Academies of Sciences, Engineering,, and Medicine. (2022). *A Research Strategy for Ocean-based Carbon Dioxide Removal and Sequestration*. The National Academies Press. doi:10.17226/26278. https://www.nationalacademies.org/read/26278/.
- **[national_academies_ocean_cdr_2022]** National Academies of Sciences, Engineering,, and Medicine. (2022). *A Research Strategy for Ocean-based Carbon Dioxide Removal and Sequestration*. The National Academies Press. https://www.nationalacademies.org/projects/DELS-OSB-20-02/publication/26278.
- **[ncses_us_rd_2023]** National Center for Science, and Engineering Statistics. (2025). *Discovery: R&D Activity and Research Publications*. https://ncses.nsf.gov/pubs/nsb20257/table/DISC-2. Note: Science and Engineering Indicators. Accessed June 9, 2026..
- **[netl_carbon_storage_atlas_v_2015]** U.S. Department of Energy, National Energy Technology Laboratory. (2015). *Carbon Storage Atlas, Fifth Edition*. https://netl.doe.gov/node/5841. Note: Atlas V page accessed June 9, 2026..
- **[netl_sorbent_dac_2025]** Patel, Kshitij et al.. (2025). *Direct Air Capture Case Studies: Sorbent System (Rev. 1)*. doi:10.2172/2520078. https://www.osti.gov/biblio/2520078.
- **[nist_chemistry_webbook_co2]** National Institute of Standards, and Technology. (2026). *NIST Chemistry WebBook: Carbon dioxide*. https://webbook.nist.gov/cgi/cbook.cgi?Formula=CO2&NoIon=on&cIR=on&cTG=on. Note: NIST Standard Reference Database 69. Accessed June 9, 2026..
- **[nist_chemistry_webbook_co2_calculated]** AETHER model. (2026). *CO2 splitting enthalpy calculation from NIST CO2 formation enthalpy*. Note: Derived from NIST Chemistry WebBook CO2 standard gas enthalpy of formation and CO2 molar mass; CO2 -> C + O2 ideal floor is about 8.94 GJ/tCO2..
- **[nist_cryogenic_fluid_properties]** National Institute of Standards, and Technology. (2026). *Cryogenic Fluid Properties*. https://trc.nist.gov/cryogenics/fluidProperties.html. Note: NIST/TRC reference-data portal. Accessed June 9, 2026..
- **[nist_thermophysical_fluids_2009]** Lemmon, Eric W.. (2009). *Thermophysical Properties of Fluids*. National Institute of Standards and Technology. https://www.nist.gov/publications/thermophysical-properties-fluids. Note: NIST page updated June 2, 2021. Accessed June 9, 2026..
- **[noaa_gml_global_co2_2026]** NOAA Global Monitoring Laboratory. (2026). *Trends in Atmospheric Carbon Dioxide: Global Monthly Mean CO2*. https://www.gml.noaa.gov/ccgg/trends/global.html. Note: Accessed June 9, 2026. February 2026 global monthly mean reported as 428.53 ppm..
- **[noaa_gml_mauna_loa_co2_2026]** NOAA Global Monitoring Laboratory. (2026). *Trends in Atmospheric Carbon Dioxide: Monthly Average Mauna Loa CO2*. https://gml.noaa.gov/ccgg/trends/. Note: Accessed June 9, 2026. May 2026 Mauna Loa monthly average reported as 432.34 ppm..
- **[nrel_atb_2024_electricity]** National Renewable Energy Laboratory. (2024). *2024 Electricity Annual Technology Baseline*. https://atb.nrel.gov/electricity/2024/technologies.
- **[nrel_atb_land_wind_2024]** National Renewable Energy Laboratory. (2024). *Land-Based Wind: 2024 Electricity Annual Technology Baseline*. https://atb.nrel.gov/electricity/2024b/land-based_wind.
- **[nrel_atb_nuclear_2024]** National Renewable Energy Laboratory. (2024). *Nuclear: 2024 Electricity Annual Technology Baseline*. https://atb.nrel.gov/electricity/2024/nuclear.
- **[nrel_solar_land_use_2013]** Ong, Sean et al.. (2013). *Land-Use Requirements for Solar Power Plants in the United States*. https://docs.nrel.gov/docs/fy13osti/56290.pdf.
- **[onepointfive_stratos_2026]** 1PointFive. (2026). *About 1PointFive*. https://www.1pointfive.com/about. Note: Accessed June 9, 2026..
- **[osha_graphite_natural_chemicaldata_2020]** Occupational Safety, and Health Administration. (2020). *Graphite (Natural), Respirable Fraction*. https://www.osha.gov/chemicaldata/665. Note: OSHA Occupational Chemical Database. Last updated December 29, 2020..
- **[ostrom_governing_commons_1990]** Ostrom, Elinor. (1990). *Governing the Commons: The Evolution of Institutions for Collective Action*. Cambridge University Press.
- **[oxford_offsetting_principles_2024]** Axelsson, Kaya et al.. (2024). *Oxford Principles for Net Zero Aligned Carbon Offsetting: Revised 2024*. https://www.smithschool.ox.ac.uk/sites/default/files/2024-02/Oxford-Principles-for-Net-Zero-Aligned-Carbon-Offsetting-revised-2024.pdf.
- **[pubchem_magnesium_carbonate_2026]** National Center for Biotechnology Information. (2026). *PubChem Compound Summary for Magnesium Carbonate*. https://pubchem.ncbi.nlm.nih.gov/compound/Magnesium-carbonate.
- **[realmonte_2019_daccs_iam]** Realmonte, Giulia et al.. (2019). *An inter-model assessment of the role of direct air capture in deep mitigation pathways*. Nature Communications. doi:10.1038/s41467-019-10842-5. https://www.nature.com/articles/s41467-019-10842-5.
- **[roads_to_removal_2023]** Pett-Ridge, Jennifer et al.. (2023). *Roads to Removal: Options for Carbon Dioxide Removal in the United States*. doi:10.2172/2301853. https://www.osti.gov/biblio/2301853.
- **[sorrell_2009_jevons_rebound]** Sorrell, Steve. (2009). *Jevons' Paradox Revisited: The Evidence for Backfire from Improved Energy Efficiency*. Energy Policy. doi:10.1016/j.enpol.2008.12.003.
- **[sriram_2023_opendac]** Sriram, Anuroop et al.. (2023). *The Open DAC 2023 Dataset and Challenges for Sorbent Discovery in Direct Air Capture*. https://arxiv.org/abs/2311.00341.
- **[state_of_cdr_2026]** The State of Carbon Dioxide Removal. (2026). *The State of Carbon Dioxide Removal: 3rd Edition*. https://www.stateofcdr.org/report/3rd-edition. Note: Accessed June 9, 2026..
- **[thompson_2012_learning_by_doing]** Thompson, Peter. (2012). *The Relationship between Unit Cost and Cumulative Quantity and the Evidence for Organizational Learning-by-Doing*. Journal of Economic Perspectives. doi:10.1257/jep.26.3.203.
- **[unitree_g1_product_2026]** Unitree Robotics. (2026). *Unitree G1 Humanoid Robot*. https://www.unitree.com/mobile/g1/. Note: Official product page. Accessed June 9, 2026..
- **[usgs_anderson_storage_risk_liability_2017]** Anderson, Steven T.. (2017). *Risk, liability, and economic issues with long-term CO2 storage--A review*. Natural Resources Research. doi:10.1007/s11053-016-9303-6. https://www.usgs.gov/publications/risk-liability-and-economic-issues-long-term-co2-storage-a-review.
- **[usgs_circular_1386_geologic_storage]** U.S. Geological Survey Geologic Carbon Dioxide Storage Resources Assessment Team. (2013). *National Assessment of Geologic Carbon Dioxide Storage Resources--Results*. https://pubs.usgs.gov/circ/1386/.
- **[usgs_graphite_mcs_2026]** U.S. Geological Survey. (2026). *Mineral Commodity Summaries 2026: Graphite (Natural)*. https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-graphite.pdf.
- **[usgs_mcs_2025_cement]** U.S. Geological Survey. (2025). *Mineral Commodity Summaries 2025*. doi:10.3133/mcs2025. https://doi.org/10.3133/mcs2025.
- **[worldsteel_figures_2025]** World Steel Association. (2025). *World Steel in Figures 2025*. https://worldsteel.org/data/world-steel-in-figures/world-steel-in-figures-2025/.
- **[wri_scaling_dac_impacts_2024]** World Resources Institute. (2024). *Direct Air Capture: Assessing Impacts to Enable Responsible Scaling*. https://publications.wri.org/scaling-dac-in-the-us/introduction.
- **[wright_1936_learning_curve]** Wright, Theodore P.. (1936). *Factors Affecting the Cost of Airplanes*. Journal of the Aeronautical Sciences. doi:10.2514/8.155.
- **[young_2023_dacs_cost_targets]** Young, John, McQueen, Noah, and Charalambous, Charithea et al.. (2023). *The cost of direct air capture and storage can be reduced via strategic deployment but is unlikely to fall below stated cost targets*. One Earth. doi:10.1016/j.oneear.2023.06.004. https://www.sciencedirect.com/science/article/pii/S2590332223003007.
- **[zickfeld_2021_asymmetry]** Zickfeld, Kirsten et al.. (2021). *Asymmetry in the climate-carbon cycle response to positive and negative CO2 emissions*. Nature Climate Change. doi:10.1038/s41558-021-01061-2. https://www.nature.com/articles/s41558-021-01061-2.
