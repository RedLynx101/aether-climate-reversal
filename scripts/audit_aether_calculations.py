#!/usr/bin/env python3
"""Arithmetic, conservation, and accounting-layer checks for generated AETHER tables.

This audit derives expectations from the checked-in input/output ledgers. It
does not treat fixed headline numbers or scenario placeholders as evidence of
scientific validity. Source quality and model adequacy remain review work.
"""

from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "analysis" / "tables"
OUT = TABLES / "aether_independent_calculation_audit.csv"
REBOUND_OUT = TABLES / "aether_rebound_accounting_thresholds.csv"
TOLERANCE = 1e-6
audit: list[dict[str, str]] = []


def rows(name: str) -> list[dict[str, str]]:
    with (TABLES / name).open(newline="", encoding="utf-8-sig") as handle:
        result = list(csv.DictReader(handle))
    if not result:
        raise ValueError(f"No rows in {name}")
    return result


def value(row: dict[str, str], *names: str) -> float:
    for name in names:
        if name in row and row[name] != "":
            return float(row[name])
    raise KeyError(f"Expected one of {names}; available: {', '.join(row)}")


def check(check_id: str, category: str, formula: str, calculated: float, expected: float, unit: str, interpretation: str, artifacts: str, tolerance: float = TOLERANCE) -> None:
    ok = math.isfinite(calculated) and math.isfinite(expected) and abs(calculated - expected) <= tolerance
    audit.append({
        "check_id": check_id, "category": category, "formula_or_rule": formula,
        "calculated_value": f"{calculated:.9f}", "expected_value": f"{expected:.9f}",
        "tolerance": f"{tolerance:.9f}", "unit": unit, "status": "pass" if ok else "fail",
        "interpretation": interpretation, "source_artifacts": artifacts,
    })


def review_required(check_id: str, interpretation: str, artifacts: str) -> None:
    """Record an evidence boundary without turning it into an artificial pass gate."""
    audit.append({
        "check_id": check_id, "category": "evidence boundary",
        "formula_or_rule": "human source and model review required", "calculated_value": "",
        "expected_value": "", "tolerance": "", "unit": "", "status": "review_required",
        "interpretation": interpretation, "source_artifacts": artifacts,
    })


def summary_value(table: str, identifier: str) -> float:
    for row in rows(table):
        if row.get("summary_id") == identifier:
            return value(row, "value")
    raise KeyError(f"Missing {identifier} in {table}")


def audit_portfolio_chain() -> None:
    allocation = rows("aether_pathway_portfolio_allocation.csv")
    summary = rows("aether_pathway_portfolio_summary.csv")[0]
    gross = sum(value(row, "aether_optimized_allocation_gtco2_y") for row in allocation)
    cost = sum(value(row, "annual_cost_trillion_usd_y") for row in allocation)
    energy = sum(value(row, "annual_energy_twh_y") for row in allocation)
    check("portfolio_gross_conservation", "portfolio", "sum(pathway gross allocation) = summary allocation", gross, value(summary, "allocated_gtco2_y"), "GtCO2/year", "Checks allocation bookkeeping only; the target remains a stress-test assumption.", "aether_pathway_portfolio_allocation.csv; aether_pathway_portfolio_summary.csv")
    check("portfolio_cost_conservation", "portfolio", "sum(pathway annual cost) = summary annual cost", cost, value(summary, "annual_cost_trillion_usd_y"), "trillion USD/year", "Checks that aggregate cost is traceable to pathway rows.", "aether_pathway_portfolio_allocation.csv; aether_pathway_portfolio_summary.csv")
    check("portfolio_energy_conservation", "portfolio", "sum(pathway annual energy) = summary annual energy", energy, value(summary, "annual_energy_twh_y"), "TWh/year", "Checks bookkeeping; it does not establish deliverable electricity or heat.", "aether_pathway_portfolio_allocation.csv; aether_pathway_portfolio_summary.csv")


