from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TABLE_DIR = ROOT / "analysis" / "tables"

POWER_SUMMARY = TABLE_DIR / "aether_clean_power_portfolio_summary.csv"
CASES_OUT = TABLE_DIR / "aether_clean_energy_additionality_cases.csv"
COMPARATORS_OUT = TABLE_DIR / "aether_clean_energy_market_pull_comparators.csv"
POLICY_OUT = TABLE_DIR / "aether_clean_energy_policy_friction_matrix.csv"
SUMMARY_OUT = TABLE_DIR / "aether_clean_energy_additionality_summary.csv"

BASELINE_ANNUAL_CLEAN_ADDITION_TWH = 850.0
SOLAR_GENERATION_INCREMENT_2025_TWH = 600.0
DATA_CENTER_2030_TWH = 950.0
CURRENT_NUCLEAR_GENERATION_TWH = 2617.5
CURRENT_NUCLEAR_CAPACITY_GW = 377.0
GEOTHERMAL_2050_COST_EFFECTIVE_TWH = 6000.0
MICROSOFT_CRANE_GW = 0.835
GOOGLE_KAIROS_GW = 0.500
HELION_MICROSOFT_GW = 0.050
FIRM_CAPACITY_FACTOR = 0.93
FUSION_CAPACITY_FACTOR = 0.90
YEARS = 20


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"No rows to write for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {path}")


def f(value: float, digits: int = 6) -> str:
    return f"{value:.{digits}f}"


def cumulative_added_generation_twh(start_twh_y: float, growth: float, years: int = YEARS) -> float:
    if abs(growth) < 1e-12:
        return start_twh_y * years
    return start_twh_y * (((1.0 + growth) ** years - 1.0) / growth)


def annual_firm_generation_twh(gw: float, capacity_factor: float) -> float:
    return gw * 8.76 * capacity_factor


def get_target(rows: list[dict[str, str]], scenario: str) -> float:
    for row in rows:
        if row["scenario"] == scenario:
            return float(row["gross_generation_with_penalty_twh_y"])
    raise KeyError(scenario)


