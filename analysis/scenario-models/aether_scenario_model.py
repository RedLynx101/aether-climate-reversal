from __future__ import annotations

from dataclasses import dataclass
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_TABLES = ROOT / "analysis" / "tables"
OUT_TABLES.mkdir(parents=True, exist_ok=True)

GT = 1e9  # metric tons per gigatonne
KG_PER_GT = 1e12
TWH_PER_GJ_PER_TON_FOR_1_GT = 277.77777777777777  # 1 GJ/t * 1 Gt = 277.78 TWh
HOURS_PER_YEAR = 8760

@dataclass(frozen=True)
class Scenario:
    name: str
    removal_gtco2_y: float
    gross_emissions_gtco2_y: float
    capture_energy_gj_t: float
    split_fraction: float
    capture_cost_usd_t: float
    storage_cost_usd_t: float
    mrv_cost_usd_t: float
    capex_usd_per_tpa: float
    plant_size_mt_y: float
    robot_unit_cost_usd: float
    robot_life_y: float
    robot_hours_y: float
    robot_maintenance_frac_y: float


def co2_split_energy_gj_t() -> float:
    # NIST: enthalpy of formation of CO2(g) = -393.51 kJ/mol.
    # Splitting CO2 -> C + O2 requires the reverse enthalpy.
    kj_per_mol = 393.51
    kg_per_mol = 0.0440095
    return kj_per_mol / kg_per_mol / 1_000  # kJ/kg = MJ/kg; /1000 = GJ/t


def air_mass_ratio_at_ppm(ppm: float) -> float:
    # Convert dry-air molar ppm to CO2 mass fraction using MW CO2 / MW dry air.
    mol_fraction = ppm / 1_000_000
    mass_fraction = mol_fraction * (44.0095 / 28.9652)
    return 1 / mass_fraction


def scenario_row(s: Scenario) -> dict[str, float | str]:
    split_gj_t = co2_split_energy_gj_t() * s.split_fraction
    energy_gj_t = s.capture_energy_gj_t + split_gj_t
    energy_twh_y = energy_gj_t * s.removal_gtco2_y * TWH_PER_GJ_PER_TON_FOR_1_GT
    avg_tw = energy_twh_y / HOURS_PER_YEAR
    gross_ppm_y = s.removal_gtco2_y / 7.8
    net_gt_y = s.removal_gtco2_y - s.gross_emissions_gtco2_y
    net_ppm_y_simple = net_gt_y / 7.8
    o2_gt_y = s.removal_gtco2_y * (32 / 44)
    carbon_gt_y = s.removal_gtco2_y * (12 / 44)
    solid_carbon_km3_y = carbon_gt_y * KG_PER_GT / 2200 / 1e9
    supercritical_co2_km3_y = s.removal_gtco2_y * KG_PER_GT / 600 / 1e9
    co2_gas_stp_km3_y = s.removal_gtco2_y * KG_PER_GT / 1.98 / 1e9
    liquid_o2_km3_y = o2_gt_y * KG_PER_GT / 1141 / 1e9
    annual_opex_trillion = s.removal_gtco2_y * GT * (s.capture_cost_usd_t + s.storage_cost_usd_t + s.mrv_cost_usd_t) / 1e12
    capex_trillion = s.removal_gtco2_y * GT * s.capex_usd_per_tpa / 1e12
    plants = s.removal_gtco2_y * 1000 / s.plant_size_mt_y
    robot_hour_cost = (s.robot_unit_cost_usd / s.robot_life_y + s.robot_unit_cost_usd * s.robot_maintenance_frac_y) / s.robot_hours_y
    air_tonnes_per_tco2 = air_mass_ratio_at_ppm(428)
    air_mass_gt_y = s.removal_gtco2_y * air_tonnes_per_tco2
    air_volume_km3_y = air_mass_gt_y * KG_PER_GT / 1.2 / 1e9
    average_air_throughput_m3_s = air_volume_km3_y * 1e9 / (HOURS_PER_YEAR * 3600)
    air_flow_per_configured_plant_m3_s = average_air_throughput_m3_s / plants
    return {
        "scenario": s.name,
        "removal_gtco2_y": s.removal_gtco2_y,
        "gross_emissions_gtco2_y": s.gross_emissions_gtco2_y,
        "net_removal_after_current_emissions_gtco2_y": net_gt_y,
        "gross_ppm_drawdown_simple_ppm_y": gross_ppm_y,
        "net_ppm_drawdown_simple_ppm_y": net_ppm_y_simple,
        "capture_energy_gj_t": s.capture_energy_gj_t,
        "split_fraction": s.split_fraction,
        "split_energy_gj_t": split_gj_t,
        "total_energy_gj_t": energy_gj_t,
        "total_energy_twh_y": energy_twh_y,
        "average_power_tw": avg_tw,
        "annual_opex_trillion_usd": annual_opex_trillion,
        "capex_capacity_trillion_usd": capex_trillion,
        "one_mt_y_plants_equivalent": s.removal_gtco2_y * 1000,
        "plants_at_configured_size": plants,
        "configured_plant_size_mt_y": s.plant_size_mt_y,
        "carbon_product_gt_y_if_split": carbon_gt_y * s.split_fraction,
        "oxygen_product_gt_y_if_split": o2_gt_y * s.split_fraction,
        "solid_carbon_volume_km3_y_if_split": solid_carbon_km3_y * s.split_fraction,
        "liquid_o2_volume_km3_y_if_split": liquid_o2_km3_y * s.split_fraction,
        "supercritical_co2_storage_km3_y_unsplit": supercritical_co2_km3_y * (1 - s.split_fraction),
        "co2_gas_stp_volume_km3_y_unsplit": co2_gas_stp_km3_y * (1 - s.split_fraction),
        "air_mass_processed_gt_y_at_428ppm": air_mass_gt_y,
        "air_volume_processed_km3_y_at_428ppm": air_volume_km3_y,
        "average_air_throughput_m3_s_at_428ppm": average_air_throughput_m3_s,
        "air_flow_per_configured_plant_m3_s_at_428ppm": air_flow_per_configured_plant_m3_s,
        "robot_unit_cost_usd": s.robot_unit_cost_usd,
        "effective_robot_hour_cost_usd": robot_hour_cost,
    }


