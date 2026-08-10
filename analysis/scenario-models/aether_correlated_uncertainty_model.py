from __future__ import annotations

import csv
import math
import random
import statistics
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TABLE_DIR = ROOT / "analysis" / "tables"
TABLE_DIR.mkdir(parents=True, exist_ok=True)

SEED = 463033
SAMPLES_PER_FAMILY = 1500
TARGET_DURABLE_GTCO2_Y = 100.0
CURRENT_EMISSIONS_GTCO2_Y = 42.2
BASE_CLEAN_ELECTRICITY_ADDITION_TWH_Y = 850.0
BASE_ROBOT_OUTPUT_Y = 542_076.0
ROBOT_SERVICE_LIFE_Y = 8
TWH_PER_GJ_PER_TON_FOR_1_GT = 277.77777777777777


@dataclass(frozen=True)
class Parameter:
    field: str
    label: str
    low: float
    mode: float
    high: float
    unit: str
    interpretation: str
    correlation_family: str
    evidence_grade: str


@dataclass(frozen=True)
class ScenarioFamily:
    key: str
    label: str
    description: str
    shift_strength: float
    shifts: dict[str, int]


SCENARIOS = [
    ScenarioFamily(
        key="independent_reference",
        label="Independent reference",
        description="Same triangular input ranges as the current Monte Carlo screen, without explicit correlation-family shifts.",
        shift_strength=0.0,
        shifts={},
    ),
    ScenarioFamily(
        key="clean_power_abundance_correlated",
        label="Clean-power abundance",
        description="Clean generation, allocation, deliverability, and energy intensity move together in the favorable direction.",
        shift_strength=0.55,
        shifts={
            "energy_gj_tco2": -1,
            "clean_addition_growth_rate": 1,
            "aether_clean_share": 1,
            "clean_deliverability_fraction": 1,
            "cost_usd_tco2": -1,
            "execution_realization_fraction": 1,
        },
    ),
    ScenarioFamily(
        key="automation_abundance_correlated",
        label="Automation abundance",
        description="Robot output, AETHER robot allocation, task productivity, cost, and execution move together in the favorable direction.",
        shift_strength=0.55,
        shifts={
            "robot_output_growth_rate": 1,
            "aether_robot_share": 1,
            "robots_per_mtco2_y_capacity": -1,
            "cost_usd_tco2": -1,
            "gross_overbuild_factor": 1,
            "execution_realization_fraction": 1,
        },
    ),
    ScenarioFamily(
        key="storage_mrv_failure_correlated",
        label="Storage/MRV failure",
        description="Storage throughput, durability, cost, and execution move together in the adverse direction.",
        shift_strength=0.58,
        shifts={
            "storage_terminal_gtco2_y": -1,
            "durability_fraction_100y": -1,
            "cost_usd_tco2": 1,
            "gross_overbuild_factor": -1,
            "execution_realization_fraction": -1,
        },
    ),
    ScenarioFamily(
        key="policy_rebound_failure_correlated",
        label="Policy/rebound failure",
        description="Political support can raise budgets and clean-power allocation while rebound, residual emissions, and execution drag also worsen.",
        shift_strength=0.55,
        shifts={
            "annual_budget_trillion_usd": 1,
            "aether_clean_share": 1,
            "residual_emissions_2046_gtco2_y": 1,
            "rebound_fraction_of_gross": 1,
            "execution_realization_fraction": -1,
        },
    ),
    ScenarioFamily(
        key="full_abundance_aligned",
        label="Full abundance aligned",
        description="Clean power, automation, storage, cost, durability, execution, and rebound control all move together in the favorable direction.",
        shift_strength=0.65,
        shifts={
            "energy_gj_tco2": -1,
            "clean_addition_growth_rate": 1,
            "aether_clean_share": 1,
            "clean_deliverability_fraction": 1,
            "robot_output_growth_rate": 1,
            "aether_robot_share": 1,
            "robots_per_mtco2_y_capacity": -1,
            "storage_terminal_gtco2_y": 1,
            "cost_usd_tco2": -1,
            "annual_budget_trillion_usd": 1,
            "durability_fraction_100y": 1,
            "residual_emissions_2046_gtco2_y": -1,
            "rebound_fraction_of_gross": -1,
            "gross_overbuild_factor": 1,
            "execution_realization_fraction": 1,
        },
    ),
    ScenarioFamily(
        key="full_failure_clustered",
        label="Full failure clustered",
        description="Clean power, automation, storage, cost, durability, residual emissions, rebound, and execution all move together in the adverse direction.",
        shift_strength=0.65,
        shifts={
            "energy_gj_tco2": 1,
            "clean_addition_growth_rate": -1,
            "aether_clean_share": -1,
            "clean_deliverability_fraction": -1,
            "robot_output_growth_rate": -1,
            "aether_robot_share": -1,
            "robots_per_mtco2_y_capacity": 1,
            "storage_terminal_gtco2_y": -1,
            "cost_usd_tco2": 1,
            "annual_budget_trillion_usd": -1,
            "durability_fraction_100y": -1,
            "residual_emissions_2046_gtco2_y": 1,
            "rebound_fraction_of_gross": 1,
            "gross_overbuild_factor": -1,
            "execution_realization_fraction": -1,
        },
    ),
]


