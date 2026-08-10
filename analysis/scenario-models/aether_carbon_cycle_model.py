from __future__ import annotations

from dataclasses import dataclass
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analysis" / "tables"
OUT.mkdir(parents=True, exist_ok=True)

START_YEAR = 2026
END_YEAR = 2100
START_CO2_PPM = 428.53
GTCO2_PER_PPM = 7.8
CURRENT_EMISSIONS_GTCO2_Y = 42.2

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

        for year in years:
            emissions = emissions_for_year(scenario, year)
            planned_removal = removal_for_year(scenario, year)
            prior_atmospheric_burden_gtco2 = 0.0
            for pulse_year, pulse_gtco2 in pulses:
                prior_atmospheric_burden_gtco2 += pulse_gtco2 * irf_values[year - pulse_year]

            removal = planned_removal
            if scenario.atmospheric_management_floor_ppm is not None and planned_removal > 0:
                desired_burden_gtco2 = (scenario.atmospheric_management_floor_ppm - START_CO2_PPM) * GTCO2_PER_PPM
                effective_removal_per_tonne = scenario.removal_effectiveness - scenario.rebound_fraction_of_removal
                if effective_removal_per_tonne > 0:
                    removal_needed_gtco2 = (prior_atmospheric_burden_gtco2 + emissions - desired_burden_gtco2) / effective_removal_per_tonne
                    removal = min(planned_removal, max(0.0, removal_needed_gtco2))

            induced = scenario.rebound_fraction_of_removal * removal
            effective_net_pulse = emissions + induced - scenario.removal_effectiveness * removal
            direct_net_pulse = emissions + induced - removal
            pulses.append((year, effective_net_pulse))

            cumulative_emissions += emissions
            cumulative_induced += induced
            cumulative_removal += removal
            cumulative_effective_net += effective_net_pulse

            atmospheric_burden_gtco2 = 0.0
            for pulse_year, pulse_gtco2 in pulses:
                atmospheric_burden_gtco2 += pulse_gtco2 * irf_values[year - pulse_year]

            atmospheric_ppm = START_CO2_PPM + atmospheric_burden_gtco2 / GTCO2_PER_PPM
            simple_ppm = START_CO2_PPM + cumulative_effective_net / GTCO2_PER_PPM

            rows.append({
                "case": scenario.case,
                "display_name": scenario.display_name,
                "year": year,
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
                "atmospheric_burden_from_2026_pulses_gtco2": atmospheric_burden_gtco2,
                "atmospheric_co2_ppm_reduced_form": atmospheric_ppm,
                "atmosphere_only_ppm_with_same_effective_net": simple_ppm,
            })
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
            "case": scenario.case,
            "display_name": scenario.display_name,
            "description": scenario.description,
            "emissions_policy": scenario.emissions_policy,
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


def main() -> None:
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
    rows = annual_rows(scenarios)
    summaries = summary_rows(rows, scenarios)
    write_csv(OUT / "aether_carbon_cycle_pathways.csv", rows)
    write_csv(OUT / "aether_carbon_cycle_summary.csv", summaries)


if __name__ == "__main__":
    main()
