from __future__ import annotations

from dataclasses import dataclass
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analysis" / "tables"
PORTFOLIO = OUT / "aether_pathway_portfolio_allocation.csv"
OUT.mkdir(parents=True, exist_ok=True)

TWH_PER_GJ_PER_TON_FOR_1_GT = 277.77777777777777
SUPERCRITICAL_CO2_DENSITY_KG_M3 = 600.0
DEFAULT_WELL_INJECTION_MT_Y = 1.0


@dataclass(frozen=True)
class StorageRoute:
    pathway: str
    storage_route: str
    storage_region_proxy: str
    storage_resource_proxy_gtco2: float
    terminal_injection_or_processing_capacity_gt_y: float
    storage_energy_penalty_gj_tco2: float
    lifecycle_penalty_fraction: float
    annual_reversal_or_leakage_rate: float
    monitoring_duration_y: int
    one_mt_well_equivalent: bool
    source_key: str
    note: str


def route_assumptions() -> dict[str, StorageRoute]:
    return {
        "daccs_geologic": StorageRoute(
            "daccs_geologic",
            "geologic saline storage",
            "Gulf Coast / high-permeability saline basin archetype",
            3000,
            45,
            0.35,
            0.06,
            0.00001,
            100,
            True,
            "usgs_circular_1386_geologic_storage",
            "Uses USGS/AR6 scale as a resource proxy; actual AETHER siting would be global and pressure-limited.",
        ),
        "enhanced_weathering": StorageRoute(
            "enhanced_weathering",
            "surficial mineralization and dissolved alkalinity",
            "distributed mafic/ultramafic rock and agricultural logistics archetype",
            5000,
            22,
            0.25,
            0.12,
            0.0,
            100,
            False,
            "ipcc_ar6_wg3_technical_summary_cdr",
            "Capacity proxy is an AETHER stress-test assumption; mining, grinding, transport, kinetics, and MRV bind before theoretical rock abundance.",
        ),
        "ocean_alkalinity_enhancement": StorageRoute(
            "ocean_alkalinity_enhancement",
            "ocean alkalinity / dissolved inorganic carbon",
            "coastal alkalinity and monitoring archetype",
            1000,
            15,
            0.35,
            0.15,
            0.0005,
            100,
            False,
            "national_academies_ocean_cdr_2021",
            "Durability is represented as a measurement/reversal haircut, not literal reservoir leakage.",
        ),
        "beccs": StorageRoute(
            "beccs",
            "biogenic CO2 to geologic storage",
            "biomass hub plus nearby geologic storage archetype",
            3000,
            12,
            0.15,
            0.20,
            0.00001,
            100,
            True,
            "ipcc_ar6_wg3_technical_summary_cdr",
            "Lifecycle penalty reflects biomass supply, land, fertilizer, transport, and capture accounting risk.",
        ),
        "biochar": StorageRoute(
            "biochar",
            "biochar in soils or durable materials",
            "distributed biomass and soil/material storage archetype",
            1000,
            7,
            0.10,
            0.18,
            0.0020,
            100,
            False,
            "ipcc_ar6_wg3_technical_summary_cdr",
            "Reversal rate represents heterogeneous permanence, feedstock accounting, and soil/material fate.",
        ),
        "afforestation_reforestation": StorageRoute(
            "afforestation_reforestation",
            "living biomass and soil carbon",
            "land biological storage archetype",
            500,
            5,
            0.05,
            0.25,
            0.0060,
            100,
            False,
            "ipcc_ar6_wg3_technical_summary_cdr",
            "Reversal rate represents fire, drought, pests, land-use reversal, and accounting uncertainty.",
        ),
        "direct_ocean_capture": StorageRoute(
            "direct_ocean_capture",
            "electrochemical capture plus geologic or carbonate storage",
            "coastal electrochemical hub plus storage archetype",
            3000,
            5,
            0.75,
            0.12,
            0.00001,
            100,
            True,
            "national_academies_ocean_cdr_2021",
            "Higher storage-energy penalty reflects seawater handling, acid/base management, compression, and routing.",
        ),
    }


