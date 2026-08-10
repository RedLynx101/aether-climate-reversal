from __future__ import annotations

import csv
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TABLE_DIR = ROOT / "analysis" / "tables"
TABLE_DIR.mkdir(parents=True, exist_ok=True)

INPUT_BY_TASK = TABLE_DIR / "aether_robotics_productivity_by_task.csv"
IFR_2024_INDUSTRIAL_ROBOT_INSTALLS = 542_076.0
N_SAMPLES = 2_000
SEED = 42610


SCENARIO_RANGES = {
    "high_robot_intensity_translation": {
        "uptime": (0.55, 0.72, 0.86),
        "autonomy": (0.35, 0.55, 0.75),
        "task_fit": (0.45, 0.65, 0.85),
        "maintenance": (1.10, 1.25, 1.55),
        "supervision": (1.00, 1.15, 1.40),
    },
    "aether_automation_push": {
        "uptime": (0.68, 0.82, 0.93),
        "autonomy": (0.55, 0.75, 0.90),
        "task_fit": (0.65, 0.84, 0.96),
        "maintenance": (1.05, 1.15, 1.32),
        "supervision": (1.00, 1.08, 1.22),
    },
    "deep_modular_abundance": {
        "uptime": (0.78, 0.90, 0.97),
        "autonomy": (0.75, 0.90, 0.98),
        "task_fit": (0.78, 0.92, 1.00),
        "maintenance": (1.00, 1.08, 1.20),
        "supervision": (1.00, 1.04, 1.12),
    },
}


TASK_ADJUSTMENTS = {
    "plant_operations_maintenance": {
        "uptime": -0.03,
        "autonomy": -0.08,
        "task_fit": -0.04,
        "maintenance": 0.08,
        "supervision": 0.10,
        "risk_driver": "messy plant maintenance and exception handling",
    },
    "materials_handling_logistics": {
        "uptime": 0.06,
        "autonomy": 0.08,
        "task_fit": 0.08,
        "maintenance": -0.04,
        "supervision": -0.04,
        "risk_driver": "best when work is moved into warehouse-like designed environments",
    },
    "storage_field_operations": {
        "uptime": -0.08,
        "autonomy": -0.14,
        "task_fit": -0.12,
        "maintenance": 0.18,
        "supervision": 0.20,
        "risk_driver": "subsurface work, well integrity, and safety-critical field constraints",
    },
    "mrv_sensor_auditing": {
        "uptime": 0.04,
        "autonomy": 0.06,
        "task_fit": 0.05,
        "maintenance": -0.03,
        "supervision": -0.02,
        "risk_driver": "strong automation fit but adversarial verification still matters",
    },
    "factory_spares_replacement": {
        "uptime": 0.07,
        "autonomy": 0.10,
        "task_fit": 0.08,
        "maintenance": -0.05,
        "supervision": -0.05,
        "risk_driver": "factory automation is the best-evidenced robot environment",
    },
    "robotic_labs_process_improvement": {
        "uptime": 0.03,
        "autonomy": 0.04,
        "task_fit": 0.04,
        "maintenance": 0.00,
        "supervision": 0.00,
        "risk_driver": "autonomous labs need scientific throughput evidence, not only robot uptime",
    },
    "module_manufacturing": {
        "uptime": 0.06,
        "autonomy": 0.09,
        "task_fit": 0.07,
        "maintenance": -0.04,
        "supervision": -0.05,
        "risk_driver": "repeatable modules should be easier than bespoke field construction",
    },
    "construction_commissioning": {
        "uptime": -0.06,
        "autonomy": -0.10,
        "task_fit": -0.08,
        "maintenance": 0.14,
        "supervision": 0.16,
        "risk_driver": "construction productivity and commissioning exceptions",
    },
    "storage_wells_corridors": {
        "uptime": -0.10,
        "autonomy": -0.16,
        "task_fit": -0.14,
        "maintenance": 0.20,
        "supervision": 0.25,
        "risk_driver": "drilling, pressure management, right-of-way, and permitting interfaces",
    },
    "logistics_ramp": {
        "uptime": 0.05,
        "autonomy": 0.07,
        "task_fit": 0.07,
        "maintenance": -0.03,
        "supervision": -0.04,
        "risk_driver": "can be standardized if the buildout is modular",
    },
    "mrv_initialization": {
        "uptime": 0.03,
        "autonomy": 0.05,
        "task_fit": 0.04,
        "maintenance": -0.02,
        "supervision": -0.02,
        "risk_driver": "baseline mapping and sensor setup are automatable but method-specific",
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], columns: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"No rows generated for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    if columns is None:
        columns = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})
    print(f"Wrote {path}")


