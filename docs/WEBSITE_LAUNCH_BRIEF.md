# AETHER website release brief

Last updated: 2026-08-10

## Canonical deployment

- Public domain: `https://aetherclimate.com`
- Redirect domain: `https://aetherclimate.org` to the canonical `.com`
- Host: Vercel
- Application: native Next.js under `website/`

The `.com` is the canonical address because it is concise and does not imply that AETHER is a formal nonprofit. The `.org` redirect preserves paths and query strings. `www` hosts also redirect to the apex `.com` domain. Canonical metadata, robots, and the sitemap identify only the `.com` host.

## Public role

The site is a concise entrance to the research. It combines the Living Atmosphere visual system with the civic-infrastructure thesis: sense atmospheric conditions, authorize a net budget, build removal capacity, verify durable outcomes, price permitted use, and throttle the system around an operating range.

The site can be more possibility-led than the paper, but it cannot imply that AETHER is feasible, funded, deployed, legally authorized, or peer reviewed. Selected model figures link back to their source tables. The paper remains the authority for assumptions and limitations.

## Evidence posture

The home page states the uncertainty result before it makes the argument, and `/evidence` publishes the full twelve-gate submission ledger including the two failing gates. This is deliberate: the credibility of a conditional working paper rests on the failures being as visible as the thesis. Any redesign that quietly drops the failing gates, the median durable-credit figure, or the source-table links has removed the part that makes the site honest rather than promotional.

Figures on the site are quoted from generated tables under `analysis/tables/`. When a model is rerun and those tables change, `website/app/data.ts` has to be updated in the same commit or the site will misstate the research.

## Routes

- `/` — thesis, uncertainty result, constraint anchors, governance.
- `/evidence` — submission gate ledger, uncertainty distribution, selected figures.
- `/model` and `/living-atmosphere` — permanent redirects retained from the pre-2026-08 structure.

## Release verification

For each production release:

1. confirm the deployed commit;
2. run the local Next.js build and runtime test;
3. verify HTTPS and the `.org` and `www` redirect chains with path/query preservation;
4. inspect `/`, `/evidence`, `/robots.txt`, and `/sitemap.xml`, and confirm `/model` and `/living-atmosphere` still redirect;
5. verify the paper, charts, favicon, canonical metadata, GitHub link, and social image;
6. confirm that discarded design routes return 404;
7. inspect the rendered desktop and mobile layouts before announcing the release.

The planned video, long-form X post, and portfolio-site integration remain later work. The site does not advertise a video that does not exist.
