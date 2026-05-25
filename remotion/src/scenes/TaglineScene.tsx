import { AbsoluteFill, useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";
import { theme } from "../theme";

const Line: React.FC<{ text: string; delay: number; gradient?: boolean }> = ({
  text,
  delay,
  gradient,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame: frame - delay,
    fps,
    config: { damping: 16, stiffness: 110 },
  });

  const opacity = interpolate(frame - delay, [0, 12], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const y = interpolate(progress, [0, 1], [40, 0]);

  return (
    <div
      style={{
        opacity,
        transform: `translateY(${y}px)`,
        fontSize: 96,
        fontWeight: 800,
        letterSpacing: -2,
        lineHeight: 1.05,
        textAlign: "center",
        ...(gradient
          ? {
              backgroundImage: theme.gradients.brand,
              WebkitBackgroundClip: "text",
              backgroundClip: "text",
              color: "transparent",
            }
          : { color: theme.colors.text }),
      }}
    >
      {text}
    </div>
  );
};

export const TaglineScene: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
        gap: 16,
        padding: "0 80px",
      }}
    >
      <Line text="Speak with your" delay={0} />
      <Line text="AI tutor." delay={8} gradient />
    </AbsoluteFill>
  );
};
