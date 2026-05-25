import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { theme } from "../theme";

const FEATURES = [
  { icon: "🎙️", title: "Natural conversations", body: "Ask follow-ups, get instant examples." },
  { icon: "🧠", title: "Quizzes that stick", body: "Spaced review built right in." },
  { icon: "✨", title: "Made for adults", body: "Designed for serious learners 18+." },
];

const FeatureCard: React.FC<{
  icon: string;
  title: string;
  body: string;
  delay: number;
}> = ({ icon, title, body, delay }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame: frame - delay,
    fps,
    config: { damping: 14, stiffness: 100 },
  });

  const x = interpolate(progress, [0, 1], [-80, 0]);
  const opacity = interpolate(frame - delay, [0, 14], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        transform: `translateX(${x}px)`,
        opacity,
        padding: "32px 40px",
        borderRadius: 24,
        background: theme.colors.cardBg,
        border: `1px solid ${theme.colors.cardBorder}`,
        display: "flex",
        alignItems: "center",
        gap: 28,
        width: 900,
      }}
    >
      <div style={{ fontSize: 72 }}>{icon}</div>
      <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
        <div style={{ fontSize: 44, fontWeight: 700, color: theme.colors.text, letterSpacing: -0.5 }}>
          {title}
        </div>
        <div style={{ fontSize: 30, color: theme.colors.muted }}>{body}</div>
      </div>
    </div>
  );
};

export const FeaturesScene: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
        gap: 24,
      }}
    >
      {FEATURES.map((f, i) => (
        <FeatureCard
          key={f.title}
          icon={f.icon}
          title={f.title}
          body={f.body}
          delay={i * 8}
        />
      ))}
    </AbsoluteFill>
  );
};
