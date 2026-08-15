import {
  gateTally,
  githubUrl,
  paperUrl,
  submissionGates,
  tableUrl,
  type GateStatus,
} from "./data";

type EvidenceKind = "established" | "model" | "open";

export function AetherMark({ compact = false }: { compact?: boolean }) {
  return (
    <a className={`aether-mark${compact ? " mark-compact" : ""}`} href="/" aria-label="AETHER home">
      <span className="mark-orbit" aria-hidden="true"><i /></span>
      <span>AETHER</span>
    </a>
  );
}

export function EvidenceBadge({ kind }: { kind: EvidenceKind }) {
  const label = kind === "established" ? "Established" : kind === "model" ? "AETHER model" : "Open question";
  return <span className={`evidence evidence-${kind}`}>{label}</span>;
}

export function Arrow({ direction = "right" }: { direction?: "right" | "down" }) {
  return <span className={`arrow arrow-${direction}`} aria-hidden="true">{direction === "down" ? "↓" : "↗"}</span>;
}

export function ReadLinks({ className = "" }: { className?: string }) {
  return (
    <div className={`read-links ${className}`}>
      <a className="button button-primary" href={paperUrl}>Read the working paper <Arrow /></a>
      <a className="button button-secondary" href={githubUrl}>Inspect the research <Arrow /></a>
    </div>
  );
}

type NavLink = { href: string; label: string };

/**
 * The desktop bar and the mobile disclosure render the same links. Keeping them
 * as separate elements avoids relying on `details` content being restyled while
 * closed, which browsers still handle inconsistently.
 */
export function SiteNav({ links, label }: { links: readonly NavLink[]; label: string }) {
  return (
    <header className="public-nav">
      <AetherMark />
      <nav className="nav-wide" aria-label={label}>
        {links.map((link) => (
          <a href={link.href} key={link.href}>{link.label}</a>
        ))}
      </nav>
      <a className="nav-paper" href={paperUrl}>
        <span>Read the paper</span> <Arrow />
      </a>
      <details className="nav-disclosure">
        <summary aria-label="Open navigation menu"><span /><span /></summary>
        <nav aria-label={`${label}, compact`}>
          {links.map((link) => (
            <a href={link.href} key={link.href}>{link.label}</a>
          ))}
          <a className="nav-disclosure-paper" href={paperUrl}>Read the paper <Arrow /></a>
        </nav>
      </details>
    </header>
  );
}

export function SiteFooter({ note }: { note: string }) {
  return (
    <footer className="public-footer">
      <div>
        <AetherMark compact />
        <p>An open research project by Noah Hicks.</p>
      </div>
      <div className="footer-links">
        <a href="/">Home</a>
        <a href="/evidence">Evidence</a>
        <a href={paperUrl}>Working paper</a>
        <a href={githubUrl}>GitHub</a>
      </div>
      <p className="footer-note">{note}</p>
    </footer>
  );
}

const STATUS_LABEL: Record<GateStatus, string> = {
  pass: "Pass",
  partial: "Partial",
  fail: "Fail",
};

/**
 * The submission ledger, failures included. Publishing the two failing gates is
 * the point: a reader can check the claim against the generated table rather
 * than taking a summary on trust.
 */
export function GateLedger() {
  return (
    <div className="gate-ledger">
      <div className="gate-tally" aria-label="Gate tally">
        <div className="tally-pass"><strong>{gateTally.pass}</strong><span>Pass</span></div>
        <div className="tally-partial"><strong>{gateTally.partial}</strong><span>Partial</span></div>
        <div className="tally-fail"><strong>{gateTally.fail}</strong><span>Fail</span></div>
      </div>
      <ol className="gate-list">
        {submissionGates.map((gate) => (
          <li className={`gate gate-${gate.status}`} key={gate.id}>
            <span className="gate-id">{gate.id}</span>
            <h3>{gate.gate}</h3>
            <span className={`gate-status status-${gate.status}`}>{STATUS_LABEL[gate.status]}</span>
            <p className="gate-evidence">{gate.evidence}</p>
            <p className="gate-next"><span>Next</span> {gate.next}</p>
          </li>
        ))}
      </ol>
      <a className="text-link" href={tableUrl("aether_submission_readiness_gates.csv")}>
        Inspect the generated ledger <Arrow />
      </a>
    </div>
  );
}
