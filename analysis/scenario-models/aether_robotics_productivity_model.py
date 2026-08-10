from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TABLE_DIR = ROOT / "analysis" / "tables"

TARGET_GTCO2_Y = 100.0
TARGET_CAPACITY_MTCO2_Y = TARGET_GTCO2_Y * 1000.0
ANNUAL_NEW_CAPACITY_MTCO2_Y = TARGET_CAPACITY_MTCO2_Y / 20.0
POWER_PRICE_USD_MWH = 30.0
HUMAN_SUPERVISOR_COST_USD_H = 80.0
IFR_2024_INDUSTRIAL_ROBOT_INSTALLS = 542_076.0
FIGURE_ONE_PER_HOUR_ANNUALIZED = 8760.0


@dataclass(frozen=True)
class Scenario:
    key: str
    name: str
    operating_hours_per_mt_capacity_y: float
    build_hours_per_mt_new_capacity: float
    interpretation: str


@dataclass(frozen=True)
class RobotClassAssumption:
    scenario: str
    robot_class: str
    display_name: str
    unit_cost_usd: float
    useful_hours_per_year: float
    lifetime_years: float
    annual_maintenance_fraction_of_capex: float
    energy_kwh_per_useful_hour: float
    supervisor_ratio_robots_per_human: float
    integration_overhead_fraction: float
    evidence_grade: str
    source_basis: str


SCENARIOS = [
    Scenario(
        key="high_robot_intensity_translation",
        name="High robot-intensity translation",
        operating_hours_per_mt_capacity_y=180_000.0,
        build_hours_per_mt_new_capacity=35_000.0,
        interpretation="Stress case that roughly preserves the old 50 robots/MtCO2/y proxy once useful hours and replacements are counted.",
    ),
    Scenario(
        key="aether_automation_push",
        name="AETHER automation push",
        operating_hours_per_mt_capacity_y=55_000.0,
        build_hours_per_mt_new_capacity=18_000.0,
        interpretation="Designed facilities, modular plant manufacturing, high autonomy, and specialized robots lower required task-hours per tonne of capacity.",
    ),
    Scenario(
        key="deep_modular_abundance",
        name="Deep modular abundance",
        operating_hours_per_mt_capacity_y=18_000.0,
        build_hours_per_mt_new_capacity=8_000.0,
        interpretation="Upper-tail case where the plant system is redesigned around robotic factories, self-checking modules, and low-supervision field autonomy.",
    ),
]


