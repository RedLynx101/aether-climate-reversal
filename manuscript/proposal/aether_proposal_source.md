<!--
Source for the AETHER proposal document.
Built by scripts/build_aether_proposal_docx.py into DOCX and PDF.
Syntax: ## / ### / #### headings, GitHub tables, FIG: lines, TABLE-CAPTION: lines, > quotes, - bullets.
-->

TITLE: AETHER: Atmospheric Engineering Through High-Energy Removal
SUBTITLE: A Conditional Feasibility Analysis and Research Proposal for a 100 GtCO2 per Year Gross Removal Stress Test in an AI- and Robotics-Accelerated Economy
AUTHOR: Noah Hicks
DATE: August 2026
STATUS: Public working paper - conditional feasibility analysis; not peer reviewed
REPOSITORY: https://github.com/RedLynx101/aether-climate-reversal

## Abstract

This paper asks whether atmospheric CO2 drawdown could become a managed infrastructure problem rather than a loosely promised offset market. It evaluates a deliberately strong premise: that over the next two decades, AI systems and robotics improve enough to rival large portions of human scientific, engineering, construction, and industrial labor. Under that premise, the limiting question is not whether smarter models can imagine carbon removal. It is whether enough clean energy, machinery, storage capacity, measurement, capital, and governance can be assembled to remove CO2 at rates large enough to reverse atmospheric accumulation.

The analysis centers on a 100 GtCO2 per year gross removal target, roughly 2.4 times current annual anthropogenic CO2 emissions and about 45 times current global carbon dioxide removal. The target is intentionally extreme. Its purpose is to expose feasibility boundaries, not to forecast deployment. At current direct-air-capture energy intensities of 4-10 GJ/tCO2, 100 GtCO2/year would require on the order of 110,000-280,000 TWh of energy per year, several times current world electricity generation. An advanced 3 GJ/tCO2 pathway still requires about 83,000 TWh/year, and a near-thermodynamic 1 GJ/tCO2 pathway about 28,000 TWh/year. Splitting captured CO2 into solid carbon and oxygen adds an ideal enthalpy burden of 8.94 GJ/tCO2, which removes full splitting from consideration as a default storage pathway.

The analysis concludes that 100 GtCO2/year is not contradicted by the selected first-order mass-and-energy screens, but is plausible only under a narrow coordinated-abundance scenario: capture energy falling toward 1-3 GJ/tCO2, storage dominated by geologic and mineral pathways, clean-energy construction exceeding today's record growth by sustained multiples for decades, and delivered costs falling toward $10-50/tCO2. AI and robotics matter to the extent that they move binding constraints: compressing R&D cycles, lowering construction and operations labor, improving drilling and monitoring, and scaling plant manufacturing. They do not remove thermodynamic floors, reactive-media requirements, land and water conflicts, storage liability, measurement integrity, or the political problem of treating shared air and oceans as free dumping grounds. The paper therefore proposes a staged research program with explicit falsification gates: source-backed parameter models, climate-model upgrades, regional energy and storage models, robotics field-productivity evidence, and a governance branch that treats atmospheric and ocean sinks as priced or protected commons.

**Keywords:** carbon dioxide removal; direct air capture; climate reversal; AI automation; robotics; carbon storage; atmospheric commons; public trust doctrine

## 1. Introduction

### 1.1 Scope and Claim

AETHER stands for Atmospheric Engineering Through High-Energy Removal. The name is deliberately explicit. This is not a claim that climate repair is cheap, automatic, or available today. It is a research program about whether the atmosphere can become a deliberately managed infrastructure variable if energy, automation, and durable storage improve far beyond present levels.

This paper uses "climate reversal" in a narrow sense: sustained net-negative CO2 sufficient to reduce atmospheric CO2 concentration over time. It does not claim to reverse all climate damage, and it does not directly address methane, nitrous oxide, ocean acidification, biodiversity loss, hydrological shifts, or heat extremes. The central question is:

> Under a strong 2046 abundance premise, in which AI and robotics rival large amounts of human scientific and physical labor, what technical and governance conditions would have to hold for durable CO2 removal at 100 GtCO2 per year to be plausible?

The answer developed here is conditional. AETHER becomes physically plausible only if the system converges toward low capture energy, cheap and additional clean power, automated construction, durable storage, adversarial measurement, and a governance structure that makes atmospheric and ocean dumping costly or prohibited. It fails if it depends on current direct-air-capture costs, full splitting of captured CO2, weak measurement, fossil-powered removal, or carbon credits that are easier to sell than to verify.









<!-- AETHER-PUBLICATION-GATE:proposal-accounting:BEGIN -->
### 1.2 Accounting and Assumption Boundaries

The 100 GtCO2/year headline is a gross-removal stress test, not an optimum, recommendation, central forecast, or deployment promise. The analysis distinguishes gross removal, lifecycle-adjusted durable removal, creditable removal after provisional MRV buffers, and the final net climate result after residual emissions and rebound. The labels `pass` and `conditional pass` describe internal scenario gates, not empirical validation. Monte Carlo pass shares come from hand-set distributions and are not real-world probabilities. Costs are reported or scenario USD that have not been harmonized to constant 2026 dollars, and TWh values may represent electricity or heat-equivalent energy depending on the pathway.

Copyright (c) 2026 Noah Hicks. Noah Hicks is the project originator and principal author. Original research content is licensed CC BY 4.0; repository code is licensed Apache-2.0. The licenses require attribution for covered expression and code but do not make underlying ideas, systems, or methods exclusive.
<!-- AETHER-PUBLICATION-GATE:proposal-accounting:END -->








<!-- AETHER-PUBLIC-RELEASE:proposal-project:BEGIN -->
The public research record is maintained at https://github.com/RedLynx101/aether-climate-reversal. This paper is one presentation layer for the concept, not the project boundary. The repository contains the underlying models, tables, figures, source discipline, review gates, and contribution workflow so outside reviewers can inspect or extend the work.
<!-- AETHER-PUBLIC-RELEASE:proposal-project:END -->

### 1.3 Prior Work and Contribution

AETHER is not the first carbon dioxide removal roadmap, the first direct-air-capture cost model, the first argument that DAC can scale modularly, the first atmospheric-commons governance proposal, or the first use of AI for carbon-capture materials discovery. The project would be weaker if it pretended otherwise.

The prior work is substantial. The National Academies, the IPCC, the State of Carbon Dioxide Removal reports, and Roads to Removal establish the CDR research agenda, pathway set, current scale, and regional planning frame (National Academies, 2019; IPCC, 2022a; State of CDR, 2026; Pett-Ridge et al., 2023). Realmonte et al. (2019) model direct air capture with carbon storage in deep mitigation pathways, including 30 GtCO2/year capacity cases. Chatterjee and Huang (2020) challenge very large DAC deployment on energy, materials, sorbent, and coproduct grounds. Young et al. (2023) show why DAC-with-storage costs may remain far above optimistic public targets without strong deployment and policy support. Keith et al. (2018), the National Academies (2019b), and NETL (Patel et al., 2025) provide process, contactor, and sorbent-engineering anchors.

Adjacent work already touches the AI and robotics premise. McQueen and Drennan (2024) connect warehouse automation to scalable DAC design. The OpenDAC dataset provides a machine-learning materials-discovery benchmark for DAC sorbents (Sriram et al., 2023), and Giro et al. (2023) demonstrate AI-driven automated discovery of carbon-capture polymer membranes. None of this proves that AI scientists and robots can deliver removal at the scale considered here. It proves the narrower point that parts of the premise are already visible in the literature as separate active fields.

The intended contribution is the coupling. This paper asks what happens when those fields are forced into a single 100 GtCO2/year feasibility-boundary model under an explicit 2046 abundance premise. The claim is not that nobody has thought about the pieces. The claim is that the coupled system has to be judged as a coupled system: energy, contactors, sorbents, storage, robot productivity, cost floors, carbon-cycle response, rebound, measurement, and governance all have to clear together, and the analysis should say plainly where each gate currently stands.

### 1.3 Evidence Standard

The analysis combines official climate and energy statistics, derived physical calculations, scenario models, and provisional technology signals. These do not deserve the same certainty, so every quantitative claim in this paper belongs to one of four classes.

TABLE-CAPTION: Claim classes used throughout this paper.

| Claim class | Allowed use | Examples |
|---|---|---|
| Source-backed anchor | Stated as a current external fact, with citation. | Atmospheric CO2 concentration, current emissions, current CDR scale, official energy statistics. |
| Derived calculation | Stated as arithmetic or model output with inputs visible. | Annual energy at a stated GJ/tCO2, contactor face area, storage volumes, cost at a stated $/tCO2. |
| Scenario assumption | Used to test plausibility, never asserted as forecast. | AI/robotics cost compression, clean-power allocation shares, deep-abundance cost floors. |
| Provisional signal | Treated as a lead or hypothesis until independently verified. | Company production-rate announcements, governance mechanisms, future fusion market pull. |

A claim-evidence matrix mapping the paper's main claims to evidence class, anchors, and required upgrades is maintained with the underlying model; the full parameter database, equation ledger, unit checks, and generated tables are available in the public research repository. Reported figures in this paper are rounded to the precision the underlying evidence supports.

## 2. Current State

Atmospheric CO2 is still rising. NOAA's global monthly mean was 428.5 ppm in February 2026, and the Mauna Loa monthly mean was 432.3 ppm in May 2026 (NOAA GML, 2026a, 2026b). The Global Carbon Budget projects fossil CO2 emissions of 38.1 GtCO2 in 2025 and total anthropogenic CO2 emissions of about 42.2 GtCO2/year including land use (Friedlingstein et al., 2026).

Current carbon dioxide removal is nowhere near the scale considered here. The State of Carbon Dioxide Removal report puts current global CDR at roughly 2.2 GtCO2/year, almost all from conventional land-based methods; novel CDR is around 2 MtCO2/year (State of CDR, 2026). A 100 GtCO2/year target is therefore about 45 times current total CDR and four to five orders of magnitude above current novel CDR.

That gap is the reason this paper is not written as a near-term deployment claim. The useful question is whether the gap changes character under a very strong automation and energy-abundance premise, and what would have to be demonstrated, in order, for anyone to believe that it had.

## 3. Method: An Integrated Feasibility Screening Framework

The model underlying this paper is a set of coupled first-order screens rather than a single complex simulation. That is deliberate. The purpose at this stage is to expose feasibility boundaries transparently, with every transformation auditable, before investing in full coupled carbon-cycle and industrial-learning models. Each screen is simple enough to check by hand; the discipline comes from forcing them to clear jointly.

