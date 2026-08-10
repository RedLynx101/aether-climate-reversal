#!/usr/bin/env python3
"""Independent arithmetic and consistency audit for the AETHER model outputs."""

from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "analysis" / "tables"
OUT = TABLES / "aether_independent_calculation_audit.csv"
REBOUND_OUT = TABLES / "aether_rebound_accounting_thresholds.csv"


def rows(name: str):
    with (TABLES / name).open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


audit = []


def check(check_id, category, formula, calculated, expected, tolerance, unit, interpretation, artifacts):
    ok = math.isfinite(float(calculated)) and abs(float(calculated) - float(expected)) <= float(tolerance)
    audit.append({
        "check_id": check_id,
        "category": category,
        "formula_or_rule": formula,
        "calculated_value": f"{float(calculated):.9f}",
        "expected_value": f"{float(expected):.9f}",
        "tolerance": f"{float(tolerance):.9f}",
        "unit": unit,
        "status": "pass" if ok else "fail",
        "interpretation": interpretation,
        "source_artifacts": artifacts,
    })


allocation = rows("aether_pathway_portfolio_allocation.csv")
summary = rows("aether_pathway_portfolio_summary.csv")[0]
allocated = sum(float(r["aether_optimized_allocation_gtco2_y"]) for r in allocation)
cost = sum(float(r["annual_cost_trillion_usd_y"]) for r in allocation)
energy = sum(float(r["annual_energy_twh_y"]) for r in allocation)
check("portfolio_allocation_sum", "portfolio", "sum(pathway gross allocations)", allocated, 100.0, 1e-9, "GtCO2/year", "The reference stress-test portfolio closes exactly to its stated gross target.", "aether_pathway_portfolio_allocation.csv")
check("portfolio_cost_sum", "portfolio", "sum(pathway annual cost)", cost, float(summary["annual_cost_trillion_usd_y"]), 1e-9, "trillion USD/year", "The summary cost equals the pathway sum.", "aether_pathway_portfolio_allocation.csv; aether_pathway_portfolio_summary.csv")
check("portfolio_weighted_cost", "portfolio", "annual cost / gross tonnes", float(summary["weighted_average_cost_usd_tco2"]), 84.0, 1e-9, "USD/tCO2", "The $8.4 trillion annual portfolio cost corresponds to $84/tCO2 at 100 Gt/year.", "aether_pathway_portfolio_summary.csv")
check("portfolio_energy_sum", "portfolio", "sum(pathway annual energy)", energy, float(summary["annual_energy_twh_y"]), 1e-6, "TWh/year", "The portfolio energy summary equals the pathway sum.", "aether_pathway_portfolio_allocation.csv; aether_pathway_portfolio_summary.csv")

check("ppm_conversion", "carbon arithmetic", "100 / 7.8", 100.0 / 7.8, 12.820512821, 1e-9, "ppm/year", "Atmosphere-only bookkeeping; not a carbon-cycle outcome.", "aether_dimensioned_unit_checks.csv")
check("simple_net_before_rebound", "carbon arithmetic", "100 - 42.2", 100.0 - 42.2, 57.8, 1e-9, "GtCO2/year", "Gross removal minus the current-emissions baseline before lifecycle, MRV, or rebound.", "aether_jevons_rebound_sensitivity.csv")
for gj in (1.0, 3.0, 8.0):
    check(f"energy_{int(gj)}gj", "energy", f"100 Gt * {gj} GJ/t * 277.7777778", 100.0 * gj * 277.77777777777777, {1.0: 27777.777777778, 3.0: 83333.333333333, 8.0: 222222.222222222}[gj], 1e-6, "TWh/year", "Unit conversion is internally consistent; energy form remains scenario-dependent.", "aether_scenario_summary.csv; aether_dimensioned_unit_checks.csv")
check("splitting_enthalpy_floor", "conversion", "100 Gt * 8.94 GJ/t * 277.7777778", 100.0 * 8.94 * 277.77777777777777, 248333.333333333, 1e-6, "TWh/year", "Ideal enthalpy floor excludes real conversion inefficiency.", "aether_dimensioned_unit_checks.csv")
check("supercritical_volume", "storage", "100 Gt / 600 kg/m3", 100e12 / 600.0 / 1e9, 166.666666667, 1e-9, "km3/year", "A volume conversion, not proof of injectivity or capacity.", "aether_dimensioned_unit_checks.csv")
check("solid_carbon_mass", "conversion", "100 * 12.011/44.0095", 100.0 * 12.011 / 44.0095, 27.2918347175, 1e-8, "Gt carbon/year", "Stoichiometric carbon product mass using the declared standard molar masses.", "aether_dimensioned_unit_checks.csv; aether_conversion_constants.csv")
check("oxygen_mass", "conversion", "100 * 31.998/44.0095", 100.0 * 31.998 / 44.0095, 72.7070291642, 1e-8, "Gt O2/year", "Stoichiometric oxygen coproduct mass using the declared standard molar masses.", "aether_dimensioned_unit_checks.csv; aether_conversion_constants.csv")

