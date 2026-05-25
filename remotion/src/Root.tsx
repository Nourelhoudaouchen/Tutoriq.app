import { Composition } from "remotion";
import { TutoriqPromo } from "./TutoriqPromo";

const FPS = 30;
const DURATION_SECONDS = 12;

export const Root: React.FC = () => {
  return (
    <>
      <Composition
        id="TutoriqPromo"
        component={TutoriqPromo}
        durationInFrames={FPS * DURATION_SECONDS}
        fps={FPS}
        width={1920}
        height={1080}
      />
      <Composition
        id="TutoriqPromoVertical"
        component={TutoriqPromo}
        durationInFrames={FPS * DURATION_SECONDS}
        fps={FPS}
        width={1080}
        height={1920}
      />
    </>
  );
};
