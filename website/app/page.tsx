import type { Metadata } from "next";
import { Arrow, EvidenceBadge, ReadLinks, SiteFooter, SiteNav } from "./components";
import { atmosphere, constraints, correctionUrl, githubUrl, tableUrl } from "./data";

export const metadata: Metadata = {
  title: "Climate recovery as public infrastructure",
  description:
    "Explore atmospheric carbon as public infrastructure: a regional research case, accountable automation, and an open working paper by Noah Hicks.",
  alternates: { canonical: "/" },
};

const navLinks = [
  { href: "#utility", label: "The utility" },
  { href: "#regional", label: "Regional case" },
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
    copy: "Operating fees and separately identified legacy-removal funding cover service, monitoring and reserves. Independent verification keeps operators accountable.",
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

export default function Home() {
  return (
    <main className="aether-site" id="main">
      <SiteNav links={navLinks} label="Primary navigation" />

      <section className="public-hero">
        <div className="public-hero-image" role="img" aria-label="A coastal landscape under heavy atmosphere" />
        <div className="public-hero-shade" aria-hidden="true" />
        <div className="public-hero-copy">
          <p className="section-code">AETHER / OPEN RESEARCH / NOAH HICKS</p>
          <h1>The atmosphere is shared. <em>What if we managed it?</em></h1>
          <p className="public-hero-deck">
            AETHER explores atmospheric carbon as public infrastructure: autonomous systems doing the work, useful industry inside a measured budget, and institutions accountable for the balance.
          </p>
          <div className="hero-actions">
            <a className="button button-primary" href="#utility">See the system <Arrow direction="down" /></a>
            <a className="button button-glass" href="/evidence">Read the evidence <Arrow /></a>
          </div>
        </div>
        <div className="hero-status" aria-label="Project status">
          <span>STATUS / CONDITIONAL WORKING PAPER</span>
          <p>An ambitious research direction, with a smaller operating case you can inspect. No deployment or probability of success is claimed.</p>
        </div>
      </section>

      <section className="honest-band" id="regional" aria-labelledby="regional-heading">
        <p className="section-code">01 / START WITH ONE OPERATING SYSTEM</p>
        <h2 id="regional-heading">A planetary ambition.<br /><em>A regional test of the idea.</em></h2>
        <div className="honest-figures">
          <div>
            <strong>1 Mt / yr</strong>
            <span>Illustrative nameplate capacity</span>
            <p>A regional direct-air-capture and storage benchmark. Actual output is limited by its resources and operating assumptions.</p>
          </div>
          <div>
            <strong>Same physics</strong>
            <span>Two operating cases</span>
            <p>Compare ordinary operations with assumed automation assistance. Electricity, heat and storage requirements do not disappear.</p>
          </div>
          <div>
            <strong>Open ledger</strong>
            <span>Carbon and cash, separately</span>
            <p>See gross capture, lifecycle burdens, durability and funding. Change a constraint and the supported output must change with it.</p>
          </div>
        </div>
        <p className="honest-note">
          This is an analytical example, not a proposed construction site or a validated plant design. The original 100 Gt/year global case remains a stress test, not the project&rsquo;s predicted scale. <a href="/evidence#regional-case">Explore the paired case <Arrow /></a>
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
              A capture machine provides one service. A working system also needs power and heat, storage, maintenance, a solvent operator and an independent account of what happened to the carbon. AETHER studies those connections through a regional example and a wider set of screening models.
            </p>
            <p>
              The optimistic premise is that increasingly capable AI and robotics could make this infrastructure easier to build and operate. The research question is where that improvement survives contact with physical constraints, competing uses of resources and public consent.
            </p>
          </div>
        </div>
      </section>

      <section className="public-utility" id="utility">
        <div className="utility-intro">
          <p className="section-code">03 / A PUBLIC CARBON UTILITY</p>
          <h2>A shared service.<br />A measured balance.</h2>
          <p>
            AETHER examines a public carbon utility: an institution that sets an operating budget, procures removal and carries long-term obligations. Public trusts, regulated operators and regional procurement arrangements have different authority and incentive problems. None is assumed to work merely because it is public.
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
          <p>Managing ongoing emissions and drawing down historical accumulation are different services. Their physical obligations and funding need to be accounted for separately.</p>
        </div>
      </section>

      <section className="strain-section" id="strain">
        <div className="strain-head">
          <p className="section-code">04 / WHERE THE MODEL STRAINS</p>
          <h2>What determines<br />how far it can go.</h2>
          <p>
            These are the constraints the research has to connect. A correct calculation can expose a requirement; it cannot establish that the necessary infrastructure or institution will exist.
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
            The paired regional example asks a narrower question: what changes if maintenance takes fewer labor hours or equipment stays available longer? Those improvements are explicit assumptions, not demonstrated robot performance. Measuring them in the field is a useful next contribution.
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
            NOAA&rsquo;s preliminary {atmosphere.observationMonth} global monthly mean is a dated observation, not a live feed. Roughly 280 ppm is our long-horizon restoration aspiration, not a demonstrated safe or optimal modern setpoint. Getting there is a carbon-cycle and governance problem, not subtraction.
          </p>
        </div>
        <div className="ppm-compare">
          <div className="ppm-row ppm-now">
            <div><span>{atmosphere.observationMonth.toUpperCase()} / NOAA GLOBAL MEAN</span><strong>{atmosphere.current} <small>ppm</small></strong></div>
            <div className="ppm-track" aria-label={`${atmosphere.current} parts per million`}><i /></div>
            <p>{atmosphere.dryAirPercent.toFixed(6)}% of dry air · {atmosphere.referenceRatio.toFixed(2)}× the {atmosphere.preindustrial} ppm anchor · about {((atmosphere.referenceRatio - 1) * 100).toFixed(0)}% above it</p>
          </div>
          <div className="ppm-row ppm-goal">
            <div><span>LONG-HORIZON RESTORATION NORTH STAR</span><strong>≈{atmosphere.preindustrial} <small>ppm</small></strong></div>
            <div className="ppm-track" aria-label={`Approximately ${atmosphere.preindustrial} parts per million`}><i style={{ width: `${100 / atmosphere.referenceRatio}%` }} /></div>
            <p>0.028% of dry air · a {atmosphere.gapPpm.toFixed(2)} ppm gap from the dated observation · about {atmosphere.reductionPercent.toFixed(1)}% below that concentration</p>
          </div>
        </div>
        <div className="target-note">
            <EvidenceBadge kind="open" />
          <p>
            No credible arrival date is established here. Absolute climate projections have been withdrawn after a failed baseline diagnostic. A responsible trajectory must account for land, oceans, other climate forcings and ecological effects.
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
            Carbon use is not automatically durable removal. Fuels and short-lived products can release it again; long-lived products need a verified fate. Product revenue also cannot be assumed to fund the entire removal system.
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
            These projects explore different AI futures. They provide scenario context, not measured inputs for construction speed, robot reliability, capture energy or storage throughput.
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
          <h2>Help turn the idea<br />into evidence.</h2>
        </div>
        <div>
          <p>
            Start with a specific question: check the regional energy balance, replace an automation assumption with field evidence, or test the utility&rsquo;s funding under failure. The working paper is not externally peer reviewed. <a className="inline-link" href={`${githubUrl}/blob/main/docs/REVIEW_GUIDE.md`}>The review guide</a> identifies contributions that could change its conclusions.
          </p>
          <ReadLinks />
          <a className="text-link" href={correctionUrl}>What changed in v0.46 <Arrow /></a>
        </div>
      </section>

      <SiteFooter note="Conditional research, not a deployment claim. Every figure is a sourced measurement or a labeled model output." />
    </main>
  );
}
