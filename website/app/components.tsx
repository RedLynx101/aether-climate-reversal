import { githubUrl, paperUrl } from "./data";

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
