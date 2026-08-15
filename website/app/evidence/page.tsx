/* eslint-disable @next/next/no-img-element -- Static research figures are already optimized publication assets. */
import type { Metadata } from "next";
import { Arrow, EvidenceBadge, GateLedger, SiteFooter, SiteNav } from "../components";
import { githubUrl, paperUrl, tableUrl, uncertainty } from "../data";

export const metadata: Metadata = {
  title: "Evidence and open gates",
  description:
    "The AETHER submission ledger, the uncertainty distribution behind the headline case, and selected model figures with their source tables.",
  alternates: { canonical: "/evidence" },
};

const navLinks = [
  { href: "/#utility", label: "The utility" },
  { href: "#gates", label: "Gates" },
  { href: "#uncertainty", label: "Uncertainty" },
  { href: "#figures", label: "Figures" },
] as const;

const figures = [
  {
    id: "capacity",
    number: "01",
    title: "Capacity under integrated constraints",
    src: "/charts/integrated-capacity-paths-2026-2046.png",
    alt: "AETHER modeled removal-capacity paths from 2026 to 2046 under integrated constraints",
    badge: "model" as const,
    interpretation:
      "Actual capacity is the minimum of the target schedule, clean energy, robot supply, storage, and budget. Only upper-tail branches approach the 100 GtCO₂/year stress-test target by 2046.",
    caution:
      "A conditional scenario comparison. It assigns no probability to the upper-tail branches and does not show their joint assumptions are achievable.",
    table: "aether_integrated_feasibility_timepaths.csv",
  },
  {
    id: "gates-figure",
    number: "02",
    title: "The gates have to clear together",
    src: "/charts/feasibility-gate-scorecard.png",
    alt: "AETHER feasibility gate scorecard across physical, economic, scientific, and governance constraints",
    badge: "model" as const,
    interpretation:
      "First-order physical possibility is not enough. Clean power, contactor scale, durable credited storage, delivered cost, climate modeling, robotics evidence, uncertainty, and governance each remain a bottleneck or an open gap.",
    caution:
      "Status labels are internal research judgments synthesized from the current model suite. They are not expert consensus or peer-reviewed validation.",
    table: "aether_feasibility_gate_scorecard.csv",
  },
  {
    id: "robotics",
    number: "03",
    title: "Robotics is a field-productivity problem",
    src: "/charts/robotics-field-productivity-gate.png",
    alt: "AETHER robotics field-productivity distribution gate comparing annual robot requirements",
    badge: "open" as const,
    interpretation:
      "Uptime, autonomy, task-fit, maintenance, and supervision multipliers are applied before AETHER robot requirements are compared with current annual industrial robot installations.",
    caution:
      "The optimistic deep-modular case clears the count comparison only because infrastructure is assumed to be redesigned for automation. That task suitability still needs field evidence.",
    table: "aether_robotics_field_productivity_distribution_summary.csv",
  },
] as const;

const percent = (share: number, digits = 2) => `${(share * 100).toFixed(digits)}%`;

/** Percentile bars are drawn against the 100 Gt stress-test target. */
const barWidth = (value: number) => `${Math.min(100, (value / 100) * 100).toFixed(1)}%`;

