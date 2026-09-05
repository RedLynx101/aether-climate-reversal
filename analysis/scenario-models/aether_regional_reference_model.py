"""Bounded regional DAC-plus-storage and public-utility reference model.

This is one annual analytical benchmark, not an hourly dispatch model, plant
design, permit application, cost forecast, or tariff recommendation.  The two
paired cases share every physical and financial input except the explicitly
whitelisted automation/operations fields in ``scenarios.json``.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PARAMETERS = ROOT / "data" / "regional-reference" / "parameters.csv"
DEFAULT_SCENARIOS = ROOT / "data" / "regional-reference" / "scenarios.json"
DEFAULT_OUTPUT_DIR = ROOT / "analysis" / "tables"

OUTPUT_FILENAMES = (
    "aether_regional_reference_summary.csv",
    "aether_regional_reference_resource_ledger.csv",
    "aether_regional_reference_utility_ledger.csv",
    "aether_regional_reference_failure_cases.csv",
    "aether_regional_reference_invariants.csv",
    "aether_regional_reference_summary.json",
)

CASE_REQUIRED_FIELDS = {
    "scenario_id",
    "case_label",
    "uptime_fraction",
    "task_hours_by_class",
    "hourly_task_cost_usd",
    "automation_system_cost_usd_y",
    "evidence_class",
    "interpretation",
}
FUNCTIONAL_CASE_FIELDS = {
    "uptime_fraction",
    "task_hours_by_class",
    "hourly_task_cost_usd",
    "automation_system_cost_usd_y",
}
REQUIRED_PARAMETERS = {
    "benchmark_nameplate_gross_capture",
    "electricity_intensity",
    "thermal_intensity",
    "transport_delivery_fraction",
    "injection_acceptance_fraction",
    "retention_fraction",
    "electricity_emissions_intensity",
    "thermal_emissions_intensity",
    "other_lifecycle_emissions_intensity",
    "measurement_discount_fraction",
    "risk_buffer_fraction",
    "maximum_measurement_discrepancy",
    "electricity_budget",
    "thermal_budget",
    "storage_injection_budget",
    "capital_basis",
    "annual_capital_charge_factor",
    "fixed_non_task_opex",
    "variable_nonenergy_opex",
    "electricity_price",
    "thermal_price",
    "transport_storage_cost",
    "reserve_contribution",
    "current_load_subject_to_settlement",
    "current_load_settlement_rate",
    "legacy_drawdown_funding",
    "minimum_reserve_coverage_fraction",
}


def _finite_nonnegative(value: float, label: str) -> float:
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"{label} must be finite and nonnegative, got {value!r}")
    return value


def load_parameters(path: Path) -> tuple[dict[str, float], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    expected = {
        "parameter_id", "value", "unit", "category", "evidence_class",
        "source_id", "source_url", "lower_bound", "upper_bound", "note",
    }
    if not rows or set(rows[0]) != expected:
        raise ValueError(f"Parameter schema must be exactly {sorted(expected)}")
    if len({row["parameter_id"] for row in rows}) != len(rows):
        raise ValueError("parameter_id values must be unique")
    values: dict[str, float] = {}
    for row in rows:
        parameter_id = row["parameter_id"]
        value = _finite_nonnegative(float(row["value"]), parameter_id)
        low = float(row["lower_bound"])
        high = float(row["upper_bound"])
        if not math.isfinite(low) or not math.isfinite(high) or low > high:
            raise ValueError(f"{parameter_id} bounds must be finite and ordered")
        if not low <= value <= high:
            raise ValueError(f"{parameter_id}={value} is outside [{low}, {high}]")
        if not row["unit"] or not row["evidence_class"] or not row["note"]:
            raise ValueError(f"{parameter_id} is missing units/evidence/note metadata")
        values[parameter_id] = value
    missing = REQUIRED_PARAMETERS - values.keys()
    if missing:
        raise ValueError(f"Missing required parameters: {sorted(missing)}")
    for fraction in (
        "transport_delivery_fraction", "injection_acceptance_fraction",
        "retention_fraction", "measurement_discount_fraction",
        "risk_buffer_fraction", "maximum_measurement_discrepancy",
        "minimum_reserve_coverage_fraction",
    ):
        if values[fraction] > 1:
            raise ValueError(f"{fraction} must not exceed one")
    for denominator in (
        "benchmark_nameplate_gross_capture",
        "electricity_intensity",
        "thermal_intensity",
        "transport_delivery_fraction",
        "injection_acceptance_fraction",
    ):
        if values[denominator] <= 0:
            raise ValueError(f"{denominator} must be strictly positive")
    return values, rows


def load_scenarios(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    cases = payload.get("cases", [])
    if len(cases) != 2 or {case.get("scenario_id") for case in cases} != {
        "ordinary_operations", "automation_assisted"
    }:
        raise ValueError(
            "Exactly the ordinary_operations and automation_assisted cases are required"
        )
    for case in cases:
        if set(case) != CASE_REQUIRED_FIELDS:
            raise ValueError(
                f"{case.get('scenario_id')} fields must be exactly {sorted(CASE_REQUIRED_FIELDS)}"
            )
        if not 0 <= float(case["uptime_fraction"]) <= 1:
            raise ValueError("uptime_fraction must be between zero and one")
        hours = case["task_hours_by_class"]
        if set(hours) != {"operations", "maintenance", "measurement_reporting_verification"}:
            raise ValueError("task_hours_by_class has an unexpected class")
        for task, value in hours.items():
            _finite_nonnegative(float(value), f"{case['scenario_id']}.{task}")
        _finite_nonnegative(
            float(case["hourly_task_cost_usd"]),
            f"{case['scenario_id']}.hourly_task_cost_usd",
        )
        _finite_nonnegative(
            float(case["automation_system_cost_usd_y"]),
            f"{case['scenario_id']}.automation_system_cost_usd_y",
        )
    allowed_failure_parameters = {
        "electricity_budget", "thermal_budget", "storage_injection_budget",
        "current_load_subject_to_settlement", "legacy_drawdown_funding",
    }
    for failure in payload.get("failure_cases", []):
        multipliers = failure.get("parameter_multipliers", {})
        unexpected = set(multipliers) - allowed_failure_parameters
        if unexpected:
            raise ValueError(f"Failure case changes out-of-scope parameters: {sorted(unexpected)}")
        for parameter_id, multiplier in multipliers.items():
            _finite_nonnegative(float(multiplier), f"{failure.get('failure_id')}.{parameter_id}")
    return payload


def _verification_stop_reasons(
    parameters: dict[str, float], verification: dict[str, Any]
) -> list[str]:
    reasons: list[str] = []
    independent_passed = verification.get("independent_verification_passed", False)
    storage_plan_accepted = verification.get("storage_mrv_plan_accepted", False)
    if independent_passed is not True:
        reasons.append("independent_verification_unavailable")
    if storage_plan_accepted is not True:
        reasons.append("storage_mrv_plan_not_accepted")
    try:
        discrepancy = float(verification.get("measurement_discrepancy_fraction", math.inf))
    except (TypeError, ValueError):
        discrepancy = math.nan
    if not math.isfinite(discrepancy) or discrepancy < 0:
        reasons.append("mass_balance_discrepancy_invalid")
    elif discrepancy > parameters["maximum_measurement_discrepancy"]:
        reasons.append("mass_balance_discrepancy_above_threshold")
    try:
        reserve_coverage = float(verification.get("reserve_coverage_fraction", math.nan))
    except (TypeError, ValueError):
        reserve_coverage = math.nan
    if not math.isfinite(reserve_coverage) or reserve_coverage < 0:
        reasons.append("reserve_coverage_invalid")
    elif reserve_coverage < parameters["minimum_reserve_coverage_fraction"]:
        reasons.append("reserve_coverage_below_threshold")
    return reasons


def evaluate_case(
    parameters: dict[str, float],
    case: dict[str, Any],
    verification: dict[str, Any],
) -> dict[str, Any]:
    p = parameters
    stop_reasons = _verification_stop_reasons(p, verification)
    storage_yield = p["transport_delivery_fraction"] * p["injection_acceptance_fraction"]
    emissions_per_gross = (
        p["electricity_intensity"] * p["electricity_emissions_intensity"]
        + p["thermal_intensity"] * p["thermal_emissions_intensity"]
        + p["other_lifecycle_emissions_intensity"]
    )
    retained_per_gross = storage_yield * p["retention_fraction"]
    net_retained_per_gross = retained_per_gross - emissions_per_gross
    credit_yield = (
        max(net_retained_per_gross, 0.0)
        * (1 - p["measurement_discount_fraction"])
        * (1 - p["risk_buffer_fraction"])
    )

    total_task_hours = sum(float(value) for value in case["task_hours_by_class"].values())
    task_labor = total_task_hours * float(case["hourly_task_cost_usd"])
    automation_system = float(case["automation_system_cost_usd_y"])
    annual_capital_charge = p["capital_basis"] * p["annual_capital_charge_factor"]
    fixed_uses = annual_capital_charge + p["fixed_non_task_opex"] + task_labor + automation_system
    variable_cost_per_gross = (
        p["variable_nonenergy_opex"]
        + p["electricity_intensity"] * p["electricity_price"]
        + p["thermal_intensity"] * p["thermal_price"]
        + p["transport_storage_cost"]
        + credit_yield * p["reserve_contribution"]
    )
    if variable_cost_per_gross <= 0 or not math.isfinite(variable_cost_per_gross):
        raise ValueError("variable_cost_per_gross must be finite and strictly positive")
    settlement_revenue = (
        p["current_load_subject_to_settlement"] * p["current_load_settlement_rate"]
    )
    total_sources = settlement_revenue + p["legacy_drawdown_funding"]

    nameplate_limit = p["benchmark_nameplate_gross_capture"]
    uptime_limit = nameplate_limit * float(case["uptime_fraction"])
    electricity_limit = p["electricity_budget"] / p["electricity_intensity"]
    thermal_limit = p["thermal_budget"] / p["thermal_intensity"]
    storage_limit = p["storage_injection_budget"] / storage_yield
    budget_limit = max(total_sources - fixed_uses, 0.0) / variable_cost_per_gross
    limits = {
        "nameplate": nameplate_limit,
        "uptime": uptime_limit,
        "electricity": electricity_limit,
        "thermal": thermal_limit,
        "storage": storage_limit,
        "budget": budget_limit,
    }
    binding_limit = min(limits, key=limits.get)
    gross = 0.0 if stop_reasons else limits[binding_limit]
    transport_loss = gross * (1 - p["transport_delivery_fraction"])
    delivered = gross - transport_loss
    injection_rejection = delivered * (1 - p["injection_acceptance_fraction"])
    gross_stored = delivered - injection_rejection
    retained = gross_stored * p["retention_fraction"]
    emissions = gross * emissions_per_gross
    net_retained = retained - emissions
    risk_adjusted_credits = (
        max(net_retained, 0.0)
        * (1 - p["measurement_discount_fraction"])
        * (1 - p["risk_buffer_fraction"])
    )

    electricity_used = gross * p["electricity_intensity"]
    thermal_used = gross * p["thermal_intensity"]
    variable_nonenergy = gross * p["variable_nonenergy_opex"]
    electricity_cost = electricity_used * p["electricity_price"]
    thermal_cost = thermal_used * p["thermal_price"]
    transport_storage_cost = gross * p["transport_storage_cost"]
    reserve = risk_adjusted_credits * p["reserve_contribution"]
    total_uses = (
        annual_capital_charge + p["fixed_non_task_opex"] + task_labor
        + automation_system + variable_nonenergy + electricity_cost + thermal_cost
        + transport_storage_cost + reserve
    )
    cash_balance = total_sources - total_uses

    current_service = min(risk_adjusted_credits, p["current_load_subject_to_settlement"])
    legacy_service = max(risk_adjusted_credits - current_service, 0.0)
    current_shortfall = max(p["current_load_subject_to_settlement"] - current_service, 0.0)

    # This annual benchmark has no electric storage subsystem. Zero initial and
    # final states make the boundary explicit instead of silently supplying energy.
    requested_electricity = uptime_limit * p["electricity_intensity"]
    electricity_allowance = p["electricity_budget"]
    unserved_requested_load = max(requested_electricity - electricity_used, 0.0)
    unallocated_allowance = max(electricity_allowance - electricity_used, 0.0)

    return {
        "scenario_id": case["scenario_id"],
        "case_label": case["case_label"],
        "interpretation": case["interpretation"],
        "uptime_fraction": float(case["uptime_fraction"]),
        "total_task_hours_y": total_task_hours,
        "task_labor_cost_usd_y": task_labor,
        "automation_system_cost_usd_y": automation_system,
        "limits": limits,
        "binding_limit": "verification_stop" if stop_reasons else binding_limit,
        "stop_triggered": bool(stop_reasons),
        "stop_reasons": stop_reasons,
        "gross_capture_tco2_y": gross,
        "transport_loss_tco2_y": transport_loss,
        "delivered_to_storage_tco2_y": delivered,
        "injection_rejection_tco2_y": injection_rejection,
        "gross_stored_tco2_y": gross_stored,
        "retained_tco2_y": retained,
        "project_emissions_tco2e_y": emissions,
        "net_retained_tco2e_y": net_retained,
        "risk_adjusted_credits_tco2e_y": risk_adjusted_credits,
        "electricity_used_mwh_y": electricity_used,
        "thermal_used_gj_y": thermal_used,
        "annual_electricity_allowance_twh_y": electricity_allowance / 1_000_000,
        "requested_electricity_load_twh_y": requested_electricity / 1_000_000,
        "allocated_electricity_twh_y": electricity_used / 1_000_000,
        "unserved_requested_load_twh_y": unserved_requested_load / 1_000_000,
        "unallocated_electricity_allowance_twh_y": unallocated_allowance / 1_000_000,
        "initial_state_gwh": 0.0,
        "final_state_gwh": 0.0,
        "storage_state_change_twh_y": 0.0,
        "current_load_service_tco2e_y": current_service,
        "legacy_drawdown_service_tco2e_y": legacy_service,
        "current_load_service_shortfall_tco2e_y": current_shortfall,
        "current_load_settlement_revenue_usd_y": settlement_revenue,
        "legacy_drawdown_funding_usd_y": p["legacy_drawdown_funding"],
        "annual_capital_charge_usd_y": annual_capital_charge,
        "fixed_non_task_opex_usd_y": p["fixed_non_task_opex"],
        "variable_nonenergy_opex_usd_y": variable_nonenergy,
        "electricity_cost_usd_y": electricity_cost,
        "thermal_cost_usd_y": thermal_cost,
        "transport_storage_cost_usd_y": transport_storage_cost,
        "reserve_contribution_usd_y": reserve,
        "total_sources_usd_y": total_sources,
        "total_uses_usd_y": total_uses,
        "cash_balance_usd_y": cash_balance,
    }


def _with_multipliers(
    parameters: dict[str, float], multipliers: dict[str, float]
) -> dict[str, float]:
    result = dict(parameters)
    for parameter_id, multiplier in multipliers.items():
        result[parameter_id] *= float(multiplier)
    return result


def _summary_row(result: dict[str, Any], scope: str) -> dict[str, Any]:
    keys = (
        "scenario_id", "case_label", "uptime_fraction", "total_task_hours_y",
        "gross_capture_tco2_y", "gross_stored_tco2_y", "project_emissions_tco2e_y",
        "retained_tco2_y", "net_retained_tco2e_y", "risk_adjusted_credits_tco2e_y",
        "current_load_service_tco2e_y", "legacy_drawdown_service_tco2e_y",
        "electricity_used_mwh_y", "thermal_used_gj_y", "total_sources_usd_y",
        "total_uses_usd_y", "cash_balance_usd_y", "binding_limit", "stop_triggered",
    )
    row = {key: result[key] for key in keys}
    row["benchmark_scope"] = scope
    row["claim_boundary"] = (
        "Analytical mechanism test only; no field validation, cost-reduction forecast, "
        "plant/permit claim, or economically optimal tariff."
    )
    return row


def _resource_rows(result: dict[str, Any], parameters: dict[str, float]) -> list[dict[str, Any]]:
    p = parameters
    storage_intensity = p["transport_delivery_fraction"] * p["injection_acceptance_fraction"]
    if result["gross_capture_tco2_y"]:
        storage_intensity = result["gross_stored_tco2_y"] / result["gross_capture_tco2_y"]
    budget_intensity = 0.0
    if result["gross_capture_tco2_y"]:
        budget_intensity = result["total_uses_usd_y"] / result["gross_capture_tco2_y"]
    specifications = (
        ("nameplate", p["benchmark_nameplate_gross_capture"], "tCO2/year", 1.0),
        ("uptime", result["limits"]["uptime"], "tCO2/year gross capacity", 1.0),
        ("electricity", p["electricity_budget"], "MWh/year", p["electricity_intensity"]),
        (
            "thermal",
            p["thermal_budget"],
            "GJ_HHV fuel-input-equivalent/year",
            p["thermal_intensity"],
        ),
        (
            "storage",
            p["storage_injection_budget"],
            "tCO2/year gross stored",
            storage_intensity,
        ),
        ("budget", result["total_sources_usd_y"], "USD/year", budget_intensity),
    )
    rows: list[dict[str, Any]] = []
    for resource_id, available, unit, intensity in specifications:
        maximum = result["limits"][resource_id]
        rows.append({
            "scenario_id": result["scenario_id"],
            "resource_id": resource_id,
            "available_quantity": available,
            "available_unit": unit,
            "use_intensity_per_gross_tco2": intensity,
            "maximum_gross_capture_tco2_y": maximum,
            "actual_gross_capture_tco2_y": result["gross_capture_tco2_y"],
            "headroom_tco2_y": max(maximum - result["gross_capture_tco2_y"], 0.0),
            "is_binding": result["binding_limit"] == resource_id,
            "annual_electricity_allowance_twh_y": (
                result["annual_electricity_allowance_twh_y"]
                if resource_id == "electricity"
                else ""
            ),
            "requested_electricity_load_twh_y": (
                result["requested_electricity_load_twh_y"]
                if resource_id == "electricity"
                else ""
            ),
            "allocated_electricity_twh_y": (
                result["allocated_electricity_twh_y"]
                if resource_id == "electricity"
                else ""
            ),
            "unserved_requested_load_twh_y": (
                result["unserved_requested_load_twh_y"]
                if resource_id == "electricity"
                else ""
            ),
            "unallocated_electricity_allowance_twh_y": (
                result["unallocated_electricity_allowance_twh_y"]
                if resource_id == "electricity"
                else ""
            ),
            "initial_state_gwh": (
                result["initial_state_gwh"] if resource_id == "electricity" else ""
            ),
            "final_state_gwh": (
                result["final_state_gwh"] if resource_id == "electricity" else ""
            ),
            "storage_state_change_twh_y": (
                result["storage_state_change_twh_y"] if resource_id == "electricity" else ""
            ),
            "boundary_note": (
                "Annual allowance/allocation envelope, not actual generation, dispatch, "
                "or curtailment; no electric storage subsystem and zero state change."
                if resource_id == "electricity"
                else ""
            ),
        })
    return rows


def _utility_rows(result: dict[str, Any]) -> list[dict[str, Any]]:
    accounts = (
        (
            "cash_source",
            "current_load_settlements",
            result["current_load_settlement_revenue_usd_y"],
            "Current-load emissions settlement; not legacy drawdown funding.",
        ),
        (
            "cash_source",
            "legacy_drawdown_funding",
            result["legacy_drawdown_funding_usd_y"],
            "Separately identified funding for historical atmospheric drawdown.",
        ),
        (
            "cash_use",
            "annual_capital_charge",
            result["annual_capital_charge_usd_y"],
            "Annual capital carrying charge; capital basis is not expensed again.",
        ),
        (
            "cash_use",
            "fixed_non_task_opex",
            result["fixed_non_task_opex_usd_y"],
            "Fixed O&M excluding task labor and automation system.",
        ),
        (
            "cash_use",
            "task_labor",
            result["task_labor_cost_usd_y"],
            "Case-specific operations, maintenance, and verification task hours.",
        ),
        (
            "cash_use",
            "automation_system",
            result["automation_system_cost_usd_y"],
            "Explicit automation-system cost; zero in ordinary case.",
        ),
        (
            "cash_use",
            "variable_nonenergy_opex",
            result["variable_nonenergy_opex_usd_y"],
            "Consumables/non-energy variable O&M only.",
        ),
        (
            "cash_use",
            "electricity",
            result["electricity_cost_usd_y"],
            "Electrical demand priced separately from heat.",
        ),
        (
            "cash_use",
            "thermal_energy",
            result["thermal_cost_usd_y"],
            "Thermal-service proxy priced per GJ_HHV fuel-input-equivalent; no "
            "conversion efficiency or electrical-equivalent substitution.",
        ),
        (
            "cash_use",
            "transport_and_storage",
            result["transport_storage_cost_usd_y"],
            "Transport/storage service once; not embedded in non-energy O&M.",
        ),
        (
            "cash_use",
            "restricted_risk_reserve",
            result["reserve_contribution_usd_y"],
            "Cash reserve tied to risk-adjusted credits; not a physical-emissions debit.",
        ),
        (
            "cash_balance",
            "surplus_or_deficit",
            result["cash_balance_usd_y"],
            "Sources minus uses; nonnegative because budget is an output cap.",
        ),
    )
    rows = [{
        "scenario_id": result["scenario_id"], "ledger_section": section,
        "account": account, "amount": amount, "unit": "USD/year", "note": note,
    } for section, account, amount, note in accounts]
    rows.extend(
        [
            {
                "scenario_id": result["scenario_id"],
                "ledger_section": "physical_service",
                "account": "current_load_settlement_service",
                "amount": result["current_load_service_tco2e_y"],
                "unit": "tCO2e/year risk-adjusted",
                "note": "Credits allocated first to the current-load settlement obligation.",
            },
            {
                "scenario_id": result["scenario_id"],
                "ledger_section": "physical_service",
                "account": "legacy_drawdown_service",
                "amount": result["legacy_drawdown_service_tco2e_y"],
                "unit": "tCO2e/year risk-adjusted",
                "note": (
                    "Credits remaining after current-load settlement; not financed by "
                    "relabeling current-load revenue."
                ),
            },
            {
                "scenario_id": result["scenario_id"],
                "ledger_section": "physical_service",
                "account": "current_load_service_shortfall",
                "amount": result["current_load_service_shortfall_tco2e_y"],
                "unit": "tCO2e/year risk-adjusted",
                "note": "Unsettled current-load obligation carried as a service shortfall.",
            },
        ]
    )
    return rows


def _close(a: float, b: float, tolerance: float = 1e-6) -> bool:
    return math.isclose(a, b, rel_tol=1e-10, abs_tol=tolerance)


def canonical_text_sha256(path: Path) -> str:
    """Hash text with CRLF normalized to LF for cross-platform provenance."""
    canonical_bytes = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(canonical_bytes).hexdigest()


def _invariant_rows(
    baseline: list[dict[str, Any]], failure_rows: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    def add(name: str, passed: bool, evidence: str) -> None:
        rows.append({"invariant_id": name, "passed": passed, "evidence": evidence})

    for result in baseline:
        scenario = result["scenario_id"]
        physical_chain_ordered = (
            0
            <= result["risk_adjusted_credits_tco2e_y"]
            <= max(result["net_retained_tco2e_y"], 0.0)
            and result["net_retained_tco2e_y"] <= result["retained_tco2_y"]
            <= result["gross_stored_tco2_y"]
            <= result["delivered_to_storage_tco2_y"]
            <= result["gross_capture_tco2_y"]
        )
        add(
            f"{scenario}.physical_chain_ordered",
            physical_chain_ordered,
            "credits <= positive net benefit; signed net <= retained <= stored <= "
            "delivered <= captured",
        )
        add(
            f"{scenario}.signed_net_identity",
            _close(
                result["net_retained_tco2e_y"],
                result["retained_tco2_y"] - result["project_emissions_tco2e_y"],
            ),
            "signed net retained = retained storage - project emissions; no zero floor",
        )
        add(
            f"{scenario}.co2_mass_balance",
            _close(
                result["gross_capture_tco2_y"],
                result["transport_loss_tco2_y"]
                + result["gross_stored_tco2_y"]
                + result["injection_rejection_tco2_y"],
            ),
            "captured = transport loss + injection rejection + gross stored",
        )
        add(
            f"{scenario}.cash_reconciles",
            _close(
                result["total_sources_usd_y"] - result["total_uses_usd_y"],
                result["cash_balance_usd_y"],
                0.01,
            )
            and result["cash_balance_usd_y"] >= -0.01,
            "cash balance = distinct sources - distinct uses and is nonnegative",
        )
        add(
            f"{scenario}.electricity_allowance_reconciles",
            _close(
                result["annual_electricity_allowance_twh_y"],
                result["allocated_electricity_twh_y"]
                + result["unallocated_electricity_allowance_twh_y"],
            )
            and _close(
                result["requested_electricity_load_twh_y"],
                result["allocated_electricity_twh_y"]
                + result["unserved_requested_load_twh_y"],
            ),
            "allowance = allocated + unallocated; requested = allocated + unserved",
        )
        add(
            f"{scenario}.cyclic_electric_storage_boundary",
            _close(result["initial_state_gwh"], result["final_state_gwh"])
            and _close(result["storage_state_change_twh_y"], 0),
            "no electric storage subsystem; initial = final = 0",
        )
        resource_limits_hold = (
            result["electricity_used_mwh_y"]
            <= result["annual_electricity_allowance_twh_y"] * 1_000_000 + 1e-6
            and result["gross_capture_tco2_y"] <= min(result["limits"].values()) + 1e-6
        )
        add(
            f"{scenario}.resource_limits",
            resource_limits_hold,
            "energy use and gross capture remain within every deliverability cap",
        )

    ordinary = next(row for row in baseline if row["scenario_id"] == "ordinary_operations")
    assisted = next(row for row in baseline if row["scenario_id"] == "automation_assisted")
    add(
        "paired_cases.only_automation_fields_vary",
        True,
        f"functional case whitelist={sorted(FUNCTIONAL_CASE_FIELDS)}; all other inputs shared",
    )
    add(
        "paired_cases.automation_not_worse_under_shared_physical_limits",
        assisted["gross_capture_tco2_y"] >= ordinary["gross_capture_tco2_y"],
        "higher assumed uptime/lower task hours cannot reduce output under shared physicals",
    )

    indexed = {(row["failure_id"], row["scenario_id"]): row for row in failure_rows}
    monotonic_failures = (
        "electricity_delivery_half",
        "thermal_delivery_half",
        "storage_acceptance_half",
        "shrinking_current_load_revenue",
        "legacy_drawdown_funding_zero",
    )
    for failure_id in monotonic_failures:
        for reference in baseline:
            stressed = indexed[(failure_id, reference["scenario_id"])]
            add(
                f"{reference['scenario_id']}.{failure_id}.nonincreasing_output",
                stressed["gross_capture_tco2_y"]
                <= reference["gross_capture_tco2_y"] + 1e-6,
                "lower resource/funding input cannot increase gross output",
            )
    for reference in baseline:
        stopped = indexed[("independent_verification_failure", reference["scenario_id"])]
        add(
            f"{reference['scenario_id']}.verification_fail_closed",
            stopped["stop_triggered"]
            and _close(stopped["gross_capture_tco2_y"], 0)
            and _close(stopped["risk_adjusted_credits_tco2e_y"], 0),
            "independent-verification failure stops operation and credit issuance",
        )
    return rows


def build_outputs(parameters_path: Path, scenarios_path: Path) -> dict[str, Any]:
    parameters, parameter_rows = load_parameters(parameters_path)
    scenarios = load_scenarios(scenarios_path)
    baseline = [
        evaluate_case(parameters, case, scenarios["verification"])
        for case in scenarios["cases"]
    ]
    failures: list[dict[str, Any]] = []
    for failure in scenarios["failure_cases"]:
        stressed_parameters = _with_multipliers(
            parameters, failure.get("parameter_multipliers", {})
        )
        stressed_verification = {
            **scenarios["verification"],
            **failure.get("verification_overrides", {}),
        }
        for case in scenarios["cases"]:
            result = evaluate_case(stressed_parameters, case, stressed_verification)
            failures.append({
                "failure_id": failure["failure_id"],
                "failure_description": failure["description"],
                "parameter_multipliers": json.dumps(
                    failure.get("parameter_multipliers", {}), sort_keys=True
                ),
                "verification_overrides": json.dumps(
                    failure.get("verification_overrides", {}), sort_keys=True
                ),
                **result,
            })
    resource_rows = [row for result in baseline for row in _resource_rows(result, parameters)]
    utility_rows = [row for result in baseline for row in _utility_rows(result)]
    invariants = _invariant_rows(baseline, failures)
    if not all(row["passed"] for row in invariants):
        failed = [row["invariant_id"] for row in invariants if not row["passed"]]
        raise AssertionError(f"Regional-reference invariants failed: {failed}")
    return {
        "metadata": {
            "model_id": scenarios["model_id"],
            "benchmark_scope": scenarios["benchmark_scope"],
            "paired_case_rule": scenarios["paired_case_rule"],
            "parameters_sha256": canonical_text_sha256(parameters_path),
            "scenarios_sha256": canonical_text_sha256(scenarios_path),
            "input_hash_contract": (
                "SHA-256 of source bytes after explicit CRLF-to-LF normalization."
            ),
            "output_order": list(OUTPUT_FILENAMES),
            "parameter_count": len(parameter_rows),
            "claim_boundary": (
                "Analytical mechanism test only; not field validation, an actual plant or "
                "permit claim, a cost-reduction forecast, or an economically optimal tariff."
            ),
        },
        "summary": [_summary_row(result, scenarios["benchmark_scope"]) for result in baseline],
        "resource_ledger": resource_rows,
        "utility_ledger": utility_rows,
        "failure_cases": failures,
        "invariants": invariants,
    }


def _csv_safe(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    safe: list[dict[str, Any]] = []
    for row in rows:
        safe.append({
            key: (
                json.dumps(value, sort_keys=True)
                if isinstance(value, (dict, list))
                else round(value, 6)
                if isinstance(value, float)
                else value
            )
            for key, value in row.items()
        })
    return safe


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"No rows for {path}")
    rows = _csv_safe(rows)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(outputs: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    sections = ("summary", "resource_ledger", "utility_ledger", "failure_cases", "invariants")
    for filename, section in zip(OUTPUT_FILENAMES[:-1], sections, strict=True):
        _write_csv(output_dir / filename, outputs[section])
    (output_dir / OUTPUT_FILENAMES[-1]).write_text(
        json.dumps(outputs, indent=2, sort_keys=False) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parameters", type=Path, default=DEFAULT_PARAMETERS)
    parser.add_argument("--scenarios", type=Path, default=DEFAULT_SCENARIOS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = build_outputs(args.parameters.resolve(), args.scenarios.resolve())
    write_outputs(outputs, args.output_dir.resolve())
    print(
        f"Wrote {len(OUTPUT_FILENAMES)} regional-reference outputs to "
        f"{args.output_dir.resolve()}"
    )


if __name__ == "__main__":
    main()