CLASS_BY_SCENARIO = [
    # High robot-intensity translation.
    RobotClassAssumption("high_robot_intensity_translation", "industrial_factory_robot", "Industrial factory robots", 100_000, 4500, 10, 0.10, 2.0, 40, 0.25, "B/C", "IFR industrial-robot scale plus scenario cost assumptions"),
    RobotClassAssumption("high_robot_intensity_translation", "mobile_logistics_robot", "Mobile logistics robots", 45_000, 4000, 6, 0.12, 1.0, 75, 0.20, "B/C", "Amazon-style designed-environment fleet plus scenario cost assumptions"),
    RobotClassAssumption("high_robot_intensity_translation", "humanoid_generalist", "Humanoid and generalist field robots", 120_000, 2500, 5, 0.18, 0.8, 8, 0.35, "C", "Unitree/Figure/Agility price and factory leads, not audited productivity"),
    RobotClassAssumption("high_robot_intensity_translation", "autonomous_construction_equipment", "Autonomous construction equipment", 450_000, 2500, 8, 0.15, 25.0, 5, 0.30, "C", "Scenario assumption; needs construction-robot productivity sources"),
    RobotClassAssumption("high_robot_intensity_translation", "drilling_subsurface_robotics", "Drilling and subsurface robotics", 800_000, 2200, 8, 0.18, 30.0, 4, 0.35, "D", "Scenario assumption; needs drilling automation and well-cost sources"),
    RobotClassAssumption("high_robot_intensity_translation", "mrv_drones_sensor_nodes", "MRV drones and sensor networks", 12_000, 2500, 4, 0.25, 0.2, 100, 0.25, "C", "Scenario assumption tied to MRV automation, not method-specific yet"),
    RobotClassAssumption("high_robot_intensity_translation", "robotic_lab_workcell", "Robotic lab workcells", 300_000, 5000, 7, 0.12, 5.0, 10, 0.30, "C", "Autonomous-lab analogy; needs CDR-specific R&D throughput data"),
    # AETHER automation push.
    RobotClassAssumption("aether_automation_push", "industrial_factory_robot", "Industrial factory robots", 60_000, 6000, 10, 0.08, 1.8, 100, 0.15, "B/C", "Scenario assumes mass-manufactured industrial automation"),
    RobotClassAssumption("aether_automation_push", "mobile_logistics_robot", "Mobile logistics robots", 20_000, 5500, 7, 0.08, 0.8, 200, 0.12, "B/C", "Scenario assumes designed AETHER logistics environments"),
    RobotClassAssumption("aether_automation_push", "humanoid_generalist", "Humanoid and generalist field robots", 35_000, 4500, 6, 0.12, 0.7, 50, 0.20, "C", "Scenario assumes useful supervised autonomy improves substantially"),
    RobotClassAssumption("aether_automation_push", "autonomous_construction_equipment", "Autonomous construction equipment", 250_000, 4000, 10, 0.10, 20.0, 25, 0.20, "C", "Scenario assumes modular construction with robotic equipment"),
    RobotClassAssumption("aether_automation_push", "drilling_subsurface_robotics", "Drilling and subsurface robotics", 450_000, 3500, 10, 0.12, 25.0, 20, 0.22, "D", "Scenario assumes improved storage-field automation"),
    RobotClassAssumption("aether_automation_push", "mrv_drones_sensor_nodes", "MRV drones and sensor networks", 4_000, 5000, 5, 0.15, 0.15, 500, 0.12, "C", "Scenario assumes dense autonomous monitoring networks"),
    RobotClassAssumption("aether_automation_push", "robotic_lab_workcell", "Robotic lab workcells", 140_000, 7000, 8, 0.08, 4.0, 40, 0.18, "C", "Scenario assumes AETHER-directed autonomous labs"),
    # Deep modular abundance.
    RobotClassAssumption("deep_modular_abundance", "industrial_factory_robot", "Industrial factory robots", 35_000, 7000, 12, 0.06, 1.5, 250, 0.08, "C", "Upper-tail mass-manufacturing scenario"),
    RobotClassAssumption("deep_modular_abundance", "mobile_logistics_robot", "Mobile logistics robots", 10_000, 6500, 8, 0.05, 0.6, 500, 0.06, "C", "Upper-tail designed logistics and low-cost robot supply"),
    RobotClassAssumption("deep_modular_abundance", "humanoid_generalist", "Humanoid and generalist field robots", 15_000, 5500, 7, 0.08, 0.6, 200, 0.10, "D", "Upper-tail humanoid/generalist productivity assumption"),
    RobotClassAssumption("deep_modular_abundance", "autonomous_construction_equipment", "Autonomous construction equipment", 140_000, 5200, 12, 0.07, 15.0, 100, 0.12, "D", "Upper-tail autonomous construction assumption"),
    RobotClassAssumption("deep_modular_abundance", "drilling_subsurface_robotics", "Drilling and subsurface robotics", 250_000, 4800, 12, 0.08, 18.0, 80, 0.12, "D", "Upper-tail subsurface automation assumption"),
    RobotClassAssumption("deep_modular_abundance", "mrv_drones_sensor_nodes", "MRV drones and sensor networks", 1_500, 7500, 6, 0.08, 0.10, 1500, 0.06, "C/D", "Upper-tail sensor-network cost and autonomy assumption"),
    RobotClassAssumption("deep_modular_abundance", "robotic_lab_workcell", "Robotic lab workcells", 70_000, 8000, 10, 0.06, 3.0, 120, 0.10, "C/D", "Upper-tail autonomous-lab cost and throughput assumption"),
]