def f(value: float, digits: int = 6) -> str:
    return f"{value:.{digits}f}"


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def shifted_range(base: tuple[float, float, float], delta: float, low: float, high: float) -> tuple[float, float, float]:
    values = [clamp(v + delta, low, high) for v in base]
    values.sort()
    return values[0], values[1], values[2]


def task_ranges(scenario: str, task_family: str) -> dict[str, tuple[float, float, float]]:
    base = SCENARIO_RANGES[scenario]
    adj = TASK_ADJUSTMENTS[task_family]
    return {
        "uptime": shifted_range(base["uptime"], adj["uptime"], 0.10, 0.99),
        "autonomy": shifted_range(base["autonomy"], adj["autonomy"], 0.05, 0.99),
        "task_fit": shifted_range(base["task_fit"], adj["task_fit"], 0.05, 1.00),
        "maintenance": shifted_range(base["maintenance"], adj["maintenance"], 1.00, 2.50),
        "supervision": shifted_range(base["supervision"], adj["supervision"], 1.00, 2.50),
    }


def triangular(rng: random.Random, values: tuple[float, float, float]) -> float:
    low, mode, high = values
    return rng.triangular(low, high, mode)


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return float("nan")
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    idx = (len(ordered) - 1) * pct
    lo = int(idx)
    hi = min(lo + 1, len(ordered) - 1)
    frac = idx - lo
    return ordered[lo] * (1.0 - frac) + ordered[hi] * frac


