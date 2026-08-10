# Air-Contactor and Sorbent Physical Scale Notes

Last updated: 2026-06-09

This note translates AETHER's atmospheric capture target into plant-scale hardware. It is intentionally mechanical: air flow, contactor face area, fan energy, plant-equivalent counts, sorbent inventory, and replacement mass. It is not a CFD model, a final adsorber design, or a complete direct-air-capture TEA.

## Source Anchors

- NOAA's February 2026 global CO2 value, 428.53 ppm, is used as the current atmospheric concentration anchor.
- NASEM's direct-air-capture chapter reports that at 1.5 m/s air velocity and 75% capture, a 1 MtCO2/year contactor needs about 38,000 m2 cross-sectional area.
- NASEM's same chapter gives solid-sorbent ranges including 0.5-1.5 mol CO2/kg sorbent, 1-5 m/s air velocity, 0.25-5 year adsorbent life, 300-1,400 Pa pressure drop, and fan energy ranges.
- Keith et al. provide a 1 MtCO2/year aqueous KOH DAC engineering design and cost basis.
- Climeworks Mammoth is a useful commercial comparator at 36,000 tCO2/year nameplate capacity; 1PointFive STRATOS is a larger industrial comparator at 500,000 tCO2/year.

## Main Result

For the 100 GtCO2/year all-air stress test, the NASEM reference case gives about 5.7 billion m3/s of air flow, about 3,771 km2 of contactor face area, and about 9,290 TWh/year of fan electricity before regeneration heat, compression, storage, maintenance, and lifecycle penalties.

The current AETHER portfolio allocates 40 GtCO2/year to DACCS rather than 100 GtCO2/year. Even that narrower DACCS allocation gives about 1,508 km2 of NASEM-reference contactor face area and about 80,000 STRATOS-scale 500 kt/year facility equivalents.

The AETHER low-pressure modular case reduces the 100 GtCO2/year all-air face-area proxy to about 1,627 km2 and fan energy to about 5,621 TWh/year. That is not a current-technology claim. It requires better contactor architecture, low pressure drop, high velocity without unacceptable capture loss, automated cleaning, and high factory throughput. The high-pressure warning case goes the other direction: fan energy alone reaches about 130,056 TWh/year, which is larger than the main 3 GJ/tCO2 capture-energy target.

## Sorbent Inventory

The NETL-style reference loading case gives about 150.1 Mt of sorbent inventory and about 75.1 Mt/year replacement for 100 GtCO2/year all-air capture. For the 40 GtCO2/year DACCS allocation, the same case gives about 60.0 Mt inventory and 30.0 Mt/year replacement.

The AETHER improved sorbent case lowers the 100 GtCO2/year inventory to about 34.8 Mt and replacement to about 7.0 Mt/year. This is a useful moonshot target for AI materials discovery and automated manufacturing, but it should remain labeled as a scenario until material stability, humidity tolerance, fouling, cycle energy, and low-cost manufacture are demonstrated.

## Interpretation

The result is not "DAC is impossible." It is that DAC at climate-reversal scale becomes a factory and fluid-mechanics problem before it becomes a policy slogan. AI and robotics can help by designing sorbents, optimizing contactors, automating fabrication, cleaning fouled modules, and coordinating maintenance. They cannot remove the need to move enough air across enough active surface with acceptable pressure drop.
