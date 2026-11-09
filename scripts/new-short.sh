#!/usr/bin/env bash
# usage: bash scripts/new-short.sh <name>     e.g. bash scripts/new-short.sh cannon
# Copies the bridge short (the template) to src/videos/<name>/ and prints what to register.
set -euo pipefail
name="${1:?usage: new-short.sh <name>}"
[ -e "src/videos/$name" ] && { echo "src/videos/$name already exists"; exit 1; }
cp -r src/videos/bridge "src/videos/$name"
Comp="$(echo "${name:0:1}" | tr a-z A-Z)${name:1}Short"
echo "Created src/videos/$name"
echo
echo "1) In src/Root.tsx add:"
echo "   import { BridgeShort as ${Comp}, BRIDGE_FRAMES as ${Comp}_FRAMES } from \"./videos/$name/Bridge\";"
echo "   <Composition id=\"$Comp\" component={$Comp} durationInFrames={${Comp}_FRAMES} fps={30} width={720} height={1280} />"
echo "2) In src/videos/$name/story.ts set TOTAL = 1200 for a 40 s short, then rewrite SHOTS/CAMS/KICKS to your words.json."
echo "3) In render.config.json set composition=$Comp and totalFrames=1200."
