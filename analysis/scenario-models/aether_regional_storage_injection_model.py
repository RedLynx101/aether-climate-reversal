"""AETHER regional storage and injection-corridor screen.

This model turns the previous storage-lifecycle result into a first regional
deployment screen. It is not a reservoir simulator. It asks how much geologic
storage throughput would have to be assigned to regional corridors, how many
injection wells that implies under simple productivity cases, and which parts
are source-backed versus scenario placeholders.
"""

from __future__ import annotations

from dataclasses import dataclass
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analysis" / "tables"
OUT.mkdir(parents=True, exist_ok=True)

USGS_US_STORAGE_GT = 3000.0
USGS_GULF_SHARE = 0.59
GEOLOGIC_TARGET_GT_Y = 54.0
CORRIDOR_WELL_EQUIVALENTS = 50.0


@dataclass(frozen=True)
class StorageRegion:
    region_id: str
    region_name: str
    evidence_class: str
    proxy_capacity_gtco2: float
    assigned_injection_gtco2_y: float
    pressure_management_multiplier: float
    source_distance_index_1_low_5_high: int
    permit_complexity_index_1_low_5_high: int
    regulatory_basis: str
    primary_source_keys: str
    note: str


def storage_regions() -> list[StorageRegion]:
    gulf_capacity = USGS_US_STORAGE_GT * USGS_GULF_SHARE
    other_us_capacity = USGS_US_STORAGE_GT - gulf_capacity
    return [
        StorageRegion(
            "us_gulf_coast_coastal_plains",
            "U.S. Gulf Coast / Coastal Plains",
            "source-backed U.S. capacity anchor; AETHER allocation scenario",
            gulf_capacity,
            16.0,
            1.40,
            2,
            5,
            "EPA Class VI individual well permits plus state primacy where applicable",
            "usgs_circular_1386_geologic_storage;epa_class_vi_wells_2026;epa_current_class_vi_projects_2026",
            "USGS reports the Gulf Coast area represents 59% of assessed U.S. storage capacity; allocation is a scenario stress test, not a siting plan.",
        ),
        StorageRegion(
            "other_us_basins",
            "Other U.S. assessed basins",
            "source-backed U.S. capacity anchor; AETHER allocation scenario",
            other_us_capacity,
            8.0,
            1.30,
            3,
            5,
            "EPA Class VI individual well permits plus state primacy where applicable",
            "usgs_circular_1386_geologic_storage;netl_carbon_storage_atlas_v_2015;epa_class_vi_wells_2026;epa_current_class_vi_projects_2026",
            "Represents the non-Gulf remainder of the USGS 36-basin assessment; real allocation requires basin and pore-space data.",
        ),
        StorageRegion(
            "north_sea_northwest_europe",
            "North Sea / Northwest Europe",
            "scenario placeholder using global storage literature; needs regional source upgrade",
            200.0,
            5.0,
            1.25,
            2,
            4,
            "country-specific CCS, offshore, and marine permitting",
            "ipcc_ar6_wg3_ch6_ccs_storage",
            "Included as a storage-province archetype because industrial CO2 storage planning is active; capacity proxy is not yet source-backed in this repo.",
        ),
        StorageRegion(
            "middle_east_north_africa",
            "Middle East / North Africa storage provinces",
            "scenario placeholder using global storage literature; needs regional source upgrade",
            500.0,
            8.0,
            1.20,
            3,
            3,
            "country-specific storage, hydrocarbon-field, saline-basin, and water rules",
            "ipcc_ar6_wg3_ch6_ccs_storage",
            "Large sedimentary basins are plausible in the global screen, but this row is not a paper-ready regional estimate.",
        ),
        StorageRegion(
            "east_south_asia_industrial_basins",
            "East and South Asia industrial basins",
            "scenario placeholder using global storage literature; needs regional source upgrade",
            600.0,
            9.0,
            1.45,
            4,
            4,
            "country-specific storage, land, water, and industrial-siting rules",
            "ipcc_ar6_wg3_ch6_ccs_storage",
            "High industrial demand and dense siting create routing and public-consent constraints; capacity proxy needs source-backed upgrade.",
        ),
        StorageRegion(
            "australia_high_storage_basins",
            "Australia and other high-storage basins",
            "scenario placeholder using global storage literature; needs regional source upgrade",
            350.0,
            4.0,
            1.15,
            3,
            3,
            "country-specific CCS, land, water, and offshore permitting",
            "ipcc_ar6_wg3_ch6_ccs_storage",
            "Represents lower-density storage opportunities with potentially easier colocation but long-distance logistics.",
        ),
        StorageRegion(
            "other_global_saline_basins",
            "Other global saline-basin corridors",
            "scenario placeholder using global storage literature; needs regional source upgrade",
            350.0,
            4.0,
            1.35,
            5,
            4,
            "country-specific storage, land, indigenous rights, and public-trust rules",
            "ipcc_ar6_wg3_ch6_ccs_storage",
            "Remainder bucket for the first screen; must be replaced by a basin-level dataset before publication claims.",
        ),
    ]


