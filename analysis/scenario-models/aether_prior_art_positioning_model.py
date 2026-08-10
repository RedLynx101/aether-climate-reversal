"""AETHER prior-art positioning model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PriorArtPosition:
    category: str
    aether_positioning: str
    contribution_type: str
    overclaim_risk: str


def validate_position(row: PriorArtPosition) -> None:
    if not row.overclaim_risk:
        raise ValueError(f"Missing overclaim risk for {row.category}")