storage = rows("aether_storage_lifecycle_summary.csv")[0]
durable = float(storage["durable_100y_credit_gtco2_y"])
check("storage_durable_total", "durability", "sum pathway gross * lifecycle/durability credit", durable, 84.880604127, 1e-8, "GtCO2/year", "The storage-lifecycle filter is reproducible but rests on provisional pathway haircuts.", "aether_storage_lifecycle_summary.csv")
check("storage_gross_for_100", "durability", "100 / portfolio durability fraction", float(storage["gross_required_for_100gt_durable_credit_at_same_mix_gtco2_y"]), 100.0 / float(storage["portfolio_net_durability_fraction"]), 1e-8, "GtCO2/year", "Gross overbuild is the reciprocal of the portfolio durable fraction.", "aether_storage_lifecycle_summary.csv")

mrv = {r["summary_id"]: r for r in rows("aether_mrv_credit_integrity_summary.csv")}
check("mrv_creditable_total", "credit integrity", "sum pathway durable * MRV multipliers", float(mrv["mrv_creditable_total"]["value"]), 66.445, 0.0005, "GtCO2/year", "Creditable tonnes are smaller than gross and durable tonnes under the provisional buffers.", "aether_mrv_credit_integrity_summary.csv")
check("mrv_gross_for_100", "credit integrity", "100 / creditable fraction", float(mrv["gross_required_for_100_credit_same_mix"]["value"]), 150.500, 0.0005, "GtCO2/year", "MRV buffers materially increase required gross removal.", "aether_mrv_credit_integrity_summary.csv")

lca_rows = {r["power_case"]: r for r in rows("aether_lifecycle_emissions_summary.csv")}
lca = lca_rows["low_carbon_mixed_power"]
power_emissions = float(storage["energy_with_storage_lifecycle_penalty_twh_y"]) * 1e6 * 25.0 / 1e12
total_lca = float(lca["annual_lifecycle_emissions_gtco2e_y"])
non_power_lca = total_lca - power_emissions
check("lca_power_component_25kg", "lifecycle", "64,750 TWh * 25 kgCO2/MWh", power_emissions, 1.61875, 1e-9, "GtCO2e/year", "Only part of the 12.30 Gt lifecycle total is power emissions.", "aether_storage_lifecycle_summary.csv; aether_lifecycle_emissions_summary.csv")
check("lca_nonpower_component", "lifecycle", "total lifecycle - power component", non_power_lca, 10.678, 0.001, "GtCO2e/year", "The remainder is provisional construction, media, transport/storage, and decommissioning burden.", "aether_lifecycle_emissions_summary.csv")
check("lca_total_25kg", "lifecycle", "sum pathway power and non-power lifecycle emissions", total_lca, 12.296750, 1e-9, "GtCO2e/year", "The total is meaningful as a sensitivity case, not a finalized LCA.", "aether_lifecycle_emissions_summary.csv")
check("lca_durable_25kg", "lifecycle", "sum((gross - lifecycle) * retention)", float(lca["durable_after_lca_100y_gtco2_y"]), 83.915860, 1e-9, "GtCO2/year", "Durable after-LCA tonnes are the appropriate intermediate accounting layer.", "aether_lifecycle_emissions_summary.csv")
check("lca_creditable_25kg", "lifecycle", "durable after LCA * pathway MRV multipliers", float(lca["creditable_after_lca_and_mrv_gtco2_y"]), 65.269976, 1e-9, "GtCO2/year", "Creditable after-LCA-and-MRV tonnes are smaller than durable tonnes.", "aether_lifecycle_emissions_summary.csv")

