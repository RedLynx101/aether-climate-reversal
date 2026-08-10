from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TABLE_DIR = ROOT / "analysis" / "tables"

CARBON_CYCLE_PATH = TABLE_DIR / "aether_carbon_cycle_pathways.csv"
PATHWAY_OUTPUT = TABLE_DIR / "aether_climate_emulator_pathways.csv"
SUMMARY_OUTPUT = TABLE_DIR / "aether_climate_emulator_summary.csv"
FORCING_OUTPUT = TABLE_DIR / "aether_climate_emulator_forcing_assumptions.csv"
CALIBRATION_OUTPUT = TABLE_DIR / "aether_climate_emulator_calibration.csv"

PREINDUSTRIAL_CO2_PPM = 278.0
CO2_DOUBLING_ERF_W_M2 = 3.93
ECS_C = 3.0
TCR_TARGET_C = 1.8


@dataclass(frozen=True)
class ForcingPolicy:
    key: str
    name: str
    nonco2_2026: float
    nonco2_2050: float
    nonco2_2100: float
    aerosol_2026: float
    aerosol_2050: float
    aerosol_2100: float
    basis: str
    caveat: str


FORCING_POLICIES = [
    ForcingPolicy(
        key="co2_only_screen",
        name="CO2-only emulator screen",
        nonco2_2026=0.0,
        nonco2_2050=0.0,
        nonco2_2100=0.0,
        aerosol_2026=0.0,
        aerosol_2050=0.0,
        aerosol_2100=0.0,
        basis="Comparison case. Holds non-CO2 and aerosol terms at zero so the dynamic emulator can be compared with the static CO2-only proxy.",
        caveat="Not a total warming estimate; comparison case only.",
    ),
    ForcingPolicy(
        key="mitigation_with_aerosol_cleanup",
        name="Mitigation with aerosol cleanup",
        nonco2_2026=1.20,
        nonco2_2050=0.75,
        nonco2_2100=0.45,
        aerosol_2026=-0.70,
        aerosol_2050=-0.25,
        aerosol_2100=-0.05,
        basis="Scenario assumption anchored to AR6 forcing literature: positive non-CO2 forcing declines while aerosol cooling is reduced by air-pollution cleanup.",
        caveat="Non-CO2 and aerosol paths are policy screens, not forecasts.",
    ),
    ForcingPolicy(
        key="nonco2_delay_aerosol_unmasking",
        name="Delayed non-CO2 mitigation plus aerosol unmasking",
        nonco2_2026=1.20,
        nonco2_2050=1.15,
        nonco2_2100=1.05,
        aerosol_2026=-0.70,
        aerosol_2050=-0.15,
        aerosol_2100=-0.05,
        basis="Stress test. Non-CO2 forcing stays high while aerosol cooling weakens, exposing warming that CO2-only accounting misses.",
        caveat="Useful failure case for AETHER governance; not a central forecast.",
    ),
    ForcingPolicy(
        key="active_full_forcing_management",
        name="Active full-forcing management",
        nonco2_2026=1.20,
        nonco2_2050=0.55,
        nonco2_2100=0.20,
        aerosol_2026=-0.70,
        aerosol_2050=-0.15,
        aerosol_2100=0.00,
        basis="Optimistic management case. CO2 removal is paired with strong methane, nitrous-oxide, ozone-precursor, and industrial-emissions control.",
        caveat="Requires non-CO2 policy and technology success outside the AETHER CO2-removal system.",
    ),
]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"No rows to write for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {path}")


def f(value: float, digits: int = 6) -> str:
    return f"{value:.{digits}f}"


def co2_erf(ppm: float) -> float:
    if ppm <= 0:
        raise ValueError(f"CO2 ppm must be positive, got {ppm}")
    return CO2_DOUBLING_ERF_W_M2 * math.log(ppm / PREINDUSTRIAL_CO2_PPM, 2)


def interpolate(year: int, y0: int, v0: float, y1: int, v1: float) -> float:
    if year <= y0:
        return v0
    if year >= y1:
        return v1
    share = (year - y0) / (y1 - y0)
    return v0 + share * (v1 - v0)


def policy_forcing(policy: ForcingPolicy, year: int) -> tuple[float, float]:
    if year < 2026:
        progress = max(0.0, min(1.0, (year - 1850) / (2026 - 1850)))
        progress = progress ** 1.25
        return policy.nonco2_2026 * progress, policy.aerosol_2026 * progress
    if year <= 2050:
        nonco2 = interpolate(year, 2026, policy.nonco2_2026, 2050, policy.nonco2_2050)
        aerosol = interpolate(year, 2026, policy.aerosol_2026, 2050, policy.aerosol_2050)
        return nonco2, aerosol
    nonco2 = interpolate(year, 2050, policy.nonco2_2050, 2100, policy.nonco2_2100)
    aerosol = interpolate(year, 2050, policy.aerosol_2050, 2100, policy.aerosol_2100)
    return nonco2, aerosol


