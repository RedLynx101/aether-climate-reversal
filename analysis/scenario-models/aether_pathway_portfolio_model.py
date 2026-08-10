from __future__ import annotations

from dataclasses import dataclass
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analysis" / "tables"
OUT.mkdir(parents=True, exist_ok=True)

TWH_PER_GJ_PER_TON_FOR_1_GT = 277.77777777777777
HOURS_PER_YEAR = 8760
TARGET_GTCO2_Y = 100.0


@dataclass(frozen=True)
class Pathway:
    key: str
    display_name: str
    category: str
    storage_form: str
    storage_duration: str
    trl: str
    ipcc_cost_low_usd_t: float | None
    ipcc_cost_high_usd_t: float | None
    assessed_central_potential_gt_y: float
    assessed_high_potential_gt_y: float
    aether_allocation_gt_y: float
    aether_optimized_cost_usd_t: float
    aether_optimized_energy_gj_t: float
    material_t_per_tco2: float
    source_key: str
    bottleneck: str


def pathways() -> list[Pathway]:
    return [
        Pathway(
            "daccs_geologic",
            "DACCS with geologic storage",
            "chemical/geologic",
            "compressed or supercritical CO2 in geologic reservoirs",
            "10,000+ years if storage is selected, operated, and monitored well",
            "medium",
            100,
            300,
            20,
            40,
            40,
            75,
            3.0,
            1.0,
            "ipcc_ar6_wg3_technical_summary_cdr",
            "low-carbon energy, sorbents/solvents, contactor scale, compression, storage permitting, injection rates, MRV",
        ),
        Pathway(
            "enhanced_weathering",
            "Enhanced weathering and surficial mineralization",
            "geochemical",
            "bicarbonate/carbonate in soils, rivers, and ocean system",
            "centuries to millennia if alkalinity reaches durable reservoirs",
            "low",
            50,
            200,
            3,
            20,
            20,
            75,
            1.2,
            2.5,
            "ipcc_ar6_wg3_technical_summary_cdr",
            "mining, grinding, transport, trace metals, dissolution kinetics, agricultural logistics, MRV of delivered alkalinity",
        ),
        Pathway(
            "ocean_alkalinity_enhancement",
            "Ocean alkalinity enhancement",
            "ocean/geochemical",
            "dissolved bicarbonate and carbonate alkalinity",
            "centuries to millennia if chemistry and circulation behave as intended",
            "low",
            40,
            500,
            1,
            15,
            15,
            100,
            1.8,
            2.0,
            "national_academies_ocean_cdr_2021",
            "marine ecology, alkalinity sourcing, mineral dissolution, monitoring, public legitimacy, international ocean governance",
        ),
        Pathway(
            "beccs",
            "BECCS",
            "biomass/geologic",
            "biogenic CO2 in geologic reservoirs",
            "10,000+ years for stored CO2; biomass supply creates lifecycle uncertainty",
            "medium-low",
            15,
            400,
            5,
            11,
            10,
            90,
            0.5,
            1.5,
            "ipcc_ar6_wg3_technical_summary_cdr",
            "land, water, biodiversity, fertilizer, biomass logistics, capture rate, storage access, lifecycle accounting",
        ),
        Pathway(
            "biochar",
            "Biochar",
            "biomass/soil-product",
            "stable aromatic carbon in soils or materials",
            "decades to centuries; fraction depends on feedstock and pyrolysis conditions",
            "medium",
            10,
            345,
            3,
            6.6,
            6,
            80,
            0.5,
            3.0,
            "ipcc_ar6_wg3_technical_summary_cdr",
            "sustainable biomass, soil response, permanence distribution, particulate emissions, credit quality, competing biomass uses",
        ),
        Pathway(
            "afforestation_reforestation",
            "Afforestation and reforestation",
            "land biological",
            "living biomass and soils",
            "decades to centuries but vulnerable to fire, drought, pests, and land-use reversal",
            "high",
            0,
            240,
            5,
            10,
            5,
            60,
            0.1,
            0.0,
            "ipcc_ar6_wg3_technical_summary_cdr",
            "land competition, food, biodiversity, permanence, wildfire, governance of reversal risk",
        ),
        Pathway(
            "direct_ocean_capture",
            "Direct ocean capture and electrochemical mCDR",
            "ocean/electrochemical",
            "CO2 sent to geologic storage or converted to durable carbonate species",
            "varies by storage route; geologic storage can be very durable",
            "low",
            150,
            500,
            0.5,
            5,
            4,
            180,
            6.0,
            0.0,
            "national_academies_ocean_cdr_2021",
            "electricity, membranes/electrodes, acid/base handling, seawater throughput, brine chemistry, MRV, ocean governance",
        ),
    ]


