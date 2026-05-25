import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";

export const Background: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  // Slowly drifting radial gradients to add subtle motion
  const drift = Math.sin(frame / 60) * 40;

  return (
    <AbsoluteFill
      style={{
        background: `
          radial-gradient(${width * 0.6}px ${height * 0.55}px at ${80 + drift / 4}% ${-10 + drift / 8}%, rgba(34,211,238,0.18), transparent),
          radial-gradient(${width * 0.45}px ${height * 0.4}px at ${10 - drift / 6}% ${-10 - drift / 10}%, rgba(124,58,237,0.22), transparent),
          radial-gradient(${width * 0.5}px ${height * 0.5}px at 50% 110%, rgba(56,189,248,0.10), transparent),
          ${theme.colors.bg}
        `,
      }}
    />
  );
};
