"""AETHER manuscript evidence model.

This module documents the claim classes used by the working paper. It is a
lightweight companion to the CSV matrix, not a replacement for the physical
models. The intent is to keep reviewer-facing claims from drifting beyond the
evidence class that supports them.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ManuscriptClaim:
    claim: str
    claim_class: str
    evidence_strength: str
    evidence_anchor: str
    paper_usage_rule: str


VALID_EVIDENCE_STRENGTHS = {"A", "B", "C", "D"}


def validate_claim(claim: ManuscriptClaim) -> None:
    if claim.evidence_strength not in VALID_EVIDENCE_STRENGTHS:
        raise ValueError(f"Unknown evidence strength: {claim.evidence_strength}")
    if not claim.evidence_anchor:
        raise ValueError(f"Missing evidence anchor for {claim.claim}")
    if claim.evidence_strength in {"C", "D"} and "forecast" in claim.paper_usage_rule.lower():
        raise ValueError("Weak-evidence claims must not be framed as forecasts.")
