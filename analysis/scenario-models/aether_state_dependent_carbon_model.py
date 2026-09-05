from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

from aether_carbon_cycle_model import BASELINE_ID, BASELINE_METHOD, PUBLICATION_METADATA, REFERENCE_BASELINE, START_CO2_PPM


ROOT = Path(__file__).resolve().parents[2]
TABLE_DIR = ROOT / "analysis" / "tables"

GTCO2_PER_PPM = 7.8
INITIAL_PPM_2025 = START_CO2_PPM
START_YEAR = 2026
END_YEAR = 2100

JOOS_A0 = 0.2173
JOOS_TERMS = [
    (0.2240, 394.4),
    (0.2824, 36.54),
    (0.2763, 4.304),
]


@dataclass(frozen=True)
class EffectivenessCase:
    key: str
    name: str
    base_effectiveness: float
    minimum_effectiveness: float
    drawdown_penalty_per_ppm: float
    overshoot_penalty_per_ratio: float
    low_ppm_penalty: float
    management_floor_ppm: float
    interpretation: str


EFFECTIVENESS_CASES = [
    EffectivenessCase(
        key="fixed_0p96_current",
        name="Fixed 0.96 current screen",
        base_effectiveness=0.96,
        minimum_effectiveness=0.96,
        drawdown_penalty_per_ppm=0.0,
        overshoot_penalty_per_ratio=0.0,
        low_ppm_penalty=0.0,
        management_floor_ppm=350.0,
        interpretation="Current v0.31 assumption retained as the reference comparison.",
    ),
    EffectivenessCase(
        key="optimistic_active_management",
        name="Optimistic active management",
        base_effectiveness=0.98,
        minimum_effectiveness=0.84,
        drawdown_penalty_per_ppm=0.0008,
        overshoot_penalty_per_ratio=0.025,
        low_ppm_penalty=0.035,
        management_floor_ppm=350.0,
        interpretation="Assumes improved monitoring and pathway selection keep land/ocean compensation relatively low.",
    ),
    EffectivenessCase(
        key="conservative_state_dependent",
        name="Conservative state-dependent",
        base_effectiveness=0.92,
        minimum_effectiveness=0.70,
        drawdown_penalty_per_ppm=0.0018,
        overshoot_penalty_per_ratio=0.060,
        low_ppm_penalty=0.080,
        management_floor_ppm=350.0,
        interpretation="Assumes removal effectiveness declines as ppm falls and cumulative removals become large.",
    ),
    EffectivenessCase(
        key="asymmetry_stress",
        name="Asymmetry stress",
        base_effectiveness=0.85,
        minimum_effectiveness=0.60,
        drawdown_penalty_per_ppm=0.0028,
        overshoot_penalty_per_ratio=0.095,
        low_ppm_penalty=0.120,
        management_floor_ppm=350.0,
        interpretation="Stress case for stronger land/ocean compensation and emission-removal asymmetry.",
    ),
]


def irf(years_after_pulse: int) -> float:
    return JOOS_A0 + sum(coef * math.exp(-years_after_pulse / tau) for coef, tau in JOOS_TERMS)


def read_base_rows() -> dict[str, list[dict[str, str]]]:
    path = TABLE_DIR / "aether_carbon_cycle_pathways.csv"
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(row["case"], []).append(row)
    for case_rows in grouped.values():
        case_rows.sort(key=lambda item: int(item["year"]))
    return grouped


def f(value: float, digits: int = 6) -> str:
    return f"{value:.{digits}f}"


def effectiveness(case: EffectivenessCase, prior_ppm: float, cumulative_gross: float, cumulative_positive: float) -> float:
    if case.key == "fixed_0p96_current":
        return case.base_effectiveness
    drawdown_ppm = max(0.0, INITIAL_PPM_2025 - prior_ppm)
    overshoot_ratio = cumulative_gross / max(1.0, cumulative_positive)
    overshoot_penalty = max(0.0, overshoot_ratio - 1.0) * case.overshoot_penalty_per_ratio
    low_ppm_proximity = max(0.0, (390.0 - prior_ppm) / 40.0)
    value = (
        case.base_effectiveness
        - drawdown_ppm * case.drawdown_penalty_per_ppm
        - overshoot_penalty
        - low_ppm_proximity * case.low_ppm_penalty
    )
    return max(case.minimum_effectiveness, min(1.0, value))


def atmospheric_burden(pulses: list[tuple[int, float]], year: int) -> float:
    return sum(pulse * irf(year - pulse_year) for pulse_year, pulse in pulses)


