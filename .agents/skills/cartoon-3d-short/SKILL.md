---
name: cartoon-3d-short
description: Make a ~40 s vertical cartoon story short (720x1280, 30 fps) in the "2D characters in a colourful 3D world" style (flat bean-head cartoon cards with ink outlines, painted 3D town, saturated sky, depth-of-field, gliding cameras, voice narration, synthesized SFX and march-style music), rendered with three.js inside Remotion on GitHub Actions. Proven on "The Bridge That Fell for a Song". Use when the user asks for a new story short in that cartoon 3D style, "like the bridge video", or says "use the cartoon short skill".
---

# Cartoon 3D story short (three.js + Remotion, rendered on GitHub Actions)

This repo is set up for **Antigravity CLI (`agy`)** working from a phone (Termux). The phone never renders and never holds big files:
you edit code and text, push, and GitHub Actions renders the video. The final MP4 is a GitHub artifact (or Release).

## Defaults (change only if the user says so)
- Output **720x1280, 30 fps, 40 s = 1200 frames** (`TOTAL = 1200` in `story.ts`, `totalFrames: 1200` in `render.config.json`).
- Render on Actions only: software WebGL (`--gl=swangle`), 4 parallel chunks, then joined. Never run a full render on the phone.
- Story, characters and voice are always original. The `references/` material is private style study: never publish it, never copy its scripts, characters or shots, never name the channel in a voice-over or description. `references/frames/` and `references/sheets/` are git-ignored, keep them that way.
- No captions or labels in the video. English only. Voice: one steady tone. Jokes are researched real facts.
- Mix: music +3 dB, SFX -6 dB, voice unchanged (`audio/mix.py`).

## Repo map
- `src/videos/bridge/`: the proven bridge short (world, characters, ink, lens blur, grade, story/camera). It is also the template.
- `src/Root.tsx`: composition registry (720x1280).
- `scripts/`: `new-short.sh`, `bridge-stills.mjs`, `short_qa.py`, `sbs_sheet.py`, `bridge_shots.py`.
- `audio/`: synthesized SFX + march score + mix (bridge-specific `timeline.py` must be rewritten per story).
- `voice/`: `voice.wav` + `words.json` for the current short.
- `public/bridge/kenney/`: CC0 GLB props (see its README; missing files are skipped).
- `render.config.json`: `composition`, `totalFrames`, `chunks`, `release`.
- `.github/workflows/render.yml` (video) and `stills.yml` (single frames).

## Pipeline
1. **Topic and facts.** One surprising true story with a physical cause and effect (visual), plus a simple everyday analogy. Put the facts with sources at the top of `SCRIPT.md`.
2. **Script, ~150 words for 40 s** (~3.7 words/s). Beats (compress the bridge formula): Hook (the absurd fact in one line) > Setting (year, place) > Action (2-3 escalating beats) > Snap (the break) > Deadpan "Luckily ... / Unluckily ..." > Explanation (one physics idea via an everyday analogy) > Consequence (the rule it created) > Callback twist. Never describe on screen what the viewer already sees. See `templates/SCRIPT_example.md` (that one is 67 s).
3. **Voice.** The user supplies or approves `voice/voice.wav` (free TTS or their own voice) and `voice/words.json` (word timings from any speech-to-text with word times; hand-fix them). Everything is timed to `words.json`. Commit both: CI builds the audio from them.
4. **New short folder.** `bash scripts/new-short.sh <name>`, then follow its printed steps (register in `src/Root.tsx` at 720x1280, set `TOTAL = 1200` in `story.ts`, update `render.config.json`).
5. **Shot plan in `story.ts`.** `SHOTS` (id, a/b frames, light day/golden, crowd mode, `tau`), `XFADE`, `FLASH_AT`, `CAMS` (per-shot keys `{f, dur?, cut?, s: f => {pos, look, fov, roll}}`), `KICKS`, `DOF`/`dofAt`, `FOREGROUND`. Every visual reaction lands 0-3 frames before its word.
6. **World** (`lights.ts`, `shade.ts`, `build.ts`, `paint.ts`, `world.ts`): light presets, two-tone shading, town and Kenney props with sight-line culling, painted textures, sky shader, fog = horizon colour.
7. **Characters** (`toon.ts`, `cast.ts`, `cardshade.ts`): Canvas2D `Pen` drawing API on a 600x1000 design canvas, bean heads, camera-facing billboards on the `NOINK` layer, crowds, blinks, walk cycles.
8. **Post** (`Bridge.tsx`, `ink.ts`, `lensblur.ts`, `grade.ts`): ink > lens pre > lens main > bloom > NEUTRAL tone map > grade (MSAA 4). All pixel parameters scale with output height / 1920, so 720x1280 keeps the same look. The canvas follows the composition size (`useVideoConfig`).
9. **Sound** (`audio/`): rewrite `timeline.py` (event table, `DUR = 40.0`) and the music sections in `mix.py` for the new story, then `python3 audio/mix.py` needs numpy + scipy and writes `audio/mix.wav` (48 kHz, exact length). The sound is locked to picture time: any later timing change means re-running it. CI runs `mix.py` itself when `voice/voice.wav` and `voice/words.json` are committed.
10. **Look checks on Actions** (cheap, do these before any full render): Actions tab > **Stills** > Run workflow with e.g. `0,100,400`, open the JPEGs from the run's artifacts. Compare with the reference frames by eye (they live only on the user's machine, not in the repo).
11. **Smoke test, then full render.**
    - Commit with `[smoke]` in the message (or run **Render** with smoke = true): renders 30 frames, proves the toolchain.
    - Full video: commit with `[render]` in the message, or run **Render** with smoke = false. Chunks render in parallel; `finish` joins them, adds `audio/mix.wav`, and uploads `final.mp4` as artifact `short-<run number>` (set `"release": true` in `render.config.json` to also create a GitHub Release).
