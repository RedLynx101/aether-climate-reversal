from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from aether_carbon_cycle_model import PUBLICATION_METADATA


ROOT = Path(__file__).resolve().parents[2]
TABLE_DIR = ROOT / "analysis" / "tables"
TABLE_DIR.mkdir(parents=True, exist_ok=True)

CLIMATE_PATHWAYS = TABLE_DIR / "aether_climate_emulator_pathways.csv"
STATE_PATHWAYS = TABLE_DIR / "aether_state_dependent_carbon_pathways.csv"
INPUT_DECK = TABLE_DIR / "aether_fair_readiness_input_deck.csv"
SUMMARY = TABLE_DIR / "aether_fair_readiness_summary.csv"
GAP_MATRIX = TABLE_DIR / "aether_fair_readiness_gap_matrix.csv"
RUN_MANIFEST = TABLE_DIR / "aether_fair_readiness_run_manifest.csv"

FIXED_EFFECTIVENESS = "fixed_0p96_current"


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


climate_rows = read_csv(CLIMATE_PATHWAYS)
state_rows = [
    row for row in read_csv(STATE_PATHWAYS)
    if row["effectiveness_case"] == FIXED_EFFECTIVENESS
]
state_by_key = {(row["base_case"], int(row["year"])): row for row in state_rows}

gap_rows = [
    {
        "fair_variable_family": "CO2 emissions time series",
        "current_status": "provisional_proxy",
        "current_artifact": "aether_state_dependent_carbon_pathways.csv",
        "publication_gap": "Use exact fossil, land-use, and lifecycle emissions time series in FAIR-native units instead of a derived direct-net pulse.",
        "next_action": "Map each AETHER pathway to annual emissions and removals by source category.",
        "priority": "P0",
    },
    {
        "fair_variable_family": "CO2 removal time series",
        "current_status": "provisional_proxy",
        "current_artifact": "aether_state_dependent_carbon_pathways.csv",
        "publication_gap": "Gross and effective removal are represented, but not separated by method, durability, leakage, and lifecycle boundary.",
        "next_action": "Connect pathway portfolio, MRV, and lifecycle screens to method-specific removal time series.",
        "priority": "P0",
    },
    {
        "fair_variable_family": "CO2 concentration",
        "current_status": "rejected_off_reference",
        "current_artifact": "aether_climate_emulator_pathways.csv",
        "publication_gap": PUBLICATION_METADATA["failure_reason"],
        "next_action": "Compare against independently historically initialized emissions-driven FAIR output; forcing mode cannot validate the carbon cycle.",
        "priority": "P0",
    },
    {
        "fair_variable_family": "CO2 radiative forcing",
        "current_status": "usable_screen",
        "current_artifact": "aether_climate_emulator_pathways.csv",
        "publication_gap": "CO2 forcing uses the AR6 logarithmic anchor but not a full species forcing stack.",
        "next_action": "Keep as a cross-check against FAIR forcing diagnostics.",
        "priority": "P1",
    },
    {
        "fair_variable_family": "Non-CO2 forcing aggregate",
        "current_status": "aggregate_placeholder",
        "current_artifact": "aether_climate_emulator_forcing_assumptions.csv",
        "publication_gap": "Methane, nitrous oxide, halocarbons, ozone, and other forcing agents are aggregated into policy screens.",
        "next_action": "Replace aggregate non-CO2 forcing with species-level emissions or forcing trajectories.",
        "priority": "P0",
    },
    {
        "fair_variable_family": "Aerosol forcing",
        "current_status": "aggregate_placeholder",
        "current_artifact": "aether_climate_emulator_forcing_assumptions.csv",
        "publication_gap": "Aerosol cooling is an aggregate path, not precursor-emissions chemistry.",
        "next_action": "Add sulfur, black carbon, organic carbon, nitrate, and cloud-interaction assumptions.",
        "priority": "P0",
    },
    {
        "fair_variable_family": "Methane emissions",
        "current_status": "missing",
        "current_artifact": "none",
        "publication_gap": "No explicit CH4 emissions trajectory.",
        "next_action": "Add CH4 baseline, mitigation, rebound, and removals-independent policy assumptions.",
        "priority": "P0",
    },
    {
        "fair_variable_family": "Nitrous oxide emissions",
        "current_status": "missing",
        "current_artifact": "none",
        "publication_gap": "No explicit N2O emissions trajectory.",
        "next_action": "Add N2O baseline and mitigation cases, especially for bioenergy and land-use pathways.",
        "priority": "P0",
    },
    {
        "fair_variable_family": "Land-use and albedo forcing",
        "current_status": "missing",
        "current_artifact": "none",
        "publication_gap": "No explicit land-use forcing, albedo, or biogeophysical response.",
        "next_action": "Add land-use forcing for biomass, afforestation, alkalinity infrastructure, and materials footprints.",
        "priority": "P1",
    },
    {
        "fair_variable_family": "Lifecycle emissions trace",
        "current_status": "provisional_proxy",
        "current_artifact": "aether_lifecycle_emissions_summary.csv",
        "publication_gap": "Lifecycle emissions exist as pathway stress tests, but they are not annual species-level forcing inputs.",
        "next_action": "Convert lifecycle screen into annual CO2e and species-specific emissions traces.",
        "priority": "P0",
    },
    {
        "fair_variable_family": "Ocean heat uptake",
        "current_status": "usable_screen",
        "current_artifact": "aether_climate_emulator_pathways.csv",
        "publication_gap": "Two-box ocean index is useful for screening, not a calibrated ocean-heat-content validation.",
        "next_action": "Compare against FAIR thermal response and observed historical heat uptake constraints.",
        "priority": "P1",
    },
    {
        "fair_variable_family": "Zero-emissions commitment",
        "current_status": "missing",
        "current_artifact": "none",
        "publication_gap": "No explicit ZEC treatment after net zero or during net-negative phases.",
        "next_action": "Add ZEC diagnostics for net-zero and net-negative AETHER cases.",
        "priority": "P0",
    },
    {
        "fair_variable_family": "Carbon-cycle asymmetry",
        "current_status": "provisional_proxy",
        "current_artifact": "aether_state_dependent_carbon_summary.csv",
        "publication_gap": "Asymmetry is a hand-set stress test, not a calibrated land-ocean response.",
        "next_action": "Use FAIR/ESM comparison to calibrate or discard the current coefficients.",
        "priority": "P0",
    },
    {
        "fair_variable_family": "Ocean chemistry and alkalinity feedback",
        "current_status": "missing",
        "current_artifact": "none",
        "publication_gap": "Ocean alkalinity and direct ocean CDR have no carbonate-system response model.",
        "next_action": "Add ocean-chemistry submodel or source-backed simplification before ocean CDR claims.",
        "priority": "P1",
    },
    {
        "fair_variable_family": "Uncertainty ensemble",
        "current_status": "missing",
        "current_artifact": "none",
        "publication_gap": "The climate emulator is deterministic for each policy screen.",
        "next_action": "Run ensemble ranges across ECS, TCR, carbon-cycle response, non-CO2 forcing, aerosol cleanup, and lifecycle emissions.",
        "priority": "P0",
    },
    {
        "fair_variable_family": "Regional climate response",
        "current_status": "missing",
        "current_artifact": "none",
        "publication_gap": "No regional heat, precipitation, circulation, or extreme-risk response.",
        "next_action": "Keep the paper global until regional response can be sourced or modeled.",
        "priority": "P2",
    },
    {
        "fair_variable_family": "Historical spin-up and calibration",
        "current_status": "provisional_proxy",
        "current_artifact": "aether_climate_emulator_calibration.csv",
        "publication_gap": "Historical CO2 is a published RCMIP series; non-CO2 history and thermal state remain synthetic/unvalidated, with no calibrated historical carbon reservoirs.",
        "next_action": "Initialize FAIR with historical emissions and compare 2026 state against observed temperature and concentration.",
        "priority": "P0",
    },
]

