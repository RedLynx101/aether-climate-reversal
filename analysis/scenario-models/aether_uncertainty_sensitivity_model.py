from __future__ import annotations

import csv
import math
import random
import statistics
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analysis" / "tables"
OUT.mkdir(parents=True, exist_ok=True)

SEED = 462046
SAMPLES = 20_000
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


PARAMETERS = [
    Parameter("energy_gj_tco2", "Full-system energy intensity", 1.25, 2.25, 5.50, "GJ/tCO2", "Lower values make the clean-energy constraint less binding."),
    Parameter("clean_addition_growth_rate", "Annual clean-addition growth", 0.04, 0.15, 0.24, "fraction/year", "Growth rate for annual global clean-generation additions through 2046."),
    Parameter("aether_clean_share", "AETHER share of new clean generation", 0.15, 0.50, 0.75, "fraction", "Share of new clean generation that can be allocated to AETHER after other demand claims."),
    Parameter("clean_deliverability_fraction", "Clean-energy deliverability", 0.55, 0.85, 1.00, "fraction", "Discount for interconnection, firming, transmission, downtime, and siting mismatch."),
    Parameter("robot_output_growth_rate", "Annual robot-output growth", 0.10, 0.24, 0.38, "fraction/year", "Growth rate for robot production relevant to AETHER construction and operations."),
    Parameter("aether_robot_share", "AETHER share of robot output", 0.05, 0.25, 0.45, "fraction", "Share of robot output available for AETHER rather than the rest of the economy."),
    Parameter("robots_per_mtco2_y_capacity", "Robots per MtCO2/year capacity", 15.0, 75.0, 400.0, "robots per Mt/y", "Lower values mean each robot-mediated deployment system supports more removal capacity."),
    Parameter("storage_terminal_gtco2_y", "Terminal storage capacity", 35.0, 105.0, 160.0, "GtCO2/year", "Geologic, mineral, ocean, biomass, and product storage throughput available by 2046."),
    Parameter("cost_usd_tco2", "Delivered cost", 25.0, 75.0, 220.0, "USD/tCO2", "Full delivered cost after learning, energy, storage, MRV, finance, and operations."),
    Parameter("annual_budget_trillion_usd", "Annual budget", 2.0, 7.0, 14.0, "trillion USD/year", "Public, private, and treaty-backed annual spending capacity."),
    Parameter("durability_fraction_100y", "100-year durable credit fraction", 0.68, 0.85, 0.96, "fraction", "Fraction of gross captured CO2 credited after lifecycle and 100-year durability haircuts."),
    Parameter("residual_emissions_2046_gtco2_y", "Residual emissions in 2046", 5.0, 15.0, 35.0, "GtCO2/year", "Positive emissions remaining when the AETHER system reaches industrial scale."),
    Parameter("rebound_fraction_of_gross", "Rebound or delayed-abatement fraction", 0.02, 0.18, 0.65, "fraction of gross removal", "Extra emissions or delayed abatement induced by cheap removal."),
    Parameter("gross_overbuild_factor", "Gross overbuild factor", 1.00, 1.18, 1.35, "multiple of 100 Gt/y", "Program design capacity above 100 Gt/y to cover durability and downtime."),
    Parameter("execution_realization_fraction", "Execution realization", 0.65, 0.95, 1.08, "fraction", "Coordination, permitting, supply-chain, and operations realization of designed capacity."),
]


def draw_triangular(rng: random.Random, p: Parameter) -> float:
    return rng.triangular(p.low, p.high, p.mode)


def cumulative_clean_twh(growth_rate: float, share: float, deliverability: float) -> float:
    gross_new_clean = sum(BASE_CLEAN_ELECTRICITY_ADDITION_TWH_Y * ((1 + growth_rate) ** t) for t in range(21))
    return gross_new_clean * share * deliverability


def robots_in_service(growth_rate: float, share: float) -> float:
    return sum(BASE_ROBOT_OUTPUT_Y * ((1 + growth_rate) ** t) * share for t in range(21 - ROBOT_SERVICE_LIFE_Y, 21))


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


