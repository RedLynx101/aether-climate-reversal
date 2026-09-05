"""Scientific regression invariants for the conditional carbon/climate screen.

These tests detect initialization and attribution regressions. Passing them is
not validation of a historical carbon state or a climate forecast.
"""
from __future__ import annotations

import csv
from dataclasses import replace
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis" / "scenario-models"))
import aether_carbon_cycle_model as carbon
import aether_state_dependent_carbon_model as state


def read_table(name: str) -> list[dict[str, str]]:
    with (ROOT / "analysis" / "tables" / name).open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


class CarbonBaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scenarios = carbon.default_scenarios()
        cls.rows = carbon.annual_rows(cls.scenarios)
        cls.by_case = {scenario.case: [row for row in cls.rows if row["case"] == scenario.case] for scenario in cls.scenarios}

    def test_source_is_pinned_and_complete_without_constant_initial_offset(self):
        manifest = json.loads((carbon.BASELINE_DIR / "provenance.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["dataset_doi"], "10.5281/zenodo.4589756")
        self.assertEqual(manifest["files"]["concentrations"]["md5"], "0d82c3c3cdd4dd632b2bb9449a5c315f")
        self.assertEqual(manifest["files"]["emissions"]["md5"], "4044106f55ca65b094670e7577eaf9b3")
        self.assertEqual(len(carbon.load_reference_baseline()), 251)
        self.assertEqual(carbon.START_CO2_PPM, carbon.REFERENCE_BASELINE[2025]["co2_ppm"])
        self.assertNotEqual(carbon.START_CO2_PPM, 428.53)

    def test_source_sparse_years_use_only_bracketed_linear_interpolation(self):
        with (carbon.BASELINE_DIR / "rcmip_ssp245_co2_1850_2100.csv").open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        blanks_tested = 0
        for source_key, model_key, scale in [("reference_co2_ppm", "co2_ppm", 1.0), ("reference_emissions_mtco2_y", "emissions_gtco2_y", 0.001)]:
            known = {int(row["year"]): float(row[source_key]) * scale for row in rows if row[source_key]}
            for row in rows:
                year = int(row["year"])
                if not row[source_key]:
                    before = max(y for y in known if y < year)
                    after = min(y for y in known if y > year)
                    expected = known[before] + (known[after] - known[before]) * (year - before) / (after - before)
                    self.assertAlmostEqual(carbon.REFERENCE_BASELINE[year][model_key], expected, places=10)
                    blanks_tested += 1
        self.assertGreater(blanks_tested, 0)

    def test_extract_checksum_and_values_survive_lf_and_crlf_checkouts(self):
        filename = "rcmip_ssp245_co2_1850_2100.csv"
        canonical = (carbon.BASELINE_DIR / filename).read_bytes().replace(b"\r\n", b"\n")
        manifest_text = (carbon.BASELINE_DIR / "provenance.json").read_text(encoding="utf-8")
        self.assertEqual(json.loads(manifest_text)["extract_hash_line_endings"], "LF")
        # Fixture writes are confined to an OS-generated, task-specific temp
        # directory; the committed source extract is never modified.
        with TemporaryDirectory(prefix="aether-carbon-newlines-") as directory:
            fixture_dir = Path(directory)
            (fixture_dir / "provenance.json").write_text(manifest_text, encoding="utf-8")
            for newline_name, payload in [("LF", canonical), ("CRLF", canonical.replace(b"\n", b"\r\n"))]:
                with self.subTest(line_endings=newline_name):
                    (fixture_dir / filename).write_bytes(payload)
                    with patch.object(carbon, "BASELINE_DIR", fixture_dir):
                        self.assertEqual(carbon.load_reference_baseline(), carbon.REFERENCE_BASELINE)

    def test_canonical_checksum_still_rejects_numeric_tampering(self):
        filename = "rcmip_ssp245_co2_1850_2100.csv"
        canonical = (carbon.BASELINE_DIR / filename).read_bytes().replace(b"\r\n", b"\n")
        manifest_text = (carbon.BASELINE_DIR / "provenance.json").read_text(encoding="utf-8")
        tampered = canonical.replace(b"284.3169987996419", b"285.3169987996419", 1)
        self.assertNotEqual(tampered, canonical)
        with TemporaryDirectory(prefix="aether-carbon-integrity-") as directory:
            fixture_dir = Path(directory)
            (fixture_dir / "provenance.json").write_text(manifest_text, encoding="utf-8")
            (fixture_dir / filename).write_bytes(tampered.replace(b"\n", b"\r\n"))
            with patch.object(carbon, "BASELINE_DIR", fixture_dir):
                with self.assertRaisesRegex(ValueError, "checksum mismatch"):
                    carbon.load_reference_baseline()

    def test_reference_emissions_reproduce_published_evolving_concentration(self):
        scenario = replace(self.scenarios[0], emissions_policy="reference_ssp245")
        rows = carbon.annual_rows([scenario])
        for row in rows:
            self.assertAlmostEqual(float(row["atmospheric_co2_ppm_reduced_form"]), carbon.REFERENCE_BASELINE[row["year"]]["co2_ppm"], places=10)
            self.assertAlmostEqual(float(row["future_emissions_anomaly_vs_reference_gtco2_y"]), 0.0, places=10)
        self.assertNotEqual(rows[0]["atmospheric_co2_ppm_reduced_form"], rows[-1]["atmospheric_co2_ppm_reduced_form"])

    def test_zero_future_response_failure_is_detected_and_rejected(self):
        scenario = replace(self.scenarios[0], emissions_policy="zero_future")
        rows = carbon.annual_rows([scenario])
        concentrations = [float(row["atmospheric_co2_ppm_reduced_form"]) for row in rows]
        self.assertGreater(max(concentrations) - min(concentrations), 1.0)
        # This failed scientific acceptance check is preserved, not tuned away.
        # Tests assert that the known anomaly is detected AND quarantined.
        self.assertLess(min(concentrations), concentrations[0])
        self.assertGreater(concentrations[-1], concentrations[0])
        diagnostics = read_table("aether_carbon_baseline_diagnostics.csv")
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0]["zero_future_response_check"], "fail_unresolved_reference_response_mismatch")
        self.assertEqual(diagnostics[0]["absolute_projection_accepted"], "false")
        self.assertAlmostEqual(float(diagnostics[0]["final_2100_diagnostic_ppm"]), concentrations[-1], places=10)
        base_rows = [{key: str(value) for key, value in row.items()} for row in rows]
        state_rows = state.simulate_case(scenario.case, base_rows, state.EFFECTIVENESS_CASES[0])
        for left, right in zip(rows, state_rows):
            self.assertAlmostEqual(float(left["atmospheric_co2_ppm_reduced_form"]), float(right["atmospheric_co2_ppm_reduced_form"]), places=5)

    def test_known_future_pulse_is_added_once_relative_to_reference(self):
        scenario = replace(self.scenarios[0], emissions_policy="reference_ssp245")
        def emissions(_scenario, year):
            return carbon.REFERENCE_BASELINE[year]["emissions_gtco2_y"] + (7.8 if year == 2030 else 0.0)
        with patch.object(carbon, "emissions_for_year", side_effect=emissions):
            rows = carbon.annual_rows([scenario])
        for row in rows:
            year = int(row["year"])
            expected = carbon.REFERENCE_BASELINE[year]["co2_ppm"]
            if year >= 2030:
                expected += carbon.joos_airborne_fraction(year - 2030)
            self.assertAlmostEqual(float(row["atmospheric_co2_ppm_reduced_form"]), expected, places=10)

    def test_every_default_case_has_same_co2_policy_no_aether_control(self):
        scenarios = {scenario.case: scenario for scenario in self.scenarios}
        for scenario in self.scenarios:
            control = scenarios[carbon.matched_control_case(scenario.emissions_policy)]
            self.assertEqual(control.emissions_policy, scenario.emissions_policy)
            self.assertEqual(control.removal_target_gtco2_y, 0.0)
            for year in range(2026, 2101):
                self.assertEqual(carbon.emissions_for_year(scenario, year), carbon.emissions_for_year(control, year))

    def test_floor_rebound_and_fixed_state_screen_match_carbon_screen(self):
        for scenario in self.scenarios:
            base_rows = [{key: str(value) for key, value in row.items()} for row in self.by_case[scenario.case]]
            state_rows = state.simulate_case(scenario.case, base_rows, state.EFFECTIVENESS_CASES[0])
            for actual, expected in zip(state_rows, self.by_case[scenario.case]):
                self.assertAlmostEqual(float(actual["atmospheric_co2_ppm_reduced_form"]), float(expected["atmospheric_co2_ppm_reduced_form"]), places=5)
                self.assertAlmostEqual(float(actual["induced_or_delayed_emissions_gtco2_y"]), scenario.rebound_fraction_of_removal * float(actual["actual_gross_removal_gtco2_y"]), places=5)
                if scenario.atmospheric_management_floor_ppm is not None:
                    self.assertGreaterEqual(float(actual["atmospheric_co2_ppm_reduced_form"]), scenario.atmospheric_management_floor_ppm - 0.000001)

    def test_all_exported_climate_comparators_use_identical_policies(self):
        for filename, temperature, avoided, extra in [
            ("aether_climate_response_summary.csv", "co2_only_transient_proxy_2100_c", "transient_proxy_avoided_vs_no_aether_2100_c", []),
            ("aether_climate_emulator_summary.csv", "temperature_2100_c", "avoided_temperature_vs_no_aether_2100_c", ["forcing_policy"]),
            ("aether_fair_forcing_summary.csv", "fair_temperature_2100_c", "avoided_temperature_vs_matched_no_aether_2100_c", ["forcing_policy", "config"]),
        ]:
            rows = read_table(filename)
            index = {(row["case"], *(row[key] for key in extra)): row for row in rows}
            for row in rows:
                control = index[(row["matched_no_aether_case"], *(row[key] for key in extra))]
                self.assertEqual(row["emissions_policy"], control["emissions_policy"])
                self.assertAlmostEqual(float(row[avoided]), float(control[temperature]) - float(row[temperature]), places=5)
                if row["case"] == row["matched_no_aether_case"]:
                    self.assertEqual(float(row[avoided]), 0.0)

    def test_regenerated_carbon_table_matches_current_code(self):
        exported = read_table("aether_carbon_cycle_pathways.csv")
        self.assertEqual(len(exported), len(self.rows))
        for actual, expected in zip(exported, self.rows):
            self.assertEqual(actual["case"], expected["case"])
            self.assertEqual(actual["matched_no_aether_case"], expected["matched_no_aether_case"])
            for column in ["atmospheric_co2_ppm_reduced_form", "gross_aether_removal_gtco2_y", "reference_co2_ppm", "future_emissions_anomaly_vs_reference_gtco2_y", "co2_difference_vs_matched_no_aether_ppm"]:
                self.assertAlmostEqual(float(actual[column]), float(expected[column]), places=10)

    def test_readiness_join_is_consistent_and_still_diagnostic(self):
        for row in read_table("aether_fair_readiness_input_deck.csv"):
            self.assertLessEqual(abs(float(row["co2_concentration_join_mismatch_ppm"])), 0.00001)
            self.assertIn("cannot validate", row["deck_caveat"])
        for row in read_table("aether_fair_forcing_summary.csv"):
            self.assertIn("does not validate upstream carbon cycle", row["publication_use"])

    def test_every_affected_trajectory_and_summary_blocks_absolute_promotion(self):
        filenames = [
            "aether_carbon_cycle_pathways.csv", "aether_carbon_cycle_summary.csv",
            "aether_state_dependent_carbon_pathways.csv", "aether_state_dependent_carbon_summary.csv",
            "aether_climate_response_pathways.csv", "aether_climate_response_summary.csv",
            "aether_climate_emulator_pathways.csv", "aether_climate_emulator_summary.csv",
            "aether_fair_readiness_input_deck.csv", "aether_fair_readiness_summary.csv",
            "aether_fair_forcing_temperature_paths.csv", "aether_fair_forcing_summary.csv",
            "aether_fair_forcing_delta_vs_emulator.csv",
            "aether_species_emissions_handoff_pathways.csv", "aether_species_emissions_summary.csv",
        ]
        for filename in filenames:
            for row in read_table(filename):
                self.assertEqual(row["publication_status"], "quarantined_hybrid_off_reference", filename)
                self.assertEqual(row["absolute_projection_accepted"], "false", filename)
                self.assertIn("response fails", row["failure_reason"], filename)


if __name__ == "__main__":
    unittest.main()