def main() -> None:
    power_summary = read_csv(POWER_SUMMARY)
    target_3gj = get_target(power_summary, "advanced_3gj_balanced_firm")
    target_lifecycle = get_target(power_summary, "portfolio_lifecycle_balanced_firm")

    scenario_defs = [
        {
            "scenario": "status_quo_friction",
            "display_name": "Status quo friction",
            "growth": 0.08,
            "delivery": 0.55,
            "aether_allocation": 0.20,
            "additionality": 0.70,
            "policy_frame": "Cheap clean energy grows, but queues, transmission, ordinary electrification, and weak additionality dominate.",
            "source_keys": "iea_global_energy_review_2026;irena_power_costs_2024;berkeley_lab_queued_up_2025;iea_energy_ai_2025",
            "evidence_class": "scenario_assumption_with_source_anchors",
        },
        {
            "scenario": "market_unlocked_texas_style",
            "display_name": "Market-unlocked buildout",
            "growth": 0.15,
            "delivery": 0.75,
            "aether_allocation": 0.35,
            "additionality": 0.85,
            "policy_frame": "Market-led clean energy expands quickly when transmission, siting, and interconnection are unlocked.",
            "source_keys": "irena_power_costs_2024;eia_texas_energy_profile_2024;california_energy_commission_2024_tseg;berkeley_lab_queued_up_2025",
            "evidence_class": "scenario_assumption_with_source_anchors",
        },
        {
            "scenario": "aether_dedicated_buildout",
            "display_name": "Dedicated AETHER buildout",
            "growth": 0.20,
            "delivery": 0.80,
            "aether_allocation": 0.60,
            "additionality": 0.90,
            "policy_frame": "AETHER receives dedicated new clean-power construction but still competes with other loads.",
            "source_keys": "iea_global_energy_review_2026;irena_power_costs_2024;nrel_atb_2024_electricity;iea_electricity_2026",
            "evidence_class": "aggressive_scenario_assumption",
        },
        {
            "scenario": "abundance_clean_power_push",
            "display_name": "Abundance clean-power push",
            "growth": 0.22,
            "delivery": 0.85,
            "aether_allocation": 0.75,
            "additionality": 0.95,
            "policy_frame": "AI, robotics, finance, permitting reform, and manufacturing scale raise clean-energy additions enough for AETHER to become energy-plausible.",
            "source_keys": "iea_state_energy_innovation_2026;irena_power_costs_2024;nrel_atb_2024_electricity;iea_electricity_2026",
            "evidence_class": "upper_tail_scenario_assumption",
        },
        {
            "scenario": "dirty_or_nonadditional_grid",
            "display_name": "Nonadditional grid pull",
            "growth": 0.15,
            "delivery": 0.75,
            "aether_allocation": 0.35,
            "additionality": 0.30,
            "policy_frame": "Same nominal buildout as market-unlocked case, but most power is displaced from other decarbonization uses or drawn from dirty marginal supply.",
            "source_keys": "berkeley_lab_queued_up_2025;iea_energy_ai_2025",
            "evidence_class": "failure_boundary",
        },
    ]

    case_rows: list[dict[str, object]] = []
    for case in scenario_defs:
        added_generation = cumulative_added_generation_twh(BASELINE_ANNUAL_CLEAN_ADDITION_TWH, case["growth"])
        delivered_after_grid = added_generation * case["delivery"]
        nominal_aether_generation = delivered_after_grid * case["aether_allocation"]
        truly_additional_aether_generation = nominal_aether_generation * case["additionality"]
        target_share = truly_additional_aether_generation / target_3gj
        lifecycle_target_share = truly_additional_aether_generation / target_lifecycle
        residual_gap = max(target_3gj - truly_additional_aether_generation, 0.0)
        case_rows.append(
            {
                "scenario": case["scenario"],
                "display_name": case["display_name"],
                "baseline_annual_clean_addition_twh_y": f(BASELINE_ANNUAL_CLEAN_ADDITION_TWH, 3),
                "annual_clean_addition_growth_rate": f(case["growth"], 4),
                "total_added_clean_generation_2046_twh_y": f(added_generation, 3),
                "delivery_factor_after_interconnection_transmission_siting": f(case["delivery"], 4),
                "aether_allocation_fraction_after_competing_loads": f(case["aether_allocation"], 4),
                "additionality_fraction": f(case["additionality"], 4),
                "nominal_aether_clean_generation_twh_y": f(nominal_aether_generation, 3),
                "truly_additional_aether_clean_generation_twh_y": f(truly_additional_aether_generation, 3),
                "target_3gj_balanced_gross_generation_twh_y": f(target_3gj, 3),
                "share_of_3gj_balanced_target": f(target_share, 6),
                "share_of_current_portfolio_lifecycle_target": f(lifecycle_target_share, 6),
                "residual_3gj_balanced_gap_twh_y": f(residual_gap, 3),
                "residual_3gj_balanced_gap_average_tw": f(residual_gap / 8760.0, 6),
                "passes_3gj_balanced_power_gate": "true" if target_share >= 1.0 else "false",
                "policy_frame": case["policy_frame"],
                "source_keys": case["source_keys"],
                "evidence_class": case["evidence_class"],
            }
        )

    comparators = [
        {
            "comparator": "2025_global_electricity_increment",
            "display_name": "2025 global electricity growth",
            "annual_generation_twh_y": BASELINE_ANNUAL_CLEAN_ADDITION_TWH,
            "relationship_to_aether": "Current annual growth anchor; not all clean, not all additional, and not assignable to AETHER.",
            "source_keys": "iea_global_energy_review_2026",
            "evidence_class": "verified_source_anchor",
        },
        {
            "comparator": "2025_solar_generation_increment",
            "display_name": "2025 solar generation growth",
            "annual_generation_twh_y": SOLAR_GENERATION_INCREMENT_2025_TWH,
            "relationship_to_aether": "Solar is scaling fast, but variable generation still needs land, transmission, storage, and firming.",
            "source_keys": "iea_global_energy_review_2026",
            "evidence_class": "verified_source_anchor",
        },
        {
            "comparator": "iea_data_center_2030",
            "display_name": "IEA 2030 data-centre demand",
            "annual_generation_twh_y": DATA_CENTER_2030_TWH,
            "relationship_to_aether": "Competing demand and market-pull signal for clean firm power.",
            "source_keys": "iea_energy_ai_2025",
            "evidence_class": "verified_source_anchor",
        },
        {
            "comparator": "current_global_nuclear_generation",
            "display_name": "Current global nuclear generation",
            "annual_generation_twh_y": CURRENT_NUCLEAR_GENERATION_TWH,
            "relationship_to_aether": "Firm clean comparator; current global nuclear generation is still small relative to AETHER power demand.",
            "source_keys": "iaea_nuclear_status_2025",
            "evidence_class": "verified_source_anchor",
        },
        {
            "comparator": "iea_geothermal_2050_case",
            "display_name": "IEA cost-effective geothermal 2050 case",
            "annual_generation_twh_y": GEOTHERMAL_2050_COST_EFFECTIVE_TWH,
            "relationship_to_aether": "Firm clean upside from drilling/geothermal learning; still a minority of the 3 GJ/tCO2 AETHER case.",
            "source_keys": "iea_geothermal_future_2024",
            "evidence_class": "verified_source_anchor",
        },
        {
            "comparator": "microsoft_constellation_crane",
            "display_name": "Microsoft/Constellation Crane PPA",
            "annual_generation_twh_y": annual_firm_generation_twh(MICROSOFT_CRANE_GW, FIRM_CAPACITY_FACTOR),
            "relationship_to_aether": "Firm-power market-pull signal measured in single-digit TWh/year.",
            "source_keys": "microsoft_constellation_crane_2024",
            "evidence_class": "company_primary_source_signal",
        },
        {
            "comparator": "google_kairos_agreement",
            "display_name": "Google/Kairos advanced nuclear agreement",
            "annual_generation_twh_y": annual_firm_generation_twh(GOOGLE_KAIROS_GW, FIRM_CAPACITY_FACTOR),
            "relationship_to_aether": "Advanced nuclear market-pull signal measured in a few TWh/year.",
            "source_keys": "google_kairos_2024",
            "evidence_class": "company_primary_source_signal",
        },
        {
            "comparator": "helion_microsoft_fusion_ppa",
            "display_name": "Helion/Microsoft fusion PPA",
            "annual_generation_twh_y": annual_firm_generation_twh(HELION_MICROSOFT_GW, FUSION_CAPACITY_FACTOR),
            "relationship_to_aether": "Fusion upside signal; high technical risk and not a base-case AETHER power source.",
            "source_keys": "helion_microsoft_fusion_2023;fusion_industry_association_2025",
            "evidence_class": "company_primary_source_high_risk_signal",
        },
    ]

    comparator_rows: list[dict[str, object]] = []
    for item in comparators:
        generation = float(item["annual_generation_twh_y"])
        comparator_rows.append(
            {
                "comparator": item["comparator"],
                "display_name": item["display_name"],
                "annual_generation_twh_y": f(generation, 3),
                "share_of_3gj_balanced_target": f(generation / target_3gj, 6),
                "relationship_to_aether": item["relationship_to_aether"],
                "source_keys": item["source_keys"],
                "evidence_class": item["evidence_class"],
            }
        )

    policy_rows = [
        {
            "policy_case": "market_led_clean_power",
            "main_anchor": "Texas wind and solar scale; IRENA low-cost renewables",
            "upside_for_aether": "Lets cheap clean energy expand without treating every MW as a bespoke mandate.",
            "failure_mode": "Can still fail through interconnection, transmission, local opposition, and weak additionality.",
            "paper_use_rule": "Use as evidence that markets can scale clean energy when resource quality and grid access line up, not as proof that AETHER gets the energy.",
            "source_keys": "irena_power_costs_2024;eia_texas_energy_profile_2024;berkeley_lab_queued_up_2025",
        },
        {
            "policy_case": "policy_heavy_clean_standard",
            "main_anchor": "California 62% clean total-system generation",
            "upside_for_aether": "Can push high clean shares and demand durable public standards.",
            "failure_mode": "Can add administrative, permitting, cost, and siting friction if process becomes the product.",
            "paper_use_rule": "Use as a comparison case, not as a claim that bureaucracy is always bad or always necessary.",
            "source_keys": "california_energy_commission_2024_tseg",
        },
        {
            "policy_case": "interconnection_queue_constraint",
            "main_anchor": "Berkeley Lab Queued Up 2025",
            "upside_for_aether": "Shows a clear target for reform: queued clean projects are not the same as delivered clean power.",
            "failure_mode": "AETHER claims power on paper while projects wait years for interconnection and transmission.",
            "paper_use_rule": "Treat delivered, additional clean generation as the accounting unit.",
            "source_keys": "berkeley_lab_queued_up_2025",
        },
        {
            "policy_case": "data_center_firm_power_pull",
            "main_anchor": "Microsoft/Constellation, Google/Kairos, IEA Energy and AI",
            "upside_for_aether": "Data centers can finance early clean firm power, licensing pathways, and modular supply chains.",
            "failure_mode": "Data centers also compete for the same clean electricity and grid capacity.",
            "paper_use_rule": "Use as market-pull evidence, not as base-case AETHER supply.",
            "source_keys": "microsoft_constellation_crane_2024;google_kairos_2024;iea_energy_ai_2025",
        },
        {
            "policy_case": "fusion_optionality",
            "main_anchor": "Helion/Microsoft PPA; FIA investment report",
            "upside_for_aether": "Fusion could change the firm-power frontier if it arrives and scales.",
            "failure_mode": "High technical and scale risk; using it as a base assumption would hide the real power problem.",
            "paper_use_rule": "Treat as upside optionality only.",
            "source_keys": "helion_microsoft_fusion_2023;fusion_industry_association_2025",
        },
    ]

    summary_rows = [
        {
            "summary_id": "target_3gj_balanced_gross_generation_twh_y",
            "value": f(target_3gj, 3),
            "unit": "TWh/year",
            "interpretation": "Gross clean generation required for the 3 GJ/tCO2 balanced AETHER power case.",
        },
        {
            "summary_id": "best_case_additional_generation_twh_y",
            "value": f(max(float(row["truly_additional_aether_clean_generation_twh_y"]) for row in case_rows), 3),
            "unit": "TWh/year",
            "interpretation": "Best additional AETHER clean generation across the additionality scenarios.",
        },
        {
            "summary_id": "best_case_share_of_target",
            "value": f(max(float(row["share_of_3gj_balanced_target"]) for row in case_rows), 6),
            "unit": "fraction",
            "interpretation": "Best modeled share of the 3 GJ/tCO2 balanced power gate.",
        },
        {
            "summary_id": "market_unlocked_share_of_target",
            "value": next(row["share_of_3gj_balanced_target"] for row in case_rows if row["scenario"] == "market_unlocked_texas_style"),
            "unit": "fraction",
            "interpretation": "Modeled share of AETHER power target in the market-unlocked case.",
        },
        {
            "summary_id": "aether_dedicated_share_of_target",
            "value": next(row["share_of_3gj_balanced_target"] for row in case_rows if row["scenario"] == "aether_dedicated_buildout"),
            "unit": "fraction",
            "interpretation": "Modeled share of AETHER power target in the dedicated-buildout case.",
        },
        {
            "summary_id": "data_center_2030_share_of_target",
            "value": f(DATA_CENTER_2030_TWH / target_3gj, 6),
            "unit": "fraction",
            "interpretation": "IEA 2030 data-centre demand as a share of the 3 GJ/tCO2 balanced AETHER power gate.",
        },
    ]

    write_csv(CASES_OUT, case_rows)
    write_csv(COMPARATORS_OUT, comparator_rows)
    write_csv(POLICY_OUT, policy_rows)
    write_csv(SUMMARY_OUT, summary_rows)


if __name__ == "__main__":
    main()

