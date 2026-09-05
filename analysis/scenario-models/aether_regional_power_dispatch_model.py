from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TABLE_DIR = ROOT / "analysis" / "tables"
TABLE_DIR.mkdir(parents=True, exist_ok=True)

TWH_PER_GJ_PER_TON_FOR_1_GT = 277.77777777777777
BALANCED_ENERGY_GJ_PER_TCO2 = 3.0
DELIVERY_AND_FIRMING_PENALTY = 0.10
HOURS = list(range(24))


def gate_twh(target_gtco2_y: float, energy_gj_tco2: float = BALANCED_ENERGY_GJ_PER_TCO2) -> float:
    return target_gtco2_y * energy_gj_tco2 * TWH_PER_GJ_PER_TON_FOR_1_GT * (1.0 + DELIVERY_AND_FIRMING_PENALTY)


def normalized(values: list[float]) -> list[float]:
    average = sum(values) / len(values)
    if average <= 0.0:
        return [1.0 for _ in values]
    return [value / average for value in values]


def solar_shape(phase_shift: float) -> list[float]:
    values = []
    for hour in HOURS:
        angle = math.pi * (hour - 6.0 + phase_shift) / 12.0
        values.append(max(0.0, math.sin(angle)) ** 1.55)
    return normalized(values)


def wind_shape(phase_shift: float, strength: float) -> list[float]:
    values = []
    for hour in HOURS:
        daily = strength * math.sin((2.0 * math.pi * (hour - phase_shift)) / 24.0)
        secondary = 0.08 * math.sin((4.0 * math.pi * (hour - phase_shift)) / 24.0)
        values.append(max(0.2, 1.0 + daily + secondary))
    return normalized(values)