status_weights = {
    "rejected_off_reference": 0.0,
    "usable_screen": 1.0,
    "provisional_proxy": 0.62,
    "aggregate_placeholder": 0.35,
    "missing": 0.0,
}
readiness_score = sum(status_weights[row["current_status"]] for row in gap_rows) / len(gap_rows)
critical_gap_count = sum(1 for row in gap_rows if row["priority"] == "P0" and row["current_status"] in {"missing", "aggregate_placeholder", "provisional_proxy", "rejected_off_reference"})
missing_or_placeholder_count = sum(1 for row in gap_rows if row["current_status"] in {"missing", "aggregate_placeholder"})

deck_rows: list[dict[str, object]] = []
for climate in climate_rows:
    year = int(climate["year"])
    key = (climate["case"], year)
    if key not in state_by_key:
        raise RuntimeError(f"Missing state-dependent carbon row for {key}")
    state = state_by_key[key]
    positive = f(state, "positive_emissions_gtco2_y")
    gross = f(state, "actual_gross_removal_gtco2_y")
    effective = f(state, "effective_removal_gtco2_y")
    direct_net = f(state, "direct_net_pulse_gtco2_y")
    ppm_mismatch = f(climate, "co2_ppm") - f(state, "atmospheric_co2_ppm_reduced_form")
    if abs(ppm_mismatch) > 0.00001:
        raise RuntimeError(f"Carbon/forcing handoff mismatch for {key}: {ppm_mismatch} ppm")
    deck_rows.append({
        **PUBLICATION_METADATA,
        "scenario_id": f"{climate['case']}__{climate['forcing_policy']}",
        "case": climate["case"],
        "display_name": climate["display_name"],
        "emissions_policy": climate["emissions_policy"],
        "matched_no_aether_case": climate["matched_no_aether_case"],
        "carbon_baseline_id": climate["carbon_baseline_id"],
        "carbon_baseline_method": climate["carbon_baseline_method"],
        "forcing_policy": climate["forcing_policy"],
        "forcing_policy_name": climate["forcing_policy_name"],
        "year": year,
        "positive_emissions_gtco2_y": round(positive, 6),
        "gross_removal_gtco2_y": round(gross, 6),
        "effective_removal_gtco2_y": round(effective, 6),
        "fair_proxy_net_co2_emissions_gtco2_y": round(direct_net, 6),
        "co2_ppm_reduced_form": round(f(climate, "co2_ppm"), 6),
        "co2_erf_w_m2": round(f(climate, "co2_erf_w_m2"), 6),
        "non_co2_positive_forcing_w_m2": round(f(climate, "non_co2_positive_forcing_w_m2"), 6),
        "aerosol_forcing_w_m2": round(f(climate, "aerosol_forcing_w_m2"), 6),
        "total_erf_w_m2": round(f(climate, "total_erf_w_m2"), 6),
        "surface_temperature_anomaly_c": round(f(climate, "surface_temperature_anomaly_c"), 6),
        "deep_ocean_temperature_index_c": round(f(climate, "deep_ocean_temperature_index_c"), 6),
        "ocean_heat_uptake_w_m2": round(f(climate, "ocean_heat_uptake_w_m2"), 6),
        "co2_concentration_join_mismatch_ppm": round(ppm_mismatch, 9),
        "fair_readiness_score_0_1": round(readiness_score, 4),
        "critical_fair_gap_count": critical_gap_count,
        "missing_or_placeholder_variable_families": missing_or_placeholder_count,
        "deck_caveat": "Conditional hybrid input scaffold, not a calibrated historical state or species-emissions FAIR run. Forcing-mode execution cannot validate these carbon concentrations; species-level non-CO2 and aerosol emissions remain missing.",
    })

