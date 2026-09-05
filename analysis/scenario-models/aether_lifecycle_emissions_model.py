from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TABLE_DIR = ROOT / "analysis" / "tables"

PORTFOLIO = TABLE_DIR / "aether_pathway_portfolio_allocation.csv"
STORAGE = TABLE_DIR / "aether_storage_lifecycle_routes.csv"
MRV = TABLE_DIR / "aether_mrv_credit_integrity_by_pathway.csv"

ASSUMPTIONS_OUT = TABLE_DIR / "aether_lifecycle_emissions_assumptions.csv"
BY_PATHWAY_OUT = TABLE_DIR / "aether_lifecycle_emissions_by_pathway.csv"
SUMMARY_OUT = TABLE_DIR / "aether_lifecycle_emissions_summary.csv"

MWH_PER_GJ = 0.2777777777777778

POWER_CASES = [
    {
        "power_case": "near_zero_clean_power",
        "power_emissions_kgco2_mwh": 5.0,
        "interpretation": "Dedicated very-low-carbon power with residual construction, backup, and balancing emissions.",
    },
    {
        "power_case": "low_carbon_mixed_power",
        "power_emissions_kgco2_mwh": 25.0,
        "interpretation": "Low-carbon but not zero-carbon electricity after firming, transmission, curtailment, and backup are counted.",
    },
    {
        "power_case": "grid_leakage_case",
        "power_emissions_kgco2_mwh": 100.0,
        "interpretation": "A warning case where AETHER pulls from an incompletely decarbonized grid or displaces clean power from other uses.",
    },
    {
        "power_case": "fossil_contaminated_case",
        "power_emissions_kgco2_mwh": 250.0,
        "interpretation": "Disqualifying stress test: removal powered by materially fossil-contaminated energy.",
    },
]

PATHWAY_LCA = {
    "daccs_geologic": {
        "non_energy_embodied_tco2e_tco2": 0.040,
        "media_replacement_tco2e_tco2": 0.010,
        "transport_storage_tco2e_tco2": 0.015,
        "decommissioning_tco2e_tco2": 0.003,
        "source_keys": "wri_scaling_dac_impacts_2024;worldsteel_figures_2025;usgs_mcs_2025_cement;epa_subpart_rr_mrv_2026",
        "evidence_class": "scenario_lca_placeholder",
        "note": "DACCS has observable storage but heavy plant, sorbent, compression, transport, and wellfield infrastructure burdens.",
    },
    "enhanced_weathering": {
        "non_energy_embodied_tco2e_tco2": 0.070,
        "media_replacement_tco2e_tco2": 0.000,
        "transport_storage_tco2e_tco2": 0.060,
        "decommissioning_tco2e_tco2": 0.002,
        "source_keys": "ipcc_ar6_wg3_technical_summary_cdr;iea_critical_minerals_outlook_2025",
        "evidence_class": "scenario_lca_placeholder",
        "note": "Mining, grinding, transport, spreading, monitoring, and trace-material handling dominate the placeholder burden.",
    },
    "ocean_alkalinity_enhancement": {
        "non_energy_embodied_tco2e_tco2": 0.080,
        "media_replacement_tco2e_tco2": 0.000,
        "transport_storage_tco2e_tco2": 0.050,
        "decommissioning_tco2e_tco2": 0.003,
        "source_keys": "national_academies_ocean_cdr_2022;ipcc_ar6_wg3_technical_summary_cdr",
        "evidence_class": "scenario_lca_placeholder",
        "note": "Alkalinity production, transport, coastal operations, and ecological monitoring are represented as provisional burdens.",
    },
    "beccs": {
        "non_energy_embodied_tco2e_tco2": 0.130,
        "media_replacement_tco2e_tco2": 0.000,
        "transport_storage_tco2e_tco2": 0.050,
        "decommissioning_tco2e_tco2": 0.004,
        "source_keys": "ipcc_ar6_wg3_technical_summary_cdr;epa_subpart_rr_mrv_2026",
        "evidence_class": "scenario_lca_placeholder",
        "note": "Biomass supply, land-use accounting, fertilizer, transport, capture, and storage infrastructure can materially reduce net credit.",
    },
    "biochar": {
        "non_energy_embodied_tco2e_tco2": 0.070,
        "media_replacement_tco2e_tco2": 0.000,
        "transport_storage_tco2e_tco2": 0.030,
        "decommissioning_tco2e_tco2": 0.002,
        "source_keys": "state_of_cdr_2026;eu_crcf_2024;oxford_offsetting_principles_2024",
        "evidence_class": "scenario_lca_placeholder",
        "note": "Feedstock collection, pyrolysis energy, transport, and product fate are represented as a provisional LCA burden.",
    },
    "afforestation_reforestation": {
        "non_energy_embodied_tco2e_tco2": 0.040,
        "media_replacement_tco2e_tco2": 0.000,
        "transport_storage_tco2e_tco2": 0.010,
        "decommissioning_tco2e_tco2": 0.001,
        "source_keys": "ipcc_ar6_wg3_technical_summary_cdr;state_of_cdr_2026",
        "evidence_class": "scenario_lca_placeholder",
        "note": "Nursery, planting, monitoring, and land-management emissions are small relative to permanence and counterfactual risk.",
    },
    "direct_ocean_capture": {
        "non_energy_embodied_tco2e_tco2": 0.070,
        "media_replacement_tco2e_tco2": 0.030,
        "transport_storage_tco2e_tco2": 0.050,
        "decommissioning_tco2e_tco2": 0.004,
        "source_keys": "national_academies_ocean_cdr_2022;wri_scaling_dac_impacts_2024",
        "evidence_class": "scenario_lca_placeholder",
        "note": "Electrochemical equipment, membranes, coastal infrastructure, acid/base handling, and final storage are provisional LCA burdens.",
    },
}


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