def allocation_rows(pathway_list: list[Pathway]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for p in pathway_list:
        annual_cost_trillion = p.aether_allocation_gt_y * p.aether_optimized_cost_usd_t / 1000
        annual_energy_twh = p.aether_allocation_gt_y * p.aether_optimized_energy_gj_t * TWH_PER_GJ_PER_TON_FOR_1_GT
        average_power_tw = annual_energy_twh / HOURS_PER_YEAR
        material_gt_y = p.aether_allocation_gt_y * p.material_t_per_tco2
        rows.append({
            "pathway": p.key,
            "display_name": p.display_name,
            "category": p.category,
            "storage_form": p.storage_form,
            "storage_duration": p.storage_duration,
            "technology_readiness": p.trl,
            "ipcc_or_assessment_cost_low_usd_tco2": p.ipcc_cost_low_usd_t if p.ipcc_cost_low_usd_t is not None else "",
            "ipcc_or_assessment_cost_high_usd_tco2": p.ipcc_cost_high_usd_t if p.ipcc_cost_high_usd_t is not None else "",
            "assessed_central_potential_gtco2_y": p.assessed_central_potential_gt_y,
            "assessed_high_potential_gtco2_y": p.assessed_high_potential_gt_y,
            "aether_optimized_allocation_gtco2_y": p.aether_allocation_gt_y,
            "aether_optimized_cost_usd_tco2_assumption": p.aether_optimized_cost_usd_t,
            "aether_optimized_energy_gj_tco2_assumption": p.aether_optimized_energy_gj_t,
            "annual_cost_trillion_usd_y": annual_cost_trillion,
            "annual_energy_twh_y": annual_energy_twh,
            "average_power_tw": average_power_tw,
            "material_or_feedstock_gt_y_indicator": material_gt_y,
            "source_key": p.source_key,
            "primary_bottleneck": p.bottleneck,
        })
    return rows


def summary_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    total_allocation = sum(float(r["aether_optimized_allocation_gtco2_y"]) for r in rows)
    total_assessed_central = sum(float(r["assessed_central_potential_gtco2_y"]) for r in rows)
    total_assessed_high = sum(float(r["assessed_high_potential_gtco2_y"]) for r in rows)
    total_cost = sum(float(r["annual_cost_trillion_usd_y"]) for r in rows)
    total_energy = sum(float(r["annual_energy_twh_y"]) for r in rows)
    total_power = total_energy / HOURS_PER_YEAR
    weighted_cost = total_cost * 1000 / total_allocation
    weighted_energy = total_energy / (total_allocation * TWH_PER_GJ_PER_TON_FOR_1_GT)
    return [{
        "scenario": "aether_optimized_100gt_pathway_portfolio",
        "target_gtco2_y": TARGET_GTCO2_Y,
        "allocated_gtco2_y": total_allocation,
        "assessed_central_potential_sum_gtco2_y": total_assessed_central,
        "assessed_high_potential_sum_gtco2_y": total_assessed_high,
        "central_assessment_gap_to_100gt_gtco2_y": TARGET_GTCO2_Y - total_assessed_central,
        "high_assessment_gap_to_100gt_gtco2_y": TARGET_GTCO2_Y - total_assessed_high,
        "annual_cost_trillion_usd_y": total_cost,
        "weighted_average_cost_usd_tco2": weighted_cost,
        "annual_energy_twh_y": total_energy,
        "average_power_tw": total_power,
        "weighted_average_energy_gj_tco2": weighted_energy,
        "interpretation": "100 GtCO2/year requires pushing several pathways toward or beyond optimistic assessment ranges; DACCS and geochemical/ocean pathways carry the bulk of the durable scale.",
    }]


def write_csv(name: str, rows: list[dict[str, object]]) -> None:
    path = OUT / name
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {path}")


def main() -> None:
    p = pathways()
    rows = allocation_rows(p)
    write_csv("aether_pathway_portfolio_allocation.csv", rows)
    write_csv("aether_pathway_portfolio_summary.csv", summary_rows(rows))


if __name__ == "__main__":
    main()