def allocation_rows(regions: list[StorageRegion]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for region in regions:
        one_mt_pressure_adjusted_wells = (
            region.assigned_injection_gtco2_y * 1000.0 * region.pressure_management_multiplier
        )
        rows.append(
            {
                "region_id": region.region_id,
                "region_name": region.region_name,
                "evidence_class": region.evidence_class,
                "proxy_capacity_gtco2": region.proxy_capacity_gtco2,
                "assigned_injection_gtco2_y": region.assigned_injection_gtco2_y,
                "capacity_years_at_assigned_rate": region.proxy_capacity_gtco2
                / region.assigned_injection_gtco2_y,
                "share_of_geologic_target": region.assigned_injection_gtco2_y
                / GEOLOGIC_TARGET_GT_Y,
                "pressure_management_multiplier": region.pressure_management_multiplier,
                "one_mt_y_pressure_adjusted_well_equivalents": one_mt_pressure_adjusted_wells,
                "fifty_well_corridor_equivalents_at_1mt_y": one_mt_pressure_adjusted_wells
                / CORRIDOR_WELL_EQUIVALENTS,
                "source_distance_index_1_low_5_high": region.source_distance_index_1_low_5_high,
                "permit_complexity_index_1_low_5_high": region.permit_complexity_index_1_low_5_high,
                "regulatory_basis": region.regulatory_basis,
                "primary_source_keys": region.primary_source_keys,
                "model_note": region.note,
            }
        )
    return rows


def corridor_rows(regions: list[StorageRegion]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for region in regions:
        for productivity in [0.25, 0.5, 1.0, 2.0]:
            required_wells = (
                region.assigned_injection_gtco2_y
                * 1000.0
                * region.pressure_management_multiplier
                / productivity
            )
            is_us = region.region_id in {
                "us_gulf_coast_coastal_plains",
                "other_us_basins",
            }
            rows.append(
                {
                    "region_id": region.region_id,
                    "region_name": region.region_name,
                    "well_productivity_mtco2_y": productivity,
                    "assigned_injection_mtco2_y": region.assigned_injection_gtco2_y
                    * 1000.0,
                    "pressure_management_multiplier": region.pressure_management_multiplier,
                    "required_injection_wells": required_wells,
                    "fifty_well_corridor_equivalents": required_wells
                    / CORRIDOR_WELL_EQUIVALENTS,
                    "us_class_vi_individual_well_permit_equivalents": required_wells
                    if is_us
                    else "",
                    "regulatory_basis": region.regulatory_basis,
                    "primary_source_keys": region.primary_source_keys,
                }
            )
    return rows


def summary_rows(regions: list[StorageRegion]) -> list[dict[str, object]]:
    allocation = allocation_rows(regions)
    corridors = corridor_rows(regions)
    total_proxy_capacity = sum(r.proxy_capacity_gtco2 for r in regions)
    source_backed_us_capacity = USGS_US_STORAGE_GT
    us_assigned = sum(
        r.assigned_injection_gtco2_y
        for r in regions
        if r.region_id in {"us_gulf_coast_coastal_plains", "other_us_basins"}
    )
    us_one_mt_wells = sum(
        row["required_injection_wells"]
        for row in corridors
        if row["well_productivity_mtco2_y"] == 1.0
        and row["region_id"] in {"us_gulf_coast_coastal_plains", "other_us_basins"}
    )
    total_one_mt_wells = sum(
        row["required_injection_wells"]
        for row in corridors
        if row["well_productivity_mtco2_y"] == 1.0
    )
    total_quarter_mt_wells = sum(
        row["required_injection_wells"]
        for row in corridors
        if row["well_productivity_mtco2_y"] == 0.25
    )
    total_two_mt_wells = sum(
        row["required_injection_wells"]
        for row in corridors
        if row["well_productivity_mtco2_y"] == 2.0
    )
    return [
        {
            "scenario": "aether_v0_21_regional_storage_injection_screen",
            "geologic_storage_target_gtco2_y": GEOLOGIC_TARGET_GT_Y,
            "total_proxy_capacity_gtco2": total_proxy_capacity,
            "source_backed_us_storage_capacity_gtco2": source_backed_us_capacity,
            "source_backed_us_capacity_years_at_54gt_y": source_backed_us_capacity
            / GEOLOGIC_TARGET_GT_Y,
            "scenario_proxy_capacity_years_at_54gt_y": total_proxy_capacity
            / GEOLOGIC_TARGET_GT_Y,
            "us_assigned_injection_gtco2_y": us_assigned,
            "us_share_of_geologic_target": us_assigned / GEOLOGIC_TARGET_GT_Y,
            "us_class_vi_permit_equivalents_at_1mt_y": us_one_mt_wells,
            "total_pressure_adjusted_wells_at_0_25mt_y": total_quarter_mt_wells,
            "total_pressure_adjusted_wells_at_1mt_y": total_one_mt_wells,
            "total_pressure_adjusted_wells_at_2mt_y": total_two_mt_wells,
            "total_fifty_well_corridors_at_1mt_y": total_one_mt_wells
            / CORRIDOR_WELL_EQUIVALENTS,
            "regions_count": len(regions),
            "source_backed_capacity_rows": sum(
                1 for row in allocation if row["evidence_class"].startswith("source-backed")
            ),
            "scenario_placeholder_capacity_rows": sum(
                1
                for row in allocation
                if row["evidence_class"].startswith("scenario placeholder")
            ),
            "interpretation": "The U.S. capacity anchor is large enough to matter, but AETHER-scale injection is a corridor, well, pressure-management, permitting, and public-legitimacy problem, not just a pore-volume problem.",
        }
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
    regions = storage_regions()
    write_csv(OUT / "aether_regional_storage_allocation.csv", allocation_rows(regions))
    write_csv(
        OUT / "aether_injection_corridor_requirements.csv", corridor_rows(regions)
    )
    write_csv(OUT / "aether_regional_storage_summary.csv", summary_rows(regions))


if __name__ == "__main__":
    main()

