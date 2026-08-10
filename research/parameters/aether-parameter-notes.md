# AETHER Parameter Notes

This note documents the quantitative parameters used in `analysis/scenario-models/aether_scenario_model.py` as of 2026-06-09. Values are intentionally explicit and conservative enough to audit. They are not claims that AETHER can be built today.

## Current-State Anchors

| Parameter | Value | Source key | Use |
|---|---:|---|---|
| Global monthly mean CO2, February 2026 | 428.53 ppm | `noaa_gml_global_co2_2026` | Air-processing mass fraction and current-state framing |
| Mauna Loa monthly mean CO2, May 2026 | 432.34 ppm | `noaa_gml_mauna_loa_co2_2026` | Public-facing current CO2 reference |
| 2025 fossil CO2 emissions | 38.1 GtCO2/year | `global_carbon_budget_2025` | Emissions baseline |
| 2025 total anthropogenic CO2 emissions | 42.2 GtCO2/year | `global_carbon_budget_2025` | Net-removal comparison |
| Current global CDR | 2.2 GtCO2/year | `state_of_cdr_2026` | Present-day removal scale |
| Current novel CDR | 0.00204 GtCO2/year | `state_of_cdr_2026` | Gap between new engineered methods and 100 Gt/year target |

## Energy Parameters

| Parameter | Value | Source key | Interpretation |
|---|---:|---|---|
| DAC theoretical minimum separation energy | 0.5 GJ/tCO2 | `ipcc_ar6_wg3_ch12` | Thermodynamic lower bound for separating dilute CO2 from air |
| Current DAC total energy range | 4-10 GJ/tCO2 | `ipcc_ar6_wg3_ch12` | Current technology range cited by IPCC WGIII |
| CO2 formation enthalpy | -393.51 kJ/mol | `nist_chemistry_webbook_co2` | Used to calculate ideal CO2 splitting floor |
| CO2 -> C + O2 splitting floor | 8.94 GJ/tCO2 | `nist_chemistry_webbook_co2_calculated` | Enthalpy floor; real systems are higher |

Energy conversion used in the model:

```text
1 GJ/tCO2 * 1 GtCO2/year = 277.78 TWh/year
average TW = annual TWh / 8,760 h/year
```

This makes energy sensitivity stark. At 100 GtCO2/year:

| Total energy intensity | Annual energy | Average power |
|---:|---:|---:|
| 1 GJ/tCO2 | 27,778 TWh/year | 3.17 TW |
| 3 GJ/tCO2 | 83,333 TWh/year | 9.51 TW |
| 8 GJ/tCO2 | 222,222 TWh/year | 25.37 TW |
| 11.94 GJ/tCO2 | 331,708 TWh/year | 37.87 TW |

The last row is the model's advanced-capture plus 100% CO2-splitting case: 3 GJ/tCO2 capture plus 8.94 GJ/tCO2 ideal splitting.

## Atmosphere and Storage Conversions

Simple atmospheric conversion:

```text
1 ppm atmospheric CO2 ~= 7.8 GtCO2
```

This is used only for simple atmosphere-only bookkeeping. It does not model land-ocean rebound, changing natural sinks, or climate-carbon feedbacks.

At 100 GtCO2/year gross removal:

| Quantity | Approximate value | Notes |
|---|---:|---|
| Gross atmosphere-only drawdown | 12.82 ppm/year | 100 / 7.8 |
| Net atmosphere-only drawdown after 42.2 GtCO2/year emissions | 7.41 ppm/year | (100 - 42.2) / 7.8 |
| Air mass processed at 428 ppm | 153,775 Gt air/year | Dry-air mass fraction estimate using MW CO2 / MW dry air |
| Air volume processed at 1.2 kg/m3 | 128,146,008 km3/year | About 4.06 billion m3/s average flow |
| Supercritical CO2 storage volume | 166.7 km3/year | Uses 600 kg/m3 storage density |
| CO2 gas volume at STP | 50,505 km3/year | Uses 1.98 kg/m3 gas density |
| Solid carbon volume if all CO2 is split | 12.4 km3/year | Uses 2,200 kg/m3 graphite-like density |
| Liquid O2 volume if all CO2 is split | 63.7 km3/year | Uses 1,141 kg/m3 liquid oxygen density |

The storage-state result is central: splitting CO2 into solid carbon and O2 has a much smaller storage volume than storing CO2 as a gas or supercritical fluid, but it adds a very large thermodynamic burden. Geologic storage is the lower-energy default; full splitting needs a specific reason to justify the energy penalty.

## Robotics and Automation Assumptions

The model includes robot unit costs of $25,000 to $100,000, lifetimes of 7-8 years, 5,000-7,000 annual operating hours, and maintenance rates of 8-12% of unit cost per year. These are scenario variables, not verified market facts.

The point of including them is to test whether cheap embodied labor changes the buildout economics. Direct robot-hour cost can fall below human wages under aggressive assumptions, but AETHER remains constrained by energy, materials, storage, permitting, siting, compression, transport, drilling, MRV, and institutional trust. Humanoid robots are useful only if they materially reduce those bottlenecks.

## Governance Branch

The commons-ownership track treats atmosphere, oceans, and lakes as citizen-owned or trust-held sinks. The parameter implication is that emissions and other outputs should have rates, liability, monitoring, and prohibitions. Some outputs may be priced; dangerous outputs should be restricted or banned rather than monetized. This track is exploratory and should not become a license-to-pollute argument.
