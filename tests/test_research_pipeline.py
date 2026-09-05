from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INTEGRATED_MODEL = ROOT / "analysis" / "scenario-models" / "aether_integrated_feasibility_model.py"
REPRODUCTION_SCRIPT = ROOT / "scripts" / "reproduce_research.py"


def load_integrated_model():
    spec = importlib.util.spec_from_file_location("aether_integrated_feasibility_model", INTEGRATED_MODEL)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {INTEGRATED_MODEL}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_reproduction_script():
    spec = importlib.util.spec_from_file_location("aether_reproduce_research", REPRODUCTION_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {REPRODUCTION_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ResearchPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = load_integrated_model()
        cls.reference = next(s for s in cls.model.scenarios() if s.key == "reference_extrapolation")
        cls.reproduction = load_reproduction_script()

    def test_learning_state_only_advances_with_operated_capacity(self) -> None:
        path = self.model.capacity_limited_path(self.reference)
        for row in path:
            self.assertAlmostEqual(
                row["cumulative_realized_production_at_end_gtco2"],
                row["cumulative_realized_production_at_start_gtco2"] + row["actual_capacity_gtco2_y"],
            )

    def test_unbuilt_plan_does_not_reduce_cost(self) -> None:
        path = self.model.capacity_limited_path(self.reference)
        startup, first_planned = path[:2]
        self.assertEqual(startup["actual_capacity_gtco2_y"], 0.0)
        self.assertGreater(first_planned["planned_linear_target_gtco2_y"], 0.0)
        self.assertEqual(
            startup["cumulative_realized_production_at_start_gtco2"],
            first_planned["cumulative_realized_production_at_start_gtco2"],
        )
        self.assertEqual(startup["learned_cost_usd_tco2"], first_planned["learned_cost_usd_tco2"])

    def test_integrated_screen_declares_partial_coupling(self) -> None:
        row = self.model.capacity_limited_path(self.reference)[0]
        self.assertEqual(row["integration_scope"], "partially_coupled_screening")
        self.assertIn("does not establish a common feasible scenario", row["integration_note"])

    def test_dependency_contract_documents_safe_check(self) -> None:
        dependencies = (ROOT / "docs" / "MODEL_DEPENDENCIES.md").read_text(encoding="utf-8")
        reproducibility = (ROOT / "docs" / "reproducibility.md").read_text(encoding="utf-8")
        self.assertIn("aether_regional_reference_model.py", dependencies)
        self.assertIn("scripts/reproduce_research.py --check", reproducibility)

    def test_reproduction_accepts_csv_line_ending_only_difference(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkout = root / "checkout.csv"
            generated = root / "generated.csv"
            checkout.write_bytes(b"metric,value\r\nnet,83.568044\r\n")
            generated.write_bytes(b"metric,value\nnet,83.568044\n")
            self.assertTrue(self.reproduction.outputs_match(checkout, generated))

    def test_reproduction_rejects_csv_numeric_difference(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkout = root / "checkout.csv"
            generated = root / "generated.csv"
            checkout.write_text("metric,value\nnet,83.568044\n", encoding="utf-8")
            generated.write_text("metric,value\nnet,83.568045\n", encoding="utf-8")
            self.assertFalse(self.reproduction.outputs_match(checkout, generated))

    def test_reproduction_excludes_local_environment_and_build_cache(self) -> None:
        ignored = self.reproduction.ignored_copy_paths(
            "unused",
            [".env", ".env.local", ".next", "analysis", "node_modules"],
        )
        self.assertEqual(ignored, {".env", ".env.local", ".next", "node_modules"})


if __name__ == "__main__":
    unittest.main()
