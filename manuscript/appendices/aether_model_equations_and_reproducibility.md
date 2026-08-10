# AETHER Model Equations and Reproducibility Appendix

Last updated: 2026-06-09

This appendix makes the current AETHER model suite easier to audit. The working paper now has many scenario models, but the scientific question depends on a smaller set of repeated transformations: CO2 to ppm-equivalent, GJ/tCO2 to TWh/year, TWh/year to average TW, CO2 splitting stoichiometry, storage volume, durable-credit haircuts, learning curves, injection-well equivalents, and rebound thresholds.

Implementation:

- `analysis/scenario-models/aether_equation_ledger_model.py`
- `analysis/tables/aether_model_equation_ledger.csv`
- `analysis/tables/aether_dimensioned_unit_checks.csv`

## Equation Ledger

| ID | Quantity | Equation | Evidence class | Main artifact |
|---|---|---|---|---|
| `eq_ppm_equivalent` | atmosphere-only ppm-equivalent gross drawdown | `ppm_equivalent = gross_removal_GtCO2_y / 7.8` | derived calculation from carbon-cycle bookkeeping convention | `analysis/tables/aether_scenario_summary.csv` |
| `eq_net_before_rebound` | simple net removal before rebound | `net_removal = gross_removal - residual_emissions` | derived calculation from source-backed emissions baseline plus scenario target | `analysis/tables/aether_scenario_summary.csv` |
| `eq_energy_twh` | annual electricity or heat-equivalent energy | `TWh_y = GtCO2_y * GJ_per_tCO2 * 277.7777778` | unit conversion | `analysis/tables/aether_scenario_summary.csv` |
| `eq_average_power` | average continuous power | `TW_average = TWh_y / 8760` | unit conversion | `analysis/tables/aether_scenario_summary.csv` |
| `eq_co2_splitting_energy` | ideal CO2 splitting energy floor | `splitting_TWh_y = GtCO2_y * 8.94_GJ_tCO2 * 277.7777778` | source-backed plus derived thermodynamic calculation | `analysis/tables/aether_splitting_fraction_sensitivity.csv` |
| `eq_supercritical_volume` | supercritical CO2 storage volume | `volume_km3_y = GtCO2_y * 1e12 / density_kg_m3 / 1e9` | source-backed plus derived storage-state calculation | `analysis/tables/aether_conversion_state_ledger.csv` |
| `eq_solid_carbon_mass` | solid carbon mass from complete CO2 splitting | `carbon_Gt_y = CO2_Gt_y * carbon_molar_mass / CO2_molar_mass` | stoichiometric calculation | `analysis/tables/aether_conversion_state_ledger.csv` |
| `eq_o2_coproduct_mass` | oxygen coproduct mass from complete CO2 splitting | `oxygen_Gt_y = CO2_Gt_y * oxygen_molar_mass / CO2_molar_mass` | stoichiometric calculation | `analysis/tables/aether_conversion_state_ledger.csv` |
| `eq_durable_credit` | 100-year durable credited removal | `durable_credit = gross * (1 - lifecycle_penalty) * (1 - annual_reversal_rate) ** 100` | scenario assumption and derived model output | `analysis/tables/aether_storage_lifecycle_routes.csv` |
| `eq_geologic_well_equivalents` | geologic injection well-equivalent count | `wells = geologic_GtCO2_y * 1000 / well_productivity_MtCO2_y` | scenario assumption and derived model output | `analysis/tables/aether_injection_corridor_requirements.csv` |
| `eq_storage_capacity_years` | capacity years at assigned storage throughput | `capacity_years = proxy_capacity_GtCO2 / assigned_injection_GtCO2_y` | source-backed anchor plus scenario allocation | `analysis/tables/aether_regional_storage_allocation.csv` |
| `eq_robot_hour_cost` | direct robot-hour cost | `robot_hour_cost = unit_cost * (1 + maintenance_fraction) / (lifetime_years * utilization_hours_y)` | scenario assumption and derived calculation | `analysis/tables/aether_robot_labor_costs.csv` |
| `eq_learning_curve` | learning-curve cost decline | `cost = max(floor_cost, initial_cost * (1 - learning_rate) ** doublings)` | scenario assumption grounded in learning-curve literature | `analysis/tables/aether_learning_curve_costs.csv` |
| `eq_rebound_threshold` | rebound threshold that erases simple net removal | `rebound_threshold = (gross_removal - residual_emissions) / gross_removal` | derived calculation from emissions baseline and target | `analysis/tables/aether_jevons_rebound_sensitivity.csv` |
| `eq_air_contactor_area` | air-contactor face-area scale | `area = CO2_flow / (air_CO2_concentration * capture_fraction * face_velocity * uptime)` | source-backed engineering relation plus derived model output | `analysis/tables/aether_air_contactor_scale.csv` |

## Unit Checks

| Check | Calculated | Expected | Tolerance | Unit | Status |
|---|---:|---:|---:|---|---|
| 100 GtCO2/year atmosphere-only ppm equivalent | 12.821 | 12.82 | 0.02 | ppm/year | pass |
| 100 GtCO2/year at 3 GJ/tCO2 | 83333.333 | 83333.33 | 1 | TWh/year | pass |
| 100 GtCO2/year at 1 GJ/tCO2 | 27777.778 | 27777.78 | 1 | TWh/year | pass |
| 100 GtCO2/year ideal splitting floor | 248333.333 | 248333.33 | 5 | TWh/year | pass |
| 100 GtCO2/year as supercritical CO2 at 600 kg/m3 | 166.667 | 166.67 | 0.2 | km3/year | pass |
| solid carbon from splitting 100 GtCO2/year | 27.292 | 27.3 | 0.1 | Gt carbon/year | pass |
| oxygen coproduct from splitting 100 GtCO2/year | 72.707 | 72.7 | 0.1 | Gt O2/year | pass |
| U.S. 3,000 GtCO2 storage anchor at 54 GtCO2/year | 55.556 | 55.56 | 0.1 | years | pass |
| 54 GtCO2/year at one MtCO2/year per well before pressure multiplier | 54000 | 54000 | 1 | well equivalents | pass |
| all-air NASEM-reference contactor face area | 3771 | 3771 | 2 | km2 | pass |

## Reproducibility Rule

The equation ledger is not a substitute for the full models. It is the audit layer between the paper and the models. If the manuscript states a headline number, it should be traceable to one of three things:

1. A source-backed anchor in `references/source-register.md`.
2. A derived equation in `analysis/tables/aether_model_equation_ledger.csv`.
3. A scenario model output in `analysis/tables/` with assumptions visible in the corresponding `analysis/scenario-models/` script.

The current unit checks all pass. That does not prove AETHER is feasible. It proves the main unit transformations are at least explicit enough to be challenged.

