from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from aether_carbon_cycle_model import PUBLICATION_METADATA

import numpy as np
from fair import FAIR
from fair.interface import fill, initialise

try:
    import fair as fair_package
    FAIR_VERSION = getattr(fair_package, "__version__", "unknown")
except Exception:
    FAIR_VERSION = "unknown"


ROOT = Path(__file__).resolve().parents[2]
TABLE_DIR = ROOT / "analysis" / "tables"
TABLE_DIR.mkdir(parents=True, exist_ok=True)

INPUT_DECK = TABLE_DIR / "aether_fair_readiness_input_deck.csv"
PATHWAY_OUTPUT = TABLE_DIR / "aether_fair_forcing_temperature_paths.csv"
SUMMARY_OUTPUT = TABLE_DIR / "aether_fair_forcing_summary.csv"
CONFIG_OUTPUT = TABLE_DIR / "aether_fair_forcing_config.csv"
DELTA_OUTPUT = TABLE_DIR / "aether_fair_forcing_delta_vs_emulator.csv"

SPECIES = ["CO2 forcing", "aggregate non-CO2 forcing", "aggregate aerosol forcing"]
SPECIES_PROPERTIES = {
    "CO2 forcing": {
        "type": "co2",
        "input_mode": "forcing",
        "greenhouse_gas": True,
        "aerosol_chemistry_from_emissions": False,
        "aerosol_chemistry_from_concentration": False,
    },
    "aggregate non-CO2 forcing": {
        "type": "unspecified",
        "input_mode": "forcing",
        "greenhouse_gas": False,
        "aerosol_chemistry_from_emissions": False,
        "aerosol_chemistry_from_concentration": False,
    },
    "aggregate aerosol forcing": {
        "type": "ari",
        "input_mode": "forcing",
        "greenhouse_gas": False,
        "aerosol_chemistry_from_emissions": False,
        "aerosol_chemistry_from_concentration": False,
    },
}

