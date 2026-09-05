from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

from aether_carbon_cycle_model import PUBLICATION_METADATA


ROOT = Path(__file__).resolve().parents[2]
TABLE_DIR = ROOT / "analysis" / "tables"
TABLE_DIR.mkdir(parents=True, exist_ok=True)

FAIR_DECK = TABLE_DIR / "aether_fair_readiness_input_deck.csv"
PATHWAYS = TABLE_DIR / "aether_species_emissions_handoff_pathways.csv"
REQUIREMENTS = TABLE_DIR / "aether_species_emissions_requirement_matrix.csv"
SUMMARY = TABLE_DIR / "aether_species_emissions_summary.csv"
PUBLICATION_GATES = TABLE_DIR / "aether_species_emissions_publication_gates.csv"

STATUS_WEIGHT = {
    "usable_screen": 1.0,
    "provisional_proxy": 0.62,
    "aggregate_placeholder": 0.35,
    "missing": 0.0,
}

SPECIES_REQUIREMENTS = [
    {
        "species_group": "net_CO2_proxy",
        "fair_input_hint": "CO2 emissions/removals",
        "required_units": "GtCO2/year before FAIR-native conversion",
        "current_proxy_column": "fair_proxy_net_co2_emissions_gtco2_y",
        "proxy_units": "GtCO2/year",
        "current_status": "provisional_proxy",
        "priority": "P0",
        "publication_gap": "Net CO2 is a derived pulse, not separated into fossil, industrial, land-use, and removal streams.",
        "next_dataset": "annual fossil/industrial CO2, land-use CO2, and removals by pathway and region",
    },
    {
        "species_group": "gross_CDR_by_method",
        "fair_input_hint": "negative CO2 emissions by removal method",
        "required_units": "GtCO2/year",
        "current_proxy_column": "gross_removal_gtco2_y",
        "proxy_units": "GtCO2/year",
        "current_status": "provisional_proxy",
        "priority": "P0",
        "publication_gap": "Gross removal is not split by DACCS, mineralization, ocean alkalinity, BECCS, biochar, afforestation, or direct ocean CDR.",
        "next_dataset": "method-specific annual gross removal, durability, leakage, and MRV-adjusted crediting traces",
    },
    {
        "species_group": "fossil_industrial_CO2",
        "fair_input_hint": "CO2 fossil and industrial emissions",
        "required_units": "GtCO2/year",
        "current_proxy_column": "positive_emissions_gtco2_y",
        "proxy_units": "GtCO2/year",
        "current_status": "provisional_proxy",
        "priority": "P0",
        "publication_gap": "Positive emissions are scenario-level totals, not sector-specific fossil and industrial traces.",
        "next_dataset": "sectoral fossil/industrial emissions pathways under no-AETHER, rebound, and net-zero cases",
    },
    {
        "species_group": "land_use_CO2",
        "fair_input_hint": "land-use CO2 emissions",
        "required_units": "GtCO2/year",
        "current_proxy_column": "",
        "proxy_units": "",
        "current_status": "missing",
        "priority": "P0",
        "publication_gap": "Land-use CO2 is missing even though BECCS, afforestation, biomass supply, and land footprints matter.",
        "next_dataset": "land-use emissions and removals by land-intensive pathway",
    },
    {
        "species_group": "CH4",
        "fair_input_hint": "methane emissions or concentration",
        "required_units": "MtCH4/year or ppb",
        "current_proxy_column": "non_co2_positive_forcing_w_m2",
        "proxy_units": "W/m2 aggregate non-CO2 forcing",
        "current_status": "aggregate_placeholder",
        "priority": "P0",
        "publication_gap": "Methane is buried inside aggregate non-CO2 forcing.",
        "next_dataset": "CH4 baseline, mitigation, leakage, agriculture, fossil, and rebound trajectories",
    },
    {
        "species_group": "N2O",
        "fair_input_hint": "nitrous oxide emissions or concentration",
        "required_units": "MtN2O/year or ppb",
        "current_proxy_column": "non_co2_positive_forcing_w_m2",
        "proxy_units": "W/m2 aggregate non-CO2 forcing",
        "current_status": "aggregate_placeholder",
        "priority": "P0",
        "publication_gap": "Nitrous oxide is buried inside aggregate non-CO2 forcing and may move with bioenergy and land-use cases.",
        "next_dataset": "N2O baseline and mitigation pathways, including bioenergy and agriculture interactions",
    },
    {
        "species_group": "halogenated_gases",
        "fair_input_hint": "F-gases and ozone-depleting substances",
        "required_units": "species-specific emissions or concentration",
        "current_proxy_column": "non_co2_positive_forcing_w_m2",
        "proxy_units": "W/m2 aggregate non-CO2 forcing",
        "current_status": "aggregate_placeholder",
        "priority": "P1",
        "publication_gap": "Halogenated gases are not separated from aggregate non-CO2 forcing.",
        "next_dataset": "species-level F-gas and ODS pathways or imported assessed scenario trajectories",
    },
    {
        "species_group": "ozone_precursors",
        "fair_input_hint": "NOx, CO, VOC emissions",
        "required_units": "Mt/year by precursor",
        "current_proxy_column": "non_co2_positive_forcing_w_m2",
        "proxy_units": "W/m2 aggregate non-CO2 forcing",
        "current_status": "aggregate_placeholder",
        "priority": "P1",
        "publication_gap": "Tropospheric ozone chemistry is not represented.",
        "next_dataset": "NOx, CO, and VOC pathways or assessed scenario imports",
    },
    {
        "species_group": "SO2_aerosol_precursor",
        "fair_input_hint": "sulfur dioxide emissions",
        "required_units": "MtSO2/year",
        "current_proxy_column": "aerosol_forcing_w_m2",
        "proxy_units": "W/m2 aggregate aerosol forcing",
        "current_status": "aggregate_placeholder",
        "priority": "P0",
        "publication_gap": "Aerosol cooling is an aggregate forcing path, not precursor-emissions chemistry.",
        "next_dataset": "SO2 emissions by energy, industry, and cleanup scenario",
    },
    {
        "species_group": "black_carbon",
        "fair_input_hint": "BC emissions",
        "required_units": "MtBC/year",
        "current_proxy_column": "aerosol_forcing_w_m2",
        "proxy_units": "W/m2 aggregate aerosol forcing",
        "current_status": "aggregate_placeholder",
        "priority": "P1",
        "publication_gap": "Black-carbon forcing is not separated from aggregate aerosol forcing.",
        "next_dataset": "BC emissions or assessed scenario imports",
    },
    {
        "species_group": "organic_carbon",
        "fair_input_hint": "OC emissions",
        "required_units": "MtOC/year",
        "current_proxy_column": "aerosol_forcing_w_m2",
        "proxy_units": "W/m2 aggregate aerosol forcing",
        "current_status": "aggregate_placeholder",
        "priority": "P1",
        "publication_gap": "Organic-carbon forcing is not separated from aggregate aerosol forcing.",
        "next_dataset": "OC emissions or assessed scenario imports",
    },
    {
        "species_group": "ammonia_nitrate",
        "fair_input_hint": "NH3 and nitrate aerosol precursors",
        "required_units": "Mt/year by precursor",
        "current_proxy_column": "",
        "proxy_units": "",
        "current_status": "missing",
        "priority": "P1",
        "publication_gap": "Nitrate aerosol chemistry and ammonia precursors are missing.",
        "next_dataset": "NH3 and nitrate-relevant precursor pathways",
    },
    {
        "species_group": "land_use_albedo_forcing",
        "fair_input_hint": "land-use forcing",
        "required_units": "W/m2 or land-use forcing pathway",
        "current_proxy_column": "",
        "proxy_units": "",
        "current_status": "missing",
        "priority": "P1",
        "publication_gap": "Land-use albedo and biogeophysical response are missing.",
        "next_dataset": "land-use forcing by afforestation, biomass, solar/industrial land, and materials footprints",
    },
    {
        "species_group": "lifecycle_species_trace",
        "fair_input_hint": "CO2, CH4, N2O lifecycle emissions",
        "required_units": "annual species-level emissions",
        "current_proxy_column": "",
        "proxy_units": "",
        "current_status": "missing",
        "priority": "P0",
        "publication_gap": "Lifecycle emissions are route-level CO2e stress tests, not annual species traces.",
        "next_dataset": "pathway-specific LCA time series with CO2, CH4, N2O, replacement, recycling, and decommissioning",
    },
    {
        "species_group": "historical_spinup_state",
        "fair_input_hint": "historical emissions, concentrations, forcing, and temperature initialization",
        "required_units": "historical time series",
        "current_proxy_column": "surface_temperature_anomaly_c",
        "proxy_units": "deg C screening initial state",
        "current_status": "provisional_proxy",
        "priority": "P0",
        "publication_gap": "CO2 history now comes from published RCMIP concentrations, but non-CO2 history and thermal state remain synthetic/unvalidated; historical carbon reservoirs are not calibrated.",
        "next_dataset": "historical emissions, concentration, forcing, and observed-temperature spin-up through 2026",
    },
    {
        "species_group": "ZEC_and_net_negative_response",
        "fair_input_hint": "zero-emissions commitment and net-negative response diagnostic",
        "required_units": "temperature-response diagnostic",
        "current_proxy_column": "",
        "proxy_units": "",
        "current_status": "missing",
        "priority": "P0",
        "publication_gap": "ZEC and net-negative temperature-response behavior are not separated from the forcing screen.",
        "next_dataset": "ZEC and net-negative response experiment set for AETHER net-zero and drawdown cases",
    },
]