TASKS = [
    # Operating-capacity tasks. Shares sum to 1.0.
    {"task_family": "plant_operations_maintenance", "display_name": "Plant O&M and maintenance", "basis": "operating_capacity", "share": 0.35, "robot_class": "humanoid_generalist", "evidence_grade": "C", "caveat": "Needs plant-level work breakdown and reliability data."},
    {"task_family": "materials_handling_logistics", "display_name": "Materials handling and logistics", "basis": "operating_capacity", "share": 0.15, "robot_class": "mobile_logistics_robot", "evidence_grade": "B/C", "caveat": "Best when AETHER moves work into designed environments."},
    {"task_family": "storage_field_operations", "display_name": "Storage field operations", "basis": "operating_capacity", "share": 0.20, "robot_class": "drilling_subsurface_robotics", "evidence_grade": "D", "caveat": "Subsurface automation is still a major evidence gap."},
    {"task_family": "mrv_sensor_auditing", "display_name": "MRV sensing and auditing", "basis": "operating_capacity", "share": 0.15, "robot_class": "mrv_drones_sensor_nodes", "evidence_grade": "C", "caveat": "Must be linked to adversarial MRV and method-specific sampling."},
    {"task_family": "factory_spares_replacement", "display_name": "Factory spares and replacements", "basis": "operating_capacity", "share": 0.10, "robot_class": "industrial_factory_robot", "evidence_grade": "B/C", "caveat": "Depends on modular plant designs and supply-chain redundancy."},
    {"task_family": "robotic_labs_process_improvement", "display_name": "Robotic labs and process improvement", "basis": "operating_capacity", "share": 0.05, "robot_class": "robotic_lab_workcell", "evidence_grade": "C", "caveat": "Represents ongoing R&D throughput, not direct tonne handling."},
    # New-capacity buildout tasks. Shares sum to 1.0.
    {"task_family": "module_manufacturing", "display_name": "Module manufacturing", "basis": "new_capacity", "share": 0.30, "robot_class": "industrial_factory_robot", "evidence_grade": "B/C", "caveat": "Needs plant-specific module bill of process."},
    {"task_family": "construction_commissioning", "display_name": "Construction and commissioning", "basis": "new_capacity", "share": 0.35, "robot_class": "autonomous_construction_equipment", "evidence_grade": "C", "caveat": "Needs construction productivity distributions."},
    {"task_family": "storage_wells_corridors", "display_name": "Storage wells and corridors", "basis": "new_capacity", "share": 0.20, "robot_class": "drilling_subsurface_robotics", "evidence_grade": "D", "caveat": "Needs rig count, well cost, permitting, and pressure-management data."},
    {"task_family": "logistics_ramp", "display_name": "Buildout logistics ramp", "basis": "new_capacity", "share": 0.10, "robot_class": "mobile_logistics_robot", "evidence_grade": "B/C", "caveat": "Depends on warehouse-like staging and standardized modules."},
    {"task_family": "mrv_initialization", "display_name": "MRV initialization", "basis": "new_capacity", "share": 0.05, "robot_class": "mrv_drones_sensor_nodes", "evidence_grade": "C", "caveat": "Needs method-specific baseline and monitoring design."},
]


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"No rows to write for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {path}")


def f(value: float, digits: int = 6) -> str:
    return f"{value:.{digits}f}"


def annual_cost_per_useful_hour(assumption: RobotClassAssumption) -> float:
    annualized_capex = assumption.unit_cost_usd / assumption.lifetime_years
    annual_maintenance = assumption.unit_cost_usd * assumption.annual_maintenance_fraction_of_capex
    capex_maintenance_per_hour = (annualized_capex + annual_maintenance) / assumption.useful_hours_per_year
    energy_per_hour = assumption.energy_kwh_per_useful_hour * (POWER_PRICE_USD_MWH / 1000.0)
    supervision_per_hour = HUMAN_SUPERVISOR_COST_USD_H / assumption.supervisor_ratio_robots_per_human
    direct = capex_maintenance_per_hour + energy_per_hour + supervision_per_hour
    return direct * (1.0 + assumption.integration_overhead_fraction)


