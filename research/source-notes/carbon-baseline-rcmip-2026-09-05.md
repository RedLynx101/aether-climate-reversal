# Carbon baseline correction: source record and acceptance boundary

Status: **QUARANTINED / rejected for absolute projections.** Source provenance
and paired-control infrastructure are verified. The source-faithful hybrid
failed its off-reference zero-future-emissions acceptance experiment. Absolute
ppm/temperature values may be retained only as rejected-model diagnostics, not
as capability evidence, target dates, forecasts, or validation. No substitute
historical calibration was invented to close this gap.

## Primary sources

- Nicholls, Z., and Lewis, J. (2021), *Reduced Complexity Model Intercomparison
  Project (RCMIP) protocol*, v5.1.0,
  [immutable dataset](https://doi.org/10.5281/zenodo.4589756). Both full CSV files
  matched the MD5 values published by Zenodo before extraction. See
  `data/carbon-baseline/provenance.json` for all checksums and exact row metadata.
- Nicholls et al. (2020), *Reduced Complexity Model Intercomparison Project
  Phase 1: introduction and evaluation of global-mean temperature response*,
  [GMD 13, 5175-5190](https://doi.org/10.5194/gmd-13-5175-2020).
- Meinshausen et al. (2020), *The shared socio-economic pathway (SSP)
  greenhouse gas concentrations and their extensions to 2500*,
  [GMD 13, 3571-3605](https://doi.org/10.5194/gmd-13-3571-2020). The concentration
  series combines observation-based historical inputs and MAGICC7 projections.
  Its future points are scenario-model outputs, not observations.
- Joos et al. (2013), *Carbon dioxide and climate impulse response functions
  for the computation of greenhouse gas metrics: a multi-model analysis*,
  [ACP 13, 2793-2825](https://doi.org/10.5194/acp-13-2793-2013). Its pulse
  responses depend on background and pulse size; the published coefficients
  are not a historical reservoir initialization.
- [FaIR basic example, input modes and initialization](https://docs.fairmodel.net/en/latest/examples/basic_run_example.html),
  accessed September 5, 2026. Forcing mode accepts externally supplied forcing;
  running it does not independently validate the supplied carbon concentrations.

## Verified extraction

The selected concentration variable is `Atmospheric Concentrations|CO2` (ppm);
the emissions variable is `Emissions|CO2` (Mt CO2/yr). Both are World, ssp245,
MESSAGE-GLOBIOM. The extract preserves the exact source numeric text and blanks
from 1850 through 2100. Interior missing years are linearly interpolated in the
model, with no extrapolation. This is documented interpolation, not fitted data.

The reference's 2025 concentration is 429.0299580891927 ppm. This is an older
published scenario datum, not an observed 2025 global mean and not an update to
the repository's separate observational-source claims.

## Candidate hybrid method and failed acceptance check

The initial correction candidate uses

`C_s(y) = C_reference(y) + sum[J(y-t) * (E_s(t) + rebound(t) - eta(t)*R(t) - E_reference(t))] / 7.8`.

Only future (2026 onward) **emissions differences from the reference** enter the
Joos convolution. Adding all future emissions to the reference concentration
would double-count emissions already represented by that concentration path.
Annual pulses are a coarse annual-mean/discrete-time approximation.

It reproduces the source concentration exactly when future emissions equal the
source emissions, and it eliminates the old fixed 428.53 ppm additive offset.
However, applying this hybrid to zero future anthropogenic CO2 emissions yields
426.582160 ppm in 2026, a minimum of 409.543497 ppm in 2050, and 433.368307 ppm
in 2100 (a 23.824810 ppm rebound from the minimum). This is an unacceptable basis for claiming a repaired zero-emissions
projection: the response embedded in the source concentration trajectory is not
the same as the Joos response applied to a very large negative anomaly. The
test result is a diagnostic, not a source estimate of zero-emissions commitment.
Do not tune source values or relabel a synthetic initialization to hide it.

## Paired-control contract

Every AETHER case is paired with a no-AETHER case having exactly the same
non-AETHER CO2 emissions policy. Climate comparisons additionally match the
non-CO2/aerosol forcing policy and, in FaIR, thermal-response configuration.
Rebound emissions induced by AETHER remain part of the intervention difference;
they are zero when removal is zero. The new controls are
`baseline_half_2046_zero_2060_no_aether` and
`baseline_net_zero_2050_no_aether`; the existing constant-emissions control
remains. No-control cases must never borrow a control with a different policy.

The state-dependent screen recomputes induced emissions from its **actual**
floor-throttled removal. It must not inherit induced emissions computed from a
different screen's removal quantity. Fixed effectiveness is regression-checked
against the base carbon screen.

The two-box temperature calculation now reads the source historical CO2
concentrations instead of inventing a power-law CO2 history. Historical
non-CO2/aerosol forcing, the initial thermal state, and sensitivity coefficients
remain assumptions. Matching one TCR/ECS target does not make that history
calibrated. FaIR's forcing continuation is still only a diagnostic.

## Regeneration order

Run the existing model scripts in this order to reproduce the **quarantined
diagnostics**, including `aether_carbon_baseline_diagnostics.csv`:

1. `aether_carbon_cycle_model.py`
2. `aether_state_dependent_carbon_model.py`
3. `aether_climate_response_model.py`
4. `aether_climate_emulator_model.py`
5. `aether_fair_readiness_model.py`
6. `aether_species_emissions_handoff_model.py`
7. `aether_fair_forcing_execution_model.py`

Then run `python -m unittest discover -s tests -p test_carbon_baseline.py -v`.
The regression suite checks detection and rejection of the known response
failure, source identity/interpolation, exact source recovery under matching
emissions, single-pulse accounting, matched CO2/non-CO2/configuration controls,
fixed state-screen consistency, regenerated tables, and mandatory quarantine
metadata on every affected trajectory and summary. Passing these engineering
checks means the defect is exposed and promotion is blocked; it does not mean
the scientific acceptance check passed.

## Required work before trajectory promotion

Use one internally consistent emissions-driven carbon/climate model with a
sourced historical emissions/forcing history, explicit reservoir initialization,
and independently assessed parameter ensemble. Compare historical concentration,
growth rate, temperature, and ocean heat uptake against independent observations.
Then test zero-emissions commitment, positive/negative pulse asymmetry, large
net-negative paths, and sensitivity to initialization and annual time alignment.
Keep method-specific physical CO2 and non-CO2 flows separate from scalar CO2e
accounting and MRV credit buffers. Run identical no-AETHER policy controls and
seek carbon-cycle expert review before interpreting absolute concentrations or
temperatures. FaIR forcing-mode agreement cannot satisfy these requirements.
