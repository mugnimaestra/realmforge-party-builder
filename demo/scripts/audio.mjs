// Original deterministic 120 BPM score, plus attributed cinematic sound effects.
import {mkdir,writeFile,readFile} from 'node:fs/promises';
import {existsSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';

await mkdir('public/audio',{recursive:true});
await mkdir('public/fonts',{recursive:true});
const sr=48000, seconds=50, samples=new Float32Array(sr*seconds);
let state=711;
const noise=()=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return state/4294967296*2-1};
const add=(start,duration,fn,gain=1)=>{
  const offset=Math.round(start*sr),count=Math.round(duration*sr);
  for(let i=0;i<count&&offset+i<samples.length;i++)if(offset+i>=0)samples[offset+i]+=fn(i/sr,i/count)*gain;
};
const note=m=>440*2**((m-69)/12);
// Four-on-the-floor pulse, a warm minor-key bass, restrained hats, and wide pads.
// The quiet opening and encounter break give the product room to breathe.
for(let beat=0;beat<100;beat++){
  const t=beat/2, energy=beat<6?.32:beat<20?.55:beat>=56&&beat<64?.42:beat>=86?1:.8;
  add(t,.34,(s)=>Math.sin(2*Math.PI*(48*s+7*(1-Math.exp(-s*38))))*Math.exp(-s*18),.43*energy);
  if(beat%2===1)add(t,.16,s=>(noise()*.75+Math.sin(2*Math.PI*180*s)*.25)*Math.exp(-s*32),.13*energy);
  if(beat>=12){
    add(t+.25,.09,s=>noise()*Math.exp(-s*65),.055*energy);
    add(t,.055,s=>noise()*Math.exp(-s*95),.025*energy);
  }
  const roots=[38,34,41,36], root=roots[Math.floor(beat/8)%4];
  add(t+.05,.36,(s,p)=>{
    const f=note(root),wave=Math.sin(2*Math.PI*f*s)+.23*Math.sin(4*Math.PI*f*s);
    return wave*Math.min(1,s*90)*(1-p)**2;
  },.18*energy);
  if(beat%4===0){
    const chord=[root+24,root+27,root+31];
    add(t,2,(s,p)=>chord.reduce((v,m,j)=>v+Math.sin(2*Math.PI*note(m)*(1+j*.0008)*s),0)/3*Math.sin(Math.PI*p)**2,.065);
  }
}
// A restrained ascending texture leads into the final wordmark landing at b90.
add(43,2,(s,p)=>noise()*p*p*Math.sin(Math.PI*p),.10);
for(let i=0;i<samples.length;i++){
  const t=i/sr,fade=Math.min(1,t/.03,(seconds-t)/1.5);
  samples[i]=Math.tanh(samples[i]*1.3)*fade;
}
function wav(data){
  const b=Buffer.alloc(44+data.length*2);b.write('RIFF');b.writeUInt32LE(b.length-8,4);b.write('WAVEfmt ',8);b.writeUInt32LE(16,16);b.writeUInt16LE(1,20);b.writeUInt16LE(1,22);b.writeUInt32LE(sr,24);b.writeUInt32LE(sr*2,28);b.writeUInt16LE(2,32);b.writeUInt16LE(16,34);b.write('data',36);b.writeUInt32LE(data.length*2,40);
  data.forEach((v,i)=>b.writeInt16LE(Math.round(Math.max(-1,Math.min(1,v))*32760),44+i*2));return b;
}
await writeFile('public/audio/score.wav',wav(samples));
const assets=[
  ['impact',1143,'Cinematic whoosh deep impact'],
  ['sweep',1490,'Fast whoosh transition'],
  ['paper',1104,'Page turn single'],
  ['shimmer',2633,'Sweeping sparkle presentation intro'],
];
const manifest={sourceVersion:1,score:{author:'RealmForge demo production',bpm:120,sampleRate:sr,beat0:0,seed:711,license:'Original project asset'},sfx:[]};
for(const [name,id,title] of assets){
  const url=`https://assets.mixkit.co/active_storage/sfx/${id}/${id}-preview.mp3`;
  const src=`public/audio/${name}-source.mp3`;
  if(!existsSync(src)){
    const response=await fetch(url);if(!response.ok)throw Error(`${name}: ${response.status}`);
    await writeFile(src,Buffer.from(await response.arrayBuffer()));
  }
  execFileSync('ffmpeg',['-v','error','-y','-i',src,'-ac','1','-ar',String(sr),'-af','loudnorm=I=-19:TP=-3:LRA=7',`public/audio/${name}.wav`]);
  const bytes=await readFile(src);
  const pcm=execFileSync('ffmpeg',['-v','error','-i',`public/audio/${name}.wav`,'-f','f32le','-ac','1','-ar',String(sr),'-']);
  let peak=0,index=0;for(let i=0;i<pcm.length/4;i++){let v=Math.abs(pcm.readFloatLE(i*4));if(v>peak){peak=v;index=i}}
  manifest.sfx.push({name,title,url,license:'Mixkit Sound Effects Free License',sha256:createHash('sha256').update(bytes).digest('hex'),peakSeconds:index/sr,duration:pcm.length/4/sr});
}
const fonts=[['CormorantGaramond','cormorantgaramond','CormorantGaramond[wght].ttf'],['SourceSans3','sourcesans3','SourceSans3[wght].ttf'],['IBMPlexMono','ibmplexmono','IBMPlexMono-Regular.ttf']];
const fontData={};
for(const [name,dir,file] of fonts){
  for(const [remote,local] of [[file,`${name}.ttf`],['OFL.txt',`${name}-OFL.txt`]]){
    const path=`public/fonts/${local}`;if(existsSync(path))continue;
    const url=`https://raw.githubusercontent.com/google/fonts/main/ofl/${dir}/${encodeURIComponent(remote)}`;
    const response=await fetch(url);if(!response.ok)throw Error(`Font ${name}: ${response.status}`);
    await writeFile(path,Buffer.from(await response.arrayBuffer()));
  }
  fontData[name]=(await readFile(`public/fonts/${name}.ttf`)).toString('base64');
}
await writeFile('public/fonts/font-data.json',JSON.stringify(fontData));
await writeFile('src/audio-manifest.json',JSON.stringify(manifest,null,2)+'\n');
console.log('Original 120 BPM score, normalized SFX, font files, and provenance ready');
