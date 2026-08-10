from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TABLE_DIR = ROOT / "analysis" / "tables"

ASSUMPTIONS = TABLE_DIR / "aether_uncertainty_assumptions.csv"
REGISTRY = TABLE_DIR / "aether_uncertainty_distribution_registry.csv"
PRIORITIES = TABLE_DIR / "aether_uncertainty_distribution_upgrade_priorities.csv"
CORRELATIONS = TABLE_DIR / "aether_uncertainty_correlation_hypotheses.csv"


METADATA: dict[str, dict[str, object]] = {
    "energy_gj_tco2": {
        "evidence_grade": "B",
        "current_distribution_status": "source_informed_handset",
        "source_keys": "ipcc_ar6_wg3_ch12;national_academies_dac_ch5_2018;keith_2018_process_dac;netl_sorbent_dac_2025;climeworks_mammoth_2024;onepointfive_stratos_2026",
        "distribution_rationale": "Bounded by published DAC energy ranges and advanced-process claims, but the Monte Carlo range is still a hand-set cross-pathway screen.",
        "needed_distribution_type": "pathway-specific PERT or lognormal distributions by capture process and deployment year",
        "correlation_family": "energy_cost_coupling;clean_power_coupling",
        "upgrade_priority": 1,
        "review_owner": "energy systems reviewer",
        "paper_use_rule": "Use as a sensitivity input, not as a calibrated forecast of future energy intensity.",
        "next_evidence_task": "Fit pathway-specific energy distributions from DAC, mineralization, ocean CDR, and BECCS literature.",
    },
    "clean_addition_growth_rate": {
        "evidence_grade": "B",
        "current_distribution_status": "source_informed_handset",
        "source_keys": "iea_electricity_2026;iea_global_energy_review_2026;irena_power_costs_2024;berkeley_lab_queued_up_2025",
        "distribution_rationale": "Anchored to recent electricity and clean-generation growth, then stretched for an AETHER-scale acceleration scenario.",
        "needed_distribution_type": "scenario-family distribution tied to IEA/NREL/IRENA buildout baselines and interconnection constraints",
        "correlation_family": "clean_power_coupling;energy_cost_coupling",
        "upgrade_priority": 1,
        "review_owner": "power systems reviewer",
        "paper_use_rule": "Treat as a buildout stress-test variable until tied to regional grid models.",
        "next_evidence_task": "Create clean-power growth scenarios with transmission, interconnection, storage-duration, and firm-power constraints.",
    },
    "aether_clean_share": {
        "evidence_grade": "D",
        "current_distribution_status": "scenario_assumption",
        "source_keys": "iea_energy_ai_2025;microsoft_constellation_crane_2024;google_kairos_2024;helion_microsoft_fusion_2023",
        "distribution_rationale": "Represents political and market allocation of new clean power to AETHER after data centers, electrification, industry, and households.",
        "needed_distribution_type": "governance and market-allocation scenario distribution",
        "correlation_family": "clean_power_coupling;policy_rebound_coupling",
        "upgrade_priority": 1,
        "review_owner": "energy policy reviewer",
        "paper_use_rule": "Use only as a scenario assumption; do not cite as likely clean-power allocation.",
        "next_evidence_task": "Model opportunity cost of assigning clean power to AETHER versus electrification and AI/data-center demand.",
    },
    "clean_deliverability_fraction": {
        "evidence_grade": "C",
        "current_distribution_status": "source_informed_handset",
        "source_keys": "berkeley_lab_queued_up_2025;nrel_atb_2024_electricity;nrel_atb_land_wind_2024;nrel_atb_nuclear_2024;iea_geothermal_future_2024",
        "distribution_rationale": "Discounts clean generation for capacity factor, curtailment, firming, transmission, siting, and downtime; currently a single coarse scalar.",
        "needed_distribution_type": "regional deliverability distribution by technology mix and grid topology",
        "correlation_family": "clean_power_coupling",
        "upgrade_priority": 1,
        "review_owner": "grid integration reviewer",
        "paper_use_rule": "Use only as a crude deliverability discount until a dispatch or power-system model exists.",
        "next_evidence_task": "Replace the scalar with regional capacity-factor, storage-duration, curtailment, and transmission assumptions.",
    },
    "robot_output_growth_rate": {
        "evidence_grade": "D",
        "current_distribution_status": "provisional_lead",
        "source_keys": "ifr_world_robotics_2025;amazon_robotics_750k_robots_2024;unitree_g1_product_2026;figure_botq_2025;figure_ramping_2026;agility_robofab_2023",
        "distribution_rationale": "Uses robotics production and company-scale leads as acceleration signals, but humanoid ramp claims are not yet citation-grade for AETHER-scale deployment.",
        "needed_distribution_type": "manufacturing-ramp distribution separated by industrial robots, field robots, humanoids, and specialized automation",
        "correlation_family": "automation_coupling",
        "upgrade_priority": 1,
        "review_owner": "robotics manufacturing reviewer",
        "paper_use_rule": "Treat social-media and company-rate claims as leads until archived and corroborated.",
        "next_evidence_task": "Build a robotics production-rate dataset with audited annual capacity, factory count, task class, and utilization.",
    },
    "aether_robot_share": {
        "evidence_grade": "D",
        "current_distribution_status": "scenario_assumption",
        "source_keys": "ifr_world_robotics_2025;amazon_robotics_750k_robots_2024;figure_botq_2025;agility_robofab_2023",
        "distribution_rationale": "Represents whether AETHER gets robot capacity ahead of construction, logistics, manufacturing, eldercare, defense, households, and general industry.",
        "needed_distribution_type": "industrial allocation and opportunity-cost scenario distribution",
        "correlation_family": "automation_coupling;policy_rebound_coupling",
        "upgrade_priority": 2,
        "review_owner": "industrial strategy reviewer",
        "paper_use_rule": "Use as a program-design lever, not as an autonomous robotics forecast.",
        "next_evidence_task": "Estimate competing robot-demand sectors and how a public or private AETHER program could reserve capacity.",
    },
    "robots_per_mtco2_y_capacity": {
        "evidence_grade": "D",
        "current_distribution_status": "scenario_assumption",
        "source_keys": "amazon_robotics_750k_robots_2024;unitree_g1_product_2026;figure_botq_2025;agility_robofab_2023",
        "distribution_rationale": "No direct evidence yet maps a general robot to MtCO2/year of durable CDR capacity; this is the central robotics productivity placeholder.",
        "needed_distribution_type": "task-based productivity distribution by construction, drilling, logistics, maintenance, inspection, and MRV",
        "correlation_family": "automation_coupling",
        "upgrade_priority": 1,
        "review_owner": "robotics task-productivity reviewer",
        "paper_use_rule": "Treat as a dominant speculative input and stress-test it adversarially.",
        "next_evidence_task": "Convert CDR deployment work packages into robot-hours, supervised-autonomy rates, payload limits, and uptime assumptions.",
    },
    "storage_terminal_gtco2_y": {
        "evidence_grade": "C",
        "current_distribution_status": "source_informed_handset",
        "source_keys": "netl_carbon_storage_atlas_v_2015;usgs_circular_1386_geologic_storage;epa_class_vi_wells_2026;epa_current_class_vi_projects_2026;national_academies_ocean_cdr_2022",
        "distribution_rationale": "Capacity and throughput are both relevant; current range mixes geologic, mineral, biomass, product, and ocean storage without basin-level injection distributions.",
        "needed_distribution_type": "regional throughput distribution by storage route, permit regime, injection rate, and monitoring burden",
        "correlation_family": "storage_mrv_coupling",
        "upgrade_priority": 1,
        "review_owner": "storage geoscience reviewer",
        "paper_use_rule": "Do not treat resource capacity as deployable annual throughput.",
        "next_evidence_task": "Build basin-level storage throughput curves with pressure management, leakage, Class VI equivalents, and monitoring duration.",
    },
    "cost_usd_tco2": {
        "evidence_grade": "C",
        "current_distribution_status": "source_informed_handset",
        "source_keys": "young_2023_dacs_cost_targets;realmonte_2019_daccs_iam;chatterjee_huang_2020_unrealistic_dac;keith_2018_process_dac;wri_scaling_dac_impacts_2024",
        "distribution_rationale": "Cost ranges reflect DAC and CDR cost literature plus AETHER automation assumptions; current Monte Carlo does not yet decompose capex, energy, storage, MRV, finance, and liability.",
        "needed_distribution_type": "component cost-stack distributions with correlated learning curves",
        "correlation_family": "automation_coupling;energy_cost_coupling",
        "upgrade_priority": 1,
        "review_owner": "climate economics reviewer",
        "paper_use_rule": "Use as a delivered-cost stress test until each cost bucket has its own distribution.",
        "next_evidence_task": "Fit cost distributions by pathway and cost bucket, then correlate energy price, robot productivity, MRV burden, and finance.",
    },
    "annual_budget_trillion_usd": {
        "evidence_grade": "D",
        "current_distribution_status": "scenario_assumption",
        "source_keys": "ncses_us_rd_2023;iea_state_energy_innovation_2026;state_of_cdr_2026",
        "distribution_rationale": "Program budget depends on public legitimacy, market demand, carbon price/tax structure, citizen-dividend design, and competing spending priorities.",
        "needed_distribution_type": "political-economy and carbon-market scenario distribution",
        "correlation_family": "policy_rebound_coupling",
        "upgrade_priority": 2,
        "review_owner": "public finance reviewer",
        "paper_use_rule": "Use as a funding-cap stress test, not as a financing forecast.",
        "next_evidence_task": "Compare AETHER annual spending with global energy investment, R&D, military, infrastructure, and climate-finance flows.",
    },
    "durability_fraction_100y": {
        "evidence_grade": "C",
        "current_distribution_status": "source_informed_handset",
        "source_keys": "state_of_cdr_2026;eu_crcf_2024;oxford_offsetting_principles_2024;epa_subpart_rr_mrv_2026;national_academies_ocean_cdr_2022",
        "distribution_rationale": "Current fraction combines lifecycle emissions, permanence, reversal, measurement, method uncertainty, and crediting buffers into one number.",
        "needed_distribution_type": "pathway-specific durability and MRV-crediting distribution",
        "correlation_family": "storage_mrv_coupling",
        "upgrade_priority": 1,
        "review_owner": "MRV and permanence reviewer",
        "paper_use_rule": "Use only as a portfolio haircut until pathway-specific reversal and measurement distributions exist.",
        "next_evidence_task": "Separate lifecycle emissions, measurement error, reversal risk, leakage, invalidation reserve, and liability into independent but correlated terms.",
    },
    "residual_emissions_2046_gtco2_y": {
        "evidence_grade": "C",
        "current_distribution_status": "scenario_assumption",
        "source_keys": "global_carbon_budget_2025;iea_global_energy_review_2026;ipcc_ar6_wg3_ch12",
        "distribution_rationale": "Residual emissions depend on global mitigation speed, policy, energy abundance, industrial substitution, and whether AETHER delays abatement.",
        "needed_distribution_type": "emissions-scenario distribution coupled to rebound and clean-power allocation",
        "correlation_family": "policy_rebound_coupling",
        "upgrade_priority": 2,
        "review_owner": "integrated assessment reviewer",
        "paper_use_rule": "Use as a scenario branch; do not hide emissions futures inside removal capacity.",
        "next_evidence_task": "Map residual emissions to SSP-like pathways and explicit AETHER-induced delay assumptions.",
    },
    "rebound_fraction_of_gross": {
        "evidence_grade": "C",
        "current_distribution_status": "source_informed_handset",
        "source_keys": "alcott_2005_jevons_paradox;sorrell_2009_jevons_rebound;georgetown_atmospheric_trust_2023;cornell_public_trust_doctrine",
        "distribution_rationale": "Jevons-style rebound is real enough to model, but no source directly calibrates rebound from globally cheap durable CDR.",
        "needed_distribution_type": "behavioral, policy, and market-response scenario distribution",
        "correlation_family": "policy_rebound_coupling",
        "upgrade_priority": 1,
        "review_owner": "climate policy reviewer",
        "paper_use_rule": "Keep rebound visible as a climate-result subtractor, not a footnote.",
        "next_evidence_task": "Build rebound scenarios tied to carbon pricing, commons ownership, offset quality, sectoral abatement delay, and income effects.",
    },
    "gross_overbuild_factor": {
        "evidence_grade": "C",
        "current_distribution_status": "derived_screen",
        "source_keys": "state_of_cdr_2026;eu_crcf_2024;oxford_offsetting_principles_2024;epa_subpart_rr_mrv_2026",
        "distribution_rationale": "Overbuild derives from lifecycle, durability, MRV, downtime, leakage, reversal reserves, and pathway mix; current scalar compresses those layers.",
        "needed_distribution_type": "derived distribution from pathway-specific gross-to-creditable crediting model",
        "correlation_family": "storage_mrv_coupling",
        "upgrade_priority": 2,
        "review_owner": "model integration reviewer",
        "paper_use_rule": "Prefer deriving this from the MRV model rather than sampling it independently.",
        "next_evidence_task": "Use the MRV credit-integrity model to generate overbuild distributions by portfolio mix.",
    },
    "execution_realization_fraction": {
        "evidence_grade": "D",
        "current_distribution_status": "scenario_assumption",
        "source_keys": "berkeley_lab_queued_up_2025;epa_current_class_vi_projects_2026;state_of_cdr_2026;wri_scaling_dac_impacts_2024",
        "distribution_rationale": "Captures coordination, permitting, logistics, siting, supply-chain, labor, safety, and operating failures that are not yet modeled physically.",
        "needed_distribution_type": "program-execution risk distribution with correlated permitting, supply-chain, and social-license failures",
        "correlation_family": "automation_coupling;storage_mrv_coupling;policy_rebound_coupling",
        "upgrade_priority": 1,
        "review_owner": "infrastructure delivery reviewer",
        "paper_use_rule": "Treat as a major unknown, not a cleanup factor added after optimistic modeling.",
        "next_evidence_task": "Build a failure-mode register from megaproject, grid, CCS permitting, mining, and large industrial deployment evidence.",
    },
}


