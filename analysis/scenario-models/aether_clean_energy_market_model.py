from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analysis" / "tables"
OUT.mkdir(parents=True, exist_ok=True)

TWH_PER_GJ_PER_TON_FOR_1_GT = 277.77777777777777
YEARS = 20
BASE_ANNUAL_CLEAN_ADDITION_TWH = 850.0


def cumulative_generation_added(base_addition_twh_y: float, growth_rate: float, years: int) -> float:
    if growth_rate == 0:
        return base_addition_twh_y * years
    return base_addition_twh_y * (((1 + growth_rate) ** years - 1) / growth_rate)


def main() -> None:
    rows: list[dict[str, object]] = []
    energy_cases = [
        ("near_thermo_capture_storage_100Gt", 1.0),
        ("advanced_capture_storage_100Gt", 3.0),
        ("current_DAC_like_100Gt", 8.0),
        ("advanced_capture_100pct_split_100Gt", 11.941478544405184),
    ]
    growth_rates = [0.0, 0.05, 0.10, 0.12, 0.15, 0.20]
    for case_name, energy_gj_t in energy_cases:
        demand_twh_y = energy_gj_t * 100 * TWH_PER_GJ_PER_TON_FOR_1_GT
        annual_addition_required_twh_y = demand_twh_y / YEARS
        for growth_rate in growth_rates:
            cumulative_twh_y = cumulative_generation_added(BASE_ANNUAL_CLEAN_ADDITION_TWH, growth_rate, YEARS)
            rows.append({
                "case": case_name,
                "energy_gj_tco2": energy_gj_t,
                "aether_energy_demand_twh_y": demand_twh_y,
                "annual_addition_required_for_20y_buildout_twh_y": annual_addition_required_twh_y,
                "starting_global_clean_addition_twh_y": BASE_ANNUAL_CLEAN_ADDITION_TWH,
                "annual_growth_rate_in_clean_additions": growth_rate,
                "cumulative_new_annual_clean_generation_after_20y_twh_y": cumulative_twh_y,
                "coverage_of_aether_energy_demand_before_other_demand": cumulative_twh_y / demand_twh_y,
            })
    path = OUT / "aether_clean_energy_buildout_sensitivity.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