groups: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
for row in deck_rows:
    groups[(str(row["case"]), str(row["forcing_policy"]))].append(row)

summary_rows: list[dict[str, object]] = []
for (case, policy), rows in sorted(groups.items()):
    rows = sorted(rows, key=lambda r: int(r["year"]))
    by_year = {int(row["year"]): row for row in rows}
    row_2026 = by_year[2026]
    row_2050 = by_year[2050]
    row_2100 = by_year[2100]
    peak = max(rows, key=lambda r: float(r["surface_temperature_anomaly_c"]))
    minimum = min(rows, key=lambda r: float(r["surface_temperature_anomaly_c"]))
    summary_rows.append({
        **PUBLICATION_METADATA,
        "case": case,
        "display_name": row_2026["display_name"],
        "emissions_policy": row_2026["emissions_policy"],
        "matched_no_aether_case": row_2026["matched_no_aether_case"],
        "carbon_baseline_id": row_2026["carbon_baseline_id"],
        "carbon_baseline_method": row_2026["carbon_baseline_method"],
        "forcing_policy": policy,
        "forcing_policy_name": row_2026["forcing_policy_name"],
        "temperature_2026_c": row_2026["surface_temperature_anomaly_c"],
        "temperature_2050_c": row_2050["surface_temperature_anomaly_c"],
        "temperature_2100_c": row_2100["surface_temperature_anomaly_c"],
        "peak_temperature_c": peak["surface_temperature_anomaly_c"],
        "peak_temperature_year": peak["year"],
        "minimum_temperature_c": minimum["surface_temperature_anomaly_c"],
        "minimum_temperature_year": minimum["year"],
        "co2_ppm_2100": row_2100["co2_ppm_reduced_form"],
        "total_erf_2100_w_m2": row_2100["total_erf_w_m2"],
        "cumulative_positive_emissions_2026_2100_gtco2": round(sum(float(row["positive_emissions_gtco2_y"]) for row in rows), 3),
        "cumulative_effective_removal_2026_2100_gtco2": round(sum(float(row["effective_removal_gtco2_y"]) for row in rows), 3),
        "cumulative_proxy_net_co2_2026_2100_gtco2": round(sum(float(row["fair_proxy_net_co2_emissions_gtco2_y"]) for row in rows), 3),
        "max_abs_join_mismatch_ppm": round(max(abs(float(row["co2_concentration_join_mismatch_ppm"])) for row in rows), 9),
        "fair_readiness_score_0_1": round(readiness_score, 4),
        "critical_fair_gap_count": critical_gap_count,
        "missing_or_placeholder_variable_families": missing_or_placeholder_count,
        "publication_use": "Quarantined FAIR/ESM handoff scaffold; do not cite as a FAIR result or absolute concentration/temperature evidence.",
    })

