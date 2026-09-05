#!/usr/bin/env python3
"""Safely regenerate the core AETHER research tables and compare them to the tree.

``--check`` never writes under the repository.  It copies the repository to a
temporary directory, runs the declared dependency order there, and byte-compares
the resulting CSV/JSON outputs with the checked-in outputs.  The comparison is
intentionally narrow: it verifies deterministic generation, not the validity of
the scenario assumptions or an integrated physical result.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "analysis" / "tables"


@dataclass(frozen=True)
class Step:
    name: str
    script: str
    outputs: tuple[str, ...]


# The order is an interface contract, not an assertion that all of these
# independent scenario families can be numerically combined.  See
# docs/MODEL_DEPENDENCIES.md for accounting and compatibility boundaries.
CORE_STEPS = (
    Step(
        "pathway portfolio",
        "analysis/scenario-models/aether_pathway_portfolio_model.py",
        (
            "aether_pathway_portfolio_allocation.csv",
            "aether_pathway_portfolio_summary.csv",
            "aether_pathway_source_gap_analysis.csv",
        ),
    ),
    Step(
        "storage lifecycle",
        "analysis/scenario-models/aether_storage_lifecycle_model.py",
        ("aether_storage_lifecycle_routes.csv", "aether_storage_lifecycle_summary.csv"),
    ),
    Step(
        "MRV integrity",
        "analysis/scenario-models/aether_mrv_credit_integrity_model.py",
        (
            "aether_mrv_credit_integrity_assumptions.csv",
            "aether_mrv_credit_integrity_by_pathway.csv",
            "aether_mrv_credit_integrity_summary.csv",
        ),
    ),
    Step(
        "lifecycle emissions",
        "analysis/scenario-models/aether_lifecycle_emissions_model.py",
        (
            "aether_lifecycle_emissions_assumptions.csv",
            "aether_lifecycle_emissions_by_pathway.csv",
            "aether_lifecycle_emissions_summary.csv",
        ),
    ),
    Step(
        "regional dispatch diagnostic",
        "analysis/scenario-models/aether_regional_power_dispatch_model.py",
        (
            "aether_regional_power_region_assumptions.csv",
            "aether_regional_power_dispatch_cases.csv",
            "aether_regional_power_dispatch_by_region.csv",
            "aether_regional_power_hourly_sample.csv",
            "aether_regional_power_colocation_scorecard.csv",
            "aether_regional_power_dispatch_summary.csv",
        ),
    ),
    Step(
        "legacy partially-coupled feasibility screen",
        "analysis/scenario-models/aether_integrated_feasibility_model.py",
        (
            "aether_integrated_feasibility_timepaths.csv",
            "aether_integrated_feasibility_scenarios.csv",
            "aether_integrated_feasibility_bottlenecks.csv",
        ),
    ),
)

AUDIT_OUTPUTS = (
    "aether_independent_calculation_audit.csv",
    "aether_rebound_accounting_thresholds.csv",
)


def ignored_copy_paths(_: str, names: list[str]) -> set[str]:
    """Exclude local caches and environment files from the isolated rerun."""
    ignored = {".git", ".venv", ".next", "node_modules", "work", "__pycache__"}
    return {name for name in names if name in ignored or name.startswith(".env")}


def run(stage: Path, relative_script: str, *args: str) -> None:
    command = [sys.executable, str(stage / relative_script), *args]
    print("+", " ".join(command))
    subprocess.run(command, cwd=stage, check=True)


def canonical_output_bytes(path: Path) -> bytes:
    """Normalize only line endings in textual generated CSV/JSON artifacts.

    Git's checkout policy can change LF to CRLF on Windows.  This avoids a
    platform-only mismatch while retaining every other byte: headers, values,
    ordering, encoding marker, and whitespace other than newline form remain
    comparison-significant. Non-CSV/JSON files are always compared as bytes.
    """
    content = path.read_bytes()
    if path.suffix.lower() not in {".csv", ".json"}:
        return content
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        return content
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def outputs_match(source: Path, generated: Path) -> bool:
    return canonical_output_bytes(source) == canonical_output_bytes(generated)


def compare_output(source: Path, generated: Path, differences: list[str]) -> None:
    if not source.is_file():
        differences.append(f"missing checked-in output: {source.relative_to(ROOT)}")
    elif not generated.is_file():
        differences.append(f"model did not generate: {generated.name}")
    elif not outputs_match(source, generated):
        differences.append(f"stale or non-deterministic output: {source.relative_to(ROOT)}")


def run_optional_regional_reference(stage: Path) -> tuple[str, ...]:
    """Run the forthcoming regional reference model only when its contract exists."""
    script = stage / "analysis" / "scenario-models" / "aether_regional_reference_model.py"
    if not script.is_file():
        return ()
    parameters = stage / "data" / "regional-reference" / "parameters.csv"
    scenarios = stage / "data" / "regional-reference" / "scenarios.json"
    if not parameters.is_file() or not scenarios.is_file():
        raise RuntimeError("regional reference script exists without its declared parameter/scenario contract")
    run(
        stage,
        "analysis/scenario-models/aether_regional_reference_model.py",
        "--parameters",
        str(parameters),
        "--scenarios",
        str(scenarios),
        "--output-dir",
        str(stage / "analysis" / "tables"),
    )
    return tuple(path.name for path in (stage / "analysis" / "tables").glob("aether_regional_reference_*"))


def check() -> int:
    if not TABLES.is_dir():
        raise RuntimeError(f"missing generated table directory: {TABLES}")
    with tempfile.TemporaryDirectory(prefix="aether-reproduce-") as temporary:
        stage = Path(temporary) / "aether-revision"
        shutil.copytree(ROOT, stage, ignore=ignored_copy_paths)
        for step in CORE_STEPS:
            run(stage, step.script)
        regional_outputs = run_optional_regional_reference(stage)
        run(stage, "scripts/audit_aether_calculations.py")

        differences: list[str] = []
        expected = [*AUDIT_OUTPUTS, *regional_outputs]
        for step in CORE_STEPS:
            expected.extend(step.outputs)
        for output in expected:
            compare_output(TABLES / output, stage / "analysis" / "tables" / output, differences)
        if differences:
            print("Reproduction check failed:")
            for difference in differences:
                print(f"- {difference}")
            return 1
    print("Reproduction check passed: core outputs regenerated in an isolated temporary tree.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="safely regenerate and compare core outputs")
    args = parser.parse_args(argv)
    if not args.check:
        parser.error("only --check is supported; this tool never overwrites repository outputs")
    return check()


if __name__ == "__main__":
    raise SystemExit(main())
