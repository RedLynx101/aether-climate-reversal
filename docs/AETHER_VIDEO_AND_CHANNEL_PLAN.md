# AETHER Video and YouTube Channel Plan

Status: **planning only**

Last updated: 2026-08-10

Owner and on-camera authority: Noah Hicks

No video, narration, music, YouTube channel, upload, or external account action has been created from this plan. This file is intentionally repository-only; the public website does not present a section for a video that does not exist. The local icon is a design prototype for review.

## Recommended package

- Channel display name: **AETHER**
- Recommended film title: **AETHER: Climate Recovery as Public Infrastructure**
- Format: 3:30-4:15 YouTube explainer, 16:9
- Audience: technically curious general viewers, climate and carbon-removal researchers, AI and robotics practitioners, public-infrastructure and governance audiences
- Narrative promise: show how AETHER turns a large speculative idea into an inspectable operating problem, then name the conditions that would have to be true
- Destination: YouTube embed on `aetherclimate.com`, with direct links to the working paper and GitHub repository
- Tone: optimistic about capability, disciplined about evidence, specific about constraints

## One-sentence concept

What would it take to manage atmospheric carbon as a public utility—setting a budget, metering net use, pricing the load, and building enough removal capacity to hold the balance?

## Story structure

Target narration length: 520-610 words at roughly 145-155 words per minute.

| Time | Beat | Narration purpose | Visual direction |
|---|---|---|---|
| 0:00-0:18 | The shared system | Establish that the atmosphere is already affected by human infrastructure, but is not operated as one accountable system. | Living coastline; clouds; current 428.55 ppm datum enters quietly. No music for the first 5-8 seconds. |
| 0:18-0:43 | The target | State the long-horizon north star: from NOAA's April 2026 global monthly mean of 428.55 ppm, or 0.042855%, toward the approximate 280 ppm preindustrial anchor, or 0.028%. | Precise ppm comparison. Label April 2026. Show 1.53x and the 148.55 ppm gap without implying simple one-for-one removal arithmetic. |
| 0:43-1:03 | The name | Expand Atmospheric Engineering Through High-Energy Removal. Explain that "High-Energy" names the constraint rather than hiding it. | Six clean typographic beats using the AETHER letter system. |
| 1:03-1:40 | The public carbon utility | Explain the proposed operating band, net carbon budget, metering, atmospheric-service charge, removal procurement, and public authority. Useful industry can continue, but net use is measured and paid for. | A ruled public ledger: set the budget, meter net use, price the load, maintain the system. Avoid a circular graphic. |
| 1:40-2:28 | AI and robotics | Show where AI may accelerate discovery, design, scheduling, control, and anomaly detection; show specialized robots doing factory, construction, logistics, maintenance, drilling, and inspection work. | Original facility imagery, paper figures, robot-task diagrams, sensor and verification footage. Do not use generic humanoid-robot spectacle. |
| 2:28-2:58 | What software cannot solve | Name energy, materials, geology, water, land, permitting, storage liability, ecological effects, and public consent. | The system view pauses at red/amber gates. Human authority and independent verification remain visible. |
| 2:58-3:26 | Carbon after restoration | Explain that the system should throttle near an agreed atmospheric range. Carbon may become a durable material or closed-loop resource only when lifecycle accounting prevents net re-emission. | Carbon ledger splits into durable storage, verified material use, and rejected re-emission pathways. |
| 3:26-3:52 | Scenario context | Situational Awareness, AI 2027, and AI 2040 widen the timing and governance envelope but do not prove physical feasibility. | Three linked source covers or typographic citations, clearly labeled as scenarios. |
| 3:52-4:08 | Invitation | Invite viewers to inspect the model, challenge assumptions, and contribute evidence. | Paper, repository, and AETHER mark. End on the living atmosphere, not machinery. |

## Scientific and editorial guardrails

- Say **"roughly 280 ppm"** or **"the approximate preindustrial anchor"**, not a false single-value natural set point.
- Say **"NOAA's April 2026 global monthly mean was 428.55 ppm"**, not "today's level."
- Explain that 428.55 ppm is 0.042855% of dry air; 280 ppm is 0.028%; the April baseline is about 1.53 times the 280 ppm anchor.
- Do not suggest that reducing concentration by 148.55 ppm is a simple atmospheric inventory subtraction. Land and ocean responses, future emissions, lifecycle emissions, durability, and removal effectiveness change the required gross removal.
- Distinguish the north star from the paper's illustrative 350 ppm management floor. The 350 ppm value is a control-model assumption, not the final target.
- Treat CO2 as a managed system load, not a moral category. Explain that useful industrial processes can continue inside a measured net budget when users cover the full atmospheric-service cost.
- State that the public-carbon-utility model is an AETHER proposal, not current law, and that local or high-risk harms remain under separate restrictions.
- Use AI scenarios as boundary conditions, not citations for robot productivity or carbon-removal performance.
- Do not depict autonomous systems as holding final authority. Humans and public institutions set targets, permissions, liability, and stop conditions.
- Label model results, measurements, assumptions, and speculative visuals on screen.

