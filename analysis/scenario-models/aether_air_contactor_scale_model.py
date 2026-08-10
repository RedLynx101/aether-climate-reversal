"""AETHER air-contactor and sorbent physical-scale model.

This model converts the 100 GtCO2/year AETHER target, and the current
40 GtCO2/year DACCS portfolio allocation, into air flow, contactor face area,
fan energy, plant-equivalent counts, sorbent inventory, and replacement mass.
It is first-order plant-scale arithmetic, not a CFD, adsorber, or TEA model.
"""

from __future__ import annotations

from dataclasses import dataclass


SECONDS_PER_YEAR = 365.0 * 24.0 * 3600.0
CO2_PPM = 428.53
CO2_MASS_PER_M3_AT_400PPM_KG = 1000.0 / (0.0409 * SECONDS_PER_YEAR)
CO2_MASS_PER_M3_KG = CO2_MASS_PER_M3_AT_400PPM_KG * (CO2_PPM / 400.0)


@dataclass(frozen=True)
class AirScenario:
    capture_fraction: float
    air_velocity_m_s: float
    pressure_drop_pa: float
    fan_efficiency: float
    uptime_fraction: float


@dataclass(frozen=True)
class SorbentScenario:
    total_capacity_mol_kg: float
    swing_fraction: float
    cycle_time_min: float
    uptime_fraction: float
    lifetime_y: float


def air_scale(target_gtco2_y: float, scenario: AirScenario) -> dict[str, float]:
    target_tpy = target_gtco2_y * 1_000_000_000.0
    target_kg_y = target_tpy * 1000.0
    operating_seconds = SECONDS_PER_YEAR * scenario.uptime_fraction
    air_flow_m3_s = target_kg_y / (
        CO2_MASS_PER_M3_KG * scenario.capture_fraction * operating_seconds
    )
    area_m2 = air_flow_m3_s / scenario.air_velocity_m_s
    volume_per_tonne_m3 = 1000.0 / (
        CO2_MASS_PER_M3_KG * scenario.capture_fraction
    )
    fan_energy_gj_t = (
        scenario.pressure_drop_pa * volume_per_tonne_m3
    ) / (scenario.fan_efficiency * 1_000_000_000.0)
    fan_energy_twh_y = fan_energy_gj_t * target_tpy / 3_600_000.0
    return {
        "air_flow_m3_s": air_flow_m3_s,
        "area_km2": area_m2 / 1_000_000.0,
        "fan_energy_gj_t": fan_energy_gj_t,
        "fan_energy_twh_y": fan_energy_twh_y,
        "fan_average_power_tw": fan_energy_twh_y / 8760.0,
    }


def sorbent_scale(target_gtco2_y: float, scenario: SorbentScenario) -> dict[str, float]:
    target_kg_y = target_gtco2_y * 1_000_000_000_000.0
    working_kg_kg = (
        scenario.total_capacity_mol_kg * scenario.swing_fraction * 44.0095 / 1000.0
    )
    cycles_y = scenario.uptime_fraction * 365.0 * 24.0 * 60.0 / scenario.cycle_time_min
    co2_per_kg_sorbent_y = working_kg_kg * cycles_y
    inventory_kg = target_kg_y / co2_per_kg_sorbent_y
    return {
        "working_capacity_kg_kg": working_kg_kg,
        "cycles_per_year": cycles_y,
        "sorbent_inventory_mt": inventory_kg / 1_000_000_000.0,
        "sorbent_replacement_mt_y": inventory_kg / scenario.lifetime_y / 1_000_000_000.0,
    }