def simulate_energy_balance(
    forcings: list[float],
    mixed_heat_capacity_wyr_m2_c: float,
    deep_heat_capacity_wyr_m2_c: float,
    exchange_w_m2_c: float,
) -> list[tuple[float, float, float]]:
    lambda_w_m2_c = CO2_DOUBLING_ERF_W_M2 / ECS_C
    surface_temp = 0.0
    deep_temp = 0.0
    rows: list[tuple[float, float, float]] = []
    for forcing in forcings:
        ocean_heat_uptake = exchange_w_m2_c * (surface_temp - deep_temp)
        surface_temp += (forcing - lambda_w_m2_c * surface_temp - ocean_heat_uptake) / mixed_heat_capacity_wyr_m2_c
        deep_temp += ocean_heat_uptake / deep_heat_capacity_wyr_m2_c
        rows.append((surface_temp, deep_temp, ocean_heat_uptake))
    return rows


def calibrate_parameters() -> tuple[dict[str, float], dict[str, object]]:
    tcr_forcings = [co2_erf(PREINDUSTRIAL_CO2_PPM * (1.01 ** year)) for year in range(1, 71)]
    best: tuple[float, float, float, float] | None = None
    for mixed in [6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]:
        for deep in [80.0, 100.0, 120.0, 140.0, 160.0]:
            for exchange_step in range(6, 31):
                exchange = exchange_step / 20.0
                tcr_path = simulate_energy_balance(tcr_forcings, mixed, deep, exchange)
                achieved = tcr_path[-1][0]
                error = abs(achieved - TCR_TARGET_C)
                candidate = (error, mixed, deep, exchange)
                if best is None or candidate < best:
                    best = candidate
    assert best is not None
    _, mixed, deep, exchange = best
    achieved_tcr = simulate_energy_balance(tcr_forcings, mixed, deep, exchange)[-1][0]
    params = {
        "mixed_heat_capacity_wyr_m2_c": mixed,
        "deep_ocean_heat_capacity_wyr_m2_c": deep,
        "ocean_heat_exchange_w_m2_c": exchange,
        "climate_feedback_lambda_w_m2_c": CO2_DOUBLING_ERF_W_M2 / ECS_C,
    }
    row = {
        "calibration_target": "central AR6-style screening pair",
        "ecs_target_c": f(ECS_C, 3),
        "tcr_target_c": f(TCR_TARGET_C, 3),
        "achieved_tcr_c": f(achieved_tcr, 3),
        "mixed_heat_capacity_wyr_m2_c": f(mixed, 3),
        "deep_ocean_heat_capacity_wyr_m2_c": f(deep, 3),
        "ocean_heat_exchange_w_m2_c": f(exchange, 3),
        "climate_feedback_lambda_w_m2_c": f(params["climate_feedback_lambda_w_m2_c"], 3),
        "calibration_note": "Grid-search two-box screening emulator; calibrated to approximate TCR while ECS is set by lambda = F2x/ECS. This is not FAIR and not an Earth-system model.",
    }
    return params, row


