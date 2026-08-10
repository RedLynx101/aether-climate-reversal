/* eslint-disable @next/next/no-img-element -- Static research figures are already optimized publication assets. */
import type { Metadata } from "next";
import { AetherMark, Arrow, EvidenceBadge } from "../components";
import { githubUrl, paperUrl } from "../data";

export const metadata: Metadata = {
  title: "Inside the systems model",
  description: "Selected AETHER figures on integrated capacity, feasibility gates, and robotics field productivity.",
  alternates: { canonical: "/model" },
};

const figures = [
  {
    id: "capacity",
    number: "01",
    title: "Capacity under integrated constraints",
    src: "/charts/integrated-capacity-paths-2026-2046.png",
    alt: "AETHER modeled removal-capacity paths from 2026 to 2046 under integrated constraints",
    badge: "model" as const,
    interpretation: "Actual removal capacity is defined as the minimum of the target schedule, clean energy, robot supply, storage, and budget capacity. Only upper-tail branches approach the 100 GtCO₂/year stress-test target by 2046.",
    caution: "This is a conditional scenario comparison. It does not assign a probability to the upper-tail branches or prove that their joint assumptions can be achieved.",
    source: `${githubUrl}/blob/main/analysis/tables/aether_integrated_feasibility_timepaths.csv`,
  },
  {
    id: "gates",
    number: "02",
    title: "The gates have to clear together",
    src: "/charts/feasibility-gate-scorecard.png",
    alt: "AETHER feasibility gate scorecard across physical, economic, scientific, and governance constraints",
    badge: "model" as const,
    interpretation: "The current scorecard shows why first-order physical possibility is not enough. Clean power, air-contactor scale, durable credited storage, delivered cost, climate modeling, robotics evidence, uncertainty, and governance remain bottlenecks or research gaps.",
    caution: "The scorecard is a synthesis of the current model suite. Status labels are internal research judgments, not expert consensus or peer-reviewed validation.",
    source: `${githubUrl}/blob/main/analysis/tables/aether_feasibility_gate_scorecard.csv`,
  },
  {
    id: "robotics",
    number: "03",
    title: "Robotics is a field-productivity problem",
    src: "/charts/robotics-field-productivity-gate.png",
    alt: "AETHER robotics field-productivity distribution gate comparing annual robot requirements",
    badge: "open" as const,
    interpretation: "The model applies uptime, autonomy, task-fit, maintenance, and supervision multipliers before comparing AETHER robot requirements with current annual industrial robot installations.",
    caution: "The optimistic deep-modular case clears the count comparison because infrastructure is assumed to be redesigned for automation. That task suitability still has to be demonstrated in field evidence.",
    source: `${githubUrl}/blob/main/analysis/tables/aether_robotics_field_productivity_distribution_summary.csv`,
  },
] as const;

export default function ModelGallery() {
  return (
    <main className="model-page">
      <header className="public-nav">
        <AetherMark />
        <nav aria-label="Model navigation">
          <a href="/#system">System</a>
          <a href="#capacity">Capacity</a>
          <a href="#gates">Gates</a>
          <a href="#robotics">Robotics</a>
        </nav>
        <a className="nav-paper" href={paperUrl}>Read the paper <Arrow /></a>
      </header>

      <section className="model-gallery-hero">
        <p className="section-code">AETHER / SELECTED MODEL VIEWS</p>
        <h1>Show the system.<br /><em>Show where it breaks.</em></h1>
        <div>
          <p>These figures are outputs from a coupled feasibility-boundary model. They expose how energy, industrial capacity, storage, economics, robotics, climate response, verification, and governance interact.</p>
          <p>They are not forecasts. The 100 GtCO₂/year reference case is intentionally extreme so hidden dependencies become visible.</p>
        </div>
      </section>

      <section className="model-gallery">
        {figures.map((figure) => (
          <article id={figure.id} key={figure.id}>
            <header>
              <span>{figure.number}</span>
              <h2>{figure.title}</h2>
              <EvidenceBadge kind={figure.badge} />
            </header>
            <figure>
              <img src={figure.src} alt={figure.alt} loading="lazy" />
            </figure>
            <div className="figure-reading">
              <div><span>WHAT IT SHOWS</span><p>{figure.interpretation}</p></div>
              <div><span>READ WITH CAUTION</span><p>{figure.caution}</p></div>
              <a href={figure.source}>Inspect the source table <Arrow /></a>
            </div>
          </article>
        ))}
      </section>

      <section className="model-gallery-close">
        <p className="section-code">THE RESEARCH LAYER</p>
        <h2>Every curve should lead back to assumptions, units, and source tables.</h2>
        <div><a className="button button-primary" href={paperUrl}>Read the working paper <Arrow /></a><a className="button button-secondary" href={githubUrl}>Inspect the repository <Arrow /></a></div>
      </section>

      <footer className="public-footer">
        <div><AetherMark compact /><p>A public research project initiated by Noah Hicks.</p></div>
        <div className="footer-links"><a href="/">Home</a><a href={paperUrl}>Working paper</a><a href={githubUrl}>GitHub</a></div>
        <p className="footer-note">Selected outputs from the AETHER model suite. Scenario results are not deployment claims.</p>
      </footer>
    </main>
  );
}