export default function Evidence() {
  return (
    <main className="aether-site evidence-page" id="main">
      <SiteNav links={navLinks} label="Evidence navigation" />

      <section className="evidence-hero">
        <p className="section-code">AETHER / WHAT THE MODEL ACTUALLY SHOWS</p>
        <h1>Show the system.<br /><em>Show where it breaks.</em></h1>
        <div>
          <p>
            These are outputs from a coupled feasibility-boundary model. They expose how energy, industrial capacity, storage, economics, robotics, climate response, verification, and governance interact.
          </p>
          <p>
            They are not forecasts. The 100 GtCO₂/year reference case is deliberately extreme so that hidden dependencies become visible rather than staying buried in an optimistic branch.
          </p>
        </div>
      </section>

      <section className="gates-section" id="gates">
        <div className="gates-head">
          <p className="section-code">01 / SUBMISSION READINESS</p>
          <h2>Twelve gates. Two of them fail.</h2>
          <p>
            This ledger is generated, not written by hand. The two failing gates are the honest reason AETHER is a working paper rather than a submission: temperature claims currently rest on a forcing-driven diagnostic, and the species-level emissions inputs that would make them publication-grade do not exist yet.
          </p>
        </div>
        <GateLedger />
      </section>

      <section className="uncertainty-section" id="uncertainty">
        <div className="uncertainty-head">
          <p className="section-code">02 / THE UNCERTAINTY SCREEN</p>
          <h2>What {uncertainty.samples.toLocaleString()} draws say about the headline number.</h2>
          <p>
            A Monte Carlo screen over the stated assumption ranges. It measures how much of the possibility space actually reaches the target — which is the question a single optimistic curve cannot answer.
          </p>
        </div>

        <div className="distribution" aria-label="Durable credited removal distribution against the 100 Gt target">
          <div className="distribution-scale"><span>0</span><span>50 Gt</span><span>100 Gt target</span></div>
          {[
            { label: "10th percentile", value: uncertainty.durableCredit.p10 },
            { label: "Median", value: uncertainty.durableCredit.p50, emphasis: true },
            { label: "90th percentile", value: uncertainty.durableCredit.p90 },
          ].map((row) => (
            <div className={`distribution-row${row.emphasis ? " distribution-median" : ""}`} key={row.label}>
              <span className="distribution-label">{row.label}</span>
              <div className="distribution-track">
                <i style={{ width: barWidth(row.value) }} />
              </div>
              <span className="distribution-value">{row.value} Gt/yr</span>
            </div>
          ))}
        </div>

        <dl className="uncertainty-stats">
          <div>
            <dt>Draws reaching 100 Gt gross</dt>
            <dd>{percent(uncertainty.grossHundredShare)}</dd>
          </div>
          <div>
            <dt>Draws reaching 100 Gt durable credit</dt>
            <dd>{percent(uncertainty.durableHundredShare)}</dd>
          </div>
          <div>
            <dt>Draws with any net removal</dt>
            <dd>{percent(uncertainty.positiveReversalShare, 0)}</dd>
          </div>
          <div>
            <dt>Draws reversing at today&rsquo;s emission rate</dt>
            <dd>{percent(uncertainty.strongReversalShare, 1)}</dd>
          </div>
        </dl>

        <div className="uncertainty-caveat">
          <EvidenceBadge kind="open" />
          <p>
            These ranges are currently hand-set rather than elicited from experts, and the sampling does not yet model correlation between optimistic assumptions properly. That makes this a screen, not a probability estimate — and it is itself one of the open gates above.
          </p>
          <a href={tableUrl(uncertainty.table)}>Inspect the table <Arrow /></a>
        </div>
      </section>

      <section className="figure-gallery" id="figures">
        <div className="gallery-head">
          <p className="section-code">03 / SELECTED FIGURES</p>
          <h2>Every curve should lead back to assumptions, units, and a source table.</h2>
        </div>
        {figures.map((figure) => (
          <article id={figure.id} key={figure.id}>
            <header>
              <span className="figure-number">{figure.number}</span>
              <h3>{figure.title}</h3>
              <EvidenceBadge kind={figure.badge} />
            </header>
            <figure>
              <div className="figure-scroll">
                <img src={figure.src} alt={figure.alt} loading="lazy" />
              </div>
            </figure>
            <div className="figure-reading">
              <div><span>WHAT IT SHOWS</span><p>{figure.interpretation}</p></div>
              <div><span>READ WITH CAUTION</span><p>{figure.caution}</p></div>
              <a href={tableUrl(figure.table)}>Inspect the source table <Arrow /></a>
            </div>
          </article>
        ))}
      </section>

      <section className="evidence-close">
        <p className="section-code">CONTRIBUTE</p>
        <h2>Scientific criticism is a contribution.</h2>
        <p>
          Reproduce a model, replace a weak parameter, add a missing constraint, or take apart a claim that deserves it. The review guide explains how to challenge a specific number.
        </p>
        <div>
          <a className="button button-primary" href={paperUrl}>Read the working paper <Arrow /></a>
          <a className="button button-secondary" href={`${githubUrl}/blob/main/docs/REVIEW_GUIDE.md`}>Open the review guide <Arrow /></a>
        </div>
      </section>

      <SiteFooter note="Selected outputs from the AETHER model suite. Scenario results are not deployment claims." />
    </main>
  );
}
