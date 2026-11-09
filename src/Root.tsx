import React from "react";
import { Composition } from "remotion";
import { BridgeShort, BRIDGE_FRAMES } from "./videos/bridge/Bridge";
import { BridgeShort as FallShort, BRIDGE_FRAMES as FallShort_FRAMES } from "./videos/fall/Bridge";

// 720x1280 @ 30 fps is the default output of this repo (free CPU rendering on GitHub Actions).
// The look is resolution independent: ink, lens blur and bloom scale with height / 1920.
export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="BridgeShort" component={BridgeShort} durationInFrames={BRIDGE_FRAMES} fps={30} width={720} height={1280} />
    <Composition id="FallShort" component={FallShort} durationInFrames={FallShort_FRAMES} fps={30} width={720} height={1280} />
  </>
);