def simulate_case(base_case: str, rows: list[dict[str, str]], eff_case: EffectivenessCase) -> list[dict[str, object]]:
    pulses: list[tuple[int, float]] = []
    output: list[dict[str, object]] = []
    cumulative_positive = 0.0
    cumulative_planned_gross = 0.0
    cumulative_gross = 0.0
    cumulative_effective_removal = 0.0
    cumulative_direct_net = 0.0
    display_name = rows[0]["display_name"]

    for row in rows:
        year = int(row["year"])
        prior_year = year - 1
        prior_burden = atmospheric_burden(pulses, prior_year) if pulses else 0.0
        prior_ppm = REFERENCE_BASELINE[prior_year]["co2_ppm"] + prior_burden / GTCO2_PER_PPM
        reference = REFERENCE_BASELINE[year]

        baseline = float(row["baseline_emissions_gtco2_y"])
        rebound_fraction = float(row["rebound_fraction_of_removal"])
        planned_gross = float(row["planned_gross_aether_removal_gtco2_y"])
        eff = effectiveness(eff_case, prior_ppm, cumulative_gross, cumulative_positive)
        desired_effective_removal = planned_gross * eff
        actual_effective_removal = desired_effective_removal
        actual_gross = planned_gross

        preliminary_pulse = baseline + rebound_fraction * planned_gross - desired_effective_removal - reference["emissions_gtco2_y"]
        preliminary_burden = atmospheric_burden(pulses + [(year, preliminary_pulse)], year)
        preliminary_ppm = reference["co2_ppm"] + preliminary_burden / GTCO2_PER_PPM
        throttled = False
        floor_gap = eff_case.management_floor_ppm - preliminary_ppm
        if floor_gap > 0 and desired_effective_removal > 0 and eff > rebound_fraction:
            required_pulse_increase = floor_gap * GTCO2_PER_PPM
            actual_gross = max(0.0, planned_gross - required_pulse_increase / (eff - rebound_fraction))
            actual_effective_removal = actual_gross * eff
            throttled = actual_gross < planned_gross - 1e-9

        induced = rebound_fraction * actual_gross
        positive = baseline + induced
        direct_net_pulse = positive - actual_effective_removal
        anomaly_pulse = direct_net_pulse - reference["emissions_gtco2_y"]
        pulses.append((year, anomaly_pulse))
        burden = atmospheric_burden(pulses, year)
        ppm = reference["co2_ppm"] + burden / GTCO2_PER_PPM
        atmosphere_only_ppm = reference["co2_ppm"] + sum(pulse for _, pulse in pulses) / GTCO2_PER_PPM

        cumulative_positive += positive
        cumulative_planned_gross += planned_gross
        cumulative_gross += actual_gross
        cumulative_effective_removal += actual_effective_removal
        cumulative_direct_net += direct_net_pulse

        output.append(
            {
                "base_case": base_case,
                **PUBLICATION_METADATA,
                "base_display_name": display_name,
                "emissions_policy": row["emissions_policy"],
                "matched_no_aether_case": row["matched_no_aether_case"],
                "carbon_baseline_id": BASELINE_ID,
                "carbon_baseline_method": BASELINE_METHOD,
                "effectiveness_case": eff_case.key,
                "effectiveness_display_name": eff_case.name,
                "year": year,
                "reference_co2_ppm": f(reference["co2_ppm"]),
                "reference_emissions_gtco2_y": f(reference["emissions_gtco2_y"]),
                "future_emissions_anomaly_vs_reference_gtco2_y": f(anomaly_pulse),
                "baseline_emissions_gtco2_y": f(baseline, 6),
                "induced_or_delayed_emissions_gtco2_y": f(induced, 6),
                "positive_emissions_gtco2_y": f(positive, 6),
                "planned_gross_removal_gtco2_y": f(planned_gross, 6),
                "actual_gross_removal_gtco2_y": f(actual_gross, 6),
                "removal_effectiveness_multiplier": f(eff, 6),
                "effective_removal_gtco2_y": f(actual_effective_removal, 6),
                "direct_net_pulse_gtco2_y": f(direct_net_pulse, 6),
                "atmospheric_co2_ppm_reduced_form": f(ppm, 6),
                "atmosphere_only_ppm_same_direct_net": f(atmosphere_only_ppm, 6),
                "compensation_vs_atmosphere_only_ppm": f(ppm - atmosphere_only_ppm, 6),
                "management_floor_ppm": f(eff_case.management_floor_ppm, 6),
                "floor_throttled": "true" if throttled else "false",
                "cumulative_positive_emissions_gtco2": f(cumulative_positive, 6),
                "cumulative_planned_gross_removal_gtco2": f(cumulative_planned_gross, 6),
                "cumulative_actual_gross_removal_gtco2": f(cumulative_gross, 6),
                "cumulative_effective_removal_gtco2": f(cumulative_effective_removal, 6),
                "cumulative_direct_net_pulse_gtco2": f(cumulative_direct_net, 6),
            }
        )
    return output


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"No rows to write for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {path}")