def read_parameters() -> list[Parameter]:
    path = TABLE_DIR / "aether_uncertainty_distribution_registry.csv"
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    parameters: list[Parameter] = []
    for row in rows:
        parameters.append(
            Parameter(
                field=row["parameter"],
                label=row["label"],
                low=float(row["current_low"]),
                mode=float(row["current_mode"]),
                high=float(row["current_high"]),
                unit=row["unit"],
                interpretation=row["current_interpretation"],
                correlation_family=row["correlation_family"],
                evidence_grade=row["evidence_grade"],
            )
        )
    return parameters


def draw_triangular(rng: random.Random, p: Parameter) -> float:
    return rng.triangular(p.low, p.high, p.mode)


def shift_value(value: float, p: Parameter, direction: int, strength: float, common: float, rng: random.Random) -> float:
    if direction == 0 or strength <= 0.0:
        return value
    target = p.high if direction > 0 else p.low
    variable_noise = 0.82 + 0.36 * rng.random()
    alpha = min(0.95, max(0.0, strength * (0.50 + 0.50 * common) * variable_noise))
    shifted = value + alpha * (target - value)
    return max(p.low, min(p.high, shifted))


def cumulative_clean_twh(growth_rate: float, share: float, deliverability: float) -> float:
    gross_new_clean = sum(BASE_CLEAN_ELECTRICITY_ADDITION_TWH_Y * ((1.0 + growth_rate) ** t) for t in range(21))
    return gross_new_clean * share * deliverability


def robots_in_service(growth_rate: float, share: float) -> float:
    return sum(BASE_ROBOT_OUTPUT_Y * ((1.0 + growth_rate) ** t) * share for t in range(21 - ROBOT_SERVICE_LIFE_Y, 21))


def quantile(values: list[float], q: float) -> float:
    if not values:
        return float("nan")
    ordered = sorted(values)
    pos = (len(ordered) - 1) * q
    low = math.floor(pos)
    high = math.ceil(pos)
    if low == high:
        return ordered[int(pos)]
    return ordered[low] + (ordered[high] - ordered[low]) * (pos - low)


def mean_flag(rows: list[dict[str, object]], field: str) -> float:
    return sum(float(row[field]) for row in rows) / len(rows)