CONFIGS = {
    "central_diagnostic": {
        "ocean_heat_capacity": [4.0, 10.0, 100.0],
        "ocean_heat_transfer": [1.25, 0.70, 0.15],
        "deep_ocean_efficacy": 1.10,
        "forcing_4co2": 7.86,
        "interpretation": "Central diagnostic continuation run; not a calibrated constrained AR6 ensemble.",
    },
    "faster_response": {
        "ocean_heat_capacity": [3.0, 8.0, 80.0],
        "ocean_heat_transfer": [1.05, 0.55, 0.12],
        "deep_ocean_efficacy": 1.05,
        "forcing_4co2": 7.86,
        "interpretation": "Higher near-term response stress test.",
    },
    "slower_ocean_lag": {
        "ocean_heat_capacity": [6.0, 14.0, 140.0],
        "ocean_heat_transfer": [1.55, 0.90, 0.20],
        "deep_ocean_efficacy": 1.20,
        "forcing_4co2": 7.86,
        "interpretation": "Stronger ocean-lag stress test.",
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def f(row: dict[str, str], key: str, default: float = 0.0) -> float:
    raw = row.get(key, "")
    if raw in ("", None):
        return default
    return float(raw)


deck_rows = read_csv(INPUT_DECK)
years = sorted({int(row["year"]) for row in deck_rows})
scenario_ids = sorted({row["scenario_id"] for row in deck_rows})
rows_by_scenario = defaultdict(list)
for row in deck_rows:
    rows_by_scenario[row["scenario_id"]].append(row)
for scenario_id in scenario_ids:
    rows_by_scenario[scenario_id].sort(key=lambda row: int(row["year"]))
    if [int(row["year"]) for row in rows_by_scenario[scenario_id]] != years:
        raise RuntimeError(f"Scenario {scenario_id} does not cover the complete year grid.")

fair_model = FAIR()
fair_model.define_time(years[0], years[-1], 1)
fair_model.define_scenarios(scenario_ids)
fair_model.define_configs(list(CONFIGS.keys()))
fair_model.define_species(SPECIES, SPECIES_PROPERTIES)
fair_model.allocate()

for config_name, config in CONFIGS.items():
    fill(fair_model.climate_configs["ocean_heat_capacity"], np.array(config["ocean_heat_capacity"]), config=config_name)
    fill(fair_model.climate_configs["ocean_heat_transfer"], np.array(config["ocean_heat_transfer"]), config=config_name)
    fill(fair_model.climate_configs["deep_ocean_efficacy"], config["deep_ocean_efficacy"], config=config_name)
    fill(fair_model.climate_configs["forcing_4co2"], config["forcing_4co2"], config=config_name)
    fill(fair_model.climate_configs["stochastic_run"], False, config=config_name)
    fill(fair_model.climate_configs["use_seed"], False, config=config_name)

for scenario_id in scenario_ids:
    scenario_rows = rows_by_scenario[scenario_id]
    forcing = np.array(
        [
            [
                f(row, "co2_erf_w_m2"),
                f(row, "non_co2_positive_forcing_w_m2"),
                f(row, "aerosol_forcing_w_m2"),
            ]
            for row in scenario_rows
        ]
    )
    first = scenario_rows[0]
    surface_initial = f(first, "surface_temperature_anomaly_c")
    deep_initial = f(first, "deep_ocean_temperature_index_c")
    initial_state = np.array([surface_initial, deep_initial, deep_initial * 0.35])
    for config_name in CONFIGS:
        fill(fair_model.forcing, forcing, scenario=scenario_id, config=config_name)
        initialise(fair_model.temperature, initial_state, scenario=scenario_id, config=config_name)

fair_model.run(progress=False)

pathway_rows: list[dict[str, object]] = []
summary_rows: list[dict[str, object]] = []
delta_rows: list[dict[str, object]] = []

for scenario_id in scenario_ids:
    source_rows = rows_by_scenario[scenario_id]
    first = source_rows[0]
    for config_name, config in CONFIGS.items():
        temps = fair_model.temperature.sel(scenario=scenario_id, config=config_name).values
        surface = temps[:, 0]
        mid_ocean = temps[:, 1]
        deep_ocean = temps[:, 2]
        for idx, row in enumerate(source_rows):
            fair_temp = float(surface[idx])
            emulator_temp = f(row, "surface_temperature_anomaly_c")
            pathway_rows.append({
                **PUBLICATION_METADATA,
                "scenario_id": scenario_id,
                "case": row["case"],
                "display_name": row["display_name"],
                "emissions_policy": row["emissions_policy"],
                "matched_no_aether_case": row["matched_no_aether_case"],
                "carbon_baseline_id": row["carbon_baseline_id"],
                "forcing_policy": row["forcing_policy"],
                "forcing_policy_name": row["forcing_policy_name"],
                "config": config_name,
                "year": int(row["year"]),
                "fair_surface_temperature_c": round(fair_temp, 6),
                "fair_mid_ocean_temperature_c": round(float(mid_ocean[idx]), 6),
                "fair_deep_ocean_temperature_c": round(float(deep_ocean[idx]), 6),
                "emulator_surface_temperature_c": round(emulator_temp, 6),
                "fair_minus_emulator_c": round(fair_temp - emulator_temp, 6),
                "co2_erf_w_m2": row["co2_erf_w_m2"],
                "non_co2_positive_forcing_w_m2": row["non_co2_positive_forcing_w_m2"],
                "aerosol_forcing_w_m2": row["aerosol_forcing_w_m2"],
                "total_erf_w_m2": row["total_erf_w_m2"],
                "run_caveat": "Forcing-driven FAIR diagnostic using conditional hybrid carbon inputs and aggregate forcing; not a full species-emissions run, historical calibration, or carbon-cycle validation. Absolute temperature is not a validated prediction.",
            })
        year_to_idx = {int(row["year"]): idx for idx, row in enumerate(source_rows)}
        idx_2026 = year_to_idx[2026]
        idx_2050 = year_to_idx[2050]
        idx_2100 = year_to_idx[2100]
        peak_idx = int(np.argmax(surface))
        min_idx = int(np.argmin(surface))
        summary_rows.append({
            **PUBLICATION_METADATA,
            "scenario_id": scenario_id,
            "case": first["case"],
            "display_name": first["display_name"],
            "emissions_policy": first["emissions_policy"],
            "matched_no_aether_case": first["matched_no_aether_case"],
            "carbon_baseline_id": first["carbon_baseline_id"],
            "forcing_policy": first["forcing_policy"],
            "forcing_policy_name": first["forcing_policy_name"],
            "config": config_name,
            "fair_version": FAIR_VERSION,
            "fair_temperature_2026_c": round(float(surface[idx_2026]), 6),
            "fair_temperature_2050_c": round(float(surface[idx_2050]), 6),
            "fair_temperature_2100_c": round(float(surface[idx_2100]), 6),
            "emulator_temperature_2100_c": round(f(source_rows[idx_2100], "surface_temperature_anomaly_c"), 6),
            "fair_minus_emulator_2100_c": round(float(surface[idx_2100]) - f(source_rows[idx_2100], "surface_temperature_anomaly_c"), 6),
            "peak_fair_temperature_c": round(float(surface[peak_idx]), 6),
            "peak_fair_temperature_year": years[peak_idx],
            "minimum_fair_temperature_c": round(float(surface[min_idx]), 6),
            "minimum_fair_temperature_year": years[min_idx],
            "co2_ppm_2100": source_rows[idx_2100]["co2_ppm_reduced_form"],
            "total_erf_2100_w_m2": source_rows[idx_2100]["total_erf_w_m2"],
            "config_interpretation": config["interpretation"],
            "publication_use": "Forcing-mode diagnostic only; does not validate upstream carbon cycle or absolute temperature. Matched controls isolate AETHER conditional on shared policy and response assumptions.",
        })
        delta_rows.append({
            **PUBLICATION_METADATA,
            "scenario_id": scenario_id,
            "case": first["case"],
            "forcing_policy": first["forcing_policy"],
            "config": config_name,
            "fair_minus_emulator_2100_c": round(float(surface[idx_2100]) - f(source_rows[idx_2100], "surface_temperature_anomaly_c"), 6),
            "absolute_delta_2100_c": round(abs(float(surface[idx_2100]) - f(source_rows[idx_2100], "surface_temperature_anomaly_c")), 6),
            "interpretation": "Positive means the FAIR forcing execution is warmer than the AETHER screening emulator in 2100.",
        })

by_path_key = {(row["case"], row["forcing_policy"], row["config"], row["year"]): row for row in pathway_rows}
for row in pathway_rows:
    control = by_path_key[(row["matched_no_aether_case"], row["forcing_policy"], row["config"], row["year"])]
    row["avoided_temperature_vs_matched_no_aether_c"] = round(float(control["fair_surface_temperature_c"]) - float(row["fair_surface_temperature_c"]), 6)
by_summary_key = {(row["case"], row["forcing_policy"], row["config"]): row for row in summary_rows}
for row in summary_rows:
    control = by_summary_key[(row["matched_no_aether_case"], row["forcing_policy"], row["config"])]
    row["avoided_temperature_vs_matched_no_aether_2100_c"] = round(float(control["fair_temperature_2100_c"]) - float(row["fair_temperature_2100_c"]), 6)

config_rows = []
for config_name, config in CONFIGS.items():
    config_rows.append({
        "config": config_name,
        "fair_version": FAIR_VERSION,
        "ocean_heat_capacity": ";".join(str(x) for x in config["ocean_heat_capacity"]),
        "ocean_heat_transfer": ";".join(str(x) for x in config["ocean_heat_transfer"]),
        "deep_ocean_efficacy": config["deep_ocean_efficacy"],
        "forcing_4co2_w_m2": config["forcing_4co2"],
        "run_type": "forcing-driven FAIR diagnostic",
        "interpretation": config["interpretation"],
    })

pathway_fields = [
    *PUBLICATION_METADATA,
    "scenario_id",
    "case",
    "display_name",
    "emissions_policy",
    "matched_no_aether_case",
    "carbon_baseline_id",
    "avoided_temperature_vs_matched_no_aether_c",
    "forcing_policy",
    "forcing_policy_name",
    "config",
    "year",
    "fair_surface_temperature_c",
    "fair_mid_ocean_temperature_c",
    "fair_deep_ocean_temperature_c",
    "emulator_surface_temperature_c",
    "fair_minus_emulator_c",
    "co2_erf_w_m2",
    "non_co2_positive_forcing_w_m2",
    "aerosol_forcing_w_m2",
    "total_erf_w_m2",
    "run_caveat",
]
summary_fields = [
    *PUBLICATION_METADATA,
    "scenario_id",
    "case",
    "display_name",
    "emissions_policy",
    "matched_no_aether_case",
    "carbon_baseline_id",
    "avoided_temperature_vs_matched_no_aether_2100_c",
    "forcing_policy",
    "forcing_policy_name",
    "config",
    "fair_version",
    "fair_temperature_2026_c",
    "fair_temperature_2050_c",
    "fair_temperature_2100_c",
    "emulator_temperature_2100_c",
    "fair_minus_emulator_2100_c",
    "peak_fair_temperature_c",
    "peak_fair_temperature_year",
    "minimum_fair_temperature_c",
    "minimum_fair_temperature_year",
    "co2_ppm_2100",
    "total_erf_2100_w_m2",
    "config_interpretation",
    "publication_use",
]
config_fields = [
    "config",
    "fair_version",
    "ocean_heat_capacity",
    "ocean_heat_transfer",
    "deep_ocean_efficacy",
    "forcing_4co2_w_m2",
    "run_type",
    "interpretation",
]
delta_fields = [
    *PUBLICATION_METADATA,
    "scenario_id",
    "case",
    "forcing_policy",
    "config",
    "fair_minus_emulator_2100_c",
    "absolute_delta_2100_c",
    "interpretation",
]

write_csv(PATHWAY_OUTPUT, pathway_rows, pathway_fields)
write_csv(SUMMARY_OUTPUT, summary_rows, summary_fields)
write_csv(CONFIG_OUTPUT, config_rows, config_fields)
write_csv(DELTA_OUTPUT, delta_rows, delta_fields)

print(f"Wrote {PATHWAY_OUTPUT}")
print(f"Wrote {SUMMARY_OUTPUT}")
print(f"Wrote {CONFIG_OUTPUT}")
print(f"Wrote {DELTA_OUTPUT}")

