# Regional reference model source notes

Accessed 2026-09-05. These notes support one bounded analytical benchmark. They do not establish that a specific site is feasible, permitted, financeable, or ready to build.

## NETL DAC Case 1 process anchor

- Source: U.S. Department of Energy, National Energy Technology Laboratory, *Direct Air Capture Case Studies: Solvent System* (2022), https://www.netl.doe.gov/projects/files/DirectAirCaptureCaseStudiesSolventSystem_083122.pdf
- Source type: official technical report with a conceptual process model informed by Carbon Engineering process data; not operating data from a commercial 1 Mt/year DAC plant.
- Relevant reported data:
  - Exhibit 5-2: 909,225 tCO2/year gross removed from air at 85% capacity factor.
  - Exhibit 5-3: 65.1 MWe total auxiliary load, including 23.36 MWe of CO2 compression along with air fans, pumps, air separation, cooling, and balance of plant.
  - Exhibit 5-8: 836 GJ/hour calciner natural-gas HHV fuel input and a separate 70 GJ/hour unaccounted-by-difference term. The benchmark uses the stated calciner fuel input only as a thermal-service proxy; it does not claim useful delivered heat or closure of NETL's full process energy balance.
- Derived parameters used here:
  - Electricity: `65.1 MW x 8,760 h/year x 0.85 / 909,225 tCO2/year = 0.5331294234 MWh/tCO2`.
  - Calciner fuel-input-equivalent thermal-service proxy: `836 GJ_HHV/hour x 8,760 h/year x 0.85 / 909,225 tCO2/year = 6.8463317661 GJ_HHV fuel-input-equivalent/tCO2`.
- Translation boundary: NETL supplies natural gas to an oxy-fired calciner and a separate gas turbine that provides electricity. The benchmark does not convert the calciner fuel input into delivered useful heat and assumes no conversion efficiency. It retains the reported HHV fuel input as a separately constrained thermal-service proxy while treating the stated auxiliary load as electricity. Any alternative low-carbon thermal supply, required temperature, conversion efficiency, integration loss, emissions intensity, and price are scenario assumptions needing independent process proof. The gas-turbine fuel is not also charged to the thermal-service proxy.
- Why this is only an archetype: the benchmark rescales the intensities to a 1,000,000 tCO2/year nameplate, does not reproduce NETL's KOH/calcium-loop material flows, does not store captured fossil-process CO2, and does not reproduce a real site or project.
- Lifecycle boundary: the model is not a full LCA. Its provisional per-tonne “other lifecycle” term does not separately represent fixed embodied emissions, construction timing, decommissioning, or continuing monitoring/remediation/liability after shutdown. It must not be described as a complete lifecycle inventory.

## EPA geologic-storage accounting anchor

- Source: U.S. Environmental Protection Agency, “Subpart RR – Geologic Sequestration of Carbon Dioxide,” https://www.epa.gov/ghgreporting/subpart-rr-geologic-sequestration-carbon-dioxide
- Source type: primary regulator guidance and rule implementation page.
- Use in this model: the physical ledger follows the mass-balance distinction among CO2 received, injected, produced/leaked, and sequestered, and makes independent verification and an accepted storage MRV plan explicit stop conditions.
- What the source does not support: EPA approval of an MRV plan is not an endorsement of a project. It does not support this benchmark's illustrative loss, retention, uncertainty-discount, risk-buffer, reserve, cost, or capacity numbers.

## DOE regional-removal context

- Source: U.S. Department of Energy, “Department of Energy ‘Roads to Removal’ Report Maps Path to Gigatonne-Scale CO2 Removal,” 2024, https://www.energy.gov/hgeo/articles/department-energy-roads-removal-report-maps-path-gigatonne-scale-co2-removal
- Source type: official summary of the multi-laboratory *Roads to Removal* assessment.
- Use in this model: supports studying region-specific CDR opportunities and pairing DAC with purpose-built low-carbon energy and durable storage.
- What the source does not support: it is not evidence for this benchmark's specific corridor, automation effect, financing split, energy budget, or cost parameters.

## Evidence classification

- `primary_source_datum`: copied from the identified table/exhibit in a primary or official source.
- `derived_primary_source`: arithmetic transformation of primary-source data, with the equation preserved above and in tests.
- `scenario_assumption`: chosen to make a constraint, accounting mechanism, or failure case executable. It must not be presented as observed performance or a forecast.
- `scenario_assumption_not_forecast`: an explicitly hypothetical automation mechanism test.

All source-derived and assumed values, units, sensitivity bounds, and notes are kept together in `data/regional-reference/parameters.csv`.
