import { Config } from "@remotion/cli/config";

Config.setOverwriteOutput(true);
// the Kenney GLB kit is loaded before the first frame; software GL on CI is slow
Config.setDelayRenderTimeoutInMilliseconds(180000);