def mean_bool(rows: list[dict[str, float]], field: str) -> float:
    return sum(float(r[field]) for r in rows) / len(rows)


def pearson(xs: list[float], ys: list[float]) -> float:
    if len(xs) != len(ys) or len(xs) < 3:
        return float("nan")
    mx = statistics.fmean(xs)
    my = statistics.fmean(ys)
    dx = [x - mx for x in xs]
    dy = [y - my for y in ys]
    denom = math.sqrt(sum(x * x for x in dx) * sum(y * y for y in dy))
    if denom == 0:
        return 0.0
    return sum(x * y for x, y in zip(dx, dy)) / denom


def standardized_mean_difference(values: list[float], passes: list[float]) -> float:
    pass_values = [v for v, p in zip(values, passes) if p >= 0.5]
    fail_values = [v for v, p in zip(values, passes) if p < 0.5]
    if not pass_values or not fail_values:
        return 0.0
    sd = statistics.pstdev(values)
    if sd == 0:
        return 0.0
    return (statistics.fmean(pass_values) - statistics.fmean(fail_values)) / sd


def run() -> None:
    rng = random.Random(SEED)
    rows: list[dict[str, float | str]] = []

    for sample_id in range(1, SAMPLES + 1):
        sample = {p.field: draw_triangular(rng, p) for p in PARAMETERS}

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

        row = {
            "sample_id": sample_id,
            **sample,
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
        rows.append(row)

    sample_path = OUT / "aether_uncertainty_samples.csv"
    fieldnames = list(rows[0].keys())
    with sample_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    gross_values = [float(r["gross_capacity_gtco2_y"]) for r in rows]
    durable_values = [float(r["durable_100y_credit_gtco2_y"]) for r in rows]
    net_values = [float(r["net_after_emissions_and_rebound_gtco2_y"]) for r in rows]

    summary_rows = [
        ("sample_count", float(SAMPLES), "samples", "Monte Carlo draws using explicit AETHER v0.8 assumption ranges."),
        ("gross_100_probability", mean_bool(rows, "gross_100_pass"), "probability", "Share of samples with gross terminal capacity at or above 100 GtCO2/year."),
        ("durable_100_probability", mean_bool(rows, "durable_100_pass"), "probability", "Share of samples crediting at least 100 GtCO2/year after lifecycle and 100-year durability haircuts."),
        ("positive_climate_reversal_probability", mean_bool(rows, "positive_climate_reversal_pass"), "probability", "Share of samples with positive net removal after residual emissions and rebound."),
        ("strong_reversal_probability", mean_bool(rows, "strong_reversal_pass"), "probability", "Share of samples with net removal after emissions and rebound at least as large as current annual anthropogenic emissions."),
        ("gross_capacity_p10", quantile(gross_values, 0.10), "GtCO2/year", "10th percentile terminal gross capacity."),
        ("gross_capacity_p50", quantile(gross_values, 0.50), "GtCO2/year", "Median terminal gross capacity."),
        ("gross_capacity_p90", quantile(gross_values, 0.90), "GtCO2/year", "90th percentile terminal gross capacity."),
        ("durable_credit_p10", quantile(durable_values, 0.10), "GtCO2/year", "10th percentile 100-year durable credited removal."),
        ("durable_credit_p50", quantile(durable_values, 0.50), "GtCO2/year", "Median 100-year durable credited removal."),
        ("durable_credit_p90", quantile(durable_values, 0.90), "GtCO2/year", "90th percentile 100-year durable credited removal."),
        ("net_after_emissions_rebound_p10", quantile(net_values, 0.10), "GtCO2/year", "10th percentile net removal after residual emissions and rebound."),
        ("net_after_emissions_rebound_p50", quantile(net_values, 0.50), "GtCO2/year", "Median net removal after residual emissions and rebound."),
        ("net_after_emissions_rebound_p90", quantile(net_values, 0.90), "GtCO2/year", "90th percentile net removal after residual emissions and rebound."),
        ("median_clean_energy_available", quantile([float(r["clean_energy_available_twh_y"]) for r in rows], 0.50), "TWh/year", "Median AETHER-deliverable clean generation in 2046."),
        ("median_robot_capacity", quantile([float(r["robot_limited_capacity_gtco2_y"]) for r in rows], 0.50), "GtCO2/year", "Median robot-limited terminal capacity."),
        ("median_storage_capacity", quantile([float(r["storage_capacity_gtco2_y"]) for r in rows], 0.50), "GtCO2/year", "Median storage-limited terminal capacity."),
        ("median_budget_capacity", quantile([float(r["budget_limited_capacity_gtco2_y"]) for r in rows], 0.50), "GtCO2/year", "Median budget-limited terminal capacity."),
    ]
    with (OUT / "aether_uncertainty_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["metric", "value", "unit", "interpretation"])
        writer.writeheader()
        writer.writerows({"metric": m, "value": v, "unit": u, "interpretation": interp} for m, v, u, interp in summary_rows)

    constraints = ["clean_energy", "robot_supply", "storage", "budget", "program_execution"]
    bottleneck_rows = []
    failed_durable = [r for r in rows if float(r["durable_100_pass"]) < 0.5]
    for constraint in constraints:
        count_all = sum(1 for r in rows if r["binding_constraint"] == constraint)
        count_failed = sum(1 for r in failed_durable if r["binding_constraint"] == constraint)
        bottleneck_rows.append({
            "binding_constraint": constraint,
            "count_all_samples": count_all,
            "share_all_samples": count_all / len(rows),
            "count_failed_durable_samples": count_failed,
            "share_failed_durable_samples": count_failed / len(failed_durable) if failed_durable else 0.0,
        })
    with (OUT / "aether_uncertainty_bottlenecks.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(bottleneck_rows[0].keys()))
        writer.writeheader()
        writer.writerows(bottleneck_rows)

    pass_flags = [float(r["durable_100_pass"]) for r in rows]
    sensitivity_rows = []
    for p in PARAMETERS:
        values = [float(r[p.field]) for r in rows]
        sensitivity_rows.append({
            "parameter": p.field,
            "label": p.label,
            "unit": p.unit,
            "assumption_low": p.low,
            "assumption_mode": p.mode,
            "assumption_high": p.high,
            "correlation_with_gross_capacity": pearson(values, gross_values),
            "correlation_with_durable_credit": pearson(values, durable_values),
            "correlation_with_net_climate": pearson(values, net_values),
            "standardized_mean_difference_for_durable_100_pass": standardized_mean_difference(values, pass_flags),
            "interpretation": p.interpretation,
        })
    sensitivity_rows.sort(key=lambda r: abs(float(r["correlation_with_net_climate"])), reverse=True)
    with (OUT / "aether_uncertainty_sensitivity.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(sensitivity_rows[0].keys()))
        writer.writeheader()
        writer.writerows(sensitivity_rows)

    parameter_rows = [
        {
            "parameter": p.field,
            "label": p.label,
            "low": p.low,
            "mode": p.mode,
            "high": p.high,
            "unit": p.unit,
            "interpretation": p.interpretation,
        }
        for p in PARAMETERS
    ]
    with (OUT / "aether_uncertainty_assumptions.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(parameter_rows[0].keys()))
        writer.writeheader()
        writer.writerows(parameter_rows)

    print(f"Wrote {sample_path}")
    print(f"Wrote {OUT / 'aether_uncertainty_summary.csv'}")
    print(f"Wrote {OUT / 'aether_uncertainty_sensitivity.csv'}")
    print(f"Wrote {OUT / 'aether_uncertainty_bottlenecks.csv'}")
    print(f"Wrote {OUT / 'aether_uncertainty_assumptions.csv'}")


if __name__ == "__main__":
    run()