def build_summary(pathway_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], list[dict[str, object]]] = {}
    for row in pathway_rows:
        grouped.setdefault((str(row["base_case"]), str(row["effectiveness_case"])), []).append(row)

    fixed_2100: dict[str, float] = {}
    for (base_case, eff_case), rows in grouped.items():
        if eff_case == "fixed_0p96_current":
            fixed_2100[base_case] = float([row for row in rows if int(row["year"]) == 2100][0]["atmospheric_co2_ppm_reduced_form"])

    summary: list[dict[str, object]] = []
    for (base_case, eff_case), rows in sorted(grouped.items()):
        rows.sort(key=lambda row: int(row["year"]))
        by_year = {int(row["year"]): row for row in rows}
        final = rows[-1]
        minimum = min(rows, key=lambda row: float(row["atmospheric_co2_ppm_reduced_form"]))
        cumulative_gross = float(final["cumulative_actual_gross_removal_gtco2"])
        cumulative_effective = float(final["cumulative_effective_removal_gtco2"])
        cumulative_planned = float(final["cumulative_planned_gross_removal_gtco2"])
        fixed = fixed_2100.get(base_case)
        ppm_penalty = 0.0 if fixed is None else float(by_year[2100]["atmospheric_co2_ppm_reduced_form"]) - fixed
        summary.append(
            {
                "base_case": base_case,
                **PUBLICATION_METADATA,
                "base_display_name": str(final["base_display_name"]),
                "effectiveness_case": eff_case,
                "effectiveness_display_name": str(final["effectiveness_display_name"]),
                "emissions_policy": final["emissions_policy"],
                "matched_no_aether_case": final["matched_no_aether_case"],
                "carbon_baseline_id": BASELINE_ID,
                "carbon_baseline_method": BASELINE_METHOD,
                "co2_difference_vs_matched_no_aether_2100_ppm": final["co2_difference_vs_matched_no_aether_ppm"],
                "co2_ppm_2046": f(float(by_year[2046]["atmospheric_co2_ppm_reduced_form"]), 6),
                "co2_ppm_2050": f(float(by_year[2050]["atmospheric_co2_ppm_reduced_form"]), 6),
                "co2_ppm_2100": f(float(by_year[2100]["atmospheric_co2_ppm_reduced_form"]), 6),
                "minimum_co2_ppm": f(float(minimum["atmospheric_co2_ppm_reduced_form"]), 6),
                "minimum_co2_year": minimum["year"],
                "cumulative_planned_gross_removal_gtco2": f(cumulative_planned, 6),
                "cumulative_actual_gross_removal_gtco2": f(cumulative_gross, 6),
                "cumulative_effective_removal_gtco2": f(cumulative_effective, 6),
                "actual_to_planned_gross_ratio": f(cumulative_gross / cumulative_planned if cumulative_planned > 0 else 0.0, 6),
                "effective_to_actual_gross_ratio": f(cumulative_effective / cumulative_gross if cumulative_gross > 0 else 0.0, 6),
                "ppm_penalty_vs_fixed_current_2100": f(ppm_penalty, 6),
                "paper_use_rule": "quarantined off-reference diagnostic; requires internally consistent historically initialized emissions-driven validation, not forcing-mode agreement",
            }
        )
    return summary


def main() -> None:
    base_rows = read_base_rows()
    pathway_rows: list[dict[str, object]] = []
    for base_case, rows in sorted(base_rows.items()):
        for eff_case in EFFECTIVENESS_CASES:
            pathway_rows.extend(simulate_case(base_case, rows, eff_case))

    by_key = {(row["base_case"], row["effectiveness_case"], row["year"]): row for row in pathway_rows}
    for row in pathway_rows:
        control = by_key[(row["matched_no_aether_case"], row["effectiveness_case"], row["year"])]
        row["co2_difference_vs_matched_no_aether_ppm"] = f(float(row["atmospheric_co2_ppm_reduced_form"]) - float(control["atmospheric_co2_ppm_reduced_form"]))

    case_rows = [
        {
            "effectiveness_case": case.key,
            "effectiveness_display_name": case.name,
            "base_effectiveness": f(case.base_effectiveness, 6),
            "minimum_effectiveness": f(case.minimum_effectiveness, 6),
            "drawdown_penalty_per_ppm": f(case.drawdown_penalty_per_ppm, 8),
            "overshoot_penalty_per_ratio": f(case.overshoot_penalty_per_ratio, 6),
            "low_ppm_penalty": f(case.low_ppm_penalty, 6),
            "management_floor_ppm": f(case.management_floor_ppm, 6),
            "interpretation": case.interpretation,
        }
        for case in EFFECTIVENESS_CASES
    ]

    summary_rows = build_summary(pathway_rows)
    write_rows(TABLE_DIR / "aether_removal_effectiveness_cases.csv", case_rows)
    write_rows(TABLE_DIR / "aether_state_dependent_carbon_pathways.csv", pathway_rows)
    write_rows(TABLE_DIR / "aether_state_dependent_carbon_summary.csv", summary_rows)


if __name__ == "__main__":
    main()

