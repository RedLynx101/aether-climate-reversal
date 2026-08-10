"""Fail when the tracked tree contains known private or legacy release material."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

BLOCKED_PATHS = {
    "docs/project-prompts/2026-08-09-public-research-release.md",
    "website/DESIGN_DIRECTIONS.md",
    "website/build/sites-vite-plugin.ts",
    "website/tests/rendered-html.test.mjs",
    "website/vite.config.ts",
    "website/worker/index.ts",
    "manuscript/review/aether_internal_peer_review_v0.44.md",
    "manuscript/submission/AETHER_Atmospheric_Engineering_Through_High_Energy_Removal_v0.42.docx",
    "manuscript/submission/AETHER_Atmospheric_Engineering_Through_High_Energy_Removal_v0.43.docx",
    "manuscript/submission/AETHER_Atmospheric_Engineering_Through_High_Energy_Removal_v0.44.docx",
}
BLOCKED_PREFIXES = {
    "reference-material/abundance-carbon-removal-memo/working-pack/",
}
TEXT_SUFFIXES = {
    ".cff",
    ".css",
    ".html",
    ".js",
    ".json",
    ".md",
    ".mjs",
    ".ps1",
    ".py",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}
BLOCKED_PATTERNS = {
    "personal Windows profile path": re.compile(r"C:\\Users\\", re.IGNORECASE),
    "personal Codex workspace path": re.compile(r"Documents\\Codex", re.IGNORECASE),
    "personal OneDrive path": re.compile(r"\bOneDrive\b", re.IGNORECASE),
    "private personal-wiki reference": re.compile(r"\bRedWiki\b", re.IGNORECASE),
    "private historical email": re.compile(r"NoahHicks101@gmail\.com", re.IGNORECASE),
    "private course identifier": re.compile(r"\b95-724\b"),
    "private submission workflow": re.compile(r"Canvas/Turnitin", re.IGNORECASE),
    "legacy Vinext dependency": re.compile(r"\bvinext\b", re.IGNORECASE),
}


def tracked_paths() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [item.decode("utf-8") for item in result.stdout.split(b"\0") if item]


def main() -> None:
    failures: list[str] = []
    paths = tracked_paths()
    path_set = set(paths)

    for path in sorted(BLOCKED_PATHS & path_set):
        failures.append(f"blocked legacy/private path is tracked: {path}")
    for prefix in sorted(BLOCKED_PREFIXES):
        for path in paths:
            if path.startswith(prefix):
                failures.append(f"blocked private directory is tracked: {path}")

    for relative in paths:
        if relative == "scripts/check_public_release.py":
            continue
        path = ROOT / relative
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            failures.append(f"tracked text file is not valid UTF-8: {relative}")
            continue
        for label, pattern in BLOCKED_PATTERNS.items():
            if pattern.search(text):
                failures.append(f"{label} found in {relative}")

    required = {
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/workflows/ci.yml",
        "CITATION.cff",
        "LICENSING.md",
        "LICENSE",
        "LICENSE-CONTENT.md",
        "SECURITY.md",
    }
    for path in sorted(required - path_set):
        failures.append(f"required public-release file is missing: {path}")

    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    for required_text in ("version: 0.45", "Apache-2.0", "CC-BY-4.0"):
        if required_text not in citation:
            failures.append(f"CITATION.cff is missing: {required_text}")

    paper = (ROOT / "manuscript/paper/aether_scientific_paper.md").read_text(encoding="utf-8")
    headings = [line.strip() for line in paper.splitlines() if re.match(r"^#{1,6}\s+", line)]
    duplicate_headings = sorted({heading for heading in headings if headings.count(heading) > 1})
    for heading in duplicate_headings:
        failures.append(f"duplicate paper heading found: {heading}")

    if failures:
        raise SystemExit("Public-release check failed:\n- " + "\n- ".join(sorted(set(failures))))
    print(f"Public-release check passed for {len(paths)} tracked files.")


if __name__ == "__main__":
    main()
