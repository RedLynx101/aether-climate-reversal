from __future__ import annotations

"""AETHER deployment timepath model.

This Python file mirrors the generated CSV layer used by the AETHER sync
scripts. It is intentionally simple: it turns explicit scenario assumptions
about capacity ramps, clean-energy allocation, robot supply, storage, budgets,
durable-credit haircuts, residual emissions, and rebound into annual deployment
paths. The outputs are scenario screens, not forecasts.
"""

from dataclasses import dataclass
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analysis" / "tables"
START_YEAR = 2026
END_YEAR = 2060
TARGET_GT = 100.0
CURRENT_NOVEL_CDR_GT_Y = 0.00204
TWH_PER_GJ_PER_GT = 277.77777777777777
BASE_CLEAN_ADDITION_TWH_Y = 850.0
BASE_ROBOT_OUTPUT_Y = 542_076.0
ROBOT_SERVICE_LIFE_Y = 8


@dataclass(frozen=True)
class Scenario:
    scenario: str
    display_name: str
    interpretation: str
    target_year: int
    ramp_exponent: float
    energy_gj_tco2: float
    clean_growth: float
    aether_clean_share: float
    robot_growth: float
    aether_robot_share: float
    robots_per_mtco2_y: float
    storage_terminal_gtco2_y: float
    storage_ramp_exponent: float
    annual_budget_trillion_usd: float
    initial_cost_usd_tco2: float
    learning_rate: float
    floor_cost_usd_tco2: float
    durable_fraction: float
    emissions_2046_gtco2_y: float
    emissions_2050_gtco2_y: float
    emissions_2060_gtco2_y: float
    rebound_fraction: float


def scenarios() -> list[Scenario]:
    return [
        Scenario("linear_reference_2046", "Linear 2046 reference", "Straight 20-year ramp with strong but bounded assumptions.", 2046, 1.0, 3.0, 0.15, 0.55, 0.25, 0.35, 50.0, 105.0, 1.05, 9.0, 300.0, 0.22, 84.0, 0.849, 15.0, 8.0, 2.0, 0.15),
        Scenario("s_curve_industrialization", "S-curve industrialization", "Slower early ramp, faster after factories and automation compound.", 2046, 2.0, 2.4, 0.16, 0.58, 0.27, 0.38, 45.0, 110.0, 1.20, 9.5, 300.0, 0.23, 76.0, 0.86, 12.0, 5.0, 1.0, 0.12),
        Scenario("abundance_acceleration_2040", "Abundance acceleration 2040", "Optimistic automation and clean-energy case reaching 100 Gt/year earlier.", 2040, 1.35, 1.8, 0.18, 0.55, 0.30, 0.40, 30.0, 125.0, 0.95, 8.0, 260.0, 0.27, 45.0, 0.90, 7.0, 2.0, 0.0, 0.05),
        Scenario("energy_delayed", "Energy-delayed buildout", "Robotics improves, but dedicated clean energy and firm power arrive too slowly.", 2046, 1.0, 3.0, 0.10, 0.28, 0.25, 0.35, 50.0, 100.0, 1.05, 9.0, 300.0, 0.22, 84.0, 0.849, 18.0, 10.0, 3.0, 0.15),
        Scenario("rebound_failure", "Rebound failure", "Physical buildout mostly works, but governance fails and rebound is too high.", 2046, 1.0, 2.4, 0.16, 0.58, 0.27, 0.38, 45.0, 110.0, 1.05, 9.5, 300.0, 0.23, 76.0, 0.86, 30.0, 28.0, 18.0, 0.58),
    ]


def ramp_progress(year: int, target_year: int, exponent: float) -> float:
    if year <= START_YEAR:
        return 0.0
    if year >= target_year:
        return 1.0
    return ((year - START_YEAR) / (target_year - START_YEAR)) ** exponent


def clean_generation_stock(year_index: int, growth: float, share: float) -> float:
    return sum(BASE_CLEAN_ADDITION_TWH_Y * ((1 + growth) ** i) for i in range(year_index + 1)) * share


