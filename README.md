# Cartoon 3D Shorts (Antigravity CLI + GitHub Actions)

Fork of [mromidev/claude-animated-shorts](https://github.com/mromidev/claude-animated-shorts) (MIT), reworked so that
**Antigravity CLI (`agy`)** can drive it from a phone and **GitHub Actions** does all the rendering.

- Output: vertical 720x1280, 30 fps, 40 s story shorts (2D cartoon characters in a 3D world, ink outlines, lens blur,
  synthesized music and SFX). No AI video generator.
- Nothing heavy on your device: you push code and text, Actions renders, you download the small MP4 (artifact or Release).

## Use it
1. Push this repo to a **public** GitHub repo (free Actions minutes).
2. Add the free CC0 Kenney GLB props you want to `public/bridge/kenney/` (see its README). Optional.
3. In `agy`, in this folder: *"Use the cartoon short skill and make a 40 s short about ..."*
4. Run the **Render** workflow (smoke test first), then the full render with a `[render]` commit message.

Agent instructions: `AGENTS.md` and `.agents/skills/cartoon-3d-short/SKILL.md`.

## Status
Untested end to end: the first smoke run will probably need small package-version fixes (see the skill's first-run checklist).

## Licence
Code and docs: MIT (see `LICENSE`). The original reference frames are not included (style study only).
