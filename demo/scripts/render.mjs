// Remotion produces the picture and both timeline-driven PCM mixes. FFmpeg
// performs final AAC/MP4 muxing so encoder priming is represented correctly.
import {execFileSync} from 'node:child_process';
import {existsSync} from 'node:fs';
import {mkdir} from 'node:fs/promises';

const noBgm=process.argv.includes('--nobgm');
const reuse=process.argv.includes('--reuse-picture');
await mkdir('out',{recursive:true});
const run=(command,args)=>execFileSync(command,args,{stdio:'inherit'});
const common=['remotion','render','src/index.ts','RealmForge'];
if((!noBgm&&!reuse)||!existsSync('out/picture.mp4')){
  run('npx',[...common,'out/picture.mp4','--muted','--codec=h264','--crf=25','--concurrency=2','--timeout=120000']);
}
const mix=noBgm?'out/mix-nobgm.wav':'out/mix.wav';
run('npx',[...common,mix,'--codec=wav','--concurrency=2','--timeout=120000',...(noBgm?['--props=props-nobgm.json']:[])]);
const output=noBgm?'../docs/demo-nobgm.mp4':'../docs/demo.mp4';
const metadata=JSON.parse(execFileSync('ffprobe',['-v','error','-show_entries','format=duration','-of','json','out/picture.mp4'],{encoding:'utf8'}));
const duration=Number(metadata.format.duration);
if(!Number.isFinite(duration)||duration<=0)throw Error('Picture track has no valid duration');
run('ffmpeg',['-v','error','-y','-i','out/picture.mp4','-i',mix,'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-af',`apad=whole_dur=${duration}`,'-t',String(duration),'-movflags','+faststart',output]);
console.log(`Finished ${output}; shared picture track, ${noBgm?'SFX only':'score and SFX'}`);