def read_portfolio() -> list[dict[str, str]]:
    with PORTFOLIO.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def account_retention_and_lifecycle(
    gross_gtco2_y: float,
    retained_fraction: float,
    lifecycle_emissions_gtco2e_y: float,
) -> tuple[float, float]:
    """Return physical retention and the separate scalar lifecycle accounting result."""
    if gross_gtco2_y < 0.0 or lifecycle_emissions_gtco2e_y < 0.0:
        raise ValueError("Gross removal and lifecycle emissions must be non-negative")
    if not 0.0 <= retained_fraction <= 1.0:
        raise ValueError("Retained fraction must be between zero and one")
    physically_retained = gross_gtco2_y * retained_fraction
    return physically_retained, physically_retained - lifecycle_emissions_gtco2e_y


def gross_required_for_positive_net(
    gross_gtco2_y: float, net_gtco2e_y: float, target_gtco2e_y: float = 100.0
) -> float | None:
    """Scale gross to a positive net target, or return None for a non-positive denominator."""
    if gross_gtco2_y < 0.0 or target_gtco2e_y < 0.0:
        raise ValueError("Gross removal and target must be non-negative")
    if net_gtco2e_y <= 0.0:
        return None
    return gross_gtco2_y * target_gtco2e_y / net_gtco2e_y


def route_rows() -> list[dict[str, object]]:
    assumptions = route_assumptions()
    rows: list[dict[str, object]] = []
    for portfolio_row in read_portfolio():
        key = portfolio_row["pathway"]
        route = assumptions[key]
        gross = float(portfolio_row["aether_optimized_allocation_gtco2_y"])
        total_energy_gj_t = float(portfolio_row["aether_optimized_energy_gj_tco2_assumption"]) + route.storage_energy_penalty_gj_tco2
        annual_storage_energy_twh = gross * route.storage_energy_penalty_gj_tco2 * TWH_PER_GJ_PER_TON_FOR_1_GT
        retained_100y = (1 - route.annual_reversal_or_leakage_rate) ** route.monitoring_duration_y
        lifecycle_emissions_proxy = gross * route.lifecycle_penalty_fraction
        physically_retained_100y, net_accounting_proxy = account_retention_and_lifecycle(
            gross, retained_100y, lifecycle_emissions_proxy
        )
        gross_required = gross_required_for_positive_net(gross, net_accounting_proxy)
        gross_to_net_multiplier = gross_required / 100.0 if gross_required is not None else ""
        supercritical_volume_km3_y = gross * 1e12 / SUPERCRITICAL_CO2_DENSITY_KG_M3 / 1e9
        one_mt_wells = gross * 1000 / DEFAULT_WELL_INJECTION_MT_Y if route.one_mt_well_equivalent else 0.0
        ten_mt_hubs = gross * 1000 / 10.0
        rows.append({
            "pathway": key,
            "display_name": portfolio_row["display_name"],
            "storage_route": route.storage_route,
            "storage_region_proxy": route.storage_region_proxy,
            "gross_allocation_gtco2_y": gross,
            "storage_resource_proxy_gtco2": route.storage_resource_proxy_gtco2,
            "years_of_resource_at_allocation": route.storage_resource_proxy_gtco2 / gross if gross else "",
            "terminal_injection_or_processing_capacity_gtco2_y": route.terminal_injection_or_processing_capacity_gt_y,
            "capacity_adequacy_ratio": route.terminal_injection_or_processing_capacity_gt_y / gross if gross else "",
            "one_mt_injection_well_equivalents": one_mt_wells,
            "ten_mt_hub_equivalents": ten_mt_hubs,
            "storage_energy_penalty_gj_tco2": route.storage_energy_penalty_gj_tco2,
            "total_energy_with_storage_penalty_gj_tco2": total_energy_gj_t,
            "annual_storage_energy_penalty_twh_y": annual_storage_energy_twh,
            "lifecycle_penalty_fraction": route.lifecycle_penalty_fraction,
            "annual_reversal_or_leakage_rate": route.annual_reversal_or_leakage_rate,
            "retained_fraction_after_100y": retained_100y,
            "physically_retained_after_100y_gtco2_y": physically_retained_100y,
            "lifecycle_emissions_proxy_gtco2e_y": lifecycle_emissions_proxy,
            "net_after_retention_minus_lifecycle_proxy_gtco2e_y": net_accounting_proxy,
            "retention_and_lifecycle_accounting_shortfall_gtco2e_y": gross - net_accounting_proxy,
            "gross_to_net_multiplier_for_same_route": gross_to_net_multiplier,
            "gross_to_net_multiplier_status": (
                "defined_positive_net" if gross_required is not None else "infeasible_nonpositive_net"
            ),
            "supercritical_volume_km3_y_if_geologic": supercritical_volume_km3_y if route.one_mt_well_equivalent else "",
            "source_key": route.source_key,
            "model_note": route.note,
            "accounting_boundary_note": "Physical 100-year retention is calculated before subtracting the provisional lifecycle CO2e proxy. The scalar result is an accounting screen, not a time- or species-resolved climate flow and not an issued credit.",
        })
    return rows


