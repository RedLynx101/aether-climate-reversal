from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TABLE_DIR = ROOT / "analysis" / "tables"
TABLE_DIR.mkdir(parents=True, exist_ok=True)

PRODUCTIVITY_SUMMARY = TABLE_DIR / "aether_robotics_productivity_summary.csv"

IFR_INSTALLS_2024 = 542_076.0
IFR_STOCK_2024 = 4_663_698.0
AMAZON_MOBILE_ROBOT_STOCK = 750_000.0
FIGURE_BOTQ_CAPACITY_Y = 12_000.0
FIGURE_ONE_PER_HOUR_Y = 8_760.0
FIGURE_DELIVERED_STOCK = 350.0
FIGURE_ACTUATORS = 9_000.0
FIGURE_250_MONTH_LEAD_Y = 3_000.0
AGILITY_ROBOFAB_CAPACITY_Y = 10_000.0
UNITREE_G1_PRICE_USD = 13_500.0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def number(value: float, digits: int = 6) -> str:
    return f"{value:.{digits}f}"


def safe_multiple(numerator: float, denominator: float) -> float:
    if denominator <= 0.0:
        return float("nan")
    return numerator / denominator


def ramp_metrics(start_flow: float, target_flow: float, years: float = 20.0) -> tuple[float, float, bool]:
    ratio = safe_multiple(target_flow, start_flow)
    already_sufficient = ratio <= 1.0
    if already_sufficient:
        return 0.0, 0.0, True
    return (ratio ** (1.0 / years) - 1.0) * 100.0, math.log(ratio, 2.0), False


