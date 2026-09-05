import {
  githubUrl,
  paperUrl,
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
      </div>
      <div className="footer-contact">
        <span>Contact / contribute</span>
        <a href="mailto:noahhicks101@gmail.com">noahhicks101@gmail.com</a>
        <a href={githubUrl}>GitHub <Arrow /></a>
      </div>
      <p className="footer-note">{note}</p>
    </footer>
  );
}
