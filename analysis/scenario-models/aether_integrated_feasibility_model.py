from __future__ import annotations

from dataclasses import dataclass
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analysis" / "tables"
OUT.mkdir(parents=True, exist_ok=True)

START_YEAR = 2026
END_YEAR = 2046
YEARS = END_YEAR - START_YEAR
TARGET_GTCO2_Y = 100.0
CURRENT_NOVEL_CDR_GT_Y = 0.00204
BASE_CLEAN_ELECTRICITY_ADDITION_TWH_Y = 850.0
BASE_ROBOT_OUTPUT_Y = 542_076.0
TWH_PER_GJ_PER_TON_FOR_1_GT = 277.77777777777777
ROBOT_SERVICE_LIFE_Y = 8


@dataclass(frozen=True)
class FeasibilityScenario:
    key: str
    display_name: str
    description: str
    energy_gj_tco2: float
    initial_cost_usd_tco2: float
    floor_cost_usd_tco2: float
    learning_rate: float
    clean_addition_growth_rate: float
    aether_clean_share: float
    robot_output_growth_rate: float
    aether_robot_share: float
    robots_per_mtco2_y_capacity: float
    storage_terminal_gtco2_y: float
    storage_ramp_exponent: float
    annual_budget_trillion_usd: float
    emissions_2046_gtco2_y: float
    rebound_fraction_of_gross_removal: float


def scenarios() -> list[FeasibilityScenario]:
    return [
        FeasibilityScenario(
            key="reference_extrapolation",
            display_name="Reference extrapolation",
            description="Moderate learning, slow clean-energy growth, limited storage, and high rebound. Useful as the failure baseline.",
            energy_gj_tco2=6.0,
            initial_cost_usd_tco2=500.0,
            floor_cost_usd_tco2=180.0,
            learning_rate=0.10,
            clean_addition_growth_rate=0.06,
            aether_clean_share=0.15,
            robot_output_growth_rate=0.12,
            aether_robot_share=0.10,
            robots_per_mtco2_y_capacity=300,
            storage_terminal_gtco2_y=25,
            storage_ramp_exponent=1.45,
            annual_budget_trillion_usd=2.0,
            emissions_2046_gtco2_y=38.0,
            rebound_fraction_of_gross_removal=0.45,
        ),
        FeasibilityScenario(
            key="fast_learning_energy_constrained",
            display_name="Fast learning, energy constrained",
            description="Better automation and learning, but clean-energy allocation remains too small for 100 Gt/year.",
            energy_gj_tco2=3.0,
            initial_cost_usd_tco2=400.0,
            floor_cost_usd_tco2=90.0,
            learning_rate=0.18,
            clean_addition_growth_rate=0.10,
            aether_clean_share=0.30,
            robot_output_growth_rate=0.18,
            aether_robot_share=0.25,
            robots_per_mtco2_y_capacity=100,
            storage_terminal_gtco2_y=60,
            storage_ramp_exponent=1.25,
            annual_budget_trillion_usd=4.0,
            emissions_2046_gtco2_y=25.0,
            rebound_fraction_of_gross_removal=0.25,
        ),
        FeasibilityScenario(
            key="aether_portfolio_push",
            display_name="AETHER portfolio push",
            description="The current v0.5 portfolio cost and energy case, plus aggressive clean-energy allocation and contained rebound.",
            energy_gj_tco2=2.035,
            initial_cost_usd_tco2=300.0,
            floor_cost_usd_tco2=84.0,
            learning_rate=0.22,
            clean_addition_growth_rate=0.15,
            aether_clean_share=0.65,
            robot_output_growth_rate=0.25,
            aether_robot_share=0.35,
            robots_per_mtco2_y_capacity=50,
            storage_terminal_gtco2_y=105,
            storage_ramp_exponent=1.05,
            annual_budget_trillion_usd=9.0,
            emissions_2046_gtco2_y=15.0,
            rebound_fraction_of_gross_removal=0.15,
        ),
        FeasibilityScenario(
            key="moonshot_low_energy",
            display_name="Moonshot low-energy",
            description="Low energy intensity, very strong learning, fast robot manufacturing, strong emissions decline, and low rebound.",
            energy_gj_tco2=1.35,
            initial_cost_usd_tco2=250.0,
            floor_cost_usd_tco2=35.0,
            learning_rate=0.28,
            clean_addition_growth_rate=0.18,
            aether_clean_share=0.50,
            robot_output_growth_rate=0.30,
            aether_robot_share=0.35,
            robots_per_mtco2_y_capacity=25,
            storage_terminal_gtco2_y=120,
            storage_ramp_exponent=0.95,
            annual_budget_trillion_usd=6.0,
            emissions_2046_gtco2_y=5.0,
            rebound_fraction_of_gross_removal=0.05,
        ),
        FeasibilityScenario(
            key="rebound_failure",
            display_name="High-rebound failure",
            description="Physical buildout mostly works, but cheap removal induces enough emissions or delayed abatement to destroy most net-negative value.",
            energy_gj_tco2=2.035,
            initial_cost_usd_tco2=300.0,
            floor_cost_usd_tco2=84.0,
            learning_rate=0.22,
            clean_addition_growth_rate=0.15,
            aether_clean_share=0.65,
            robot_output_growth_rate=0.25,
            aether_robot_share=0.35,
            robots_per_mtco2_y_capacity=50,
            storage_terminal_gtco2_y=105,
            storage_ramp_exponent=1.05,
            annual_budget_trillion_usd=9.0,
            emissions_2046_gtco2_y=30.0,
            rebound_fraction_of_gross_removal=0.65,
        ),
    ]


