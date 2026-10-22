import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {Main} from './Main';
import {FPS,TOTAL} from './timeline';

registerRoot(()=>React.createElement(Composition,{id:'RealmForge',component:Main,durationInFrames:TOTAL,fps:FPS,width:1920,height:1080,defaultProps:{bgm:true}}));
