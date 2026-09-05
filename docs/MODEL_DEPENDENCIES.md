# AETHER model dependencies and compatibility boundaries

Last updated: 2026-09-05

This document records execution dependencies, not scientific validation. A
table can be reproducible and still contain scenario assumptions, source gaps,
or a boundary condition that needs review. Do not add favorable results from
separate screens unless they share the same scenario ID, region, year,
accounting layer, resource ledger, and parameter version.

## Current pipeline

```text
pathway portfolio
  -> storage lifecycle
  -> MRV integrity
  -> detailed lifecycle emissions

regional dispatch diagnostic (separate diagnostic family)
regional reference model (separate ordinary-vs-automation case family)
legacy partially-coupled feasibility screen (separate legacy screening family)

generated outputs -> calculation audit -> figures / paper / evidence exports
```

The first chain shares pathway allocations. The three lower scenario families
must not be summed or treated as independent confirmations of one common 100
GtCO2/year outcome. The calculation audit tests stated arithmetic invariants;
it does not certify source quality or feasibility.

## Executable order

1. `aether_pathway_portfolio_model.py` writes the gross allocation and pathway
   assumptions.
2. `aether_storage_lifecycle_model.py` consumes that allocation and writes the
   retained-storage layer.
3. `aether_mrv_credit_integrity_model.py` consumes both to apply MRV and
   liability buffers.
4. `aether_lifecycle_emissions_model.py` consumes the shared pathway,
   retention, and MRV fields. Its physical accounting invariant is
   `signed_net = gross * retained_fraction - lifecycle_emissions`, with a
   separately named nonnegative credit-eligible layer before the MRV
   multiplier. A lifecycle debit is not reduced by a permanence haircut, and a
   negative signed result must not be hidden by a zero-floor credit field.
5. `aether_regional_power_dispatch_model.py` is a synthetic daily dispatch
   diagnostic. Its energy and storage boundary are separate from the pathway
   chain.
6. `aether_regional_reference_model.py` (when present) reads
   `data/regional-reference/parameters.csv` and `scenarios.json`, then writes
   its reference outputs. It compares ordinary and automation-assisted cases
   under shared physical inputs; it is not an input to the legacy integrated
   screen.
7. `aether_integrated_feasibility_model.py` remains explicitly labeled
   `partially_coupled_screening`. It only jointly constrains the internally
   modeled planned capacity, clean-energy, robot, storage, budget, emissions,
   rebound, and realized-production learning assumptions.
8. `scripts/audit_aether_calculations.py` checks the regenerated ledgers and
   writes the calculation-audit tables. Run it after every upstream change.

`scripts/reproduce_research.py --check` executes the supported order in an
isolated temporary copy and compares its outputs to the checked-in tables. It
never overwrites the working tree.

## Publication generation status

`scripts/build_current_publication.py` is the only supported current-paper
generator. `--check` verifies the current publication manifest, source hashes,
PDFs, website copies, and extracted text without writing. Run
`scripts/export_public_evidence.py --check` after it to verify source-linked
public evidence and figures. The legacy v0.45 submission-package, Word, and
bibliography scripts are retained solely for explicit historical recovery and
fail closed without `--legacy-v0-45-rebuild --legacy-output-dir PATH`, with
`PATH` a separate complete AETHER checkout; they are not pipeline steps.

## Cross-model contract

An output is eligible for a future coupled portfolio model only if it declares:

- `model_id` and version or source revision;
- scenario ID and assumptions/parameter artifact;
- geography or region, time period, and duration;
- gross, physically retained, lifecycle-debit, and creditable accounting
  layers with units; and
- a resource ledger that identifies electricity, heat by temperature grade,
  chemical energy, storage/injection, land/biomass/minerals, transport, and
  any resource allocated to another pathway.

In the regional-reference ledger, `thermal_used_gj_y` is retained for
compatibility but denotes **GJ_HHV fuel-input-equivalent/year**, not useful
delivered heat. A future coupled adapter must not substitute it for
temperature-grade process heat without an explicit conversion and source.

The forthcoming regional-reference interface is:

```text
inputs:  data/regional-reference/parameters.csv
         data/regional-reference/scenarios.json
CLI:     --parameters PATH --scenarios PATH --output-dir PATH
outputs: aether_regional_reference_{summary,resource_ledger,utility_ledger,
         failure_cases,invariants}.csv and summary.json
```

Its ordinary and automation-assisted cases must share physical conditions for
their comparison. An adapter may consume it only after it maps the regional
energy/heat and storage ledger to the same scenario and accounting layer as a
pathway portfolio. Until then, recording both outputs in a paper is comparison,
not integration.

## Learning-state contract

The legacy screen learns from `cumulative_realized_removal_gtco2`, not planned
capacity. Each annual row records its beginning state, learning doublings, cost,
and ending state. The reference cumulative-production value is currently a
clearly labeled screening proxy, not a sourced historical cumulative-production
series. Only constrained capacity operated in preceding model years increments
the state. A planned but unbuilt deployment cannot reduce cost.
