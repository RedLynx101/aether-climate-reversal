# AETHER next steps

The next milestone is not a larger headline. It is a regional result that a specialist can reproduce, break, or improve without accepting the rest of AETHER.

## Immediate research work

1. Resolve the quarantined carbon baseline. Preserve source provenance and paired controls, but do not publish absolute concentration or temperature paths until reservoir initialization and off-reference behavior are defensible.
2. Upgrade the regional benchmark to a named, 8760-hour electricity-and-heat case with weather, load, transmission, firming, outages, maintenance, additionality, and ordinary demand.
3. Replace generic storage terms with a basin-level injection, pressure, permitting, monitoring, financial-responsibility, and long-tail-liability study.
4. Replace automation task-hour assumptions with measured or independently reviewable evidence. Keep ordinary and automation-assisted cases under the same physical constraints.
5. Expand the service ledger to stress current-load settlements, legacy drawdown, capital, reserves, under-delivery, and declining fee revenue.

## Before seeking broad scientific or policy review

- Use the v0.46 paper, supplement, correction notice, and current-publication manifest.
- Provide a finite falsification question to each specialist reviewer.
- Identify one compatible scenario contract across power, heat, process, storage, lifecycle, MRV, capital, and automation.
- Record claim changes resulting from review.

## Routine reproducibility checks

```powershell
uv sync --locked --group publication
uv run python -m unittest discover -s tests
uv run python scripts/reproduce_research.py --check
uv run python scripts/export_public_evidence.py --check
uv run python scripts/build_current_publication.py --check
uv run python scripts/audit_aether_calculations.py
uv run python scripts/check_public_release.py
uv run python scripts/check_source_register.py
```

These are engineering checks, not a scientific-promotion gate.
