# Carbon-Cycle Response Notes

Last updated: 2026-06-09

This note documents the first AETHER carbon-cycle time-path model. It replaces pure atmosphere-only ppm arithmetic as the main drawdown view, while keeping the simple conversion as an intuition check.

## Why This Exists

The simple AETHER endpoint calculation treats 1 ppm atmospheric CO2 as about 7.8 GtCO2 and subtracts annual emissions from annual removals. That is useful for scale, but it is not enough for scientific claims. Land and ocean reservoirs exchange carbon with the atmosphere. When emissions add CO2, a fraction is taken up by land and oceans over time. When removal lowers atmospheric CO2, those same reservoirs can release some CO2 back relative to the removal path. A ton removed from the air is therefore not always equal and opposite to a ton emitted, especially over large changes and changing background states.

## Current Reduced-Form Model

Implementation: `analysis/scenario-models/aether_carbon_cycle_model.py`

Outputs:

- `analysis/tables/aether_carbon_cycle_pathways.csv`
- `analysis/tables/aether_carbon_cycle_summary.csv`
- `analysis/figures/carbon_cycle_atmospheric_co2_pathways.png`

The model uses the Joos et al. 2013 multi-model mean CO2 impulse-response function:

`R(t) = 0.2173 + 0.2240 exp(-t/394.4) + 0.2824 exp(-t/36.54) + 0.2763 exp(-t/4.304)`

This gives the fraction of a CO2 pulse that remains in the atmosphere after `t` years in the reduced-form approximation. The coefficients are used directly for scenario comparison. The model tracks annual effective pulses from 2026 through 2100 and convolves those pulses with the impulse response.

## Removal Effectiveness

The base AETHER runs use a `0.96` removal-effectiveness multiplier for durable removals. This is not a universal constant. It is a caution factor based on IPCC AR6 WG1's discussion that, across assessed models, an emission raises atmospheric CO2 slightly more than an equivalent removal lowers it, with the difference depending on background state and removal scale. The model should later test a wider range: 1.00, 0.96, 0.90, and state-dependent versions.

## Management Floor

Most AETHER scenarios now use an illustrative 350 ppm atmospheric management floor. This prevents the model from pretending that a serious earth-management system would keep removing 100 GtCO2/year after the atmosphere has already returned to a lower target range. If the reduced-form path reaches the floor, the model throttles annual AETHER removals to the amount needed to avoid pushing below it.

The 350 ppm floor is a scenario control, not a recommendation. A final paper should test multiple managed targets, including 420, 400, 350, and preindustrial-adjacent levels, while considering ocean acidification, ecological effects, food systems, ice-sheet risk, and governance.

## Current Scenario Set

- No AETHER, constant emissions.
- Managed AETHER ramps toward 100 GtCO2/year by 2046 while current emissions continue, then throttles near 350 ppm.
- Managed AETHER ramps toward 100 GtCO2/year by 2046 while current emissions continue and rebound/delayed abatement reaches 57.8% of gross removal.
- Managed AETHER ramps toward 100 GtCO2/year by 2046 while emissions halve by 2046 and reach zero by 2060, then throttles near 350 ppm.
- Managed AETHER ramps toward 100 GtCO2/year by 2046 while emissions reach zero by 2050, then throttles near 350 ppm.
- Managed AETHER ramps toward 100 GtCO2/year by 2046 while emissions reach zero by 2050 and rebound reaches 25% of gross removal, then throttles near 350 ppm.

## Interpretation

This model changes the paper's tone. AETHER can create very large atmospheric drawdown in favorable scenarios, but the time path depends strongly on ordinary emissions policy, rebound, and control rules. If removal becomes an excuse to keep emitting, the system loses much of its scientific and political value. If removal is paired with fast emissions decline, the modeled atmosphere can return toward an explicit management range this century.

## Limits

This is not an Earth-system model. It does not include temperature feedbacks, nonlinear ocean chemistry, state-dependent land/ocean response, methane and nitrous oxide, lifecycle emissions from AETHER infrastructure, albedo, aerosols, regional climate effects, ecological recovery, ice dynamics, or ocean-acidification reversal.

The right use is feasibility screening: it shows which scenarios are obviously too weak, which scenarios are physically interesting, and where a later FAIR-class or Earth-system-model workflow should focus.
