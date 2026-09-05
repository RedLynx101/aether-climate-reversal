# AETHER regional reference benchmark

## Result and boundary

This is one reproducible annual benchmark for a generic, approximately 1 MtCO2/year liquid-solvent direct-air-capture plus geologic-storage corridor. It is an arithmetic mechanism test, not an actual plant design, siting analysis, permit claim, field validation, cost-reduction forecast, tariff recommendation, or investment case.

Using the checked-in inputs, ordinary operations capture 850,000 tCO2/year gross and issue 758,696 tCO2e/year of risk-adjusted credits. The automation-assisted case captures 900,000 tCO2/year gross and issues 803,326 tCO2e/year of risk-adjusted credits. Both are uptime-limited. The 50,000 tCO2/year difference is conditional on an assumed increase in uptime from 0.85 to 0.90 and fewer operating-task hours; it is not an observed or forecast automation effect.

The physical contract is identical in both cases. Only these functional case fields may differ:

- uptime fraction;
- operations, maintenance, and measurement/reporting/verification task hours;
- hourly task cost; and
- explicit annual automation-system cost.

In the checked-in pair, the hourly task rate is also held equal. The assisted case reduces assumed task hours from 660,000 to 345,000 per year and adds $12 million/year of automation-system cost. Electricity intensity, process-heat intensity, emissions, transport/storage performance, credit discounts, capital, energy prices, funding, and deliverability limits are shared.

## Reproduce

From the repository root, using Python 3.11 or later:

```powershell
python analysis/scenario-models/aether_regional_reference_model.py --parameters data/regional-reference/parameters.csv --scenarios data/regional-reference/scenarios.json --output-dir analysis/tables
python -m unittest tests.test_regional_reference
```

The model writes files in this deterministic order:

1. `analysis/tables/aether_regional_reference_summary.csv`
2. `analysis/tables/aether_regional_reference_resource_ledger.csv`
3. `analysis/tables/aether_regional_reference_utility_ledger.csv`
4. `analysis/tables/aether_regional_reference_failure_cases.csv`
5. `analysis/tables/aether_regional_reference_invariants.csv`
6. `analysis/tables/aether_regional_reference_summary.json`

The JSON is the compact downstream interface. It contains input SHA-256 hashes, ordered output names, the two summaries, resource and utility ledgers, failure cases, and invariant results. Input hashes use canonical text bytes after explicitly normalizing CRLF to LF, so Windows `core.autocrlf` checkouts match LF-only checkouts. No wall-clock timestamp is included, so identical canonical inputs produce byte-identical outputs.

## Parameter and evidence contract

`data/regional-reference/parameters.csv` is the single numeric parameter table. Every row has a parameter ID, value, unit, category, evidence class, source ID/URL, sensitivity bounds, and a claim-boundary note. `data/regional-reference/scenarios.json` contains exactly two paired cases plus bounded stress tests.

The process anchor is NETL's 2022 conceptual solvent-DAC Case 1. Exhibit 5-2 reports 909,225 tCO2/year gross atmospheric capture at 85% capacity factor; Exhibit 5-3 reports 65.1 MWe total auxiliary demand; and Exhibit 5-8 reports 836 GJ/hour of calciner natural-gas HHV fuel input. Those values imply 0.533129 MWh of electricity and 6.846332 GJ_HHV of fuel input per gross tonne captured. The latter is retained only as a fuel-input-equivalent thermal-service proxy. It is not delivered useful heat, and the benchmark invents no conversion efficiency. Electricity and this proxy remain separate. Details and caveats are in `research/source-notes/regional-reference-sources.md`.

Most other numbers are deliberately labeled scenario assumptions. In particular, none of the cost, labor, automation, loss, retention, risk-buffer, reserve, settlement-rate, funding, or corridor-capacity values are forecasts or field measurements. The alternative low-carbon thermal-service technology, temperature suitability, conversion efficiency, integration losses, emissions intensity, and price all require separate evidence.

## Physical ledger

For each case, the model records these quantities separately:

1. gross atmospheric CO2 captured;
2. transport loss and injection rejection;
3. gross CO2 stored;
4. CO2 retained after the stated storage-retention factor;
5. modeled project emissions, which are subtracted after retention rather than reduced by it;
6. signed net retained removal, which can be negative; and
7. risk-adjusted credits after separate measurement and risk-buffer discounts.

The governing chain is:

`captured = transport loss + injection rejection + gross stored`

`retained = gross stored x retention fraction`

`signed net retained = retained - modeled project emissions`

`risk-adjusted credits = max(signed net retained, 0) x (1 - measurement discount) x (1 - risk buffer)`

Thus gross captured, gross stored, emitted, retained, net-benefit, and creditable tonnes are never synonyms. A high-emissions case preserves a negative result rather than relabeling it as zero benefit; only credit issuance is floored at zero.

