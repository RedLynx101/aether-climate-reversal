from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TABLE_DIR = ROOT / "analysis" / "tables"
TABLE_DIR.mkdir(parents=True, exist_ok=True)


PANELS = [
    {
        "panel_order": 1,
        "reviewer_panel": "carbon_cycle_and_climate",
        "discipline": "carbon-cycle and climate modeling",
        "risk_score": 5,
        "evidence_maturity_score": 2,
        "likely_attack": "The climate response remains a reduced-form screen; CO2 removal is not necessarily symmetric with emissions and non-CO2 forcing can dominate near-term outcomes.",
        "current_defense": "AETHER now has Joos impulse-response, climate-response proxy, dynamic emulator, and state-dependent removal-effectiveness screens, all explicitly labeled as non-final.",
        "decisive_test": "Re-run core pathways in FAIR or a comparable Earth-system workflow with non-CO2 forcing, aerosols, lifecycle emissions, ocean heat uptake, and removal asymmetry.",
        "failure_condition": "If FAIR-class modeling removes the strong-reversal outcome under net-zero 2050 plus AETHER, the paper must retreat from climate-reversal language to removal-infrastructure stress testing.",
        "next_artifact": "FAIR-class climate workflow and methods appendix",
        "primary_artifacts": "aether_climate_emulator_summary.csv; aether_state_dependent_carbon_summary.csv",
    },
    {
        "panel_order": 2,
        "reviewer_panel": "energy_systems_and_power_markets",
        "discipline": "power systems, industrial energy, and market design",
        "risk_score": 5,
        "evidence_maturity_score": 2,
        "likely_attack": "Annual TWh arithmetic does not prove deliverable additional clean power because hourly matching, transmission, interconnection, curtailment, and competing loads bind.",
        "current_defense": "AETHER separates gross clean-energy demand from additionality and competing demand, and it treats generic clean-energy growth as insufficient unless delivered to AETHER.",
        "decisive_test": "Regional dispatch and interconnection model for 10, 30, 50, and 100 GtCO2/year cases with hourly matching, firm clean power, storage duration, and data-center/industrial competing load.",
        "failure_condition": "If delivered additional low-carbon power cannot clear the 3 GJ/tCO2 balanced gate, the 100 GtCO2/year target becomes energy-constrained before storage or robotics can matter.",
        "next_artifact": "regional dispatch and additionality model",
        "primary_artifacts": "aether_clean_power_portfolio_summary.csv; aether_clean_energy_additionality_cases.csv",
    },
    {
        "panel_order": 3,
        "reviewer_panel": "cdr_process_and_materials",
        "discipline": "DAC/CDR process engineering and materials",
        "risk_score": 5,
        "evidence_maturity_score": 2,
        "likely_attack": "Contactor face area, sorbent life, pressure drop, fouling, replacement media, water, and commodity competition are not yet component-level designs.",
        "current_defense": "The paper now includes contactor-scale, sorbent-inventory, material supply-chain, lifecycle-emissions, and pathway source-range screens.",
        "decisive_test": "Pathway-specific bill-of-materials and process model for DACCS, enhanced weathering, ocean alkalinity, BECCS, biochar, direct ocean CDR, and mineralization with replacement schedules.",
        "failure_condition": "If any required media or contactor pathway exceeds credible production, recycling, or land/water constraints by orders of magnitude, the portfolio allocation must be redesigned.",
        "next_artifact": "pathway-specific BOM and process TEA",
        "primary_artifacts": "aether_air_contactor_scale_summary.csv; aether_material_supply_chain_summary.csv",
    },
    {
        "panel_order": 4,
        "reviewer_panel": "storage_and_subsurface",
        "discipline": "geologic storage, mineralization, ocean storage, and permitting",
        "risk_score": 5,
        "evidence_maturity_score": 2,
        "likely_attack": "Annual storage capacity is not enough; injection rate, pressure management, monitoring duration, leakage, induced seismicity, pore-space rights, and public consent can dominate.",
        "current_defense": "AETHER distinguishes gross capture from durable credited removal and now has route-level storage, regional corridor, injection-well, MRV, and liability screens.",
        "decisive_test": "Basin-level storage and mineralization model with injection-rate limits, pressure management, monitoring cost, permitting queues, leakage distributions, and liability buffers.",
        "failure_condition": "If basin-level injection and durability constraints cannot support the geologic/mineral share, the paper must lower the target or shift to more expensive storage states.",
        "next_artifact": "basin-level storage and liability model",
        "primary_artifacts": "aether_regional_storage_summary.csv; aether_injection_corridor_requirements.csv",
    },
    {
        "panel_order": 5,
        "reviewer_panel": "robotics_and_ai_productivity",
        "discipline": "robotics, autonomy, industrial automation, and AI R&D",
        "risk_score": 4,
        "evidence_maturity_score": 2,
        "likely_attack": "Robot production counts and humanoid announcements do not translate into useful autonomous field labor, drilling productivity, lab throughput, or maintenance reliability.",
        "current_defense": "The robotics layer separates robot classes, useful task-hours, duty cycle, supervision, replacement flow, and task-family demand; company claims remain leads.",
        "decisive_test": "Source-backed task-productivity distributions for autonomous construction, drilling, plant maintenance, inspection, material handling, robot labs, and MRV networks.",
        "failure_condition": "If autonomous useful work per robot-year stays low or supervision ratios stay high, robot cost falls but physical deployment does not scale fast enough.",
        "next_artifact": "task-family productivity distribution database",
        "primary_artifacts": "aether_robotics_productivity_summary.csv; aether_robotics_evidence.csv",
    },
    {
        "panel_order": 6,
        "reviewer_panel": "economics_and_finance",
        "discipline": "techno-economics, learning curves, capital formation, and macro constraints",
        "risk_score": 4,
        "evidence_maturity_score": 2,
        "likely_attack": "The cost stack is hand-set and may understate finance, insurance, siting, permitting, MRV, liability, replacement, and supply-chain inflation at extreme scale.",
        "current_defense": "AETHER keeps cost cases as scenario frontiers and preserves non-automatable floors for energy, storage, MRV, finance, materials, and liability.",
        "decisive_test": "Component-level TEA with sourced learning distributions, capital curves, financing assumptions, supply-chain inflation, and program-stage RD&D throughput.",
        "failure_condition": "If delivered cost remains above plausible public or market budgets after clean energy and automation, AETHER becomes a much smaller strategic CDR program.",
        "next_artifact": "component TEA and capital program model",
        "primary_artifacts": "aether_cost_improvement_frontier.csv; aether_trillion_rd_program_comparators.csv",
    },
    {
        "panel_order": 7,
        "reviewer_panel": "mrv_credit_integrity_and_law",
        "discipline": "MRV, carbon markets, environmental law, and liability",
        "risk_score": 4,
        "evidence_maturity_score": 2,
        "likely_attack": "Gross, durable, creditable, and legally accountable removal are different products; fraud, reversal, invalidation, cross-border leakage, and liability can erase nominal tonnes.",
        "current_defense": "The MRV layer applies provisional measurement, method, reversal, leakage, invalidation, and liability buffers and reports gross overbuild needed for creditable removal.",
        "decisive_test": "Method-specific MRV distributions and adversarial verification model with registry rules, invalidation processes, monitoring duration, and liability reserve design.",
        "failure_condition": "If credit integrity forces gross overbuild far above the portfolio's physical capacity, the target must shift from gross capture to verified durable credit.",
        "next_artifact": "method-specific MRV and liability model",
        "primary_artifacts": "aether_mrv_credit_integrity_summary.csv; aether_lifecycle_emissions_summary.csv",
    },
    {
        "panel_order": 8,
        "reviewer_panel": "governance_and_rebound",
        "discipline": "climate policy, commons governance, justice, and political economy",
        "risk_score": 5,
        "evidence_maturity_score": 1,
        "likely_attack": "Cheap removal can become permission to emit; treating atmosphere, oceans, and lakes as citizen-owned sinks is legally and politically underdeveloped.",
        "current_defense": "AETHER models rebound thresholds, separates the commons-ownership branch as exploratory, and treats shared sinks as assets needing fees, bans, liability, and MRV.",
        "decisive_test": "Governance model comparing carbon tax, cap-and-dividend, public atmospheric trust, sink-use fees, output bans, liability, and citizen dividends under MRV failure modes.",
        "failure_condition": "If rebound and delayed abatement cannot be constrained, AETHER stops being climate reversal even if the hardware works.",
        "next_artifact": "governance and rebound-control model",
        "primary_artifacts": "aether_jevons_rebound_sensitivity.csv; commons-ownership-and-citizen-dividends.md",
    },
]