def main() -> None:
    rng = random.Random(SEED)
    task_rows = read_csv(INPUT_BY_TASK)
    scenarios = sorted({row["scenario"] for row in task_rows})

    assumptions = []
    for row in task_rows:
        ranges = task_ranges(row["scenario"], row["task_family"])
        assumptions.append({
            "scenario": row["scenario"],
            "scenario_name": row["scenario_name"],
            "task_family": row["task_family"],
            "display_name": row["display_name"],
            "assigned_robot_class": row["assigned_robot_class"],
            "evidence_grade": row["evidence_grade"],
            "uptime_low": f(ranges["uptime"][0], 4),
            "uptime_mode": f(ranges["uptime"][1], 4),
            "uptime_high": f(ranges["uptime"][2], 4),
            "autonomy_low": f(ranges["autonomy"][0], 4),
            "autonomy_mode": f(ranges["autonomy"][1], 4),
            "autonomy_high": f(ranges["autonomy"][2], 4),
            "task_fit_low": f(ranges["task_fit"][0], 4),
            "task_fit_mode": f(ranges["task_fit"][1], 4),
            "task_fit_high": f(ranges["task_fit"][2], 4),
            "maintenance_factor_low": f(ranges["maintenance"][0], 4),
            "maintenance_factor_mode": f(ranges["maintenance"][1], 4),
            "maintenance_factor_high": f(ranges["maintenance"][2], 4),
            "supervision_factor_low": f(ranges["supervision"][0], 4),
            "supervision_factor_mode": f(ranges["supervision"][1], 4),
            "supervision_factor_high": f(ranges["supervision"][2], 4),
            "risk_driver": TASK_ADJUSTMENTS[row["task_family"]]["risk_driver"],
        })

    sample_rows = []
    task_sample_rows = []
    for scenario in scenarios:
        scenario_tasks = [row for row in task_rows if row["scenario"] == scenario]
        for sample_id in range(1, N_SAMPLES + 1):
            adjusted_stock = 0.0
            adjusted_replacement = 0.0
            adjusted_buildout = 0.0
            adjusted_cost = 0.0
            baseline_stock = 0.0
            baseline_production = 0.0
            baseline_cost = 0.0
            weighted_effective_numerator = 0.0
            weighted_effective_denominator = 0.0
            for row in scenario_tasks:
                ranges = task_ranges(scenario, row["task_family"])
                uptime = triangular(rng, ranges["uptime"])
                autonomy = triangular(rng, ranges["autonomy"])
                task_fit = triangular(rng, ranges["task_fit"])
                maintenance = triangular(rng, ranges["maintenance"])
                supervision = triangular(rng, ranges["supervision"])
                effective_multiplier = clamp((uptime * autonomy * task_fit) / (maintenance * supervision), 0.02, 1.00)

                stock = float(row["robot_stock_required"])
                replacement = float(row["annual_replacement_flow"])
                buildout = stock / 20.0
                cost = float(row["annual_robot_operating_cost_billion_usd"])

                adj_stock = stock / effective_multiplier
                adj_replacement = replacement / effective_multiplier
                adj_buildout = buildout / effective_multiplier
                adj_cost = cost / effective_multiplier

                adjusted_stock += adj_stock
                adjusted_replacement += adj_replacement
                adjusted_buildout += adj_buildout
                adjusted_cost += adj_cost
                baseline_stock += stock
                baseline_production += replacement + buildout
                baseline_cost += cost
                weighted_effective_numerator += effective_multiplier * stock
                weighted_effective_denominator += stock

                task_sample_rows.append({
                    "scenario": scenario,
                    "scenario_name": row["scenario_name"],
                    "sample_id": sample_id,
                    "task_family": row["task_family"],
                    "display_name": row["display_name"],
                    "assigned_robot_class": row["assigned_robot_class"],
                    "effective_task_hour_multiplier": f(effective_multiplier, 6),
                    "adjusted_robot_stock": f(adj_stock, 4),
                    "adjusted_annual_production_robots": f(adj_replacement + adj_buildout, 4),
                    "adjusted_annual_operating_cost_billion_usd": f(adj_cost, 6),
                })

            adjusted_production = adjusted_replacement + adjusted_buildout
            weighted_effective = weighted_effective_numerator / weighted_effective_denominator
            sample_rows.append({
                "scenario": scenario,
                "sample_id": sample_id,
                "weighted_effective_task_hour_multiplier": f(weighted_effective, 6),
                "adjusted_robot_stock_million": f(adjusted_stock / 1e6, 6),
                "adjusted_annual_production_robots": f(adjusted_production, 4),
                "production_multiple_of_ifr_2024": f(adjusted_production / IFR_2024_INDUSTRIAL_ROBOT_INSTALLS, 6),
                "adjusted_annual_operating_cost_billion_usd": f(adjusted_cost, 6),
                "stock_multiplier_vs_baseline": f(adjusted_stock / baseline_stock, 6),
                "production_multiplier_vs_baseline": f(adjusted_production / baseline_production, 6),
                "cost_multiplier_vs_baseline": f(adjusted_cost / baseline_cost, 6),
                "passes_ifr_installation_count_basis": str(adjusted_production <= IFR_2024_INDUSTRIAL_ROBOT_INSTALLS).lower(),
            })

    summary_rows = []
    for scenario in scenarios:
        rows = [row for row in sample_rows if row["scenario"] == scenario]
        productions = [float(row["adjusted_annual_production_robots"]) for row in rows]
        stocks = [float(row["adjusted_robot_stock_million"]) for row in rows]
        costs = [float(row["adjusted_annual_operating_cost_billion_usd"]) for row in rows]
        multipliers = [float(row["weighted_effective_task_hour_multiplier"]) for row in rows]
        pass_share = sum(1 for row in rows if row["passes_ifr_installation_count_basis"] == "true") / len(rows)
        scenario_name = next(row["scenario_name"] for row in task_rows if row["scenario"] == scenario)
        summary_rows.append({
            "scenario": scenario,
            "scenario_name": scenario_name,
            "samples": len(rows),
            "effective_multiplier_p10": f(percentile(multipliers, 0.10), 6),
            "effective_multiplier_p50": f(percentile(multipliers, 0.50), 6),
            "effective_multiplier_p90": f(percentile(multipliers, 0.90), 6),
            "annual_production_p10_robots": f(percentile(productions, 0.10), 2),
            "annual_production_p50_robots": f(percentile(productions, 0.50), 2),
            "annual_production_p90_robots": f(percentile(productions, 0.90), 2),
            "robot_stock_p50_million": f(percentile(stocks, 0.50), 6),
            "annual_cost_p50_billion_usd": f(percentile(costs, 0.50), 6),
            "ifr_pass_share": f(pass_share, 6),
            "p50_production_multiple_ifr": f(percentile(productions, 0.50) / IFR_2024_INDUSTRIAL_ROBOT_INSTALLS, 6),
            "interpretation": "Field productivity multipliers stress-test whether useful autonomous task-hours survive uptime, autonomy, task-fit, maintenance, and supervision penalties.",
        })

    bottleneck_rows = []
    for scenario in scenarios:
        scenario_task_rows = [row for row in task_sample_rows if row["scenario"] == scenario]
        scenario_samples = [row for row in sample_rows if row["scenario"] == scenario]
        scenario_p50_production = percentile([float(row["adjusted_annual_production_robots"]) for row in scenario_samples], 0.50)
        task_families = sorted({row["task_family"] for row in scenario_task_rows})
        for task_family in task_families:
            rows = [row for row in scenario_task_rows if row["task_family"] == task_family]
            production_values = [float(row["adjusted_annual_production_robots"]) for row in rows]
            multiplier_values = [float(row["effective_task_hour_multiplier"]) for row in rows]
            display_name = rows[0]["display_name"]
            bottleneck_rows.append({
                "scenario": scenario,
                "task_family": task_family,
                "display_name": display_name,
                "assigned_robot_class": rows[0]["assigned_robot_class"],
                "effective_multiplier_p10": f(percentile(multiplier_values, 0.10), 6),
                "effective_multiplier_p50": f(percentile(multiplier_values, 0.50), 6),
                "effective_multiplier_p90": f(percentile(multiplier_values, 0.90), 6),
                "annual_production_p50_robots": f(percentile(production_values, 0.50), 4),
                "share_of_scenario_p50_production": f(percentile(production_values, 0.50) / scenario_p50_production, 6),
                "risk_driver": TASK_ADJUSTMENTS[task_family]["risk_driver"],
            })

    metric_lookup = {row["scenario"]: row for row in summary_rows}
    compact_summary = [
        {"metric": "high_p50_annual_production_robots", "value": metric_lookup["high_robot_intensity_translation"]["annual_production_p50_robots"], "unit": "robots/year", "interpretation": "Median annual robot production requirement after field-productivity multipliers in the high robot-intensity stress case."},
        {"metric": "push_p50_annual_production_robots", "value": metric_lookup["aether_automation_push"]["annual_production_p50_robots"], "unit": "robots/year", "interpretation": "Median annual robot production requirement after field-productivity multipliers in the AETHER automation-push case."},
        {"metric": "deep_p50_annual_production_robots", "value": metric_lookup["deep_modular_abundance"]["annual_production_p50_robots"], "unit": "robots/year", "interpretation": "Median annual robot production requirement after field-productivity multipliers in the deep modular case."},
        {"metric": "high_p50_stock_million", "value": metric_lookup["high_robot_intensity_translation"]["robot_stock_p50_million"], "unit": "million robots", "interpretation": "Median robot stock after field-productivity multipliers in the high robot-intensity stress case."},
        {"metric": "push_p50_stock_million", "value": metric_lookup["aether_automation_push"]["robot_stock_p50_million"], "unit": "million robots", "interpretation": "Median robot stock after field-productivity multipliers in the AETHER automation-push case."},
        {"metric": "deep_p50_stock_million", "value": metric_lookup["deep_modular_abundance"]["robot_stock_p50_million"], "unit": "million robots", "interpretation": "Median robot stock after field-productivity multipliers in the deep modular case."},
        {"metric": "push_ifr_pass_share", "value": metric_lookup["aether_automation_push"]["ifr_pass_share"], "unit": "share", "interpretation": "Share of AETHER automation-push samples below current annual industrial robot installations on a count basis."},
        {"metric": "deep_ifr_pass_share", "value": metric_lookup["deep_modular_abundance"]["ifr_pass_share"], "unit": "share", "interpretation": "Share of deep modular abundance samples below current annual industrial robot installations on a count basis."},
        {"metric": "high_p50_multiple_ifr", "value": metric_lookup["high_robot_intensity_translation"]["p50_production_multiple_ifr"], "unit": "multiple", "interpretation": "Median high-intensity field-productivity-adjusted production requirement relative to IFR 2024 installations."},
        {"metric": "push_p50_multiple_ifr", "value": metric_lookup["aether_automation_push"]["p50_production_multiple_ifr"], "unit": "multiple", "interpretation": "Median automation-push field-productivity-adjusted production requirement relative to IFR 2024 installations."},
        {"metric": "deep_p50_multiple_ifr", "value": metric_lookup["deep_modular_abundance"]["p50_production_multiple_ifr"], "unit": "multiple", "interpretation": "Median deep modular field-productivity-adjusted production requirement relative to IFR 2024 installations."},
    ]

    write_csv(TABLE_DIR / "aether_robotics_field_productivity_distribution_assumptions.csv", assumptions)
    write_csv(TABLE_DIR / "aether_robotics_field_productivity_distribution_samples.csv", sample_rows)
    write_csv(TABLE_DIR / "aether_robotics_field_productivity_distribution_summary.csv", summary_rows)
    write_csv(TABLE_DIR / "aether_robotics_field_productivity_bottlenecks.csv", bottleneck_rows)
    write_csv(TABLE_DIR / "aether_robotics_field_productivity_summary_metrics.csv", compact_summary)


if __name__ == "__main__":
    main()