The framework has eight component families:

- **Carbon cycle and climate response.** Stock-flow bookkeeping, a reduced-form impulse-response carbon-cycle model, a two-box climate emulator with non-CO2 forcing scenarios, and a forcing-driven run of the FAIR simple climate model as a diagnostic bridge toward publication-grade climate modeling.
- **Energy and power systems.** Capture energy intensity, optional CO2-splitting energy, annual energy and average power, portfolio capacity buildout, firm-power requirements, land and storage proxies, and explicit additionality, deliverability, and regional dispatch gates.
- **Capture hardware and materials.** Air throughput, contactor face area, fan energy under pressure-drop sensitivity, plant-equivalent counts, sorbent inventory and replacement, and a material supply-chain screen against world production of steel, cement, copper, and reactive media.
- **Storage.** A conversion and storage-state ledger across gas, supercritical, mineral-carbonate, and solid-carbon states; storage lifecycle and 100-year durability haircuts; and a regional injection-corridor screen including well counts and permitting frames.
- **Pathway portfolio.** A seven-pathway CDR portfolio compared against assessed potential, cost, and readiness ranges from the literature.
- **Cost and learning.** A delivered-cost stack decomposed into energy, plant, materials, storage, measurement, robot operations, finance, and product handling; learning curves with explicit physical floors; and capital-program comparators.
- **Robotics and automation.** Task-hour-based productivity models, field-productivity distributions, and a production-verification gate that grades robotics claims by source quality.
- **Integration, uncertainty, and governance.** A constrained 2026-2046 deployment screen, deployment timepaths through 2060, Monte Carlo and correlated-scenario uncertainty screens, rebound analysis, and an exploratory commons-governance branch.

Every equation in the framework is recorded in a dedicated ledger with dimensional unit checks, all of which pass. The unit checks do not validate the scenario assumptions; they guarantee that the headline transformations are explicit and internally consistent, which is the precondition for honest review.

## 4. Physical Feasibility

### 4.1 The Scale of 100 GtCO2 per Year

Using a conversion of 1 ppm atmospheric CO2 to about 7.8 GtCO2, gross removal of 100 GtCO2/year corresponds to about 12.8 ppm/year of atmosphere-only drawdown. Against a 42.2 GtCO2/year current-emissions baseline, the same gross removal gives 57.8 GtCO2/year net removal, or about 7.4 ppm/year. These numbers are bookkeeping, not climate outcomes: they exclude land and ocean rebound. Their value is the order of magnitude. A 100 GtCO2/year system is not an offset adjustment; it is an industrial flow larger than current annual emissions.

### 4.2 Carbon-Cycle Response

Land and ocean reservoirs do not stay passive when atmospheric CO2 changes. IPCC AR6 WGI treats the airborne fraction, carbon-cycle feedbacks, and the response to carbon dioxide removal as central constraints on future atmospheric CO2 (IPCC, 2021a), and its CDR-pulse experiments show that CO2 removed from the atmosphere is partly offset by land and ocean reservoir response (IPCC, 2021b). Zickfeld et al. (2021) further show that positive emissions and equivalent removals are not symmetric in the climate-carbon system.

The framework therefore convolves annual positive emissions and negative removals with the Joos et al. (2013) multi-model CO2 impulse-response function. Durable removals carry a 0.96 removal-effectiveness multiplier as a first caution factor, and managed scenarios apply an illustrative 350 ppm management floor: once the modeled atmospheric path reaches that range, removals throttle rather than continuing blindly. The floor is a control assumption, not a recommended target, and it matters for reading the results below: scenarios that report 350 ppm in 2100 are pinned at that value by the throttle, not driven there by independent dynamics.

FIG: carbon_cycle_atmospheric_co2_pathways.png | Reduced-form atmospheric CO2 pathways under combined emissions and removal scenarios, using the Joos et al. (2013) impulse-response function. Paths reaching 350 ppm reflect the management-floor throttle assumption.

TABLE-CAPTION: Reduced-form atmospheric CO2 pathways. Entries of 350 ppm are pinned by the management-floor control assumption.

| Scenario | 2046 CO2 (ppm) | 2050 CO2 (ppm) | 2100 CO2 (ppm) | Interpretation |
|---|---|---|---|---|
| No AETHER, constant emissions | 510 | 523 | 656 | Failure baseline: atmospheric CO2 keeps rising. |
| AETHER, constant emissions | 409 | 388 | 350 (floor) | Removal overcomes current emissions, then throttles at the floor. |
| AETHER, 58% rebound | 470 | 469 | 473 | Rebound or delayed abatement erases most of the net-negative effect. |
| AETHER plus net-zero 2050 | 372 | 350 (floor) | 350 (floor) | Strongest pathway: removal becomes managed reversal rather than offset accounting. |

The time paths change the interpretation of the target. If current emissions continue while removal ramps linearly to 100 GtCO2/year by 2046, atmospheric CO2 falls later in the century, but more slowly than atmosphere-only arithmetic implies. If emissions reach zero by 2050 while removal reaches industrial scale, the modeled system can return the atmosphere to a lower managed range this century and then reduce removal activity. If cheap removal induces rebound or delayed abatement, much of the benefit disappears.

A state-dependent extension stress-tests the fixed 0.96 effectiveness multiplier with cases in which realized removal effectiveness degrades as drawdown deepens and cumulative removals grow large relative to positive emissions. The coefficients are scenario assumptions; their job is to expose sensitivity. In the 58% rebound scenario, 2100 concentration moves from 473 ppm under the fixed multiplier to 492 ppm in the conservative state-dependent case and 526 ppm under asymmetry stress. The lesson is structural: the program cannot only show that gross removal is mechanically possible. It has to show that the gross system produces enough realized atmospheric drawdown after carbon-cycle response, lifecycle emissions, measurement buffers, and rebound behavior.

### 4.3 Climate Response

The concentration paths above are converted to temperature three ways, in increasing order of defensibility, and none of the three is yet a publication-grade climate claim.

First, a static proxy uses the AR6 effective radiative forcing for CO2 doubling, F = 3.93 x log2(C/278) W/m2 (IPCC, 2021c), with an equilibrium sensitivity of 3.0 Â°C and a transient response of 1.8 Â°C (IPCC, 2021d). Second, a two-box energy-balance emulator calibrated to the same sensitivities passes the CO2 forcing through an ocean-lag response and adds explicit non-CO2 and aerosol forcing scenarios, starting from about +1.2 W/m2 of non-CO2 forcing and -0.7 W/m2 of aerosol cooling in 2026. Third, the same forcing paths are run through FAIR 2.2.4 in forcing mode (Smith et al., 2018), initialized to the 2026 temperature state, as a diagnostic against a real package-executed response engine.

FIG: fair_forcing_execution_comparison.png | Forcing-driven FAIR temperature diagnostics compared with the screening emulator across AETHER scenarios.

TABLE-CAPTION: 2100 temperature outcomes (Â°C above pre-industrial) across the three screening layers, central configurations.

| Scenario | CO2-only transient proxy | Two-box emulator, full forcing | FAIR, forcing-driven |
|---|---|---|---|
| No AETHER, stress forcing | 2.2 | 3.2 | 4.1 |
| AETHER, 58% rebound, stress forcing | 1.4 | 2.4 | 2.9 |
| AETHER plus net-zero 2050, managed forcing | 0.6 | 1.1 | 1.2 |

Two things follow. The avoided warming attributable to removal is large in every layer, on the order of 0.9-1.7 Â°C against same-forcing baselines. And the spread between layers is itself a finding: moving from a CO2-only proxy to explicit non-CO2 forcing and a real response engine raises stress-case 2100 temperature by nearly 2 Â°C. Climate reversal is not a CO2-only control problem. Publication-grade claims require a species-level FAIR or Earth-system workflow with CH4 and N2O trajectories, aerosol precursors, land-use forcing, lifecycle-emissions traces, historical spin-up, zero-emissions-commitment diagnostics, and uncertainty ensembles. A structured handoff for that upgrade exists: a gap matrix currently tracks 16 species and forcing families, of which none are yet usable at publication grade. Closing it is the first deliverable of the proposed research program (Section 11).

### 4.4 Energy

IPCC AR6 WGIII reports a theoretical minimum energy for separating CO2 from air of about 0.5 GJ/tCO2 and current-technology total requirements of 4-10 GJ/tCO2 (IPCC, 2022b). The framework evaluates 1, 3, and 8 GJ/tCO2 capture cases, plus splitting variants. NIST lists the standard enthalpy of formation of gaseous CO2 as -393.5 kJ/mol (NIST, 2026a); reversing CO2 into carbon and oxygen therefore carries an ideal floor of about 8.94 GJ/tCO2 before any real electrochemical losses, separations, compression, or product handling.

TABLE-CAPTION: Energy requirements at 100 GtCO2/year gross removal.

| Scenario | Capture energy | Split fraction | Total energy | Annual energy | Average power |
|---|---|---|---|---|---|
| Near-thermodynamic capture and storage | 1.0 GJ/tCO2 | 0% | 1.0 GJ/tCO2 | ~28,000 TWh/y | 3.2 TW |
| Advanced capture and storage | 3.0 GJ/tCO2 | 0% | 3.0 GJ/tCO2 | ~83,000 TWh/y | 9.5 TW |
| Current DAC-like capture and storage | 8.0 GJ/tCO2 | 0% | 8.0 GJ/tCO2 | ~222,000 TWh/y | 25 TW |
| Advanced capture plus 25% splitting | 3.0 GJ/tCO2 | 25% | 5.2 GJ/tCO2 | ~145,000 TWh/y | 17 TW |
| Advanced capture plus full splitting | 3.0 GJ/tCO2 | 100% | 11.9 GJ/tCO2 | ~332,000 TWh/y | 38 TW |

FIG: energy_by_pathway_100gt.png | Annual energy demand at 100 GtCO2/year across capture and splitting cases.

The energy conclusion is harsh. Even the near-thermodynamic case requires a dedicated power system measured in terawatts. The advanced 3 GJ/tCO2 case requires roughly 98 times the entire 2025 global electricity-generation increase of just over 850 TWh (IEA, 2026a). Spread over a 20-year linear buildout, it requires adding about 4,200 TWh/year of dedicated clean generation every year, nearly five times the 2025 total global electricity increment and about seven times the 2025 solar PV increase of roughly 600 TWh (IEA, 2026a).

That does not make the target impossible. It establishes the central structural fact of this analysis: AETHER is mainly an energy and storage problem, with AI and robotics as accelerants.

