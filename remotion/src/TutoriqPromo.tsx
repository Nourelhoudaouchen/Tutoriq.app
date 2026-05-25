import { AbsoluteFill, Sequence, useVideoConfig } from "remotion";
import { Background } from "./components/Background";
import { LogoScene } from "./scenes/LogoScene";
import { TaglineScene } from "./scenes/TaglineScene";
import { LanguagesScene } from "./scenes/LanguagesScene";
import { FeaturesScene } from "./scenes/FeaturesScene";
import { CtaScene } from "./scenes/CtaScene";

// Scene timing in seconds
const SCENES = {
  logo: { from: 0, duration: 2 },
  tagline: { from: 2, duration: 2.5 },
  languages: { from: 4.5, duration: 2.5 },
  features: { from: 7, duration: 2.5 },
  cta: { from: 9.5, duration: 2.5 },
};

export const TutoriqPromo: React.FC = () => {
  const { fps } = useVideoConfig();

  const toFrames = (seconds: number) => Math.round(seconds * fps);

  return (
    <AbsoluteFill style={{ fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, sans-serif" }}>
      <Background />

      <Sequence
        from={toFrames(SCENES.logo.from)}
        durationInFrames={toFrames(SCENES.logo.duration)}
      >
        <LogoScene />
      </Sequence>

      <Sequence
        from={toFrames(SCENES.tagline.from)}
        durationInFrames={toFrames(SCENES.tagline.duration)}
      >
        <TaglineScene />
      </Sequence>

      <Sequence
        from={toFrames(SCENES.languages.from)}
        durationInFrames={toFrames(SCENES.languages.duration)}
      >
        <LanguagesScene />
      </Sequence>

      <Sequence
        from={toFrames(SCENES.features.from)}
        durationInFrames={toFrames(SCENES.features.duration)}
      >
        <FeaturesScene />
      </Sequence>

      <Sequence
        from={toFrames(SCENES.cta.from)}
        durationInFrames={toFrames(SCENES.cta.duration)}
      >
        <CtaScene />
      </Sequence>
    </AbsoluteFill>
  );
};
