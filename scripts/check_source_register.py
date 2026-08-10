"""Lightweight checks for references/source-register.md.

This script is intentionally small. It catches missing table fields before the
source register turns into an unusable notes dump.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_REGISTER = ROOT / "references" / "source-register.md"
REQUIRED_HEADERS = ["Key", "Source", "Type", "Status", "Use"]


def parse_markdown_table(path: Path) -> tuple[list[str], list[list[str]]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    table_lines = [line for line in lines if line.startswith("|") and line.endswith("|")]
    if len(table_lines) < 2:
        raise ValueError(f"No markdown table found in {path}")

    headers = [cell.strip() for cell in table_lines[0].strip("|").split("|")]
    rows: list[list[str]] = []
    for line in table_lines[2:]:
        rows.append([cell.strip() for cell in line.strip("|").split("|")])
    return headers, rows


def main() -> int:
    headers, rows = parse_markdown_table(SOURCE_REGISTER)
    missing_headers = [header for header in REQUIRED_HEADERS if header not in headers]
    if missing_headers:
        print(f"Missing required headers: {', '.join(missing_headers)}")
        return 1

    key_index = headers.index("Key")
    failures: list[str] = []
    seen_keys: set[str] = set()

    for row_number, row in enumerate(rows, start=1):
        if len(row) != len(headers):
            failures.append(f"Row {row_number} has {len(row)} fields, expected {len(headers)}")
            continue

        key = row[key_index]
        if not key:
            failures.append(f"Row {row_number} is missing a source key")
        elif key in seen_keys:
            failures.append(f"Duplicate source key: {key}")
        seen_keys.add(key)

        for header, value in zip(headers, row):
            if not value:
                failures.append(f"Source {key or row_number} is missing {header}")

    if failures:
        print("Source register check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Source register check passed: {len(rows)} sources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

