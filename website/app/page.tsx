import type { Metadata } from "next";
import { Arrow, EvidenceBadge, ReadLinks, SiteFooter, SiteNav } from "./components";
import { atmosphere, constraints, gateTally, tableUrl, uncertainty } from "./data";

export const metadata: Metadata = {
  title: "Climate recovery as public infrastructure",
  description:
    "AETHER models what it would take to run atmospheric carbon as a metered public utility, and publishes the points where that model breaks.",
  alternates: { canonical: "/" },
};

const navLinks = [
  { href: "#utility", label: "The utility" },
  { href: "#strain", label: "Where it strains" },
  { href: "#target", label: "Target" },
  { href: "/evidence", label: "Evidence" },
] as const;

const utilityLedger = [
  {
    number: "01",
    title: "Set the budget",
    copy: "A public institution fixes the atmospheric operating range and the net carbon budget, and states the conditions under which that budget tightens.",
  },
  {
    number: "02",
    title: "Meter net use",
    copy: "Additions and removals are recorded by source, pathway, durability, location, and risk. A tonne nobody measured does not enter the ledger.",
  },
  {
    number: "03",
    title: "Price the load",
    copy: "Industry pays for permitted net use of a shared service. The price tracks scarcity, removal cost, storage durability, and system risk.",
  },
  {
    number: "04",
    title: "Maintain the system",
    copy: "Revenue funds removal, storage, monitoring, liability reserves, and public benefit. Operators move capacity as the measurements move.",
  },
] as const;

const acronym = [
  ["A", "Atmospheric", "The medium whose carbon concentration the system manages."],
  ["E", "Engineering", "A maintainable capability, measured — not an offset promise."],
  ["T", "Through", "The link across energy, industry, storage, markets, and law."],
  ["H", "High-", "The real industrial burden, even in an automation-rich future."],
  ["E", "Energy", "The input that intelligence cannot remove from the equation."],
  ["R", "Removal", "Verified drawdown, used to keep the budget balanced over time."],
] as const;

const scenarioLinks = [
  {
    name: "Situational Awareness",
    href: "https://situational-awareness.ai/",
    timing: "Fast capability branch",
    copy: "Stress-tests rapid cognitive progress, datacenter power demand, and industrial mobilization.",
  },
  {
    name: "AI 2027",
    href: "https://ai-2027.com/",
    timing: "Short-timeline branch",
    copy: "Asks how little time institutions and physical supply chains might get.",
  },
  {
    name: "AI 2040: Plan A",
    href: "https://ai-2040.com/",
    timing: "Governance-bounded branch",
    copy: "Tests slower scaling with transparency, verification, and coordinated control.",
  },
] as const;

const percent = (share: number, digits = 2) => `${(share * 100).toFixed(digits)}%`;

