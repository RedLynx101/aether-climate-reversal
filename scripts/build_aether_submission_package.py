from __future__ import annotations

import csv
import re
import struct
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER_PATH = ROOT / "manuscript" / "paper" / "aether_scientific_paper.md"
SUBMISSION_CHECKLIST_PATH = ROOT / "manuscript" / "review" / "aether_submission_checklist.md"
SUBMISSION_DIR = ROOT / "manuscript" / "submission"
SUBMISSION_MANUSCRIPT_PATH = SUBMISSION_DIR / "aether_submission_manuscript.md"
SUBMISSION_MANIFEST_PATH = SUBMISSION_DIR / "aether_submission_manifest.md"
SUBMISSION_README_PATH = SUBMISSION_DIR / "README.md"
TABLE_DIR = ROOT / "analysis" / "tables"
FIGURE_DIR = ROOT / "analysis" / "figures"
NOTE_PATH = ROOT / "research" / "parameters" / "submission-package-and-manuscript-readiness-notes.md"
FIGURE_INVENTORY_PATH = TABLE_DIR / "aether_figure_inventory.csv"
READINESS_GATES_PATH = TABLE_DIR / "aether_submission_readiness_gates.csv"
STYLE_AUDIT_PATH = TABLE_DIR / "aether_manuscript_style_audit.csv"
VERSION = "v0.45"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {path}")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print(f"Wrote {path}")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def add_unique_line_after(text: str, anchor: str, line: str) -> str:
    if line in text:
        return text
    if anchor in text:
        return text.replace(anchor, anchor + "\n" + line, 1)
    return text.rstrip() + "\n" + line + "\n"


def replace_section_before_heading(text: str, heading: str, next_heading: str, replacement: str) -> str:
    pattern = re.compile(r"(?ms)^" + re.escape(heading) + r".*?(?=^" + re.escape(next_heading) + r")")
    replacement = replacement.rstrip() + "\n\n"
    if pattern.search(text):
        return pattern.sub(replacement, text, count=1)
    return text.replace(next_heading, replacement + next_heading, 1)