def main() -> None:
    carbon_rows = read_rows(CARBON_CYCLE_PATH)
    by_case: dict[str, list[dict[str, str]]] = {}
    for row in carbon_rows:
        by_case.setdefault(row["case"], []).append(row)
    for rows in by_case.values():
        rows.sort(key=lambda row: int(row["year"]))

    params, calibration_row = calibrate_parameters()
    pathway_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []

    for case, case_rows in by_case.items():
        future_by_year = {int(row["year"]): row for row in case_rows}
        first_future = case_rows[0]
        first_ppm = float(first_future["atmospheric_co2_ppm_reduced_form"])
        display_name = first_future["display_name"]

        for policy in FORCING_POLICIES:
            years = list(range(1850, 2101))
            forcing_inputs: list[dict[str, float]] = []
            for year in years:
                if year <= 2025:
                    progress = max(0.0, min(1.0, (year - 1850) / (2026 - 1850)))
                    ppm = PREINDUSTRIAL_CO2_PPM + (first_ppm - PREINDUSTRIAL_CO2_PPM) * (progress ** 1.15)
                else:
                    ppm = float(future_by_year[year]["atmospheric_co2_ppm_reduced_form"])
                co2_forcing = co2_erf(ppm)
                nonco2, aerosol = policy_forcing(policy, year)
                forcing_inputs.append({
                    "year": float(year),
                    "co2_ppm": ppm,
                    "co2_erf": co2_forcing,
                    "nonco2": nonco2,
                    "aerosol": aerosol,
                    "total": co2_forcing + nonco2 + aerosol,
                })

            simulated = simulate_energy_balance(
                [row["total"] for row in forcing_inputs],
                params["mixed_heat_capacity_wyr_m2_c"],
                params["deep_ocean_heat_capacity_wyr_m2_c"],
                params["ocean_heat_exchange_w_m2_c"],
            )
            temp_by_year: dict[int, tuple[float, float, float]] = {
                int(row["year"]): simulated[index]
                for index, row in enumerate(forcing_inputs)
            }
            temp_2026 = temp_by_year[2026][0]

            case_policy_rows: list[dict[str, object]] = []
            for row in forcing_inputs:
                year = int(row["year"])
                if year < 2026:
                    continue
                surface_temp, deep_temp, uptake = temp_by_year[year]
                out = {
                    "case": case,
                    "display_name": display_name,
                    "forcing_policy": policy.key,
                    "forcing_policy_name": policy.name,
                    "year": year,
                    "co2_ppm": f(row["co2_ppm"], 6),
                    "co2_erf_w_m2": f(row["co2_erf"], 6),
                    "non_co2_positive_forcing_w_m2": f(row["nonco2"], 6),
                    "aerosol_forcing_w_m2": f(row["aerosol"], 6),
                    "total_erf_w_m2": f(row["total"], 6),
                    "surface_temperature_anomaly_c": f(surface_temp, 6),
                    "deep_ocean_temperature_index_c": f(deep_temp, 6),
                    "ocean_heat_uptake_w_m2": f(uptake, 6),
                    "temperature_change_vs_2026_c": f(surface_temp - temp_2026, 6),
                    "emulator_caveat": "Two-box screening emulator with scenario non-CO2 and aerosol forcing; not FAIR, not CMIP, and not publication-grade attribution.",
                }
                pathway_rows.append(out)
                case_policy_rows.append(out)

            by_year = {int(row["year"]): row for row in case_policy_rows}
            final = by_year[2100]
            row_2026 = by_year[2026]
            row_2050 = by_year[2050]
            peak = max(case_policy_rows, key=lambda row: float(row["surface_temperature_anomaly_c"]))
            minimum = min(case_policy_rows, key=lambda row: float(row["surface_temperature_anomaly_c"]))
            summary_rows.append({
                "case": case,
                "display_name": display_name,
                "forcing_policy": policy.key,
                "forcing_policy_name": policy.name,
                "temperature_2026_c": row_2026["surface_temperature_anomaly_c"],
                "temperature_2050_c": row_2050["surface_temperature_anomaly_c"],
                "temperature_2100_c": final["surface_temperature_anomaly_c"],
                "temperature_change_2026_to_2100_c": final["temperature_change_vs_2026_c"],
                "peak_temperature_c": peak["surface_temperature_anomaly_c"],
                "peak_temperature_year": peak["year"],
                "minimum_temperature_c": minimum["surface_temperature_anomaly_c"],
                "minimum_temperature_year": minimum["year"],
                "co2_ppm_2100": final["co2_ppm"],
                "co2_erf_2100_w_m2": final["co2_erf_w_m2"],
                "non_co2_positive_forcing_2100_w_m2": final["non_co2_positive_forcing_w_m2"],
                "aerosol_forcing_2100_w_m2": final["aerosol_forcing_w_m2"],
                "total_erf_2100_w_m2": final["total_erf_w_m2"],
                "avoided_temperature_vs_no_aether_2100_c": "",
                "model_class": "calibrated two-box screening emulator",
                "caveat": policy.caveat,
            })

    baseline_final_by_policy = {
        row["forcing_policy"]: float(row["temperature_2100_c"])
        for row in summary_rows
        if row["case"] == "baseline_constant_emissions_no_aether"
    }
    for row in summary_rows:
        baseline = baseline_final_by_policy[row["forcing_policy"]]
        avoided = baseline - float(row["temperature_2100_c"])
        row["avoided_temperature_vs_no_aether_2100_c"] = f(avoided, 6)

    forcing_rows = [
        {
            "forcing_policy": policy.key,
            "forcing_policy_name": policy.name,
            "non_co2_positive_2026_w_m2": f(policy.nonco2_2026, 3),
            "non_co2_positive_2050_w_m2": f(policy.nonco2_2050, 3),
            "non_co2_positive_2100_w_m2": f(policy.nonco2_2100, 3),
            "aerosol_2026_w_m2": f(policy.aerosol_2026, 3),
            "aerosol_2050_w_m2": f(policy.aerosol_2050, 3),
            "aerosol_2100_w_m2": f(policy.aerosol_2100, 3),
            "assumption_basis": policy.basis,
            "paper_use_rule": "Use as scenario screen only; do not cite as a forecast of future non-CO2 or aerosol forcing.",
        }
        for policy in FORCING_POLICIES
    ]

    write_rows(PATHWAY_OUTPUT, pathway_rows)
    write_rows(SUMMARY_OUTPUT, summary_rows)
    write_rows(FORCING_OUTPUT, forcing_rows)
    write_rows(CALIBRATION_OUTPUT, [calibration_row])


if __name__ == "__main__":
    main()