export default function Home() {
  return (
    <main className="aether-site" id="main">
      <SiteNav links={navLinks} label="Primary navigation" />

      <section className="public-hero">
        <div className="public-hero-image" role="img" aria-label="A coastal landscape under heavy atmosphere" />
        <div className="public-hero-shade" aria-hidden="true" />
        <div className="public-hero-copy">
          <p className="section-code">AETHER / OPEN RESEARCH / NOAH HICKS</p>
          <h1>The atmosphere is infrastructure. <em>Nobody controls it.</em></h1>
          <p className="public-hero-deck">
            AETHER models what it would take to run atmospheric carbon as a metered public utility. It lays out a scenario for highly autonomous systems to manage our atmosphere directly.
          </p>
          <div className="hero-actions">
            <a className="button button-primary" href="#utility">See the system <Arrow direction="down" /></a>
            <a className="button button-glass" href="/evidence">Read the evidence <Arrow /></a>
          </div>
        </div>
        <div className="hero-status" aria-label="Project status">
          <span>STATUS / CONDITIONAL WORKING PAPER</span>
          <p>This is a feasibility test built to be attacked. And when the time comes, it is meant to remind us to push for incredible goals.</p>
        </div>
      </section>

      <section className="honest-band" aria-labelledby="honest-heading">
        <p className="section-code">01 / THE NUMBER THAT KEEPS THIS HONEST</p>
        <h2 id="honest-heading">
          Across {uncertainty.samples.toLocaleString()} model draws, <em>{percent(uncertainty.durableHundredShare)}</em> deliver 100 Gt of durable credited removal a year.
        </h2>
        <div className="honest-figures">
          <div>
            <strong>{uncertainty.durableCredit.p50} Gt</strong>
            <span>Median durable credit per year</span>
            <p>Well under a third of the headline case the paper stress-tests.</p>
          </div>
          <div>
            <strong>{percent(uncertainty.positiveReversalShare, 0)}</strong>
            <span>Draws with any net removal at all</span>
            <p>After residual emissions and rebound are subtracted.</p>
          </div>
          <div>
            <strong>{percent(uncertainty.strongReversalShare, 1)}</strong>
            <span>Draws reversing at today&rsquo;s emission rate</span>
            <p>Strong reversal is a tail outcome, not the central expectation.</p>
          </div>
        </div>
        <p className="honest-note">
          The 100 GtCO₂/year case is an extreme boundary chosen to expose hidden dependencies, not a forecast. Publishing the distribution rather than the best branch is the whole point of the exercise.
          {" "}
          <a href={tableUrl(uncertainty.table)}>Inspect the uncertainty table <Arrow /></a>
        </p>
      </section>

      <section className="public-proposition">
        <div className="public-margin"><span>02</span><p>THE PROPOSITION</p></div>
        <div>
          <p className="public-lead">
            Industrial carbon can be useful. Atmospheric capacity is finite. AETHER asks how a public system could <em>measure, price, and settle</em> the difference.
          </p>
          <div className="proposition-columns">
            <p>
              This is a model of the whole operating problem rather than one capture machine — energy and materials at the front, storage and verification at the back, capital and public authority holding it together. Component models pass on their own. The integrated system is where the trouble lives.
            </p>
            <p>
              The premise is not that every emission disappears. Useful activity continues inside a measured budget. The optimistic bet is that capable AI and autonomous systems make that budget physically manageable. Thermodynamics, geology, supply chains, and consent still set the terms.
            </p>
          </div>
        </div>
      </section>

      <section className="public-utility" id="utility">
        <div className="utility-intro">
          <p className="section-code">03 / A PUBLIC CARBON UTILITY</p>
          <h2>Use atmospheric capacity. Pay for it. Keep the balance public.</h2>
          <p>
            An institutional proposal, not a description of current law: citizens hold the atmospheric service through a public trust or comparable commons institution. Industry can draw a defined share when the social value justifies it, and that draw is metered, priced, and reconciled against durable removal.
          </p>
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
          <p>What ends is the assumption that the shared sink is free, unlimited, and governed only after the damage lands.</p>
        </div>
      </section>

      <section className="strain-section" id="strain">
        <div className="strain-head">
          <p className="section-code">04 / WHERE THE MODEL STRAINS</p>
          <h2>Six places the system stops being clever and starts being physics.</h2>
          <p>
            Each anchor below is quoted from a generated table, not restated from the argument. Four are bottlenecks, one is an open research gap, one is a governance problem that no amount of engineering fixes.
          </p>
        </div>
        <ul className="strain-list">
          {constraints.map((item) => (
            <li key={item.name}>
              <div className="strain-label">
                <h3>{item.name}</h3>
                <span className={`strain-verdict verdict-${item.verdict.split(" ")[0].toLowerCase()}`}>{item.verdict}</span>
              </div>
              <div className="strain-anchor">
                <strong>{item.anchor}</strong>
                <span>{item.anchorNote}</span>
              </div>
              <p className="strain-reading">{item.reading}</p>
              <a href={tableUrl(item.table)} aria-label={`Source table for ${item.name}`}>Source <Arrow /></a>
            </li>
          ))}
        </ul>
      </section>

      <section className="autonomy-infrastructure">
        <div className="autonomy-visual" role="img" aria-label="Coastal carbon-removal infrastructure integrated with a living landscape">
          <div className="autonomy-caption">
            <span>AI + ROBOTICS</span>
            <p>Coordination becomes physical only through machines, energy, materials, and operators who can be held to account.</p>
          </div>
        </div>
        <div className="autonomy-copy">
          <p className="section-code">05 / AUTONOMOUS INFRASTRUCTURE</p>
          <h2>Intelligence schedules the work. Something still has to do it.</h2>
          <p>
            AI could compress materials discovery, plant design, dispatch, anomaly detection, and system-wide optimization. Robots could build modules, service sites, inspect wells, maintain contactors, and gather field evidence.
          </p>
          <p>
            The model does not assume that software capability becomes reliable field robotics. In the automation-push case, duty-cycle, autonomy, task-fit, maintenance, and supervision penalties raise median annual production from about 234,000 to 840,000 robots and reduce the count-screen pass share to zero. The deep-modular branch still clears that count screen, but only by assuming infrastructure redesigned around automation. That gap is the research, not a footnote to it.
          </p>
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
          <p className="section-code">06 / THE ATMOSPHERIC NORTH STAR</p>
          <h2>From {atmosphere.current} ppm toward roughly {atmosphere.preindustrial}.</h2>
          <p>
            NOAA&rsquo;s April 2026 global monthly mean is a dated baseline, not a permanent &ldquo;current&rdquo; value. The preindustrial anchor is approximate. What sits between them is a carbon-cycle and governance problem, not subtraction.
          </p>
        </div>
        <div className="ppm-compare">
          <div className="ppm-row ppm-now">
            <div><span>APRIL 2026 / NOAA GLOBAL MEAN</span><strong>{atmosphere.current} <small>ppm</small></strong></div>
            <div className="ppm-track" aria-label={`${atmosphere.current} parts per million`}><i /></div>
            <p>0.042855% of dry air · 1.53× the {atmosphere.preindustrial} ppm anchor · about 53% above it</p>
          </div>
          <div className="ppm-row ppm-goal">
            <div><span>LONG-HORIZON RESTORATION NORTH STAR</span><strong>≈{atmosphere.preindustrial} <small>ppm</small></strong></div>
            <div className="ppm-track" aria-label={`Approximately ${atmosphere.preindustrial} parts per million`}><i /></div>
            <p>0.028% of dry air · a 148.55 ppm gap from the April baseline · about 34.7% below that concentration</p>
          </div>
        </div>
        <div className="target-note">
          <EvidenceBadge kind="model" />
          <p>
            The current paper uses a {atmosphere.controlFloor} ppm control floor to test whether a managed system throttles instead of removing blindly. It is not the recommended final target. Modeling a responsible path to a preindustrial range is still ahead.
          </p>
          <a href={atmosphere.source}>NOAA measurement source <Arrow /></a>
        </div>
      </section>

      <section className="carbon-after">
        <div className="carbon-statement">
          <p className="section-code">07 / CARBON AFTER RESTORATION</p>
          <h2>The target is a control boundary, not a finish line to overshoot.</h2>
        </div>
        <div className="carbon-copy">
          <p>
            As concentration approaches an agreed operating range, the removal system should throttle down. Captured carbon can become feedstock for durable materials or tightly closed industrial cycles, provided lifecycle accounting shows where it went and for how long.
          </p>
          <p>
            Treating carbon as a managed resource keeps useful industrial flows running while the public balance sheet stops net loading from outrunning verified removal.
          </p>
        </div>
      </section>

      <section className="aether-definition" id="name">
        <div className="definition-heading">
          <p className="section-code">08 / WHAT AETHER MEANS</p>
          <h2>The name focuses on the details.</h2>
          <p>Managing atmospheric carbon at scale takes physical infrastructure, public authority, and an enormous amount of clean energy. The acronym says so out loud.</p>
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

      <section className="governance-band">
        <div><span>AUTHORITY</span><strong>Who sets the target?</strong><p>Public institutions, affected communities, and independent science. Not an autonomous fleet.</p></div>
        <div><span>EVIDENCE</span><strong>What counts as removal?</strong><p>Net, additional, durable, independently measured carbon, with lifecycle emissions and reversal risk included.</p></div>
        <div><span>STOP CONDITION</span><strong>What ends an intervention?</strong><p>Atmospheric thresholds, ecological harm, failed verification, revoked permission, or a safer alternative.</p></div>
      </section>

      <section className="scenario-context" id="research">
        <div className="scenario-intro">
          <p className="section-code">09 / AI SCENARIO CONTEXT</p>
          <h2>Borrow the timelines. Don&rsquo;t borrow the certainty.</h2>
          <p>
            These projects explore very different futures for advanced AI, and AETHER uses them as boundary conditions. None of them establishes robot field productivity, clean-power availability, capture energy, or storage throughput — which is exactly where this model spends its time.
          </p>
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

      <section className="terraform-note">
        <p className="section-code">10 / THE LONG VIEW</p>
        <div>
          <h2>A low form of terraforming, starting with responsibility on Earth.</h2>
          <p>
            Deliberately changing an atmosphere at scale is a restrained form of terraforming, and that framing raises the burden of evidence and consent rather than lowering it. Descendant systems for autonomous construction, resource cycling, atmospheric processing, and remote verification might one day matter on other bodies. Earth is where the governance has to be learned first.
          </p>
        </div>
      </section>

      <section className="public-invitation">
        <div>
          <p className="section-code">11 / OPEN THE MODEL</p>
          <h2>Make the optimistic claim precise enough to break.</h2>
        </div>
        <div>
          <p>
            {gateTally.pass} of twelve submission gates pass, {gateTally.partial} are partial, and {gateTally.fail} fail outright. Those two failures are published, named, and linked to the work that would close them. Reproduce a model, replace a weak parameter, or take apart a claim that deserves it.
          </p>
          <ReadLinks />
        </div>
      </section>

      <SiteFooter note="Conditional research, not a deployment claim. Every figure is a sourced measurement or a labeled model output." />
    </main>
  );
}
