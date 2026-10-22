import React from 'react';
import {AbsoluteFill,Sequence,staticFile} from 'remotion';
import {Audio} from '@remotion/media';
import {SCENES} from './Scenes';
import {SHOTS} from './timeline';
import {SCORE_VOLUME,SOUND_CUES} from './audio';
import {C} from './visual';

export type MainProps={bgm?:boolean};
export const Main:React.FC<MainProps>=({bgm=true})=><AbsoluteFill style={{background:C.bg}}>
  {SHOTS.map(shot=>{
    const Component=SCENES[shot.id];
    return <Sequence key={shot.id} from={shot.from} durationInFrames={shot.duration} premountFor={30}><Component/></Sequence>;
  })}
  {bgm&&<Audio src={staticFile('audio/score.wav')} volume={SCORE_VOLUME}/>}
  {SOUND_CUES.map((cue,i)=><Sequence key={i} from={cue.from} durationInFrames={cue.duration} premountFor={30}><Audio src={staticFile(cue.src)} volume={cue.volume}/></Sequence>)}
</AbsoluteFill>;