REGIONS = [
    {
        "region": "texas_gulf_storage_corridor",
        "display_name": "Texas/Gulf storage corridor",
        "base_clean_generation_twh_y": 15000.0,
        "solar_share": 0.33,
        "wind_share": 0.47,
        "firm_share": 0.20,
        "storage_hours": 8.0,
        "roundtrip_efficiency": 0.86,
        "interconnection_factor": 0.84,
        "transmission_factor": 0.86,
        "additionality_factor": 0.90,
        "colocation_score": 0.88,
        "storage_corridor_score": 0.92,
        "water_and_heat_score": 0.72,
        "aether_allocation_share": 0.18,
        "solar_phase_shift": 0.0,
        "wind_phase_shift": 18.0,
        "wind_strength": 0.28,
        "source_keys": "eia_texas_energy_profile_2024;berkeley_lab_queued_up_2025;netl_carbon_storage_atlas_v_2015",
    },
    {
        "region": "california_west_desert",
        "display_name": "California/West desert grid",
        "base_clean_generation_twh_y": 14000.0,
        "solar_share": 0.58,
        "wind_share": 0.17,
        "firm_share": 0.25,
        "storage_hours": 10.0,
        "roundtrip_efficiency": 0.86,
        "interconnection_factor": 0.80,
        "transmission_factor": 0.82,
        "additionality_factor": 0.84,
        "colocation_score": 0.74,
        "storage_corridor_score": 0.64,
        "water_and_heat_score": 0.62,
        "aether_allocation_share": 0.13,
        "solar_phase_shift": -0.5,
        "wind_phase_shift": 20.0,
        "wind_strength": 0.18,
        "source_keys": "california_energy_commission_2024_tseg;irena_power_costs_2024;nrel_atb_2024_electricity",
    },
    {
        "region": "interior_wind_geothermal",
        "display_name": "Interior wind/geothermal belt",
        "base_clean_generation_twh_y": 13000.0,
        "solar_share": 0.25,
        "wind_share": 0.50,
        "firm_share": 0.25,
        "storage_hours": 12.0,
        "roundtrip_efficiency": 0.84,
        "interconnection_factor": 0.78,
        "transmission_factor": 0.80,
        "additionality_factor": 0.88,
        "colocation_score": 0.78,
        "storage_corridor_score": 0.70,
        "water_and_heat_score": 0.76,
        "aether_allocation_share": 0.14,
        "solar_phase_shift": 0.5,
        "wind_phase_shift": 17.0,
        "wind_strength": 0.33,
        "source_keys": "nrel_atb_land_wind_2024;iea_geothermal_future_2024;berkeley_lab_queued_up_2025",
    },
    {
        "region": "north_africa_middle_east_solar",
        "display_name": "North Africa/Middle East solar",
        "base_clean_generation_twh_y": 19000.0,
        "solar_share": 0.68,
        "wind_share": 0.12,
        "firm_share": 0.20,
        "storage_hours": 12.0,
        "roundtrip_efficiency": 0.84,
        "interconnection_factor": 0.74,
        "transmission_factor": 0.76,
        "additionality_factor": 0.90,
        "colocation_score": 0.70,
        "storage_corridor_score": 0.62,
        "water_and_heat_score": 0.54,
        "aether_allocation_share": 0.17,
        "solar_phase_shift": 0.0,
        "wind_phase_shift": 19.0,
        "wind_strength": 0.16,
        "source_keys": "irena_power_costs_2024;iea_electricity_2026;nrel_atb_2024_electricity",
    },
    {
        "region": "australia_pacific_mineral_corridor",
        "display_name": "Australia/Pacific mineral corridor",
        "base_clean_generation_twh_y": 15000.0,
        "solar_share": 0.50,
        "wind_share": 0.30,
        "firm_share": 0.20,
        "storage_hours": 10.0,
        "roundtrip_efficiency": 0.85,
        "interconnection_factor": 0.76,
        "transmission_factor": 0.78,
        "additionality_factor": 0.90,
        "colocation_score": 0.82,
        "storage_corridor_score": 0.76,
        "water_and_heat_score": 0.66,
        "aether_allocation_share": 0.14,
        "solar_phase_shift": 0.3,
        "wind_phase_shift": 18.5,
        "wind_strength": 0.22,
        "source_keys": "irena_power_costs_2024;iea_critical_minerals_outlook_2025;nrel_atb_2024_electricity",
    },
    {
        "region": "north_sea_europe_firm_wind",
        "display_name": "North Sea/Europe firm wind",
        "base_clean_generation_twh_y": 12000.0,
        "solar_share": 0.12,
        "wind_share": 0.58,
        "firm_share": 0.30,
        "storage_hours": 8.0,
        "roundtrip_efficiency": 0.86,
        "interconnection_factor": 0.82,
        "transmission_factor": 0.80,
        "additionality_factor": 0.86,
        "colocation_score": 0.76,
        "storage_corridor_score": 0.58,
        "water_and_heat_score": 0.78,
        "aether_allocation_share": 0.12,
        "solar_phase_shift": 0.0,
        "wind_phase_shift": 16.0,
        "wind_strength": 0.35,
        "source_keys": "nrel_atb_land_wind_2024;iea_electricity_2026;iaea_nuclear_status_2025",
    },
    {
        "region": "south_america_hydro_biomass",
        "display_name": "South America hydro/biomass",
        "base_clean_generation_twh_y": 10000.0,
        "solar_share": 0.28,
        "wind_share": 0.22,
        "firm_share": 0.50,
        "storage_hours": 8.0,
        "roundtrip_efficiency": 0.84,
        "interconnection_factor": 0.72,
        "transmission_factor": 0.72,
        "additionality_factor": 0.84,
        "colocation_score": 0.68,
        "storage_corridor_score": 0.66,
        "water_and_heat_score": 0.82,
        "aether_allocation_share": 0.12,
        "solar_phase_shift": -0.2,
        "wind_phase_shift": 18.0,
        "wind_strength": 0.20,
        "source_keys": "nrel_atb_2024_electricity;iea_electricity_2026;national_academies_ocean_cdr_2022",
    },
]


