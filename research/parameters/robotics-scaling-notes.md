# Robotics Scaling Notes

Last updated: 2026-06-09

AETHER treats robotics as a physical deployment accelerator, not as a magic substitute for energy, storage, and materials. The central modeling question is whether cheap embodied labor and autonomous machinery can compress the time and cost of building climate-reversal infrastructure.

## Verified Baseline

IFR World Robotics 2025 reports 542,076 industrial robots installed in 2024 and an operational stock of 4,663,698 industrial robots. This is the current industrial baseline for robot deployment. It is large enough to matter, but it is not yet a planetary construction workforce.

Source key: `ifr_world_robotics_2025`

## Figure Robotics Leads

Noah supplied two X links attributed to Brett Adcock:

- `https://x.com/adcock_brett/status/2063472470850744390?s=46` - summarized as Figure producing one humanoid per hour.
- `https://x.com/adcock_brett/status/2064059797365006378?s=20` - summarized as Figure producing 250 robots in one month.

A third-party mirror/search result showed a profile item reading `Humanoid robots manufactured at Figure by month` with visible values `13 11 250`. This is useful, but it is not enough to make the claim a paper fact.

Current status: unresolved lead.

Acceptable paper use: scenario calibration and evidence that humanoid manufacturing claims are moving quickly.

Unacceptable paper use: treating Figure's 250/month or one/hour as audited production statistics without an archive, screenshot, or official primary statement that can be preserved.

## AETHER Robot Fleet Sensitivity

The transition model tests assumed robots per MtCO2/year of removal capacity. This does not mean robots remove CO2 directly. It is a proxy for construction, operations, logistics, inspection, maintenance, drilling, and sensor deployment support.

| Robots per MtCO2/year capacity | Fleet for 100 GtCO2/year | Annual production over 20 years | Multiple of IFR 2024 industrial robot installations | Multiple of 250/month Figure lead, annualized |
|---:|---:|---:|---:|---:|
| 10 | 1,000,000 | 50,000/year | 0.09x | 16.7x |
| 50 | 5,000,000 | 250,000/year | 0.46x | 83.3x |
| 100 | 10,000,000 | 500,000/year | 0.92x | 166.7x |
| 500 | 50,000,000 | 2,500,000/year | 4.61x | 833.3x |
| 1,000 | 100,000,000 | 5,000,000/year | 9.22x | 1,666.7x |

Interpretation: AETHER does not require the whole world to wait for humanoids. At low robot-intensity assumptions, the needed annual robot production is below current global industrial robot installations. At high robot-intensity assumptions, the required production becomes a new global robotics industry several times larger than today's installation rate. Figure-level humanoid production is promising as a signal, but a single 250/month company run rate is still two to three orders of magnitude below high-end AETHER robot-fleet requirements.

## Robot Cost Assumptions

The scenario model uses $25,000-$100,000 unit costs, 7-8 year lifetimes, 5,000-7,000 operating hours per year, and 8-12% annual maintenance. These are assumptions. Under those assumptions, direct robot-hour costs can fall below $1-$3/hour before power, supervision, tooling, downtime, and overhead.

The paper should emphasize that direct hourly cost is not the main bottleneck. The important variables are task productivity, reliability, autonomous recovery, useful work per day, spare parts, deployment rate, and whether robots can work on energy and storage infrastructure rather than only in clean factory demos.
