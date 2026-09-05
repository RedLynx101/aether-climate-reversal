import evidence from "./evidence.generated.json";

export const githubUrl = "https://github.com/RedLynx101/aether-climate-reversal";
export const paperUrl = "/papers/AETHER_v0.46_working_paper.pdf";
export const supplementUrl = "/papers/AETHER_v0.46_technical_supplement.pdf";
export const correctionUrl = `${githubUrl}/blob/main/docs/CORRECTIONS_v0.46.md`;
export const atmosphere = evidence.atmosphere;
export const regional = evidence;
export function tableUrl(file: string) {
  return `${githubUrl}/blob/main/analysis/tables/${file}`;
}

// Research boundaries, not a tally of independently validated gates.
export const constraints = [
  { name: "Energy", verdict: "Engineering constraint", anchor: "Power + heat", anchorNote: "Different services, specified separately", reading: "Annual energy is only a first check. A real corridor needs hourly delivery, temperature-appropriate heat, grid access and additional low-carbon supply.", table: "aether_regional_reference_resource_ledger.csv" },
  { name: "Storage", verdict: "Site evidence needed", anchor: "A real basin", anchorNote: "Injection rate is not the same as pore-space capacity", reading: "Wells, transport, permits, monitoring and long-lived liability have to fit a named site. No site-specific storage plan is established here.", table: "aether_regional_reference_summary.csv" },
  { name: "Automation", verdict: "Field evidence needed", anchor: "Measured uptime", anchorNote: "Task hours and reliability—not robot counts alone", reading: "The regional comparison changes labor hours and availability explicitly. It does not assume that intelligence removes material or energy constraints.", table: "aether_regional_reference_summary.csv" },
  { name: "Accounting", verdict: "Separate ledgers", anchor: "Capture ≠ credit", anchorNote: "Keep physical retention, emissions and risk separate", reading: "Transport losses, project emissions, measurement uncertainty and reversal risk each reduce what the service can responsibly claim.", table: "aether_regional_reference_summary.csv" },
  { name: "Funding", verdict: "Scenario assumption", anchor: "Two obligations", anchorNote: "Current atmospheric use and historical cleanup", reading: "A fee on current emissions does not automatically pay for legacy drawdown or post-closure care. Each obligation needs an identified funding source.", table: "aether_regional_reference_utility_ledger.csv" },
  { name: "Climate response", verdict: "Projection withdrawn", anchor: "No target date", anchorNote: "Absolute climate projections are quarantined", reading: "A failed baseline diagnostic prevents credible concentration and temperature claims. A historically consistent carbon-and-climate model is still required.", table: "aether_carbon_cycle_summary.csv" },
] as const;