def robots_in_service(year_index: int, growth: float, share: float) -> float:
    start = max(0, year_index - ROBOT_SERVICE_LIFE_Y + 1)
    return sum(BASE_ROBOT_OUTPUT_Y * ((1 + growth) ** i) * share for i in range(start, year_index + 1))


def learned_cost(capacity_gt_y: float, initial_cost: float, learning_rate: float, floor_cost: float) -> float:
    capacity = max(capacity_gt_y, CURRENT_NOVEL_CDR_GT_Y)
    doublings = math.log(capacity / CURRENT_NOVEL_CDR_GT_Y, 2)
    raw = initial_cost * ((1 - learning_rate) ** doublings)
    return max(floor_cost, raw)


def emissions_path(year: int, s: Scenario) -> float:
    if year <= 2046:
        p = (year - 2026) / 20
        return 42.2 + (s.emissions_2046_gtco2_y - 42.2) * p
    if year <= 2050:
        p = (year - 2046) / 4
        return s.emissions_2046_gtco2_y + (s.emissions_2050_gtco2_y - s.emissions_2046_gtco2_y) * p
    p = min(1.0, (year - 2050) / 10)
    return s.emissions_2050_gtco2_y + (s.emissions_2060_gtco2_y - s.emissions_2050_gtco2_y) * p


def build_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for s in scenarios():
        cumulative_gross = cumulative_durable = cumulative_net = cumulative_energy = cumulative_cost = 0.0
        for year in range(START_YEAR, END_YEAR + 1):
            i = year - START_YEAR
            progress = ramp_progress(year, s.target_year, s.ramp_exponent)
            planned = TARGET_GT * progress
            cost = learned_cost(max(planned, CURRENT_NOVEL_CDR_GT_Y), s.initial_cost_usd_tco2, s.learning_rate, s.floor_cost_usd_tco2)
            clean_twh = clean_generation_stock(i, s.clean_growth, s.aether_clean_share)
            energy_cap = clean_twh / (s.energy_gj_tco2 * TWH_PER_GJ_PER_GT)
            robots = robots_in_service(i, s.robot_growth, s.aether_robot_share)
            robot_cap = robots / (s.robots_per_mtco2_y * 1000)
            storage_cap = s.storage_terminal_gtco2_y * (max(progress, 0.0) ** s.storage_ramp_exponent)
            budget_cap = s.annual_budget_trillion_usd * 1000 / cost
            actual = min(planned, energy_cap, robot_cap, storage_cap, budget_cap)
            durable = actual * s.durable_fraction
            emissions = emissions_path(year, s)
            rebound = actual * s.rebound_fraction
            net = durable - emissions - rebound
            energy_twh = actual * s.energy_gj_tco2 * TWH_PER_GJ_PER_GT
            annual_cost = actual * cost / 1000
            cumulative_gross += actual
            cumulative_durable += durable
            cumulative_net += net
            cumulative_energy += energy_twh
            cumulative_cost += annual_cost
            rows.append({
                "scenario": s.scenario,
                "display_name": s.display_name,
                "year": year,
                "planned_capacity_gtco2_y": planned,
                "actual_gross_removal_gtco2_y": actual,
                "durable_credit_gtco2_y": durable,
                "net_after_emissions_rebound_gtco2_y": net,
                "cumulative_gross_removal_gtco2": cumulative_gross,
                "cumulative_durable_credit_gtco2": cumulative_durable,
                "cumulative_net_after_emissions_rebound_gtco2": cumulative_net,
                "energy_twh_y": energy_twh,
                "average_power_tw": energy_twh / 8760,
                "annual_cost_trillion_usd": annual_cost,
                "scenario_interpretation": s.interpretation,
            })
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    rows = build_rows()
    write_csv(OUT / "aether_deployment_timepath_annual.csv", rows)
    print(f"Wrote {OUT / 'aether_deployment_timepath_annual.csv'}")

