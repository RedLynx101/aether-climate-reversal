from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER_PATH = ROOT / "manuscript" / "paper" / "aether_scientific_paper.md"
BIB_PATH = ROOT / "references" / "bibtex" / "sources.bib"
REFERENCES_PATH = ROOT / "manuscript" / "paper" / "aether_references_rendered.md"
COVERAGE_PATH = ROOT / "analysis" / "tables" / "aether_bibliography_coverage.csv"


def clean_value(value: str) -> str:
    value = value.strip().strip(",")
    if (value.startswith("{") and value.endswith("}")) or (value.startswith('"') and value.endswith('"')):
        value = value[1:-1]
    previous = None
    while previous != value:
        previous = value
        value = re.sub(r"\{([^{}]*)\}", r"\1", value)
    value = value.replace("\\&", "&").replace("\\%", "%")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def find_matching_brace(text: str, start: int) -> int:
    depth = 0
    in_quote = False
    escape = False
    for idx in range(start, len(text)):
        ch = text[idx]
        if ch == "\\" and not escape:
            escape = True
            continue
        if ch == '"' and not escape:
            in_quote = not in_quote
        if not in_quote:
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return idx
        escape = False
    raise ValueError("Unclosed BibTeX entry")


def parse_fields(body: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    idx = 0
    while idx < len(body):
        while idx < len(body) and body[idx] in " \r\n\t,":
            idx += 1
        match = re.match(r"([A-Za-z_][A-Za-z0-9_-]*)\s*=", body[idx:])
        if not match:
            idx += 1
            continue
        name = match.group(1).lower()
        idx += match.end()
        while idx < len(body) and body[idx].isspace():
            idx += 1
        if idx >= len(body):
            break
        if body[idx] == "{":
            end = find_matching_brace(body, idx)
            raw = body[idx : end + 1]
            idx = end + 1
        elif body[idx] == '"':
            idx += 1
            start = idx
            while idx < len(body) and body[idx] != '"':
                idx += 1
            raw = '"' + body[start:idx] + '"'
            idx += 1
        else:
            start = idx
            while idx < len(body) and body[idx] != ",":
                idx += 1
            raw = body[start:idx]
        fields[name] = clean_value(raw)
    return fields


def parse_bibtex(text: str) -> dict[str, dict[str, object]]:
    entries: dict[str, dict[str, object]] = {}
    idx = 0
    entry_pattern = re.compile(r"@([A-Za-z]+)\s*\{\s*([^,\s]+)\s*,", re.MULTILINE)
    while True:
        match = entry_pattern.search(text, idx)
        if not match:
            break
        entry_type = match.group(1).lower()
        key = match.group(2).strip()
        brace = text.find("{", match.start())
        end = find_matching_brace(text, brace)
        comma = text.find(",", brace)
        body = text[comma + 1 : end]
        fields = parse_fields(body)
        fields["entry_type"] = entry_type
        fields["key"] = key
        entries[key] = fields
        idx = end + 1
    return entries


def citation_keys(paper: str) -> list[str]:
    keys = set()
    for match in re.finditer(r"@([A-Za-z0-9_:-]+)", paper):
        keys.add(match.group(1))
    return sorted(keys, key=str.lower)


def author_text(raw: str) -> str:
    if not raw:
        return "Unknown author"
    raw = raw.replace(" and others", " et al.")
    parts = [part.strip() for part in raw.split(" and ") if part.strip()]
    if not parts:
        return raw
    if len(parts) == 1:
        return parts[0]
    if len(parts) > 3:
        return parts[0] + " et al."
    return ", ".join(parts[:-1]) + ", and " + parts[-1]


def format_entry(key: str, entry: dict[str, object] | None) -> str:
    if entry is None:
        return f"- **[{key}]** Missing BibTeX entry."

    fields = {str(k): str(v) for k, v in entry.items()}
    authors = author_text(fields.get("author", ""))
    year = fields.get("year", "n.d.")
    title = fields.get("title", "Untitled")
    bits = [f"- **[{key}]** {authors}. ({year}). *{title}*."]

    journal = fields.get("journal", "")
    booktitle = fields.get("booktitle", "")
    publisher = fields.get("publisher", "")
    doi = fields.get("doi", "")
    url = fields.get("url", "")
    note = fields.get("note", "")

    if journal:
        bits.append(f"{journal}.")
    elif booktitle:
        bits.append(f"In *{booktitle}*.")
    if publisher and publisher not in " ".join(bits):
        bits.append(f"{publisher}.")
    if doi:
        bits.append(f"doi:{doi}.")
    if url:
        bits.append(f"{url}.")
    if note:
        bits.append(f"Note: {note}.")
    return " ".join(bits)


def main() -> None:
    paper = PAPER_PATH.read_text(encoding="utf-8")
    bib = BIB_PATH.read_text(encoding="utf-8")
    keys = citation_keys(paper)
    entries = parse_bibtex(bib)

    rows = []
    rendered_entries = []
    for key in keys:
        entry = entries.get(key)
        status = "ok" if entry else "missing_bib"
        rows.append(
            {
                "key": key,
                "cited_in_paper": "true",
                "in_bibtex": "true" if entry else "false",
                "coverage_status": status,
                "entry_type": str(entry.get("entry_type", "")) if entry else "",
                "year": str(entry.get("year", "")) if entry else "",
                "title": str(entry.get("title", "")) if entry else "",
                "url": str(entry.get("url", "")) if entry else "",
                "doi": str(entry.get("doi", "")) if entry else "",
            }
        )
        rendered_entries.append(format_entry(key, entry))

    missing = [row["key"] for row in rows if row["coverage_status"] != "ok"]
    header = [
        "# AETHER Rendered References",
        "",
        "Generated from `references/bibtex/sources.bib` and citation keys used in `manuscript/paper/aether_scientific_paper.md`.",
        "",
        f"- Cited source keys: {len(keys)}",
        f"- BibTeX entries found: {len(keys) - len(missing)}",
        f"- Missing BibTeX entries: {len(missing)}",
        "",
        "Source keys are retained in brackets for traceability to the source register. The next publication step is a target-journal CSL/Pandoc render, not hand-editing this generated list.",
        "",
    ]
    rendered = "\n".join(header + rendered_entries) + "\n"
    REFERENCES_PATH.write_text(rendered, encoding="utf-8")

    COVERAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with COVERAGE_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "key",
                "cited_in_paper",
                "in_bibtex",
                "coverage_status",
                "entry_type",
                "year",
                "title",
                "url",
                "doi",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    paper = re.sub(r"Status: Working paper v0\.\d+", "Status: Working paper v0.45", paper)
    paper_rendered = rendered.replace("# AETHER Rendered References", "### AETHER Rendered References", 1)
    references_section = "\n\n## References\n\n" + paper_rendered
    if re.search(r"\n## References\s", paper):
        paper = re.sub(r"\n## References\s.*\Z", references_section, paper, flags=re.DOTALL)
    else:
        paper = paper.rstrip() + references_section
    PAPER_PATH.write_text(paper.rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