PUBLICATION_GATE_DEFS = [
    ("G0_carbon_baseline_response", PUBLICATION_METADATA["failure_reason"], "fail", "P0"),
    ("G1_CO2_split", "Separate fossil/industrial CO2, land-use CO2, and CDR removals before a full FAIR run.", "partial", "P0"),
    ("G2_CDR_methods", "Split CDR by method, durability, leakage, MRV, and lifecycle boundary.", "partial", "P0"),
    ("G3_CH4_N2O", "Replace aggregate non-CO2 forcing with CH4 and N2O trajectories.", "fail", "P0"),
    ("G4_aerosol_precursors", "Replace aggregate aerosol forcing with SO2, BC, OC, nitrate, and cloud-interaction inputs.", "fail", "P0"),
    ("G5_lifecycle_species", "Convert lifecycle CO2e into annual CO2, CH4, N2O, replacement, recycling, and decommissioning traces.", "fail", "P0"),
    ("G6_land_use_forcing", "Add land-use CO2, albedo, and biogeophysical forcing for land-intensive pathways.", "fail", "P1"),
    ("G7_historical_spinup", "Initialize from historical emissions, concentration, forcing, and observed-temperature state.", "partial", "P0"),
    ("G8_ZEC_net_negative", "Run zero-emissions commitment and net-negative response diagnostics.", "fail", "P0"),
    ("G9_uncertainty_ensemble", "Run ensemble ranges across climate response, forcing, carbon-cycle, and lifecycle parameters.", "fail", "P0"),
    ("G10_ocean_chemistry", "Add ocean chemistry and alkalinity feedback treatment for ocean CDR claims.", "fail", "P1"),
]


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


