/* eslint-disable @next/next/no-img-element -- Reproducible publication figures, shared with the paper. */
import type { Metadata } from "next";
import { Arrow, EvidenceBadge, SiteFooter, SiteNav } from "../components";
import { correctionUrl, githubUrl, paperUrl, regional, supplementUrl, tableUrl } from "../data";

export const metadata: Metadata = {
  title: "Evidence, assumptions and limits",
  description: "A reproducible regional carbon-service example, its physical and financial ledgers, and the evidence AETHER still needs.",
  alternates: { canonical: "/evidence" },
};
const navLinks = [{ href: "/#utility", label: "The idea" }, { href: "#regional-case", label: "Regional case" }, { href: "#figures", label: "Figures" }, { href: "#limits", label: "Open questions" }];
const format = (value: number, digits=0) => value.toLocaleString("en-US", { maximumFractionDigits: digits, minimumFractionDigits: digits });
const rows = [
  ["Gross capture", "gross_capture_tco2_y", "tCO₂/year"],
  ["Gross stored", "gross_stored_tco2_y", "tCO₂/year"],
  ["Physical retention", "retained_tco2_y", "tCO₂/year"],
  ["Project emissions (debit)", "project_emissions_tco2e_y", "tCO₂e/year"],
  ["Net after project emissions", "net_retained_tco2e_y", "tCO₂e/year"],
  ["Risk-adjusted credits", "risk_adjusted_credits_tco2e_y", "tCO₂e/year"],
] as const;
const figures = [
  { id: "carbon-ledger", title: "A captured tonne is the start of the ledger.", src: "regional-carbon-ledger", alt: "Grouped bars distinguish gross capture, stored carbon, retention, net benefit and risk-adjusted credits in two regional cases.", table: "aether_regional_reference_summary.csv", reading: "Ordinary and automation-assisted cases share all per-tonne physical assumptions. The assumed availability improvement raises gross capture from 850,000 to 900,000 tonnes/year. Losses, project emissions and credit buffers remain explicit.", caution: "The difference is conditional on assumed uptime and task productivity. It is not measured automation performance. CO₂e accounting is not a species- and time-resolved climate prediction." },
  { id: "resources", title: "The tightest constraint sets the output.", src: "regional-resource-limits", alt: "Resource-limit comparison shows uptime limits ordinary and assisted output below their electricity, thermal-proxy, storage and budget ceilings.", table: "aether_regional_reference_resource_ledger.csv", reading: "The model takes the minimum of nameplate, availability, electricity, thermal-energy allowance, injection and budget. Halving electricity, the thermal allowance or storage removes the output advantage of the automation case.", caution: "This is an annual resource envelope, not hourly dispatch, a permitted site or a construction design. The graph's vertical axis starts at 700,000 tonnes/year to make differences readable." },
  { id: "funding", title: "Two services need two identified funding sources.", src: "regional-funding-ledger", alt: "Both regional cases assume 120 million dollars of current-load settlements and 180 million dollars of separate legacy funding; modeled uses are about 281 and 276 million dollars.", table: "aether_regional_reference_utility_ledger.csv", reading: "An illustrative current-load settlement funds part of the annual service. Separate legacy funding covers the wider drawdown program. Capital charges, labor, automation, energy, storage and reserves are counted once.", caution: "These are explicit funding and price assumptions, not available revenue, a recommended tariff, an investment return or a cost forecast. A positive annual balance does not establish full long-term solvency." },
];