CASES = [
    {
        "case": "market_regional_reference",
        "display_name": "Market regional reference",
        "target_gtco2_y": 35.0,
        "clean_supply_multiplier": 0.58,
        "ordinary_demand_claim_twh_y": 20000.0,
        "aether_dedication_fraction": 0.50,
        "grid_delivery_modifier": 0.95,
        "additionality_modifier": 0.95,
        "storage_multiplier": 0.85,
        "firm_share_bonus": 0.00,
        "paper_use_rule": "Market-driven clean energy helps but does not create a 100 Gt/year AETHER power system.",
    },
    {
        "case": "dedicated_aether_corridors_dispatch",
        "display_name": "Dedicated AETHER corridors",
        "target_gtco2_y": 70.0,
        "clean_supply_multiplier": 0.95,
        "ordinary_demand_claim_twh_y": 26000.0,
        "aether_dedication_fraction": 0.82,
        "grid_delivery_modifier": 1.03,
        "additionality_modifier": 1.00,
        "storage_multiplier": 1.10,
        "firm_share_bonus": 0.02,
        "paper_use_rule": "Dedicated corridors move AETHER into tens of Gt/year, but still fail the full 100 Gt/year gate.",
    },
    {
        "case": "firm_colocated_backbone_dispatch",
        "display_name": "Firm colocated backbone",
        "target_gtco2_y": 85.0,
        "clean_supply_multiplier": 1.08,
        "ordinary_demand_claim_twh_y": 28000.0,
        "aether_dedication_fraction": 0.86,
        "grid_delivery_modifier": 1.08,
        "additionality_modifier": 1.00,
        "storage_multiplier": 1.35,
        "firm_share_bonus": 0.09,
        "paper_use_rule": "Firm clean colocation improves load service but remains below 100 Gt/year in this screen.",
    },
    {
        "case": "upper_tail_ai_energy_abundance_dispatch",
        "display_name": "Upper-tail AI energy abundance",
        "target_gtco2_y": 125.0,
        "clean_supply_multiplier": 2.00,
        "ordinary_demand_claim_twh_y": 38000.0,
        "aether_dedication_fraction": 0.93,
        "grid_delivery_modifier": 1.15,
        "additionality_modifier": 1.00,
        "storage_multiplier": 1.65,
        "firm_share_bonus": 0.10,
        "paper_use_rule": "Even this upper-tail clean-energy abundance case remains below 100 Gt/year once the repeated representative day has a cyclic storage boundary.",
    },
    {
        "case": "nonadditional_fragmented_grid",
        "display_name": "Nonadditional fragmented grid",
        "target_gtco2_y": 50.0,
        "clean_supply_multiplier": 0.72,
        "ordinary_demand_claim_twh_y": 32000.0,
        "aether_dedication_fraction": 0.45,
        "grid_delivery_modifier": 0.78,
        "additionality_modifier": 0.45,
        "storage_multiplier": 0.70,
        "firm_share_bonus": 0.00,
        "paper_use_rule": "Failure case where clean supply is fragmented, nonadditional, or claimed by other loads.",
    },
]


def adjusted_mix(region: dict, firm_bonus: float) -> tuple[float, float, float]:
    solar = region["solar_share"]
    wind = region["wind_share"]
    firm = min(0.72, region["firm_share"] + firm_bonus)
    variable_total = solar + wind
    new_variable_total = max(0.0, 1.0 - firm)
    if variable_total <= 0:
        return 0.0, 0.0, 1.0
    return solar * new_variable_total / variable_total, wind * new_variable_total / variable_total, firm