def proxy_value(deck_row: dict[str, str], requirement: dict[str, str]) -> object:
    column = requirement["current_proxy_column"]
    if not column:
        return ""
    value = f(deck_row, column)
    if requirement["species_group"] == "gross_CDR_by_method":
        return round(-value, 6)
    return round(value, 6)


deck_rows = read_csv(FAIR_DECK)
if not deck_rows:
    raise RuntimeError("FAIR-readiness deck is empty.")

scenario_ids = sorted({row["scenario_id"] for row in deck_rows})
years = sorted({int(row["year"]) for row in deck_rows})
requirement_rows: list[dict[str, object]] = []
for requirement in SPECIES_REQUIREMENTS:
    status = requirement["current_status"]
    requirement_rows.append({
        **requirement,
        "readiness_score_0_1": STATUS_WEIGHT[status],
        "paper_use_rule": "diagnostic only" if status != "usable_screen" else "screening cross-check",
    })

pathway_rows: list[dict[str, object]] = []
for deck_row in deck_rows:
    for requirement in SPECIES_REQUIREMENTS:
        status = requirement["current_status"]
        pathway_rows.append({
            **PUBLICATION_METADATA,
            "scenario_id": deck_row["scenario_id"],
            "case": deck_row["case"],
            "emissions_policy": deck_row["emissions_policy"],
            "matched_no_aether_case": deck_row["matched_no_aether_case"],
            "carbon_baseline_id": deck_row["carbon_baseline_id"],
            "forcing_policy": deck_row["forcing_policy"],
            "year": deck_row["year"],
            "species_group": requirement["species_group"],
            "fair_input_hint": requirement["fair_input_hint"],
            "current_proxy_value": proxy_value(deck_row, requirement),
            "proxy_units": requirement["proxy_units"],
            "current_status": status,
            "readiness_score_0_1": STATUS_WEIGHT[status],
            "priority": requirement["priority"],
            "publication_gap": requirement["publication_gap"],
            "next_dataset": requirement["next_dataset"],
            "paper_use_rule": "do not use as species-emissions result" if status in {"missing", "aggregate_placeholder"} else "diagnostic handoff only",
        })

requirements_by_status = Counter(row["current_status"] for row in requirement_rows)
p0_blocking_groups = sum(
    1 for row in requirement_rows
    if row["priority"] == "P0" and row["current_status"] in {"missing", "aggregate_placeholder", "provisional_proxy"}
)
readiness_score = sum(float(row["readiness_score_0_1"]) for row in requirement_rows) / len(requirement_rows)

