import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
import {mkdir} from 'node:fs/promises';
const run=promisify(execFile);
const frames=[30,150,210,330,390,570,630,810,990,1050,1290,1350,1560,1650,1710,1890,2130,2190,2280,2340,2370,2550,2610,2730,2970];
await mkdir('out/qa',{recursive:true});
// Two owned render workers; no shared browser/profile and no unbounded fan-out.
let index=0;
await Promise.all([0,1].map(async()=>{
  while(index<frames.length){
    const frame=frames[index++];
    await run('npx',['remotion','still','src/index.ts','RealmForge',`out/qa/f${frame}.png`,`--frame=${frame}`],{maxBuffer:1024*1024});
    console.log(`Checked frame ${frame}`);
  }
}));
