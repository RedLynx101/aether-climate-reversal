from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analysis" / "tables"
OUT.mkdir(parents=True, exist_ok=True)

TARGET_GROSS_GTCO2_Y = 100.0
GROSS_REQUIRED_FOR_100_DURABLE_GTCO2_Y = 117.8125450786615
MWH_PER_GJ = 0.2777777777777778
CO2_SPLITTING_GJ_TCO2 = 8.94


@dataclass(frozen=True)
class CostScenario:
    key: str
    display_name: str
    description: str
    capture_energy_gj_tco2: float
    split_fraction: float
    electricity_price_usd_mwh: float
    contactor_capex_usd_tco2: float
    sorbent_material_usd_tco2: float
    compression_transport_storage_usd_tco2: float
    mrv_insurance_liability_usd_tco2: float
    robot_ops_maintenance_usd_tco2: float
    finance_permitting_overhead_usd_tco2: float
    product_handling_usd_tco2: float
    automation_leverage_fraction: float
    automation_reduction_factor_on_levered_cost: float


SCENARIOS = [
    CostScenario(
        key="current_dac_like",
        display_name="Current DAC-like",
        description="High-energy, high-capex engineered removal benchmark; useful as the implausible status-quo case.",
        capture_energy_gj_tco2=8.0,
        split_fraction=0.0,
        electricity_price_usd_mwh=70.0,
        contactor_capex_usd_tco2=170.0,
        sorbent_material_usd_tco2=80.0,
        compression_transport_storage_usd_tco2=35.0,
        mrv_insurance_liability_usd_tco2=15.0,
        robot_ops_maintenance_usd_tco2=65.0,
        finance_permitting_overhead_usd_tco2=85.0,
        product_handling_usd_tco2=0.0,
        automation_leverage_fraction=0.0,
        automation_reduction_factor_on_levered_cost=1.0,
    ),
    CostScenario(
        key="aether_automation_push",
        display_name="AETHER automation push",
        description="Low-energy portfolio case where AI/robotics compress plant manufacturing, construction, operations, storage logistics, and MRV cost.",
        capture_energy_gj_tco2=2.05,
        split_fraction=0.0,
        electricity_price_usd_mwh=35.0,
        contactor_capex_usd_tco2=24.0,
        sorbent_material_usd_tco2=10.0,
        compression_transport_storage_usd_tco2=14.0,
        mrv_insurance_liability_usd_tco2=5.0,
        robot_ops_maintenance_usd_tco2=4.0,
        finance_permitting_overhead_usd_tco2=9.0,
        product_handling_usd_tco2=0.0,
        automation_leverage_fraction=0.78,
        automation_reduction_factor_on_levered_cost=6.0,
    ),
    CostScenario(
        key="moonshot_modular",
        display_name="Moonshot modular",
        description="Very low energy, cheap clean power, modular factories, automated construction, mature sorbents, and low-friction storage.",
        capture_energy_gj_tco2=1.5,
        split_fraction=0.0,
        electricity_price_usd_mwh=20.0,
        contactor_capex_usd_tco2=10.0,
        sorbent_material_usd_tco2=5.0,
        compression_transport_storage_usd_tco2=8.0,
        mrv_insurance_liability_usd_tco2=3.0,
        robot_ops_maintenance_usd_tco2=2.0,
        finance_permitting_overhead_usd_tco2=4.0,
        product_handling_usd_tco2=0.0,
        automation_leverage_fraction=0.84,
        automation_reduction_factor_on_levered_cost=14.0,
    ),
    CostScenario(
        key="splitting_default_failure",
        display_name="Full splitting default",
        description="Advanced capture plus full CO2 splitting into carbon and oxygen; compact storage but energy-dominated and usually the wrong default.",
        capture_energy_gj_tco2=3.0,
        split_fraction=1.0,
        electricity_price_usd_mwh=35.0,
        contactor_capex_usd_tco2=20.0,
        sorbent_material_usd_tco2=8.0,
        compression_transport_storage_usd_tco2=8.0,
        mrv_insurance_liability_usd_tco2=5.0,
        robot_ops_maintenance_usd_tco2=5.0,
        finance_permitting_overhead_usd_tco2=10.0,
        product_handling_usd_tco2=45.0,
        automation_leverage_fraction=0.55,
        automation_reduction_factor_on_levered_cost=6.0,
    ),
    CostScenario(
        key="deep_abundance_floor",
        display_name="Deep abundance floor",
        description="Extreme abundance case used to show that even aggressive automation leaves an energy/storage/MRV floor.",
        capture_energy_gj_tco2=1.0,
        split_fraction=0.0,
        electricity_price_usd_mwh=15.0,
        contactor_capex_usd_tco2=6.0,
        sorbent_material_usd_tco2=3.0,
        compression_transport_storage_usd_tco2=5.0,
        mrv_insurance_liability_usd_tco2=2.0,
        robot_ops_maintenance_usd_tco2=1.5,
        finance_permitting_overhead_usd_tco2=2.5,
        product_handling_usd_tco2=0.0,
        automation_leverage_fraction=0.88,
        automation_reduction_factor_on_levered_cost=24.0,
    ),
]


