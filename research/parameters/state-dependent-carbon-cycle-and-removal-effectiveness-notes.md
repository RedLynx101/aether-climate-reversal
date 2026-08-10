# State-Dependent Carbon-Cycle and Removal-Effectiveness Notes

Last updated: 2026-06-10

Implementation: `analysis/scenario-models/aether_state_dependent_carbon_model.py`

This v0.32 layer is a discipline upgrade for the carbon-cycle section. The earlier reduced-form model used the Joos impulse-response function and a fixed 0.96 removal-effectiveness multiplier. That was useful for getting out of atmosphere-only ppm arithmetic, but it still hid a central scientific problem: negative emissions do not necessarily have the same realized atmospheric effect at every atmospheric state or at every cumulative-removal depth.

The new screen keeps the Joos impulse-response model and adds four removal-effectiveness cases:

- Fixed 0.96 current screen: the v0.31 reference case.
- Optimistic active management: assumes pathway choice, MRV, and management reduce land/ocean compensation.
- Conservative state-dependent: assumes effectiveness falls as ppm declines and removals outrun positive emissions.
- Asymmetry stress: assumes stronger land/ocean compensation and emission-removal asymmetry.

| Scenario | Fixed 0.96 2100 ppm | Conservative 2100 ppm | Asymmetry stress 2100 ppm | Stress penalty vs fixed |
| --- | --- | --- | --- | --- |
| Net-zero 2050 | 350.0 | 350.0 | 350.0 | 0.0 |
| Constant emissions | 350.0 | 350.0 | 350.0 | 0.0 |
| 58% rebound | 473.3 | 492.4 | 525.9 | 52.7 |

The table should be read as a stress test, not as a climate-model result. It makes the paper less dependent on a single fixed multiplier. The main result is structural: AETHER looks most robust when emissions fall rapidly and removals are throttled near a management floor. It looks much weaker when cheap removal induces rebound or delayed abatement, and the penalty grows when the carbon-cycle response is less favorable.

## Paper Use Rule

Use this layer to show why state dependence matters and to bound sensitivity around the current reduced-form model. Do not treat these multipliers as fitted Earth-system outputs. The next publication-grade step is still a FAIR-class or Earth-system-model workflow with explicit temperature response, non-CO2 forcing, aerosols, ocean heat uptake, zero-emissions commitment, ocean chemistry, lifecycle emissions, and regional impacts.