### 4.5 Power-System Buildout

Energy demand must translate into installed capacity, capacity factors, land, firm supply, storage, and annual construction. The buildout screen uses NREL's Annual Technology Baseline for technology parameters (NREL, 2024a, 2024b, 2024c), NREL land-use data for utility-scale solar proxies (Ong et al., 2013), IAEA data for current nuclear scale (IAEA, 2025), IEA's geothermal outlook (IEA, 2024), and IEA Electricity 2026 for storage and flexibility anchors (IEA, 2026b).

The advanced 3 GJ/tCO2 case needs about 83,000 TWh/year delivered. Applying a 10% gross-generation adder for curtailment, storage, transmission, and auxiliary needs raises the screen to roughly 92,000 TWh/year. This is an adder to delivered demand, not a claim that losses are exactly 10%. In a balanced portfolio at current capacity factors, the nameplate requirement is about 27.5 TW: roughly 15 TW solar, 9 TW wind, 2.3 TW nuclear, and 1.2 TW advanced geothermal, including about 3.5 TW of firm clean capacity.

TABLE-CAPTION: Power-system requirements across portfolio cases.

| Portfolio | Delivered | Gross generation | Nameplate | Firm capacity | Solar land proxy | 4-h storage proxy |
|---|---|---|---|---|---|---|
| Near-thermo balanced | ~28,000 TWh/y | ~31,000 TWh/y | 9.2 TW | 1.2 TW | ~150,000 km2 | ~2,400 GWh |
| Portfolio balanced | ~65,000 TWh/y | ~71,000 TWh/y | 21 TW | 2.7 TW | ~350,000 km2 | ~5,700 GWh |
| 3 GJ balanced | ~83,000 TWh/y | ~92,000 TWh/y | 27.5 TW | 3.5 TW | ~450,000 km2 | ~7,300 GWh |
| 3 GJ solar-heavy | ~83,000 TWh/y | ~100,000 TWh/y | 39 TW | 1.3 TW | ~920,000 km2 | ~10,300 GWh |
| Full-split balanced | ~332,000 TWh/y | ~365,000 TWh/y | 109 TW | 14 TW | ~1.8 million km2 | ~29,000 GWh |

FIG: clean_energy_capacity_requirements_100gt.png | Required clean-power capacity at 100 GtCO2/year by portfolio case.

Three comparisons anchor the difficulty. Current operational nuclear capacity is about 377 GW(e), with 64.5 GW(e) under construction at the end of 2024 (IAEA, 2025); the balanced case needs firm clean capacity an order of magnitude larger. IEA's cost-effective 2050 geothermal case is about 800 GW producing almost 6,000 TWh/year if technology improves (IEA, 2024); AETHER's firm-power gap exceeds it. The solar-heavy case lowers the firm-power requirement but pushes nameplate capacity to 39 TW and the utility-scale land proxy toward 0.9 million km2. The land proxy is not a forecast, since deployment could use rooftops, deserts, agrivoltaics, offshore resources, or higher-efficiency modules, but it shows that even a market-led clean-energy path needs siting, transmission, and public legitimacy at continental scale.

The four-hour storage proxy, sized to shift 25% of average variable-renewable output, is about 7,300 GWh for the balanced case, roughly $1.1 trillion at IEA's 2024 utility-scale anchor near $150/kWh (IEA, 2026b). It is not seasonal storage and not a reliability reserve; it is a floor-level reminder that generation capacity is only one piece of the requirement. AI and robotics can accelerate solar factories, nuclear construction, geothermal drilling, and transmission work. They cannot make 24% solar capacity factors behave like firm power. The energy system is the largest coupled bottleneck in the framework.

### 4.6 Storage States and the Conversion Ledger

At 100 GtCO2/year, storage state matters as much as capture technology. Gas-phase CO2 is too bulky for planetary-scale storage; supercritical geologic storage at a representative density near 600 kg/m3 is far denser (National Academies, 2019a). NIST fluid-property data underpin the density calculations across states (Lemmon, 2009; NIST, 2026b).

TABLE-CAPTION: Annual physical quantities by storage state or product at 100 GtCO2/year.

| State or product | Mass | Volume | Added conversion energy | Reading |
|---|---|---|---|---|
| CO2 gas at STP | 100 Gt/y | ~50,500 km3/y | 0 | Not a serious storage state at this scale. |
| Supercritical CO2 | 100 Gt/y | ~167 km3/y | 0 | Plausible default, subject to geology, injection rates, pressure, monitoring, and liability. |
| Solid carbon from full splitting | ~27 Gt/y | ~12 km3/y | ~248,000 TWh/y | Compact, but carries the 8.94 GJ/tCO2 ideal splitting burden before real losses. |
| Liquid O2 coproduct of full splitting | ~73 Gt/y | ~64 km3/y | coupled to splitting | Product handling unsafe at scale; atmospheric release likely preferable. |
| Magnesite-equivalent mineral carbonate | ~192 Gt/y | ~64 km3/y | pathway-specific | Durable and dense, but constrained by reactive minerals, grinding, transport, kinetics, water, and land. |

FIG: conversion_storage_ledger_100gt.png | Conversion and storage-state ledger at 100 GtCO2/year.

The ledger argues against full CO2 splitting as a default plan. The splitting energy alone, about 248,000 TWh/year at 100 GtCO2/year, exceeds the entire capture budget of the advanced case by a factor of three. The product streams are also extreme: about 27 Gt/year of solid carbon is roughly 15,000 times current world natural graphite production of 1.8 Mt/year and about 34 times reported recoverable natural graphite resources, every year (USGS, 2026; OSHA, 2020). Mineral carbonation avoids the oxygen coproduct and is highly durable, with a magnesite-equivalent proxy of about 192 Gt/year of carbonate product (PubChem, 2026), but shifts the bottleneck into mineral supply, mining, grinding, transport, kinetics, water, and local environmental governance.

The conclusion is narrow: most removal should use geologic storage, in situ mineralization, or ocean-alkalinity pathways where safe. Splitting remains a specialized option for industrial carbon products or closed-loop processes, not a base case, unless energy becomes extraordinarily cheap and product handling is engineered explicitly.

### 4.7 Air Throughput, Contactors, and Sorbents

The dilution problem is physical, not economic. At 428.5 ppm, ambient air holds about 0.83 grams of CO2 per cubic meter. The National Academies' DAC chapter provides the engineering anchor: at 1.5 m/s face velocity and 75% capture, a 1 MtCO2/year contactor needs about 38,000 m2 of cross-sectional area (National Academies, 2019b), with Keith et al. (2018) as the engineered 1 MtCO2/year process comparator.

TABLE-CAPTION: Air throughput and contactor scale. The 100 Gt all-air rows are stress tests; the current portfolio assigns 40 GtCO2/year to DAC.

| Case | Air flow | Contactor face area | Fan electricity | 1 Mt/y plant equivalents |
|---|---|---|---|---|
| 40 Gt/y DAC, NASEM reference | ~2.3 billion m3/s | ~1,500 km2 | ~3,700 TWh/y | 40,000 |
| 40 Gt/y DAC, low-pressure design | ~2.0 billion m3/s | ~650 km2 | ~2,200 TWh/y | 40,000 |
| 100 Gt/y all-air, NASEM reference | ~5.7 billion m3/s | ~3,800 km2 | ~9,300 TWh/y | 100,000 |
| 100 Gt/y all-air, low-pressure design | ~4.9 billion m3/s | ~1,600 km2 | ~5,600 TWh/y | 100,000 |
| 100 Gt/y all-air, high-pressure warning | ~7.5 billion m3/s | ~7,500 km2 | ~130,000 TWh/y | 100,000 |

FIG: air_contactor_physical_scale_100gt.png | Physical scale of air contactors across design cases.

Scale markers make the factory problem concrete. 1PointFive's STRATOS is designed for up to 500,000 tCO2/year when fully operational (1PointFive, 2026); Climeworks' Mammoth is up to 36,000 tCO2/year nameplate (Climeworks, 2024). Even the 40 GtCO2/year DAC branch of the portfolio implies about 80,000 STRATOS-scale facility equivalents. These comparisons are not criticisms of either company. They mean that extrapolating from first commercial plants to climate-relevant scale requires a factory-rate model, not a multiplication sign.

The pressure-drop sensitivity is the design lesson. Between the low-pressure and high-pressure 100 Gt cases, fan electricity alone moves from about 5,600 to about 130,000 TWh/year. AI-designed contactors and sorbents matter only if they reduce real pressure drop, fouling, cycle time, thermal load, and maintenance. A better model cannot make a bad contactor cheap.

Solid sorbents add an inventory problem. Under NETL-style reference loadings, the 100 Gt all-air case needs about 150 Mt of sorbent inventory and 75 Mt/year of replacement (Patel et al., 2025; National Academies, 2019b). An improved-sorbent case lowers that to about 35 Mt and 7 Mt/year, but that is a research target, not a current materials claim.

### 4.8 Materials and Supply Chains

A removal system this large is built from steel, cement, copper, sorbents, solvents, membranes, catalysts, fans, compressors, pipelines, and drilling equipment. WRI's review makes the point directly: DAC plants require concrete, steel, plastic, aluminum, and copper, and upstream impacts matter in high scale-up scenarios (WRI, 2024). World crude steel production was about 1,885 Mt in 2024 (World Steel Association, 2025); world cement production was about 4,000 Mt (USGS, 2025); and energy-transition copper demand is already growing against constrained supply (IEA, 2025a).

TABLE-CAPTION: Material screen at 100 GtCO2/year (20-year buildout where applicable).

| Screen item | Annual demand | Share of world production comparator | Evidence class |
|---|---|---|---|
| Legacy NaOH solvent makeup, 0.17-0.29 t/tCO2 | 17,000-29,000 Mt/y | 4-7x world cement production | Source-backed critique scaled to the AETHER target |
| DAC replacement media at 0.5% per tonne | 200 Mt/y | 5% of world cement production | Scenario assumption informed by DAC material-risk literature |
| DAC replacement media at 2% per tonne | 800 Mt/y | 20% of world cement production | Scenario assumption informed by DAC material-risk literature |
| Power-system copper | ~3 Mt/y | ~10% of refined copper production | Scenario assumption with IEA critical-minerals context |
| Power-system steel | ~69 Mt/y | ~3.6% of world crude steel | Scenario assumption with source-backed comparator |
| Contactor structural steel | ~19 Mt/y | ~1% of world crude steel | Scenario assumption with source-backed comparator |