Actual capture is the minimum of nameplate, uptime, deliverable electricity, deliverable heat, storage acceptance, and available-budget limits. The stress table demonstrates that halving electricity, heat, or storage caps both cases at the same physical bottleneck; automation cannot create a missing MWh, GJ, or injection slot. Halving the current-load settlement base reduces ordinary gross output to 632,213 tCO2/year and assisted output to 710,774 tCO2/year because the budget becomes binding.

This is not an hourly dispatch model and contains no battery. It therefore does not claim actual generation, dispatch, unserved hourly load, or curtailment. The resource ledger exposes an annual allowance envelope: `annual_electricity_allowance_twh_y`, `requested_electricity_load_twh_y`, `allocated_electricity_twh_y`, `unserved_requested_load_twh_y`, and `unallocated_electricity_allowance_twh_y`. It reconciles allowance = allocated + unallocated and requested = allocated + unserved. The separately reported `initial_state_gwh`, `final_state_gwh`, and `storage_state_change_twh_y` are all zero, making the no-storage boundary machine-testable. Hourly matching, actual generation, curtailment, firming, and transmission remain omitted.

## Public-utility cash and service ledgers

The benchmark distinguishes two obligations and funding streams:

- current-load settlement: a fee applied to a modeled current emissions base, with credits allocated first to that obligation; and
- legacy drawdown: separately identified public appropriation/procurement funding and the remaining risk-adjusted removal service.

These are arithmetic institutional mechanisms, not policy recommendations. The assumed $200/tCO2 current-load settlement rate is not claimed to be equitable, efficient, politically feasible, or economically optimal.

Cash sources equal current-load settlement revenue plus legacy-drawdown funding. Cash uses list the annual capital charge, fixed non-task O&M, task labor, automation system, variable non-energy O&M, electricity, the fuel-input-equivalent thermal-service proxy, transport/storage, and restricted reserve exactly once. The capital basis is not also expensed. The reserve is a restricted cash use tied to risk-adjusted credits, not a physical-emissions debit. Output is budget-capped so sources minus uses remains nonnegative; unfunded service appears as a current-load service shortfall rather than a fictitious credit. The compatibility output key `thermal_used_gj_y` therefore means GJ_HHV fuel-input-equivalent per year, not measured delivered useful heat.

Shrinking emissions revenue is a structural stress: when the current-load base falls, settlement revenue falls even though historical drawdown obligations do not. Removing legacy funding entirely leaves the ordinary case unable to cover its fixed annual uses and limits the assisted case to about 72,712 gross tCO2/year. This illustrates the funding distinction; it does not choose how the gap should be filled.

## Failure and stop conditions

The bounded failure table covers electricity delivery, process-heat delivery, storage acceptance, shrinking current-load revenue, absent legacy funding, and independent-verification failure. It does not define a larger scenario family.

The model fails closed—zero operation and zero credits—if any of these checks fails:

- independent verification is unavailable;
- the storage MRV plan is not accepted;
- independently reconciled source-to-storage mass-balance discrepancy exceeds the configured threshold; or
- required reserve coverage is not fully funded.

This is stricter than claiming that an EPA-approved MRV plan endorses a project; EPA explicitly says it does not. A real operating protocol would need staged shutdown rules, safety consequences, remediation procedures, appeals, and legal review.

## Institutional alternatives for research

The same physical ledger can be tested under several governance mechanisms without presuming one preferred political design:

- A regulated regional utility could use cost-of-service oversight and ring-fenced reserves. It may lower financing risk but creates rate-design, prudence-review, and regulatory-capture questions.
- A public procurement authority could contract independent capture, transport, storage, and verification providers. Competition may reveal costs, while fragmented contracts increase interface and counterparty risk.
- A producer takeback obligation with a pooled clearing mechanism could tie current fossil-carbon flows to storage duties. It still needs a separate rule for legacy drawdown and a credible treatment of a shrinking obligated base.
- A municipal, cooperative, or special-purpose district could localize accountability and benefit sharing. Smaller balance sheets and uneven geology can make portfolio diversification and long-tail liability harder.

Under every option, target setting, operation, credit issuance, independent verification, and adjudication should remain distinguishable functions in the model. The benchmark does not determine their legally optimal allocation.

## Omitted variables and use limits

The result can change materially with hourly/weather-matched supply, heat quality and temperature, startup/ramp behavior, redundancy, solvent/material replacement, water, land, air quality, corrosion, pipeline hydraulics, reservoir pressure, injectivity, induced seismicity, permitting, community consent, construction schedule, taxes, financing, insurance, liability duration, measurement error distributions, and lifecycle boundaries. The emissions ledger is not a full LCA: it applies variable per-tonne energy and a provisional other-lifecycle intensity, but does not separately schedule fixed embodied emissions, construction timing, decommissioning, or continuing monitoring, remediation, and liability costs after shutdown. Those omitted fixed and tail obligations can make low-throughput and stopped cases worse than shown. The 1 Mt/year scale is a reproducible analytical reference, not evidence that one common site clears those gates.
