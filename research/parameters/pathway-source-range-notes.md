# Pathway Source Range Notes

Last updated: 2026-06-09

This note adds a source-range layer to the AETHER pathway portfolio. The current portfolio model asks what mix could add to 100 GtCO2/year. This source-range layer asks whether each pathway allocation is inside, near the edge of, or beyond the ranges assessed in major CDR syntheses.

Current files:

- `data/parameters/aether_cdr_pathway_source_ranges.csv`
- `analysis/tables/aether_pathway_source_gap_analysis.csv`
- `analysis/figures/pathway_source_ranges_vs_aether.png`
- `scripts/make_aether_pathway_source_range_figure.ps1`

## Source-Range Table

| Pathway | AETHER allocation | Assessed potential | Assessed cost | TRL | Current read |
|---|---:|---:|---:|---:|---|
| DACCS | 40 Gt/y | 5-40 Gt/y | $100-300/tCO2; full range $84-386/tCO2 | 6 | AETHER uses the top of the IPCC assessed DACCS potential range, so DACCS cannot absorb much model slippage. |
| Enhanced weathering/mineralization | 20 Gt/y | 2-4; full range <1-95 Gt/y | $50-200/tCO2; full range $24-578/tCO2 | 3-4 | AETHER is five times the central high estimate but still inside the very wide full literature range. |
| Ocean alkalinity enhancement | 15 Gt/y | 1-100 Gt/y | $40-260/tCO2 | 1-2 | The allocation is inside the assessed potential range, but the method is low-TRL and must survive marine chemistry, ecology and governance review. |
| BECCS | 10 Gt/y | 0.5-11 Gt/y | $15-400/tCO2 | 5-6 | AETHER is close to the upper assessed range; the land, water and biomass-supply penalty is the main reason not to push it harder. |
| Biochar | 6 Gt/y | 0.3-6.6 Gt/y | $10-345/tCO2 | 6-7 | AETHER is near the upper assessed range, which is plausible only with large sustainable biomass and high-quality permanence/MRV. |
| Afforestation/reforestation | 5 Gt/y | 0.5-10 Gt/y | $0-240/tCO2 | 8-9 | The allocation is inside the assessed range, but it is not a substitute for durable engineered storage. |
| Direct ocean/electrochemical CDR | 4 Gt/y | not resolved as a separate pathway range Gt/y | NASEM: end-to-end CDR roughly $70-700/tCO2; electrochemical has highest assessed scale-up cost among ocean approaches | research-to-early demonstration | The 4 GtCO2/year allocation is a placeholder until electrochemical ocean CDR has method-specific sourced ranges. |

## Interpretation

The current AETHER portfolio is not impossible by source ranges, but it is aggressive in exactly the places that should make a scientist cautious.

DACCS is set at the top of the IPCC assessed potential range. BECCS and biochar are near their assessed upper ranges. Enhanced weathering is far above the central assessed range, although still inside the very wide full literature range. Ocean alkalinity has a large assessed potential range but low TRL and high governance/MRV uncertainty. Direct ocean/electrochemical CDR remains a placeholder rather than a source-backed pathway allocation.

The effect is to make portfolio substitution less generous. If DACCS, BECCS, or biochar underperform, the replacement tonnes probably have to come from enhanced weathering, ocean alkalinity, or future engineered systems, not from a large unused mature pathway. That means AETHER's optimism should be concentrated on source-backed bottlenecks: clean energy, material throughput, MRV, storage/injection, ecological monitoring, and automated deployment.