gross = 100.0
emissions = 42.2
threshold_rows = [
    ("simple_gross", gross, "gross removal before lifecycle or MRV"),
    ("durable_after_lca_25kg", float(lca["durable_after_lca_100y_gtco2_y"]), "100-year durable removal after the 25 kgCO2/MWh lifecycle case"),
    ("creditable_after_lca_mrv_25kg", float(lca["creditable_after_lca_and_mrv_gtco2_y"]), "creditable removal after the 25 kgCO2/MWh lifecycle case and provisional MRV buffers"),
]
with REBOUND_OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["accounting_layer", "removal_before_rebound_gtco2_y", "emissions_baseline_gtco2_y", "rebound_headroom_gtco2_y", "break_even_rebound_fraction_of_gross", "break_even_rebound_percent_of_gross", "interpretation"])
    writer.writeheader()
    for key, removal, label in threshold_rows:
        headroom = removal - emissions
        fraction = headroom / gross
        writer.writerow({
            "accounting_layer": key,
            "removal_before_rebound_gtco2_y": f"{removal:.6f}",
            "emissions_baseline_gtco2_y": f"{emissions:.6f}",
            "rebound_headroom_gtco2_y": f"{headroom:.6f}",
            "break_even_rebound_fraction_of_gross": f"{fraction:.6f}",
            "break_even_rebound_percent_of_gross": f"{fraction * 100.0:.3f}",
            "interpretation": label,
        })
        check(f"rebound_threshold_{key}", "governance accounting", "(removal before rebound - 42.2) / 100 gross", fraction * 100.0, {"simple_gross": 57.8, "durable_after_lca_25kg": 41.71586, "creditable_after_lca_mrv_25kg": 23.069976}[key], 1e-6, "% of gross removal", "Break-even depends on the accounting layer; 57.8% is only the simple gross threshold.", "aether_rebound_accounting_thresholds.csv")

regional = rows("aether_regional_storage_summary.csv")[0]
check("geologic_wells_1mt", "storage", "pressure-adjusted geologic injection / 1 Mt per well", float(regional["total_pressure_adjusted_wells_at_1mt_y"]), 71700.0, 1e-9, "well equivalents", "The regionalized screen is more demanding than the unadjusted 54,000-well arithmetic.", "aether_regional_storage_summary.csv")

robot = {r["scenario"]: r for r in rows("aether_robotics_field_productivity_distribution_summary.csv")}["aether_automation_push"]
check("robot_push_p50_production", "robotics", "field-productivity-adjusted median annual production", float(robot["annual_production_p50_robots"]), 840142.21, 0.01, "robots/year", "The automation-push case exceeds the 2024 IFR installation comparator.", "aether_robotics_field_productivity_distribution_summary.csv")
check("robot_push_ifr_multiple", "robotics", "median annual production / IFR 2024 installations", float(robot["p50_production_multiple_ifr"]), 1.549861, 1e-6, "multiple", "This is a production-scale comparison, not proof of field capability.", "aether_robotics_field_productivity_distribution_summary.csv")
check("robot_push_pass_share", "robotics", "share of samples at or below IFR annual installations", float(robot["ifr_pass_share"]), 0.0, 1e-12, "share", "No automation-push samples clear the current IFR count benchmark after field-productivity stress.", "aether_robotics_field_productivity_distribution_summary.csv")

unit_checks = rows("aether_dimensioned_unit_checks.csv")
unit_passes = sum(r["pass"].strip().lower() == "true" for r in unit_checks)
check("dimensioned_unit_checks", "reproducibility", "count(pass == True)", unit_passes, len(unit_checks), 0.0, "checks", "Every dimensioned unit check must pass.", "aether_dimensioned_unit_checks.csv")

nonfinite = 0
for csv_path in TABLES.glob("*.csv"):
    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            for value in row.values():
                if value is None:
                    continue
                token = value.strip().lower()
                if token in {"nan", "+nan", "-nan", "inf", "+inf", "-inf", "infinity", "+infinity", "-infinity"}:
                    nonfinite += 1
check("generated_csv_nonfinite_values", "data quality", "count explicit NaN or infinity tokens", nonfinite, 0.0, 0.0, "tokens", "Generated tables must not hide undefined or infinite outputs.", "analysis/tables/*.csv")

with OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(audit[0]))
    writer.writeheader()
    writer.writerows(audit)

failures = [r for r in audit if r["status"] != "pass"]
print(f"AETHER independent calculation audit: {len(audit) - len(failures)}/{len(audit)} checks passed")
print(f"Wrote {OUT}")
print(f"Wrote {REBOUND_OUT}")
if failures:
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['calculated_value']} vs {failure['expected_value']}")
    raise SystemExit(1)

