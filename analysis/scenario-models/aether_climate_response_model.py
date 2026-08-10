from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TABLE_DIR = ROOT / "analysis" / "tables"

CARBON_CYCLE_PATH = TABLE_DIR / "aether_carbon_cycle_pathways.csv"
PATHWAY_OUTPUT = TABLE_DIR / "aether_climate_response_pathways.csv"
SUMMARY_OUTPUT = TABLE_DIR / "aether_climate_response_summary.csv"

PREINDUSTRIAL_CO2_PPM = 278.0
CO2_DOUBLING_ERF_W_M2 = 3.93
ECS_CENTRAL_C = 3.0
TCR_CENTRAL_C = 1.8


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
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


def equilibrium_proxy(forcing_w_m2: float) -> float:
    return forcing_w_m2 / CO2_DOUBLING_ERF_W_M2 * ECS_CENTRAL_C


def transient_proxy(forcing_w_m2: float) -> float:
    return forcing_w_m2 / CO2_DOUBLING_ERF_W_M2 * TCR_CENTRAL_C


def main() -> None:
    carbon_rows = read_rows(CARBON_CYCLE_PATH)
    by_case: dict[str, list[dict[str, str]]] = {}
    for row in carbon_rows:
        by_case.setdefault(row["case"], []).append(row)
    for case_rows in by_case.values():
        case_rows.sort(key=lambda row: int(row["year"]))

    output_rows: list[dict[str, object]] = []
    for case, case_rows in by_case.items():
        first_ppm = float(case_rows[0]["atmospheric_co2_ppm_reduced_form"])
        first_forcing = co2_erf(first_ppm)
        first_equilibrium = equilibrium_proxy(first_forcing)
        first_transient = transient_proxy(first_forcing)

        for row in case_rows:
            ppm = float(row["atmospheric_co2_ppm_reduced_form"])
            forcing = co2_erf(ppm)
            equilibrium = equilibrium_proxy(forcing)
            transient = transient_proxy(forcing)
            output_rows.append({
                "case": case,
                "display_name": row["display_name"],
                "year": row["year"],
                "co2_ppm": f(ppm, 6),
                "co2_erf_w_m2": f(forcing, 6),
                "co2_erf_change_vs_2026_w_m2": f(forcing - first_forcing, 6),
                "co2_only_equilibrium_warming_proxy_c": f(equilibrium, 6),
                "co2_only_transient_warming_proxy_c": f(transient, 6),
                "co2_only_equilibrium_change_vs_2026_c": f(equilibrium - first_equilibrium, 6),
                "co2_only_transient_change_vs_2026_c": f(transient - first_transient, 6),
                "ppm_above_preindustrial": f(ppm - PREINDUSTRIAL_CO2_PPM, 6),
                "source_formula": "CO2 ERF = 3.93 * log2(C/278); proxies scale forcing by ECS=3.0C and TCR=1.8C",
            })

    response_by_case: dict[str, list[dict[str, object]]] = {}
    for row in output_rows:
        response_by_case.setdefault(str(row["case"]), []).append(row)

    baseline_case = "baseline_constant_emissions_no_aether"
    baseline_by_year = {
        int(row["year"]): row for row in response_by_case[baseline_case]
    }

    summary_rows: list[dict[str, object]] = []
    for case, rows in response_by_case.items():
        row_by_year = {int(row["year"]): row for row in rows}
        final = row_by_year[2100]
        baseline_final = baseline_by_year[2100]
        peak = max(rows, key=lambda row: float(row["co2_only_transient_warming_proxy_c"]))
        minimum = min(rows, key=lambda row: float(row["co2_only_transient_warming_proxy_c"]))
        summary_rows.append({
            "case": case,
            "display_name": str(rows[0]["display_name"]),
            "co2_ppm_2050": row_by_year[2050]["co2_ppm"],
            "co2_erf_w_m2_2050": row_by_year[2050]["co2_erf_w_m2"],
            "co2_only_transient_proxy_2050_c": row_by_year[2050]["co2_only_transient_warming_proxy_c"],
            "co2_only_equilibrium_proxy_2050_c": row_by_year[2050]["co2_only_equilibrium_warming_proxy_c"],
            "co2_ppm_2100": final["co2_ppm"],
            "co2_erf_w_m2_2100": final["co2_erf_w_m2"],
            "co2_only_transient_proxy_2100_c": final["co2_only_transient_warming_proxy_c"],
            "co2_only_equilibrium_proxy_2100_c": final["co2_only_equilibrium_warming_proxy_c"],
            "transient_proxy_change_2026_to_2100_c": final["co2_only_transient_change_vs_2026_c"],
            "equilibrium_proxy_change_2026_to_2100_c": final["co2_only_equilibrium_change_vs_2026_c"],
            "transient_proxy_avoided_vs_no_aether_2100_c": f(float(baseline_final["co2_only_transient_warming_proxy_c"]) - float(final["co2_only_transient_warming_proxy_c"]), 6),
            "equilibrium_proxy_avoided_vs_no_aether_2100_c": f(float(baseline_final["co2_only_equilibrium_warming_proxy_c"]) - float(final["co2_only_equilibrium_warming_proxy_c"]), 6),
            "peak_transient_proxy_c": peak["co2_only_transient_warming_proxy_c"],
            "peak_transient_proxy_year": peak["year"],
            "minimum_transient_proxy_c": minimum["co2_only_transient_warming_proxy_c"],
            "minimum_transient_proxy_year": minimum["year"],
            "caveat": "CO2-only proxy; excludes non-CO2 forcing, aerosols, ocean heat uptake dynamics, ice sheets, regional effects, and full carbon-climate feedbacks.",
        })

    write_rows(PATHWAY_OUTPUT, output_rows)
    write_rows(SUMMARY_OUTPUT, summary_rows)


if __name__ == "__main__":
    main()