rows_by_scenario = defaultdict(list)
for row in deck_rows:
    rows_by_scenario[row["scenario_id"]].append(row)

summary_rows: list[dict[str, object]] = []
for scenario_id, rows in sorted(rows_by_scenario.items()):
    rows = sorted(rows, key=lambda row: int(row["year"]))
    row_2100 = rows[-1]
    summary_rows.append({
        **PUBLICATION_METADATA,
        "scenario_id": scenario_id,
        "case": row_2100["case"],
        "emissions_policy": row_2100["emissions_policy"],
        "matched_no_aether_case": row_2100["matched_no_aether_case"],
        "carbon_baseline_id": row_2100["carbon_baseline_id"],
        "forcing_policy": row_2100["forcing_policy"],
        "year_count": len(rows),
        "species_group_count": len(SPECIES_REQUIREMENTS),
        "pathway_row_count": len(rows) * len(SPECIES_REQUIREMENTS),
        "usable_screen_groups": requirements_by_status["usable_screen"],
        "provisional_proxy_groups": requirements_by_status["provisional_proxy"],
        "aggregate_placeholder_groups": requirements_by_status["aggregate_placeholder"],
        "missing_groups": requirements_by_status["missing"],
        "p0_blocking_groups": p0_blocking_groups,
        "species_handoff_readiness_score_0_1": round(readiness_score, 4),
        "cumulative_positive_co2_gtco2_2026_2100": round(sum(f(row, "positive_emissions_gtco2_y") for row in rows), 6),
        "cumulative_gross_cdr_gtco2_2026_2100": round(sum(f(row, "gross_removal_gtco2_y") for row in rows), 6),
        "cumulative_net_co2_proxy_gtco2_2026_2100": round(sum(f(row, "fair_proxy_net_co2_emissions_gtco2_y") for row in rows), 6),
        "non_co2_forcing_2100_w_m2": round(f(row_2100, "non_co2_positive_forcing_w_m2"), 6),
        "aerosol_forcing_2100_w_m2": round(f(row_2100, "aerosol_forcing_w_m2"), 6),
        "publication_gate": "blocked: aggregate non-CO2, aerosol precursors, lifecycle species traces, spin-up, and ZEC remain unresolved",
    })

publication_gate_rows = []
for gate_id, test, status, priority in PUBLICATION_GATE_DEFS:
    publication_gate_rows.append({
        "gate_id": gate_id,
        "test": test,
        "gate_status": status,
        "priority": priority,
        "paper_use_rule": "must pass before publication-grade temperature claims" if priority == "P0" else "needed before stronger method claims",
    })

write_csv(PATHWAYS, pathway_rows, [
    *PUBLICATION_METADATA,
    "scenario_id",
    "case",
    "emissions_policy",
    "matched_no_aether_case",
    "carbon_baseline_id",
    "forcing_policy",
    "year",
    "species_group",
    "fair_input_hint",
    "current_proxy_value",
    "proxy_units",
    "current_status",
    "readiness_score_0_1",
    "priority",
    "publication_gap",
    "next_dataset",
    "paper_use_rule",
])
write_csv(REQUIREMENTS, requirement_rows, [
    "species_group",
    "fair_input_hint",
    "required_units",
    "current_proxy_column",
    "proxy_units",
    "current_status",
    "priority",
    "publication_gap",
    "next_dataset",
    "readiness_score_0_1",
    "paper_use_rule",
])
write_csv(SUMMARY, summary_rows, [
    *PUBLICATION_METADATA,
    "scenario_id",
    "case",
    "emissions_policy",
    "matched_no_aether_case",
    "carbon_baseline_id",
    "forcing_policy",
    "year_count",
    "species_group_count",
    "pathway_row_count",
    "usable_screen_groups",
    "provisional_proxy_groups",
    "aggregate_placeholder_groups",
    "missing_groups",
    "p0_blocking_groups",
    "species_handoff_readiness_score_0_1",
    "cumulative_positive_co2_gtco2_2026_2100",
    "cumulative_gross_cdr_gtco2_2026_2100",
    "cumulative_net_co2_proxy_gtco2_2026_2100",
    "non_co2_forcing_2100_w_m2",
    "aerosol_forcing_2100_w_m2",
    "publication_gate",
])
write_csv(PUBLICATION_GATES, publication_gate_rows, [
    "gate_id",
    "test",
    "gate_status",
    "priority",
    "paper_use_rule",
])