export default function Evidence() {
  return <main className="aether-site evidence-page" id="main">
    <SiteNav links={navLinks} label="Evidence navigation" />
    <section className="evidence-hero">
      <p className="section-code">AETHER / EVIDENCE YOU CAN INSPECT</p>
      <h1>Show the system.<br /><em>Show its limits.</em></h1>
      <div><p>The ambition is planetary. The useful next test is regional: one process, shared physical constraints, two operating cases and a ledger that can be checked.</p><p>This is conditional research. The example below is neither a real plant proposal nor a forecast. It shows how a carbon service would have to account for its work.</p></div>
    </section>

    <section className="regional-section" id="regional-case">
      <div className="regional-head"><p className="section-code">01 / A BOUNDED OPERATING EXAMPLE</p><h2>Same process.<br />Different execution.</h2><p>A 1 MtCO₂/year gross nameplate benchmark anchored to a published NETL solvent-DAC process. Only assumed uptime, task hours and explicit automation costs change between the two cases.</p></div>
      <div className="regional-pair">
        {regional.cases.map((item) => <article key={item.scenario_id}>
          <span className="section-code">{item.case_label}</span><strong>{format(item.risk_adjusted_credits_tco2e_y / 1000, 1)}<small>thousand risk-adjusted tCO₂e/year</small></strong>
          <dl><div><dt>Assumed uptime</dt><dd>{format(item.uptime_fraction * 100)}%</dd></div><div><dt>Assumed task hours/year</dt><dd>{format(item.total_task_hours_y)}</dd></div><div><dt>Annual modeled uses</dt><dd>${format(item.total_uses_usd_y / 1e6, 1)}m</dd></div></dl>
        </article>)}
      </div>
      <p className="regional-caution">The automation-assisted case includes $12m/year of additional system cost. Higher uptime and fewer task hours are hypotheses to test—not capabilities already demonstrated by AETHER.</p>
      <details className="evidence-disclosure"><summary>Open the physical ledger and energy requirements <Arrow direction="down" /></summary>
        {/* The horizontally scrollable table needs keyboard focus on narrow screens. */}
        {/* eslint-disable-next-line jsx-a11y/no-noninteractive-tabindex */}
        <div className="ledger-scroll" tabIndex={0} role="region" aria-label="Regional carbon accounting table">
          <table><caption>Annual analytical outputs; displayed values rounded to whole tonnes.</caption><thead><tr><th scope="col">Accounting layer</th><th scope="col">Ordinary</th><th scope="col">Assisted</th></tr></thead><tbody>{rows.map(([label, key, unit]) => <tr key={key}><th scope="row">{label}<small>{unit}</small></th>{regional.cases.map(item => <td key={item.scenario_id}>{format(item[key])}</td>)}</tr>)}</tbody></table>
        </div>
        <p>Electricity and thermal energy have separate boundaries. Ordinary operations use {format(regional.cases[0].electricity_used_mwh_y / 1000, 1)} GWh/year and {format(regional.cases[0].thermal_used_gj_y / 1e6, 2)} PJ/year of fuel-input-equivalent thermal energy; the assisted case uses {format(regional.cases[1].electricity_used_mwh_y / 1000, 1)} GWh and {format(regional.cases[1].thermal_used_gj_y / 1e6, 2)} PJ. The thermal proxy derives from NETL&rsquo;s natural-gas HHV input, not delivered useful heat. Low-carbon substitution, temperature, conversion efficiency and hourly availability still need engineering evidence.</p>
        <a className="text-link" href={`${githubUrl}/blob/main/data/regional-reference/parameters.csv`}>Every parameter, unit and evidence label <Arrow /></a>
      </details>
    </section>

    <section className="figure-gallery" id="figures">
      <div className="gallery-head"><p className="section-code">02 / FOLLOW THE ACCOUNTING</p><h2>Three views of the same case.</h2><p>These figures and the website numbers are generated from the same checked-in regional outputs used by the paper.</p></div>
      {figures.map((figure, n) => <article id={figure.id} key={figure.id}>
        <header><span className="figure-number">0{n+1}</span><h3>{figure.title}</h3><EvidenceBadge kind="model" /></header>
        <figure>
          <figcaption className="figure-caption"><span className="figure-pan-hint">Swipe sideways to explore the chart.</span><a href={`/charts/${figure.src}.png`} target="_blank" rel="noreferrer">Open full-size chart <Arrow /></a></figcaption>
          {/* Native overflow regions need keyboard focus for arrow-key scrolling. */}
          {/* eslint-disable-next-line jsx-a11y/no-noninteractive-tabindex */}
          <div className="figure-scroll" role="region" aria-label={`${figure.title} Scrollable chart`} tabIndex={0}><img src={`/charts/${figure.src}.png`} alt={figure.alt} loading="lazy" /></div>
        </figure>
        <div className="figure-reading"><div><span>WHAT IT SHOWS</span><p>{figure.reading}</p></div><div><span>READ WITH CAUTION</span><p>{figure.caution}</p></div><a href={tableUrl(figure.table)}>Inspect the source table <Arrow /></a></div>
      </article>)}
    </section>

    <section className="research-limits" id="limits">
      <p className="section-code">03 / WHAT IS NOT ESTABLISHED</p><h2>Confidence should follow evidence.</h2>
      <div className="limit-grid">
        <article><span>WITHDRAWN</span><h3>Absolute climate projections</h3><p>The replacement baseline failed a zero-future-emissions diagnostic. Absolute concentration, temperature and arrival-date claims are quarantined. Historical carbon reservoirs and consistent emissions inputs must be resolved first.</p></article>
        <article><span>NOT A PROBABILITY</span><h3>The old Monte Carlo headline</h3><p>Sampling hand-set ranges measures those assumptions, not the likelihood of AETHER succeeding. The public headline no longer uses a pass percentage. Correlated cases also change marginal assumptions.</p></article>
        <article><span>NOT FULLY COUPLED</span><h3>The global model suite</h3><p>Power, robotics, storage and cost screens do not yet share a complete regional, chronological resource contract. Favorable standalone outputs cannot be added into a validated deployment path.</p></article>
        <article><span>EVIDENCE STILL NEEDED</span><h3>Real operating conditions</h3><p>Hourly power and heat, field automation data, basin-specific storage, independent verification, full lifecycle impacts and long-term funding remain open research tasks.</p></article>
      </div>
      <a className="text-link" href={correctionUrl}>Read the v0.46 correction record <Arrow /></a>
    </section>

    <section className="evidence-close"><p className="section-code">CONTRIBUTE</p><h2>A better parameter can change the conclusion.</h2><p>Reproduce the regional case, challenge its assumptions, or bring evidence for one missing constraint. The most useful contribution has a source, a unit, an uncertainty range and a clear account of what it changes.</p><div><a className="button button-primary" href={paperUrl}>Read the working paper <Arrow /></a><a className="button button-secondary" href={supplementUrl}>Technical supplement <Arrow /></a></div><a className="text-link" href={`${githubUrl}/blob/main/docs/REVIEW_GUIDE.md`}>Review and contribution guide <Arrow /></a></section>
    <SiteFooter note="Analytical scenarios, not deployment claims. Internal review is not external peer review." />
  </main>;
}
