# Carbon reference data

**The current hybrid model is quarantined.** These verified source data remain
usable research infrastructure; the resulting off-reference absolute CO2 and
temperature trajectories are rejected diagnostics, not accepted predictions.

`rcmip_ssp245_co2_1850_2100.csv` is a small, unrounded extract of the
**World / ssp245 / MESSAGE-GLOBIOM** CO2 concentration and total CO2 emissions
rows in [RCMIP v5.1.0](https://doi.org/10.5281/zenodo.4589756), retrieved on
September 5, 2026. This immutable 2021 scenario dataset is not a current CO2
observation or a forecast endorsement.

`provenance.json` records source URLs, source byte counts, exact selected row
metadata, Zenodo's published MD5 checksums, independently computed SHA256
checksums, and the extract SHA256 (canonical LF line endings, so Windows Git
checkout conversion is harmless). The model verifies the extract checksum on
load. Source concentration units are ppm; source emissions units are Mt CO2/yr
and are divided by 1000 for GtCO2/yr.

Only the local extract checksum uses canonical text line endings. MD5 and
SHA256 checksums for the two full downloaded source files are calculated from
their original response bytes, without any newline normalization. Regression
tests load both LF and CRLF extract fixtures and reject a changed numeric value.
Generated model CSV regressions parse rows and compare values, not newline bytes.

Some source years are blank. The extract preserves those blanks. The model
linearly interpolates only between bracketing published values and refuses to
extrapolate. Interpolated annual values must not be described as annual source
observations.

To reproduce the extract (requires access to two public Zenodo files, about
69 MB combined):

```powershell
python data/carbon-baseline/extract_rcmip.py
```

Offline model runs do not download data. The extractor is separate from the
normal reproduction pipeline, so the data are not silently refreshed.

See [the source/method note](../../research/source-notes/carbon-baseline-rcmip-2026-09-05.md)
for interpretation and the scientific acceptance boundary.
