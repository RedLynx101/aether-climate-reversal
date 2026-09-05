from __future__ import annotations

from dataclasses import dataclass, replace
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analysis" / "tables"
OUT.mkdir(parents=True, exist_ok=True)

START_YEAR = 2026
END_YEAR = 2100
GTCO2_PER_PPM = 7.8
CURRENT_EMISSIONS_GTCO2_Y = 42.2
BASELINE_ID = "rcmip_v5.1.0_ssp245_world_co2"
BASELINE_METHOD = "published evolving reference plus Joos future emissions anomalies; conditional hybrid screen, not historical reservoir calibration"
PUBLICATION_METADATA = {
    "publication_status": "quarantined_hybrid_off_reference",
    "absolute_projection_accepted": "false",
    "failure_reason": "Hybrid zero-future CO2 response fails (late rebound above initial); absolute ppm/temperature trajectories quarantined.",
}
BASELINE_DIR = ROOT / "data" / "carbon-baseline"


def load_reference_baseline() -> dict[int, dict[str, float]]:
    """Read the checksum-verified, annual-mean published reference offline.

    The extract is not an observation of today's concentration. Its paired
    emissions MUST be subtracted before applying the future-pulse response.
    """
    path = BASELINE_DIR / "rcmip_ssp245_co2_1850_2100.csv"
    manifest = json.loads((BASELINE_DIR / "provenance.json").read_text(encoding="utf-8"))
    if manifest.get("extract_hash_line_endings") != "LF":
        raise ValueError("Unsupported carbon reference extract checksum convention")
    # Git may materialize CRLF on Windows; the committed extract digest is
    # defined over canonical LF bytes, not checkout-specific newline bytes.
    if hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest() != manifest["extract_sha256"]:
        raise ValueError("Carbon reference extract checksum mismatch")
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    result: dict[int, dict[str, float]] = {int(row["year"]): {} for row in rows}
    for source_key, key, scale in [("reference_co2_ppm", "co2_ppm", 1.0),
                                   ("reference_emissions_mtco2_y", "emissions_gtco2_y", 0.001)]:
        known = {int(row["year"]): float(row[source_key]) * scale for row in rows if row[source_key]}
        for year in result:
            if year in known:
                result[year][key] = known[year]
            else:
                before = max((y for y in known if y < year), default=None)
                after = min((y for y in known if y > year), default=None)
                if before is None or after is None:
                    raise ValueError(f"Refusing to extrapolate carbon reference at {year}")
                share = (year - before) / (after - before)
                result[year][key] = known[before] + share * (known[after] - known[before])
    if len(result) != len(rows) or set(result) != set(range(1850, END_YEAR + 1)):
        raise ValueError("Carbon reference must contain every year 1850-2100 exactly once")
    if any(not math.isfinite(value) for row in result.values() for value in row.values()):
        raise ValueError("Non-finite carbon reference value")
    return result


REFERENCE_BASELINE = load_reference_baseline()
START_CO2_PPM = REFERENCE_BASELINE[START_YEAR - 1]["co2_ppm"]


def matched_control_case(emissions_policy: str) -> str:
    return f"baseline_{emissions_policy}_emissions_no_aether" if emissions_policy == "constant" else f"baseline_{emissions_policy}_no_aether"

# Joos et al. 2013 multi-model mean impulse-response coefficients.
# The terms sum to 1.0 at t=0. This is a reduced-form approximation for
# scenario comparison, not a replacement for an Earth-system model.
JOOS_TERMS = [
    (0.2173, None),
    (0.2240, 394.4),
    (0.2824, 36.54),
    (0.2763, 4.304),
]


@dataclass(frozen=True)
class Scenario:
    case: str
    display_name: str
    description: str
    emissions_policy: str
    removal_target_gtco2_y: float
    removal_target_year: int
    rebound_fraction_of_removal: float
    removal_effectiveness: float
    atmospheric_management_floor_ppm: float | None


def joos_airborne_fraction(age_years: int) -> float:
    total = 0.0
    for coefficient, tau in JOOS_TERMS:
        if tau is None:
            total += coefficient
        else:
            total += coefficient * math.exp(-age_years / tau)
    return total


def linear_between(year: int, start_year: int, start_value: float, end_year: int, end_value: float) -> float:
    if year <= start_year:
        return start_value
    if year >= end_year:
        return end_value
    fraction = (year - start_year) / (end_year - start_year)
    return start_value + fraction * (end_value - start_value)