def dispatch_day(
    generation_by_hour: list[float],
    hourly_load: float,
    storage_capacity: float,
    roundtrip_efficiency: float,
    initial_storage_state: float,
) -> tuple[dict[str, float], list[dict[str, float]]]:
    """Dispatch one repeated representative day while conserving bus and storage energy.

    All energy values are TWh. Storage state is internal stored energy; charge and
    discharge are measured at the grid bus. This makes conversion losses explicit.
    """
    if not 0.0 < roundtrip_efficiency <= 1.0:
        raise ValueError("roundtrip_efficiency must be in (0, 1]")
    if storage_capacity < 0.0 or not 0.0 <= initial_storage_state <= storage_capacity:
        raise ValueError("storage state must lie within non-negative capacity")

    charge_eff = math.sqrt(roundtrip_efficiency)
    discharge_eff = charge_eff
    storage_state = initial_storage_state
    totals = {
        "generation": 0.0,
        "served": 0.0,
        "unserved": 0.0,
        "curtailed": 0.0,
        "charge_input": 0.0,
        "discharge_delivered": 0.0,
        "storage_conversion_loss": 0.0,
    }
    hourly_rows: list[dict[str, float]] = []

    for hour, generation in enumerate(generation_by_hour):
        start_state = storage_state
        direct_served = min(generation, hourly_load)
        surplus = max(0.0, generation - direct_served)
        deficit = max(0.0, hourly_load - direct_served)
        charge_input = min(surplus, (storage_capacity - storage_state) / charge_eff)
        storage_state += charge_input * charge_eff
        discharge_delivered = min(deficit, storage_state * discharge_eff)
        storage_state -= discharge_delivered / discharge_eff
        served = direct_served + discharge_delivered
        unserved = hourly_load - served
        curtailed = surplus - charge_input
        conversion_loss = charge_input * (1.0 - charge_eff) + discharge_delivered * (
            1.0 / discharge_eff - 1.0
        )

        totals["generation"] += generation
        totals["served"] += served
        totals["unserved"] += unserved
        totals["curtailed"] += curtailed
        totals["charge_input"] += charge_input
        totals["discharge_delivered"] += discharge_delivered
        totals["storage_conversion_loss"] += conversion_loss
        hourly_rows.append(
            {
                "hour": hour,
                "load": hourly_load,
                "generation": generation,
                "served": served,
                "unserved": unserved,
                "curtailed": curtailed,
                "storage_charge_input": charge_input,
                "storage_discharge_delivered": discharge_delivered,
                "storage_conversion_loss": conversion_loss,
                "storage_state_start": start_state,
                "storage_state_end": storage_state,
            }
        )

    totals["storage_state_start"] = initial_storage_state
    totals["storage_state_end"] = storage_state
    totals["bus_balance_residual"] = (
        totals["generation"]
        + totals["discharge_delivered"]
        - totals["served"]
        - totals["charge_input"]
        - totals["curtailed"]
    )
    totals["full_energy_balance_residual"] = (
        totals["generation"]
        + initial_storage_state
        - totals["served"]
        - totals["curtailed"]
        - storage_state
        - totals["storage_conversion_loss"]
    )
    return totals, hourly_rows


def cyclic_dispatch_day(
    generation_by_hour: list[float],
    hourly_load: float,
    storage_capacity: float,
    roundtrip_efficiency: float,
    tolerance_twh: float = 1e-12,
    max_days: int = 10_000,
) -> tuple[dict[str, float], list[dict[str, float]]]:
    """Find a storage state whose end equals its start for the repeated synthetic day."""
    state = storage_capacity * 0.5
    for convergence_days in range(1, max_days + 1):
        trial, _ = dispatch_day(
            generation_by_hour,
            hourly_load,
            storage_capacity,
            roundtrip_efficiency,
            state,
        )
        end_state = trial["storage_state_end"]
        if abs(end_state - state) <= tolerance_twh:
            totals, hourly_rows = dispatch_day(
                generation_by_hour,
                hourly_load,
                storage_capacity,
                roundtrip_efficiency,
                state,
            )
            totals["cyclic_convergence_days"] = float(convergence_days)
            return totals, hourly_rows
        state = end_state
    raise RuntimeError("Representative-day storage state did not converge to a cyclic boundary")