FIG: material_supply_chain_pressure.png | Material and industrial supply-chain pressure at 100 GtCO2/year.

The reactive-media row is the sharpest result. Chatterjee and Huang (2020) report NaOH makeup rates of 0.17-0.29 t per tCO2 in a large-deployment DAC case. Scaled to 100 GtCO2/year, that is several times current world cement production in caustic soda alone. Legacy high-makeup solvent chemistry is therefore not a plausible base case at this scale under any automation assumption. The optimistic case is not that materials stop mattering; it is that AI-assisted chemistry, closed-loop media recovery, longer sorbent lifetimes, and automated recycling push replacement rates down by orders of magnitude. Even then, replacement media at 0.5-2% per tonne is a 200-800 Mt/year chemical industry that must be cheap, low-toxicity, recyclable, and low-carbon.

Structural materials read as a major but conceivable industrial allocation. Reactive media and copper read as gating constraints. The next model layer must replace pathway-level cost buckets with pathway-specific bills of materials, replacement schedules, and commodity competition against the rest of the energy transition.

## 5. From Gross Removal to Creditable Removal

A gross captured tonne is an engineering output. A durable tonne is a physical climate claim after lifecycle and permanence. A creditable tonne is a governance claim: someone is allowed to count it. The distinctions are not academic. At this scale a ten-percent error between those categories is ten gigatonnes per year. This section follows one hundred gross gigatonnes through the filters.

### 5.1 Pathway Portfolio Against Assessed Ranges

The target should not be read as a DAC-only proposal. IPCC AR6 WGIII reports very different cost, potential, maturity, and risk profiles across CDR methods (IPCC, 2022a), and the National Academies treat ocean approaches as important but research-constrained (National Academies, 2022). The portfolio allocates: 40 Gt/y DAC with geologic storage, 20 Gt/y enhanced weathering and mineralization, 15 Gt/y ocean alkalinity enhancement, 10 Gt/y BECCS, 6 Gt/y biochar, 5 Gt/y afforestation and reforestation, and 4 Gt/y direct ocean and electrochemical capture.

FIG: pathway_source_ranges_vs_aether.png | AETHER portfolio allocations compared with assessed potential ranges from the literature.

Compared against assessed ranges, the portfolio is openly aggressive, and that should be stated as a finding rather than buried as a caveat: the 100 GtCO2/year total requires upper-tail performance from essentially every pathway at once. DAC at 40 Gt/y sits at the top of the IPCC assessed potential range of 5-40 Gt/y, so it cannot absorb slippage elsewhere. Enhanced weathering at 20 Gt/y is five times the central assessed estimate of 2-4 Gt/y, although inside the very wide full literature range. BECCS at 10 Gt/y and biochar at 6 Gt/y sit near their upper assessed ranges. Ocean alkalinity at 15 Gt/y is inside its assessed range but at low technology readiness, and must survive marine chemistry, ecology, and governance review. The electrochemical ocean allocation is a placeholder pending method-specific ranges. The sum of central assessed potentials is about 37.5 Gt/y, against 107.6 Gt/y for the high ends.

In current model output the portfolio totals roughly $8.4 trillion/year, 56,500 TWh/year, a weighted energy intensity of 2.0 GJ/tCO2, and a weighted cost of $84/tCO2. It should be treated as a stress-test portfolio. If a 100 Gt/y portfolio cannot be turned into a governed industrial system, the number is rhetoric; if it can, the project resembles a global infrastructure program more than a carbon-removal company.

### 5.2 Storage Lifecycle and 100-Year Durability

The storage resource headline is encouraging but incomplete. USGS estimates a mean technically accessible U.S. geologic storage resource near 3,000 GtCO2 (USGS, 2013). IPCC AR6 puts theoretical global geologic storage near 10,000 GtCO2, with usable storage lower, capacity concentrated in saline aquifers, and injection often pressure-limited even where resource is large; well-managed sites show very low estimated leakage (IPCC, 2022c). A USGS review adds the institutional warning: required volumes far exceed everything injected to date, and pressure management, induced seismicity, liability, and property rights can bind before pore space does (Anderson, 2017).

Applying route-specific lifecycle penalties and 100-year retention haircuts, the 100 Gt/y gross portfolio yields about 85 Gt/y of 100-year durable removal. Holding the same mix, about 118 Gt/y of gross removal would be needed to credit 100. Storage and lifecycle energy add roughly 8,200 TWh/year to the portfolio energy screen, bringing it to about 65,000 TWh/year.

### 5.3 Regional Storage and Injection Corridors

Storage is regional. There is no "global storage capacity" to inject into; there are source-to-sink corridors with wells, compression, pipelines or shipping, brine and pressure management, pore-space rights, monitoring, and a regulator willing to permit the operation.

A first corridor screen allocates the portfolio's 54 Gt/y geologic component across regional archetypes. The U.S. rows are anchored to the USGS national assessment, which concentrates 59% of U.S. capacity in the Gulf Coast region (USGS, 2013), with North American context from NETL's Carbon Storage Atlas (NETL, 2015). Non-U.S. rows are scenario placeholders pending regional basin sources. The result that survives any allocation: at 1 MtCO2/year per pressure-adjusted injection well, the 54 Gt/y target needs about 72,000 well equivalents globally; at 0.25 Mt/y per well, about 287,000. The U.S. permitting frame makes the institutional scale visible. EPA Class VI wells require individual applications covering site characterization, plume and pressure-front modeling, corrective action, monitoring, financial responsibility, and post-injection care (EPA, 2026a, 2026b); the U.S. rows alone imply on the order of 33,000 Class VI permit-equivalent wells.

FIG: regional_storage_injection_corridors.png | Regional storage allocation, proxy capacity, and injection-corridor requirements for the geologic component.

Capacity is therefore necessary but not sufficient. Storage needs its own model: basin-level capacity and permeability, injection-rate distributions, pressure management, brine handling, transport routes, legacy-well corrective action, pore-space ownership, induced-seismicity screening, long-term liability, and community consent.

### 5.4 Measurement, Reporting, Verification, and Credit Integrity

The credit-integrity filter applies provisional discounts for measurement uncertainty, method uncertainty, reversal and leakage buffers, and credit-invalidation reserves on top of the lifecycle screen. The anchors are institutional rather than numeric: EPA Class VI and Subpart RR define a concrete U.S. geologic MRV frame (EPA, 2026a, 2026c); the EU Carbon Removals and Carbon Farming regulation defines a certification frame with third-party verification (European Commission, 2024); the Oxford offsetting principles push toward durable, low-reversal removals (Axelsson et al., 2024); and the National Academies keep ocean methods in a research-gap posture (National Academies, 2022).

TABLE-CAPTION: From gross to creditable removal by pathway, provisional MRV assumptions.

| Pathway | Gross (Gt/y) | 100-year durable (Gt/y) | Creditable (Gt/y) | Gross required per credited tonne |
|---|---|---|---|---|
| DAC with geologic storage | 40.0 | 37.6 | 34.6 | 1.16x |
| Direct ocean and electrochemical capture | 4.0 | 3.5 | 2.9 | 1.38x |
| BECCS | 10.0 | 8.0 | 6.8 | 1.47x |
| Enhanced weathering and mineralization | 20.0 | 17.6 | 11.8 | 1.70x |
| Ocean alkalinity enhancement | 15.0 | 12.1 | 7.1 | 2.11x |
| Biochar | 6.0 | 4.0 | 2.5 | 2.45x |
| Afforestation and reforestation | 5.0 | 2.1 | 0.8 | 6.48x |

FIG: mrv_credit_integrity_overbuild.png | Gross-to-creditable overbuild requirements under provisional MRV buffers.

Under these assumptions the 100 Gt/y gross portfolio credits about 66 Gt/y. To credit 100, gross removal must rise to roughly 150 Gt/y at the same mix. Geologic storage performs best because its boundary is observable. Diffuse land and ocean pathways may still be valuable, but they should not be treated as fungible credit until the measurement and reversal problem is solved. A program that sells gross tonnes as creditable tonnes is an offset machine with better branding. The serious version requires adversarial MRV, public registries, invalidation rules, liability reserves, and a willingness to reject cheap credits that cannot survive measurement.

### 5.5 Lifecycle Emissions

Operational energy emissions and embodied emissions are a separate filter. The screen uses four electricity-emissions cases and pathway-specific placeholder burdens for construction, media replacement, transport, storage, and decommissioning (WRI, 2024).

TABLE-CAPTION: Lifecycle-emissions sensitivity at 100 GtCO2/year gross removal.

| Power-grid intensity | Lifecycle emissions | Durable after LCA | Creditable after LCA and MRV | Gross needed for 100 creditable |
|---|---|---|---|---|
| 5 kgCO2/MWh | ~11 Gt/y | ~85 Gt/y | ~66 Gt/y | ~151 Gt/y |
| 25 kgCO2/MWh | ~12 Gt/y | ~84 Gt/y | ~65 Gt/y | ~153 Gt/y |
| 100 kgCO2/MWh | ~17 Gt/y | ~79 Gt/y | ~61 Gt/y | ~163 Gt/y |
| 250 kgCO2/MWh | ~27 Gt/y | ~70 Gt/y | ~53 Gt/y | ~187 Gt/y |

In the 25 kgCO2/MWh case, about 1.619 GtCO2e/year comes from power and roughly 10.678 GtCO2e/year from provisional non-power construction, media, transport/storage, and decommissioning terms. Those non-power terms dominate and require pathway-specific LCAs. In the 25 kgCO2/MWh case, about 1.619 GtCO2e/year comes from power and roughly 10.678 GtCO2e/year from provisional non-power construction, media, transport/storage, and decommissioning terms. Those non-power terms dominate and require pathway-specific LCAs. In the 25 kgCO2/MWh case, about 1.619 GtCO2e/year comes from power and roughly 10.678 GtCO2e/year from provisional non-power construction, media, transport/storage, and decommissioning terms. Those non-power terms dominate and require pathway-specific LCAs. In the 25 kgCO2/MWh case, about 1.619 GtCO2e/year comes from power and roughly 10.678 GtCO2e/year from provisional non-power construction, media, transport/storage, and decommissioning terms. Those non-power terms dominate and require pathway-specific LCAs. In the 25 kgCO2/MWh case, about 1.619 GtCO2e/year comes from power and roughly 10.678 GtCO2e/year from provisional non-power construction, media, transport/storage, and decommissioning terms. Those non-power terms dominate and require pathway-specific LCAs. The dirtier-grid rows are failure boundaries, not designs. They show why cheap energy is not enough: the energy must be additional, low-carbon on the margin, and not displaced from other decarbonization uses. The reporting standard that falls out of Sections 5.2-5.5 applies to every scenario in this paper: report gross capture, lifecycle emissions, 100-year durable removal, and creditable removal. Anything less hides the climate accounting.