CORRELATION_ROWS = [
    {
        "correlation_family": "clean_power_coupling",
        "parameters": "clean_addition_growth_rate;aether_clean_share;clean_deliverability_fraction;energy_gj_tco2",
        "hypothesized_relationship": "Higher clean buildout can raise available AETHER power, but allocation and deliverability can fall when ordinary electrification and data-center demand compete for the same supply.",
        "direction": "mixed",
        "why_it_matters": "AETHER cannot treat clean generation, clean allocation, and deliverability as independent wins.",
        "test_or_source_needed": "Regional power-system scenarios with interconnection, transmission, firming, and opportunity-cost accounting.",
    },
    {
        "correlation_family": "automation_coupling",
        "parameters": "robot_output_growth_rate;aether_robot_share;robots_per_mtco2_y_capacity;cost_usd_tco2;execution_realization_fraction",
        "hypothesized_relationship": "Better automation can raise robot supply, lower labor cost, improve execution, and reduce robot count per unit of capacity at the same time.",
        "direction": "positive for capacity, negative for cost",
        "why_it_matters": "The robotics premise is coupled; sampling each variable independently can understate both success and failure clustering.",
        "test_or_source_needed": "Task-level robotics productivity model with manufacturing ramp and useful autonomous work-hour distributions.",
    },
    {
        "correlation_family": "storage_mrv_coupling",
        "parameters": "storage_terminal_gtco2_y;durability_fraction_100y;gross_overbuild_factor;execution_realization_fraction",
        "hypothesized_relationship": "High-throughput storage routes may carry higher MRV burden, public resistance, reversal risk, or pressure-management constraints.",
        "direction": "mixed",
        "why_it_matters": "Storage capacity, creditability, and execution should not be separated in a publication model.",
        "test_or_source_needed": "Basin-level and pathway-level storage throughput, MRV, leakage, reversal, liability, and permit-duration distributions.",
    },
    {
        "correlation_family": "policy_rebound_coupling",
        "parameters": "rebound_fraction_of_gross;residual_emissions_2046_gtco2_y;annual_budget_trillion_usd;aether_clean_share",
        "hypothesized_relationship": "Political support for AETHER can increase budget and clean-power allocation while also increasing moral hazard if removal substitutes for abatement.",
        "direction": "mixed",
        "why_it_matters": "A large removal program can either complement mitigation or become permission to keep using the atmospheric sink.",
        "test_or_source_needed": "Policy scenarios for carbon pricing, citizen-owned commons, credit rules, and restrictions on dangerous emissions.",
    },
    {
        "correlation_family": "energy_cost_coupling",
        "parameters": "energy_gj_tco2;cost_usd_tco2;clean_addition_growth_rate;clean_deliverability_fraction",
        "hypothesized_relationship": "Energy intensity and power-system cost interact directly; cheap clean power lowers delivered cost only when it is deliverable and not opportunity-cost constrained.",
        "direction": "positive cost coupling, negative abundance coupling",
        "why_it_matters": "A low $/tCO2 case is not credible without checking energy intensity, power price, firming, and grid deliverability together.",
        "test_or_source_needed": "Cost-stack model with regional electricity prices, capacity factors, firming cost, storage duration, and learning curves.",
    },
]


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


