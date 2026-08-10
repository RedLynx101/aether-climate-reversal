from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analysis" / "tables"
OUT.mkdir(parents=True, exist_ok=True)

TARGET_GT = 100.0
TARGET_MT = TARGET_GT * 1000
CURRENT_TOTAL_EMISSIONS_GT = 42.2
CURRENT_NOVEL_CDR_GT = 0.00204
PPM_GTCO2 = 7.8
YEARS = 20
IFR_2024_INDUSTRIAL_ROBOT_INSTALLS = 542_076
FIGURE_250_PER_MONTH_LEAD_ANNUALIZED = 250 * 12


def write_csv(name: str, rows: list[dict[str, object]]) -> None:
    path = OUT / name
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def energy_floor_usd_t(energy_gj_t: float, power_usd_mwh: float) -> float:
    # 1 GJ = 277.777... kWh = 0.277777... MWh.
    return energy_gj_t * 0.2777777777777778 * power_usd_mwh


def learning_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    initial_cost = 500.0
    floor_storage_mrv_usd_t = 12.0
    capture_energy_gj_t = 3.0
    doublings = math.log(TARGET_GT / CURRENT_NOVEL_CDR_GT, 2)
    for lr in [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40]:
        raw = initial_cost * ((1 - lr) ** doublings)
        for power_price in [10, 20, 30]:
            floor = energy_floor_usd_t(capture_energy_gj_t, power_price) + floor_storage_mrv_usd_t
            bounded = max(raw, floor)
            rows.append({
                "learning_rate_per_capacity_doubling": lr,
                "initial_engineered_cdr_capacity_gt_y": CURRENT_NOVEL_CDR_GT,
                "target_capacity_gt_y": TARGET_GT,
                "capacity_doublings_to_target": doublings,
                "initial_cost_usd_t": initial_cost,
                "raw_learned_cost_usd_t": raw,
                "capture_energy_gj_t": capture_energy_gj_t,
                "power_price_usd_mwh": power_price,
                "energy_plus_storage_mrv_floor_usd_t": floor,
                "bounded_cost_usd_t": bounded,
                "annual_cost_at_100gt_trillion_usd": bounded * TARGET_GT * 1e9 / 1e12,
            })
    return rows


def rebound_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for rebound in [0.00, 0.10, 0.25, 0.50, 0.578, 0.75, 1.00]:
        induced_or_delayed_emissions = TARGET_GT * rebound
        net = TARGET_GT - CURRENT_TOTAL_EMISSIONS_GT - induced_or_delayed_emissions
        rows.append({
            "gross_removal_gtco2_y": TARGET_GT,
            "current_emissions_gtco2_y": CURRENT_TOTAL_EMISSIONS_GT,
            "jevons_or_policy_rebound_fraction_of_gross_removal": rebound,
            "induced_or_delayed_emissions_gtco2_y": induced_or_delayed_emissions,
            "net_removal_gtco2_y": net,
            "simple_ppm_y": net / PPM_GTCO2,
            "interpretation": "net-negative" if net > 0 else ("break-even" if abs(net) < 1e-9 else "net-positive"),
        })
    return rows


def scale_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for plant_size in [1, 5, 10, 25, 100]:
        plant_count = TARGET_MT / plant_size
        for alpha in [0.65, 0.75, 0.85, 0.95]:
            unit_capex_multiplier = plant_size ** (alpha - 1)
            rows.append({
                "plant_size_mtco2_y": plant_size,
                "plant_count_for_100gt_y": plant_count,
                "capex_scaling_exponent_alpha": alpha,
                "relative_unit_capex_vs_1mt_plant": unit_capex_multiplier,
                "unit_capex_reduction_percent_vs_1mt": (1 - unit_capex_multiplier) * 100,
            })
    return rows


def robot_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for robots_per_mt in [10, 25, 50, 100, 250, 500, 1000]:
        fleet = robots_per_mt * TARGET_MT
        annual = fleet / YEARS
        rows.append({
            "robots_per_mtco2_y_capacity_assumption": robots_per_mt,
            "target_capacity_mtco2_y": TARGET_MT,
            "implied_aether_robot_fleet": fleet,
            "annual_robot_production_over_20y": annual,
            "multiple_of_ifr_2024_industrial_robot_installations": annual / IFR_2024_INDUSTRIAL_ROBOT_INSTALLS,
            "multiple_of_figure_250_per_month_lead_annualized": annual / FIGURE_250_PER_MONTH_LEAD_ANNUALIZED,
            "figure_250_per_month_lead_annualized": FIGURE_250_PER_MONTH_LEAD_ANNUALIZED,
        })
    return rows


def buildout_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    cagr = (TARGET_GT / CURRENT_NOVEL_CDR_GT) ** (1 / YEARS) - 1
    linear_addition = TARGET_GT / YEARS
    for year_index in range(YEARS + 1):
        year = 2026 + year_index
        exponential_capacity = CURRENT_NOVEL_CDR_GT * ((1 + cagr) ** year_index)
        linear_capacity = linear_addition * year_index
        rows.append({
            "year": year,
            "years_from_2026": year_index,
            "exponential_capacity_gtco2_y_from_current_novel_cdr": exponential_capacity,
            "required_exponential_cagr": cagr,
            "linear_capacity_gtco2_y_to_100gt_by_2046": linear_capacity,
            "linear_new_capacity_addition_gtco2_y_per_year": linear_addition,
            "linear_energy_twh_y_at_3gj_t": linear_capacity * 3.0 * 277.77777777777777,
            "linear_average_power_tw_at_3gj_t": (linear_capacity * 3.0 * 277.77777777777777) / 8760,
        })
    return rows


def main() -> None:
    write_csv("aether_learning_curve_costs.csv", learning_rows())
    write_csv("aether_jevons_rebound_sensitivity.csv", rebound_rows())
    write_csv("aether_economies_of_scale.csv", scale_rows())
    write_csv("aether_robot_fleet_requirements.csv", robot_rows())
    write_csv("aether_20y_buildout_pathways.csv", buildout_rows())
    for name in [
        "aether_learning_curve_costs.csv",
        "aether_jevons_rebound_sensitivity.csv",
        "aether_economies_of_scale.csv",
        "aether_robot_fleet_requirements.csv",
        "aether_20y_buildout_pathways.csv",
    ]:
        print(f"Wrote {OUT / name}")


if __name__ == "__main__":
    main()