def main() -> None:
    productivity_rows = read_csv(PRODUCTIVITY_SUMMARY)
    scenarios = []
    for row in productivity_rows:
        scenarios.append(
            {
                "scenario": row["scenario"],
                "scenario_name": row["scenario_name"],
                "required_annual_robot_production_robots": float(row["annual_robot_production_requirement_robots"]),
                "robot_stock_required_million": float(row["robot_stock_required_million"]),
            }
        )

    claims = [
        {
            "anchor_key": "ifr_industrial_robot_installations_2024",
            "source_key": "ifr_world_robotics_2025",
            "source_type": "industry statistical report",
            "evidence_class": "independent industry statistic",
            "metric_type": "annual_robot_installations",
            "claimed_value": IFR_INSTALLS_2024,
            "annualized_robot_flow": IFR_INSTALLS_2024,
            "stock_count": "",
            "claim_status": "verified external anchor",
            "paper_use": "Use as a current industrial robot installation comparator, not as humanoid production.",
            "notes": "Industrial robots are mostly factory systems and cannot be assumed to perform AETHER field work.",
        },
        {
            "anchor_key": "ifr_operational_robot_stock_2024",
            "source_key": "ifr_world_robotics_2025",
            "source_type": "industry statistical report",
            "evidence_class": "independent industry statistic",
            "metric_type": "operational_stock",
            "claimed_value": IFR_STOCK_2024,
            "annualized_robot_flow": "",
            "stock_count": IFR_STOCK_2024,
            "claim_status": "verified external anchor",
            "paper_use": "Use as current global industrial robot stock comparator.",
            "notes": "Stock count does not imply general-purpose autonomy.",
        },
        {
            "anchor_key": "amazon_mobile_robot_stock_2024",
            "source_key": "amazon_robotics_750k_robots_2024",
            "source_type": "company operations article",
            "evidence_class": "company claim",
            "metric_type": "deployed_stock",
            "claimed_value": AMAZON_MOBILE_ROBOT_STOCK,
            "annualized_robot_flow": "",
            "stock_count": AMAZON_MOBILE_ROBOT_STOCK,
            "claim_status": "company-reported stock",
            "paper_use": "Use as a designed-facility fleet-management comparator.",
            "notes": "Warehouse robots are a strong automation signal but are not open-field construction robots.",
        },
        {
            "anchor_key": "figure_botq_first_generation_capacity_2025",
            "source_key": "figure_botq_2025",
            "source_type": "company primary source",
            "evidence_class": "company announced capacity",
            "metric_type": "annual_factory_capacity",
            "claimed_value": FIGURE_BOTQ_CAPACITY_Y,
            "annualized_robot_flow": FIGURE_BOTQ_CAPACITY_Y,
            "stock_count": "",
            "claim_status": "company-announced capacity",
            "paper_use": "Use as a frontier humanoid factory-capacity comparator, not independent proof of sustained output.",
            "notes": "BotQ first-generation line was described as capable of up to 12,000 humanoids per year.",
        },
        {
            "anchor_key": "figure_one_per_hour_cadence_2026",
            "source_key": "figure_ramping_2026",
            "source_type": "company primary source",
            "evidence_class": "company demonstrated cadence",
            "metric_type": "annualized_cycle_time",
            "claimed_value": 1.0,
            "annualized_robot_flow": FIGURE_ONE_PER_HOUR_Y,
            "stock_count": "",
            "claim_status": "company-announced cadence",
            "paper_use": "Use as a company-primary ramp signal; label as not independently audited.",
            "notes": "One robot per hour annualizes to 8,760 robots/year if sustained continuously.",
        },
        {
            "anchor_key": "figure_delivered_over_350_robots_2026",
            "source_key": "figure_ramping_2026",
            "source_type": "company primary source",
            "evidence_class": "company delivered-stock claim",
            "metric_type": "delivered_stock",
            "claimed_value": FIGURE_DELIVERED_STOCK,
            "annualized_robot_flow": "",
            "stock_count": FIGURE_DELIVERED_STOCK,
            "claim_status": "company-reported delivered stock",
            "paper_use": "Use as a scale-of-current-fleet caution.",
            "notes": "Hundreds of delivered humanoids are meaningful for learning loops and still far below AETHER fleet needs.",
        },
        {
            "anchor_key": "figure_actuators_produced_2026",
            "source_key": "figure_ramping_2026",
            "source_type": "company primary source",
            "evidence_class": "company component-production claim",
            "metric_type": "component_count",
            "claimed_value": FIGURE_ACTUATORS,
            "annualized_robot_flow": "",
            "stock_count": "",
            "claim_status": "company-reported component count",
            "paper_use": "Use as a manufacturing-process signal, not as complete robot production.",
            "notes": "Component output supports the ramp story but is not equivalent to deployed robots.",
        },
        {
            "anchor_key": "figure_250_robots_month_x_lead_2026",
            "source_key": "figure_x_user_claim_2026_06_250_month",
            "source_type": "user-supplied social-media lead",
            "evidence_class": "unresolved social-media lead",
            "metric_type": "annualized_monthly_lead",
            "claimed_value": 250.0,
            "annualized_robot_flow": FIGURE_250_MONTH_LEAD_Y,
            "stock_count": "",
            "claim_status": "unresolved lead",
            "paper_use": "Do not cite as fact; use only as a verification queue item or sensitivity comparator.",
            "notes": "Annualizes to 3,000 robots/year but remains below official one-hour cadence and needs archival verification.",
        },
        {
            "anchor_key": "agility_robofab_capacity_2023",
            "source_key": "agility_robofab_2023",
            "source_type": "company primary source",
            "evidence_class": "company announced capacity",
            "metric_type": "annual_factory_capacity",
            "claimed_value": AGILITY_ROBOFAB_CAPACITY_Y,
            "annualized_robot_flow": AGILITY_ROBOFAB_CAPACITY_Y,
            "stock_count": "",
            "claim_status": "company-announced capacity",
            "paper_use": "Use as a humanoid factory-capacity comparator, not sustained-output proof.",
            "notes": "Factory capacity above 10,000 robots/year is a useful manufacturing benchmark.",
        },
        {
            "anchor_key": "unitree_g1_price_floor_2026",
            "source_key": "unitree_g1_product_2026",
            "source_type": "company product page",
            "evidence_class": "vendor product claim",
            "metric_type": "unit_price_floor_usd",
            "claimed_value": UNITREE_G1_PRICE_USD,
            "annualized_robot_flow": "",
            "stock_count": "",
            "claim_status": "vendor listed price",
            "paper_use": "Use only as a low-end hardware price floor with duty-cycle caveats.",
            "notes": "A low price does not prove industrial field productivity, uptime, reliability, or safety.",
        },
    ]

    flow_anchors = [
        {
            "anchor_key": "ifr_industrial_robot_installations_2024",
            "label": "IFR 2024 industrial robot installations",
            "annualized_robot_flow": IFR_INSTALLS_2024,
            "evidence_class": "independent industry statistic",
        },
        {
            "anchor_key": "figure_botq_first_generation_capacity_2025",
            "label": "Figure BotQ first-generation line",
            "annualized_robot_flow": FIGURE_BOTQ_CAPACITY_Y,
            "evidence_class": "company announced capacity",
        },
        {
            "anchor_key": "figure_one_per_hour_cadence_2026",
            "label": "Figure one robot/hour cadence",
            "annualized_robot_flow": FIGURE_ONE_PER_HOUR_Y,
            "evidence_class": "company demonstrated cadence",
        },
        {
            "anchor_key": "figure_250_robots_month_x_lead_2026",
            "label": "Figure 250/month X lead",
            "annualized_robot_flow": FIGURE_250_MONTH_LEAD_Y,
            "evidence_class": "unresolved social-media lead",
        },
        {
            "anchor_key": "agility_robofab_capacity_2023",
            "label": "Agility RoboFab capacity",
            "annualized_robot_flow": AGILITY_ROBOFAB_CAPACITY_Y,
            "evidence_class": "company announced capacity",
        },
    ]

    comparison_rows = []
    for scenario in scenarios:
        required = scenario["required_annual_robot_production_robots"]
        for anchor in flow_anchors:
            flow = anchor["annualized_robot_flow"]
            multiple = safe_multiple(required, flow)
            if multiple <= 1.0:
                interpretation = "Current anchor is at or above this AETHER annual flow on a count basis; task suitability remains unproven."
            elif multiple < 10.0:
                interpretation = "Single-anchor flow is within one order of magnitude of this AETHER annual flow, before task suitability and supply-chain limits."
            elif multiple < 100.0:
                interpretation = "AETHER would require many comparable lines or a major ramp from this anchor."
            else:
                interpretation = "AETHER would require a new global robotics manufacturing industry relative to this anchor."
            comparison_rows.append(
                {
                    "scenario": scenario["scenario"],
                    "scenario_name": scenario["scenario_name"],
                    "anchor_key": anchor["anchor_key"],
                    "anchor_label": anchor["label"],
                    "evidence_class": anchor["evidence_class"],
                    "required_annual_robot_production_robots": number(required, 2),
                    "anchor_annualized_robot_flow": number(flow, 2),
                    "multiple_of_anchor_flow": number(multiple, 6),
                    "interpretation": interpretation,
                }
            )

    ramp_start_anchors = [
        ("ifr_industrial_robot_installations_2024", "IFR 2024 annual industrial robot installations", IFR_INSTALLS_2024, "independent industry statistic"),
        ("figure_botq_first_generation_capacity_2025", "Figure BotQ first-generation line", FIGURE_BOTQ_CAPACITY_Y, "company announced capacity"),
        ("figure_one_per_hour_cadence_2026", "Figure one robot/hour cadence", FIGURE_ONE_PER_HOUR_Y, "company demonstrated cadence"),
        ("agility_robofab_capacity_2023", "Agility RoboFab capacity", AGILITY_ROBOFAB_CAPACITY_Y, "company announced capacity"),
    ]

    ramp_rows = []
    for scenario in scenarios:
        target = scenario["required_annual_robot_production_robots"]
        for key, label, start_flow, evidence_class in ramp_start_anchors:
            cagr, doublings, already_sufficient = ramp_metrics(start_flow, target)
            ramp_rows.append(
                {
                    "scenario": scenario["scenario"],
                    "scenario_name": scenario["scenario_name"],
                    "start_anchor_key": key,
                    "start_anchor_label": label,
                    "evidence_class": evidence_class,
                    "start_annual_flow_robots": number(start_flow, 2),
                    "target_annual_flow_robots": number(target, 2),
                    "flow_multiple_needed": number(safe_multiple(target, start_flow), 6),
                    "doublings_needed_over_20y": number(doublings, 6),
                    "required_cagr_pct_over_20y": number(cagr, 6),
                    "already_at_or_above_target_on_count_basis": str(already_sufficient).lower(),
                    "interpretation": "Count basis only; AETHER still needs task productivity, uptime, reliability, service, safety, and field integration evidence.",
                }
            )

    scenario_lookup = {row["scenario"]: row for row in scenarios}
    high = scenario_lookup["high_robot_intensity_translation"]["required_annual_robot_production_robots"]
    push = scenario_lookup["aether_automation_push"]["required_annual_robot_production_robots"]
    deep = scenario_lookup["deep_modular_abundance"]["required_annual_robot_production_robots"]
    company_primary_rows = [row for row in claims if row["evidence_class"].startswith("company") or row["evidence_class"] == "vendor product claim"]
    social_media_rows = [row for row in claims if "social-media" in row["evidence_class"]]

    summary_rows = [
        ("high_required_robots_y", high, "robots/year", "High robot-intensity translation annual robot production plus replacement requirement."),
        ("push_required_robots_y", push, "robots/year", "AETHER automation-push annual robot production plus replacement requirement."),
        ("deep_required_robots_y", deep, "robots/year", "Deep modular abundance annual robot production plus replacement requirement."),
        ("high_multiple_ifr", safe_multiple(high, IFR_INSTALLS_2024), "multiple", "High case relative to IFR 2024 annual industrial robot installations."),
        ("push_multiple_ifr", safe_multiple(push, IFR_INSTALLS_2024), "multiple", "Automation-push case relative to IFR 2024 annual industrial robot installations."),
        ("deep_multiple_ifr", safe_multiple(deep, IFR_INSTALLS_2024), "multiple", "Deep modular case relative to IFR 2024 annual industrial robot installations."),
        ("high_figure_botq_factories", safe_multiple(high, FIGURE_BOTQ_CAPACITY_Y), "BotQ-equivalent lines", "High case as Figure BotQ first-generation line equivalents."),
        ("push_figure_botq_factories", safe_multiple(push, FIGURE_BOTQ_CAPACITY_Y), "BotQ-equivalent lines", "Automation-push case as Figure BotQ first-generation line equivalents."),
        ("deep_figure_botq_factories", safe_multiple(deep, FIGURE_BOTQ_CAPACITY_Y), "BotQ-equivalent lines", "Deep modular case as Figure BotQ first-generation line equivalents."),
        ("high_figure_hourly_lines", safe_multiple(high, FIGURE_ONE_PER_HOUR_Y), "one-hour-cadence lines", "High case as Figure one-robot-per-hour line equivalents."),
        ("push_figure_hourly_lines", safe_multiple(push, FIGURE_ONE_PER_HOUR_Y), "one-hour-cadence lines", "Automation-push case as Figure one-robot-per-hour line equivalents."),
        ("deep_figure_hourly_lines", safe_multiple(deep, FIGURE_ONE_PER_HOUR_Y), "one-hour-cadence lines", "Deep modular case as Figure one-robot-per-hour line equivalents."),
        ("verified_external_or_company_claim_rows", len([row for row in claims if row["claim_status"] != "unresolved lead"]), "rows", "Rows that can be used as external anchors with their evidence class visible."),
        ("company_primary_claim_rows", len(company_primary_rows), "rows", "Company-primary or vendor-product rows, still not independent audits."),
        ("unresolved_social_media_lead_rows", len(social_media_rows), "rows", "Social-media leads that should not be cited as paper facts."),
        ("production_anchor_count", len(flow_anchors), "flow anchors", "Annualized production-flow anchors compared with AETHER annual robot requirements."),
    ]
    summary = [
        {
            "metric": metric,
            "value": number(float(value), 6),
            "unit": unit,
            "interpretation": interpretation,
        }
        for metric, value, unit, interpretation in summary_rows
    ]

    write_csv(
        TABLE_DIR / "aether_robotics_production_claims.csv",
        claims,
        [
            "anchor_key",
            "source_key",
            "source_type",
            "evidence_class",
            "metric_type",
            "claimed_value",
            "annualized_robot_flow",
            "stock_count",
            "claim_status",
            "paper_use",
            "notes",
        ],
    )
    write_csv(
        TABLE_DIR / "aether_robotics_production_scale_comparison.csv",
        comparison_rows,
        [
            "scenario",
            "scenario_name",
            "anchor_key",
            "anchor_label",
            "evidence_class",
            "required_annual_robot_production_robots",
            "anchor_annualized_robot_flow",
            "multiple_of_anchor_flow",
            "interpretation",
        ],
    )
    write_csv(
        TABLE_DIR / "aether_robotics_production_ramp_paths.csv",
        ramp_rows,
        [
            "scenario",
            "scenario_name",
            "start_anchor_key",
            "start_anchor_label",
            "evidence_class",
            "start_annual_flow_robots",
            "target_annual_flow_robots",
            "flow_multiple_needed",
            "doublings_needed_over_20y",
            "required_cagr_pct_over_20y",
            "already_at_or_above_target_on_count_basis",
            "interpretation",
        ],
    )
    write_csv(
        TABLE_DIR / "aether_robotics_production_verification_summary.csv",
        summary,
        ["metric", "value", "unit", "interpretation"],
    )


if __name__ == "__main__":
    main()