def write_csv(name: str, rows: list[dict[str, float | str]]) -> None:
    path = OUT_TABLES / name
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    scenarios = [
        Scenario("current_DAC_like_100Gt", 100, 42.2, 8.0, 0.0, 500, 20, 5, 1200, 1, 100_000, 7, 5000, 0.12),
        Scenario("advanced_capture_storage_100Gt", 100, 42.2, 3.0, 0.0, 75, 12, 3, 400, 10, 50_000, 7, 6000, 0.10),
        Scenario("near_thermo_capture_storage_100Gt", 100, 42.2, 1.0, 0.0, 25, 8, 2, 150, 25, 25_000, 8, 7000, 0.08),
        Scenario("advanced_capture_25pct_split_100Gt", 100, 42.2, 3.0, 0.25, 90, 10, 3, 550, 10, 50_000, 7, 6000, 0.10),
        Scenario("advanced_capture_100pct_split_100Gt", 100, 42.2, 3.0, 1.0, 130, 3, 4, 900, 10, 50_000, 7, 6000, 0.10),
        Scenario("portfolio_10Gt", 10, 42.2, 3.5, 0.0, 80, 12, 3, 500, 5, 50_000, 7, 6000, 0.10),
        Scenario("portfolio_30Gt", 30, 42.2, 3.2, 0.0, 70, 12, 3, 450, 10, 40_000, 7, 6000, 0.10),
        Scenario("portfolio_50Gt", 50, 42.2, 3.0, 0.0, 60, 12, 3, 400, 10, 35_000, 7, 6500, 0.09),
    ]
    rows = [scenario_row(s) for s in scenarios]
    write_csv("aether_scenario_summary.csv", rows)

    parameter_rows = [
        {"parameter": "Mauna Loa CO2 monthly mean, May 2026", "value": 432.34, "unit": "ppm", "source_key": "noaa_gml_mauna_loa_co2_2026"},
        {"parameter": "Global CO2 trend, Feb 2026", "value": 428.53, "unit": "ppm", "source_key": "noaa_gml_global_co2_2026"},
        {"parameter": "Fossil CO2 emissions, 2025", "value": 38.1, "unit": "GtCO2/yr", "source_key": "global_carbon_budget_2025"},
        {"parameter": "Total anthropogenic CO2 emissions, 2025 preliminary", "value": 42.2, "unit": "GtCO2/yr", "source_key": "global_carbon_budget_2025"},
        {"parameter": "Current global CDR, 2026", "value": 2.2, "unit": "GtCO2/yr", "source_key": "state_of_cdr_2026"},
        {"parameter": "Current novel CDR, 2025", "value": 0.00204, "unit": "GtCO2/yr", "source_key": "state_of_cdr_2026"},
        {"parameter": "DAC theoretical minimum separation energy", "value": 0.5, "unit": "GJ/tCO2", "source_key": "ipcc_ar6_wg3_ch12"},
        {"parameter": "DAC current technology total energy range low", "value": 4.0, "unit": "GJ/tCO2", "source_key": "ipcc_ar6_wg3_ch12"},
        {"parameter": "DAC current technology total energy range high", "value": 10.0, "unit": "GJ/tCO2", "source_key": "ipcc_ar6_wg3_ch12"},
        {"parameter": "CO2 formation enthalpy", "value": -393.51, "unit": "kJ/mol", "source_key": "nist_chemistry_webbook_co2"},
        {"parameter": "CO2 to C + O2 theoretical split energy", "value": co2_split_energy_gj_t(), "unit": "GJ/tCO2", "source_key": "nist_chemistry_webbook_co2_calculated"},
        {"parameter": "CO2 per atmospheric ppm", "value": 7.8, "unit": "GtCO2/ppm", "source_key": "standard_atmosphere_conversion"},
        {"parameter": "Supercritical CO2 density in geologic storage", "value": 600, "unit": "kg/m3", "source_key": "national_academies_net_reliable_sequestration"},
        {"parameter": "Industrial robot installations, 2024", "value": 542076, "unit": "robots", "source_key": "ifr_world_robotics_2025"},
        {"parameter": "Operational stock of industrial robots, 2024", "value": 4663698, "unit": "robots", "source_key": "ifr_world_robotics_2025"},
        {"parameter": "Solar PV generation increase, 2025", "value": 600, "unit": "TWh", "source_key": "iea_global_energy_review_2026"},
        {"parameter": "Global electricity generation increase, 2025", "value": 850, "unit": "TWh", "source_key": "iea_global_energy_review_2026"},
    ]
    write_csv("aether_parameter_table.csv", parameter_rows)

    print(f"Wrote {OUT_TABLES / 'aether_scenario_summary.csv'}")
    print(f"Wrote {OUT_TABLES / 'aether_parameter_table.csv'}")


if __name__ == "__main__":
    main()