def markdown_table(rows: list[dict[str, object]], columns: list[str], headers: list[str]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        cells = [str(row.get(column, "")).replace("|", "/") for column in columns]
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def png_dimensions(path: Path) -> tuple[int | str, int | str]:
    try:
        data = path.read_bytes()
        if data[:8] != b"\x89PNG\r\n\x1a\n":
            return "", ""
        width, height = struct.unpack(">II", data[16:24])
        return width, height
    except OSError:
        return "", ""


def citation_keys(text: str) -> set[str]:
    return set(re.findall(r"@([A-Za-z0-9_:-]+)", text))


def count_words(text: str) -> int:
    body = re.sub(r"```.*?```", " ", text, flags=re.S)
    body = re.sub(r"`[^`]*`", " ", body)
    return len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", body))


def pass_fail(ok: bool) -> str:
    return "pass" if ok else "fail"


def source_register_add(content: str, key: str, row: str) -> str:
    if f"| {key} |" in content:
        return content
    marker = "## Source Discipline"
    if marker in content:
        return content.replace(marker, row + "\n" + marker, 1)
    return content.rstrip() + "\n" + row + "\n"


paper = read_text(PAPER_PATH)
paper = re.sub(r"Status: Working paper v0\.\d+", f"Status: Working paper {VERSION}", paper)

limitations = """## 16. Limitations

AETHER is a conditional feasibility analysis, not a forecast. It asks what would have to be true for 100 GtCO2/year gross removal to become a serious climate-reversal infrastructure program under aggressive AI, robotics, and energy-abundance assumptions.

The carbon-cycle and climate-response treatment is now better than atmosphere-only ppm conversion, but still too simple for final climate claims. The Joos impulse-response model, AR6-anchored forcing proxy, dynamic emulator, FAIR-readiness deck, forcing-driven FAIR execution, and species-emissions handoff are useful for scenario discipline. They do not replace a full species-emissions FAIR or Earth-system treatment of state-dependent land/ocean response, non-CO2 forcing, aerosols, ocean heat uptake, zero-emissions commitment, ocean chemistry, lifecycle species traces, or regional climate effects.

The cost and robot models are deliberately explicit, but still coarse. They show which orders of magnitude matter; they do not yet replace component-level TEA, process simulation, audited factory learning curves, field-productivity measurements, duty-cycle data, service-cost data, or pathway-specific bills of materials.

Storage, MRV, and lifecycle accounting remain major gates. The repo now separates gross captured tonnes, durable tonnes, and creditable tonnes, but method-specific leakage, reversal, monitoring duration, invalidation, liability, and replacement-media loops still need to be sourced and modeled at the pathway and region level.

Robotics assumptions are especially uncertain. Industrial robot deployment statistics are real, but humanoid and general-purpose robot production claims remain noisy. The paper should not rely on social-media claims except as leads, and it should treat company-primary production claims as signals until independent audits or field data exist.

The public-carbon-utility model is an AETHER design hypothesis, not settled law or a demonstrated institution. Treating atmospheric capacity as citizen-held or trust-administered may align incentives, but a weak budget or price could authorize more net loading than the removal system can manage. Legal authority, cross-border coordination, measurement, liability, local pollution controls, revenue allocation, and democratic accountability remain unresolved gates.

Finally, the 100 GtCO2/year target is intentionally extreme. A smaller program may be easier to justify, finance, and govern. The point of the 100 Gt screen is to expose physical and institutional bottlenecks clearly enough that the feasible scale can be argued with evidence instead of slogans.

### 16.1 Planetary Engineering and the Terraforming Boundary

AETHER qualifies as a low form of terraforming in a literal but limited sense: deliberate, planetary-scale alteration of atmospheric composition to maintain a chosen climate state. On Earth, that framing increases the burden of consent, monitoring, reversibility, liability, and international governance. It does not make the planet fully controllable, and it does not imply that carbon removal can reconstruct extinct species, lost ice, displaced communities, or every regional climate state.

Descendant capabilities could have off-world uses. Autonomous construction, atmosphere processing, gas separation, mineralization, closed-loop clean power, and environmental monitoring are plausible components of future habitat engineering on other celestial bodies. The present work does not model Mars, Venus, the Moon, or any other extraterrestrial environment, and it provides no evidence that terrestrial AETHER designs transfer directly. Off-world application remains a speculative research branch outside this paper's feasibility claim.
"""
paper = replace_section_before_heading(paper, "## 16. Limitations", "## 17. Conclusion", limitations)

figure_ref_matches = list(re.finditer(r"!\[([^\]]*)\]\(\.\./\.\./analysis/figures/([^)]+)\)", paper))
figure_refs_ordered: list[tuple[str, str]] = []
seen_refs: set[str] = set()
for match in figure_ref_matches:
    alt_text = match.group(1).strip()
    figure_file = match.group(2).strip()
    if figure_file not in seen_refs:
        seen_refs.add(figure_file)
        figure_refs_ordered.append((alt_text, figure_file))

figure_inventory: list[dict[str, object]] = []
for idx, (alt_text, figure_file) in enumerate(figure_refs_ordered, start=1):
    path = FIGURE_DIR / figure_file
    width, height = png_dimensions(path)
    size_kb = round(path.stat().st_size / 1024, 1) if path.exists() else ""
    figure_inventory.append({
        "figure_id": f"Figure {idx}",
        "paper_order": idx,
        "alt_text": alt_text,
        "file": f"analysis/figures/{figure_file}",
        "referenced_in_paper": "true",
        "file_exists": str(path.exists()).lower(),
        "width_px": width,
        "height_px": height,
        "size_kb": size_kb,
        "submission_action": "add journal caption and verify final layout",
    })

referenced_files = {file_name for _, file_name in figure_refs_ordered}
for path in sorted(FIGURE_DIR.glob("*.png"), key=lambda p: p.name.lower()):
    if path.name in referenced_files:
        continue
    width, height = png_dimensions(path)
    figure_inventory.append({
        "figure_id": "",
        "paper_order": "",
        "alt_text": "",
        "file": f"analysis/figures/{path.name}",
        "referenced_in_paper": "false",
        "file_exists": "true",
        "width_px": width,
        "height_px": height,
        "size_kb": round(path.stat().st_size / 1024, 1),
        "submission_action": "supporting figure or candidate appendix figure",
    })

missing_figures = [row for row in figure_inventory if row["referenced_in_paper"] == "true" and row["file_exists"] != "true"]

bibliography_rows = read_csv(TABLE_DIR / "aether_bibliography_coverage.csv")
missing_bib = [row for row in bibliography_rows if row.get("coverage_status") != "ok"]
unit_rows = read_csv(TABLE_DIR / "aether_dimensioned_unit_checks.csv")
unit_failures = [row for row in unit_rows if row.get("pass") not in {"True", "true", "1", "yes"}]
claim_rows = read_csv(TABLE_DIR / "aether_manuscript_claim_evidence_matrix.csv")
species_gate_rows = read_csv(TABLE_DIR / "aether_species_emissions_publication_gates.csv")
adversarial_rows = read_csv(TABLE_DIR / "aether_falsification_tests.csv")
clean_power_summary = read_csv(TABLE_DIR / "aether_clean_power_deliverability_summary.csv")

paper_keys = citation_keys(paper)
paper_for_style = re.sub(
    r"(?ms)^## Appendix B: Submission Package and Review Gates.*?(?=^## (?:Appendix [AC]:|References))",
    "",
    paper,
)
todo_count = len(re.findall(r"\b(?:TODO|TBD|FIXME)\b", paper_for_style, flags=re.I))
old_repeated_phrase = "but they now feed a FAIR-readiness handoff deck"
old_phrase_count = paper_for_style.count(old_repeated_phrase)
word_count = count_words(paper)

readiness_gates = [
    {
        "gate_id": "S01_citation_coverage",
        "gate": "All manuscript citation keys resolve to BibTeX entries",
        "status": pass_fail(len(missing_bib) == 0 and len(bibliography_rows) >= len(paper_keys)),
        "current_evidence": f"{len(paper_keys)} cited keys; {len(missing_bib)} missing BibTeX entries",
        "next_upgrade": "Render through target-journal CSL, Pandoc, or LaTeX style.",
    },
    {
        "gate_id": "S02_figure_resolution",
        "gate": "All paper figure references resolve to repo PNGs",
        "status": pass_fail(len(missing_figures) == 0 and len(figure_refs_ordered) >= 35),
        "current_evidence": f"{len(figure_refs_ordered)} paper figure references; {len(missing_figures)} missing files",
        "next_upgrade": "Add final journal captions, numbering, and page-layout checks.",
    },
    {
        "gate_id": "S03_equation_reproducibility",
        "gate": "Headline equations and unit checks are inspectable",
        "status": pass_fail(len(unit_rows) >= 10 and not unit_failures),
        "current_evidence": f"{len(unit_rows)} unit checks; {len(unit_failures)} failures",
        "next_upgrade": "Connect every major claim row to equation ids and generated tables.",
    },
    {
        "gate_id": "S04_claim_evidence",
        "gate": "Main manuscript claims are mapped to evidence classes",
        "status": pass_fail(len(claim_rows) >= 12),
        "current_evidence": f"{len(claim_rows)} claim-evidence rows",
        "next_upgrade": "Expand with reviewer comments and claim-specific source upgrades.",
    },
    {
        "gate_id": "S05_climate_model_publication_grade",
        "gate": "Temperature claims use species-emissions FAIR or Earth-system modeling",
        "status": "fail",
        "current_evidence": "Forcing-driven FAIR diagnostic exists, but species-emissions handoff still blocks publication-grade climate claims.",
        "next_upgrade": "Build species-level CH4, N2O, aerosol, land-use, lifecycle, spin-up, ZEC, and uncertainty inputs.",
    },
    {
        "gate_id": "S06_species_emissions_inputs",
        "gate": "Species-emissions publication gates pass",
        "status": "fail",
        "current_evidence": f"{sum(1 for row in species_gate_rows if row.get('gate_status') == 'fail')} failing species-emissions gates out of {len(species_gate_rows)}",
        "next_upgrade": "Use aether_species_emissions_requirement_matrix.csv as the climate-modeling worklist.",
    },
    {
        "gate_id": "S07_clean_power_delivery",
        "gate": "Clean power is delivered, additional, hourly matched, and regionally feasible",
        "status": "partial",
        "current_evidence": f"{len(clean_power_summary)} clean-power deliverability summary rows plus regional dispatch screen",
        "next_upgrade": "Replace representative-day archetypes with 8760-hour regional dispatch and interconnection modeling.",
    },
    {
        "gate_id": "S08_storage_mrv_lifecycle",
        "gate": "Storage, MRV, and lifecycle penalties are method-specific",
        "status": "partial",
        "current_evidence": "Route-level storage, lifecycle, MRV, and credit-integrity screens exist.",
        "next_upgrade": "Replace route-level screens with basin-level storage, method-specific LCA, and registry/invalidation rules.",
    },
    {
        "gate_id": "S09_robotics_field_productivity",
        "gate": "Robotics premise is supported by task-level field productivity",
        "status": "partial",
        "current_evidence": "Production verification and field-productivity distribution screens exist, but multipliers remain provisional.",
        "next_upgrade": "Collect source-backed duty cycle, autonomy, task-fit, failure-rate, supervision, and service-cost data.",
    },
    {
        "gate_id": "S10_adversarial_review",
        "gate": "High-risk specialist objections are turned into decisive tests",
        "status": "partial",
        "current_evidence": f"{len(adversarial_rows)} falsification-test rows in the adversarial review packet",
        "next_upgrade": "Run expert review and narrow claims where P0 tests fail.",
    },
    {
        "gate_id": "S11_style_and_duplicate_scan",
        "gate": "Generated manuscript avoids obvious duplicated boilerplate",
        "status": pass_fail(old_phrase_count <= 1 and todo_count == 0),
        "current_evidence": f"old repeated FAIR phrase count: {old_phrase_count}; editorial placeholder hits: {todo_count}",
        "next_upgrade": "Run a human editorial pass after target-journal format is chosen.",
    },
    {
        "gate_id": "S12_submission_format",
        "gate": "Submission manuscript and package manifest exist",
        "status": "partial",
        "current_evidence": "Generated Markdown submission package exists; final journal format is not selected.",
        "next_upgrade": "Choose target venue and render with required figure, table, citation, and supplement rules.",
    },
]

style_audit = [
    {
        "check_id": "style_001_version",
        "check": f"Paper status updated to {VERSION}",
        "status": pass_fail(f"Status: Working paper {VERSION}" in paper),
        "detail": f"Target version {VERSION}",
    },
    {
        "check_id": "style_002_repeated_fair_phrase",
        "check": "Repeated FAIR-readiness caveat removed",
        "status": pass_fail(old_phrase_count <= 1),
        "detail": f"Phrase count after cleanup: {old_phrase_count}",
    },
    {
        "check_id": "style_003_todo_markers",
        "check": "No TODO/TBD/FIXME markers remain in the main paper",
        "status": pass_fail(todo_count == 0),
        "detail": f"Markers found: {todo_count}",
    },
    {
        "check_id": "style_004_references",
        "check": "Rendered references section present",
        "status": pass_fail("## References" in paper and "AETHER Rendered References" in paper),
        "detail": f"Citation keys in paper: {len(paper_keys)}",
    },
    {
        "check_id": "style_005_figures",
        "check": "Paper figure links resolve",
        "status": pass_fail(len(missing_figures) == 0),
        "detail": f"Referenced figures: {len(figure_refs_ordered)}; missing: {len(missing_figures)}",
    },
    {
        "check_id": "style_006_word_count",
        "check": "Paper length tracked for target-journal editing",
        "status": "tracked",
        "detail": f"Approximate word count: {word_count}",
    },
]

write_csv(FIGURE_INVENTORY_PATH, figure_inventory, [
    "figure_id",
    "paper_order",
    "alt_text",
    "file",
    "referenced_in_paper",
    "file_exists",
    "width_px",
    "height_px",
    "size_kb",
    "submission_action",
])
write_csv(READINESS_GATES_PATH, readiness_gates, [
    "gate_id",
    "gate",
    "status",
    "current_evidence",
    "next_upgrade",
])
write_csv(STYLE_AUDIT_PATH, style_audit, [
    "check_id",
    "check",
    "status",
    "detail",
])

status_counts = Counter(row["status"] for row in readiness_gates)
figure_inventory_count = len(figure_inventory)
referenced_figure_count = len(figure_refs_ordered)
style_fail_count = sum(1 for row in style_audit if row["status"] == "fail")
gate_table = markdown_table(readiness_gates, ["gate_id", "status", "current_evidence"], ["Gate", "Status", "Current evidence"])

appendix = f"""## Appendix B: Submission Package and Review Gates

The v0.45 repo includes a submission package so the paper can be reviewed as a managed research artifact rather than a loose Markdown draft. This does not make AETHER publication-ready. It makes the remaining barriers visible and reproducible.

Generated package artifacts:

- `manuscript/submission/aether_submission_manuscript.md`
- `manuscript/submission/aether_submission_manifest.md`
- `manuscript/submission/README.md`
- `analysis/tables/aether_figure_inventory.csv`
- `analysis/tables/aether_submission_readiness_gates.csv`
- `analysis/tables/aether_manuscript_style_audit.csv`
- `manuscript/review/aether_submission_checklist.md`

The current package inventories {referenced_figure_count} paper figures and {figure_inventory_count} total PNG figures. The submission-gate table marks {status_counts.get('pass', 0)} gates as pass, {status_counts.get('partial', 0)} as partial, and {status_counts.get('fail', 0)} as fail. The failing gates are not cosmetic: climate response and species-emissions inputs still block publication-grade temperature claims.

{gate_table}
"""
paper = re.sub(
    r"(?ms)^## Appendix B: Submission Package and Review Gates.*?(?=^## (?:Appendix [AC]:|References))",
    "",
    paper,
)
appendix_anchor = "## Appendix C: Independent Calculation Audit" if "## Appendix C: Independent Calculation Audit" in paper else "## References"
paper = paper.replace(appendix_anchor, appendix.rstrip() + "\n\n" + appendix_anchor, 1)
write_text(PAPER_PATH, paper)

submission_header = """<!--
Generated by scripts/build_aether_submission_package.py.
Edit the source paper or model scripts, then regenerate this package.
-->
"""
write_text(SUBMISSION_MANUSCRIPT_PATH, submission_header + "\n" + paper)

manifest = f"""# AETHER Submission Manifest

Last updated: 2026-08-10

This manifest is generated from the current AETHER repo state. It is meant for academic review preparation, not for journal upload without a final venue-specific formatting pass.

## Package Counts

- Working-paper version: {VERSION}
- Approximate paper word count: {word_count}
- Paper citation keys: {len(paper_keys)}
- Bibliography coverage rows: {len(bibliography_rows)}
- Missing BibTeX entries: {len(missing_bib)}
- Paper figure references: {referenced_figure_count}
- Total PNG figures in repo: {figure_inventory_count}
- Missing paper figures: {len(missing_figures)}
- Submission gates passing: {status_counts.get('pass', 0)}
- Submission gates partial: {status_counts.get('partial', 0)}
- Submission gates failing: {status_counts.get('fail', 0)}
- Style audit failures: {style_fail_count}

## Generated Artifacts

- `aether_submission_manuscript.md`
- `aether_submission_manifest.md`
- `README.md`
- `../../analysis/tables/aether_figure_inventory.csv`
- `../../analysis/tables/aether_submission_readiness_gates.csv`
- `../../analysis/tables/aether_manuscript_style_audit.csv`
- `../review/aether_submission_checklist.md`

## Current Read

AETHER is now organized enough to show to scientists as a serious working-paper package. It should still be described as a conditional feasibility proposal. The strongest current blockers are climate-model publication quality, species-emissions inputs, field-productivity evidence for robotics, method-specific LCA/MRV/storage, and final journal rendering.
"""
write_text(SUBMISSION_MANIFEST_PATH, manifest)

submission_readme = """# AETHER Submission Package

This folder is generated by `scripts/build_aether_submission_package.py`.

Use `aether_submission_manuscript.md` as the current review copy and `aether_submission_manifest.md` as the package index. Do not hand-edit generated files here; edit the source paper or model scripts, then rerun this repository-local builder.

The package is intentionally conservative. It tracks figures, references, review gates, and remaining blockers. It does not claim the paper is ready for journal submission.
"""
write_text(SUBMISSION_README_PATH, submission_readme)

checklist = f"""# AETHER Submission Checklist

Last updated: 2026-08-10

Use this before sending AETHER to a scientist, advisor, or potential collaborator.

## Current Package

- Review manuscript: `manuscript/submission/aether_submission_manuscript.md`
- Package manifest: `manuscript/submission/aether_submission_manifest.md`
- Figure inventory: `analysis/tables/aether_figure_inventory.csv`
- Readiness gates: `analysis/tables/aether_submission_readiness_gates.csv`
- Style audit: `analysis/tables/aether_manuscript_style_audit.csv`

## Gate Summary

{gate_table}

## Minimum Before Formal Submission

1. Pick the target venue or advisor-facing format.
2. Render citations through the required CSL, Pandoc, or LaTeX pipeline.
3. Add final numbered captions for all paper figures.
4. Replace the climate-response proxy with species-emissions FAIR-class or Earth-system modeling.
5. Upgrade field-productivity, storage, lifecycle, MRV, and regional dispatch assumptions from screens to source-backed distributions.
6. Run adversarial review against the P0 falsification tests and narrow the claim where needed.
"""
write_text(SUBMISSION_CHECKLIST_PATH, checklist)

note = f"""# Submission Package and Manuscript Readiness Notes

Last updated: 2026-08-10

The v0.45 layer includes a generated submission package around the existing AETHER working paper. The goal is not to pretend the manuscript is ready for journal submission. The goal is to make a serious review copy and a reproducible readiness ledger.

## Outputs

- `manuscript/submission/aether_submission_manuscript.md`
- `manuscript/submission/aether_submission_manifest.md`
- `manuscript/submission/README.md`
- `manuscript/review/aether_submission_checklist.md`
- `analysis/tables/aether_figure_inventory.csv`
- `analysis/tables/aether_submission_readiness_gates.csv`
- `analysis/tables/aether_manuscript_style_audit.csv`
- `scripts/build_aether_submission_package.py`

## Current Result

The package tracks {referenced_figure_count} paper figures, {len(paper_keys)} citation keys, {len(bibliography_rows)} bibliography coverage rows, and {len(readiness_gates)} submission gates. It also fixes the repeated climate-method caveat in the limitations section.

The central publication blockers remain climate-modeling quality, species-emissions inputs, robotics field-productivity evidence, storage/MRV/LCA specificity, and target-journal formatting.
"""
write_text(NOTE_PATH, note)

print("AETHER submission package sync complete.")

