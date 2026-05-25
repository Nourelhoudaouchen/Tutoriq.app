import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { theme } from "../theme";

export const CtaScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleProgress = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 110 },
  });
  const titleY = interpolate(titleProgress, [0, 1], [40, 0]);
  const titleOpacity = interpolate(frame, [0, 12], [0, 1], { extrapolateRight: "clamp" });

  const buttonProgress = spring({
    frame: frame - 14,
    fps,
    config: { damping: 12, stiffness: 130 },
  });
  const buttonScale = interpolate(buttonProgress, [0, 1], [0.7, 1]);
  const buttonOpacity = interpolate(frame - 14, [0, 12], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Subtle pulsing on the button after it appears
  const pulse = 1 + Math.sin((frame - 26) / 8) * 0.02;
  const finalButtonScale = frame > 26 ? buttonScale * pulse : buttonScale;

  const urlOpacity = interpolate(frame, [40, 52], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
        gap: 48,
      }}
    >
      <div
        style={{
          opacity: titleOpacity,
          transform: `translateY(${titleY}px)`,
          fontSize: 84,
          fontWeight: 800,
          color: theme.colors.text,
          letterSpacing: -1.5,
          textAlign: "center",
        }}
      >
        Join the waitlist.
      </div>

      <div
        style={{
          opacity: buttonOpacity,
          transform: `scale(${finalButtonScale})`,
          padding: "28px 56px",
          borderRadius: 20,
          background: theme.gradients.brand,
          color: "white",
          fontSize: 52,
          fontWeight: 700,
          letterSpacing: -0.5,
          boxShadow: "0 20px 60px rgba(124,58,237,0.45), 0 16px 40px rgba(34,211,238,0.25)",
        }}
      >
        Get early access →
      </div>

      <div
        style={{
          opacity: urlOpacity,
          fontSize: 36,
          color: theme.colors.muted,
          fontWeight: 500,
          letterSpacing: 0.5,
        }}
      >
        tutoriq.app
      </div>
    </AbsoluteFill>
  );
};
