# AETHER figure status

Last reviewed: 2026-09-05

Most figures in this directory are historical visualizations. Their presence
does not make them current publication evidence. The supported public evidence
exporter is `scripts/export_public_evidence.py`; `--check` verifies byte-exact
current outputs against their source-linked inputs.

## Current regional public figures

Only these three figures are current public evidence:

| Source figure | Website copy | Scope |
| --- | --- | --- |
| `regional-carbon-ledger.png` | `website/public/charts/regional-carbon-ledger.png` | Gross captured, stored, physically retained, signed net of project emissions, and risk-adjusted credits for the stated ordinary and automation-assisted regional cases. |
| `regional-resource-limits.png` | `website/public/charts/regional-resource-limits.png` | The binding-resource envelope for those same cases. It is not a universal deployment forecast. |
| `regional-funding-ledger.png` | `website/public/charts/regional-funding-ledger.png` | Illustrative current-service and separate-legacy-funding ledger; it does not establish a tariff, forecast, or financing recommendation. |

These figures must be read with the linked regional summary, resource ledger,
utility ledger, failure cases, invariants, and parameter/scenario files. They
are not evidence that a larger AETHER portfolio is feasible.

## Quarantined climate figures

The following are retained diagnostics only and must not appear as current
public capability evidence: `carbon_cycle_atmospheric_co2_pathways.png`,
`climate_response_temperature_proxy.png`,
`climate_emulator_temperature_paths.png`,
`fair_readiness_climate_input_deck.png`,
`fair_forcing_execution_comparison.png`, and
`species_emissions_handoff_gap_matrix.png`. Their associated carbon/climate
outputs remain quarantined even when regenerated.

## Historical or unreconciled figures

Every other PNG in `analysis/figures/` is historical, exploratory, or
unreconciled under the current correction contracts. This explicitly includes
`feasibility_gate_scorecard.png`, `integrated_feasibility_screen_2046.png`,
`integrated_capacity_paths_2026_2046.png`, and
`regional_power_dispatch_gate.png`. Do not reuse these figures in the current
paper, website, or a public evidence package without a scoped regeneration,
dependency review, and visual inspection.