FALSIFICATION_TESTS = [
    {
        "test_order": 1,
        "test_id": "F1_fair_climate_reversal",
        "target_claim": "AETHER plus emissions decline can produce climate reversal rather than offset bookkeeping.",
        "falsification_rule": "FAIR-class or Earth-system modeling with lifecycle emissions and non-CO2 forcing cannot produce a material 2100 temperature or concentration improvement under net-zero 2050 plus AETHER.",
        "current_status": "not_run; screening emulator only",
        "owner_panel": "carbon_cycle_and_climate",
        "priority": "P0",
        "decision_if_failed": "Remove climate-reversal language and frame AETHER as an infrastructure stress test.",
        "evidence_artifacts": "aether_climate_emulator_summary.csv; aether_state_dependent_carbon_summary.csv",
    },
    {
        "test_order": 2,
        "test_id": "F2_additional_clean_power",
        "target_claim": "A 3 GJ/tCO2 AETHER system can be powered with additional low-carbon energy.",
        "falsification_rule": "Regional hourly dispatch and interconnection modeling cannot supply the balanced AETHER power gate after ordinary electrification and data-center demand.",
        "current_status": "not_run; annual buildout screen only",
        "owner_panel": "energy_systems_and_power_markets",
        "priority": "P0",
        "decision_if_failed": "Cap feasible removal by delivered clean power or shift to slower deployment.",
        "evidence_artifacts": "aether_clean_power_portfolio_summary.csv; aether_clean_energy_additionality_cases.csv",
    },
    {
        "test_order": 3,
        "test_id": "F3_storage_injection_capacity",
        "target_claim": "AETHER can store or mineralize tens of GtCO2/year durably.",
        "falsification_rule": "Basin-level injection, pressure, mineralization, leakage, permitting, and monitoring constraints cannot support the portfolio's durable storage share.",
        "current_status": "partial; corridor and route screens only",
        "owner_panel": "storage_and_subsurface",
        "priority": "P0",
        "decision_if_failed": "Lower the portfolio target or move to costlier storage/conversion states.",
        "evidence_artifacts": "aether_regional_storage_summary.csv; aether_injection_corridor_requirements.csv",
    },
    {
        "test_order": 4,
        "test_id": "F4_creditable_overbuild",
        "target_claim": "100 GtCO2/year gross capture can be turned into roughly target-scale durable credit.",
        "falsification_rule": "Pathway-specific LCA, MRV, reversal, leakage, invalidation, and liability buffers require gross overbuild outside the physical portfolio capacity.",
        "current_status": "partial; provisional MRV and LCA screens",
        "owner_panel": "mrv_credit_integrity_and_law",
        "priority": "P0",
        "decision_if_failed": "Use creditable tonnes as the headline target and treat 100 Gt gross as insufficient.",
        "evidence_artifacts": "aether_mrv_credit_integrity_summary.csv; aether_lifecycle_emissions_summary.csv",
    },
    {
        "test_order": 5,
        "test_id": "F5_component_tea_floor",
        "target_claim": "AI and robotics can drive delivered costs toward the AETHER automation-push or deep-abundance frontier.",
        "falsification_rule": "Component-level TEA keeps delivered cost above plausible public or market budgets after energy, storage, finance, MRV, materials, and liability floors.",
        "current_status": "not_run; scenario cost stack only",
        "owner_panel": "economics_and_finance",
        "priority": "P1",
        "decision_if_failed": "Reduce target scale or frame AETHER as a strategic insurance program requiring explicit subsidy.",
        "evidence_artifacts": "aether_cost_improvement_frontier.csv; aether_cost_bucket_reduction_factors.csv",
    },
    {
        "test_order": 6,
        "test_id": "F6_robot_productivity",
        "target_claim": "AI and robotics can materially accelerate physical deployment.",
        "falsification_rule": "Task-family productivity distributions show low autonomous useful work, high supervision, short duty cycles, or high maintenance across construction, drilling, MRV, and plant operations.",
        "current_status": "partial; robot class and task-demand screen",
        "owner_panel": "robotics_and_ai_productivity",
        "priority": "P1",
        "decision_if_failed": "Keep AI as an R&D accelerator but remove strong labor-abundance assumptions.",
        "evidence_artifacts": "aether_robotics_productivity_summary.csv; aether_robotics_evidence.csv",
    },
    {
        "test_order": 7,
        "test_id": "F7_process_materials",
        "target_claim": "The 100 GtCO2/year pathway portfolio is physically buildable.",
        "falsification_rule": "Pathway-specific BOM and replacement models show sorbent, alkaline media, water, steel, cement, copper, land, or disposal streams exceeding credible production and recycling pathways.",
        "current_status": "partial; material pressure screen only",
        "owner_panel": "cdr_process_and_materials",
        "priority": "P1",
        "decision_if_failed": "Reallocate away from failed pathways or lower total target.",
        "evidence_artifacts": "aether_material_supply_chain_summary.csv; aether_air_contactor_scale_summary.csv",
    },
    {
        "test_order": 8,
        "test_id": "F8_rebound_control",
        "target_claim": "AETHER can remain net-negative rather than enabling new emissions.",
        "falsification_rule": "Policy and market modeling cannot keep rebound, delayed abatement, and induced emissions below the threshold that erases simple net-negative benefit.",
        "current_status": "partial; arithmetic rebound threshold only",
        "owner_panel": "governance_and_rebound",
        "priority": "P0",
        "decision_if_failed": "Make emissions controls and sink-use pricing a binding precondition rather than an optional governance section.",
        "evidence_artifacts": "aether_jevons_rebound_sensitivity.csv; commons-ownership-and-citizen-dividends.md",
    },
    {
        "test_order": 9,
        "test_id": "F9_joint_probability",
        "target_claim": "The favorable AETHER case is a plausible upper-tail scenario rather than a cherry-picked pile of independent optimism.",
        "falsification_rule": "Expert elicitation and covariance modeling show that favorable clean power, automation, storage, cost, rebound, and execution assumptions rarely co-occur.",
        "current_status": "partial; hand-set correlated scenario families",
        "owner_panel": "economics_and_finance",
        "priority": "P1",
        "decision_if_failed": "Retain AETHER as a research agenda but stop presenting the full 100 Gt case as plausibly reachable in 20 years.",
        "evidence_artifacts": "aether_correlated_uncertainty_summary.csv; aether_uncertainty_distribution_registry.csv",
    },
    {
        "test_order": 10,
        "test_id": "F10_prior_art_collision",
        "target_claim": "AETHER contributes a useful coupled feasibility-boundary model.",
        "falsification_rule": "A direct prior-art audit finds an existing work that already provides the same coupled 100 GtCO2/year AI/robotics/energy/storage/governance model with stronger evidence.",
        "current_status": "partial; first positioning matrix only",
        "owner_panel": "cdr_process_and_materials",
        "priority": "P2",
        "decision_if_failed": "Reframe AETHER as replication, extension, or review rather than a new proposal.",
        "evidence_artifacts": "aether_prior_art_positioning_matrix.csv",
    },
]


