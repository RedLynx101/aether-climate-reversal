"""AETHER material and industrial supply-chain screen.

This model is a first-pass material pressure test for a 100 GtCO2/year AETHER
system. It separates ordinary structural mass from reactive media, power-system
metals, and CO2 transport materials. The main point is reviewer discipline:
large energy and robot assumptions do not automatically imply enough sorbent,
solvent, steel, cement, copper, pipeline capacity, and chemical logistics.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analysis" / "tables"
OUT.mkdir(parents=True, exist_ok=True)

GLOBAL_STEEL_MT_Y = 1885.0
GLOBAL_CEMENT_MT_Y = 4000.0
GLOBAL_REFINED_COPPER_MT_Y = 27.0
BUILDOUT_YEARS = 20.0

TARGET_GTCO2_Y = 100.0
DACCS_BRANCH_GTCO2_Y = 40.0
GEOLOGIC_BRANCH_GTCO2_Y = 54.0
ALL_AIR_CONTACTOR_AREA_KM2 = 3771.0
DACCS_BRANCH_CONTACTOR_AREA_KM2 = ALL_AIR_CONTACTOR_AREA_KM2 * DACCS_BRANCH_GTCO2_Y / TARGET_GTCO2_Y
POWER_NAMEPLATE_3GJ_BALANCED_TW = 27.5


def mass_from_area(area_km2: float, kg_per_m2: float) -> float:
    """Return total material mass in Mt for a surface-area intensity."""
    return area_km2 * 1_000_000.0 * kg_per_m2 / 1_000_000_000.0


def annualized(total_mt: float) -> float:
    return total_mt / BUILDOUT_YEARS


def requirement_row(
    row_id: str,
    material: str,
    pressure_class: str,
    scenario: str,
    quantity_basis: str,
    total_mt: float | str,
    annual_mt_y: float,
    comparator_name: str,
    comparator_mt_y: float,
    evidence_class: str,
    source_keys: str,
    interpretation: str,
    figure_label: str,
) -> dict[str, object]:
    share = annual_mt_y / comparator_mt_y * 100.0 if comparator_mt_y else ""
    return {
        "row_id": row_id,
        "material_or_system": material,
        "pressure_class": pressure_class,
        "scenario": scenario,
        "quantity_basis": quantity_basis,
        "total_material_mt": total_mt,
        "annualized_or_annual_material_mt_y": annual_mt_y,
        "global_comparator_name": comparator_name,
        "global_comparator_mt_y": comparator_mt_y,
        "share_of_global_comparator_pct": share,
        "evidence_class": evidence_class,
        "source_keys": source_keys,
        "figure_label": figure_label,
        "interpretation": interpretation,
    }


def build_requirements() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    target_mtco2_y = TARGET_GTCO2_Y * 1000.0
    daccs_mtco2_y = DACCS_BRANCH_GTCO2_Y * 1000.0

    for label, intensity in [
        ("legacy_naoh_low", 0.17),
        ("legacy_naoh_high", 0.29),
    ]:
        annual_mt_y = target_mtco2_y * intensity
        rows.append(
            requirement_row(
                label,
                "NaOH-equivalent reactive media makeup",
                "legacy DAC chemistry warning",
                "100 GtCO2/y all-air legacy solvent stress test",
                f"{intensity:.2f} t reactive media per tCO2 captured",
                "annual flow",
                annual_mt_y,
                "world cement production proxy",
                GLOBAL_CEMENT_MT_Y,
                "source-backed critique scaled to AETHER target",
                "chatterjee_huang_2020_unrealistic_dac;usgs_mcs_2025_cement",
                "Legacy high-makeup solvent cases imply bulk-chemical flows larger than today's cement industry.",
                f"Legacy NaOH {intensity:.2f} t/t",
            )
        )

    for label, intensity in [
        ("advanced_media_0_5pct_daccs", 0.005),
        ("advanced_media_2pct_daccs", 0.020),
        ("advanced_media_5pct_daccs", 0.050),
    ]:
        annual_mt_y = daccs_mtco2_y * intensity
        rows.append(
            requirement_row(
                label,
                "Advanced sorbent or solvent replacement",
                "AETHER media requirement",
                "40 GtCO2/y DACCS branch",
                f"{intensity:.3f} t replacement media per tCO2 captured",
                "annual flow",
                annual_mt_y,
                "world cement production proxy",
                GLOBAL_CEMENT_MT_Y,
                "scenario assumption informed by DAC material-risk literature",
                "wri_scaling_dac_impacts_2024;chatterjee_huang_2020_unrealistic_dac;usgs_mcs_2025_cement",
                "The DACCS branch only becomes plausible if media losses are pushed orders of magnitude below legacy critique cases.",
                f"DACCS media {intensity * 100:.1f}%/t",
            )
        )

    for label, area, kg_m2, figure_label in [
        ("daccs_contactor_steel_moderate", DACCS_BRANCH_CONTACTOR_AREA_KM2, 100.0, "DACCS contactor steel"),
        ("all_air_contactor_steel_moderate", ALL_AIR_CONTACTOR_AREA_KM2, 100.0, "All-air contactor steel"),
    ]:
        total_mt = mass_from_area(area, kg_m2)
        rows.append(
            requirement_row(
                label,
                "Contactor structural steel",
                "structural material",
                "moderate contactor-frame case",
                f"{kg_m2:.0f} kg steel per m2 contactor face area",
                total_mt,
                annualized(total_mt),
                "world crude steel production",
                GLOBAL_STEEL_MT_Y,
                "scenario assumption with source-backed global comparator",
                "worldsteel_figures_2025;national_academies_dac_ch5_2018;wri_scaling_dac_impacts_2024",
                "Structural contactor steel is large but not the dominant global-material impossibility if designs stay light and modular.",
                figure_label,
            )
        )

    for label, area, kg_m2 in [
        ("daccs_foundation_cement_moderate", DACCS_BRANCH_CONTACTOR_AREA_KM2, 60.0),
        ("all_air_foundation_cement_moderate", ALL_AIR_CONTACTOR_AREA_KM2, 60.0),
    ]:
        total_mt = mass_from_area(area, kg_m2)
        rows.append(
            requirement_row(
                label,
                "Cement-equivalent foundations",
                "structural material",
                "moderate contactor-foundation case",
                f"{kg_m2:.0f} kg cement-equivalent per m2 contactor face area",
                total_mt,
                annualized(total_mt),
                "world cement production",
                GLOBAL_CEMENT_MT_Y,
                "scenario assumption with source-backed global comparator",
                "usgs_mcs_2025_cement;wri_scaling_dac_impacts_2024",
                "Cement demand is not the first-order limit in this simple screen, but its embodied emissions must be counted.",
                "Contactor cement",
            )
        )

    power_steel_total_mt = POWER_NAMEPLATE_3GJ_BALANCED_TW * 1_000_000.0 * 50.0 / 1_000_000.0
    rows.append(
        requirement_row(
            "power_system_steel_3gj_balanced",
            "Power-system structural steel",
            "power-system material",
            "3 GJ/tCO2 balanced clean-power case",
            "50 t steel per MW nameplate proxy across mixed clean-power buildout",
            power_steel_total_mt,
            annualized(power_steel_total_mt),
            "world crude steel production",
            GLOBAL_STEEL_MT_Y,
            "scenario assumption with source-backed global comparator",
            "worldsteel_figures_2025;nrel_atb_2024_electricity",
            "The power system can dominate structural steel demand more than DAC contactor frames.",
            "Power steel",
        )
    )

    power_copper_total_mt = POWER_NAMEPLATE_3GJ_BALANCED_TW * 1_000_000.0 * 2.0 / 1_000_000.0
    rows.append(
        requirement_row(
            "power_system_copper_3gj_balanced",
            "Power-system copper",
            "critical mineral",
            "3 GJ/tCO2 balanced clean-power case",
            "2 t copper per MW nameplate proxy across generation, grid, and balance-of-system",
            power_copper_total_mt,
            annualized(power_copper_total_mt),
            "world refined copper production proxy",
            GLOBAL_REFINED_COPPER_MT_Y,
            "scenario assumption with IEA critical-minerals context",
            "iea_critical_minerals_outlook_2025",
            "Copper is a serious parallel bottleneck because AETHER would compete with electrification, grids, data centers, and storage.",
            "Power copper",
        )
    )

    pipeline_steel_total_mt = 100_000.0 * 500.0 / 1_000_000.0
    rows.append(
        requirement_row(
            "co2_corridor_pipeline_steel",
            "CO2 corridor pipeline steel",
            "transport material",
            "54 GtCO2/y geologic-storage branch",
            "100,000 km trunk-corridor proxy at 500 t steel per km",
            pipeline_steel_total_mt,
            annualized(pipeline_steel_total_mt),
            "world crude steel production",
            GLOBAL_STEEL_MT_Y,
            "scenario placeholder with source-backed global comparator",
            "worldsteel_figures_2025;netl_carbon_storage_atlas_v_2015",
            "Pipeline steel is not the largest mass in this screen, but routing, land rights, compression, safety, and permitting may dominate.",
            "Pipeline steel",
        )
    )

    return rows


def build_inputs() -> list[dict[str, object]]:
    return [
        {
            "parameter_id": "global_crude_steel_2024_mt_y",
            "value": GLOBAL_STEEL_MT_Y,
            "unit": "Mt/year",
            "evidence_class": "source-backed anchor",
            "source_keys": "worldsteel_figures_2025",
            "note": "World Steel Association 2025 report for 2024 crude steel production.",
        },
        {
            "parameter_id": "global_cement_2024_mt_y",
            "value": GLOBAL_CEMENT_MT_Y,
            "unit": "Mt/year",
            "evidence_class": "source-backed anchor",
            "source_keys": "usgs_mcs_2025_cement",
            "note": "USGS MCS 2025 cement chapter rounded world production.",
        },
        {
            "parameter_id": "global_refined_copper_proxy_mt_y",
            "value": GLOBAL_REFINED_COPPER_MT_Y,
            "unit": "Mt/year",
            "evidence_class": "screening proxy",
            "source_keys": "iea_critical_minerals_outlook_2025",
            "note": "Rounded refined copper market proxy; next version should replace with ICSG/USGS refined production data.",
        },
        {
            "parameter_id": "aether_material_buildout_years",
            "value": BUILDOUT_YEARS,
            "unit": "years",
            "evidence_class": "scenario assumption",
            "source_keys": "aether_model_assumptions_2026",
            "note": "Matches the 2026-2046 AETHER buildout premise.",
        },
    ]


def build_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    by_id = {row["row_id"]: row for row in rows}
    return [
        {
            "summary_id": "legacy_media_is_disqualifying",
            "metric": "legacy NaOH low/high share of cement-production proxy",
            "value": f"{float(by_id['legacy_naoh_low']['share_of_global_comparator_pct']):.1f}% to {float(by_id['legacy_naoh_high']['share_of_global_comparator_pct']):.1f}%",
            "interpretation": "Legacy high-makeup DAC chemistry cannot be the AETHER base case at 100 GtCO2/year.",
        },
        {
            "summary_id": "advanced_media_still_large",
            "metric": "advanced DACCS media replacement at 0.5% to 2.0% of captured CO2",
            "value": f"{by_id['advanced_media_0_5pct_daccs']['annualized_or_annual_material_mt_y']:.0f} to {by_id['advanced_media_2pct_daccs']['annualized_or_annual_material_mt_y']:.0f} Mt/year",
            "interpretation": "Even optimistic media lifetimes create large chemical manufacturing and recycling systems.",
        },
        {
            "summary_id": "power_minerals_are_parallel_constraint",
            "metric": "power-system copper proxy share of current refined copper market",
            "value": f"{float(by_id['power_system_copper_3gj_balanced']['share_of_global_comparator_pct']):.1f}%",
            "interpretation": "Copper, transformers, grid hardware, and interconnection compete with all other electrification demand.",
        },
        {
            "summary_id": "structural_materials_are_big_not_impossible",
            "metric": "power-system steel plus all-air contactor steel annual share of current steel production",
            "value": f"{float(by_id['power_system_steel_3gj_balanced']['share_of_global_comparator_pct']) + float(by_id['all_air_contactor_steel_moderate']['share_of_global_comparator_pct']):.1f}%",
            "interpretation": "Optimized structural mass looks more like a major industrial allocation than a physical impossibility.",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"Cannot write empty CSV: {path}")
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {path}")


def main() -> None:
    requirements = build_requirements()
    write_csv(OUT / "aether_material_supply_chain_inputs.csv", build_inputs())
    write_csv(OUT / "aether_material_supply_chain_requirements.csv", requirements)
    write_csv(OUT / "aether_material_supply_chain_summary.csv", build_summary(requirements))


if __name__ == "__main__":
    main()