12. **Deliver.** Tell the user which run to open and the file size. If anything is wrong, fix, push, re-render only what changed.

## First-run checklist (the repo has not been run on CI yet)
- The first smoke run may fail on package versions (`package.json` ranges are a best guess for the bridge code: Remotion 4.0.x, React 18, react-three-fiber 8, postprocessing 6, three 0.170). Read the log, fix versions, rerun. When green, commit `package-lock.json`.
- If Chrome or WebGL errors appear, keep `--gl=swangle` and lower `--concurrency` to 1.
- If the job runs long, raise `chunks` in `render.config.json` (more parallel jobs), keep each chunk under ~5 h.
- Time the 30-frame smoke run; estimated chunk time = seconds per frame x frames per chunk.

## Final look values (bridge after 4 verifier rounds; all in `src/videos/bridge/`)
Start every new short from `src/videos/bridge/` (`bash scripts/new-short.sh <name>`): the look lives in these values, the
story lives in story.ts / build.ts layout / cast.ts roles. Opus max scores at the end: colour day 7, golden 5-6,
lighting 5-6, ink 6, textures 5-6, characters 7, depth 6-7, composition 6-7 (from 5/3/4/5/4/7/4/6 at the start).
- **Light presets** (`lights.ts`, sun camera-relative and frozen per shot):
  - day: az 75 / el 48, lit [1.58,1.5,1.33], shade [.30,.29,.36], lift [.05,.06,.11] (cool tint ONLY in shade), sky
    top #3e7fd2 → horizon #b8d0ec, fog = horizon, 25→300 m, uSat 1.08, ~15 % blue haze past 60 m.
  - golden: az 6 / el 7 (backlit low sun), key toward #FFB36B ×1.5, violet-blue shade (facade ≈ #444380), sky
    #ffc47c → #8a6f8a, peach fog only past 50 m, sun disc #ffcf9e + bloom, contact blobs + real card shadows.
- **Albedos** (`paint.ts`/`build.ts`): muted brick / cream / ochre / terracotta houses with plinth, cornice, sills,
  hoods, door step, chimney + pot, heights 7 / 8.4 / 9.8 m; warm grey/beige stone (saturation −35 % from "storybook");
  ochre wood deck C* ~51-58 with near-black seams; iron dark and desaturated. Never lemon, never lavender lit faces.
- **Ink** (`ink.ts`): #030303, 5.1 px near (6 m) → 3.3 px far (90 m) at 1080x1920, creases ×0.8 from 35°, depth
  jumps from 1 %, fog tint 0.3 only far; character cards on layer `NOINK` (they carry their own plum ink).
- **Lens** (`lensblur.ts` + `dofAt` in story.ts): cInf px at 1080: hook/river CU 15-16, close-ups 12-14, MS 10-12,
  park 7, golden sway 5, wides/aerials 0. Focus on the eyes of the front row.
- **Post** (`Bridge.tsx`): ink → lens pre → lens main → bloom (thr 1.0, int .5, 6 levels, radius .6) → NEUTRAL tone
  map → grade; MSAA 4. Film grain exists but is OFF (reference measures no grain; it quadruples the file size).
- **Characters** (`toon.ts`/`cast.ts`/`cardshade.ts`): bean heads h/w .94, plum ink #241726, eyes .26 W apart, no blush,
  14 expressions; adults 3.5 head-heights; walk bob 5 %, lean 1-7°, planted 0.8 m stride; blinks 0.5-2.3 s; tight
  contact shadow ~.5 under the feet + sun-direction tail by day; golden rim inner only (never an offset outer copy).