## 6. Cost, Capital, and Clean-Power Deliverability

### 6.1 Cost Arithmetic

At 100 GtCO2/year, every $10/tCO2 is $1 trillion per year. A price acceptable in a niche carbon-credit market becomes a macroeconomic quantity at this scale: $500/tCO2 implies $50 trillion/year, $100 implies $10 trillion/year, $25 implies $2.5 trillion/year. The scenario bands used throughout are a current DAC-like case near $525-600/tCO2, an advanced case near $90/tCO2, and a near-thermodynamic case near $35/tCO2, with corresponding capacity capex of roughly $120, $40, and $15 trillion for the full system. These are scenario assumptions that illustrate the cost collapse required. If current DAC-like costs persist, the target is not economically plausible. If costs reach $10-50/tCO2, annual spending enters the same rough order as global energy, defense, or health spending.

There is also a hard energy floor under any learning curve. At $10/MWh electricity, a 1 GJ/tCO2 system has an energy-cost floor of about $2.80/tCO2; 3 GJ/tCO2 implies $8.30; 8 GJ/tCO2 implies $22. Full splitting adds about 2,500 kWh/tCO2, roughly $25/tCO2 at $10/MWh before losses. At $30/MWh those floors triple. Very low removal costs require both low energy intensity and cheap clean power. Robotics can cut labor and construction costs; it cannot erase the energy bill.

### 6.2 The Cost Stack

Whole-system numbers hide the engineering question, which is which cost buckets can collapse and which hit floors. The stack decomposes delivered cost into energy, plant and contactors, sorbents and materials, compression-transport-storage, MRV and liability, robot operations, finance and overhead, and product handling.

TABLE-CAPTION: Delivered cost stack by scenario ($/tCO2).

| Scenario | Energy | Plant | Materials | Storage | MRV | Robot O&M | Finance | Product | Total |
|---|---|---|---|---|---|---|---|---|---|
| Current DAC-like | 156 | 170 | 80 | 35 | 15 | 65 | 85 | 0 | 606 |
| Automation push | 20 | 24 | 10 | 14 | 5 | 4 | 9 | 0 | 86 |
| Moonshot modular | 8 | 10 | 5 | 8 | 3 | 2 | 4 | 0 | 40 |
| Full splitting | 116 | 20 | 8 | 8 | 5 | 5 | 10 | 45 | 217 |
| Abundance floor | 4 | 6 | 3 | 5 | 2 | 2 | 3 | 0 | 24 |

FIG: cost_stack_by_scenario.png | Delivered cost stack by scenario at 100 GtCO2/year.

The automation-push case is a sevenfold reduction from the current DAC-like stack. That is not one miracle; it requires cheap clean energy, lower energy intensity, modular manufacturing, better sorbents, faster construction, cheaper storage logistics, lower monitoring cost, and lower finance friction simultaneously. The full-splitting row shows the danger of optimizing the wrong variable: compact stored carbon at $217/tCO2 because energy and product handling dominate. The deep-abundance floor of about $24/tCO2, $2.4 trillion/year at full scale, is the kind of number that makes the program economically imaginable, and reaching it requires the entire industrial stack to work, not a lower labor bill.

For calibration, a $1 trillion/year research and deployment program would be comparable to all U.S. R&D performance, about $940 billion in 2023 (NCSES, 2025), and nearly five times current global public plus corporate energy R&D (IEA, 2026c). This is not a climate-tech startup category. It is closer to a standing industrial-science mobilization.

### 6.3 Learning Curves and Their Floors

The optimistic case leans on learning curves and scale economies, and both are real but bounded (Wright, 1936; Thompson, 2012). Moving from current novel CDR near 2 MtCO2/year to 100 GtCO2/year is about 15.6 capacity doublings. From a $500/tCO2 starting point, a 15% learning rate lands near $40/tCO2; 20% or better collides with the combined energy-storage-MRV floor near $20/tCO2 in the 3 GJ/tCO2, $10/MWh case, after which further manufacturing learning does nothing unless energy intensity, power price, storage, or monitoring also improve. Software-style cost expectations do not transfer to the physical economy; thermodynamics and infrastructure floors eventually dominate.

Plant-level scale economies have the same shape. A 1 Mt/y plant equivalent means 100,000 plants at full scale; a 10 Mt/y hub means 10,000; a 100 Mt/y mega-hub still means 1,000. Larger hubs lower unit capex but concentrate land, air, transmission, storage, water, safety, and permitting constraints. The plausible architecture is neither tiny modules everywhere nor a few mega-sites, but regional portfolios matched to energy and storage geology.

### 6.4 Clean-Power Additionality and Deliverability

Market-driven clean energy is the strongest favorable trend in the analysis. In 2024, new utility-scale onshore wind averaged $0.034/kWh and solar $0.043/kWh globally, and 91% of newly commissioned utility-scale renewable capacity was cheaper than the cheapest new fossil alternative (IRENA, 2025). Global electricity generation grew more than 850 TWh in 2025 with solar contributing about 600 TWh, while fossil generation declined (IEA, 2026a). Texas led U.S. wind generation in 2024 with about 28% of the national total under a market-led model (EIA, 2025), while California's policy-heavy approach reached 62% clean shares (CEC, 2025). Firm-power market pull is visible in data-center procurement: the Three Mile Island Unit 1 restart for Microsoft (Constellation, 2024), Google's agreement with Kairos Power for up to 500 MW of advanced nuclear (Google, 2024), and Helion's fusion power purchase agreement (Helion, 2023), against a fusion industry that drew $2.6 billion of investment in a year (FIA, 2025). These are megawatt-to-gigawatt signals against a terawatt requirement, but they are building the licensing, financing, and modular-construction machinery that removal infrastructure would later use.

None of that growth can simply be claimed. Interconnection queues already strand large amounts of U.S. generation and storage (Berkeley Lab, 2025), data-center demand is projected to roughly double toward 950 TWh by 2030 (IEA, 2025b), and ordinary electrification has first claim on clean supply. The framework therefore treats delivered, additional clean power as an explicit falsification gate: compounding clean-generation additions over twenty years, then applying factors for ordinary-demand claims, dedication to removal, additionality, interconnection, transmission and siting, hourly matching, and firm supply.

TABLE-CAPTION: Clean-power deliverability gate at the 3 GJ/tCO2 requirement (~92,000 TWh/y gross).

| Case | Delivered additional clean power | Removal scale powered | Passes 100 Gt/y gate |
|---|---|---|---|
| Status quo friction | ~290 TWh/y | 0.3 Gt/y | no |
| Market unlocked | ~5,900 TWh/y | 6.4 Gt/y | no |
| Dedicated AETHER corridors | ~41,200 TWh/y | 45 Gt/y | no |
| Firm clean backbone | ~41,000 TWh/y | 45 Gt/y | no |
| Upper-tail AI energy abundance | ~124,000 TWh/y | 136 Gt/y | yes |
| Nonadditional grid pull | ~240 TWh/y | 0.3 Gt/y | no |

FIG: clean_power_deliverability_gate.png | Clean-power deliverability gate across cases.

A companion regional dispatch screen, using seven regional archetypes and a representative 24-hour day, is stricter still: a market regional reference supports about 16 Gt/y, dedicated corridors about 48, a firm colocated backbone about 64, and only the upper-tail abundance case clears 100 with 98% hourly matching. One case in six passes the deliverability gate; one in five passes the dispatch screen.

The discipline this imposes is the right one. Cheap clean energy in general is not removal power in particular. Every modeled tonne should report whether its electricity is additional, deliverable, low-carbon on the margin, and not taken from ordinary decarbonization. If regional hourly modeling cannot deliver additional low-carbon power at the required scale, the program does not keep its 100 Gt/y headline; it caps feasible removal at delivered power, builds dedicated firm clean infrastructure, or slows the deployment path.

## 7. Robotics and AI as Accelerants

### 7.1 The Evidence Standard for Robotics Claims

The robotics premise is easy to state badly. The weak version says cheap humanoids will exist, so the project becomes easy. The serious version asks which physical bottlenecks robots can actually move: laboratory throughput, module manufacturing, construction, drilling, field maintenance, monitoring, logistics, and sensor deployment.

The verified base is real but limited. The International Federation of Robotics reports 542,000 industrial robot installations in 2024 and an operational stock of 4.7 million (IFR, 2025). Amazon reports more than 750,000 mobile robots deployed in its operations (Quinlivan, 2024). Beyond that, the evidence quality drops a tier: humanoid production claims are company-primary statements, not audited statistics. Figure's announcements describe a first-generation manufacturing line designed for up to 12,000 humanoids/year and report over 350 robots delivered with stated cycle-time and yield figures (Figure AI, 2025, 2026); Agility has announced a humanoid factory (Agility Robotics, 2023); Unitree lists a low-cost humanoid platform (Unitree, 2026). This paper treats all company-primary claims as market signals. A press release is not a field-productivity measurement, and no scenario below is allowed to depend on one.

### 7.2 Field Productivity, Not Unit Count

The productivity model deliberately changes the variable from robot count to useful autonomous task-hours by task family, mapped to robot classes with unit cost, annual useful hours, lifetime, maintenance, supervision ratio, and integration overhead. Direct robot-hour costs span roughly $25/hour for early field humanoids down toward $1-3/hour for mass-manufactured, highly utilized industrial classes. An order-of-magnitude decline in robot-hour cost is plausible under aggressive manufacturing scenarios. Cheap robot hours are still not cheap tonnes: if each tonne still needs clean power, sorbent replacement, storage monitoring, insurance, and capital, the tonne stays expensive. The defensible claim is narrower and stronger: robotics can compress the automatable share of the cost stack and accelerate deployment; it cannot beat thermodynamics.

A field-productivity stress test then discounts task-hours for field uptime, autonomy success rates, task fit, maintenance drag, and supervision overhead, sampling across distributions.

TABLE-CAPTION: Robotics requirements before and after field-productivity stress, annual production flow including replacement.

| Scenario | Production need before stress | Median after stress | P10-P90 after stress | Multiple of 2024 industrial installations |
|---|---|---|---|---|
| High robot intensity | ~1.5 million/y | ~13 million/y | 11-17 million/y | ~24x |
| AETHER automation push | ~234,000/y | ~840,000/y | 750,000-950,000/y | ~1.6x |
| Deep modular abundance | ~53,000/y | ~116,000/y | 108,000-126,000/y | ~0.2x |

