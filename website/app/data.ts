export const githubUrl = "https://github.com/RedLynx101/aether-climate-reversal";
export const paperUrl = "/papers/AETHER_v0.45_working_paper.pdf";
export const proposalUrl = "/papers/AETHER_Conditional_Feasibility_Proposal.pdf";

/** Link to a generated table so any figure on this site can be checked at source. */
export function tableUrl(file: string) {
  return `${githubUrl}/blob/main/analysis/tables/${file}`;
}

/**
 * Monte Carlo screen over the v0.8 assumption ranges.
 * Source: analysis/tables/aether_uncertainty_summary.csv
 */
export const uncertainty = {
  samples: 20_000,
  grossHundredShare: 0.0075,
  durableHundredShare: 0.0009,
  positiveReversalShare: 0.56045,
  strongReversalShare: 0.01495,
  grossCapacity: { p10: 17.1, p50: 37.4, p90: 69.1 },
  durableCredit: { p10: 14.1, p50: 30.8, p90: 57.9 },
  table: "aether_uncertainty_summary.csv",
} as const;

/**
 * The twelve submission-readiness gates, verbatim in status from the generated
 * ledger. Five pass, five are partial, two fail.
 * Source: analysis/tables/aether_submission_readiness_gates.csv
 */
export type GateStatus = "pass" | "partial" | "fail";

export const submissionGates: ReadonlyArray<{
  id: string;
  gate: string;
  status: GateStatus;
  evidence: string;
  next: string;
}> = [
  {
    id: "S01",
    gate: "Citation coverage",
    status: "pass",
    evidence: "83 cited keys resolve; 0 missing BibTeX entries.",
    next: "Render through a target-journal citation style.",
  },
  {
    id: "S02",
    gate: "Figure resolution",
    status: "pass",
    evidence: "41 figure references resolve; 0 missing files.",
    next: "Add journal captions, numbering, and page layout.",
  },
  {
    id: "S03",
    gate: "Equation reproducibility",
    status: "pass",
    evidence: "10 dimensioned unit checks; 0 failures.",
    next: "Connect every major claim to equation ids and tables.",
  },
  {
    id: "S04",
    gate: "Claim-to-evidence mapping",
    status: "pass",
    evidence: "14 claim-evidence rows recorded.",
    next: "Expand with reviewer comments and source upgrades.",
  },
  {
    id: "S05",
    gate: "Publication-grade climate modeling",
    status: "fail",
    evidence:
      "A forcing-driven FAIR diagnostic exists, but the species-emissions handoff blocks publication-grade temperature claims.",
    next: "Build species-level CH4, N2O, aerosol, land-use, and spin-up inputs.",
  },
  {
    id: "S06",
    gate: "Species-level emissions inputs",
    status: "fail",
    evidence: "7 of 10 species-emissions gates currently fail.",
    next: "Work the species-emissions requirement matrix.",
  },
  {
    id: "S07",
    gate: "Clean-power delivery",
    status: "partial",
    evidence: "Deliverability screens plus a regional dispatch pass exist.",
    next: "Replace archetype days with 8760-hour regional dispatch.",
  },
  {
    id: "S08",
    gate: "Storage, MRV, and lifecycle",
    status: "partial",
    evidence: "Route-level storage, lifecycle, and credit-integrity screens exist.",
    next: "Move to basin-level storage and method-specific lifecycle analysis.",
  },
  {
    id: "S09",
    gate: "Robotics field productivity",
    status: "partial",
    evidence: "Field-productivity screens exist, but the multipliers are provisional.",
    next: "Collect sourced duty-cycle, autonomy, and failure-rate data.",
  },
  {
    id: "S10",
    gate: "Adversarial review",
    status: "partial",
    evidence: "10 falsification tests are written into the review packet.",
    next: "Run specialist review and narrow claims where P0 tests fail.",
  },
  {
    id: "S11",
    gate: "Style and duplication screen",
    status: "pass",
    evidence: "0 repeated boilerplate phrases; 0 editorial placeholders.",
    next: "Human editorial pass once a venue is chosen.",
  },
  {
    id: "S12",
    gate: "Submission formatting",
    status: "partial",
    evidence: "A generated submission package exists; no venue is selected.",
    next: "Choose a venue and render to its requirements.",
  },
];

export const gateTally = {
  pass: submissionGates.filter((g) => g.status === "pass").length,
  partial: submissionGates.filter((g) => g.status === "partial").length,
  fail: submissionGates.filter((g) => g.status === "fail").length,
} as const;

/**
 * Where the coupled model actually strains. Anchors are quoted from the
 * generated scorecard rather than restated from prose.
 * Source: analysis/tables/aether_feasibility_gate_scorecard.csv
 */
export const constraints = [
  {
    name: "Clean power",
    verdict: "Major bottleneck",
    anchor: "91,667 TWh/yr",
    anchorNote: "gross clean generation, with 27.5 TW nameplate and 3.5 TW firm",
    reading:
      "At 3 GJ per tonne, this stops being a capture project and becomes a power-system buildout at tens of terawatts.",
    table: "aether_clean_power_portfolio_summary.csv",
  },
  {
    name: "Air contact",
    verdict: "Major bottleneck",
    anchor: "3,771 km²",
    anchorNote: "of contactor face area — roughly 200,000 STRATOS-scale plants",
    reading:
      "Contactor scale is set by air flow, pressure drop, sorbent replacement, and factory throughput, not by the price of electricity.",
    table: "aether_air_contactor_scale_summary.csv",
  },
  {
    name: "Durable storage",
    verdict: "Major bottleneck",
    anchor: "84.9 Gt/yr",
    anchorNote: "of 100-year durable credit from 100 Gt/yr of gross capture",
    reading:
      "Delivering 100 Gt of credited removal would require 117.8 Gt of gross capture. Lifecycle emissions and reversal risk take the difference.",
    table: "aether_storage_lifecycle_summary.csv",
  },
  {
    name: "Delivered cost",
    verdict: "Major bottleneck",
    anchor: "$86/tCO₂",
    anchorNote: "in the automation-push case — $8.6T per year",
    reading:
      "Automation moves the labor buckets. Energy, storage, verification, finance, materials, and liability stay where they are.",
    table: "aether_cost_improvement_frontier.csv",
  },
  {
    name: "Robotics",
    verdict: "Research gap",
    anchor: "840,142 robots/yr",
    anchorNote: "1.55× total 2024 global industrial robot installations",
    reading:
      "The fleet arithmetic clears only before field-productivity penalties are applied. Afterwards, no sampled case passes.",
    table: "aether_robotics_field_productivity_distribution_summary.csv",
  },
  {
    name: "Rebound",
    verdict: "Governance constraint",
    anchor: "23.1%",
    anchorNote: "break-even rebound after lifecycle and verification filters",
    reading:
      "Headroom falls from 57.8% to 41.7% to 23.1% as accounting tightens. Cheap removal that licenses new emissions eats its own budget.",
    table: "aether_rebound_accounting_thresholds.csv",
  },
] as const;

/** NOAA global monthly mean, April 2026. */
export const atmosphere = {
  current: 428.55,
  preindustrial: 280,
  controlFloor: 350,
  source: "https://www.gml.noaa.gov/ccgg/trends/global.html",
} as const;
