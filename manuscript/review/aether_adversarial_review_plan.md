# AETHER Adversarial Review and Falsification Plan

Last updated: 2026-06-10

Treat this as the reviewer gauntlet for AETHER, not as a defensive appendix. It is deliberately more severe than the main paper: the purpose is to make the remaining weak points explicit enough that a scientist can attack the right claim instead of guessing what the paper means.

The generated artifacts are:

- `analysis/tables/aether_adversarial_review_panels.csv`
- `analysis/tables/aether_falsification_tests.csv`
- `analysis/tables/aether_scientist_feedback_packet.csv`
- `analysis/tables/aether_adversarial_review_summary.csv`
- `analysis/figures/adversarial_review_risk_register.png`

Current read: the model has 8 expert panels, 8 high-risk panels, 5 P0 falsification tests, average reviewer risk 4.62 on a 1-5 scale, and average evidence maturity 1.88 on a 1-5 scale. That is not a publication-ready profile; it is a serious feedback profile.

## Reviewer Panels

| Reviewer panel | Risk | Evidence maturity | Next decisive artifact |
| --- | --- | --- | --- |
| carbon_cycle_and_climate | 5 | 2 | FAIR-class climate workflow and methods appendix |
| energy_systems_and_power_markets | 5 | 2 | regional dispatch and additionality model |
| cdr_process_and_materials | 5 | 2 | pathway-specific BOM and process TEA |
| storage_and_subsurface | 5 | 2 | basin-level storage and liability model |
| robotics_and_ai_productivity | 4 | 2 | task-family productivity distribution database |
| economics_and_finance | 4 | 2 | component TEA and capital program model |
| mrv_credit_integrity_and_law | 4 | 2 | method-specific MRV and liability model |
| governance_and_rebound | 5 | 1 | governance and rebound-control model |

## P0 Falsification Tests

| P0 test | Target claim | Decision if failed |
| --- | --- | --- |
| F1_fair_climate_reversal | AETHER plus emissions decline can produce climate reversal rather than offset bookkeeping. | Remove climate-reversal language and frame AETHER as an infrastructure stress test. |
| F2_additional_clean_power | A 3 GJ/tCO2 AETHER system can be powered with additional low-carbon energy. | Cap feasible removal by delivered clean power or shift to slower deployment. |
| F3_storage_injection_capacity | AETHER can store or mineralize tens of GtCO2/year durably. | Lower the portfolio target or move to costlier storage/conversion states. |
| F4_creditable_overbuild | 100 GtCO2/year gross capture can be turned into roughly target-scale durable credit. | Use creditable tonnes as the headline target and treat 100 Gt gross as insufficient. |
| F8_rebound_control | AETHER can remain net-negative rather than enabling new emissions. | Make emissions controls and sink-use pricing a binding precondition rather than an optional governance section. |

## Use Rule

Use this plan before sending AETHER to domain scientists. If a reviewer can break a P0 test, the paper should narrow the claim immediately. The right academic posture is not to defend every optimistic assumption; it is to find which assumptions survive contact with specialists and then rebuild the paper around those survivors.

