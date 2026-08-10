from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TABLE_DIR = ROOT / "analysis" / "tables"
TABLE_DIR.mkdir(parents=True, exist_ok=True)

TWH_PER_GJ_PER_TON_FOR_1_GT = 277.77777777777777
FIRMING_AND_DELIVERY_PENALTY = 0.10
BASELINE_ANNUAL_CLEAN_ADDITION_TWH = 850.0
YEARS = 20
BALANCED_ENERGY_GJ_PER_TCO2 = 3.0
DATA_CENTER_2030_TWH = 950.0


def cumulative_generation_from_additions(first_year_addition_twh: float, growth_rate: float, years: int = YEARS) -> float:
    if abs(growth_rate) < 1e-12:
        return first_year_addition_twh * years
    return first_year_addition_twh * (((1.0 + growth_rate) ** years - 1.0) / growth_rate)


def gate_twh(target_gtco2_y: float, energy_gj_tco2: float = BALANCED_ENERGY_GJ_PER_TCO2) -> float:
    return target_gtco2_y * energy_gj_tco2 * TWH_PER_GJ_PER_TON_FOR_1_GT * (1.0 + FIRMING_AND_DELIVERY_PENALTY)


SCENARIOS = [
    {
        "scenario": "status_quo_friction",
        "display_name": "Status quo friction",
        "annual_growth_rate": 0.08,
        "starting_annual_addition_twh": BASELINE_ANNUAL_CLEAN_ADDITION_TWH,
        "ordinary_demand_claim_twh_y": 30000.0,
        "aether_dedication_fraction": 0.40,
        "additionality_factor": 0.70,
        "interconnection_factor": 0.55,
        "transmission_siting_factor": 0.65,
        "hourly_matching_factor": 0.60,
        "firm_clean_factor": 0.55,
        "source_keys": "iea_global_energy_review_2026;iea_energy_ai_2025;berkeley_lab_queued_up_2025;irena_power_costs_2024",
        "paper_use_rule": "Failure case for P0 F2; annual clean-energy arithmetic does not translate into delivered AETHER power.",
    },
    {
        "scenario": "market_unlocked_texas_style",
        "display_name": "Market unlocked",
        "annual_growth_rate": 0.15,
        "starting_annual_addition_twh": BASELINE_ANNUAL_CLEAN_ADDITION_TWH,
        "ordinary_demand_claim_twh_y": 40000.0,
        "aether_dedication_fraction": 0.55,
        "additionality_factor": 0.85,
        "interconnection_factor": 0.75,
        "transmission_siting_factor": 0.78,
        "hourly_matching_factor": 0.70,
        "firm_clean_factor": 0.65,
        "source_keys": "irena_power_costs_2024;eia_texas_energy_profile_2024;california_energy_commission_2024_tseg;berkeley_lab_queued_up_2025",
        "paper_use_rule": "Market-led upside case; cheap renewables help, but hourly and grid deliverability still bind.",
    },
    {
        "scenario": "dedicated_aether_corridors",
        "display_name": "Dedicated AETHER corridors",
        "annual_growth_rate": 0.20,
        "starting_annual_addition_twh": BASELINE_ANNUAL_CLEAN_ADDITION_TWH,
        "ordinary_demand_claim_twh_y": 45000.0,
        "aether_dedication_fraction": 0.85,
        "additionality_factor": 0.95,
        "interconnection_factor": 0.86,
        "transmission_siting_factor": 0.88,
        "hourly_matching_factor": 0.78,
        "firm_clean_factor": 0.76,
        "source_keys": "nrel_atb_2024_electricity;iea_electricity_2026;iea_geothermal_future_2024;iaea_nuclear_status_2025",
        "paper_use_rule": "Strong public/industrial buildout case; passes partial AETHER scales but not the full 100 Gt gate.",
    },
    {
        "scenario": "firm_clean_backbone",
        "display_name": "Firm clean backbone",
        "annual_growth_rate": 0.18,
        "starting_annual_addition_twh": 1000.0,
        "ordinary_demand_claim_twh_y": 42000.0,
        "aether_dedication_fraction": 0.78,
        "additionality_factor": 0.92,
        "interconnection_factor": 0.82,
        "transmission_siting_factor": 0.86,
        "hourly_matching_factor": 0.88,
        "firm_clean_factor": 0.88,
        "source_keys": "nrel_atb_nuclear_2024;iaea_nuclear_status_2025;iea_geothermal_future_2024;google_kairos_2024;microsoft_constellation_crane_2024;helion_microsoft_fusion_2023",
        "paper_use_rule": "Firm clean-power case; useful for AETHER reliability, but still not proof of 100 Gt deliverability.",
    },
    {
        "scenario": "upper_tail_ai_energy_abundance",
        "display_name": "Upper-tail AI energy abundance",
        "annual_growth_rate": 0.22,
        "starting_annual_addition_twh": 1200.0,
        "ordinary_demand_claim_twh_y": 50000.0,
        "aether_dedication_fraction": 0.92,
        "additionality_factor": 0.98,
        "interconnection_factor": 0.90,
        "transmission_siting_factor": 0.90,
        "hourly_matching_factor": 0.85,
        "firm_clean_factor": 0.85,
        "source_keys": "iea_global_energy_review_2026;nrel_atb_2024_electricity;iea_electricity_2026;iea_energy_ai_2025",
        "paper_use_rule": "Upper-tail feasibility case; the only current case that clears the full 100 Gt 3 GJ/tCO2 gate.",
    },
    {
        "scenario": "nonadditional_grid_failure",
        "display_name": "Nonadditional grid failure",
        "annual_growth_rate": 0.12,
        "starting_annual_addition_twh": BASELINE_ANNUAL_CLEAN_ADDITION_TWH,
        "ordinary_demand_claim_twh_y": 45000.0,
        "aether_dedication_fraction": 0.35,
        "additionality_factor": 0.25,
        "interconnection_factor": 0.70,
        "transmission_siting_factor": 0.72,
        "hourly_matching_factor": 0.62,
        "firm_clean_factor": 0.55,
        "source_keys": "iea_energy_ai_2025;berkeley_lab_queued_up_2025;iea_electricity_2026",
        "paper_use_rule": "Falsification-style case; apparent clean energy is mostly claimed by other demand or cannot be counted as additional.",
    },
]


