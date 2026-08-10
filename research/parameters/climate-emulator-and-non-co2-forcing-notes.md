# Climate Emulator and Non-CO2 Forcing Notes

Last updated: 2026-06-09

Implementation: `analysis/scenario-models/aether_climate_emulator_model.py`

This layer upgrades the earlier CO2-only temperature proxy without pretending to be a full climate model. The model is a calibrated two-box screening emulator. It uses the AR6 CO2 forcing anchor, `FCO2 = 3.93 * log2(C / 278)`, then adds an ocean heat-uptake lag and explicit non-CO2 plus aerosol forcing-policy screens.

The calibration is intentionally visible. ECS is set to 3.000 deg C through the feedback parameter, and the grid search reaches a TCR of about 1.800 deg C with mixed-layer heat capacity 12.000 W yr m-2 C-1, deep-ocean heat capacity 100.000 W yr m-2 C-1, and ocean exchange 0.950 W m-2 C-1.

## Forcing Policies

| Forcing policy | Non-CO2 W/m2, 2026 -> 2100 | Aerosol W/m2, 2026 -> 2100 | Use |
| --- | --- | --- | --- |
| CO2-only emulator screen | 0.000 -> 0.000 | 0.000 -> 0.000 | scenario screen |
| Mitigation with aerosol cleanup | 1.200 -> 0.450 | -0.700 -> -0.050 | scenario screen |
| Delayed non-CO2 mitigation plus aerosol unmasking | 1.200 -> 1.050 | -0.700 -> -0.050 | scenario screen |
| Active full-forcing management | 1.200 -> 0.200 | -0.700 -> 0.000 | scenario screen |

The non-CO2 and aerosol values are scenario assumptions anchored to the fact that AR6 separates CO2, non-CO2 greenhouse gases, and aerosols in the forcing budget. They are not forecasts. Their purpose is to expose a failure mode: AETHER can look strong in a CO2-only graph while total forcing remains high if methane, nitrous oxide, ozone precursors, industrial gases, and aerosol unmasking are not handled.

## Current Screen Results

| Scenario | 2050 temp | 2100 temp | 2026-2100 change | Avoided vs same-forcing no-AETHER |
| --- | --- | --- | --- | --- |
| No AETHER; delayed non-CO2 + aerosol unmasking | 2.32 | 3.24 | 1.63 | 0.00 |
| AETHER with 58% rebound; same forcing stress | 2.11 | 2.38 | 0.76 | 0.86 |
| AETHER + net-zero 2050; mitigation cleanup | 1.34 | 1.20 | -0.42 | 1.74 |
| AETHER + net-zero 2050; full-forcing management | 1.30 | 1.10 | -0.51 | 1.74 |

The important interpretation is directional. The stress case shows that cheap CO2 removal is not enough if non-CO2 mitigation is delayed and aerosol cleanup unmasks warming. The full-forcing management case shows the stronger AETHER thesis: CO2 removal must be paired with a wider program for atmospheric engineering, clean energy, pollution cleanup, and governance.

## Limitations

- This is not FAIR, MAGICC, Hector, FaIR-calibrated CMIP emulation, or an Earth-system model.
- The historical spin-up is a screening initialization, not an observed temperature reconstruction.
- Non-CO2 and aerosol forcing pathways are policy screens, not cited forecasts.
- The model has no state-dependent carbon-cycle feedback, zero-emissions commitment, ice-sheet dynamics, ocean chemistry, regional response, or damages.
- Publication-grade claims still require a real climate-emulator workflow, ideally with source-backed emissions pathways, non-CO2 gas trajectories, aerosol pathways, uncertainty ensembles, and comparison against assessed temperature metrics.

Use this layer in the paper as a discipline device: it is strong enough to show why AETHER cannot be CO2-only, but too simple to support final temperature claims.

