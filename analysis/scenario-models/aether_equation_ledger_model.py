"""AETHER equation ledger and unit-check model.

This script collects the main first-order equations used across the AETHER
working paper and writes a small unit-check table. The goal is not to replace
the scenario models. The goal is to make the arithmetic auditable enough that
a reviewer can see which quantities are source-backed, which are derived, and
which remain scenario assumptions.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analysis" / "tables"
OUT.mkdir(parents=True, exist_ok=True)

PPM_TO_GTCO2 = 7.8
TWH_PER_GJ_PER_TON_FOR_1_GT = 277.77777777777777
CO2_SPLITTING_GJ_T = 8.94
CO2_MOLAR_MASS = 44.0095
CARBON_MOLAR_MASS = 12.011
O2_MOLAR_MASS = 31.998
SUPERCRITICAL_CO2_DENSITY_KG_M3 = 600.0
AIR_CONTACTOR_REFERENCE_KM2 = 3771.0
USGS_US_STORAGE_GT = 3000.0
GEOLOGIC_STORAGE_TARGET_GT_Y = 54.0


def equation_rows() -> list[dict[str, str]]:
    return [
        {
            "equation_id": "eq_ppm_equivalent",
            "paper_quantity": "atmosphere-only ppm-equivalent gross drawdown",
            "equation": "ppm_equivalent = gross_removal_GtCO2_y / 7.8",
            "inputs": "gross_removal_GtCO2_y; ppm_to_GtCO2",
            "outputs": "ppm/year",
            "evidence_class": "derived calculation from carbon-cycle bookkeeping convention",
            "source_keys": "standard_atmosphere_conversion",
            "artifact": "analysis/tables/aether_scenario_summary.csv",
            "reviewer_note": "This is air-stock arithmetic, not a carbon-cycle outcome.",
        },
        {
            "equation_id": "eq_net_before_rebound",
            "paper_quantity": "simple net removal before rebound",
            "equation": "net_removal = gross_removal - residual_emissions",
            "inputs": "gross_removal_GtCO2_y; residual_emissions_GtCO2_y",
            "outputs": "GtCO2/year",
            "evidence_class": "derived calculation from source-backed emissions baseline plus scenario target",
            "source_keys": "global_carbon_budget_2025",
            "artifact": "analysis/tables/aether_scenario_summary.csv",
            "reviewer_note": "This ignores rebound, lifecycle emissions, and land/ocean carbon-cycle response.",
        },
        {
            "equation_id": "eq_energy_twh",
            "paper_quantity": "annual electricity or heat-equivalent energy",
            "equation": "TWh_y = GtCO2_y * GJ_per_tCO2 * 277.7777778",
            "inputs": "GtCO2_y; GJ_per_tCO2",
            "outputs": "TWh/year",
            "evidence_class": "unit conversion",
            "source_keys": "ipcc_ar6_wg3_ch12",
            "artifact": "analysis/tables/aether_scenario_summary.csv",
            "reviewer_note": "Energy form matters; final versions should separate electricity, heat, compression, transport, and storage work.",
        },
        {
            "equation_id": "eq_average_power",
            "paper_quantity": "average continuous power",
            "equation": "TW_average = TWh_y / 8760",
            "inputs": "TWh_y; hours_per_year",
            "outputs": "TW",
            "evidence_class": "unit conversion",
            "source_keys": "aether_model_assumptions_2026",
            "artifact": "analysis/tables/aether_scenario_summary.csv",
            "reviewer_note": "Average power does not solve capacity factor, dispatch, transmission, or firming.",
        },
        {
            "equation_id": "eq_co2_splitting_energy",
            "paper_quantity": "ideal CO2 splitting energy floor",
            "equation": "splitting_TWh_y = GtCO2_y * 8.94_GJ_tCO2 * 277.7777778",
            "inputs": "GtCO2_y; CO2 formation enthalpy; CO2 molar mass",
            "outputs": "TWh/year",
            "evidence_class": "source-backed plus derived thermodynamic calculation",
            "source_keys": "nist_chemistry_webbook_co2;nist_chemistry_webbook_co2_calculated",
            "artifact": "analysis/tables/aether_splitting_fraction_sensitivity.csv",
            "reviewer_note": "This is an ideal enthalpy floor before real electrochemical losses and product handling.",
        },
        {
            "equation_id": "eq_supercritical_volume",
            "paper_quantity": "supercritical CO2 storage volume",
            "equation": "volume_km3_y = GtCO2_y * 1e12 / density_kg_m3 / 1e9",
            "inputs": "GtCO2_y; density_kg_m3",
            "outputs": "km3/year",
            "evidence_class": "source-backed plus derived storage-state calculation",
            "source_keys": "national_academies_net_reliable_sequestration;nist_thermophysical_fluids_2009",
            "artifact": "analysis/tables/aether_conversion_state_ledger.csv",
            "reviewer_note": "Dense volume does not imply injectivity, pressure capacity, legal access, or monitoring readiness.",
        },
        {
            "equation_id": "eq_solid_carbon_mass",
            "paper_quantity": "solid carbon mass from complete CO2 splitting",
            "equation": "carbon_Gt_y = CO2_Gt_y * carbon_molar_mass / CO2_molar_mass",
            "inputs": "CO2_Gt_y; molar masses",
            "outputs": "Gt carbon/year",
            "evidence_class": "stoichiometric calculation",
            "source_keys": "nist_chemistry_webbook_co2;osha_graphite_natural_chemicaldata_2020;usgs_graphite_mcs_2026",
            "artifact": "analysis/tables/aether_conversion_state_ledger.csv",
            "reviewer_note": "Useful for scale comparison; it is not a claim that solid-carbon storage is economically preferred.",
        },
        {
            "equation_id": "eq_o2_coproduct_mass",
            "paper_quantity": "oxygen coproduct mass from complete CO2 splitting",
            "equation": "oxygen_Gt_y = CO2_Gt_y * oxygen_molar_mass / CO2_molar_mass",
            "inputs": "CO2_Gt_y; molar masses",
            "outputs": "Gt O2/year",
            "evidence_class": "stoichiometric calculation",
            "source_keys": "nist_chemistry_webbook_co2;nist_cryogenic_fluid_properties",
            "artifact": "analysis/tables/aether_conversion_state_ledger.csv",
            "reviewer_note": "O2 coproduct handling becomes an industrial safety and market problem at full-splitting scale.",
        },
        {
            "equation_id": "eq_durable_credit",
            "paper_quantity": "100-year durable credited removal",
            "equation": "durable_credit = gross * (1 - lifecycle_penalty) * (1 - annual_reversal_rate) ** 100",
            "inputs": "gross_GtCO2_y; lifecycle_penalty; annual_reversal_rate",
            "outputs": "GtCO2/year credited over 100 years",
            "evidence_class": "scenario assumption and derived model output",
            "source_keys": "ipcc_ar6_wg3_ch6_ccs_storage;usgs_anderson_storage_risk_liability_2017",
            "artifact": "analysis/tables/aether_storage_lifecycle_routes.csv",
            "reviewer_note": "The formula is explicit; the current penalty and reversal rates are assumptions needing pathway-specific LCA and MRV evidence.",
        },
        {
            "equation_id": "eq_geologic_well_equivalents",
            "paper_quantity": "geologic injection well-equivalent count",
            "equation": "wells = geologic_GtCO2_y * 1000 / well_productivity_MtCO2_y",
            "inputs": "geologic_GtCO2_y; well_productivity_MtCO2_y",
            "outputs": "well equivalents",
            "evidence_class": "scenario assumption and derived model output",
            "source_keys": "epa_class_vi_wells_2026;epa_current_class_vi_projects_2026",
            "artifact": "analysis/tables/aether_injection_corridor_requirements.csv",
            "reviewer_note": "A well-equivalent is not a permit-ready design; reservoir productivity and pressure management dominate.",
        },
        {
            "equation_id": "eq_storage_capacity_years",
            "paper_quantity": "capacity years at assigned storage throughput",
            "equation": "capacity_years = proxy_capacity_GtCO2 / assigned_injection_GtCO2_y",
            "inputs": "proxy_capacity_GtCO2; assigned_injection_GtCO2_y",
            "outputs": "years",
            "evidence_class": "source-backed anchor plus scenario allocation",
            "source_keys": "usgs_circular_1386_geologic_storage;netl_carbon_storage_atlas_v_2015",
            "artifact": "analysis/tables/aether_regional_storage_allocation.csv",
            "reviewer_note": "Capacity years are a screening metric; they do not prove usable pore space or public acceptance.",
        },
        {
            "equation_id": "eq_robot_hour_cost",
            "paper_quantity": "direct robot-hour cost",
            "equation": "robot_hour_cost = unit_cost * (1 + maintenance_fraction) / (lifetime_years * utilization_hours_y)",
            "inputs": "unit_cost; maintenance_fraction; lifetime_years; utilization_hours_y",
            "outputs": "USD/robot-hour",
            "evidence_class": "scenario assumption and derived calculation",
            "source_keys": "unitree_g1_product_2026;ifr_world_robotics_2025;figure_botq_2025;agility_robofab_2023",
            "artifact": "analysis/tables/aether_robot_labor_costs.csv",
            "reviewer_note": "Cheap robot-hours do not imply high autonomous task productivity.",
        },
        {
            "equation_id": "eq_learning_curve",
            "paper_quantity": "learning-curve cost decline",
            "equation": "cost = max(floor_cost, initial_cost * (1 - learning_rate) ** doublings)",
            "inputs": "initial_cost; learning_rate; capacity_doublings; floor_cost",
            "outputs": "USD/tCO2",
            "evidence_class": "scenario assumption grounded in learning-curve literature",
            "source_keys": "wright_1936_learning_curve;thompson_2012_learning_by_doing",
            "artifact": "analysis/tables/aether_learning_curve_costs.csv",
            "reviewer_note": "Learning-curve math should not be confused with a proof that the required deployment will occur.",
        },
        {
            "equation_id": "eq_rebound_threshold",
            "paper_quantity": "rebound threshold that erases simple net removal",
            "equation": "rebound_threshold = (gross_removal - residual_emissions) / gross_removal",
            "inputs": "gross_removal_GtCO2_y; residual_emissions_GtCO2_y",
            "outputs": "fraction",
            "evidence_class": "derived calculation from emissions baseline and target",
            "source_keys": "sorrell_2009_jevons_rebound;alcott_2005_jevons_paradox;global_carbon_budget_2025",
            "artifact": "analysis/tables/aether_jevons_rebound_sensitivity.csv",
            "reviewer_note": "This is a policy-behavior threshold, not an empirical rebound forecast.",
        },
        {
            "equation_id": "eq_air_contactor_area",
            "paper_quantity": "air-contactor face-area scale",
            "equation": "area = CO2_flow / (air_CO2_concentration * capture_fraction * face_velocity * uptime)",
            "inputs": "CO2_flow; atmospheric_CO2; capture_fraction; face_velocity; uptime",
            "outputs": "m2 or km2",
            "evidence_class": "source-backed engineering relation plus derived model output",
            "source_keys": "national_academies_dac_ch5_2018;noaa_gml_global_co2_2026",
            "artifact": "analysis/tables/aether_air_contactor_scale.csv",
            "reviewer_note": "Contactor area is a hardware-scale proxy; pressure drop, fan work, and sorbent cycling remain separate constraints.",
        },
    ]


def unit_check_rows() -> list[dict[str, object]]:
    carbon_gt = 100.0 * CARBON_MOLAR_MASS / CO2_MOLAR_MASS
    oxygen_gt = 100.0 * O2_MOLAR_MASS / CO2_MOLAR_MASS
    checks = [
        {
            "check_id": "check_100gt_ppm",
            "quantity": "100 GtCO2/year atmosphere-only ppm equivalent",
            "calculated_value": 100.0 / PPM_TO_GTCO2,
            "expected_value": 12.82,
            "tolerance": 0.02,
            "unit": "ppm/year",
            "equation_id": "eq_ppm_equivalent",
        },
        {
            "check_id": "check_3gj_100gt_twh",
            "quantity": "100 GtCO2/year at 3 GJ/tCO2",
            "calculated_value": 100.0 * 3.0 * TWH_PER_GJ_PER_TON_FOR_1_GT,
            "expected_value": 83333.33,
            "tolerance": 1.0,
            "unit": "TWh/year",
            "equation_id": "eq_energy_twh",
        },
        {
            "check_id": "check_1gj_100gt_twh",
            "quantity": "100 GtCO2/year at 1 GJ/tCO2",
            "calculated_value": 100.0 * 1.0 * TWH_PER_GJ_PER_TON_FOR_1_GT,
            "expected_value": 27777.78,
            "tolerance": 1.0,
            "unit": "TWh/year",
            "equation_id": "eq_energy_twh",
        },
        {
            "check_id": "check_splitting_floor_twh",
            "quantity": "100 GtCO2/year ideal splitting floor",
            "calculated_value": 100.0
            * CO2_SPLITTING_GJ_T
            * TWH_PER_GJ_PER_TON_FOR_1_GT,
            "expected_value": 248333.33,
            "tolerance": 5.0,
            "unit": "TWh/year",
            "equation_id": "eq_co2_splitting_energy",
        },
        {
            "check_id": "check_supercritical_volume",
            "quantity": "100 GtCO2/year as supercritical CO2 at 600 kg/m3",
            "calculated_value": 100.0
            * 1e12
            / SUPERCRITICAL_CO2_DENSITY_KG_M3
            / 1e9,
            "expected_value": 166.67,
            "tolerance": 0.2,
            "unit": "km3/year",
            "equation_id": "eq_supercritical_volume",
        },
        {
            "check_id": "check_solid_carbon_mass",
            "quantity": "solid carbon from splitting 100 GtCO2/year",
            "calculated_value": carbon_gt,
            "expected_value": 27.3,
            "tolerance": 0.1,
            "unit": "Gt carbon/year",
            "equation_id": "eq_solid_carbon_mass",
        },
        {
            "check_id": "check_o2_mass",
            "quantity": "oxygen coproduct from splitting 100 GtCO2/year",
            "calculated_value": oxygen_gt,
            "expected_value": 72.7,
            "tolerance": 0.1,
            "unit": "Gt O2/year",
            "equation_id": "eq_o2_coproduct_mass",
        },
        {
            "check_id": "check_storage_capacity_years",
            "quantity": "U.S. 3,000 GtCO2 storage anchor at 54 GtCO2/year",
            "calculated_value": USGS_US_STORAGE_GT / GEOLOGIC_STORAGE_TARGET_GT_Y,
            "expected_value": 55.56,
            "tolerance": 0.1,
            "unit": "years",
            "equation_id": "eq_storage_capacity_years",
        },
        {
            "check_id": "check_one_mt_wells",
            "quantity": "54 GtCO2/year at one MtCO2/year per well before pressure multiplier",
            "calculated_value": GEOLOGIC_STORAGE_TARGET_GT_Y * 1000.0,
            "expected_value": 54000.0,
            "tolerance": 1.0,
            "unit": "well equivalents",
            "equation_id": "eq_geologic_well_equivalents",
        },
        {
            "check_id": "check_all_air_contactor_reference",
            "quantity": "all-air NASEM-reference contactor face area",
            "calculated_value": AIR_CONTACTOR_REFERENCE_KM2,
            "expected_value": 3771.0,
            "tolerance": 2.0,
            "unit": "km2",
            "equation_id": "eq_air_contactor_area",
        },
    ]
    for check in checks:
        delta = abs(check["calculated_value"] - check["expected_value"])
        check["absolute_error"] = delta
        check["pass"] = delta <= check["tolerance"]
    return checks


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"Cannot write empty CSV: {path}")
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {path}")


def main() -> None:
    equations = equation_rows()
    checks = unit_check_rows()
    if not all(row["pass"] for row in checks):
        failed = [row["check_id"] for row in checks if not row["pass"]]
        raise RuntimeError(f"Unit checks failed: {failed}")
    write_csv(OUT / "aether_model_equation_ledger.csv", equations)
    write_csv(OUT / "aether_dimensioned_unit_checks.csv", checks)


if __name__ == "__main__":
    main()

