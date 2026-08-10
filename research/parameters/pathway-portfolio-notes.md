# Pathway Portfolio Notes

Last updated: 2026-06-09

This note documents the first AETHER pathway portfolio model. The model asks what a 100 GtCO2/year removal system would have to look like if it is not allowed to hide behind one magic pathway.

## Current Model

Implementation: `analysis/scenario-models/aether_pathway_portfolio_model.py`

Outputs:

- `analysis/tables/aether_pathway_portfolio_allocation.csv`
- `analysis/tables/aether_pathway_portfolio_summary.csv`
- `analysis/figures/pathway_portfolio_100gt.png`

The model uses IPCC AR6 WGIII Technical Summary Table TS.7 for assessment-level cost and potential ranges for afforestation/reforestation, biochar, DACCS, BECCS, and enhanced weathering. It uses the National Academies ocean CDR report for ocean alkalinity enhancement and electrochemical marine CDR constraints.

## Main Result

The assessment-backed central potential ranges do not get close to 100 GtCO2/year. The AETHER portfolio therefore uses explicit optimized-capacity assumptions:

- DACCS with geologic storage: 40 GtCO2/year.
- Enhanced weathering and surficial mineralization: 20 GtCO2/year.
- Ocean alkalinity enhancement: 15 GtCO2/year.
- BECCS: 10 GtCO2/year.
- Biochar: 6 GtCO2/year.
- Afforestation/reforestation: 5 GtCO2/year.
- Direct ocean capture/electrochemical mCDR: 4 GtCO2/year.

This is not a forecast. It is a stress test. If these allocations look too aggressive, that is the point: AETHER requires multiple methods to be pushed hard at once, with AI/robotics helping the physical bottlenecks rather than hand-waving them away.

## Current Portfolio Totals

- Gross removal allocation: 100 GtCO2/year.
- Weighted assumed removal cost: about $84/tCO2.
- Annual cost: about $8.4 trillion/year.
- Weighted assumed energy intensity: about 2.03 GJ/tCO2.
- Annual energy demand: about 56,528 TWh/year, or 6.45 TW average.

The energy total is lower than an all-DAC 3 GJ/tCO2 system because biological and some geochemical pathways are less electricity-intensive in this simplified model. That does not make them easy. They shift the bottlenecks into land, biomass, rock mining, grinding, transport, ocean chemistry, MRV, and permanence.

## Interpretation

AETHER should not be framed as DAC alone. DACCS is the most flexible engineered backbone, but the 100 GtCO2/year target almost certainly needs a portfolio that includes geologic storage, mineralization, ocean alkalinity, biomass carbon storage, and limited biological restoration. Each pathway fails differently. That is useful because a diversified portfolio avoids single-pathway fragility, but it also creates a governance and MRV problem across many physical systems.

The next upgrade should add uncertainty distributions, lifecycle emissions, regional constraints, and pathway-specific learning curves instead of using a single optimized-cost assumption for each pathway.
