# AETHER public website

This directory contains the production website for [aetherclimate.com](https://aetherclimate.com). Its selected visual system pairs a living atmosphere with a civic thesis: atmospheric carbon can be managed as inspectable public infrastructure with an operating range, net-use budget, evidence, prices, and accountable public authority.

`aetherclimate.org` permanently redirects to the canonical `.com` host while preserving the path and query. `www` hosts redirect to the apex `.com` domain.

## Routes

- `/` - canonical project introduction
- `/evidence` - paired regional case, carbon/resource/funding ledgers, three current figures, and explicit research limitations
- `/model` - permanent compatibility redirect to `/evidence`
- `/living-atmosphere` - permanent compatibility redirect to the canonical introduction

Discarded concept routes and assets are not shipped. The working paper and repository remain authoritative for technical claims. The website is possibility-led, but it does not claim that AETHER is feasible, funded, deployed, peer reviewed, or already authorized by law.

## Development

Requires Node.js 24.

```text
npm ci
npm run dev
npm run lint
npm test
npm audit --omit=dev --audit-level=high
```

Native Next.js is the only supported build and deployment target. `npm test` builds the production application, starts it locally, verifies the public routes and paper/chart assets, confirms discarded routes return 404, and checks the `.org` and `www` redirects.

## Brand and evidence

- `public/favicon.svg` and `public/brand/aether-mark.svg` contain the AETHER orbit mark.
- `public/art/` contains original conceptual project art.
- `public/charts/` contains public copies of selected generated research figures.
- `public/papers/` contains the v0.46 working paper and technical supplement. Earlier public PDF URLs redirect to the corrected working paper.

`app/evidence.generated.json` and the three `regional-*.png` figures come from `../scripts/export_public_evidence.py`. Do not hand-edit their numbers. Regenerate the regional model, run that exporter, then its `--check` mode. PDF sources, figures and artifacts are checked by `../scripts/build_current_publication.py --check`. Historical charts retained in Git are not current public evidence.

Concept art is not evidence of deployed infrastructure. The future video/channel plan remains at `../docs/AETHER_VIDEO_AND_CHANNEL_PLAN.md`; no nonexistent video appears on the site.

## Attribution

AETHER was originated and is principally authored by Noah Hicks. Repository software is licensed under Apache-2.0 and original research content under CC BY 4.0, subject to file-level and third-party notices. See the repository-root licensing and attribution files.
