import { AbsoluteFill, spring, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { theme } from "../theme";

export const LogoScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 120, mass: 0.8 },
  });

  const opacity = interpolate(frame, [0, 10], [0, 1], { extrapolateRight: "clamp" });
  const wordmarkOpacity = interpolate(frame, [12, 24], [0, 1], { extrapolateRight: "clamp" });
  const wordmarkY = interpolate(frame, [12, 24], [20, 0], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
        gap: 28,
      }}
    >
      <div
        style={{
          width: 220,
          height: 220,
          borderRadius: 48,
          background: theme.gradients.brand,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "white",
          fontWeight: 900,
          fontSize: 110,
          letterSpacing: -2,
          transform: `scale(${scale})`,
          opacity,
          boxShadow: "0 30px 80px rgba(124,58,237,0.45), 0 20px 60px rgba(34,211,238,0.25)",
        }}
      >
        TQ
      </div>

      <div
        style={{
          fontSize: 88,
          fontWeight: 800,
          letterSpacing: -1.5,
          color: theme.colors.text,
          opacity: wordmarkOpacity,
          transform: `translateY(${wordmarkY}px)`,
        }}
      >
        Tutoriq
      </div>
    </AbsoluteFill>
  );
};