def cumulative_clean_twh(s: FeasibilityScenario, year_index: int) -> float:
    return sum(
        BASE_CLEAN_ELECTRICITY_ADDITION_TWH_Y * ((1 + s.clean_addition_growth_rate) ** t)
        for t in range(year_index + 1)
    ) * s.aether_clean_share


def robots_in_service(s: FeasibilityScenario, year_index: int) -> float:
    start = max(0, year_index - ROBOT_SERVICE_LIFE_Y + 1)
    return sum(
        BASE_ROBOT_OUTPUT_Y * ((1 + s.robot_output_growth_rate) ** t) * s.aether_robot_share
        for t in range(start, year_index + 1)
    )


def learned_cost(s: FeasibilityScenario, planned_capacity_gt_y: float) -> float:
    capacity = max(planned_capacity_gt_y, CURRENT_NOVEL_CDR_GT_Y)
    doublings = math.log(capacity / CURRENT_NOVEL_CDR_GT_Y, 2)
    raw = s.initial_cost_usd_tco2 * ((1 - s.learning_rate) ** doublings)
    return max(s.floor_cost_usd_tco2, raw)


def capacity_limited_path(s: FeasibilityScenario) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for year in range(START_YEAR, END_YEAR + 1):
        i = year - START_YEAR
        progress = i / YEARS if YEARS else 1
        planned_capacity = TARGET_GTCO2_Y * progress
        cost = learned_cost(s, max(planned_capacity, CURRENT_NOVEL_CDR_GT_Y))
        clean_twh = cumulative_clean_twh(s, i)
        energy_capacity = clean_twh / (s.energy_gj_tco2 * TWH_PER_GJ_PER_TON_FOR_1_GT)
        available_robots = robots_in_service(s, i)
        robot_capacity = available_robots / (s.robots_per_mtco2_y_capacity * 1000)
        storage_capacity = s.storage_terminal_gtco2_y * (progress ** s.storage_ramp_exponent) if progress > 0 else 0.0
        budget_capacity = s.annual_budget_trillion_usd * 1000 / cost
        actual_capacity = min(planned_capacity, energy_capacity, robot_capacity, storage_capacity, budget_capacity)
        if actual_capacity <= 0:
            binding = "startup"
        else:
            candidates = {
                "planned_target": planned_capacity,
                "clean_energy": energy_capacity,
                "robot_supply": robot_capacity,
                "storage": storage_capacity,
                "budget": budget_capacity,
            }
            binding = min(candidates, key=candidates.get)
        emissions = 42.2 + (s.emissions_2046_gtco2_y - 42.2) * progress
        rebound = actual_capacity * s.rebound_fraction_of_gross_removal
        net_removal = actual_capacity - emissions - rebound
        rows.append({
            "scenario": s.key,
            "display_name": s.display_name,
            "year": year,
            "years_from_2026": i,
            "planned_linear_target_gtco2_y": planned_capacity,
            "actual_capacity_gtco2_y": actual_capacity,
            "binding_constraint": binding,
            "clean_energy_available_twh_y": clean_twh,
            "energy_limited_capacity_gtco2_y": energy_capacity,
            "robots_in_service_for_aether": available_robots,
            "robot_limited_capacity_gtco2_y": robot_capacity,
            "storage_limited_capacity_gtco2_y": storage_capacity,
            "budget_limited_capacity_gtco2_y": budget_capacity,
            "learned_cost_usd_tco2": cost,
            "annual_cost_trillion_usd": actual_capacity * cost / 1000,
            "emissions_gtco2_y": emissions,
            "rebound_gtco2_y": rebound,
            "net_removal_after_emissions_and_rebound_gtco2_y": net_removal,
        })
    return rows