def audit_lifecycle_and_mrv() -> None:
    storage_routes = rows("aether_storage_lifecycle_routes.csv")
    storage_summary = rows("aether_storage_lifecycle_summary.csv")[0]
    signed_storage_total = 0.0
    for route in storage_routes:
        gross = value(route, "gross_allocation_gtco2_y")
        retained = value(route, "physically_retained_after_100y_gtco2_y")
        lifecycle = value(route, "lifecycle_emissions_proxy_gtco2e_y")
        expected_signed = retained - lifecycle
        reported_signed = value(route, "net_after_retention_minus_lifecycle_proxy_gtco2e_y")
        signed_storage_total += reported_signed
        check(f"storage_signed_retention_then_debit_{route['pathway']}", "lifecycle accounting", "physically_retained_after_100y - lifecycle_emissions_proxy", reported_signed, expected_signed, "GtCO2e/year", "The storage proxy retains negative net results; only a later credit layer may use a zero floor.", "aether_storage_lifecycle_routes.csv", 5e-5)
        check(f"storage_retention_bound_{route['pathway']}", "lifecycle accounting", "physically retained = gross * retained fraction", retained, gross * value(route, "retained_fraction_after_100y"), "GtCO2/year", "Physical retention remains a distinct quantity from lifecycle emissions and credits.", "aether_storage_lifecycle_routes.csv", 5e-5)
    check("storage_signed_net_conservation", "lifecycle accounting", "sum(route signed net) = storage summary signed net", value(storage_summary, "net_after_retention_minus_lifecycle_proxy_gtco2e_y"), signed_storage_total, "GtCO2e/year", "Portfolio storage summary must preserve signed accounting across pathways.", "aether_storage_lifecycle_routes.csv; aether_storage_lifecycle_summary.csv", 5e-5)

    lca = rows("aether_lifecycle_emissions_by_pathway.csv")
    lca_summary = {row["power_case"]: row for row in rows("aether_lifecycle_emissions_summary.csv")}
    by_case: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in lca:
        by_case[row["power_case"]].append(row)
        gross = value(row, "gross_gtco2_y")
        retained = gross * value(row, "retained_fraction_after_100y")
        lifecycle = value(row, "annual_lifecycle_emissions_gtco2e_y")
        expected_net = retained - lifecycle
        reported_net = value(row, "net_after_retention_minus_lifecycle_emissions_gtco2e_y", "net_after_retention_minus_lifecycle_proxy_gtco2e_y", "durable_after_lca_100y_gtco2_y")
        check(f"lca_signed_retention_then_debit_{row['power_case']}_{row['pathway']}", "lifecycle accounting", "gross * retained_fraction_after_100y - lifecycle_emissions", reported_net, expected_net, "GtCO2e/year", "Signed net benefit preserves any negative physical-accounting result; lifecycle emissions are not reduced by the permanence haircut.", "aether_lifecycle_emissions_by_pathway.csv", 5e-5)
        expected_creditable = max(expected_net, 0.0) * value(row, "mrv_credit_multiplier_after_buffers")
        check(f"lca_credit_floor_then_mrv_{row['power_case']}_{row['pathway']}", "lifecycle accounting", "max(signed_net, 0) * mrv_multiplier", value(row, "creditable_after_lca_and_mrv_gtco2e_y", "creditable_after_lca_and_mrv_gtco2_y"), expected_creditable, "GtCO2e/year", "Only the credit-eligible layer is floored at zero before MRV buffers apply.", "aether_lifecycle_emissions_by_pathway.csv", 5e-5)
        if not row.get("source_keys") or row.get("evidence_class") in {"", "scenario_lca_placeholder"}:
            review_required(f"lca_source_review_{row['power_case']}_{row['pathway']}", "This LCA row is a scenario placeholder or lacks a source key; arithmetic agreement is not source validation.", "aether_lifecycle_emissions_by_pathway.csv")
    for power_case, case_rows in by_case.items():
        summary = lca_summary[power_case]
        net_total = sum(value(row, "net_after_retention_minus_lifecycle_emissions_gtco2e_y", "net_after_retention_minus_lifecycle_proxy_gtco2e_y", "durable_after_lca_100y_gtco2_y") for row in case_rows)
        creditable_total = sum(value(row, "creditable_after_lca_and_mrv_gtco2e_y", "creditable_after_lca_and_mrv_gtco2_y") for row in case_rows)
        check(f"lca_summary_net_conservation_{power_case}", "lifecycle accounting", "sum(pathway net_after_retention_minus_lifecycle)", value(summary, "net_after_retention_minus_lifecycle_emissions_gtco2e_y", "durable_after_lca_100y_gtco2_y"), net_total, "GtCO2e/year", "Summary must equal the separately accounted pathway ledger.", "aether_lifecycle_emissions_by_pathway.csv; aether_lifecycle_emissions_summary.csv")
        check(f"lca_summary_creditable_conservation_{power_case}", "lifecycle accounting", "sum(pathway creditable output)", value(summary, "creditable_after_lca_and_mrv_gtco2e_y", "creditable_after_lca_and_mrv_gtco2_y"), creditable_total, "GtCO2e/year", "Summary creditable output must equal the pathway sum.", "aether_lifecycle_emissions_by_pathway.csv; aether_lifecycle_emissions_summary.csv")

    mrv_rows = rows("aether_mrv_credit_integrity_by_pathway.csv")
    mrv_creditable = sum(value(row, "creditable_gtco2e_y_after_mrv", "creditable_gtco2_y_after_mrv") for row in mrv_rows)
    check("mrv_creditable_conservation", "MRV accounting", "sum(pathway creditable removal) = MRV summary", summary_value("aether_mrv_credit_integrity_summary.csv", "mrv_creditable_total"), mrv_creditable, "GtCO2e/year", "MRV table consistency does not validate reversal, fraud, or liability assumptions.", "aether_mrv_credit_integrity_by_pathway.csv; aether_mrv_credit_integrity_summary.csv", 0.01)