FIG: robotics_field_productivity_distribution_gate.png | Field-productivity distribution stress test for robot production requirements.

The middle case carries the argument. Before stress, the automation-push scenario needs fewer robots per year than the world already installs. After realistic discounts for uptime, autonomy success, and supervision, the median requirement rises to about 1.6 times current annual industrial installations, roughly twenty first-generation humanoid-line equivalents at announced capacities. The high-intensity case becomes a warning label at about 24 times current installations. The deep-modular case is easy on count but assumes the strongest claim of all: that climate infrastructure has been redesigned around robot-native factories, controlled logistics, automated construction, and dense sensor networks.

None of this proves the robotics premise. It defines what proving it would require: task-family productivity distributions measured in field conditions, not unit prices, factory cadence, or fleet-size announcements.












<!-- AETHER-PUBLIC-RELEASE:proposal-scenarios:BEGIN -->
### 7.3 External AI Scenario Benchmarks and What They Do Not Prove

AETHER's 2046 abundance premise is not sourced from any single AI forecast. Three prominent scenario projects bracket parts of the timing and governance envelope, but none validates the engineering inputs in this paper.

TABLE-CAPTION: External AI scenarios as boundary cases for AETHER, not physical-deployment evidence.

| Source | Scenario status | Capability and acceleration premise | Physical-world boundary | AETHER use |
|---|---|---|---|---|
| Situational Awareness | Argumentative forecast | AGI around 2027 and superintelligence by the end of the decade through compute, algorithms, and automated AI research. | AI R&D can accelerate virtually before robotics; power and compute remain binding. | Fast-capability and mobilization stress branch only. |
| AI 2027 | Forecast scenario; best guess at publication | Expert-human AI and automated AI R&D in 2027, followed by rapid recursive acceleration. | Uncertainty compounds beyond the near term; software acceleration does not establish field productivity. | Short-timeline branch; independently gate robots, power, and storage. |
| AI 2040: Plan A | Normative scenario and policy recommendation | Default AI R&D automation in 2030, governed scaling, and delayed superintelligence in 2040. | Physical labor follows cognitive labor and still needs automated supply chains, energy, and infrastructure. | Governance-bounded abundance branch. |
| AETHER | Conditional engineering screen | AI scientists, robotic physical labor, clean energy, storage, and measurement improve together by 2046. | Power, contactors, materials, storage, MRV, capital, and governance are explicit gates. | Test the coupled physical system; do not inherit scenario claims as data. |

Situational Awareness is useful because it explicitly separates rapid virtual AI research from slower robotics and names power as an industrial constraint (Aschenbrenner, 2024). AI 2027 offers a short-timeline branch but also acknowledges that its uncertainty grows sharply beyond the near-term scenario (Kokotajlo et al., 2025). AI 2040: Plan A is primarily a recommendation, not a prediction, and its economics makes physical abundance conditional on robots, supply chains, energy, and infrastructure rather than cognition alone (Larsen et al., 2026).

These scenarios widen the plausible timing envelope. They do not source AETHER's engineering parameters. Field robot productivity, clean-power deliverability, materials, storage, lifecycle emissions, MRV, and rebound remain independent gates.
<!-- AETHER-PUBLIC-RELEASE:proposal-scenarios:END -->

## 8. Integrated Feasibility and Uncertainty

### 8.1 The Integrated 2026-2046 Screen

The component screens matter jointly. For each scenario, actual removal capacity in each year is the minimum of five constraints: the planned ramp to 100 GtCO2/year, clean electricity available to removal, robot supply in service, storage capacity, and budget capacity at the learned cost per tonne. Remaining emissions and rebound are then subtracted. This is a constraint audit, not a forecast.

TABLE-CAPTION: Integrated feasibility screen, 2026-2046. Ratios are constraint headroom at 100 Gt/y (1.0 = exactly binding).

| Scenario | Result | 2046 capacity | Energy ratio | Robot ratio | Storage ratio | Budget ratio | Net at 100 Gt/y |
|---|---|---|---|---|---|---|---|
| Reference extrapolation | fails | 3.1 Gt/y | 0.03 | 0.10 | 0.25 | 0.11 | 17 Gt/y |
| Fast learning, energy constrained | fails | 19.6 Gt/y | 0.20 | 1.8 | 0.60 | 0.44 | 50 Gt/y |
| AETHER portfolio push | passes screen | 100 Gt/y | 1.2 | 14 | 1.1 | 1.1 | 70 Gt/y |
| Moonshot low-energy | passes screen | 100 Gt/y | 2.0 | 55 | 1.2 | 1.7 | 90 Gt/y |
| High-rebound failure | builds, fails climate | 100 Gt/y | 1.2 | 14 | 1.1 | 1.1 | 5 Gt/y |

FIG: integrated_capacity_paths_2026_2046.png | Integrated capacity paths under the five constraint sets, 2026-2046.

The reference case fails for the expected reason: moderate learning and moderate automation do not create enough energy, robots, storage, or budget headroom. The fast-learning case still fails because clean electricity and storage do not scale fast enough; robots are not the binding constraint. The first passing scenario requires several strong assumptions simultaneously: portfolio energy intensity near 2 GJ/tCO2, about 56,500 TWh/year of dedicated clean generation by 2046, storage throughput above 100 Gt/y, robot supply at roughly 50 robots per Mt/y of capacity, annual spending near $9 trillion, emissions down to 15 Gt/y, and rebound held to 15%. The high-rebound row is the political warning: the physical buildout can succeed while the climate result fails.

### 8.2 Deployment Timepaths

Endpoint screens still miss timing. The timepath layer tracks annual gross capacity, durable credit, cumulative durable credit, residual emissions, and rebound through 2060. A linear ramp to 2046 accumulates about 1,500 Gt of durable credit by 2060; an abundance-accelerated ramp reaching scale by 2040 accumulates about 2,000 Gt; an energy-delayed buildout accumulates about 640 Gt and is net-positive in 2046; a rebound-failure case builds nearly full hardware while delivering approximately zero net climate value in 2046. The program has to be judged on cumulative durable net removal, not terminal gross capacity. A late system is not the same as an early one, and a gross system is not the same as a durable one.

FIG: deployment_timepath_capacity_and_cumulative.png | Deployment timepaths: annual capacity and cumulative durable removal, 2026-2060.

### 8.3 Uncertainty: Screens, Not Probabilities

A Monte Carlo layer samples 20,000 draws across explicit triangular ranges for energy intensity, clean-energy growth, robot manufacturing, storage throughput, cost, durability, residual emissions, rebound, and execution quality. The ranges are hand-set and documented in a distribution-evidence registry that grades each input and names its upgrade path; eleven of fifteen inputs are flagged priority-one for replacement with sourced distributions or expert elicitation. The outputs are model triage, not calibrated probabilities, and this paper deliberately does not lead with them.

What the screen is good for is the shape of failure. Reaching 100 Gt/y of durable credit is an upper-tail outcome under independent sampling; the median durable credit across draws is about 31 Gt/y. Clean energy is the binding constraint in two-thirds of failed draws. The strongest correlates of a good net climate result are clean-energy growth and allocation on the positive side, and residual emissions and rebound on the negative side, ahead of any robotics variable.

Independent sampling is also too kind. A real program would not draw clean power, robot productivity, storage, durability, rebound, and execution from separate worlds; abundance tends to arrive together or fail together. A correlated-families screen makes the point sharply: under a clustered-failure family no draws reach the durable target and the median net result is negative, while under a jointly favorable abundance family a majority of draws clear it.

FIG: correlated_uncertainty_success_frontier.png | Correlated scenario families: success rates when related assumptions move together rather than independently.

That is the honest feasibility boundary. The target does not usually fail at the first-order mass-and-energy arithmetic layer. It fails because the abundance premise has to arrive as a coupled industrial package, and the analysis can name the couplings: clean-power growth with allocation and deliverability; robot manufacturing with field productivity and execution; storage throughput with measurement burden and durability; budget with rebound, residual emissions, and governance.

## 9. Rebound, Governance, and the Commons

Jevons-type rebound is the central governance risk, not a footnote (Sorrell, 2009; Alcott, 2005). Cheap removal can reduce political pressure to cut emissions and make firms and governments more willing to use the atmospheric sink on the assumption that cleanup will be available. The arithmetic is unforgiving and depends on the accounting layer. Against a 42.2 Gt/y emissions baseline, a 100 Gt/y gross system has a simple break-even rebound threshold of 57.8% of gross. In the 25 kgCO2/MWh lifecycle case, the threshold falls to 41.7% after LCA and 23.1% after provisional LCA+MRV accounting. Above the relevant threshold, the program is net-positive for the atmosphere despite enormous cleanup capacity. The high-rebound rows in Sections 4.2 and 8.1 are the same failure seen from the carbon cycle and from the industrial system.

FIG: jevons_rebound_sensitivity_100gt.png | Net removal as a function of rebound or delayed-abatement fraction.

This is why the analysis includes an exploratory governance branch rather than treating institutions as someone else's problem. The structural issue is ownership: nobody holds a clean property claim over the atmosphere or oceans, so harmful outputs are dumped into shared systems without compensation. The public trust doctrine preserves certain natural resources for public use with government as trustee (Cornell LII, 2026), atmospheric-trust arguments extend that logic to climate systems, contested and uneven across jurisdictions (Georgetown Environmental Law Review, 2023), and Ostrom's work shows that common-pool resources can sometimes be governed by rules, monitoring, sanctions, and nested institutions rather than privatization or neglect (Ostrom, 1990).

The branch tests a concrete mechanism set: shared sinks held by citizens or trusts; emitters paying for permitted sink use at rates tied to quantity, persistence, and risk; outright prohibition of outputs too dangerous to price; revenues returned as citizen dividends or invested in removal; removal credits interacting with sink fees only through verified durable storage; and liability for leakage, ecological damage, and measurement fraud. The failure modes are named alongside it. A price set too low becomes a permission slip. A dividend can make governments fiscally dependent on pollution revenue. Cross-border enforcement is genuinely hard. The branch is exploratory, but the underlying point is not: technical capacity without sink governance is a larger, cleaner-looking version of the same externality problem.

## 10. Feasibility Gates and the Falsification Standard

The analysis compresses into a gate scorecard. No single gate failing makes the idea worthless, and no single gate passing makes it real; the claim structure is the stack.