## Voice and ElevenLabs production plan

Recommended voice direction: a calm, technically literate American narrator with warmth and restrained conviction. Avoid trailer intensity, synthetic grandeur, and breathless futurism.

Create three short auditions from the same 90-word passage:

1. **Grounded systems narrator** — recommended; measured pace, low dramatic coloration.
2. **Younger civic technologist** — a little brighter and more conversational.
3. **Documentary researcher** — neutral, deliberate, strongest for scientific credibility.

Production settings and workflow:

- Generate through the ElevenLabs API only after Noah approves the locked script and voice audition.
- Record the model name, voice ID, stability/style settings, seed if available, pronunciation dictionary, generation date, and raw API output in the production manifest.
- Add pronunciations for `AETHER`, `CO2`, `ppm`, `gigatonnes`, `geologic`, `mineralization`, `MRV`, and the names of cited scenario authors if spoken.
- Generate by scene or paragraph, not as one long request, so individual readings can be replaced cleanly.
- Preserve the highest-quality lossless output available; conform final dialogue and mix assets to 48 kHz.
- Keep dialogue, music, and sound design on separate tracks.
- Run a human listen-through for clipped words, odd emphasis, number pronunciation, and unnatural pauses before picture lock.

## Music recommendation

Use music, but sparingly. The film should begin almost dry, introduce a low ambient pulse as the system architecture appears, add subtle organic texture under the atmosphere and restoration sections, and thin back to near-silence when constraints and governance are discussed. Dialogue must remain dominant.

Also export a no-music review version. If the score makes the premise feel more certain or cinematic than the evidence supports, use the no-music version.

Suno-ready concept:

- **Name:** Shared Medium
- **Style of Music:** Instrumental only. Restrained 76 BPM ambient documentary underscore with soft analog pulse, low marimba-like wooden transients, airy granular texture, a faint warm string harmonic bed, and minimal sub bass. Optimistic through clarity rather than triumph. No trailer drums, no choir, no corporate ukulele, no EDM drop, no heroic brass. Leave substantial negative space for narration. Begin nearly silent, grow gently during the infrastructure control-loop sequence, become sparse and slightly tense under engineering constraints, and resolve with an open sustained texture rather than a triumphant cadence.

## Visual system and asset plan

### Channel icon

- Use the exact orbit mark from the website header, not a separate illustration.
- Source: `website/public/brand/aether-mark.svg`.
- Required delivery: 1024x1024 PNG, RGB, with enough internal padding to survive YouTube's circular crop.
- Palette: deep atmosphere green background, chartreuse orbit and center signal.
- No text in the icon; `AETHER` becomes illegible at small sizes.

### Thumbnail

- Future thumbnail background: create or adapt a dedicated asset at production time; do not present the current website artwork as a finished video thumbnail.
- Composition: living coast and atmosphere remain dominant; plausible modular removal infrastructure occupies the lower-right; left side holds the title.
- Recommended exact overlay:
  - eyebrow: `AETHER`
  - headline: `CLIMATE RECOVERY AS PUBLIC INFRASTRUCTURE`
  - small status lozenge: `A PROPOSAL`
- Keep title to the left and away from YouTube's lower-right duration badge.
- Use the same deep green, warm ivory, and chartreuse accent as the site.
- Produce a final 1280x720 RGB PNG under 2 MB after the video title is locked.
- Test at 10% scale and on a phone-sized YouTube feed before approval.

### Footage and graphics

- Original AETHER atmospheric and infrastructure imagery.
- Selected figures from the working paper, redrawn or animated for legibility rather than shown as tiny static charts.
- Linear infrastructure diagrams and a carbon-state ledger.
- Close field details: sensors, valves, fans, drilling, inspection, modular assembly, maintenance, and environmental sampling.
- No unlicensed news clips, fake laboratory footage, fabricated field trials, or visuals that imply a deployed AETHER facility exists.
- Maintain a per-shot provenance ledger with source, license, generation prompt or capture method, edit history, and allowed use.