def summarize_scenario(s: FeasibilityScenario, path_rows: list[dict[str, object]]) -> dict[str, object]:
    final = path_rows[-1]
    target_energy_twh = TARGET_GTCO2_Y * s.energy_gj_tco2 * TWH_PER_GJ_PER_TON_FOR_1_GT
    terminal_cost = learned_cost(s, TARGET_GTCO2_Y)
    annual_cost_at_target = TARGET_GTCO2_Y * terminal_cost / 1000
    fleet_required = s.robots_per_mtco2_y_capacity * TARGET_GTCO2_Y * 1000
    terminal_robots = float(final["robots_in_service_for_aether"])
    terminal_clean_twh = float(final["clean_energy_available_twh_y"])
    net_at_target = TARGET_GTCO2_Y - s.emissions_2046_gtco2_y - (s.rebound_fraction_of_gross_removal * TARGET_GTCO2_Y)
    actual_terminal = float(final["actual_capacity_gtco2_y"])
    actual_net = float(final["net_removal_after_emissions_and_rebound_gtco2_y"])
    ratios = {
        "energy_adequacy_ratio": terminal_clean_twh / target_energy_twh,
        "robot_adequacy_ratio": terminal_robots / fleet_required,
        "storage_adequacy_ratio": s.storage_terminal_gtco2_y / TARGET_GTCO2_Y,
        "budget_adequacy_ratio": s.annual_budget_trillion_usd / annual_cost_at_target,
        "terminal_capacity_ratio": actual_terminal / TARGET_GTCO2_Y,
        "net_target_ratio_vs_current_emissions": max(0.0, net_at_target) / (TARGET_GTCO2_Y - 42.2),
    }
    bottlenecks = [name.replace("_adequacy_ratio", "") for name, value in ratios.items() if value < 1.0 and name.endswith("_adequacy_ratio")]
    binding_counts: dict[str, int] = {}
    for row in path_rows:
        binding = str(row["binding_constraint"])
        binding_counts[binding] = binding_counts.get(binding, 0) + 1
    dominant_binding = max(binding_counts, key=binding_counts.get)
    min_resource_ratio = min(ratios["energy_adequacy_ratio"], ratios["robot_adequacy_ratio"], ratios["storage_adequacy_ratio"], ratios["budget_adequacy_ratio"])
    if actual_terminal >= 95 and net_at_target >= 25 and min_resource_ratio >= 1.0:
        screen = "passes_100gt_screen"
    elif actual_terminal >= 75 and actual_net > 0:
        screen = "near_miss_or_knife_edge"
    elif actual_net > 0:
        screen = "partial_net_negative"
    else:
        screen = "fails_or_offset_only"
    return {
        "scenario": s.key,
        "display_name": s.display_name,
        "description": s.description,
        "screen_result": screen,
        "energy_gj_tco2": s.energy_gj_tco2,
        "target_energy_twh_y": target_energy_twh,
        "terminal_clean_energy_available_twh_y": terminal_clean_twh,
        "energy_adequacy_ratio": ratios["energy_adequacy_ratio"],
        "terminal_cost_usd_tco2": terminal_cost,
        "annual_cost_at_100gt_trillion_usd": annual_cost_at_target,
        "annual_budget_trillion_usd": s.annual_budget_trillion_usd,
        "budget_adequacy_ratio": ratios["budget_adequacy_ratio"],
        "robots_per_mtco2_y_capacity": s.robots_per_mtco2_y_capacity,
        "robot_fleet_required_at_100gt": fleet_required,
        "terminal_robots_in_service_for_aether": terminal_robots,
        "robot_adequacy_ratio": ratios["robot_adequacy_ratio"],
        "storage_terminal_gtco2_y": s.storage_terminal_gtco2_y,
        "storage_adequacy_ratio": ratios["storage_adequacy_ratio"],
        "terminal_actual_capacity_gtco2_y": actual_terminal,
        "terminal_capacity_ratio": ratios["terminal_capacity_ratio"],
        "emissions_2046_gtco2_y": s.emissions_2046_gtco2_y,
        "rebound_fraction_of_gross_removal": s.rebound_fraction_of_gross_removal,
        "net_at_100gt_after_emissions_and_rebound_gtco2_y": net_at_target,
        "terminal_actual_net_gtco2_y": actual_net,
        "net_target_ratio_vs_current_emissions": ratios["net_target_ratio_vs_current_emissions"],
        "dominant_binding_constraint_over_path": dominant_binding,
        "bottleneck_list": "; ".join(bottlenecks) if bottlenecks else "none",
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {path}")


def main() -> None:
    all_time_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []
    bottleneck_rows: list[dict[str, object]] = []
    for s in scenarios():
        path_rows = capacity_limited_path(s)
        all_time_rows.extend(path_rows)
        summary = summarize_scenario(s, path_rows)
        summary_rows.append(summary)
        for metric in [
            "energy_adequacy_ratio",
            "robot_adequacy_ratio",
            "storage_adequacy_ratio",
            "budget_adequacy_ratio",
            "terminal_capacity_ratio",
            "net_target_ratio_vs_current_emissions",
        ]:
            bottleneck_rows.append({
                "scenario": s.key,
                "display_name": s.display_name,
                "metric": metric,
                "ratio": summary[metric],
                "passes_screen": float(summary[metric]) >= 1.0,
            })
    write_csv(OUT / "aether_integrated_feasibility_timepaths.csv", all_time_rows)
    write_csv(OUT / "aether_integrated_feasibility_scenarios.csv", summary_rows)
    write_csv(OUT / "aether_integrated_feasibility_bottlenecks.csv", bottleneck_rows)


if __name__ == "__main__":
    main()