TABLE-CAPTION: Feasibility gate scorecard.

| Gate | Status | Quantitative anchor | Required next proof |
|---|---|---|---|
| Climate target arithmetic | conditional pass | Break-even rebound: 57.8% gross; 41.7% after LCA; 23.1% after LCA+MRV | Policy and market design that keeps removal additional rather than permissive. |
| Carbon-cycle outcome | research gap | 350 ppm is an imposed management floor; species-level FAIR gates still fail | Full species-level FAIR or Earth-system modeling. |
| Climate response | research gap | Stress-case spread of ~2 Â°C between screening layers | Species-level forcing inputs, ensembles, spin-up, ZEC diagnostics. |
| Pathway portfolio potential | upper-tail dependency | 100 Gt/y portfolio vs ~37.5 Gt/y central assessed sum | Regional cost and potential curves with substitution rules. |
| Clean power and firm energy | major bottleneck | ~92,000 TWh/y gross; 27.5 TW nameplate; 3.5 TW firm | Regional dispatch, transmission, storage-duration, colocation models. |
| Clean-power additionality | major bottleneck | Market-unlocked case delivers 21% of the power gate | Hourly-resolution additionality accounting per tonne. |
| Contactor and factory scale | major bottleneck | ~3,800 km2 face area; ~80,000 large-plant equivalents for the DAC branch | Factory-rate model for modules, sorbents, replacement logistics. |
| Durable credited storage | major bottleneck | 100 gross becomes ~85 durable; ~118 gross needed | Pathway-specific LCA plus basin-level storage models. |
| MRV and credit integrity | major bottleneck | 100 gross becomes ~66 creditable; ~150 gross needed | Method-specific MRV distributions, invalidation rules, liability reserves. |
| Lifecycle emissions | major bottleneck | ~12 GtCO2e/y at 25 kgCO2/MWh | Pathway-specific LCAs and embodied-emissions factors. |
| Delivered cost frontier | major bottleneck | Automation push $86/tCO2; deep-abundance floor $24/tCO2 | Component-level techno-economic analysis. |
| Robotics and automation | research gap | Automation-push P50 ~840,000 robots/y, 1.55x IFR 2024; 0% pass share | Field-measured task-family productivity distributions. |
| Integrated 2046 feasibility | upper-tail dependency | Legacy optimistic pass is not integrated with later P0 gates | Integrated model with sourced, correlated distributions. |
| Uncertainty discipline | research gap | 11 of 15 sampled inputs need sourced distributions | Expert elicitation and adversarial sensitivity review. |
| Governance and rebound | governance constraint | Break-even falls to 23.1% after 25 kg/MWh LCA+MRV | Operational sink-governance model: fees, bans, liability, ownership. |

FIG: feasibility_gate_scorecard.png | Feasibility gate scorecard across the model stack.

The scorecard supports an adversarial review standard. Eight specialist panels were mapped against the analysis (carbon cycle, power systems, CDR process engineering, storage, robotics, economics, MRV and law, governance), each with named decisive artifacts; average reviewer risk is high and average evidence maturity is low, which is the honest position for a feasibility-boundary paper. Five falsification tests are designated P0. If FAIR-class modeling does not preserve a meaningful reversal outcome under plausible forcing; if additional clean power cannot be delivered after hourly matching, interconnection, and competing demand; if basin-level storage fails injection, pressure, permitting, or liability constraints; if MRV and lifecycle accounting demand physically impossible overbuild; or if rebound cannot credibly be held below the break-even threshold, the claim narrows. The commitment of this research program is that a failed P0 test changes the headline number rather than being buried under another scenario.

## 11. Proposed Research Program

The gaps named above are the work plan. The program is organized as model layers that can be upgraded independently, each with a deliverable and a go/no-go gate.

- **Climate modeling.** Extend the forcing-driven FAIR diagnostic into a full species-emissions FAIR or Earth-system workflow: CH4 and N2O trajectories, aerosol precursors, land-use forcing, lifecycle traces, historical spin-up, zero-emissions-commitment diagnostics, ocean chemistry for marine pathways, and uncertainty ensembles. Gate: a meaningful reversal outcome survives.
- **Energy systems.** Replace capacity arithmetic with regional 8760-hour dispatch: real resource traces, load shapes, interconnection queues, transmission corridors, storage durations, marginal emissions, and per-tonne additionality accounting. Gate: delivered additional clean power at program scale.
- **Pathways and MRV.** Build regional cost and potential curves per pathway, with substitution rules, method-specific MRV uncertainty distributions, reversal buffers, invalidation rules, and liability reserves. Gate: gross-to-creditable overbuild stays physically and economically feasible.
- **Storage.** Basin-level models of capacity, permeability, injection rates, pressure management, brine handling, transport, pore-space rights, induced seismicity, and long-term liability, replacing regional placeholders with sourced assessments. Gate: injection at portfolio scale survives engineering and institutional constraints.
- **Materials.** Pathway-specific bills of materials, replacement schedules, recycling loops, embodied emissions, and commodity competition with the broader energy transition, with reactive media and copper as priority screens.
- **Robotics.** Convert the evidence map into field-measured distributions: useful autonomous task-hours, duty cycles, maintenance, supervision ratios, and deployment rates by task family, sourced from deployments rather than announcements. Gate: post-stress production requirements stay within credible manufacturing expansion.
- **Cost.** Component-level techno-economic analysis tied to specific plant designs and supply chains, replacing scenario cost bands.
- **Uncertainty.** Replace hand-set triangular ranges with sourced distributions, expert elicitation, and correlated scenario families subjected to adversarial sensitivity review.
- **Governance.** Compare carbon taxes, cap-and-dividend, public trusts, citizen sink ownership, liability regimes, and prohibitions for dangerous outputs, as operational mechanisms with enforcement and failure-mode analysis rather than principles.

The program's value does not depend on the 100 Gt/y target being reached. Each layer produces independently useful results: regional additionality accounting, MRV buffer design, storage corridor models, and robotics field-productivity data all matter at 5 Gt/y as much as at 100.

## 12. Limitations

This is a conditional feasibility analysis, not a forecast, and several of its layers are explicitly provisional.

The carbon-cycle and climate-response treatment is better than atmosphere-only arithmetic but is not publication-grade climate science. The impulse-response model, two-box emulator, and forcing-mode FAIR run are scenario-discipline tools; they inherit aggregate forcing assumptions and omit species-level chemistry, regional response, and ensemble uncertainty.

The cost and robotics models show which orders of magnitude matter; they do not replace component-level techno-economic analysis, audited learning curves, or field-productivity measurements. Robotics assumptions are the noisiest input class: industrial deployment statistics are real, humanoid production claims are company-primary, and no field-productivity distributions for climate-infrastructure work currently exist.

Storage, MRV, and lifecycle numbers rest on provisional buffers and placeholder LCA terms whose job is to expose structure, not to settle magnitudes. The Monte Carlo outputs are screens over hand-set ranges and must not be quoted as calibrated probabilities. The governance branch is exploratory. And the 100 GtCO2/year target is intentionally extreme; a smaller program may be easier to justify, finance, and govern. The point of the extreme screen is to expose physical and institutional bottlenecks clearly enough that the feasible scale can be argued with evidence instead of slogans.












<!-- AETHER-PUBLIC-RELEASE:proposal-terraforming:BEGIN -->
### 12.1 Planetary Engineering and the Terraforming Boundary

AETHER qualifies as a low form of terraforming in a literal but limited sense: it studies deliberate, planetary-scale alteration of atmospheric composition to maintain a chosen climate state. On Earth, that label should raise the standard for consent, monitoring, reversibility, liability, and international governance. It is not permission to treat the planet as a controllable machine, and carbon removal cannot reconstruct extinct species, lost ice, displaced communities, or every regional climate state.

Some descendant capabilities could also matter beyond Earth. Autonomous construction, atmosphere processing, gas separation, mineralization, closed-loop clean power, and environmental monitoring could contribute to habitat engineering on Mars, Venus, the Moon, or other celestial bodies. This paper does not model those environments and makes no claim that terrestrial AETHER designs transfer directly. Off-world use is a speculative research direction, not part of the present feasibility result.
<!-- AETHER-PUBLIC-RELEASE:proposal-terraforming:END -->

## 13. Conclusion

A 100 GtCO2/year removal system is far beyond today's carbon-removal industry, but it is not an identified first-order conservation-law contradiction in the selected scenarios. The binding constraints are energy, capital, storage, air throughput, materials, measurement, and governance, in roughly that order, and they bind jointly.

The strongest version of the abundance thesis is not that AI solves climate change by thinking harder. It is that AI and robotics might accelerate the physical economy enough to make previously absurd infrastructure scales reachable: faster materials discovery, cheaper plants, automated construction, better drilling, more reliable monitoring, faster clean-energy buildout. Even then, the system works only if capture energy falls toward 1-3 GJ/tCO2, storage avoids unnecessary splitting, clean power grows by sustained multiples of today's record additions and stays additional, costs fall toward $10-50/tCO2, and rebound is held down by governance that stops treating shared sinks as free.

What this paper contributes is a transparent, falsifiable structure for judging that claim: explicit screens, named gates, an adversarial review standard, and a research program whose first deliverables are the current model's own weakest layers. The goal is not to make climate reversal sound easy. It is to make the necessary machinery visible enough that the idea can be judged scientifically, before the world needs it under worse conditions.

## References












<!-- AETHER-PUBLIC-RELEASE:proposal-references:BEGIN -->
- Aschenbrenner, L. (2024). Situational awareness: The decade ahead. https://situational-awareness.ai/
- Kokotajlo, D., Alexander, S., Larsen, T., Lifland, E., & Dean, R. (2025). AI 2027. https://ai-2027.com/
- Larsen, T., Dean, R., Halstead, B., Lifland, E., Greenblatt, R., & Kokotajlo, D. (2026). AI 2040: Plan A. https://ai-2040.com/
<!-- AETHER-PUBLIC-RELEASE:proposal-references:END -->

