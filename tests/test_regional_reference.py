from __future__ import annotations

import copy
import csv
import importlib.util
import json
import math
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "analysis" / "scenario-models" / "aether_regional_reference_model.py"
PARAMETERS = ROOT / "data" / "regional-reference" / "parameters.csv"
SCENARIOS = ROOT / "data" / "regional-reference" / "scenarios.json"

SPEC = importlib.util.spec_from_file_location("aether_regional_reference_model", MODEL_PATH)
assert SPEC and SPEC.loader
MODEL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODEL)


class RegionalReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.parameters, cls.parameter_rows = MODEL.load_parameters(PARAMETERS)
        cls.scenarios = MODEL.load_scenarios(SCENARIOS)
        cls.outputs = MODEL.build_outputs(PARAMETERS, SCENARIOS)
        cls.by_scenario = {row["scenario_id"]: row for row in cls.outputs["summary"]}
        cls.failures = {
            (row["failure_id"], row["scenario_id"]): row
            for row in cls.outputs["failure_cases"]
        }

    def test_source_derived_energy_intensities_reproduce_netl_case(self) -> None:
        expected_electricity = 65.1 * 8760 * 0.85 / 909_225
        expected_thermal = 836 * 8760 * 0.85 / 909_225
        self.assertAlmostEqual(self.parameters["electricity_intensity"], expected_electricity, 9)
        self.assertAlmostEqual(self.parameters["thermal_intensity"], expected_thermal, 9)
        thermal_row = next(
            row for row in self.parameter_rows if row["parameter_id"] == "thermal_intensity"
        )
        self.assertEqual(thermal_row["unit"], "GJ_HHV_fuel_input_equivalent/tCO2")
        self.assertIn("not delivered useful heat", thermal_row["note"])

    def test_thermal_resource_ledger_preserves_fuel_input_equivalent_unit(self) -> None:
        thermal_rows = [
            row for row in self.outputs["resource_ledger"] if row["resource_id"] == "thermal"
        ]
        self.assertEqual(len(thermal_rows), 2)
        for row in thermal_rows:
            self.assertEqual(
                row["available_unit"], "GJ_HHV fuel-input-equivalent/year"
            )

    def test_parameter_rows_have_units_evidence_and_bounds(self) -> None:
        self.assertGreaterEqual(len(self.parameter_rows), 25)
        for row in self.parameter_rows:
            self.assertTrue(row["unit"])
            self.assertTrue(row["evidence_class"])
            self.assertLessEqual(float(row["lower_bound"]), float(row["value"]))
            self.assertLessEqual(float(row["value"]), float(row["upper_bound"]))

    def test_paired_case_contract_allows_only_operational_automation_fields(self) -> None:
        cases = self.scenarios["cases"]
        functional = MODEL.FUNCTIONAL_CASE_FIELDS
        self.assertEqual(
            functional,
            {
                "uptime_fraction",
                "task_hours_by_class",
                "hourly_task_cost_usd",
                "automation_system_cost_usd_y",
            },
        )
        for case in cases:
            self.assertEqual(set(case), MODEL.CASE_REQUIRED_FIELDS)
        self.assertEqual(cases[0]["hourly_task_cost_usd"], cases[1]["hourly_task_cost_usd"])

    def test_physical_and_cash_ledgers_conserve(self) -> None:
        parameters = self.parameters
        scenarios = MODEL.load_scenarios(SCENARIOS)
        results = [
            MODEL.evaluate_case(parameters, case, scenarios["verification"])
            for case in scenarios["cases"]
        ]
        for result in results:
            self.assertAlmostEqual(
                result["gross_capture_tco2_y"],
                result["transport_loss_tco2_y"]
                + result["injection_rejection_tco2_y"]
                + result["gross_stored_tco2_y"],
                places=6,
            )
            self.assertLessEqual(
                result["risk_adjusted_credits_tco2e_y"], result["net_retained_tco2e_y"]
            )
            self.assertLessEqual(result["net_retained_tco2e_y"], result["retained_tco2_y"])
            self.assertAlmostEqual(
                result["cash_balance_usd_y"],
                result["total_sources_usd_y"] - result["total_uses_usd_y"],
                places=2,
            )
            self.assertGreaterEqual(result["cash_balance_usd_y"], -0.01)

    def test_energy_allowance_has_no_implicit_storage_supply(self) -> None:
        parameters = self.parameters
        scenarios = MODEL.load_scenarios(SCENARIOS)
        for case in scenarios["cases"]:
            result = MODEL.evaluate_case(parameters, case, scenarios["verification"])
            self.assertAlmostEqual(
                result["annual_electricity_allowance_twh_y"],
                result["allocated_electricity_twh_y"]
                + result["unallocated_electricity_allowance_twh_y"],
                places=9,
            )
            self.assertAlmostEqual(
                result["requested_electricity_load_twh_y"],
                result["allocated_electricity_twh_y"]
                + result["unserved_requested_load_twh_y"],
                places=9,
            )
            self.assertEqual(result["initial_state_gwh"], 0.0)
            self.assertEqual(result["final_state_gwh"], 0.0)
            self.assertEqual(result["storage_state_change_twh_y"], 0.0)

    def test_lower_deliverability_inputs_cap_output(self) -> None:
        for failure_id in (
            "electricity_delivery_half",
            "thermal_delivery_half",
            "storage_acceptance_half",
            "shrinking_current_load_revenue",
        ):
            for scenario_id, baseline in self.by_scenario.items():
                stressed = self.failures[(failure_id, scenario_id)]
                self.assertLess(stressed["gross_capture_tco2_y"], baseline["gross_capture_tco2_y"])
        self.assertEqual(
            self.failures[("electricity_delivery_half", "ordinary_operations")]["binding_limit"],
            "electricity",
        )
        self.assertEqual(
            self.failures[("thermal_delivery_half", "ordinary_operations")]["binding_limit"],
            "thermal",
        )
        self.assertEqual(
            self.failures[("storage_acceptance_half", "ordinary_operations")]["binding_limit"],
            "storage",
        )
        self.assertEqual(
            self.failures[("shrinking_current_load_revenue", "ordinary_operations")][
                "binding_limit"
            ],
            "budget",
        )

    def test_resource_bottleneck_removes_automation_output_advantage(self) -> None:
        for failure_id in (
            "electricity_delivery_half",
            "thermal_delivery_half",
            "storage_acceptance_half",
        ):
            ordinary = self.failures[(failure_id, "ordinary_operations")]
            assisted = self.failures[(failure_id, "automation_assisted")]
            self.assertAlmostEqual(
                ordinary["gross_capture_tco2_y"], assisted["gross_capture_tco2_y"], places=6
            )

    def test_independent_verification_failure_stops_operation_and_credits(self) -> None:
        for scenario_id in self.by_scenario:
            result = self.failures[("independent_verification_failure", scenario_id)]
            self.assertTrue(result["stop_triggered"])
            self.assertIn("independent_verification_unavailable", result["stop_reasons"])
            self.assertEqual(result["gross_capture_tco2_y"], 0.0)
            self.assertEqual(result["risk_adjusted_credits_tco2e_y"], 0.0)

    def test_high_emissions_preserve_negative_benefit_but_issue_no_credits(self) -> None:
        parameters = dict(self.parameters)
        parameters["other_lifecycle_emissions_intensity"] = 2.0
        ordinary = self.scenarios["cases"][0]
        result = MODEL.evaluate_case(parameters, ordinary, self.scenarios["verification"])
        self.assertLess(result["net_retained_tco2e_y"], 0.0)
        self.assertAlmostEqual(
            result["net_retained_tco2e_y"],
            result["retained_tco2_y"] - result["project_emissions_tco2e_y"],
            places=6,
        )
        self.assertEqual(result["risk_adjusted_credits_tco2e_y"], 0.0)

    def test_each_verification_condition_fails_closed(self) -> None:
        ordinary = self.scenarios["cases"][0]
        overrides = (
            {"storage_mrv_plan_accepted": False},
            {"measurement_discrepancy_fraction": math.nan},
            {
                "measurement_discrepancy_fraction": (
                    self.parameters["maximum_measurement_discrepancy"] + 0.001
                )
            },
            {
                "reserve_coverage_fraction": math.nan,
            },
            {
                "reserve_coverage_fraction": (
                    self.parameters["minimum_reserve_coverage_fraction"] - 0.001
                )
            },
        )
        for override in overrides:
            verification = {**self.scenarios["verification"], **override}
            result = MODEL.evaluate_case(self.parameters, ordinary, verification)
            self.assertTrue(result["stop_triggered"])
            self.assertEqual(result["gross_capture_tco2_y"], 0.0)
            self.assertEqual(result["risk_adjusted_credits_tco2e_y"], 0.0)

    def test_scenario_numeric_validation_rejects_nonfinite_or_negative_costs(self) -> None:
        invalid_cases = (
            ("hourly_task_cost_usd", math.nan),
            ("hourly_task_cost_usd", -1),
            ("automation_system_cost_usd_y", math.inf),
            ("automation_system_cost_usd_y", -1),
        )
        for field, invalid_value in invalid_cases:
            payload = copy.deepcopy(self.scenarios)
            payload["cases"][0][field] = invalid_value
            with tempfile.TemporaryDirectory() as temporary:
                path = Path(temporary) / "scenarios.json"
                path.write_text(json.dumps(payload), encoding="utf-8")
                with self.assertRaises(ValueError):
                    MODEL.load_scenarios(path)

        payload = copy.deepcopy(self.scenarios)
        payload["failure_cases"][0]["parameter_multipliers"]["electricity_budget"] = math.nan
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "scenarios.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(ValueError):
                MODEL.load_scenarios(path)

    def test_zero_variable_cost_denominator_is_rejected(self) -> None:
        parameters = dict(self.parameters)
        for key in (
            "variable_nonenergy_opex",
            "electricity_price",
            "thermal_price",
            "transport_storage_cost",
            "reserve_contribution",
        ):
            parameters[key] = 0.0
        with self.assertRaisesRegex(ValueError, "variable_cost_per_gross"):
            MODEL.evaluate_case(
                parameters, self.scenarios["cases"][0], self.scenarios["verification"]
            )

    def test_zero_physical_denominator_is_rejected_during_input_load(self) -> None:
        for parameter_id in (
            "benchmark_nameplate_gross_capture",
            "electricity_intensity",
            "thermal_intensity",
            "transport_delivery_fraction",
            "injection_acceptance_fraction",
        ):
            rows = copy.deepcopy(self.parameter_rows)
            for row in rows:
                if row["parameter_id"] == parameter_id:
                    row["value"] = "0"
                    row["lower_bound"] = "0"
                    break
            with tempfile.TemporaryDirectory() as temporary:
                path = Path(temporary) / "parameters.csv"
                with path.open("w", newline="", encoding="utf-8") as handle:
                    writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                    writer.writeheader()
                    writer.writerows(rows)
                with self.assertRaisesRegex(ValueError, "strictly positive"):
                    MODEL.load_parameters(path)

    def test_nonfinite_parameter_bounds_are_rejected(self) -> None:
        rows = copy.deepcopy(self.parameter_rows)
        rows[0]["upper_bound"] = "Infinity"
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "parameters.csv"
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaisesRegex(ValueError, "bounds must be finite"):
                MODEL.load_parameters(path)

    def test_current_load_and_legacy_service_do_not_double_count_credits(self) -> None:
        parameters = self.parameters
        scenarios = MODEL.load_scenarios(SCENARIOS)
        for case in scenarios["cases"]:
            result = MODEL.evaluate_case(parameters, case, scenarios["verification"])
            self.assertAlmostEqual(
                result["current_load_service_tco2e_y"]
                + result["legacy_drawdown_service_tco2e_y"],
                result["risk_adjusted_credits_tco2e_y"],
                places=6,
            )
            self.assertAlmostEqual(
                result["current_load_settlement_revenue_usd_y"]
                + result["legacy_drawdown_funding_usd_y"],
                result["total_sources_usd_y"],
                places=2,
            )

    def test_output_set_is_deterministic_and_manifested(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_path = Path(first)
            second_path = Path(second)
            MODEL.write_outputs(self.outputs, first_path)
            MODEL.write_outputs(self.outputs, second_path)
            self.assertEqual(
                self.outputs["metadata"]["output_order"], list(MODEL.OUTPUT_FILENAMES)
            )
            for filename in MODEL.OUTPUT_FILENAMES:
                self.assertEqual(
                    (first_path / filename).read_bytes(),
                    (second_path / filename).read_bytes(),
                )
            manifest = json.loads(
                (first_path / "aether_regional_reference_summary.json").read_text(encoding="utf-8")
            )
            self.assertTrue(all(row["passed"] for row in manifest["invariants"]))
            self.assertTrue(math.isfinite(manifest["summary"][0]["gross_capture_tco2_y"]))

    def test_input_hashes_and_outputs_are_equivalent_for_lf_and_crlf(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temporary_path = Path(temporary)
            crlf_parameters = temporary_path / "parameters.csv"
            crlf_scenarios = temporary_path / "scenarios.json"
            for source, destination in (
                (PARAMETERS, crlf_parameters),
                (SCENARIOS, crlf_scenarios),
            ):
                lf_bytes = source.read_bytes().replace(b"\r\n", b"\n")
                destination.write_bytes(lf_bytes.replace(b"\n", b"\r\n"))

            crlf_outputs = MODEL.build_outputs(crlf_parameters, crlf_scenarios)
            self.assertEqual(self.outputs, crlf_outputs)
            self.assertEqual(
                MODEL.canonical_text_sha256(PARAMETERS),
                MODEL.canonical_text_sha256(crlf_parameters),
            )
            self.assertEqual(
                MODEL.canonical_text_sha256(SCENARIOS),
                MODEL.canonical_text_sha256(crlf_scenarios),
            )


if __name__ == "__main__":
    unittest.main()
