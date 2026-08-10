# Power-System Buildout and Firm Energy Notes

Last updated: 2026-06-09

This note translates AETHER electricity demand into installed clean-power capacity. It is not a dispatch model. It does not solve transmission, seasonal storage, reliability, interconnection, or siting. It answers a narrower question: if AETHER needs tens of thousands of TWh/year, what does that mean in terawatts of solar, wind, nuclear, geothermal, and short-duration flexibility?

## Source Anchors

- NREL ATB provides the technology-parameter framework for capacity factors, CAPEX, O&M, and LCOE.
- NREL's solar land-use report gives a rough utility-scale solar total-area proxy of 3.5 acres/GWh/year.
- IAEA reports 377 GW(e) operational nuclear capacity and 2,617.5 TWh of nuclear generation in 2024, with 64.5 GW(e) under construction.
- IEA's geothermal report gives a cost-effective 2050 case of about 800 GW producing almost 6,000 TWh/year, and notes geothermal utilization above 75%.
- IEA Electricity 2026 reports utility-scale battery project costs around $150/kWh in 2024, 63 GW of utility-scale battery additions in 2024, and 124 GW installed.

## Main Result

The 3 GJ/tCO2 AETHER case needs 83,333 TWh/year delivered to removal. In a balanced clean-power portfolio with 10% gross overgeneration and losses, that becomes about 91,667 TWh/year of gross generation and about 27.5 TW of installed nameplate capacity.

That balanced case includes about 3.5 TW of firm clean capacity from nuclear and advanced geothermal. That is about 9.2x current global nuclear capacity if treated as a nuclear/geothermal firm-power comparator.

The solar-heavy case has lower firm-power demand, but it moves the burden into land, storage, curtailment, and transmission. Its utility-scale solar land proxy is about 920,661 km2. That is not a literal land forecast, but it makes the spatial scale visible.

The current portfolio/lifecycle energy case, about 64,750 TWh/year, still needs about 21.3 TW of nameplate capacity in the balanced portfolio. The full-splitting case would need about 109 TW of nameplate capacity even before a real dispatch model. This is why full splitting should remain a specialized pathway.

## Short-Duration Storage Proxy

The table includes a deliberately narrow four-hour storage proxy: enough storage power to shift 25% of average variable renewable output for four hours. For the 3 GJ balanced case, this is about 7,325 GWh of battery-equivalent energy. At $150/kWh, that proxy alone is about $1,099B. This is not seasonal storage, not a reliability reserve, and not a complete grid model. It is a minimum reminder that high-VRE AETHER requires flexibility infrastructure in addition to generation capacity.

## Interpretation

The energy bottleneck is not just total TWh. It is the combination of annual generation, nameplate capacity, firm supply, land, storage, transmission, and interconnection. AI and robotics can help by speeding factories, permitting analysis, drilling, construction, grid inspection, and automated demand response. They do not eliminate capacity factors. The power system remains one of the strongest filters on AETHER plausibility.