manifest_rows = [
    {
        "artifact": "aether_fair_readiness_input_deck.csv",
        "role": "Annual joined emissions/removal/forcing/temperature deck for FAIR-class handoff",
        "row_count": len(deck_rows),
        "status": "quarantined_hybrid_off_reference",
        "next_action": "Replace rejected carbon response with a validated historically initialized emissions-driven workflow; forcing-mode continuation does not repair it.",
    },
    {
        "artifact": "aether_fair_readiness_summary.csv",
        "role": "Scenario summary for input deck and climate-emulator consistency",
        "row_count": len(summary_rows),
        "status": "quarantined_hybrid_off_reference",
        "next_action": "Compare against FAIR output after species trajectories exist.",
    },
    {
        "artifact": "aether_fair_readiness_gap_matrix.csv",
        "role": "Variable-family gap matrix for publication-grade climate modeling",
        "row_count": len(gap_rows),
        "status": "generated",
        "next_action": "Close P0 gaps before presenting temperature claims as publication-grade.",
    },
    {
        "artifact": "aether_climate_emulator_pathways.csv",
        "role": "Source climate-emulator annual forcing and temperature paths",
        "row_count": len(climate_rows),
        "status": "quarantined_hybrid_off_reference",
        "next_action": "Replace with FAIR/ESM outputs later.",
    },
    {
        "artifact": "aether_state_dependent_carbon_pathways.csv",
        "role": "Source annual positive emissions, removal, and net-pulse paths",
        "row_count": len(state_rows),
        "status": "quarantined_hybrid_off_reference",
        "next_action": "Replace hand-set removal effectiveness with calibrated response.",
    },
]

deck_fields = [
    *PUBLICATION_METADATA,
    "scenario_id",
    "case",
    "display_name",
    "emissions_policy",
    "matched_no_aether_case",
    "carbon_baseline_id",
    "carbon_baseline_method",
    "forcing_policy",
    "forcing_policy_name",
    "year",
    "positive_emissions_gtco2_y",
    "gross_removal_gtco2_y",
    "effective_removal_gtco2_y",
    "fair_proxy_net_co2_emissions_gtco2_y",
    "co2_ppm_reduced_form",
    "co2_erf_w_m2",
    "non_co2_positive_forcing_w_m2",
    "aerosol_forcing_w_m2",
    "total_erf_w_m2",
    "surface_temperature_anomaly_c",
    "deep_ocean_temperature_index_c",
    "ocean_heat_uptake_w_m2",
    "co2_concentration_join_mismatch_ppm",
    "fair_readiness_score_0_1",
    "critical_fair_gap_count",
    "missing_or_placeholder_variable_families",
    "deck_caveat",
]
summary_fields = [
    *PUBLICATION_METADATA,
    "case",
    "display_name",
    "emissions_policy",
    "matched_no_aether_case",
    "carbon_baseline_id",
    "carbon_baseline_method",
    "forcing_policy",
    "forcing_policy_name",
    "temperature_2026_c",
    "temperature_2050_c",
    "temperature_2100_c",
    "peak_temperature_c",
    "peak_temperature_year",
    "minimum_temperature_c",
    "minimum_temperature_year",
    "co2_ppm_2100",
    "total_erf_2100_w_m2",
    "cumulative_positive_emissions_2026_2100_gtco2",
    "cumulative_effective_removal_2026_2100_gtco2",
    "cumulative_proxy_net_co2_2026_2100_gtco2",
    "max_abs_join_mismatch_ppm",
    "fair_readiness_score_0_1",
    "critical_fair_gap_count",
    "missing_or_placeholder_variable_families",
    "publication_use",
]
gap_fields = [
    "fair_variable_family",
    "current_status",
    "current_artifact",
    "publication_gap",
    "next_action",
    "priority",
]
manifest_fields = ["artifact", "role", "row_count", "status", "next_action"]

write_csv(INPUT_DECK, deck_rows, deck_fields)
write_csv(SUMMARY, summary_rows, summary_fields)
write_csv(GAP_MATRIX, gap_rows, gap_fields)
write_csv(RUN_MANIFEST, manifest_rows, manifest_fields)

print(f"Wrote {INPUT_DECK}")
print(f"Wrote {SUMMARY}")
print(f"Wrote {GAP_MATRIX}")
print(f"Wrote {RUN_MANIFEST}")