def emissions_for_year(scenario: Scenario, year: int) -> float:
    if scenario.emissions_policy == "reference_ssp245":
        return REFERENCE_BASELINE[year]["emissions_gtco2_y"]
    if scenario.emissions_policy == "zero_future":
        return 0.0
    if scenario.emissions_policy == "constant":
        return CURRENT_EMISSIONS_GTCO2_Y
    if scenario.emissions_policy == "net_zero_2050":
        return linear_between(year, START_YEAR, CURRENT_EMISSIONS_GTCO2_Y, 2050, 0.0)
    if scenario.emissions_policy == "half_2046_zero_2060":
        if year <= 2046:
            return linear_between(year, START_YEAR, CURRENT_EMISSIONS_GTCO2_Y, 2046, CURRENT_EMISSIONS_GTCO2_Y / 2)
        return linear_between(year, 2046, CURRENT_EMISSIONS_GTCO2_Y / 2, 2060, 0.0)
    raise ValueError(f"Unknown emissions policy: {scenario.emissions_policy}")


def removal_for_year(scenario: Scenario, year: int) -> float:
    if scenario.removal_target_gtco2_y == 0:
        return 0.0
    return linear_between(year, START_YEAR, 0.0, scenario.removal_target_year, scenario.removal_target_gtco2_y)


