from __future__ import annotations

import csv
import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "analysis" / "scenario-models"
TABLE_DIR = ROOT / "analysis" / "tables"


def load_model(name: str):
    path = MODEL_DIR / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class DispatchConservationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dispatch = load_model("aether_regional_power_dispatch_model")

    def test_all_published_regions_use_cyclic_storage_and_conserve_energy(self):
        total_base = sum(r["base_clean_generation_twh_y"] for r in self.dispatch.REGIONS)
        for case in self.dispatch.CASES:
            for region in self.dispatch.REGIONS:
                with self.subTest(case=case["case"], region=region["region"]):
                    row, _ = self.dispatch.dispatch_region(
                        case, region, region["base_clean_generation_twh_y"] / total_base
                    )
                    self.assertAlmostEqual(
                        row["storage_state_start_gwh"], row["storage_state_end_gwh"], places=6
                    )
                    self.assertAlmostEqual(row["energy_balance_residual_gwh_per_day"], 0.0, places=6)
                    self.assertLessEqual(
                        row["served_load_twh_y"],
                        row["effective_generation_twh_y"] + 1e-6,
                    )

    def test_zero_generation_cannot_be_annualized_from_initial_storage(self):
        day, _ = self.dispatch.cyclic_dispatch_day([0.0] * 24, 1.0, 12.0, 0.81)
        self.assertAlmostEqual(day["storage_state_start"], 0.0)
        self.assertAlmostEqual(day["storage_state_end"], 0.0)
        self.assertAlmostEqual(day["served"], 0.0)
        self.assertAlmostEqual(day["unserved"], 24.0)

    def test_more_generation_does_not_reduce_served_load(self):
        low, _ = self.dispatch.cyclic_dispatch_day([0.25] * 24, 1.0, 4.0, 0.81)
        high, _ = self.dispatch.cyclic_dispatch_day([0.75] * 24, 1.0, 4.0, 0.81)
        self.assertGreaterEqual(high["served"], low["served"])
        self.assertAlmostEqual(low["full_energy_balance_residual"], 0.0, places=10)
        self.assertAlmostEqual(high["full_energy_balance_residual"], 0.0, places=10)


class CarbonAccountingLayerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.storage = load_model("aether_storage_lifecycle_model")
        cls.lifecycle = load_model("aether_lifecycle_emissions_model")
        cls.mrv = load_model("aether_mrv_credit_integrity_model")

    def test_lifecycle_emissions_are_not_reduced_by_physical_retention(self):
        for model in (self.storage, self.lifecycle):
            with self.subTest(model=model.__name__):
                retained, net = model.account_retention_and_lifecycle(10.0, 0.8, 2.0)
                self.assertAlmostEqual(retained, 8.0)
                self.assertAlmostEqual(net, 6.0)
                self.assertNotAlmostEqual(net, (10.0 - 2.0) * 0.8)

    def test_zero_input_and_monotonic_accounting(self):
        retained, net = self.lifecycle.account_retention_and_lifecycle(0.0, 0.5, 0.0)
        self.assertEqual((retained, net), (0.0, 0.0))
        _, high_retention = self.lifecycle.account_retention_and_lifecycle(10.0, 0.9, 1.0)
        _, low_retention = self.lifecycle.account_retention_and_lifecycle(10.0, 0.7, 1.0)
        _, high_emissions = self.lifecycle.account_retention_and_lifecycle(10.0, 0.9, 2.0)
        self.assertGreater(high_retention, low_retention)
        self.assertGreater(high_retention, high_emissions)

    def test_net_burden_remains_negative_while_credit_floors_at_zero(self):
        for model in (self.storage, self.lifecycle):
            with self.subTest(model=model.__name__):
                retained, signed_net = model.account_retention_and_lifecycle(10.0, 0.2, 3.0)
                self.assertAlmostEqual(retained, 2.0)
                self.assertAlmostEqual(signed_net, -1.0)
                self.assertIsNone(model.gross_required_for_positive_net(10.0, signed_net))
        multiplier, credit = self.mrv.apply_mrv_credit_buffers(-1.0, [0.1, 0.2])
        self.assertAlmostEqual(multiplier, 0.72)
        self.assertEqual(credit, 0.0)

    def test_mrv_credit_is_a_distinct_downstream_layer(self):
        multiplier, credit = self.mrv.apply_mrv_credit_buffers(8.0, [0.1, 0.2])
        self.assertAlmostEqual(multiplier, 0.72)
        self.assertAlmostEqual(credit, 5.76)
        _, zero_credit = self.mrv.apply_mrv_credit_buffers(0.0, [0.1])
        _, tighter_credit = self.mrv.apply_mrv_credit_buffers(8.0, [0.2, 0.2])
        self.assertEqual(zero_credit, 0.0)
        self.assertLess(tighter_credit, credit)

    def test_generated_lifecycle_rows_follow_retention_minus_emissions_identity(self):
        with (TABLE_DIR / "aether_lifecycle_emissions_by_pathway.csv").open(
            newline="", encoding="utf-8-sig"
        ) as handle:
            rows = list(csv.DictReader(handle))
        self.assertTrue(rows)
        for row in rows:
            with self.subTest(power_case=row["power_case"], pathway=row["pathway"]):
                retained = float(row["physically_retained_after_100y_gtco2_y"])
                emissions = float(row["annual_lifecycle_emissions_gtco2e_y"])
                net = float(row["net_after_retention_minus_lifecycle_emissions_gtco2e_y"])
                credit = float(row["creditable_after_lca_and_mrv_gtco2e_y"])
                multiplier = float(row["mrv_credit_multiplier_after_buffers"])
                self.assertAlmostEqual(net, retained - emissions, places=5)
                self.assertAlmostEqual(credit, max(net, 0.0) * multiplier, places=5)


class CorrelatedScenarioLabelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = load_model("aether_correlated_uncertainty_model")

    def test_shifted_families_disclose_marginal_and_dependence_changes(self):
        original_sample_count = self.model.SAMPLES_PER_FAMILY
        self.model.SAMPLES_PER_FAMILY = 4
        try:
            rows, scenarios = self.model.run_samples(self.model.read_parameters())
        finally:
            self.model.SAMPLES_PER_FAMILY = original_sample_count
        independent = next(s for s in scenarios if s["scenario_family"] == "independent_reference")
        shifted = [s for s in scenarios if s["scenario_family"] != "independent_reference"]
        self.assertEqual(independent["marginal_treatment"], "unchanged triangular marginals")
        for scenario in shifted:
            self.assertIn("marginals shifted", scenario["marginal_treatment"])
            self.assertIn("shared family shock", scenario["dependence_treatment"])
            self.assertIn("not correlation-only", scenario["paper_use_rule"])
        shifted_sample = next(r for r in rows if r["scenario_family"] != "independent_reference")
        self.assertEqual(shifted_sample["marginals_changed_from_reference"], 1.0)
        self.assertEqual(shifted_sample["dependence_introduced"], 1.0)


if __name__ == "__main__":
    unittest.main()
