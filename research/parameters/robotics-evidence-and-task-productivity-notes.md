# Robotics Evidence and Task Productivity Notes

Last updated: 2026-06-09

This note upgrades the AETHER robotics layer from a simple robot-fleet sensitivity into an evidence map. The point is not to prove that humanoids solve AETHER. The point is to separate three claims:

1. Robots are already deployed at large scale in factories and warehouses.
2. Humanoid robot manufacturing is moving from demos toward factory lines, but most numbers are still company claims.
3. AETHER depends on useful work per robot-year in construction, drilling, monitoring, logistics, and plant maintenance, not just purchase price.

## Evidence Anchors

| Evidence | Value | Source | AETHER use | Caution |
|---|---:|---|---|---|
| Global industrial robot installations | 542076 robots/year | `ifr_world_robotics_2025` | Current annual robot manufacturing/adoption comparator | Industrial robots are mostly factory systems, not autonomous AETHER field robots. |
| Global industrial robot operational stock | 4663698 robots | `ifr_world_robotics_2025` | Existing industrial robot stock comparator | Stock count does not imply general-purpose autonomy. |
| Amazon deployed mobile robots | 750000 robots | `amazon_robotics_750k_robots_2024` | Large fleet-management and warehouse automation comparator | Amazon robots operate in designed facilities, not open construction, mining, or storage environments. |
| Unitree G1 listed starting price | 13500 USD/unit | `unitree_g1_product_2026` | Low-end humanoid hardware price floor | Civilian early-stage platform, 2h battery, limited warranty; not evidence of industrial AETHER productivity. |
| Unitree G1 listed battery life | 2 hours | `unitree_g1_product_2026` | Runtime caution for humanoid duty-cycle assumptions | AETHER's 4,000-7,500 h/year utilization cases require charging, swappable batteries, or non-humanoid specialized systems. |
| Figure BotQ first-generation design capacity | 12000 robots/year | `figure_botq_2025` | Humanoid factory-capacity comparator | Company-announced capacity, not independent audited annual output. |
| Figure 03 demonstrated cadence | 1 robots/hour | `figure_ramping_2026` | Frontier humanoid ramp signal | Company claim; useful for scenario calibration but should not be treated as audited global production. |
| Figure 03 robots delivered by ramp announcement | 350 robots | `figure_ramping_2026` | Scale of current humanoid fleet claim | Small relative to AETHER fleet requirements. |
| Figure end-of-line first-pass yield | 80 percent | `figure_ramping_2026` | Manufacturing process maturity signal | Company-reported and improving; not an independent quality audit. |
| Figure actuators produced | 9000 actuators | `figure_ramping_2026` | Supply-chain and actuator-scale signal | Actuator production is not the same as complete robot deployment. |
| Agility RoboFab peak capacity | 10000 robots/year | `agility_robofab_2023` | Humanoid factory-capacity comparator | Factory capacity, not guaranteed sustained output. |
| AETHER 50 robots/MtCO2/y fleet | 5000000 robots | `generated_aether_transition_model` | Core robot-fleet requirement in integrated feasibility screen | Depends on the proxy assumption that 50 robots support each MtCO2/year of installed capacity. |
| AETHER 50 robots/MtCO2/y annual production over 20 years | 250000 robots/year | `generated_aether_transition_model` | Annual robot manufacturing requirement for core proxy | Does not include replacement, spares, attrition, or robots needed for upstream energy/materials buildout. |
| AETHER 1000 robots/MtCO2/y high-end fleet | 100000000 robots | `generated_aether_transition_model` | High robot-intensity stress test | Represents a new robotics industry far beyond current humanoid factory announcements. |

## Task Productivity Ladder

| Task family | AETHER role | Productivity proxy | Evidence grade | Next action |
|---|---|---|---:|---|
| Robotic laboratories | Materials, sorbents, membranes, catalysts, mineralization chemistry, ocean monitoring assays. | R&D cycle-time reduction | C | Build source-backed autonomous-lab literature review and translate into pathway-specific learning rates. |
| Factory manufacturing | Contactor modules, sensors, pumps, skids, well equipment, robots, replacement parts. | Units produced per line per year | B/C | Separate general industrial robots, humanoids, and special-purpose plant manufacturing automation. |
| Warehouse and logistics | Parts handling, warehouse operations, module movement, spare-parts logistics. | Fleet-managed moves per facility | B | Estimate how much of AETHER logistics can be moved into designed environments. |
| Construction and maintenance | Plant assembly, inspection, cleaning, replacement, site preparation. | Installed MtCO2/year capacity per robot-year | C | Create task-level work breakdown for DAC plants, wells, pipelines, grinding facilities, and monitoring networks. |
| Drilling and subsurface operations | Geologic storage wells, monitoring wells, pressure-management systems. | Wells drilled and maintained per robot-supported crew | D | Add oil/gas drilling automation, rig count, and well-cost sources. |
| MRV and field sensing | Leak detection, plume monitoring, ocean chemistry, soil/weathering sampling, biological permanence checks. | Verified tonnes monitored per autonomous sensor/robot system | C | Build adversarial MRV model with sampling rates, sensor failure, and audit cost. |
| General humanoid labor | Fallback labor in human-designed facilities, inspection, repetitive handling, supervised maintenance. | Useful autonomous task hours per robot-year | B/C | Replace unit-price optimism with useful-work and reliability distributions. |

## Current Read

The strongest robotics evidence for AETHER is not the cheapest humanoid. It is the combination of large deployed warehouse fleets, global industrial robot installations, and company-announced humanoid factories. Those make the robotics premise more concrete than it was a few years ago.

The weak point is useful field productivity. A $13.5K humanoid price floor is interesting, but it does not answer whether a robot can install contactors, maintain compressors, inspect storage sites, drill wells, handle alkaline minerals, or run ocean MRV safely for thousands of hours per year. The correct AETHER variable is useful autonomous task-hours per robot-year after charging, downtime, safety supervision, maintenance, spare parts, weather, terrain, and degraded-mode recovery.

The core transition model's 50 robots per MtCO2/year proxy implies about 5 million robots in service and 250,000 robots/year over 20 years. That annual flow is below current global industrial robot installations but above any individual humanoid factory announcement. The high 1,000 robots per MtCO2/year case implies 100 million robots and 5 million robots/year, a new robotics industry rather than an extrapolation from current humanoid lines.
