# MRV and Credit-Integrity Notes

Last updated: 2026-06-09

This note adds a first AETHER screen for measurement, reporting, verification, credit integrity, reversal buffers, invalidation reserves, and liability cost. It is a stress test, not a calibrated crediting methodology.

The model starts from the current AETHER 100 GtCO2/year gross pathway portfolio and the existing storage-lifecycle table. It then applies four additional discounts by pathway:

- measurement uncertainty,
- method and attribution uncertainty,
- reversal or leakage buffer,
- credit-invalidation reserve.

It also adds a provisional MRV/liability cost bucket. The sources anchor the governance standard, not the numeric buffer values. EPA Class VI and Subpart RR make geologic storage a better-defined MRV problem than diffuse open-system CDR. The EU CRCF and Oxford principles provide quality, verification, registry, and durable-storage framing. The National Academies ocean CDR report keeps ocean pathways in a research-gap posture.

## Current Result

The current 100 GtCO2/year gross portfolio becomes about 84.879 GtCO2/year after the existing 100-year lifecycle/durability screen, then about 66.445 GtCO2/year after the provisional MRV and credit-integrity buffers. At the same pathway mix, crediting 100 GtCO2/year would require about 150.500 GtCO2/year gross removal.

| Pathway | Gross Gt/y | 100y durable Gt/y | Creditable Gt/y | Gross per credit | MRV risk class |
| --- | --- | --- | --- | --- | --- |
| DACCS with geologic storage | 40.0 | 37.6 | 34.6 | 1.16x | lower_mrv_risk_high_durability |
| Direct ocean capture and electrochemical mCDR | 4.0 | 3.5 | 2.9 | 1.38x | medium_mrv_risk_low_trl |
| BECCS | 10.0 | 8.0 | 6.8 | 1.47x | medium_mrv_risk |
| Enhanced weathering and surficial mineralization | 20.0 | 17.6 | 11.8 | 1.70x | medium_high_mrv_risk |
| Ocean alkalinity enhancement | 15.0 | 12.1 | 7.1 | 2.11x | high_mrv_risk_low_trl |
| Biochar | 6.0 | 4.0 | 2.5 | 2.45x | medium_high_reversal_risk |
| Afforestation and reforestation | 5.0 | 2.1 | 0.8 | 6.48x | high_reversal_and_counterfactual_risk |

## Interpretation

This is a hard constraint on the story. AETHER cannot claim climate reversal by counting gross captured tonnes as if they were creditable, durable removals. The current portfolio loses value first to lifecycle and permanence, and then again to measurement uncertainty, open-system attribution, reversal buffers, and credit invalidation risk.

Geologic storage performs best in this first screen because the engineering boundary is narrower: injected mass, plume behavior, leakage pathways, pressure management, and monitoring can be regulated and reported. That does not make geologic storage easy at AETHER scale. It means the MRV problem is better formed.

Open-system pathways are different. Enhanced weathering, ocean alkalinity, biochar, and afforestation can still matter, but their creditable fraction depends on counterfactual baselines, distributed measurement, ecological risk, durability, and reversal. These pathways should be modeled as climate contributions before they are modeled as fungible credits.

The policy implication is direct: AETHER needs adversarial measurement and liability as part of the system design. If the credit layer is weak, cheaper removal can increase emissions by making offset claims cheaper than real decarbonization.

## Next Upgrade

Replace the provisional buffers with method-specific distributions:

- geologic storage: site-level pressure, plume, leakage, monitoring, post-injection care, and financial responsibility;
- biomass and biochar: feedstock counterfactuals, land-use change, process emissions, product fate, and reversal;
- enhanced weathering: rock type, grind size, spreading location, runoff chemistry, alkalinity export, and heavy-metal/ecological constraints;
- ocean CDR: air-sea exchange, mixing, ecological risk, attribution, baseline drift, and international governance;
- credit markets: fraud detection, registry duplication, invalidation rules, buffer-pool adequacy, and long-run liability.

