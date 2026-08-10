/* eslint-disable @next/next/no-img-element -- Static research figures are already optimized publication assets. */
import type { Metadata } from "next";
import { AetherMark, Arrow, EvidenceBadge, ReadLinks } from "./components";
import { githubUrl, paperUrl } from "./data";

export const metadata: Metadata = {
  title: "Climate recovery as public infrastructure",
  description:
    "AETHER asks whether AI, robotics, clean power, and durable carbon removal could make atmospheric recovery an inspectable public capability.",
  alternates: { canonical: "/" },
};

const utilityLedger = [
  {
    number: "01",
    title: "Set the budget",
    copy: "A public institution defines the atmospheric operating range, the net carbon budget, and the conditions under which that budget tightens or expands.",
  },
  {
    number: "02",
    title: "Meter net use",
    copy: "Verified additions and removals are recorded by source, pathway, durability, location, and risk. Unmeasured tonnes do not enter the ledger.",
  },
  {
    number: "03",
    title: "Price the load",
    copy: "Industry pays for permitted net use of a shared atmospheric service. The price reflects scarcity, removal cost, storage durability, and system risk.",
  },
  {
    number: "04",
    title: "Maintain the system",
    copy: "Revenue funds removal, storage, monitoring, liability reserves, and public benefit while operators adjust capacity as measurements change.",
  },
] as const;

const acronym = [
  ["A", "Atmospheric", "The medium whose carbon concentration the system is built to manage."],
  ["E", "Engineering", "A measurable, maintainable capability rather than an offset promise."],
  ["T", "Through", "The link across energy, industry, storage, markets, and public governance."],
  ["H", "High-", "The honest scale of the industrial burden, even in an automation-rich future."],
  ["E", "Energy", "The physical input that intelligence and robotics cannot remove from the equation."],
  ["R", "Removal", "Verified drawdown used to keep the atmospheric carbon budget balanced over time."],
] as const;

const scenarioLinks = [
  {
    name: "Situational Awareness",
    href: "https://situational-awareness.ai/",
    timing: "Fast capability branch",
    copy: "Useful for stress-testing rapid cognitive progress, datacenter power demand, and industrial mobilization.",
  },
  {
    name: "AI 2027",
    href: "https://ai-2027.com/",
    timing: "Short-timeline branch",
    copy: "Useful for asking how little time institutions and physical supply chains might have to adapt.",
  },
  {
    name: "AI 2040: Plan A",
    href: "https://ai-2040.com/",
    timing: "Governance-bounded branch",
    copy: "Useful for testing slower scaling, transparency, verification, and coordinated control of advanced AI.",
  },
] as const;