FEEDBACK_PACKET = [
    {
        "packet_order": 1,
        "reviewer_group": "CDR process engineers",
        "question": "Which DAC, mineralization, enhanced-weathering, ocean-CDR, biochar, and BECCS parameters are most wrong in the current portfolio?",
        "materials_to_send": "paper sections 4.6-4.8 and 4.11; aether_air_contactor_scale_summary.csv; aether_material_supply_chain_summary.csv",
        "desired_output": "Corrected pathway parameters, disqualifying process bottlenecks, and priority TEA sources.",
    },
    {
        "packet_order": 2,
        "reviewer_group": "Energy-system modelers",
        "question": "What regional dispatch and interconnection assumptions would make the 3 GJ/tCO2 balanced case fail first?",
        "materials_to_send": "sections 4.3, 4.4, and 5.1; aether_clean_power_portfolio_summary.csv; aether_clean_energy_additionality_cases.csv",
        "desired_output": "Dispatch-model specification, hourly constraints, and credible additionality test.",
    },
    {
        "packet_order": 3,
        "reviewer_group": "Storage and Class VI experts",
        "question": "Where does the 54 GtCO2/year geologic-storage branch break under basin-level injection, pressure, liability, and monitoring constraints?",
        "materials_to_send": "sections 4.8 and 4.8.1; aether_regional_storage_summary.csv; aether_injection_corridor_requirements.csv",
        "desired_output": "Basin-level storage work plan and invalid assumptions in current corridor archetypes.",
    },
    {
        "packet_order": 4,
        "reviewer_group": "Climate modelers",
        "question": "What is the minimum FAIR-class or Earth-system-model experiment set needed before AETHER can make climate-reversal claims?",
        "materials_to_send": "sections 4.2-4.2.3; aether_climate_emulator_summary.csv; aether_state_dependent_carbon_summary.csv",
        "desired_output": "Modeling protocol, forcing paths, and acceptable language for preliminary claims.",
    },
    {
        "packet_order": 5,
        "reviewer_group": "Robotics and automation experts",
        "question": "Which field tasks are actually robot-limited, and where do autonomy, supervision, reliability, and maintenance erase labor-abundance gains?",
        "materials_to_send": "section 6; aether_robotics_productivity_summary.csv; aether_robotics_task_demand.csv",
        "desired_output": "Task-productivity priors and categories where humanoid or mobile robots should not be credited.",
    },
    {
        "packet_order": 6,
        "reviewer_group": "Carbon-market and MRV experts",
        "question": "What method-specific invalidation, reversal, leakage, and liability buffers should replace the current provisional MRV screen?",
        "materials_to_send": "section 4.10; aether_mrv_credit_integrity_summary.csv; aether_lifecycle_emissions_summary.csv",
        "desired_output": "Creditable-tonne accounting rules and adversarial verification plan.",
    },
    {
        "packet_order": 7,
        "reviewer_group": "Climate-policy and commons-governance scholars",
        "question": "Can atmospheric and ocean sinks be priced or governed as citizen-owned/public-trust assets without becoming a license to pollute?",
        "materials_to_send": "sections 5.3 and 8; commons-ownership-and-citizen-dividends.md",
        "desired_output": "Governance options, rebound controls, legal blockers, and liability structure.",
    },
]


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    high_risk = [row for row in PANELS if row["risk_score"] >= 4]
    p0_tests = [row for row in FALSIFICATION_TESTS if row["priority"] == "P0"]
    summary = [
        {"metric": "review_panel_count", "value": len(PANELS), "unit": "count", "interpretation": "number of expert review panels in the adversarial gauntlet"},
        {"metric": "high_risk_panel_count", "value": len(high_risk), "unit": "count", "interpretation": "panels scoring 4 or 5 on current reviewer risk"},
        {"metric": "p0_falsification_test_count", "value": len(p0_tests), "unit": "count", "interpretation": "tests that can directly force a major reframing of the paper"},
        {"metric": "average_risk_score", "value": round(sum(row["risk_score"] for row in PANELS) / len(PANELS), 2), "unit": "score_1_to_5", "interpretation": "mean reviewer risk before the next evidence upgrade"},
        {"metric": "average_evidence_maturity_score", "value": round(sum(row["evidence_maturity_score"] for row in PANELS) / len(PANELS), 2), "unit": "score_1_to_5", "interpretation": "mean current maturity of evidence against likely reviewer attack"},
        {"metric": "feedback_packet_question_count", "value": len(FEEDBACK_PACKET), "unit": "count", "interpretation": "reviewer-facing questions ready for scientist feedback"},
    ]

    write_csv(TABLE_DIR / "aether_adversarial_review_panels.csv", PANELS)
    write_csv(TABLE_DIR / "aether_falsification_tests.csv", FALSIFICATION_TESTS)
    write_csv(TABLE_DIR / "aether_scientist_feedback_packet.csv", FEEDBACK_PACKET)
    write_csv(TABLE_DIR / "aether_adversarial_review_summary.csv", summary)


if __name__ == "__main__":
    main()

