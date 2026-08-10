# Jevons, Learning Curves, and Economies of Scale

Last updated: 2026-06-09

AETHER has two opposing economic dynamics:

1. Learning curves and economies of scale can drive down cost as cumulative deployment rises.
2. Jevons-style rebound can erase climate gains if cheaper removal or cheaper energy induces more emissions, delays abatement, or turns removal into a permission structure for continued pollution.

Both have to be in the model. Ignoring learning curves makes the project too static. Ignoring rebound makes the project politically naive.

## Learning Curves

The transition model uses a simple Wright-style learning curve:

```text
cost_at_target = initial_cost * (1 - learning_rate) ^ doublings
```

Moving from current novel CDR of about 0.00204 GtCO2/year to 100 GtCO2/year requires about 15.6 capacity doublings.

With a $500/tCO2 initial engineered-removal cost and a 3 GJ/tCO2 advanced capture assumption:

| Learning rate per capacity doubling | Raw learned cost at 100 GtCO2/year | Bounded cost at $10/MWh power plus storage/MRV floor | Annual cost at 100 GtCO2/year |
|---:|---:|---:|---:|
| 10% | $96.83/tCO2 | $96.83/tCO2 | $9.68T/year |
| 15% | $39.74/tCO2 | $39.74/tCO2 | $3.97T/year |
| 20% | $15.45/tCO2 | $20.33/tCO2 | $2.03T/year |
| 25% | $5.65/tCO2 | $20.33/tCO2 | $2.03T/year |
| 30% | $1.93/tCO2 | $20.33/tCO2 | $2.03T/year |

The bounded cost matters. Once learning pushes equipment cost below the energy/storage/MRV floor, further manufacturing learning cannot lower total cost unless energy intensity, power price, storage cost, or MRV cost also improve.

Source keys: `wright_1936_learning_curve`, `thompson_2012_learning_by_doing`, `aether_model_assumptions_2026`

## Economies of Scale

Plant-level scale economies are modeled with a simple exponent:

```text
plant_capex = base_capex * plant_size ^ alpha
unit_capex = plant_size ^ (alpha - 1)
```

If alpha is less than 1, larger plants reduce unit capex. At 100 GtCO2/year, plant count is still enormous:

| Plant size | Plants for 100 GtCO2/year |
|---:|---:|
| 1 MtCO2/year | 100,000 |
| 10 MtCO2/year | 10,000 |
| 25 MtCO2/year | 4,000 |
| 100 MtCO2/year | 1,000 |

Economies of scale therefore help, but they do not remove siting, air-contact, storage, pipeline, transmission, and public-acceptance constraints. Very large hubs can lower unit cost while increasing local concentration of risk and permitting difficulty.

## Jevons and Rebound

Jevons paradox is the warning that efficiency improvements can increase total resource use when they lower effective cost and expand demand. In AETHER, the equivalent failure mode is not only energy use. It is policy rebound:

- Cheap removal can induce additional atmospheric use faster than verified removal capacity grows.
- Firms can use removal promises to justify higher production.
- Governments can become dependent on pollution revenue.
- Consumers can treat removal as moral offsetting for higher consumption.
- More abundant energy can lower the cost of high-emission activity if governance is weak.

The rebound sensitivity model treats rebound as induced emissions or delayed abatement equal to a fraction of gross removal. Against a 42.2 GtCO2/year current-emissions baseline:

| Rebound fraction of 100 GtCO2/year gross removal | Net removal | Simple atmosphere-only ppm/year |
|---:|---:|---:|
| 0% | 57.8 GtCO2/year | 7.41 ppm/year |
| 10% | 47.8 GtCO2/year | 6.13 ppm/year |
| 25% | 32.8 GtCO2/year | 4.21 ppm/year |
| 50% | 7.8 GtCO2/year | 1.00 ppm/year |
| 57.8% | 0.0 GtCO2/year | 0.00 ppm/year |
| 75% | -17.2 GtCO2/year | -2.21 ppm/year |

AETHER must therefore keep emissions limits and commons governance separate from removal optimism. Removal capacity should not become an excuse to increase use of the atmospheric sink.

Source keys: `sorrell_2009_jevons_rebound`, `alcott_2005_jevons_paradox`
