# Climate-Response and Temperature-Proxy Notes

Last updated: 2026-06-09

This note records the first AETHER climate-response layer. The existing carbon-cycle model already turns emissions and removal time paths into atmospheric CO2 ppm trajectories. The v0.25 climate-response model turns those ppm paths into a CO2-only forcing and temperature proxy.

The source anchors are intentionally narrow:

- IPCC AR6 WGI Chapter 7 anchors CO2 effective radiative forcing for a doubling of CO2 at 3.93 W/m2.
- IPCC AR6 WGI Technical Summary anchors the TCR/ECS/TCRE context and warns that very low or net-negative CO2 pathways carry additional uncertainty.
- FAIR v1.3 is the next proper model class because it tracks CO2 concentration, radiative forcing, and temperature response rather than using a static proxy.

The current proxy uses:

`FCO2 = 3.93 * log2(C / 278)`

`CO2-only equilibrium warming proxy = FCO2 / 3.93 * 3.0`

`CO2-only transient-scaled warming proxy = FCO2 / 3.93 * 1.8`

That is not a full temperature model. It excludes non-CO2 forcing, aerosols, ocean heat uptake dynamics, ice sheets, regional climate response, ocean chemistry, and state-dependent carbon-climate feedbacks. It is useful because it makes the carbon-cycle pathways easier to compare in a reviewer-readable way, but it should be replaced by FAIR or an Earth-system workflow before publication-grade climate claims.

## Current Result

| Scenario | 2100 ppm | 2100 CO2 ERF | 2100 transient proxy | Avoided vs no AETHER |
| --- | --- | --- | --- | --- |
| No AETHER, constant emissions | 656 | 4.87 W/m2 | 2.23 deg C | 0.00 deg C |
| AETHER, constant emissions | 350 | 1.31 W/m2 | 0.60 deg C | 1.63 deg C |
| AETHER, 58% rebound | 473 | 3.02 W/m2 | 1.38 deg C | 0.85 deg C |
| AETHER plus net-zero 2050 | 350 | 1.31 W/m2 | 0.60 deg C | 1.63 deg C |

The interpretation is simple but important. AETHER plus strong emissions decline produces much lower CO2-only forcing than a no-AETHER constant-emissions case in this proxy. Rebound materially weakens that result. The result should be framed as a model-screening output, not as a forecast of total warming.

## Next Upgrade

- Run the same AETHER emissions/removal paths through FAIR.
- Add non-CO2 forcing and aerosol scenarios rather than leaving the proxy CO2-only.
- Model zero-emissions commitment and net-negative-pathway uncertainty explicitly.
- Connect temperature response to ocean chemistry and regional impact questions rather than treating global mean temperature as the whole climate result.
- Add lifecycle emissions from AETHER energy, construction, materials, transport, storage, and MRV.