def main() -> None:
    assumption_rows = read_csv(ASSUMPTIONS)
    assumption_by_parameter = {row["parameter"]: row for row in assumption_rows}
    missing = sorted(set(METADATA) - set(assumption_by_parameter))
    if missing:
        raise ValueError(f"Missing uncertainty assumptions: {missing}")

    registry_rows: list[dict[str, object]] = []
    for row in assumption_rows:
        parameter = row["parameter"]
        if parameter not in METADATA:
            raise ValueError(f"No distribution metadata for uncertainty parameter: {parameter}")
        meta = METADATA[parameter]
        source_keys = str(meta["source_keys"])
        registry_rows.append({
            "parameter": parameter,
            "label": row["label"],
            "unit": row["unit"],
            "current_low": row["low"],
            "current_mode": row["mode"],
            "current_high": row["high"],
            "current_interpretation": row["interpretation"],
            "evidence_grade": meta["evidence_grade"],
            "current_distribution_status": meta["current_distribution_status"],
            "source_keys": source_keys,
            "source_key_count": len([key for key in source_keys.split(";") if key]),
            "distribution_rationale": meta["distribution_rationale"],
            "needed_distribution_type": meta["needed_distribution_type"],
            "correlation_family": meta["correlation_family"],
            "upgrade_priority": meta["upgrade_priority"],
            "review_owner": meta["review_owner"],
            "paper_use_rule": meta["paper_use_rule"],
            "next_evidence_task": meta["next_evidence_task"],
        })

    registry_rows.sort(key=lambda row: (int(row["upgrade_priority"]), str(row["evidence_grade"]), str(row["parameter"])))

    def select_rows(kind: str) -> list[dict[str, object]]:
        if kind == "high_priority_source_distribution":
            return [
                row for row in registry_rows
                if int(row["upgrade_priority"]) == 1
                and str(row["evidence_grade"]) in {"B", "C"}
                and "source" in str(row["current_distribution_status"])
            ]
        if kind == "high_priority_assumption_correlation":
            return [
                row for row in registry_rows
                if int(row["upgrade_priority"]) == 1
                and (
                    str(row["evidence_grade"]) == "D"
                    or "scenario" in str(row["current_distribution_status"])
                    or "provisional" in str(row["current_distribution_status"])
                )
            ]
        if kind == "medium_priority_program_design":
            return [row for row in registry_rows if int(row["upgrade_priority"]) == 2]
        if kind == "lower_priority_documentation":
            return [row for row in registry_rows if int(row["upgrade_priority"]) >= 3]
        raise ValueError(kind)

    priority_specs = [
        (
            "high_priority_source_distribution",
            "Inputs with relevant source anchors but no fitted distribution yet.",
            "Fit source-backed pathway or sector distributions and replace triangular ranges.",
        ),
        (
            "high_priority_assumption_correlation",
            "Inputs that dominate feasibility while still resting on scenario or provisional robotics/program assumptions.",
            "Run adversarial sensitivity, expert elicitation, and correlated scenario families before using probabilities rhetorically.",
        ),
        (
            "medium_priority_program_design",
            "Inputs that depend on program allocation, funding, residual emissions, and derived overbuild design.",
            "Tie these variables to explicit governance, funding, and portfolio design branches.",
        ),
        (
            "lower_priority_documentation",
            "Inputs whose current documentation is acceptable for screening but still needs publication-grade source notes.",
            "Keep source notes current and promote to distributions when the surrounding model matures.",
        ),
    ]

    priority_rows: list[dict[str, object]] = []
    for band, why, next_upgrade in priority_specs:
        rows = select_rows(band)
        priority_rows.append({
            "priority_band": band,
            "parameter_count": len(rows),
            "parameters": ";".join(str(row["parameter"]) for row in rows),
            "why_it_matters": why,
            "next_upgrade": next_upgrade,
        })

    write_csv(REGISTRY, registry_rows)
    write_csv(PRIORITIES, priority_rows)
    write_csv(CORRELATIONS, CORRELATION_ROWS)


if __name__ == "__main__":
    main()