@dataclass(frozen=True)
class RobotCase:
    key: str
    display_name: str
    unit_cost_usd: float
    utilization_hours_y: float
    lifetime_y: float
    annual_maintenance_fraction: float
    power_kw: float
    electricity_price_usd_mwh: float
    supervision_overhead_usd_h: float


ROBOT_CASES = [
    RobotCase("early_humanoid", "Early humanoid / field robot", 200_000, 4_000, 5, 0.18, 2.0, 70, 6.0),
    RobotCase("industrial_scale", "Industrial scale robot", 100_000, 5_500, 7, 0.12, 2.0, 50, 3.0),
    RobotCase("aether_factory_robot", "AETHER factory robot", 50_000, 6_500, 8, 0.10, 1.5, 35, 1.5),
    RobotCase("deep_abundance_robot", "Deep abundance robot", 25_000, 7_500, 10, 0.08, 1.0, 20, 0.5),
]


def energy_cost(s: CostScenario) -> float:
    total_energy_gj = s.capture_energy_gj_tco2 + s.split_fraction * CO2_SPLITTING_GJ_TCO2
    return total_energy_gj * MWH_PER_GJ * s.electricity_price_usd_mwh


def components(s: CostScenario) -> list[tuple[str, str, float, bool]]:
    return [
        ("energy", "Energy", energy_cost(s), False),
        ("contactor_capex", "Plant/contactors", s.contactor_capex_usd_tco2, True),
        ("sorbent_materials", "Sorbents/materials", s.sorbent_material_usd_tco2, True),
        ("compression_transport_storage", "Compression/transport/storage", s.compression_transport_storage_usd_tco2, True),
        ("mrv_insurance_liability", "MRV/insurance/liability", s.mrv_insurance_liability_usd_tco2, True),
        ("robot_ops_maintenance", "Robot O&M", s.robot_ops_maintenance_usd_tco2, True),
        ("finance_permitting_overhead", "Finance/permitting/overhead", s.finance_permitting_overhead_usd_tco2, True),
        ("product_handling", "Carbon/O2 product handling", s.product_handling_usd_tco2, True),
    ]


def robot_hour_cost(r: RobotCase) -> dict[str, float | str]:
    capital = r.unit_cost_usd / (r.utilization_hours_y * r.lifetime_y)
    maintenance = r.unit_cost_usd * r.annual_maintenance_fraction / r.utilization_hours_y
    energy = r.power_kw / 1000.0 * r.electricity_price_usd_mwh
    total = capital + maintenance + energy + r.supervision_overhead_usd_h
    return {
        "case": r.key,
        "display_name": r.display_name,
        "unit_cost_usd": r.unit_cost_usd,
        "utilization_hours_y": r.utilization_hours_y,
        "lifetime_y": r.lifetime_y,
        "annual_maintenance_fraction": r.annual_maintenance_fraction,
        "power_kw": r.power_kw,
        "electricity_price_usd_mwh": r.electricity_price_usd_mwh,
        "capital_cost_usd_h": capital,
        "maintenance_cost_usd_h": maintenance,
        "energy_cost_usd_h": energy,
        "supervision_overhead_usd_h": r.supervision_overhead_usd_h,
        "direct_robot_hour_cost_usd_h": total,
    }


