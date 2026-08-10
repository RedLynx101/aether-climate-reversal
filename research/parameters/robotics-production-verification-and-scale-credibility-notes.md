# Robotics Production Verification and Scale Credibility Notes

Last updated: 2026-06-10

Implementation: `analysis/scenario-models/aether_robotics_production_verification_model.py`

This layer separates robotics production-rate evidence from robotics productivity assumptions. That distinction matters. A production claim can be true and still fail to prove that a robot can build contactors, maintain compressors, drill storage wells, inspect pipelines, or run adversarial MRV for thousands of useful hours per year.

The current evidence stack has three tiers:

- Independent industry anchor: IFR reports 542,076 industrial robot installations in 2024 and 4,663,698 operational industrial robots.
- Company-primary robotics signals: Amazon reports more than 750,000 deployed mobile robots; Figure reports BotQ first-generation capacity up to 12,000 humanoids/year, a one-robot-per-hour Figure 03 cadence, more than 350 Figure 03 robots delivered, over 80% end-of-line first-pass yield, 99.3% battery-line first-pass yield, and more than 9,000 actuators produced; Agility reports RoboFab capacity above 10,000 robots/year; Unitree lists a low humanoid price floor.
- Unresolved leads: Noah's Figure X links, including the 250-robots-in-one-month claim, remain in the verification queue. They can guide search and sensitivity analysis, but they should not be written as paper facts until archived or independently corroborated.

| Scenario | Annual robot production need | Multiple of 2024 IFR installs | Figure BotQ-equivalent lines |
| --- | --- | --- | --- |
| High robot intensity | 1,492,147 | 2.75 | 124.3 |
| AETHER automation push | 233,800 | 0.43 | 19.5 |
| Deep modular abundance | 53,251 | 0.10 | 4.4 |

The main result is measured, but useful. The high robot-intensity translation case needs about 1,492,147 robots/year for buildout plus replacement, or about 2.75x current annual industrial robot installations and 124.3 Figure BotQ first-generation line equivalents. The AETHER automation-push case needs about 233,800 robots/year, below current IFR annual installations on a count basis but still about 19.5 BotQ-equivalent lines. The deep modular abundance case needs about 53,251 robots/year and is easiest on manufacturing count, but depends on the strongest redesign premise.

## Paper Use Rule

Use official Figure, Agility, Amazon, Unitree, and IFR rows as evidence-classed anchors. Do not treat them as independent audits of AETHER-grade field productivity. Use the X claims only as leads unless the original posts are archived or a stronger primary source appears.

The next upgrade should add independent production audits, shipment data, robot bill-of-materials, service records, uptime distributions, useful autonomous task-hour measurements, failure and repair cycles, safety-supervision ratios, and task-family productivity tests for climate-infrastructure work.