def evaluate_sample(sample: dict[str, float]) -> dict[str, float | str]:
    clean_twh = cumulative_clean_twh(
        sample["clean_addition_growth_rate"],
        sample["aether_clean_share"],
        sample["clean_deliverability_fraction"],
    )
    energy_capacity = clean_twh / (sample["energy_gj_tco2"] * TWH_PER_GJ_PER_TON_FOR_1_GT)

    robot_fleet = robots_in_service(sample["robot_output_growth_rate"], sample["aether_robot_share"])
    robot_capacity = robot_fleet / (sample["robots_per_mtco2_y_capacity"] * 1000.0)

    budget_capacity = sample["annual_budget_trillion_usd"] * 1000.0 / sample["cost_usd_tco2"]
    program_execution_capacity = TARGET_DURABLE_GTCO2_Y * sample["gross_overbuild_factor"] * sample["execution_realization_fraction"]
    capacities = {
        "clean_energy": energy_capacity,
        "robot_supply": robot_capacity,
        "storage": sample["storage_terminal_gtco2_y"],
        "budget": budget_capacity,
        "program_execution": program_execution_capacity,
    }
    gross_capacity = min(capacities.values())
    binding = min(capacities, key=capacities.get)
    durable_credit = gross_capacity * sample["durability_fraction_100y"]
    rebound_gt = gross_capacity * sample["rebound_fraction_of_gross"]
    net_after_emissions = durable_credit - sample["residual_emissions_2046_gtco2_y"] - rebound_gt

    return {
        "clean_energy_available_twh_y": clean_twh,
        "energy_limited_capacity_gtco2_y": energy_capacity,
        "robots_in_service_for_aether": robot_fleet,
        "robot_limited_capacity_gtco2_y": robot_capacity,
        "storage_capacity_gtco2_y": sample["storage_terminal_gtco2_y"],
        "budget_limited_capacity_gtco2_y": budget_capacity,
        "program_execution_capacity_gtco2_y": program_execution_capacity,
        "gross_capacity_gtco2_y": gross_capacity,
        "durable_100y_credit_gtco2_y": durable_credit,
        "rebound_gtco2_y": rebound_gt,
        "net_after_emissions_and_rebound_gtco2_y": net_after_emissions,
        "binding_constraint": binding,
        "gross_100_pass": 1.0 if gross_capacity >= 100.0 else 0.0,
        "durable_100_pass": 1.0 if durable_credit >= TARGET_DURABLE_GTCO2_Y else 0.0,
        "positive_climate_reversal_pass": 1.0 if net_after_emissions > 0.0 else 0.0,
        "strong_reversal_pass": 1.0 if net_after_emissions >= CURRENT_EMISSIONS_GTCO2_Y else 0.0,
    }


