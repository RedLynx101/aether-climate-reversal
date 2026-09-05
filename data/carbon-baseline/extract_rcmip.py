"""Reproduce the small immutable RCMIP SSP2-4.5 baseline extract.

Downloads are kept in memory; only the selected numerical series and provenance
manifest are written. Offline model execution uses the committed extract.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
from pathlib import Path
from urllib.request import urlopen

DEST = Path(__file__).resolve().parent
FILES = {
    "concentrations": ("Atmospheric Concentrations|CO2", "ppm", "0d82c3c3cdd4dd632b2bb9449a5c315f"),
    "emissions": ("Emissions|CO2", "Mt CO2/yr", "4044106f55ca65b094670e7577eaf9b3"),
}


def main() -> None:
    selected = {}
    manifest = {"dataset_doi": "10.5281/zenodo.4589756", "version": "v5.1.0", "retrieved_date": "2026-09-05", "files": {}}
    for family, (variable, unit, expected_md5) in FILES.items():
        url = f"https://zenodo.org/records/4589756/files/rcmip-{family}-annual-means-v5-1-0.csv"
        with urlopen(url, timeout=60) as response:
            raw = response.read()
        if hashlib.md5(raw).hexdigest() != expected_md5:
            raise ValueError(f"Published source checksum mismatch: {family}")
        matches = [row for row in csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
                   if row["Region"] == "World" and row["Scenario"] == "ssp245" and row["Variable"] == variable]
        if len(matches) != 1 or matches[0]["Unit"] != unit:
            raise ValueError(f"Unexpected RCMIP row selection or units: {family}")
        row = matches[0]
        selected[family] = row
        manifest["files"][family] = {
            "url": url, "md5": expected_md5, "sha256": hashlib.sha256(raw).hexdigest(),
            "byte_count": len(raw), "selected_metadata": {key: value for key, value in row.items() if not key.isdigit()},
        }
    output = DEST / "rcmip_ssp245_co2_1850_2100.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["year", "reference_co2_ppm", "reference_emissions_mtco2_y"])
        for year in range(1850, 2101):
            values = [selected[family][str(year)] for family in FILES]
            # Preserve source blanks. The model explicitly linearly interpolates
            # interior gaps; it does not silently fabricate an annual source value.
            writer.writerow([year, *values])
    manifest["extract_sha256"] = hashlib.sha256(output.read_bytes()).hexdigest()
    manifest["extract_hash_line_endings"] = "LF"
    (DEST / "provenance.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
