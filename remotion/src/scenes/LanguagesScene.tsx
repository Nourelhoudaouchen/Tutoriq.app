import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { theme } from "../theme";

const LANGUAGES = [
  { name: "Arabic", native: "العربية" },
  { name: "French", native: "Français" },
  { name: "English", native: "English" },
];

const LanguagePill: React.FC<{
  name: string;
  native: string;
  delay: number;
}> = ({ name, native, delay }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame: frame - delay,
    fps,
    config: { damping: 14, stiffness: 100 },
  });

  const scale = interpolate(progress, [0, 1], [0.6, 1]);
  const opacity = interpolate(frame - delay, [0, 14], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const y = interpolate(progress, [0, 1], [60, 0]);

  return (
    <div
      style={{
        transform: `translateY(${y}px) scale(${scale})`,
        opacity,
        padding: "32px 48px",
        borderRadius: 28,
        background: theme.colors.cardBg,
        border: `2px solid ${theme.colors.cardBorder}`,
        backdropFilter: "blur(10px)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 8,
        minWidth: 280,
      }}
    >
      <div
        style={{
          fontSize: 52,
          fontWeight: 700,
          color: theme.colors.text,
          letterSpacing: -1,
        }}
      >
        {name}
      </div>
      <div
        style={{
          fontSize: 36,
          fontWeight: 500,
          color: theme.colors.muted,
        }}
      >
        {native}
      </div>
    </div>
  );
};

export const LanguagesScene: React.FC = () => {
  const frame = useCurrentFrame();

  const headerOpacity = interpolate(frame, [0, 10], [0, 1], {
    extrapolateRight: "clamp",
  });
  const headerY = interpolate(frame, [0, 10], [-20, 0], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
        gap: 60,
      }}
    >
      <div
        style={{
          opacity: headerOpacity,
          transform: `translateY(${headerY}px)`,
          fontSize: 56,
          fontWeight: 700,
          color: theme.colors.text,
          letterSpacing: -1,
        }}
      >
        Learn in 3 languages
      </div>
      <div style={{ display: "flex", gap: 32, flexWrap: "wrap", justifyContent: "center" }}>
        {LANGUAGES.map((lang, i) => (
          <LanguagePill key={lang.name} name={lang.name} native={lang.native} delay={12 + i * 6} />
        ))}
      </div>
    </AbsoluteFill>
  );
};