- **Camera** (`story.ts`): cuts on big jumps, smootherstep glides 18-40 f, every hold creeps (no static hold ≥4 f),
  flip kicks decaying over 7 f on impacts, 4-4.6° rolls, foreground props (`FOREGROUND`) in ~1/3 of shots.

## Look targets (measured from the reference; see references/reports/)
- **Ink:**
  - World lines: about 3 px at 1080 wide, near-black #0b0a0c, nearly constant with distance. Silhouettes, depth jumps and normal creases only. No line on wall/floor joins or the horizon. Character cards are never outlined by the world ink.
  - Character ink: dark plum #201628-#2f1d28, thicker on the bottom/shadow side.
- **Colour:**
  - Day median luma ~.57. Non-ink p5 ~.23 (no crushed blacks). Lit chroma C* p90 ~55. Day sky top ~#5e93d9, horizon 1.28x brighter.
  - Golden: peach horizon #ffd08a, violet-blue shadows (never brown), backlit sun.
- **Depth:**
  - DOF on about 1/3 of screen time (CU, MS, inserts), cInf 10-16 px at 1080, focus on the eyes. Establishing and wide shots stay sharp.
  - Fog = horizon colour, 25→420 m day, 20→360 m golden.
  - Bloom only on HDR emissives: threshold 1.0.
- **Camera:**
  - Hard cuts on big jumps. Everything else is a smootherstep glide of 18-40 f, peak ≤ 25 px/f at 720p.
  - Every hold pushes in 0.15-0.35 %/f, with 0.6 %/f on punch words.
  - Rolls of 4-5°.
  - No hand-held float. Impact shakes flip sign every frame and decay over 7 f.
- **Characters:**
  - About 3.5 head-heights tall, legs 1.4 HH.
  - Stick limbs about 0.055 of head width, ink-dot hands.
  - Bean head (h/w ~0.93, narrower chin, pointier crown).
  - No blush or eye highlights. Faces at brightness ~.93.
  - Walk bob 3-7 %, lean 1-7°, planted feet.
  - Blinks every 0.5-2.3 s, lasting 4 f.

## Gotchas
- Kenney nature-kit materials are teal: recolour them by material name in `build.ts`.
- Cameras end up inside houses: the sight-line culler in `build.ts`/`world.ts` removes anything blocking a camera ray.
- Ink in the same merged effect pass as DOF gets overwritten. Ink must be its own pass before the blur.
- Pixel-sized post parameters must scale with resolution (height / 1920). Do not use `--scale` to shrink: R3F clamps dpr to >= 1, so the buffer would stay full size. Set the composition size instead (`width={720} height={1280}`).
- Remotion writes a silent audio track: CI renders with `--muted` and muxes `audio/mix.wav` (`-map 0:v:0 -map 1:a:0`).
- Scratch `.ts` files inside `out/` break `tsc`: name them `.txt`.
- Film grain is OFF on purpose (reference has none, it quadruples the file size).
- Each Remotion bundle copies `public/` into the temp folder: fine on CI (throwaway), keep `public/` small (only the GLBs you use).
- Original author timings (1440x2560 at ~4 fps on a GPU PC) do not apply to CPU rendering; measure with the smoke run.
- Windows-only things from the original skill (Opus verifier agents, SendUserFile, D: temp drives, sandbox merge script) were removed. Do the look checks yourself from stills and ask the user for a judgement.

## Readability traps the verifier caught (check every new prop/shot for these)
- **A swing drawn as one rope that disappears behind the kid reads as a HANGING.** Always two ropes to a wide plank
  with the kid between them (`swingKid` in toon.ts), and a frame whose legs clear the arc (A-frame at each end).
- Props or flotsam closer than ~2 m to a lens become huge cut-off blobs at the frame edge. When a camera moves, re-check
  every prop near its new position (the river cameras moved into the floating hats).
- A foreground bush cut by the frame edge reads as a "green ball"; a foreground prop must be recognisable or gone.
- Flags: red + yellow star/diamond reads as Vietnam's. Use a period-correct flag (St George's cross for England 1831).
- Painted signs lit by a side sun go grey-blue and unreadable: give the sign face an unlit material.
- Golden rim light done as an offset outer copy turns every hat into a picture frame: inner rim only, head/torso only.
- Balcony/railing rails at chest height through characters: put the lens ~2.5 m up so rails cross legs, not torsos.
- Flat holds read as freezes in QA (frozen span ≥12 f): every hold needs a creeping push-in.