- 1PointFive. (2026). About 1PointFive. https://www.1pointfive.com/about
- Agility Robotics. (2023). Opening RoboFab: World's first factory for humanoid robots. https://www.agilityrobotics.com/content/opening-robofab-worlds-first-factory-for-humanoid-robots
- Alcott, B. (2005). Jevons' paradox. Ecological Economics, 54(1), 9-21. doi:10.1016/j.ecolecon.2005.03.020
- Anderson, S. T. (2017). Risk, liability, and economic issues with long-term CO2 storage: A review. Natural Resources Research, 26, 89-112. doi:10.1007/s11053-016-9303-6
- Axelsson, K., et al. (2024). Oxford principles for net zero aligned carbon offsetting (revised 2024). Smith School of Enterprise and the Environment, University of Oxford.
- Berkeley Lab. (2025). Queued up: 2025 edition. Characteristics of power plants seeking transmission interconnection as of the end of 2024. Lawrence Berkeley National Laboratory.
- California Energy Commission. (2025). 2024 total system electric generation. https://www.energy.ca.gov/data-reports/energy-almanac/california-electricity-data/2024-total-system-electric-generation
- Chatterjee, S., & Huang, K.-W. (2020). Unrealistic energy and materials requirement for direct air capture in deep mitigation pathways. Nature Communications, 11, 3287. doi:10.1038/s41467-020-17203-7
- Climeworks. (2024). Climeworks switches on world's largest direct air capture plant, Mammoth. Press release.
- Constellation Energy. (2024). Constellation to launch Crane Clean Energy Center, restoring jobs and carbon-free power to the grid. Press release.
- Cornell Law School, Legal Information Institute. (2026). Public trust doctrine. https://www.law.cornell.edu/wex/public_trust_doctrine
- European Commission. (2024). Carbon Removals and Carbon Farming (CRCF) Regulation. https://climate.ec.europa.eu/eu-action/carbon-removals-and-carbon-farming
- Figure AI. (2025). BotQ: A high-volume manufacturing facility for humanoid robots. Company announcement.
- Figure AI. (2026). Ramping Figure 03 production. Company announcement.
- Friedlingstein, P., et al. (2026). Global Carbon Budget 2025. Earth System Science Data, 18, 3211. doi:10.5194/essd-18-3211-2026
- Fusion Industry Association. (2025). Over $2.5 billion invested in fusion industry in past year. Press release.
- Georgetown Environmental Law Review. (2023). Up in the air: How the atmospheric trust doctrine is being used to fight climate change.
- Giro, R., Hsu, H., Kishimoto, A., et al. (2023). AI powered, automated discovery of polymer membranes for carbon capture. npj Computational Materials, 9, 133. doi:10.1038/s41524-023-01088-3
- Google. (2024). New nuclear clean energy agreement with Kairos Power. Company announcement.
- Helion Energy. (2023). Helion announces world's first fusion energy purchase agreement with Microsoft. Press release.
- IAEA. (2025). Status and prospects for nuclear power 2025. International Atomic Energy Agency.
- IEA. (2024). The future of geothermal energy. International Energy Agency.
- IEA. (2025a). Global critical minerals outlook 2025. International Energy Agency.
- IEA. (2025b). Energy and AI. International Energy Agency.
- IEA. (2026a). Global energy review 2026. International Energy Agency.
- IEA. (2026b). Electricity 2026. International Energy Agency.
- IEA. (2026c). The state of energy innovation 2026. International Energy Agency.
- IFR. (2025). World Robotics 2025: Industrial robots. International Federation of Robotics.
- IPCC. (2021a). Global carbon and other biogeochemical cycles and feedbacks. In Climate Change 2021: The Physical Science Basis (Chapter 5). Cambridge University Press.
- IPCC. (2021b). Figure 5.32: Carbon cycle response to instantaneous carbon dioxide removal from the atmosphere. In Climate Change 2021: The Physical Science Basis.
- IPCC. (2021c). The Earth's energy budget, climate feedbacks, and climate sensitivity. In Climate Change 2021: The Physical Science Basis (Chapter 7). Cambridge University Press.
- IPCC. (2021d). Technical summary. In Climate Change 2021: The Physical Science Basis. Cambridge University Press.
- IPCC. (2022a). Technical summary. In Climate Change 2022: Mitigation of Climate Change (Section TS.5.7, Table TS.7). Cambridge University Press.
- IPCC. (2022b). Cross-sectoral perspectives. In Climate Change 2022: Mitigation of Climate Change (Chapter 12). Cambridge University Press.
- IPCC. (2022c). Energy systems. In Climate Change 2022: Mitigation of Climate Change (Chapter 6, Section 6.4.2.5). Cambridge University Press.
- IRENA. (2025). Renewable power generation costs in 2024. International Renewable Energy Agency.
- Joos, F., et al. (2013). Carbon dioxide and climate impulse response functions for the computation of greenhouse gas metrics: A multi-model analysis. Atmospheric Chemistry and Physics, 13, 2793-2825. doi:10.5194/acp-13-2793-2013
- Keith, D. W., Holmes, G., St. Angelo, D., & Heidel, K. (2018). A process for capturing CO2 from the atmosphere. Joule, 2(8), 1573-1594. doi:10.1016/j.joule.2018.05.006
- Lemmon, E. W. (2009). Thermophysical properties of fluids. National Institute of Standards and Technology.
- McQueen, N., & Drennan, D. (2024). The use of warehouse automation technology for scalable and low-cost direct air capture. Frontiers in Climate, 6. doi:10.3389/fclim.2024.1415642
- National Academies of Sciences, Engineering, and Medicine. (2019a). Negative emissions technologies and reliable sequestration: A research agenda. The National Academies Press. doi:10.17226/25259
- National Academies of Sciences, Engineering, and Medicine. (2019b). Direct air capture. In Negative emissions technologies and reliable sequestration: A research agenda (Chapter 5). The National Academies Press.
- National Academies of Sciences, Engineering, and Medicine. (2022). A research strategy for ocean-based carbon dioxide removal and sequestration. The National Academies Press. doi:10.17226/26278
- NCSES. (2025). Discovery: R&D activity and research publications. Science and Engineering Indicators. National Center for Science and Engineering Statistics.
- NETL. (2015). Carbon storage atlas (5th ed.). U.S. Department of Energy, National Energy Technology Laboratory.
- NIST. (2026a). NIST Chemistry WebBook: Carbon dioxide. NIST Standard Reference Database 69. National Institute of Standards and Technology.
- NIST. (2026b). Cryogenic fluid properties. NIST/TRC reference data portal. National Institute of Standards and Technology.
- NOAA GML. (2026a). Trends in atmospheric carbon dioxide: Global monthly mean CO2. NOAA Global Monitoring Laboratory.
- NOAA GML. (2026b). Trends in atmospheric carbon dioxide: Monthly average Mauna Loa CO2. NOAA Global Monitoring Laboratory.
- NREL. (2024a). 2024 electricity annual technology baseline. National Renewable Energy Laboratory.
- NREL. (2024b). Land-based wind: 2024 electricity annual technology baseline. National Renewable Energy Laboratory.
- NREL. (2024c). Nuclear: 2024 electricity annual technology baseline. National Renewable Energy Laboratory.
- Ong, S., Campbell, C., Denholm, P., Margolis, R., & Heath, G. (2013). Land-use requirements for solar power plants in the United States (NREL/TP-6A20-56290). National Renewable Energy Laboratory.
- OSHA. (2020). Graphite (natural), respirable fraction. OSHA Occupational Chemical Database. Occupational Safety and Health Administration.
- Ostrom, E. (1990). Governing the commons: The evolution of institutions for collective action. Cambridge University Press.
- Patel, K., et al. (2025). Direct air capture case studies: Sorbent system (Rev. 1). National Energy Technology Laboratory. doi:10.2172/2520078
- Pett-Ridge, J., et al. (2023). Roads to removal: Options for carbon dioxide removal in the United States. Lawrence Livermore National Laboratory. doi:10.2172/2301853
- PubChem. (2026). Compound summary for magnesium carbonate. National Center for Biotechnology Information.
- Quinlivan, J. (2024). How Amazon deploys collaborative robots in its operations to benefit employees and customers. Amazon.
- Realmonte, G., et al. (2019). An inter-model assessment of the role of direct air capture in deep mitigation pathways. Nature Communications, 10, 3277. doi:10.1038/s41467-019-10842-5
- Smith, C. J., et al. (2018). FAIR v1.3: A simple emissions-based impulse response and carbon cycle model. Geoscientific Model Development, 11, 2273-2297. doi:10.5194/gmd-11-2273-2018
- Sorrell, S. (2009). Jevons' paradox revisited: The evidence for backfire from improved energy efficiency. Energy Policy, 37(4), 1456-1469. doi:10.1016/j.enpol.2008.12.003
- Sriram, A., et al. (2023). The Open DAC 2023 dataset and challenges for sorbent discovery in direct air capture. arXiv:2311.00341.
- State of CDR. (2026). The state of carbon dioxide removal (3rd ed.). https://www.stateofcdr.org
- Thompson, P. (2012). The relationship between unit cost and cumulative quantity and the evidence for organizational learning-by-doing. Journal of Economic Perspectives, 26(3), 203-224. doi:10.1257/jep.26.3.203
- Unitree Robotics. (2026). Unitree G1 humanoid robot. Product page.
- U.S. EIA. (2025). Texas state energy profile and analysis. U.S. Energy Information Administration.
- U.S. EPA. (2026a). Class VI: Wells used for geologic sequestration of carbon dioxide. U.S. Environmental Protection Agency.
- U.S. EPA. (2026b). Current Class VI projects under review at EPA. U.S. Environmental Protection Agency.
- U.S. EPA. (2026c). Subpart RR: Geologic sequestration of carbon dioxide. Greenhouse Gas Reporting Program. U.S. Environmental Protection Agency.
- USGS. (2013). National assessment of geologic carbon dioxide storage resources: Results (Circular 1386). U.S. Geological Survey.
- USGS. (2025). Mineral commodity summaries 2025. U.S. Geological Survey. doi:10.3133/mcs2025
- USGS. (2026). Mineral commodity summaries 2026: Graphite (natural). U.S. Geological Survey.
- World Steel Association. (2025). World steel in figures 2025.
- WRI. (2024). Direct air capture: Assessing impacts to enable responsible scaling. World Resources Institute.
- Wright, T. P. (1936). Factors affecting the cost of airplanes. Journal of the Aeronautical Sciences, 3(4), 122-128. doi:10.2514/8.155
- Young, J., McQueen, N., Charalambous, C., et al. (2023). The cost of direct air capture and storage can be reduced via strategic deployment but is unlikely to fall below stated cost targets. One Earth, 6(7), 899-917. doi:10.1016/j.oneear.2023.06.004
- Zickfeld, K., Azevedo, D., Mathesius, S., & Matthews, H. D. (2021). Asymmetry in the climate-carbon cycle response to positive and negative CO2 emissions. Nature Climate Change, 11, 613-617. doi:10.1038/s41558-021-01061-2