def annual_rows(scenarios: list[Scenario]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    years = list(range(START_YEAR, END_YEAR + 1))
    irf_values = {age: joos_airborne_fraction(age) for age in range(0, END_YEAR - START_YEAR + 1)}

    for scenario in scenarios:
        pulses: list[tuple[int, float]] = []
        cumulative_emissions = 0.0
        cumulative_induced = 0.0
        cumulative_removal = 0.0
        cumulative_effective_net = 0.0
        cumulative_reference_anomaly = 0.0

        for year in years:
            emissions = emissions_for_year(scenario, year)
            planned_removal = removal_for_year(scenario, year)
            reference = REFERENCE_BASELINE[year]
            emissions_anomaly = emissions - reference["emissions_gtco2_y"]
            prior_atmospheric_burden_gtco2 = 0.0
            for pulse_year, pulse_gtco2 in pulses:
                prior_atmospheric_burden_gtco2 += pulse_gtco2 * irf_values[year - pulse_year]

            removal = planned_removal
            if scenario.atmospheric_management_floor_ppm is not None and planned_removal > 0:
                desired_burden_gtco2 = (scenario.atmospheric_management_floor_ppm - reference["co2_ppm"]) * GTCO2_PER_PPM
                effective_removal_per_tonne = scenario.removal_effectiveness - scenario.rebound_fraction_of_removal
                if effective_removal_per_tonne > 0:
                    removal_needed_gtco2 = (prior_atmospheric_burden_gtco2 + emissions_anomaly - desired_burden_gtco2) / effective_removal_per_tonne
                    removal = min(planned_removal, max(0.0, removal_needed_gtco2))

            induced = scenario.rebound_fraction_of_removal * removal
            effective_net_pulse = emissions + induced - scenario.removal_effectiveness * removal
            direct_net_pulse = emissions + induced - removal
            reference_anomaly_pulse = effective_net_pulse - reference["emissions_gtco2_y"]
            pulses.append((year, reference_anomaly_pulse))

            cumulative_emissions += emissions
            cumulative_induced += induced
            cumulative_removal += removal
            cumulative_effective_net += effective_net_pulse
            cumulative_reference_anomaly += reference_anomaly_pulse

            atmospheric_burden_gtco2 = 0.0
            for pulse_year, pulse_gtco2 in pulses:
                atmospheric_burden_gtco2 += pulse_gtco2 * irf_values[year - pulse_year]

            atmospheric_ppm = reference["co2_ppm"] + atmospheric_burden_gtco2 / GTCO2_PER_PPM
            simple_ppm = reference["co2_ppm"] + cumulative_reference_anomaly / GTCO2_PER_PPM

            rows.append({
                **PUBLICATION_METADATA,
                "case": scenario.case,
                "display_name": scenario.display_name,
                "emissions_policy": scenario.emissions_policy,
                "matched_no_aether_case": matched_control_case(scenario.emissions_policy),
                "carbon_baseline_id": BASELINE_ID,
                "carbon_baseline_method": BASELINE_METHOD,
                "year": year,
                "reference_co2_ppm": reference["co2_ppm"],
                "reference_emissions_gtco2_y": reference["emissions_gtco2_y"],
                "future_emissions_anomaly_vs_reference_gtco2_y": reference_anomaly_pulse,
                "rebound_fraction_of_removal": scenario.rebound_fraction_of_removal,
                "baseline_emissions_gtco2_y": emissions,
                "planned_gross_aether_removal_gtco2_y": planned_removal,
                "gross_aether_removal_gtco2_y": removal,
                "induced_or_delayed_emissions_gtco2_y": induced,
                "direct_net_emissions_gtco2_y_before_carbon_cycle": direct_net_pulse,
                "removal_effectiveness_multiplier": scenario.removal_effectiveness,
                "atmospheric_management_floor_ppm": scenario.atmospheric_management_floor_ppm if scenario.atmospheric_management_floor_ppm is not None else "",
                "effective_net_pulse_gtco2_y_for_reduced_form_model": effective_net_pulse,
                "cumulative_baseline_emissions_gtco2": cumulative_emissions,
                "cumulative_induced_or_delayed_emissions_gtco2": cumulative_induced,
                "cumulative_gross_aether_removal_gtco2": cumulative_removal,
                "cumulative_effective_net_gtco2": cumulative_effective_net,
                "atmospheric_burden_from_2026_anomalies_vs_reference_gtco2": atmospheric_burden_gtco2,
                "atmospheric_co2_ppm_reduced_form": atmospheric_ppm,
                "atmosphere_only_ppm_with_same_effective_net": simple_ppm,
            })
    by_key = {(row["case"], row["year"]): row for row in rows}
    for row in rows:
        control = by_key.get((row["matched_no_aether_case"], row["year"]))
        row["co2_difference_vs_matched_no_aether_ppm"] = (
            float(row["atmospheric_co2_ppm_reduced_form"]) - float(control["atmospheric_co2_ppm_reduced_form"])
            if control is not None else ""
        )
    return rows


def summary_rows(rows: list[dict[str, object]], scenarios: list[Scenario]) -> list[dict[str, object]]:
    summaries: list[dict[str, object]] = []
    by_case = {scenario.case: [] for scenario in scenarios}
    for row in rows:
        by_case[str(row["case"])].append(row)

    for scenario in scenarios:
        case_rows = by_case[scenario.case]
        peak_row = max(case_rows, key=lambda r: float(r["atmospheric_co2_ppm_reduced_form"]))
        min_row = min(case_rows, key=lambda r: float(r["atmospheric_co2_ppm_reduced_form"]))
        final = case_rows[-1]
        row_by_year = {int(row["year"]): row for row in case_rows}
        summaries.append({
            **PUBLICATION_METADATA,
            "case": scenario.case,
            "display_name": scenario.display_name,
            "description": scenario.description,
            "emissions_policy": scenario.emissions_policy,
            "matched_no_aether_case": matched_control_case(scenario.emissions_policy),
            "carbon_baseline_id": BASELINE_ID,
            "carbon_baseline_method": BASELINE_METHOD,
            "co2_difference_vs_matched_no_aether_2100_ppm": final["co2_difference_vs_matched_no_aether_ppm"],
            "removal_target_gtco2_y": scenario.removal_target_gtco2_y,
            "removal_target_year": scenario.removal_target_year,
            "rebound_fraction_of_removal": scenario.rebound_fraction_of_removal,
            "removal_effectiveness_multiplier": scenario.removal_effectiveness,
            "atmospheric_management_floor_ppm": scenario.atmospheric_management_floor_ppm if scenario.atmospheric_management_floor_ppm is not None else "",
            "co2_ppm_2046": row_by_year[2046]["atmospheric_co2_ppm_reduced_form"],
            "co2_ppm_2050": row_by_year[2050]["atmospheric_co2_ppm_reduced_form"],
            "co2_ppm_2100": final["atmospheric_co2_ppm_reduced_form"],
            "atmosphere_only_ppm_2100": final["atmosphere_only_ppm_with_same_effective_net"],
            "peak_co2_ppm": peak_row["atmospheric_co2_ppm_reduced_form"],
            "peak_year": peak_row["year"],
            "minimum_co2_ppm": min_row["atmospheric_co2_ppm_reduced_form"],
            "minimum_year": min_row["year"],
            "cumulative_baseline_emissions_gtco2_2026_2100": final["cumulative_baseline_emissions_gtco2"],
            "cumulative_induced_or_delayed_emissions_gtco2_2026_2100": final["cumulative_induced_or_delayed_emissions_gtco2"],
            "cumulative_gross_aether_removal_gtco2_2026_2100": final["cumulative_gross_aether_removal_gtco2"],
            "cumulative_effective_net_gtco2_2026_2100": final["cumulative_effective_net_gtco2"],
            "reduced_form_ppm_change_2026_2100": float(final["atmospheric_co2_ppm_reduced_form"]) - START_CO2_PPM,
        })
    return summaries


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {path}")


def default_scenarios() -> list[Scenario]:
    scenarios = [
        Scenario(
            "baseline_constant_emissions_no_aether",
            "No AETHER, constant emissions",
            "Current emissions continue with no AETHER-scale durable removal.",
            "constant",
            0.0,
            2046,
            0.0,
            1.00,
            None,
        ),
        Scenario(
            "aether_constant_emissions_no_rebound",
            "AETHER, constant emissions",
            "AETHER ramps to 100 GtCO2/year by 2046 while current emissions continue.",
            "constant",
            100.0,
            2046,
            0.0,
            0.96,
            350.0,
        ),
        Scenario(
            "aether_constant_emissions_58pct_rebound",
            "AETHER, 58% rebound",
            "AETHER ramps to 100 GtCO2/year by 2046, but induced emissions or delayed abatement reach 57.8% of gross removal.",
            "constant",
            100.0,
            2046,
            0.578,
            0.96,
            350.0,
        ),
        Scenario(
            "aether_half_2046_zero_2060",
            "AETHER plus delayed zero",
            "Emissions halve by 2046, reach zero by 2060, and AETHER ramps to 100 GtCO2/year by 2046.",
            "half_2046_zero_2060",
            100.0,
            2046,
            0.0,
            0.96,
            350.0,
        ),
        Scenario(
            "aether_net_zero_2050",
            "AETHER plus net-zero 2050",
            "Emissions reach zero by 2050 while AETHER ramps to 100 GtCO2/year by 2046.",
            "net_zero_2050",
            100.0,
            2046,
            0.0,
            0.96,
            350.0,
        ),
        Scenario(
            "aether_net_zero_2050_25pct_rebound",
            "AETHER, net-zero 2050, 25% rebound",
            "Emissions reach zero by 2050, but cheaper removal induces extra emissions equal to 25% of gross removal.",
            "net_zero_2050",
            100.0,
            2046,
            0.25,
            0.96,
            350.0,
        ),
    ]
    # Hold the non-AETHER CO2 policy fixed when attributing removal effects.
    policies_with_controls = {s.emissions_policy for s in scenarios if s.removal_target_gtco2_y == 0}
    for scenario in list(scenarios):
        if scenario.emissions_policy not in policies_with_controls:
            scenarios.append(replace(
                scenario, case=matched_control_case(scenario.emissions_policy),
                display_name=f"No AETHER, {scenario.emissions_policy}",
                description="Matched no-AETHER control with identical non-AETHER CO2 emissions policy.",
                removal_target_gtco2_y=0.0, rebound_fraction_of_removal=0.0,
                removal_effectiveness=1.0, atmospheric_management_floor_ppm=None,
            ))
            policies_with_controls.add(scenario.emissions_policy)
    return scenarios


def main() -> None:
    scenarios = default_scenarios()
    rows = annual_rows(scenarios)
    summaries = summary_rows(rows, scenarios)
    write_csv(OUT / "aether_carbon_cycle_pathways.csv", rows)
    write_csv(OUT / "aether_carbon_cycle_summary.csv", summaries)
    # Preserve the failed experiment as an explicit rejected diagnostic. Do not
    # fit/tune a historical state to make this acceptance check disappear.
    zero = replace(scenarios[0], case="diagnostic_zero_future_emissions", emissions_policy="zero_future")
    zero_rows = annual_rows([zero])
    minimum = min(zero_rows, key=lambda row: float(row["atmospheric_co2_ppm_reduced_form"]))
    first = float(zero_rows[0]["atmospheric_co2_ppm_reduced_form"])
    final = float(zero_rows[-1]["atmospheric_co2_ppm_reduced_form"])
    write_csv(OUT / "aether_carbon_baseline_diagnostics.csv", [{
        **PUBLICATION_METADATA,
        "diagnostic": "zero_future_anthropogenic_co2_no_removal",
        "carbon_baseline_id": BASELINE_ID,
        "initial_2026_diagnostic_ppm": first,
        "minimum_diagnostic_ppm": minimum["atmospheric_co2_ppm_reduced_form"],
        "minimum_year": minimum["year"],
        "final_2100_diagnostic_ppm": final,
        "late_rebound_above_minimum_ppm": final - float(minimum["atmospheric_co2_ppm_reduced_form"]),
        "final_minus_initial_ppm": final - first,
        "zero_future_response_check": "fail_unresolved_reference_response_mismatch",
        "next_validation": "Historically initialize one internally consistent emissions-driven carbon/climate model; independently compare concentration, growth, temperature, ocean heat and zero/net-negative experiments before promoting trajectories.",
    }])


if __name__ == "__main__":
    main()
