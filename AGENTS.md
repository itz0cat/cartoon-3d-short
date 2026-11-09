# AGENTS.md (read by Antigravity CLI `agy` at session start)

Project: original vertical cartoon story shorts, "2D characters in a colourful 3D world", made with three.js inside Remotion.
Default output: 720x1280, 30 fps, 40 s (1200 frames). The full workflow is the skill in
`.agents/skills/cartoon-3d-short/SKILL.md`. Read it before doing any work here, and run `agy inspect` if the skill is not loaded.

## Hard rules
- The user works from a phone (Termux). **Never render video locally and never download or create big files on the device.**
  Rendering happens on GitHub Actions (`.github/workflows/render.yml`); stills for look checks via `stills.yml`.
- Start a render by pushing a commit whose message contains `[smoke]` (30 frames) or `[render]` (full video),
  or via `gh workflow run render.yml -f smoke=true|false` if the GitHub CLI is installed and logged in.
- Settings live in `render.config.json` (`composition`, `totalFrames`, `chunks`, `release`). Keep `totalFrames` equal to the
  composition's `durationInFrames` (40 s = 1200).
- The repo is public. Never commit `references/frames/`, `references/sheets/`, `.env` files, API keys or tokens.
  Everything in `references/` is private style study: never copy its scripts, characters or shots into a video.
- Story, characters and voice are original. English only, no captions in the video.
- Size every composition 720x1280 unless the user asks otherwise; never use `--scale` to shrink (it does not shrink the WebGL buffer).
- Do not delete or restructure `src/videos/bridge/`: it is the template for every new short (`bash scripts/new-short.sh <name>`).

## Commands
- New short: `bash scripts/new-short.sh <name>` (prints what to register).
- Type check (if Node is available): `npx tsc --noEmit`.
- Audio: `python3 audio/mix.py` (needs numpy + scipy; rewrite `audio/timeline.py` for each story first). CI runs it when
  `voice/voice.wav` and `voice/words.json` are committed.
- Smoke test: `git commit --allow-empty -m "test [smoke]" && git push`.

## Working style
- Save after every step (commit and push small changes).
- After each render, report the run link and file size, not file contents.
- When something fails on CI, read the log, fix the cause, and re-run the smallest job that proves the fix (stills or smoke).