def audit_realized_learning() -> None:
    by_scenario: dict[str, list[dict[str, str]]] = defaultdict(list)
    timepaths = rows("aether_integrated_feasibility_timepaths.csv")
    check("integrated_scope_label", "integration boundary", "all integration_scope values equal partially_coupled_screening", float(all(row.get("integration_scope") == "partially_coupled_screening" for row in timepaths)), 1.0, "boolean", "The legacy screen must not be represented as a full coupled model.", "aether_integrated_feasibility_timepaths.csv", 0.0)
    for row in timepaths:
        by_scenario[row["scenario"]].append(row)
    for scenario, path in by_scenario.items():
        path.sort(key=lambda row: int(row["year"]))
        prior_cost: float | None = None
        for row in path:
            start = value(row, "cumulative_realized_production_at_start_gtco2")
            end = value(row, "cumulative_realized_production_at_end_gtco2")
            realized = value(row, "actual_capacity_gtco2_y")
            check(f"learning_state_conservation_{scenario}_{row['year']}", "learning state", "end cumulative production = start + operated annual capacity", end, start + realized, "GtCO2", "Only constrained, actually operated capacity increments learning state.", "aether_integrated_feasibility_timepaths.csv")
            cost = value(row, "learned_cost_usd_tco2")
            if prior_cost is not None:
                check(f"learning_cost_nonincreasing_{scenario}_{row['year']}", "learning state", "cost cannot increase as realized state grows", min(cost, prior_cost), cost, "USD/tCO2", "A functional-form check, not evidence that real-world learning is monotonic.", "aether_integrated_feasibility_timepaths.csv")
            prior_cost = cost
        pre_operation = [row for row in path if value(row, "actual_capacity_gtco2_y") == 0.0]
        if pre_operation:
            first, last = pre_operation[0], pre_operation[-1]
            check(f"learning_no_unbuilt_plan_credit_{scenario}", "learning state", "planned capacity cannot change cost before operation", value(last, "learned_cost_usd_tco2"), value(first, "learned_cost_usd_tco2"), "USD/tCO2", "The plan may grow while the learning state and cost remain unchanged.", "aether_integrated_feasibility_timepaths.csv")
        first_planned = next(row for row in path if value(row, "planned_linear_target_gtco2_y") > 0.0)
        check(f"learning_first_planned_year_uses_prior_state_{scenario}", "learning state", "first planned year cost = initial-state cost", value(first_planned, "learned_cost_usd_tco2"), value(path[0], "learned_cost_usd_tco2"), "USD/tCO2", "The first scheduled capacity does not earn same-year learning before it operates.", "aether_integrated_feasibility_timepaths.csv")
        review_required(f"learning_reference_review_{scenario}", "The initial cumulative-production reference is a screening proxy, not a sourced historical cumulative-production series.", "aether_integrated_feasibility_timepaths.csv")