## Title options

1. **AETHER: Climate Recovery as Public Infrastructure** — recommended; clearest match to the site and civic thesis.
2. **What Would It Take to Operate Climate Recovery?** — strongest curiosity title; less distinctive as a project introduction.
3. **Can AI and Robotics Help Reverse Atmospheric CO2?** — strongest search framing; needs care because it foregrounds technology over governance.

## Recommended YouTube description

> AETHER is an open research program initiated by Noah Hicks. It asks whether AI, robotics, abundant clean power, durable carbon removal, storage, measurement, and public governance could become one inspectable system for atmospheric recovery.
>
> The long-horizon north star is to explore a responsible path from NOAA's April 2026 global monthly mean of 428.55 ppm toward the approximate preindustrial level of 280 ppm. The current working paper does not claim that this path is already feasible. Its 100 GtCO2/year case is a stress test designed to expose the energy, material, storage, verification, ecological, economic, and governance conditions that would have to hold.
>
> Read the working paper: https://aetherclimate.com/papers/AETHER_v0.45_working_paper.pdf
>
> Inspect or contribute to the research: https://github.com/RedLynx101/aether-climate-reversal
> Project site: https://aetherclimate.com
>
> AI scenario context discussed in the film:
>
> https://situational-awareness.ai/
>
> https://ai-2027.com/
>
> https://ai-2040.com/
>
> AETHER is a conditional research proposal, not a deployed system, peer-reviewed conclusion, forecast of AI progress, or statement of current law. Its public-carbon-utility model is open for criticism and institutional research.

## Channel copy

**Channel name:** AETHER

**Short description:**

> Open research on whether autonomous systems, clean power, and durable carbon removal could make atmospheric recovery an inspectable public capability. Initiated by Noah Hicks.

**Long description:**

> AETHER stands for Atmospheric Engineering Through High-Energy Removal. The project tests a difficult proposition: if AI and robotics accelerate science and physical infrastructure, could society build enough clean power, machinery, storage, measurement, and governance to move atmospheric CO2 toward a safer range?
>
> This channel presents the ideas more concisely than the working paper while keeping assumptions, evidence gaps, and failure modes visible. The repository is open for criticism, replication, and better models. AETHER does not claim that extreme removal is likely, that AI progress follows one forecast, or that its proposed public utility already exists in law.

## YouTube chapters

Draft chapter labels, to be retimed after picture lock:

- `00:00` The atmosphere as shared infrastructure
- `00:18` 428.55 ppm to roughly 280
- `00:43` What AETHER stands for
- `01:03` The public carbon utility
- `01:40` AI and robotics become physical
- `02:28` The constraints software cannot remove
- `02:58` Carbon as a resource after restoration
- `03:26` AI scenarios are context, not proof
- `03:52` Inspect the model

## Accessibility and delivery

- 3840x2160 editing master if the source assets support it; 1920x1080 upload minimum.
- Use a constant project frame rate chosen before editing; 24 or 30 fps are both acceptable, with 30 fps preferred for diagram motion and UI clarity.
- 48 kHz audio; preserve separate dialogue, music, and effects stems.
- Human-corrected `.srt` and `.vtt` captions, plus a plain-text transcript.
- Burn in only essential data labels; do not rely on captions for visual meaning.
- Maintain safe margins for mobile playback and YouTube controls.
- Check contrast, number legibility, caption timing, and the thumbnail at small size.

## Approval gates before production

1. Noah approves the title, channel copy, narrative beat sheet, and voice direction.
2. Scientific copy is checked against the working paper and current primary sources.
3. The full script distinguishes evidence, AETHER model outputs, scenario assumptions, and speculation.
4. Voice audition and pronunciation test are approved before full ElevenLabs generation.
5. Every visual has a provenance and rights record.
6. Rough cut is reviewed once without music and once with the restrained score.
7. Captions, description, chapters, paper link, GitHub link, and final thumbnail are checked before upload.
8. Upload remains private or unlisted until Noah gives explicit publication approval.

## Primary context links

- NOAA Global Monitoring Laboratory, global atmospheric CO2 trends: https://www.gml.noaa.gov/ccgg/trends/global.html
- IPCC AR6 Working Group I, historical and preindustrial CO2 context: https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-2/
- Situational Awareness: https://situational-awareness.ai/
- AI 2027: https://ai-2027.com/
- AI 2040: Plan A: https://ai-2040.com/
