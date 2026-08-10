# Robotics Productivity and Autonomy Economics Notes

Last updated: 2026-06-09

Implementation: `analysis/scenario-models/aether_robotics_productivity_model.py`

This layer converts the robotics discussion from "how many robots exist?" into the more relevant question: how many useful autonomous task-hours can AETHER buy, and where do those hours have to land?

The model keeps three scenarios:

- High robot-intensity translation: a stress case that roughly preserves the older 50 robots/MtCO2/year proxy after useful hours, supervision, and replacements are counted.
- AETHER automation push: modular plants, designed work environments, high utilization, and specialized robots lower the useful task-hours needed per tonne of capacity.
- Deep modular abundance: an upper-tail case where plant design, logistics, MRV, construction, and storage operations are rebuilt around robotic factories and low-supervision autonomy.

| Scenario | Useful task-hours, B/y | Robot stock, M | Production + replacement, robots/y | Robot operating cost, $B/y |
| --- | --- | --- | --- | --- |
| High robot intensity | 18.18 | 6.55 | 1,492,147 | 960 |
| AETHER automation push | 5.59 | 1.21 | 233,800 | 60 |
| Deep modular abundance | 1.84 | 0.31 | 53,251 | 6 |

The useful conclusion is not that AETHER needs exactly one of these fleet sizes. The useful conclusion is that robot optimism has to pay rent in task-hours. If AETHER requires high field-labor translation, the robot stock is multi-million and the annual production plus replacement flow is on the order of current global industrial robot installations. If AETHER can redesign work into modular factories, warehouse-like logistics, sensor networks, and automated construction workflows, the required fleet and operating cost fall by several multiples.

## Method

The model assigns useful task-hour demand to plant O&M, storage-field work, MRV, logistics, factory spares, robotic labs, module manufacturing, construction, storage corridors, and buildout MRV. It then maps each task family to a robot class: industrial factory robots, mobile logistics robots, humanoid/generalist field robots, autonomous construction equipment, drilling/subsurface robotics, MRV drones/sensor networks, or robotic lab workcells.

For each class, the model tracks unit cost, useful hours per year, lifetime, maintenance, energy use, supervision ratio, and integration overhead. Delivered robot cost per useful hour is annualized capex plus maintenance, energy, supervision, and integration overhead.

## Paper Use Rule

Use this as a scenario discipline layer, not as a robotics forecast. Company robot-price and factory claims are still leads or company claims. The next publication-grade upgrade needs source-backed distributions for task productivity, failure rates, repair cycles, field uptime, autonomy limits, and supervision ratios by task family.