def main() -> None:
    assumptions_by_key = {
        (row.scenario, row.robot_class): row
        for row in CLASS_BY_SCENARIO
    }

    class_rows: list[dict[str, object]] = []
    for row in CLASS_BY_SCENARIO:
        cost_per_hour = annual_cost_per_useful_hour(row)
        class_rows.append({
            "scenario": row.scenario,
            "robot_class": row.robot_class,
            "display_name": row.display_name,
            "unit_cost_usd": f(row.unit_cost_usd, 2),
            "useful_hours_per_year": f(row.useful_hours_per_year, 2),
            "lifetime_years": f(row.lifetime_years, 2),
            "annual_maintenance_fraction_of_capex": f(row.annual_maintenance_fraction_of_capex, 4),
            "energy_kwh_per_useful_hour": f(row.energy_kwh_per_useful_hour, 4),
            "supervisor_ratio_robots_per_human": f(row.supervisor_ratio_robots_per_human, 2),
            "integration_overhead_fraction": f(row.integration_overhead_fraction, 4),
            "delivered_cost_usd_per_useful_hour": f(cost_per_hour, 4),
            "evidence_grade": row.evidence_grade,
            "source_basis": row.source_basis,
        })

    task_rows: list[dict[str, object]] = []
    productivity_rows: list[dict[str, object]] = []
    for scenario in SCENARIOS:
        for task in TASKS:
            if task["basis"] == "operating_capacity":
                annual_basis_mt = TARGET_CAPACITY_MTCO2_Y
                hours_per_mt = scenario.operating_hours_per_mt_capacity_y * task["share"]
                basis_name = "per MtCO2/year operating capacity"
            else:
                annual_basis_mt = ANNUAL_NEW_CAPACITY_MTCO2_Y
                hours_per_mt = scenario.build_hours_per_mt_new_capacity * task["share"]
                basis_name = "per MtCO2/year new capacity added"
            annual_hours = hours_per_mt * annual_basis_mt
            assumption = assumptions_by_key[(scenario.key, task["robot_class"])]
            cost_per_hour = annual_cost_per_useful_hour(assumption)
            robot_stock = annual_hours / assumption.useful_hours_per_year
            annual_replacement_flow = robot_stock / assumption.lifetime_years
            task_rows.append({
                "scenario": scenario.key,
                "scenario_name": scenario.name,
                "task_family": task["task_family"],
                "display_name": task["display_name"],
                "basis": task["basis"],
                "basis_name": basis_name,
                "hours_per_mt_basis": f(hours_per_mt, 4),
                "annual_basis_mtco2_y": f(annual_basis_mt, 4),
                "annual_useful_task_hours": f(annual_hours, 4),
                "annual_useful_task_hours_billion": f(annual_hours / 1e9, 6),
                "assigned_robot_class": task["robot_class"],
                "task_evidence_grade": task["evidence_grade"],
                "task_caveat": task["caveat"],
            })
            productivity_rows.append({
                "scenario": scenario.key,
                "scenario_name": scenario.name,
                "task_family": task["task_family"],
                "display_name": task["display_name"],
                "assigned_robot_class": task["robot_class"],
                "annual_useful_task_hours_billion": f(annual_hours / 1e9, 6),
                "useful_hours_per_robot_year": f(assumption.useful_hours_per_year, 4),
                "robot_stock_required": f(robot_stock, 4),
                "robot_stock_required_million": f(robot_stock / 1e6, 6),
                "annual_replacement_flow": f(annual_replacement_flow, 4),
                "delivered_cost_usd_per_useful_hour": f(cost_per_hour, 4),
                "annual_robot_operating_cost_billion_usd": f((annual_hours * cost_per_hour) / 1e9, 6),
                "robot_stock_capex_billion_usd": f((robot_stock * assumption.unit_cost_usd) / 1e9, 6),
                "evidence_grade": task["evidence_grade"],
            })

    summary_rows: list[dict[str, object]] = []
    for scenario in SCENARIOS:
        rows = [row for row in productivity_rows if row["scenario"] == scenario.key]
        total_hours = sum(float(row["annual_useful_task_hours_billion"]) for row in rows)
        total_stock = sum(float(row["robot_stock_required_million"]) for row in rows)
        total_replacement = sum(float(row["annual_replacement_flow"]) for row in rows)
        total_cost = sum(float(row["annual_robot_operating_cost_billion_usd"]) for row in rows)
        stock_capex = sum(float(row["robot_stock_capex_billion_usd"]) for row in rows)
        buildout_flow = (total_stock * 1e6) / 20.0
        annual_production = total_replacement + buildout_flow
        summary_rows.append({
            "scenario": scenario.key,
            "scenario_name": scenario.name,
            "total_annual_useful_task_hours_billion": f(total_hours, 6),
            "robot_stock_required_million": f(total_stock, 6),
            "annual_replacement_flow_robots": f(total_replacement, 2),
            "annual_buildout_flow_robots_over_20y": f(buildout_flow, 2),
            "annual_robot_production_requirement_robots": f(annual_production, 2),
            "multiple_of_ifr_2024_industrial_robot_installations": f(annual_production / IFR_2024_INDUSTRIAL_ROBOT_INSTALLS, 6),
            "multiple_of_figure_one_per_hour_annualized": f(annual_production / FIGURE_ONE_PER_HOUR_ANNUALIZED, 6),
            "annual_robot_operating_cost_billion_usd": f(total_cost, 6),
            "robot_stock_capex_billion_usd": f(stock_capex, 6),
            "average_delivered_cost_usd_per_useful_hour": f((total_cost * 1e9) / (total_hours * 1e9), 6),
            "interpretation": scenario.interpretation,
        })

    write_rows(TABLE_DIR / "aether_robotics_productivity_class_costs.csv", class_rows)
    write_rows(TABLE_DIR / "aether_robotics_task_demand.csv", task_rows)
    write_rows(TABLE_DIR / "aether_robotics_productivity_by_task.csv", productivity_rows)
    write_rows(TABLE_DIR / "aether_robotics_productivity_summary.csv", summary_rows)


if __name__ == "__main__":
    main()