def dispatch_region(case: dict, region: dict, region_base_share: float) -> tuple[dict, list[dict]]:
    ordinary_claim = case["ordinary_demand_claim_twh_y"] * region_base_share
    gross_regional_clean = region["base_clean_generation_twh_y"] * case["clean_supply_multiplier"]
    surplus_clean = max(0.0, gross_regional_clean - ordinary_claim)
    pre_delivery_aether = surplus_clean * case["aether_dedication_fraction"]
    delivery_factor = min(
        0.985,
        region["interconnection_factor"]
        * region["transmission_factor"]
        * region["additionality_factor"]
        * case["grid_delivery_modifier"]
        * case["additionality_modifier"],
    )
    effective_aether_generation = pre_delivery_aether * delivery_factor

    target_twh = gate_twh(case["target_gtco2_y"]) * region["aether_allocation_share"]
    hourly_load = target_twh / 365.0 / 24.0
    storage_capacity = hourly_load * region["storage_hours"] * case["storage_multiplier"]
    solar_share, wind_share, firm_share = adjusted_mix(region, case["firm_share_bonus"])
    solar = solar_shape(region["solar_phase_shift"])
    wind = wind_shape(region["wind_phase_shift"], region["wind_strength"])
    generation_by_hour = [
        effective_aether_generation
        / 365.0
        / 24.0
        * (solar_share * solar[hour] + wind_share * wind[hour] + firm_share)
        for hour in HOURS
    ]
    day, raw_hourly = cyclic_dispatch_day(
        generation_by_hour,
        hourly_load,
        storage_capacity,
        region["roundtrip_efficiency"],
    )
    hourly_rows = [
        {
            "case": case["case"],
            "region": region["region"],
            "hour": int(hour["hour"]),
            "load_gwh": round(hour["load"] * 1000.0, 3),
            "effective_generation_gwh": round(hour["generation"] * 1000.0, 3),
            "served_gwh": round(hour["served"] * 1000.0, 3),
            "unserved_gwh": round(hour["unserved"] * 1000.0, 3),
            "curtailed_gwh": round(hour["curtailed"] * 1000.0, 3),
            "storage_charge_input_gwh": round(hour["storage_charge_input"] * 1000.0, 3),
            "storage_discharge_delivered_gwh": round(hour["storage_discharge_delivered"] * 1000.0, 3),
            "storage_conversion_loss_gwh": round(hour["storage_conversion_loss"] * 1000.0, 3),
            "storage_state_start_gwh": round(hour["storage_state_start"] * 1000.0, 3),
            "storage_state_end_gwh": round(hour["storage_state_end"] * 1000.0, 3),
        }
        for hour in raw_hourly
    ]

    served_twh_y = day["served"] * 365.0
    unserved_twh_y = day["unserved"] * 365.0
    curtail_twh_y = day["curtailed"] * 365.0
    generation_twh_y = day["generation"] * 365.0
    hourly_match = served_twh_y / target_twh if target_twh > 0 else 0.0
    storage_discharge_twh_y = day["discharge_delivered"] * 365.0
    colocation_score = (
        0.35 * region["colocation_score"]
        + 0.30 * region["storage_corridor_score"]
        + 0.20 * region["water_and_heat_score"]
        + 0.15 * hourly_match
    )

    row = {
        "case": case["case"],
        "case_display_name": case["display_name"],
        "region": region["region"],
        "region_display_name": region["display_name"],
        "target_gtco2_y_allocated": round(case["target_gtco2_y"] * region["aether_allocation_share"], 3),
        "required_power_twh_y": round(target_twh, 3),
        "gross_clean_generation_twh_y": round(gross_regional_clean, 3),
        "ordinary_demand_claim_twh_y": round(ordinary_claim, 3),
        "pre_delivery_aether_power_twh_y": round(pre_delivery_aether, 3),
        "delivery_factor": round(delivery_factor, 4),
        "effective_generation_twh_y": round(generation_twh_y, 3),
        "served_load_twh_y": round(served_twh_y, 3),
        "unserved_load_twh_y": round(unserved_twh_y, 3),
        "curtailed_generation_twh_y": round(curtail_twh_y, 3),
        "storage_discharge_twh_y": round(storage_discharge_twh_y, 3),
        "storage_charge_input_twh_y": round(day["charge_input"] * 365.0, 3),
        "storage_conversion_loss_twh_y": round(day["storage_conversion_loss"] * 365.0, 3),
        "storage_state_start_gwh": round(day["storage_state_start"] * 1000.0, 6),
        "storage_state_end_gwh": round(day["storage_state_end"] * 1000.0, 6),
        "storage_boundary_delta_gwh": round(
            (day["storage_state_end"] - day["storage_state_start"]) * 1000.0, 9
        ),
        "energy_balance_residual_gwh_per_day": round(day["full_energy_balance_residual"] * 1000.0, 9),
        "cyclic_convergence_days": int(day["cyclic_convergence_days"]),
        "temporal_scope": "one synthetic 24-hour profile repeated 365 times; cyclic storage boundary; not an 8760-hour weather trace",
        "hourly_match_share": round(hourly_match, 6),
        "max_gtco2_y_supported": round(served_twh_y / gate_twh(1.0), 3),
        "storage_capacity_gwh": round(storage_capacity * 1000.0, 3),
        "colocation_score": round(colocation_score, 4),
        "source_keys": region["source_keys"],
        "paper_use_rule": case["paper_use_rule"],
    }
    return row, hourly_rows


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    total_base_clean = sum(region["base_clean_generation_twh_y"] for region in REGIONS)
    region_rows = []
    for region in REGIONS:
        region_rows.append(
            {
                "region": region["region"],
                "display_name": region["display_name"],
                "base_clean_generation_twh_y": region["base_clean_generation_twh_y"],
                "solar_share": region["solar_share"],
                "wind_share": region["wind_share"],
                "firm_share": region["firm_share"],
                "storage_hours": region["storage_hours"],
                "interconnection_factor": region["interconnection_factor"],
                "transmission_factor": region["transmission_factor"],
                "additionality_factor": region["additionality_factor"],
                "aether_allocation_share": region["aether_allocation_share"],
                "colocation_score": region["colocation_score"],
                "storage_corridor_score": region["storage_corridor_score"],
                "water_and_heat_score": region["water_and_heat_score"],
                "source_keys": region["source_keys"],
                "evidence_class": "regional_archetype_screen",
            }
        )

    by_region: list[dict] = []
    hourly: list[dict] = []
    case_rows: list[dict] = []
    colocation_rows: list[dict] = []

    for case in CASES:
        case_region_rows = []
        case_hourly = []
        for region in REGIONS:
            base_share = region["base_clean_generation_twh_y"] / total_base_clean
            row, hourly_rows = dispatch_region(case, region, base_share)
            case_region_rows.append(row)
            case_hourly.extend(hourly_rows)
        by_region.extend(case_region_rows)
        hourly.extend(case_hourly)

        target_power = gate_twh(case["target_gtco2_y"])
        served = sum(row["served_load_twh_y"] for row in case_region_rows)
        unserved = sum(row["unserved_load_twh_y"] for row in case_region_rows)
        curtail = sum(row["curtailed_generation_twh_y"] for row in case_region_rows)
        effective_generation = sum(row["effective_generation_twh_y"] for row in case_region_rows)
        storage_charge = sum(row["storage_charge_input_twh_y"] for row in case_region_rows)
        storage_discharge = sum(row["storage_discharge_twh_y"] for row in case_region_rows)
        storage_loss = sum(row["storage_conversion_loss_twh_y"] for row in case_region_rows)
        max_gt = served / gate_twh(1.0)
        weighted_match = served / target_power if target_power > 0 else 0.0
        weighted_colocation = sum(row["colocation_score"] * row["served_load_twh_y"] for row in case_region_rows) / served if served > 0 else 0.0
        case_rows.append(
            {
                "case": case["case"],
                "display_name": case["display_name"],
                "target_gtco2_y": case["target_gtco2_y"],
                "required_power_twh_y": round(target_power, 3),
                "served_load_twh_y": round(served, 3),
                "unserved_load_twh_y": round(unserved, 3),
                "effective_generation_twh_y": round(effective_generation, 3),
                "curtailed_generation_twh_y": round(curtail, 3),
                "storage_charge_input_twh_y": round(storage_charge, 3),
                "storage_discharge_delivered_twh_y": round(storage_discharge, 3),
                "storage_conversion_loss_twh_y": round(storage_loss, 3),
                "max_abs_storage_boundary_delta_gwh": max(
                    abs(row["storage_boundary_delta_gwh"]) for row in case_region_rows
                ),
                "weighted_hourly_match_share": round(weighted_match, 6),
                "max_gtco2_y_supported": round(max_gt, 3),
                "passes_30gt": max_gt >= 30.0,
                "passes_50gt": max_gt >= 50.0,
                "passes_100gt": max_gt >= 100.0,
                "weighted_colocation_score": round(weighted_colocation, 4),
                "temporal_scope": "one synthetic 24-hour profile repeated 365 times; cyclic storage boundary; not an 8760-hour weather trace",
                "paper_use_rule": case["paper_use_rule"],
            }
        )

        for row in sorted(case_region_rows, key=lambda item: item["max_gtco2_y_supported"], reverse=True):
            colocation_rows.append(
                {
                    "case": case["case"],
                    "region": row["region"],
                    "region_display_name": row["region_display_name"],
                    "max_gtco2_y_supported": row["max_gtco2_y_supported"],
                    "hourly_match_share": row["hourly_match_share"],
                    "colocation_score": row["colocation_score"],
                    "storage_capacity_gwh": row["storage_capacity_gwh"],
                    "source_keys": row["source_keys"],
                }
            )

    summary = [
        {
            "metric": "temporal_scope",
            "value": "one synthetic 24-hour profile repeated 365 times with cyclic storage",
            "unit": "scope",
            "interpretation": "screening boundary only; not a chronological 8760-hour weather and operations model",
        },
        {
            "metric": "gate_100gt_twh_y",
            "value": round(gate_twh(100.0), 3),
            "unit": "TWh/year",
            "interpretation": "100 GtCO2/year regional dispatch power gate at 3 GJ/tCO2 plus 10% delivery and firming penalty",
        },
        {
            "metric": "best_case_supported_gtco2_y",
            "value": max(row["max_gtco2_y_supported"] for row in case_rows),
            "unit": "GtCO2/year",
            "interpretation": "largest AETHER scale supported in the representative regional dispatch screen",
        },
        {
            "metric": "market_supported_gtco2_y",
            "value": next(row["max_gtco2_y_supported"] for row in case_rows if row["case"] == "market_regional_reference"),
            "unit": "GtCO2/year",
            "interpretation": "market regional reference supported scale",
        },
        {
            "metric": "dedicated_supported_gtco2_y",
            "value": next(row["max_gtco2_y_supported"] for row in case_rows if row["case"] == "dedicated_aether_corridors_dispatch"),
            "unit": "GtCO2/year",
            "interpretation": "dedicated AETHER corridor supported scale",
        },
        {
            "metric": "firm_colocated_supported_gtco2_y",
            "value": next(row["max_gtco2_y_supported"] for row in case_rows if row["case"] == "firm_colocated_backbone_dispatch"),
            "unit": "GtCO2/year",
            "interpretation": "firm colocated clean-power backbone supported scale",
        },
        {
            "metric": "upper_tail_supported_gtco2_y",
            "value": next(row["max_gtco2_y_supported"] for row in case_rows if row["case"] == "upper_tail_ai_energy_abundance_dispatch"),
            "unit": "GtCO2/year",
            "interpretation": "upper-tail AI energy abundance supported scale",
        },
        {
            "metric": "passes_100gt_case_count",
            "value": sum(1 for row in case_rows if row["passes_100gt"]),
            "unit": "count",
            "interpretation": "number of regional dispatch cases clearing the 100 GtCO2/year gate",
        },
        {
            "metric": "passes_50gt_case_count",
            "value": sum(1 for row in case_rows if row["passes_50gt"]),
            "unit": "count",
            "interpretation": "number of regional dispatch cases clearing the 50 GtCO2/year gate",
        },
        {
            "metric": "median_hourly_match_share",
            "value": sorted(row["weighted_hourly_match_share"] for row in case_rows)[len(case_rows) // 2],
            "unit": "share",
            "interpretation": "median representative-day served-load share across regional dispatch cases",
        },
        {
            "metric": "region_count",
            "value": len(REGIONS),
            "unit": "count",
            "interpretation": "regional archetypes in the screening model",
        },
    ]

    write_csv(TABLE_DIR / "aether_regional_power_region_assumptions.csv", region_rows)
    write_csv(TABLE_DIR / "aether_regional_power_dispatch_cases.csv", case_rows)
    write_csv(TABLE_DIR / "aether_regional_power_dispatch_by_region.csv", by_region)
    write_csv(TABLE_DIR / "aether_regional_power_hourly_sample.csv", hourly)
    write_csv(TABLE_DIR / "aether_regional_power_colocation_scorecard.csv", colocation_rows)
    write_csv(TABLE_DIR / "aether_regional_power_dispatch_summary.csv", summary)


if __name__ == "__main__":
    main()