export default function Home() {
  return (
    <main className="aether-site">
      <header className="public-nav">
        <AetherMark />
        <nav aria-label="Primary navigation">
          <a href="#system">System</a>
          <a href="#name">The name</a>
          <a href="#target">Target</a>
          <a href="#research">Research</a>
          <a href="/model">Model</a>
        </nav>
        <a className="nav-paper" href={paperUrl}>Read the paper <Arrow /></a>
      </header>

      <section className="public-hero">
        <div className="public-hero-image" role="img" aria-label="A coastal landscape with atmospheric research infrastructure" />
        <div className="public-hero-shade" aria-hidden="true" />
        <div className="public-hero-copy">
          <p className="section-code">AETHER / OPEN RESEARCH / NOAH HICKS</p>
          <h1>Operate the climate-recovery system <em>in public.</em></h1>
          <p className="public-hero-deck">
            AETHER asks whether AI, robotics, clean power, and durable carbon removal could become an inspectable public capability for steering atmospheric CO₂ back toward a preindustrial range.
          </p>
          <div className="hero-actions">
            <a className="button button-primary" href="#system">See the system <Arrow direction="down" /></a>
            <a className="button button-glass" href={paperUrl}>Read the working paper <Arrow /></a>
          </div>
        </div>
        <div className="hero-status" aria-label="Project status">
          <span>STATUS / CONDITIONAL WORKING PAPER</span>
          <p>Not a deployment claim. A coupled feasibility test designed to be criticized.</p>
        </div>
      </section>

      <section className="public-proposition">
        <div className="public-margin"><span>01</span><p>THE PROPOSITION</p></div>
        <div>
          <p className="public-lead">Industrial carbon can be useful. Atmospheric capacity is finite. AETHER asks how a public system could <em>measure, price, remove, and govern</em> the difference.</p>
          <div className="proposition-columns">
            <p>AETHER is not one capture machine and not a prediction that technology will arrive on schedule. It is a model of the whole operating problem: energy, capture, materials, transport, storage, measurement, ecological limits, capital, and public authority.</p>
            <p>The premise is not that every emission must disappear. Useful activity can continue inside a measured carbon budget. The optimistic bet is that capable AI and autonomous systems could make that budget physically manageable; thermodynamics, geology, supply chains, law, and consent still set the terms.</p>
          </div>
        </div>
      </section>

      <section className="public-utility" id="system">
        <div className="utility-intro">
          <p className="section-code">02 / A PUBLIC CARBON UTILITY</p>
          <h2>Use atmospheric capacity. Pay for it. Keep the balance public.</h2>
          <p>AETHER proposes an institutional model, not a description of current law: citizens hold the atmospheric service through a public trust or comparable commons institution. Industry can use a defined share when the social value justifies it, but that use is measured, priced, and reconciled against durable removal.</p>
        </div>
        <div className="utility-ledger" aria-label="Four-part public carbon utility model">
          {utilityLedger.map((entry) => (
            <article key={entry.number}>
              <span>{entry.number}</span>
              <h3>{entry.title}</h3>
              <p>{entry.copy}</p>
            </article>
          ))}
        </div>
        <div className="utility-rule">
          <strong>Industrial activity remains possible.</strong>
          <p>What disappears is the assumption that the shared atmospheric sink is free, unlimited, or governed only after damage occurs.</p>
        </div>
      </section>

      <section className="aether-definition" id="name">
        <div className="definition-heading">
          <p className="section-code">03 / WHAT AETHER MEANS</p>
          <h2>The name states the operating burden.</h2>
          <p>AETHER is blunt about the hard part. Managing atmospheric carbon at scale requires physical infrastructure, public authority, and a great deal of clean energy.</p>
        </div>
        <div className="definition-word" aria-hidden="true">AETHER</div>
        <div className="definition-list" aria-label="AETHER acronym expanded">
          {acronym.map(([letter, word, copy]) => (
            <div className="definition-row" key={`${letter}-${word}`}>
              <strong>{letter}</strong>
              <h3>{word}</h3>
              <p>{copy}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="autonomy-infrastructure">
        <div className="autonomy-visual" role="img" aria-label="Coastal carbon-removal infrastructure integrated with a living landscape">
          <div className="autonomy-caption"><span>AI + ROBOTICS</span><p>Coordination becomes physical only through machines, energy, materials, and accountable operators.</p></div>
        </div>
        <div className="autonomy-copy">
          <p className="section-code">04 / AUTONOMOUS INFRASTRUCTURE</p>
          <h2>Intelligence coordinates. Machines do the work.</h2>
          <p>AI could compress materials discovery, plant design, scheduling, dispatch, anomaly detection, and system-wide optimization. Specialized robots could manufacture modules, build and service sites, inspect wells and pipelines, maintain contactors, and collect field evidence.</p>
          <div className="role-ledger">
            <div><span>AI systems</span><p>Search, model, allocate, schedule, monitor, diagnose.</p></div>
            <div><span>Physical automation</span><p>Manufacture, construct, move, maintain, inspect.</p></div>
            <div><span>Public institutions</span><p>Set targets, grant permission, assign liability, stop the system.</p></div>
          </div>
          <EvidenceBadge kind="open" />
        </div>
      </section>

      <section className="atmospheric-target" id="target">
        <div className="target-head">
          <p className="section-code">05 / THE ATMOSPHERIC NORTH STAR</p>
          <h2>From 428.55 ppm toward roughly 280.</h2>
          <p>NOAA’s April 2026 global monthly mean is a dated baseline, not a permanent “current” value. The preindustrial anchor is approximate. The path between them is a carbon-cycle and governance problem, not simple subtraction.</p>
        </div>
        <div className="ppm-compare">
          <div className="ppm-row ppm-now">
            <div><span>APRIL 2026 / NOAA GLOBAL MEAN</span><strong>428.55 <small>ppm</small></strong></div>
            <div className="ppm-track" aria-label="428.55 parts per million"><i /></div>
            <p>0.042855% of dry air · 1.53× the 280 ppm anchor · about 53% above it</p>
          </div>
          <div className="ppm-row ppm-goal">
            <div><span>LONG-HORIZON RESTORATION NORTH STAR</span><strong>≈280 <small>ppm</small></strong></div>
            <div className="ppm-track" aria-label="Approximately 280 parts per million"><i /></div>
            <p>0.028% of dry air · a 148.55 ppm gap from the April baseline · about 34.7% below that concentration</p>
          </div>
        </div>
        <div className="target-note">
          <EvidenceBadge kind="model" />
          <p>The current paper uses a 350 ppm control floor to test whether a managed system throttles instead of removing blindly. It is not the project’s final recommended target. Modeling a responsible path to a preindustrial range remains future work.</p>
          <a href="https://www.gml.noaa.gov/ccgg/trends/global.html">View the NOAA measurement source <Arrow /></a>
        </div>
      </section>

      <section className="carbon-after">
        <div className="carbon-statement">
          <p className="section-code">06 / CARBON AFTER RESTORATION</p>
          <h2>The target is a control boundary, not a finish line to overshoot.</h2>
        </div>
        <div className="carbon-copy">
          <p>As atmospheric CO₂ approaches an agreed operating range, the removal system should throttle. Captured carbon could become a feedstock for durable materials or tightly closed industrial cycles when lifecycle accounting shows where it goes and for how long.</p>
          <p>The opportunity is to treat carbon as a managed resource: useful industrial flows can continue, while the public balance sheet prevents net atmospheric loading from outrunning verified removal.</p>
        </div>
      </section>

      <section className="governance-band">
        <div><span>AUTHORITY</span><strong>Who sets the target?</strong><p>Public institutions, affected communities, and independent science—not an autonomous fleet.</p></div>
        <div><span>EVIDENCE</span><strong>What counts as removal?</strong><p>Net, additional, durable, independently measured carbon with lifecycle emissions and reversal risk included.</p></div>
        <div><span>STOP CONDITION</span><strong>What ends an intervention?</strong><p>Atmospheric thresholds, ecological harm, failed verification, revoked permission, or a safer alternative.</p></div>
      </section>

      <section className="scenario-context" id="research">
        <div className="scenario-intro">
          <p className="section-code">07 / AI SCENARIO CONTEXT</p>
          <h2>Use future scenarios to test the premise—not to certify it.</h2>
          <p>These projects explore very different timelines and governance paths for advanced AI. AETHER uses them as boundary conditions. None establishes robot field productivity, clean-power availability, capture energy, or storage throughput.</p>
        </div>
        <div className="scenario-list">
          {scenarioLinks.map((scenario) => (
            <a href={scenario.href} key={scenario.name}>
              <span>{scenario.timing}</span>
              <h3>{scenario.name}</h3>
              <p>{scenario.copy}</p>
              <Arrow />
            </a>
          ))}
        </div>
      </section>

      <section className="model-showcase" id="model">
        <div className="model-showcase-head">
          <p className="section-code">08 / INSIDE THE SYSTEMS MODEL</p>
          <h2>A coupled model, not a single heroic curve.</h2>
          <p>The figure suite asks whether removal capacity survives simultaneous limits on energy, robot supply, storage, budget, field productivity, lifecycle emissions, verification, and governance.</p>
          <a className="text-link" href="/model">Open the model gallery <Arrow /></a>
        </div>
        <div className="model-figure-stack">
          <figure>
            <img src="/charts/integrated-capacity-paths-2026-2046.png" alt="AETHER modeled removal-capacity paths from 2026 to 2046 under integrated constraints" />
            <figcaption><span>INTEGRATED CAPACITY PATHS</span><p>Only the upper-tail AETHER and moonshot branches approach the 100 GtCO₂/year stress-test target by 2046. Reference and energy-constrained paths remain far below it.</p></figcaption>
          </figure>
          <figure>
            <img src="/charts/robotics-field-productivity-gate.png" alt="AETHER robotics field-productivity distribution gate comparing annual robot requirements" />
            <figcaption><span>ROBOTICS PRODUCTIVITY GATE</span><p>Robot counts look plausible only when uptime, autonomy, task fit, maintenance, and supervision penalties clear together. That remains a research gate, not an established capability.</p></figcaption>
          </figure>
        </div>
      </section>

      <section className="terraform-note">
        <p className="section-code">09 / THE LONG VIEW</p>
        <div>
          <h2>A low form of terraforming—beginning with responsibility on Earth.</h2>
          <p>Deliberately changing an atmosphere at scale qualifies as a restrained form of terraforming. That framing raises the burden of evidence and consent. Descendant systems for autonomous construction, resource cycling, atmospheric processing, and remote verification could one day matter on other celestial bodies. Earth is where the governance has to be learned first.</p>
        </div>
      </section>

      <section className="public-invitation">
        <div>
          <p className="section-code">10 / OPEN THE MODEL</p>
          <h2>Make the optimistic claim precise enough to test.</h2>
        </div>
        <div>
          <p>AETHER is an open research program initiated by Noah Hicks. The paper is one interface to the idea; the repository is where assumptions, models, evidence gaps, and criticism can accumulate.</p>
          <ReadLinks />
        </div>
      </section>

      <footer className="public-footer">
        <div><AetherMark compact /><p>A public research project initiated by Noah Hicks.</p></div>
        <div className="footer-links"><a href={paperUrl}>Working paper</a><a href={githubUrl}>GitHub</a><a href="#system">System</a><a href="#target">Target</a></div>
        <p className="footer-note">Conditional research, not a deployment claim. Numbers are sourced measurements or labeled model outputs.</p>
      </footer>
    </main>
  );
}
