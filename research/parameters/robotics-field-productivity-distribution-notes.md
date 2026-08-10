# Robotics Field Productivity Distribution Notes

Last updated: 2026-06-10

Implementation: `analysis/scenario-models/aether_robotics_field_productivity_distribution_model.py`

This layer stress-tests the robotics premise that the prior productivity model leaves open. The earlier robotics screen asks how many useful task-hours AETHER needs. This one asks what happens when those task-hours are discounted by field uptime, autonomy success, task suitability, maintenance drag, and safety/supervision drag.

| Scenario | P10 production, robots/y | P50 production, robots/y | P90 production, robots/y | P50 stock, M | IFR-count pass share |
| --- | --- | --- | --- | --- | --- |
| High robot intensity | 10,933,533 | 13,220,956 | 16,522,244 | 61.02 | 0% |
| AETHER automation push | 746,069 | 840,142 | 948,342 | 4.53 | 0% |
| Deep modular abundance | 108,497 | 116,483 | 126,009 | 0.70 | 100% |

The result is intentionally uncomfortable. The high robot-intensity case becomes a nonstarter unless a very large robotics industry exists and AETHER proves useful field productivity. The automation-push case is more interesting: its unadjusted production count is below current annual industrial robot installations, but field-productivity penalties can move the median requirement back toward an economy-scale robotics buildout. Deep modular abundance stays easiest on count, but it rests on the strongest assumption: that climate-infrastructure work has been redesigned around robot-native modules, controlled logistics, sensorized MRV, and low-supervision construction.

## Method

The model reuses `analysis/tables/aether_robotics_productivity_by_task.csv`. For each scenario and task family it samples triangular distributions for:

- field uptime,
- autonomy success,
- task-fit or environment-design suitability,
- maintenance and repair drag,
- safety/supervision drag.

The effective task-hour multiplier is:

`field uptime * autonomy success * task fit / (maintenance factor * supervision factor)`

Robot stock, annual replacement, buildout flow, and robot operating cost are then scaled upward by the inverse of that multiplier. This is not a forecast. It is a stress test that says which robotics claims need real measurements before the AETHER manuscript should ask outside scientists to take them seriously.

## Paper Use Rule

Use the P10/P50/P90 values as scenario diagnostics only. The publication-grade upgrade needs measured task-family distributions: field uptime, repair cycles, failure recovery, autonomy boundary conditions, human supervision ratios, safety incidents, and productivity per robot-hour for plant maintenance, module manufacturing, construction, drilling, logistics, MRV, and autonomous labs.

