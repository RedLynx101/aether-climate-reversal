"""AETHER technology-acceleration and order-of-magnitude frontier.

This model converts the cost-stack CSV into reduction factors and compares
possible AETHER RD&D program budgets against current R&D baselines. It is not a
forecast. It is an accounting layer for the question: which reductions must
occur, where AI/robotics can plausibly help, and where hard floors remain?
"""

from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TABLE_DIR = ROOT / "analysis" / "tables"


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    components = read_csv(TABLE_DIR / "aether_cost_stack_components.csv")
    totals: dict[str, float] = {}
    display: dict[str, str] = {}
    for row in components:
        scenario = row["scenario"]
        totals[scenario] = totals.get(scenario, 0.0) + float(row["cost_usd_tco2"])
        display[scenario] = row["display_name"]
    current = totals["current_dac_like"]
    frontier = []
    for scenario, cost in totals.items():
        reduction = current / cost
        frontier.append(
            {
                "scenario": scenario,
                "display_name": display[scenario],
                "delivered_cost_usd_tco2": round(cost, 2),
                "annual_cost_trillion_usd_y_at_100gt": round(cost * 100.0 / 1000.0, 3),
                "reduction_factor_vs_current": round(reduction, 2),
                "log10_reduction_orders": round(math.log10(reduction), 3),
            }
        )
    write_csv(TABLE_DIR / "aether_cost_improvement_frontier.csv", frontier)


if __name__ == "__main__":
    main()