def audit_regional_reference_conservation() -> None:
    ledger = TABLES / "aether_regional_reference_resource_ledger.csv"
    if not ledger.is_file():
        review_required("regional_reference_not_present", "Regional reference model is not present in this revision; no regional-reference conservation result is claimed.", "docs/MODEL_DEPENDENCIES.md")
        return
    energy_rows = [row for row in rows(ledger.name) if row.get("generated_energy_twh_y") or row.get("annual_electricity_allowance_twh_y")]
    if not energy_rows:
        raise ValueError(f"No energy ledger rows in {ledger.name}")
    for index, row in enumerate(energy_rows, start=1):
        allowance = value(row, "annual_electricity_allowance_twh_y", "generated_energy_twh_y")
        allocated = value(row, "allocated_electricity_twh_y", "served_load_twh_y")
        unallocated = value(row, "unallocated_electricity_allowance_twh_y", "curtailed_energy_twh_y")
        requested = value(row, "requested_electricity_load_twh_y", "requested_load_twh_y", "required_load_twh_y")
        unserved = value(row, "unserved_requested_load_twh_y", "unserved_load_twh_y")
        check(f"regional_allowance_conservation_{index}", "regional energy conservation", "annual electricity allowance = allocated + unallocated", allowance, allocated + unallocated, "TWh/year", "Annual envelope accounting; this is not an hourly generation or dispatch claim.", ledger.name)
        check(f"regional_load_conservation_{index}", "regional energy conservation", "requested load = allocated + unserved", requested, allocated + unserved, "TWh/year", "Unserved load remains explicit and is not presented as delivered energy.", ledger.name)
        check(f"regional_cyclic_storage_{index}", "regional energy conservation", "final storage - initial storage = reported change", value(row, "final_state_gwh") - value(row, "initial_state_gwh"), value(row, "storage_state_change_twh_y") * 1000.0, "GWh", "The benchmark has no implicit storage-energy carryover.", ledger.name)


def audit_nonfinite_values() -> None:
    nonfinite = 0
    for csv_path in TABLES.glob("*.csv"):
        with csv_path.open(newline="", encoding="utf-8-sig") as handle:
            for row in csv.DictReader(handle):
                for token in row.values():
                    if token and token.strip().lower() in {"nan", "+nan", "-nan", "inf", "+inf", "-inf", "infinity", "+infinity", "-infinity"}:
                        nonfinite += 1
    check("generated_csv_nonfinite_values", "data quality", "count(explicit NaN or infinity tokens)", float(nonfinite), 0.0, "tokens", "Generated tables must not hide undefined or infinite outputs.", "analysis/tables/*.csv", 0.0)


def write_outputs() -> int:
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(audit[0]))
        writer.writeheader()
        writer.writerows(audit)
    with REBOUND_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["accounting_layer", "removal_before_rebound_gtco2_y", "emissions_baseline_gtco2_y", "rebound_headroom_gtco2_y", "break_even_rebound_fraction_of_gross", "break_even_rebound_percent_of_gross", "interpretation"])
        writer.writeheader()
        lca_summary = {row["power_case"]: row for row in rows("aether_lifecycle_emissions_summary.csv")}
        removal = value(lca_summary["low_carbon_mixed_power"], "net_after_retention_minus_lifecycle_emissions_gtco2e_y", "durable_after_lca_100y_gtco2_y")
        emissions = 42.2  # Declared scenario baseline; not a current-emissions estimate.
        for layer, amount, note in (("simple_gross", 100.0, "gross scenario target before lifecycle or MRV"), ("net_after_lca_25kg", removal, "retention minus lifecycle debit at the 25 kgCO2/MWh sensitivity case")):
            headroom, fraction = amount - emissions, (amount - emissions) / 100.0
            writer.writerow({"accounting_layer": layer, "removal_before_rebound_gtco2_y": f"{amount:.6f}", "emissions_baseline_gtco2_y": f"{emissions:.6f}", "rebound_headroom_gtco2_y": f"{headroom:.6f}", "break_even_rebound_fraction_of_gross": f"{fraction:.6f}", "break_even_rebound_percent_of_gross": f"{fraction * 100.0:.3f}", "interpretation": note})
    failures = [row for row in audit if row["status"] == "fail"]
    pass_count = sum(row["status"] == "pass" for row in audit)
    review_count = sum(row["status"] == "review_required" for row in audit)
    print(f"AETHER calculation audit: {pass_count} arithmetic checks passed; {len(failures)} failed; {review_count} review boundaries recorded")
    print(f"Wrote {OUT}\nWrote {REBOUND_OUT}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['calculated_value']} vs {failure['expected_value']}")
    return 1 if failures else 0


def main() -> int:
    audit_portfolio_chain()
    audit_lifecycle_and_mrv()
    audit_realized_learning()
    audit_regional_reference_conservation()
    audit_nonfinite_values()
    return write_outputs()


if __name__ == "__main__":
    raise SystemExit(main())
