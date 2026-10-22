import {Main} from './Main';
import {HEADLINES,SCENES} from './Scenes';
import {FPS,SHOTS,TOTAL} from './timeline';
import {SCORE_VOLUME,SOUND_CUES} from './audio';
import {C} from './visual';

export const WORKBENCH={
  name:'RealmForge — Your next move',fps:FPS,width:1920,height:1080,total:TOTAL,background:C.bg,
  shots:SHOTS.map(shot=>({...shot,component:SCENES[shot.id],props:{headline:HEADLINES[shot.id]},schema:[
    {type:'text',key:'headline',label:'Headline',default:HEADLINES[shot.id]},
    ...(shot.id==='brand'?[{type:'color',key:'color',label:'Accent',default:C.gold}]:[]),
  ]})),
  transitions:[],captions:[],overlays:[],
  sfx:SOUND_CUES.map(cue=>({from:cue.from,duration:cue.duration,src:cue.src,volume:cue.volume})),
  bgm:[{from:0,duration:TOTAL,src:'audio/score.wav',volume:SCORE_VOLUME}],
  original:Main,
};