def run() -> None:
    component_rows = []
    scenario_rows = []
    current_total = None

    for s in SCENARIOS:
        comp = components(s)
        total = sum(value for _, _, value, _ in comp)
        if s.key == "current_dac_like":
            current_total = total
        automatable = sum(value for _, _, value, is_auto in comp if is_auto)
        non_automatable = total - automatable
        for key, label, value, is_auto in comp:
            component_rows.append({
                "scenario": s.key,
                "display_name": s.display_name,
                "component": key,
                "component_label": label,
                "cost_usd_tco2": value,
                "share_of_total": value / total if total else 0.0,
                "classified_automatable": is_auto,
            })
        scenario_rows.append({
            "scenario": s.key,
            "display_name": s.display_name,
            "description": s.description,
            "capture_energy_gj_tco2": s.capture_energy_gj_tco2,
            "split_fraction": s.split_fraction,
            "total_energy_gj_tco2": s.capture_energy_gj_tco2 + s.split_fraction * CO2_SPLITTING_GJ_TCO2,
            "electricity_price_usd_mwh": s.electricity_price_usd_mwh,
            "energy_cost_usd_tco2": energy_cost(s),
            "total_cost_usd_tco2": total,
            "annual_cost_at_100gt_trillion_usd_y": total * TARGET_GROSS_GTCO2_Y / 1000.0,
            "annual_cost_at_100gt_durable_same_mix_trillion_usd_y": total * GROSS_REQUIRED_FOR_100_DURABLE_GTCO2_Y / 1000.0,
            "automatable_cost_usd_tco2": automatable,
            "non_automatable_floor_usd_tco2": non_automatable,
            "automation_leverage_fraction": s.automation_leverage_fraction,
            "automation_reduction_factor_on_levered_cost": s.automation_reduction_factor_on_levered_cost,
            "cost_reduction_factor_vs_current": (current_total / total) if current_total else 1.0,
            "interpretation": s.description,
        })

    with (OUT / "aether_cost_stack_components.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(component_rows[0].keys()))
        writer.writeheader()
        writer.writerows(component_rows)

    with (OUT / "aether_cost_stack_scenarios.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(scenario_rows[0].keys()))
        writer.writeheader()
        writer.writerows(scenario_rows)

    robot_rows = [robot_hour_cost(r) for r in ROBOT_CASES]
    with (OUT / "aether_robot_labor_costs.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(robot_rows[0].keys()))
        writer.writeheader()
        writer.writerows(robot_rows)

    baseline = scenario_rows[0]
    reduction_rows = []
    for row in scenario_rows[1:]:
        reduction_rows.append({
            "scenario": row["scenario"],
            "display_name": row["display_name"],
            "total_cost_reduction_factor_vs_current": baseline["total_cost_usd_tco2"] / row["total_cost_usd_tco2"],
            "annual_cost_reduction_trillion_usd_y_at_100gt": baseline["annual_cost_at_100gt_trillion_usd_y"] - row["annual_cost_at_100gt_trillion_usd_y"],
            "energy_cost_reduction_factor_vs_current": baseline["energy_cost_usd_tco2"] / row["energy_cost_usd_tco2"],
            "non_energy_cost_reduction_factor_vs_current": (baseline["total_cost_usd_tco2"] - baseline["energy_cost_usd_tco2"]) / (row["total_cost_usd_tco2"] - row["energy_cost_usd_tco2"]),
            "remaining_floor_usd_tco2": row["non_automatable_floor_usd_tco2"] + row["energy_cost_usd_tco2"],
            "interpretation": "Shows how much cost compression is required after separating energy from automatable and semi-automatable cost buckets.",
        })
    with (OUT / "aether_cost_reduction_requirements.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(reduction_rows[0].keys()))
        writer.writeheader()
        writer.writerows(reduction_rows)

    print(f"Wrote {OUT / 'aether_cost_stack_components.csv'}")
    print(f"Wrote {OUT / 'aether_cost_stack_scenarios.csv'}")
    print(f"Wrote {OUT / 'aether_robot_labor_costs.csv'}")
    print(f"Wrote {OUT / 'aether_cost_reduction_requirements.csv'}")


if __name__ == "__main__":
    run()
