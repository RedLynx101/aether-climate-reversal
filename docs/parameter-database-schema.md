# Parameter Database Schema

Last updated: 2026-06-09

The AETHER repo now keeps a structured parameter-evidence map at:

- `data/parameters/aether_parameter_evidence.csv`
- `analysis/tables/aether_parameter_evidence_summary.csv`

## Fields

- `parameter_id`: stable machine-readable identifier.
- `model_area`: broad model family such as `capture_energy`, `storage`, `robotics`, `cost_stack`, or `rebound`.
- `parameter_name`: reader-facing label.
- `central_value`, `low_value`, `high_value`, `unit`: quantitative value fields. Empty values are allowed for framework sources.
- `source_key`: source-register key, generated model key, or internal design-assumption key.
- `source_status`: evidence state.
- `evidence_grade`: A through D.
- `role_in_model`: why the parameter matters.
- `current_use`: where the parameter currently appears.
- `next_action`: what must happen before the parameter is strong enough for a serious outside review.
- `notes`: caveats.

## Evidence Grades

- `A`: verified primary, official, peer-reviewed, or directly calculated from such a source.
- `B`: solid framework source or derived value, but not yet specific enough for final parameterization.
- `C`: explicit AETHER scenario assumption or model output that depends materially on hand-set assumptions.
- `D`: provisional lead or moonshot boundary condition; never cite as a factual claim in the paper.

## Rule

Do not let a model parameter enter the manuscript as a factual claim unless it is `A` or a well-explained `B`. `C` and `D` parameters may appear only as scenario assumptions, sensitivity cases, or research gaps.