def summary_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    gross = sum(float(r["gross_allocation_gtco2_y"]) for r in rows)
    physically_retained = sum(float(r["physically_retained_after_100y_gtco2_y"]) for r in rows)
    lifecycle_emissions_proxy = sum(float(r["lifecycle_emissions_proxy_gtco2e_y"]) for r in rows)
    net_accounting_proxy = sum(float(r["net_after_retention_minus_lifecycle_proxy_gtco2e_y"]) for r in rows)
    storage_energy = sum(float(r["annual_storage_energy_penalty_twh_y"]) for r in rows)
    base_energy = 56527.77777777778
    one_mt_wells = sum(float(r["one_mt_injection_well_equivalents"]) for r in rows)
    geologic_volume = sum(float(r["supercritical_volume_km3_y_if_geologic"] or 0) for r in rows)
    geologic_gross = sum(float(r["gross_allocation_gtco2_y"]) for r in rows if float(r["one_mt_injection_well_equivalents"]) > 0)
    gross_required = gross_required_for_positive_net(gross, net_accounting_proxy)
    return [{
        "scenario": "aether_v0_7_storage_lifecycle_filter",
        "gross_portfolio_gtco2_y": gross,
        "physically_retained_after_100y_gtco2_y": physically_retained,
        "lifecycle_emissions_proxy_gtco2e_y": lifecycle_emissions_proxy,
        "net_after_retention_minus_lifecycle_proxy_gtco2e_y": net_accounting_proxy,
        "retention_and_lifecycle_accounting_shortfall_gtco2e_y": gross - net_accounting_proxy,
        "gross_required_for_100gt_net_accounting_proxy_at_same_mix_gtco2_y": (
            gross_required if gross_required is not None else ""
        ),
        "gross_required_for_100gt_net_accounting_proxy_status": (
            "defined_positive_net" if gross_required is not None else "infeasible_nonpositive_net"
        ),
        "portfolio_net_accounting_proxy_fraction": net_accounting_proxy / gross,
        "base_portfolio_energy_twh_y": base_energy,
        "additional_storage_lifecycle_energy_twh_y": storage_energy,
        "energy_with_storage_lifecycle_penalty_twh_y": base_energy + storage_energy,
        "average_power_with_storage_lifecycle_penalty_tw": (base_energy + storage_energy) / 8760,
        "one_mt_geologic_injection_well_equivalents": one_mt_wells,
        "geologic_storage_gross_gtco2_y": geologic_gross,
        "geologic_supercritical_volume_km3_y": geologic_volume,
        "interpretation": "At the current portfolio mix, physical 100-year retention is separated from a provisional lifecycle CO2e debit. Their scalar difference is an accounting screen, not a climate-flow calculation or an issued credit; MRV buffers are applied separately.",
    }]


def write_csv(name: str, rows: list[dict[str, object]]) -> None:
    path = OUT / name
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {path}")


def main() -> None:
    rows = route_rows()
    write_csv("aether_storage_lifecycle_routes.csv", rows)
    write_csv("aether_storage_lifecycle_summary.csv", summary_rows(rows))


if __name__ == "__main__":
    main()
