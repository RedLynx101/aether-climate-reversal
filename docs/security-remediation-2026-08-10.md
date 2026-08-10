# Publication Security Remediation

Date: 2026-08-10

Outcome: remediated and regression-tested.

## Invariants

- Document builders may read only repository-controlled figures and images.
- The proposal PDF fallback may execute only the absolute Windows system PowerShell binary.
- Private workflow material, personal filesystem paths, historical personal email addresses, and legacy deployment artifacts must not enter the public tracked tree.
- Normal repository-relative figures, DOCX generation, PDF export, calculation generation, and the Next.js website must continue to work.

## Fixes

1. `scripts/publication_safety.py` centralizes containment-checked path resolution and trusted Windows PowerShell discovery.
2. `scripts/build_aether_proposal_docx.py` constrains `FIG:` assets to `analysis/figures` and uses the absolute system PowerShell path.
3. `scripts/build_aether_word_manuscript.py` constrains Markdown image inputs to the repository and no longer mutates public status files as a build side effect.
4. `tests/test_publication_safety.py` covers valid repository-relative images, traversal rejection, absolute-path rejection, and trusted PowerShell resolution.
5. `scripts/check_public_release.py` blocks private or legacy paths and strings, missing release files, and duplicate manuscript headings.
6. Private working material, superseded manuscripts and review files, legacy website integration files, and generated legacy state were removed from the public tree.

## Verification

- Python unit tests: 4/4 passed.
- Independent calculation audit: 31/31 passed.
- Source register: 110 sources passed.
- Public-release check: 429 tracked files passed before this report was added.
- Python and PowerShell syntax checks: passed.
- Python lockfile check: passed.
- CFF 1.2.0 schema validation: passed.
- Website clean install, lint, build, and runtime test: passed.
- Production and full npm audits: 0 vulnerabilities.
- Full-tree privacy, legacy-dependency, and credential-pattern scans: no matches.
- Final DOCX packages: no comments or tracked-change elements.
- Visual inspection: every page of the 37-page proposal and 101-page working paper PDFs was reviewed. Duplicate prose, incorrect ordered-list continuation, and an orphan page found during inspection were corrected.

The original security findings no longer reproduce: traversal and absolute paths are rejected, the PowerShell fallback resolves to the trusted system executable, and private workflow material is absent from the tracked release tree. Legitimate repository-relative image embedding and both document builds remain operational.

Remaining uncertainty is limited to the paper's explicitly disclosed scientific research gaps, not the publication-security findings addressed here.
