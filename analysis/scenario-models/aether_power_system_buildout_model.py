"""AETHER power-system buildout model.

This model translates AETHER electricity demand into installed clean-power
capacity, annual buildout rates, solar land-area proxies, and a small
short-duration storage proxy. It is a first-order capacity model, not a
production-cost, unit-commitment, or transmission model.
"""

from __future__ import annotations

from dataclasses import dataclass
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TABLE_DIR = ROOT / "analysis" / "tables"


@dataclass(frozen=True)
class Technology:
    name: str
    capacity_factor: float


TECH = {
    "utility_solar_pv": Technology("Utility solar PV", 0.24),
    "land_based_wind": Technology("Land-based wind", 0.42),
    "nuclear_fission": Technology("Nuclear fission", 0.93),
    "advanced_geothermal": Technology("Advanced geothermal", 0.85),
}


def required_capacity_gw(twh_y: float, capacity_factor: float) -> float:
    return twh_y / (8.76 * capacity_factor)


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rows = []
    gross_twh = 83333.3333333333 * 1.10
    shares = {
        "utility_solar_pv": 0.35,
        "land_based_wind": 0.35,
        "nuclear_fission": 0.20,
        "advanced_geothermal": 0.10,
    }
    for key, share in shares.items():
        tech = TECH[key]
        generation = gross_twh * share
        rows.append(
            {
                "scenario": "advanced_3gj_balanced_firm",
                "technology": key,
                "technology_generation_twh_y": round(generation, 1),
                "required_nameplate_capacity_gw": round(required_capacity_gw(generation, tech.capacity_factor), 0),
            }
        )
    write_csv(TABLE_DIR / "aether_clean_power_portfolio_requirements_repro_example.csv", rows)


if __name__ == "__main__":
    main()