CONSTRAINTS = [
    {
        "constraint": "annual_clean_generation_growth",
        "question": "Can annual clean additions keep compounding for 20 years?",
        "current_anchor": "IEA reports global electricity generation increased by more than 850 TWh in 2025, with solar PV rising by about 600 TWh.",
        "model_treatment": "Scenario-specific growth rates compound annual additions into 2046 annual clean generation potential.",
        "failure_mode": "Growth slows as supply chains, land, interconnection, storage, and demand competition bind.",
        "source_keys": "iea_global_energy_review_2026;irena_power_costs_2024",
    },
    {
        "constraint": "ordinary_demand_competition",
        "question": "How much new clean power is claimed before AETHER receives any?",
        "current_anchor": "IEA Energy and AI projects data-center electricity consumption roughly doubling to about 945-950 TWh by 2030; ordinary electrification and fossil replacement are much larger.",
        "model_treatment": "Each case subtracts a scenario ordinary-demand claim before applying AETHER dedication.",
        "failure_mode": "AETHER competes with data centers, industry, electrification, hydrogen, and fossil replacement for the same clean supply.",
        "source_keys": "iea_energy_ai_2025",
    },
    {
        "constraint": "interconnection_and_transmission",
        "question": "Can new generation reach AETHER loads?",
        "current_anchor": "Berkeley Lab Queued Up 2025 is used as the interconnection bottleneck anchor.",
        "model_treatment": "Interconnection and transmission/siting factors reduce gross clean supply before crediting AETHER.",
        "failure_mode": "Paper clean power exists in queues or remote regions but does not power removal facilities on time.",
        "source_keys": "berkeley_lab_queued_up_2025",
    },
    {
        "constraint": "hourly_matching_and_firming",
        "question": "Can AETHER run as an industrial load rather than an annual accounting claim?",
        "current_anchor": "IEA Electricity 2026 and NREL ATB provide storage, flexibility, nuclear, wind, solar, and firm-power anchors.",
        "model_treatment": "Hourly matching and firm-clean factors penalize variable-only annual TWh.",
        "failure_mode": "Annual renewable energy is sufficient, but usable AETHER capacity is capped by firming, curtailment, storage duration, and industrial uptime.",
        "source_keys": "iea_electricity_2026;nrel_atb_2024_electricity;nrel_atb_nuclear_2024",
    },
    {
        "constraint": "additionality",
        "question": "Can AETHER count the electricity as additional low-carbon supply?",
        "current_anchor": "The prior clean-power additionality screen distinguishes market-unlocked, dedicated, abundance, and nonadditional-grid cases.",
        "model_treatment": "Additionality factors reduce supply that is not newly built, contractually tied, and low-carbon enough for removal credit.",
        "failure_mode": "AETHER borrows clean energy that would have decarbonized other loads, weakening net climate value.",
        "source_keys": "aether_clean_energy_additionality_model_2026",
    },
]


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    cases: list[dict] = []
    scale_targets: list[dict] = []
    target_levels = [10.0, 30.0, 50.0, 100.0]
    gate_100 = gate_twh(100.0)

    for scenario in SCENARIOS:
        raw_generation = cumulative_generation_from_additions(
            scenario["starting_annual_addition_twh"], scenario["annual_growth_rate"]
        )
        surplus_after_ordinary = max(0.0, raw_generation - scenario["ordinary_demand_claim_twh_y"])
        aether_claimed = surplus_after_ordinary * scenario["aether_dedication_fraction"]
        delivered = (
            aether_claimed
            * scenario["additionality_factor"]
            * scenario["interconnection_factor"]
            * scenario["transmission_siting_factor"]
            * scenario["hourly_matching_factor"]
            * scenario["firm_clean_factor"]
        )
        max_gt = delivered / gate_twh(1.0)
        case_row = {
            **scenario,
            "raw_new_clean_generation_2046_twh_y": round(raw_generation, 3),
            "surplus_after_ordinary_claims_twh_y": round(surplus_after_ordinary, 3),
            "aether_claimed_clean_generation_twh_y": round(aether_claimed, 3),
            "delivered_additional_aether_clean_power_twh_y": round(delivered, 3),
            "delivered_share_of_100gt_3gj_gate": round(delivered / gate_100, 6),
            "max_gtco2_y_at_3gj_balanced_gate": round(max_gt, 3),
            "passes_10gt": max_gt >= 10.0,
            "passes_30gt": max_gt >= 30.0,
            "passes_50gt": max_gt >= 50.0,
            "passes_100gt": max_gt >= 100.0,
        }
        cases.append(case_row)

        for target in target_levels:
            required = gate_twh(target)
            scale_targets.append(
                {
                    "scenario": scenario["scenario"],
                    "target_gtco2_y": target,
                    "required_clean_power_twh_y": round(required, 3),
                    "delivered_additional_aether_clean_power_twh_y": round(delivered, 3),
                    "deliverability_ratio": round(delivered / required, 6),
                    "passes_target": delivered >= required,
                    "shortfall_twh_y": round(max(0.0, required - delivered), 3),
                    "surplus_twh_y": round(max(0.0, delivered - required), 3),
                }
            )

    summary = [
        {
            "metric": "target_100gt_3gj_gate_twh_y",
            "value": round(gate_100, 3),
            "unit": "TWh/year",
            "interpretation": "delivered clean-power gate for 100 GtCO2/year at 3 GJ/tCO2 plus 10% delivery/firming penalty",
        },
        {
            "metric": "best_case_max_gtco2_y",
            "value": max(row["max_gtco2_y_at_3gj_balanced_gate"] for row in cases),
            "unit": "GtCO2/year",
            "interpretation": "largest modeled AETHER scale that clears the delivered clean-power gate",
        },
        {
            "metric": "market_unlocked_max_gtco2_y",
            "value": next(row["max_gtco2_y_at_3gj_balanced_gate"] for row in cases if row["scenario"] == "market_unlocked_texas_style"),
            "unit": "GtCO2/year",
            "interpretation": "market-led case deliverable AETHER scale after ordinary demand and grid/hourly penalties",
        },
        {
            "metric": "dedicated_corridors_max_gtco2_y",
            "value": next(row["max_gtco2_y_at_3gj_balanced_gate"] for row in cases if row["scenario"] == "dedicated_aether_corridors"),
            "unit": "GtCO2/year",
            "interpretation": "dedicated AETHER corridor case deliverable scale",
        },
        {
            "metric": "firm_backbone_max_gtco2_y",
            "value": next(row["max_gtco2_y_at_3gj_balanced_gate"] for row in cases if row["scenario"] == "firm_clean_backbone"),
            "unit": "GtCO2/year",
            "interpretation": "firm clean-power backbone case deliverable scale",
        },
        {
            "metric": "passes_100gt_case_count",
            "value": sum(1 for row in cases if row["passes_100gt"]),
            "unit": "count",
            "interpretation": "number of cases clearing the 100 GtCO2/year 3 GJ/tCO2 delivered clean-power gate",
        },
        {
            "metric": "passes_50gt_case_count",
            "value": sum(1 for row in cases if row["passes_50gt"]),
            "unit": "count",
            "interpretation": "number of cases clearing the 50 GtCO2/year 3 GJ/tCO2 delivered clean-power gate",
        },
    ]

    write_csv(TABLE_DIR / "aether_clean_power_deliverability_cases.csv", cases)
    write_csv(TABLE_DIR / "aether_clean_power_deliverability_scale_targets.csv", scale_targets)
    write_csv(TABLE_DIR / "aether_clean_power_deliverability_constraints.csv", CONSTRAINTS)
    write_csv(TABLE_DIR / "aether_clean_power_deliverability_summary.csv", summary)


if __name__ == "__main__":
    main()