def run_samples(parameters: list[Parameter]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rng = random.Random(SEED)
    rows: list[dict[str, object]] = []
    scenario_rows: list[dict[str, object]] = []
    by_field = {p.field: p for p in parameters}

    for scenario in SCENARIOS:
        scenario_rows.append(
            {
                "scenario_family": scenario.key,
                "label": scenario.label,
                "samples": SAMPLES_PER_FAMILY,
                "shift_strength": scenario.shift_strength,
                "shifted_parameters": ";".join(sorted(scenario.shifts)),
                "description": scenario.description,
                "paper_use_rule": "correlated scenario-family screen; not calibrated probability forecast",
            }
        )
        for sample_index in range(1, SAMPLES_PER_FAMILY + 1):
            common_shock = rng.random()
            sample = {p.field: draw_triangular(rng, p) for p in parameters}
            for field, direction in scenario.shifts.items():
                sample[field] = shift_value(sample[field], by_field[field], direction, scenario.shift_strength, common_shock, rng)
            evaluated = evaluate_sample(sample)
            rows.append(
                {
                    "sample_id": f"{scenario.key}_{sample_index:04d}",
                    "scenario_family": scenario.key,
                    "scenario_label": scenario.label,
                    "common_family_shock": common_shock,
                    **sample,
                    **evaluated,
                }
            )
    return rows, scenario_rows


def summarize(rows: list[dict[str, object]], scenarios: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    summary_rows: list[dict[str, object]] = []
    effect_rows: list[dict[str, object]] = []
    by_scenario = {scenario["scenario_family"]: [row for row in rows if row["scenario_family"] == scenario["scenario_family"]] for scenario in scenarios}

    def metrics(scenario_rows: list[dict[str, object]]) -> dict[str, float | str]:
        gross = [float(row["gross_capacity_gtco2_y"]) for row in scenario_rows]
        durable = [float(row["durable_100y_credit_gtco2_y"]) for row in scenario_rows]
        net = [float(row["net_after_emissions_and_rebound_gtco2_y"]) for row in scenario_rows]
        clean = [float(row["energy_limited_capacity_gtco2_y"]) for row in scenario_rows]
        robot = [float(row["robot_limited_capacity_gtco2_y"]) for row in scenario_rows]
        storage = [float(row["storage_capacity_gtco2_y"]) for row in scenario_rows]
        budget = [float(row["budget_limited_capacity_gtco2_y"]) for row in scenario_rows]
        execution = [float(row["program_execution_capacity_gtco2_y"]) for row in scenario_rows]
        binding_counts = {}
        for row in scenario_rows:
            binding = str(row["binding_constraint"])
            binding_counts[binding] = binding_counts.get(binding, 0) + 1
        primary_binding = max(binding_counts, key=binding_counts.get)
        return {
            "sample_count": float(len(scenario_rows)),
            "gross_100_probability": mean_flag(scenario_rows, "gross_100_pass"),
            "durable_100_probability": mean_flag(scenario_rows, "durable_100_pass"),
            "positive_climate_reversal_probability": mean_flag(scenario_rows, "positive_climate_reversal_pass"),
            "strong_reversal_probability": mean_flag(scenario_rows, "strong_reversal_pass"),
            "gross_capacity_p10": quantile(gross, 0.10),
            "gross_capacity_p50": quantile(gross, 0.50),
            "gross_capacity_p90": quantile(gross, 0.90),
            "durable_credit_p10": quantile(durable, 0.10),
            "durable_credit_p50": quantile(durable, 0.50),
            "durable_credit_p90": quantile(durable, 0.90),
            "net_after_emissions_rebound_p10": quantile(net, 0.10),
            "net_after_emissions_rebound_p50": quantile(net, 0.50),
            "net_after_emissions_rebound_p90": quantile(net, 0.90),
            "median_energy_capacity_gtco2_y": quantile(clean, 0.50),
            "median_robot_capacity_gtco2_y": quantile(robot, 0.50),
            "median_storage_capacity_gtco2_y": quantile(storage, 0.50),
            "median_budget_capacity_gtco2_y": quantile(budget, 0.50),
            "median_execution_capacity_gtco2_y": quantile(execution, 0.50),
            "primary_binding_constraint": primary_binding,
            "primary_binding_share": binding_counts[primary_binding] / len(scenario_rows),
        }

    labels = {scenario["scenario_family"]: scenario["label"] for scenario in scenarios}
    reference = metrics(by_scenario["independent_reference"])
    for scenario in scenarios:
        key = str(scenario["scenario_family"])
        values = metrics(by_scenario[key])
        summary_rows.append(
            {
                "scenario_family": key,
                "label": labels[key],
                **{k: f"{v:.8f}" if isinstance(v, float) else v for k, v in values.items()},
                "paper_use_rule": "scenario-family sensitivity only; do not read as calibrated probability",
            }
        )
        if key != "independent_reference":
            effect_rows.append(
                {
                    "scenario_family": key,
                    "label": labels[key],
                    "delta_gross_100_probability_vs_independent": f"{float(values['gross_100_probability']) - float(reference['gross_100_probability']):.8f}",
                    "delta_durable_100_probability_vs_independent": f"{float(values['durable_100_probability']) - float(reference['durable_100_probability']):.8f}",
                    "delta_positive_climate_reversal_probability_vs_independent": f"{float(values['positive_climate_reversal_probability']) - float(reference['positive_climate_reversal_probability']):.8f}",
                    "delta_strong_reversal_probability_vs_independent": f"{float(values['strong_reversal_probability']) - float(reference['strong_reversal_probability']):.8f}",
                    "delta_median_durable_credit_gtco2_y_vs_independent": f"{float(values['durable_credit_p50']) - float(reference['durable_credit_p50']):.8f}",
                    "delta_median_net_gtco2_y_vs_independent": f"{float(values['net_after_emissions_rebound_p50']) - float(reference['net_after_emissions_rebound_p50']):.8f}",
                    "interpretation": "directional effect of moving correlated assumptions together rather than independently",
                }
            )
    return summary_rows, effect_rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"No rows to write for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {path}")


def main() -> None:
    parameters = read_parameters()
    sample_rows, scenario_rows = run_samples(parameters)
    summary_rows, effect_rows = summarize(sample_rows, scenario_rows)
    write_csv(TABLE_DIR / "aether_correlated_uncertainty_scenarios.csv", scenario_rows)
    write_csv(TABLE_DIR / "aether_correlated_uncertainty_samples.csv", sample_rows)
    write_csv(TABLE_DIR / "aether_correlated_uncertainty_summary.csv", summary_rows)
    write_csv(TABLE_DIR / "aether_correlated_uncertainty_family_effects.csv", effect_rows)


if __name__ == "__main__":
    main()

