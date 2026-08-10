# Correlated Uncertainty and Scenario-Family Notes

Last updated: 2026-06-10

Implementation: `analysis/scenario-models/aether_correlated_uncertainty_model.py`

The v0.33 layer addresses a weakness in the earlier uncertainty screen. The independent Monte Carlo model was useful because it made AETHER's assumptions explicit, but it sampled inputs as if clean-power growth, robot productivity, storage/MRV performance, costs, residual emissions, rebound, and execution could move separately. That is not how a real climate infrastructure program would fail or succeed.

The correlated screen keeps the same physical capacity equations and the same uncertainty distribution registry, then creates named scenario families:

- Independent reference.
- Clean-power abundance.
- Automation abundance.
- Storage/MRV failure.
- Policy/rebound failure.
- Full abundance aligned.
- Full failure clustered.

| Scenario family | Durable >=100 | Net positive | Strong reversal | Median net Gt/y | Primary binding |
| --- | --- | --- | --- | --- | --- |
| Independent | 0.1% | 56.1% | 1.7% | 2.2 | clean_energy |
| Clean power | 2.4% | 88.9% | 14.4% | 19.8 | storage |
| Automation | 0.6% | 56.9% | 3.1% | 2.7 | clean_energy |
| Storage/MRV failure | 0.0% | 38.5% | 0.1% | -2.9 | clean_energy |
| Policy/rebound failure | 0.0% | 29.6% | 0.0% | -6.2 | clean_energy |
| Full abundance | 57.3% | 100.0% | 88.5% | 72.9 | program_execution |
| Full failure | 0.0% | 0.0% | 0.0% | -23.7 | clean_energy |

The interpretation is structural. AETHER does not become credible because one optimistic assumption moves alone. It becomes credible only in aligned abundance cases where clean energy, automation, storage, durability, rebound control, budgets, and execution move together. Conversely, a storage/MRV or policy/rebound failure can leave a system that looks physically large but weak as a climate-reversal program.

## Paper Use Rule

Use this as a scenario-family sensitivity layer. Do not call the percentages forecasts. They are pass rates under hand-set ranges and correlation shifts. The next upgrade is a formal uncertainty-methods appendix with sourced distributions, expert elicitation, adversarial sensitivity review, and explicit cross-parameter covariance assumptions.

