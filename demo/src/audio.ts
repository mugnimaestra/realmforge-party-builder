import manifest from './audio-manifest.json';
import {FPS,SFX,TOTAL} from './timeline';

// The source peak and encoder offset are separate measurements. Calibrate the
// latter from the rendered no-BGM output; do not alter the source beat grid.
export const OUTPUT_OFFSET_FRAMES=0;
export const SCORE_VOLUME=.62;
export const SOUND_CUES=SFX.map(cue=>{
  const source=manifest.sfx.find(s=>s.name===cue.src)!;
  const from=cue.from-Math.round(source.peakSeconds*FPS)-OUTPUT_OFFSET_FRAMES;
  return {...cue,from,duration:Math.min(Math.ceil(source.duration*FPS),TOTAL-from),src:`audio/${cue.src}.wav`,target:cue.from};
});