def account_retention_and_lifecycle(
    gross_gtco2_y: float,
    retained_fraction: float,
    lifecycle_emissions_gtco2e_y: float,
) -> tuple[float, float]:
    """Separate retained physical CO2 from the lifecycle CO2e accounting debit."""
    if gross_gtco2_y < 0.0 or lifecycle_emissions_gtco2e_y < 0.0:
        raise ValueError("Gross removal and lifecycle emissions must be non-negative")
    if not 0.0 <= retained_fraction <= 1.0:
        raise ValueError("Retained fraction must be between zero and one")
    physically_retained = gross_gtco2_y * retained_fraction
    return physically_retained, physically_retained - lifecycle_emissions_gtco2e_y


def gross_required_for_positive_net(
    gross_gtco2_y: float, net_gtco2e_y: float, target_gtco2e_y: float = 100.0
) -> float | None:
    """Return scaling for a positive net denominator; non-positive net is infeasible."""
    if gross_gtco2_y < 0.0 or target_gtco2e_y < 0.0:
        raise ValueError("Gross removal and target must be non-negative")
    if net_gtco2e_y <= 0.0:
        return None
    return gross_gtco2_y * target_gtco2e_y / net_gtco2e_y


def main() -> None:
    portfolio = {row["pathway"]: row for row in read_csv(PORTFOLIO)}
    storage = {row["pathway"]: row for row in read_csv(STORAGE)}
    mrv = {row["pathway"]: row for row in read_csv(MRV)}

    assumption_rows: list[dict[str, object]] = []
    for pathway, assumption in PATHWAY_LCA.items():
        row = {
            "pathway": pathway,
            "display_name": portfolio[pathway]["display_name"],
            **assumption,
            "total_non_power_lifecycle_tco2e_tco2": f(
                assumption["non_energy_embodied_tco2e_tco2"]
                + assumption["media_replacement_tco2e_tco2"]
                + assumption["transport_storage_tco2e_tco2"]
                + assumption["decommissioning_tco2e_tco2"],
                5,
            ),
            "use_rule": "Screening LCA placeholder; replace with pathway-specific LCA datasets before publication-grade net-removal claims.",
        }
        assumption_rows.append(row)

    by_pathway_rows: list[dict[str, object]] = []
    for power_case in POWER_CASES:
        kg_mwh = power_case["power_emissions_kgco2_mwh"]
        for pathway, assumption in PATHWAY_LCA.items():
            p = portfolio[pathway]
            s = storage[pathway]
            m = mrv[pathway]
            gross = float(p["aether_optimized_allocation_gtco2_y"])
            capture_energy_gj_t = float(p["aether_optimized_energy_gj_tco2_assumption"])
            storage_energy_gj_t = float(s["storage_energy_penalty_gj_tco2"])
            total_energy_gj_t = float(s["total_energy_with_storage_penalty_gj_tco2"])
            operational_tco2e_tco2 = total_energy_gj_t * MWH_PER_GJ * kg_mwh / 1000.0
            non_power_lca = (
                assumption["non_energy_embodied_tco2e_tco2"]
                + assumption["media_replacement_tco2e_tco2"]
                + assumption["transport_storage_tco2e_tco2"]
                + assumption["decommissioning_tco2e_tco2"]
            )
            total_lca_tco2e_tco2 = operational_tco2e_tco2 + non_power_lca
            lifecycle_emissions_gt = gross * total_lca_tco2e_tco2
            retained_fraction = float(s["retained_fraction_after_100y"])
            physically_retained, net_after_retention_minus_lifecycle = (
                account_retention_and_lifecycle(
                    gross, retained_fraction, lifecycle_emissions_gt
                )
            )
            mrv_multiplier = float(m["mrv_credit_multiplier_after_buffers"])
            creditable_after_lca_mrv = (
                max(net_after_retention_minus_lifecycle, 0.0) * mrv_multiplier
            )

            by_pathway_rows.append({
                "power_case": power_case["power_case"],
                "power_emissions_kgco2_mwh": f(kg_mwh, 3),
                "pathway": pathway,
                "display_name": p["display_name"],
                "gross_gtco2_y": f(gross, 6),
                "capture_energy_gj_tco2": f(capture_energy_gj_t, 6),
                "storage_energy_penalty_gj_tco2": f(storage_energy_gj_t, 6),
                "total_energy_gj_tco2": f(total_energy_gj_t, 6),
                "operational_power_emissions_tco2e_tco2": f(operational_tco2e_tco2, 6),
                "non_power_lifecycle_tco2e_tco2": f(non_power_lca, 6),
                "total_lifecycle_emissions_tco2e_tco2": f(total_lca_tco2e_tco2, 6),
                "annual_lifecycle_emissions_gtco2e_y": f(lifecycle_emissions_gt, 6),
                "retained_fraction_after_100y": f(retained_fraction, 6),
                "physically_retained_after_100y_gtco2_y": f(physically_retained, 6),
                "net_after_retention_minus_lifecycle_emissions_gtco2e_y": f(
                    net_after_retention_minus_lifecycle, 6
                ),
                "mrv_credit_multiplier_after_buffers": f(mrv_multiplier, 6),
                "creditable_after_lca_and_mrv_gtco2e_y": f(creditable_after_lca_mrv, 6),
                "source_keys": assumption["source_keys"],
                "evidence_class": assumption["evidence_class"],
                "accounting_boundary_note": "Physical retention is applied only to gross captured CO2; lifecycle CO2e is then debited in a scalar accounting screen. This is not a time- or species-resolved climate flow.",
            })

    summary_rows: list[dict[str, object]] = []
    for power_case in POWER_CASES:
        rows = [row for row in by_pathway_rows if row["power_case"] == power_case["power_case"]]
        gross = sum(float(row["gross_gtco2_y"]) for row in rows)
        emissions = sum(float(row["annual_lifecycle_emissions_gtco2e_y"]) for row in rows)
        physically_retained = sum(
            float(row["physically_retained_after_100y_gtco2_y"]) for row in rows
        )
        net_accounting = sum(
            float(row["net_after_retention_minus_lifecycle_emissions_gtco2e_y"])
            for row in rows
        )
        creditable = sum(float(row["creditable_after_lca_and_mrv_gtco2e_y"]) for row in rows)
        gross_required_creditable = gross_required_for_positive_net(gross, creditable)
        gross_required_net = gross_required_for_positive_net(gross, net_accounting)
        summary_rows.append({
            "power_case": power_case["power_case"],
            "power_emissions_kgco2_mwh": f(power_case["power_emissions_kgco2_mwh"], 3),
            "gross_portfolio_gtco2_y": f(gross, 6),
            "annual_lifecycle_emissions_gtco2e_y": f(emissions, 6),
            "lifecycle_emissions_fraction_of_gross": f(emissions / gross, 6),
            "physically_retained_after_100y_gtco2_y": f(physically_retained, 6),
            "net_after_retention_minus_lifecycle_emissions_gtco2e_y": f(net_accounting, 6),
            "creditable_after_lca_and_mrv_gtco2e_y": f(creditable, 6),
            "gross_required_for_100gt_net_accounting_gtco2_y": (
                f(gross_required_net, 6) if gross_required_net is not None else ""
            ),
            "gross_required_for_100gt_net_accounting_status": (
                "defined_positive_net" if gross_required_net is not None else "infeasible_nonpositive_net"
            ),
            "gross_required_for_100gt_creditable_after_lca_mrv_gtco2_y": (
                f(gross_required_creditable, 6) if gross_required_creditable is not None else ""
            ),
            "gross_required_for_100gt_creditable_after_lca_mrv_status": (
                "defined_positive_credit" if gross_required_creditable is not None else "infeasible_zero_credit"
            ),
            "interpretation": power_case["interpretation"],
            "accounting_boundary_note": "Retention, lifecycle-emissions accounting, and provisional MRV credit are separate layers. The scalar CO2e subtraction is not a climate-flow simulation.",
        })

    write_csv(ASSUMPTIONS_OUT, assumption_rows)
    write_csv(BY_PATHWAY_OUT, by_pathway_rows)
    write_csv(SUMMARY_OUT, summary_rows)


if __name__ == "__main__":
    main()

