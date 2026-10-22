import React from 'react';
import {AbsoluteFill,Easing,Freeze,Sequence,interpolate,staticFile,useCurrentFrame} from 'remotion';
import {Video} from '@remotion/media';
import evidence from './evidence.json';
import layout from '../public/textures/layout.json';
import {b} from './timeline';
import {Backdrop,C,Camera,Head,Label,Seal,Texture,clamp,ease,mono,ramp,serif} from './visual';

export type SceneProps={headline?:string;color?:string};
export const HEADLINES={chance:'Your next move.',brand:'RealmForge',table:'One table.',party:'Meet your party.',dice:'Every modifier counts.',bestiary:'Know what you face.',combat:'Test the encounter.',portrait:'Give your hero a face.',outro:'RealmForge'};
export const Chance:React.FC<SceneProps>=({headline=HEADLINES.chance})=>{
  const f=useCurrentFrame(),p=ramp(f,0,b(2));
  const rotation=interpolate(f,[0,b(2)-8,b(2)],[220,-5,0],clamp);
  return <Backdrop>
    <Label style={{position:'absolute',left:100,top:100}}>A LITTLE CHANCE</Label>
    <div style={{position:'absolute',left:710,top:140,transform:`translateY(${(1-p)*-650}px) perspective(1100px) rotateY(${(1-p)*65}deg) rotate(${rotation}deg) scale(${.65+.35*p})`,filter:'drop-shadow(-35px 50px 40px #0009)'}}>
      <Texture name="die" style={{width:500,height:548}}/>
    </div>
    <div style={{position:'absolute',left:570,top:700,width:780,height:55,background:'radial-gradient(ellipse,#0009,transparent 70%)',opacity:p}}/>
    <Head style={{position:'absolute',top:790,width:'100%',textAlign:'center',fontSize:100}}>{headline}</Head>
    <Label style={{position:'absolute',bottom:75,width:'100%',textAlign:'center',fontSize:32}}>ACTUAL ROLL · {evidence.dice.dice}</Label>
  </Backdrop>;
};

export const Brand:React.FC<SceneProps>=({headline=HEADLINES.brand,color=C.gold})=>{
  const f=useCurrentFrame();
  return <Backdrop>
    <Seal size={620} style={{position:'absolute',right:90,top:70,opacity:.13,transform:`rotate(${(1-ramp(f,0,60))*-12}deg)`}}/>
    <div style={{position:'absolute',left:100,top:320,display:'flex',fontFamily:serif,fontWeight:700,fontSize:240,letterSpacing:-8,lineHeight:1,color}}>
      {[...headline].map((letter,i)=><span key={i} style={{overflow:'hidden',display:'inline-block',paddingBottom:12}}><span style={{display:'inline-block',transform:`translateY(${(1-ramp(f,i*3,30))*115}%) rotate(${(1-ramp(f,i*3,30))*8}deg)`}}>{letter}</span></span>)}
    </div>
    <div style={{position:'absolute',left:108,top:635,width:interpolate(f,[b(2),b(3)],[0,170],clamp),height:2,background:color}}/>
    <Label style={{position:'absolute',left:108,top:690,opacity:ramp(f,b(2),b(1))}}>THE GM’S TABLE</Label>
  </Backdrop>;
};

export const Table:React.FC<SceneProps>=({headline=HEADLINES.table})=>{
  const f=useCurrentFrame(),p=ramp(f,0,b(2));
  return <Backdrop>
    <Label style={{position:'absolute',left:100,top:100}}>{headline}</Label>
    <div style={{position:'absolute',left:100,top:300}}>{['Heroes.','Dice.','Encounters.'].map((word,i)=><Head key={word} style={{fontSize:112,marginBottom:22,opacity:ramp(f,b(i*2),b(1)),transform:`translateY(${(1-ramp(f,b(i*2),b(1)))*40}px)`}}>{word}</Head>)}</div>
    <div style={{position:'absolute',left:730,top:240,width:1090,transform:`perspective(1400px) rotateY(${(1-p)*-16}deg) translateY(${(1-p)*100}px)`,boxShadow:'-35px 50px 90px #0009',border:`1px solid ${C.gold}66`}}><Texture name="welcome" style={{width:'100%'}}/></div>
    <div style={{position:'absolute',left:735,top:900,fontSize:34,color:C.muted}}>Real tools. A shared conversation.</div>
  </Backdrop>;
};

// spotlight-hero-card: exact Gallery style, adapted to a real hero-region crop.
export const Party:React.FC<SceneProps>=({headline=HEADLINES.party})=>{
  const f=useCurrentFrame(),r=layout.party.hero,cx=r.x+r.w/2,cy=r.y+r.h/2;
  const rise=interpolate(f,[b(4),b(5)],[0,1],{...clamp,easing:Easing.bezier(.2,1.25,.3,1)});
  const reseat=interpolate(f,[b(9),b(11)],[0,1],{...clamp,easing:Easing.bezier(.4,0,.3,1.05)});
  const lift=rise*(1-reseat),z=110*lift+Math.sin((f-b(5))/80*Math.PI*2)*4*lift;
  const light=ramp(f,b(2),b(2));
  const lap=f<b(7)?ramp(f,b(5),b(1)):ramp(f,b(7),b(2));
  const beam=(f>=b(5)&&f<=b(6))||(f>=b(7)&&f<=b(9));
  const press=interpolate(f,[b(11)-8,b(11)-2,b(11)],[1,.997,1],clamp);
  const note=ramp(f,b(5),b(1));
  const keys=[{frame:0,cx:960,cy:540,zoom:.9},{frame:b(2),cx:960,cy:540,zoom:.9},{frame:b(4),cx:cx-105,cy:cy-10,zoom:2.6,rx:8,ry:34,rz:2},{frame:b(14),cx:cx-105,cy:cy-10,zoom:2.6,rx:8,ry:34,rz:2}];
  return <Backdrop>
    <Camera src="party-full" keys={keys}>
      <svg width={1920} height={1080} style={{position:'absolute',transform:'translateZ(1px)',opacity:light}}>
        <defs><filter id="hero-soft"><feGaussianBlur stdDeviation="22"/></filter><mask id="hero-hole"><rect width="1920" height="1080" fill="white"/><rect x={r.x-14} y={r.y-14} width={r.w+28} height={r.h+28} fill="black" filter="url(#hero-soft)"/></mask></defs>
        <rect width="1920" height="1080" fill={C.bg} fillOpacity=".94" mask="url(#hero-hole)"/>
      </svg>
      {lift>.01&&<div style={{position:'absolute',left:r.x,top:r.y,width:r.w,height:r.h,background:C.paper,border:`1px solid ${C.gold}`,transform:'translateZ(1.5px)'}}/>}
      <div style={{position:'absolute',left:r.x,top:r.y,width:r.w,height:r.h,transform:`translateZ(${z+2}px) scale(${press})`,boxShadow:`${-10*lift}px ${10*lift}px ${12+12*lift}px #0007,${-36*lift}px ${48*lift}px ${90*lift}px #0007`,borderRadius:3}}>
        <Texture name="hero-hires" style={{width:'100%',height:'100%',borderRadius:3}}/>
        <div style={{position:'absolute',inset:0,border:`1px solid ${C.gold}`,borderRadius:3,opacity:light}}/>
        {beam&&<svg width={r.w} height={r.h} style={{position:'absolute',inset:0,overflow:'hidden',borderRadius:3,opacity:f<b(7)?1:.62}}><rect x="2" y="2" width={r.w-4} height={r.h-4} rx="3" fill="none" stroke={C.gold} strokeWidth={f<b(7)?5:3.5} pathLength="1" strokeDasharray=".16 1" strokeDashoffset={-lap}/><rect x="2" y="2" width={r.w-4} height={r.h-4} rx="3" fill="none" stroke="#fff8e7" strokeWidth={f<b(7)?2.5:1.75} pathLength="1" strokeDasharray=".16 1" strokeDashoffset={-lap}/></svg>}
      </div>
      <div style={{position:'absolute',left:r.x-250,top:r.y-8,width:225,padding:12,background:C.bg,opacity:note,transform:`translateZ(${4+88*(1-reseat)}px) translateY(${(1-note)*26}px)`,color:C.text}}>
        <Head style={{fontSize:42,letterSpacing:-1}}>{headline}</Head><div style={{fontFamily:mono,fontSize:15,color:C.gold,marginTop:14}}>FIRESTORE HEROES</div>
      </div>
    </Camera>
    <AbsoluteFill style={{pointerEvents:'none',opacity:1-light,background:`radial-gradient(420px 330px at ${interpolate(f,[0,b(1),b(2)],[24,72,43],clamp)}% ${interpolate(f,[0,b(1),b(2)],[30,42,46],clamp)}%,transparent 22%,#161914ee 100%)`}}/>
    <div style={{position:'absolute',right:100,top:-300,width:360,height:1000,transform:'rotate(28deg)',background:'linear-gradient(#fff0da17,transparent)',filter:'blur(35px)',opacity:.25*(1-light*.45)}}/>
  </Backdrop>;
};

export const Dice:React.FC<SceneProps>=({headline=HEADLINES.dice})=>{
  const f=useCurrentFrame(),roll=evidence.dice.rolls[0],modifier=evidence.dice.modifier,total=evidence.dice.total;
  return <Backdrop>
    <Label style={{position:'absolute',left:100,top:100}}>ROLL INITIATIVE</Label>
    <Head style={{position:'absolute',left:100,top:205,fontSize:100}}>{headline}</Head>
    <div style={{position:'absolute',left:110,top:430,display:'flex',alignItems:'center',gap:36,fontFamily:serif,fontSize:180,color:C.gold}}>
      {[String(roll),`+ ${modifier}`,'=',String(total)].map((value,i)=><div key={i} style={{opacity:ramp(f,b(i),b(1)),transform:`translateY(${(1-ramp(f,b(i),b(1)))*60}px)`}}>{value}</div>)}
    </div>
    <div style={{position:'absolute',left:1060,top:440,width:650,transform:`perspective(1200px) rotateY(${(1-ramp(f,b(2),b(2)))*-22}deg) translateY(${(1-ramp(f,b(2),b(2)))*120}px)`,opacity:ramp(f,b(2),b(1)),boxShadow:'-25px 40px 80px #0007'}}><Texture name="dice-panel" style={{width:'100%'}}/></div>
    <div style={{position:'absolute',left:110,top:830,fontFamily:mono,fontSize:34,color:C.muted}}>Actual tool roll · no scripted critical</div>
  </Backdrop>;
};

// row-embed: real screenshot strips land in their exact original slots.
export const Bestiary:React.FC<SceneProps>=({headline=HEADLINES.bestiary})=>{
  const f=useCurrentFrame(),rows=[0,1,5,6].map(i=>layout.bestiary.rows[i]);
  const lands=[b(2),b(5),b(7),b(8)];
  return <Backdrop>
    <Camera src="bestiary-full" keys={[{frame:0,cx:980,cy:455,zoom:1.6},{frame:b(9),cx:980,cy:460,zoom:2.1},{frame:b(12),cx:980,cy:460,zoom:2.1}]}>
      {rows.map((r,i)=>{
        const land=lands[i],cue=land-24;
        const p=interpolate(f,[cue,land],[0,1],{...clamp,easing:Easing.bezier(.5,0,.8,.75)}),air=1-p;
        const patch=1-ramp(f,land,4),scale=f<land?1.06-.065*p:interpolate(f,[land,land+8],[.995,1],clamp);
        const seam=f>=land&&f<land+16;
        return <React.Fragment key={i}>
          {patch>0&&<div style={{position:'absolute',left:r.x-2,top:r.y-2,width:r.w+4,height:r.h+4,background:C.paper,opacity:patch,border:'1px dashed #302b2322'}}/>}
          {f>=cue&&f<land+8&&<div style={{position:'absolute',left:r.x,top:r.y,width:r.w,height:r.h,opacity:ramp(f,cue,6),transform:`perspective(900px) translateY(${-120*air}px) rotateX(${16*air}deg) scale(${scale})`,backgroundImage:`url(${staticFile('textures/bestiary-full.png')})`,backgroundSize:'1920px 1080px',backgroundPosition:`-${r.x}px -${r.y}px`,boxShadow:`0 ${34*air}px ${64*air}px #0005`,filter:f<land?`blur(${Math.min(1.6,air*1.4)}px)`:'none'}}/>}
          {seam&&<div style={{position:'absolute',left:r.x,top:r.y+r.h-2,width:r.w,height:2,overflow:'hidden'}}><div style={{height:2,width:'100%',background:`linear-gradient(90deg,transparent,${C.gold},transparent)`,opacity:1-ramp(f,land+4,12),transform:`scaleX(${ramp(f,land,10)})`}}/></div>}
        </React.Fragment>;
      })}
    </Camera>
    <div style={{position:'absolute',left:100,right:100,bottom:95,background:C.bg,padding:'30px 35px',borderLeft:`2px solid ${C.gold}`}}><Head style={{fontSize:86}}>{headline}</Head><div style={{fontSize:34,color:C.muted,marginTop:18}}>Live D&amp;D 5e bestiary data</div></div>
  </Backdrop>;
};

const verifiedOutput=evidence.combat.output;
const percentage=Number(verifiedOutput.match(/Win Percentage:\s*([\d.]+)/)?.[1]);
const trials=Number(verifiedOutput.match(/Trials:\s*(\d+)/)?.[1]);
const wins=Number(verifiedOutput.match(/Wins:\s*(\d+)/)?.[1]);
export const Combat:React.FC<SceneProps>=({headline=HEADLINES.combat})=>{
  const f=useCurrentFrame(),p=ramp(f,b(1),b(3)),counter=Math.round(percentage*p);
  return <Backdrop>
    <Label style={{position:'absolute',left:100,top:100}}>THE ENCOUNTER LAB</Label>
    <Head style={{position:'absolute',left:100,top:200,fontSize:104}}>{headline}</Head>
    <div style={{position:'absolute',left:100,top:370,fontFamily:serif,fontSize:250,lineHeight:1,color:C.gold}}>{counter}<span style={{fontSize:110}}>%</span></div>
    <div style={{position:'absolute',left:110,top:650,fontSize:38,color:C.text}}>{wins.toLocaleString('en-US')} wins / {trials.toLocaleString('en-US')} trials</div>
    <div style={{position:'absolute',left:110,top:720,fontSize:34,color:C.muted}}>4 heroes versus 1 Owlbear</div>
    <div style={{position:'absolute',left:800,top:410,width:1010,opacity:ramp(f,b(1),b(1)),transform:`translateX(${(1-ramp(f,b(1),b(2)))*100}px)`,boxShadow:'-25px 35px 80px #0007'}}><Texture name="combat-card" style={{width:'100%'}}/></div>
    <div style={{position:'absolute',left:810,top:760,width:1000,fontSize:32,lineHeight:1.4,color:C.muted}}>Verbatim sandbox output.<br/>No final model summary was returned.</div>
    <div style={{position:'absolute',left:100,right:100,bottom:85,borderTop:`1px solid ${C.gold}55`,paddingTop:25,fontSize:34,lineHeight:1.35,color:C.text}}>Random targets · attacks scaled from hero stats · at most 100 rounds<br/><span style={{color:C.muted}}>Simplified combat simulation. This result is not a prediction.</span></div>
  </Backdrop>;
};

export const Portrait:React.FC<SceneProps>=({headline=HEADLINES.portrait})=>{
  const f=useCurrentFrame(),p=ramp(f,b(1),b(2));
  const motion=f>=b(7);
  return <Backdrop>
    <Label style={{position:'absolute',left:100,top:100}}>THE FORGE</Label>
    <Head style={{position:'absolute',left:100,top:300,width:motion?600:740,fontSize:motion?116:128}}>{motion?'Then set them in motion.':headline}</Head>
    <div style={{position:'absolute',left:100,top:720,fontSize:40,color:C.gold}}>Valen Ironclad</div>
    <div style={{position:'absolute',left:100,top:790,width:motion?580:650,fontSize:34,lineHeight:1.4,color:C.muted}}>{motion?'A real agent-generated video clip.':'A portrait generated by the agent during the verified conversation.'}</div>
    {!motion&&<div style={{position:'absolute',left:1000,top:100,width:820,height:840,clipPath:`inset(0 ${(1-p)*100}% 0 0)`,transform:`perspective(1500px) rotateY(${(1-p)*-14}deg)`,filter:'drop-shadow(-35px 50px 40px #0008)'}}><Texture name="portrait-frame" style={{width:'100%',height:'100%',objectFit:'contain'}}/></div>}
    <Sequence from={b(7)} durationInFrames={b(7)} premountFor={30}><Freeze frame={Math.min(Math.max(0,f-b(7)),178)}><Video src={staticFile('video/valen.mp4')} muted objectFit="contain" style={{position:'absolute',left:760,top:245,width:1060,height:596,border:`1px solid ${C.gold}88`,boxShadow:'-30px 40px 80px #0008'}}/></Freeze></Sequence>
  </Backdrop>;
};

export const Outro:React.FC<SceneProps>=({headline=HEADLINES.outro})=>{
  const f=useCurrentFrame(),arrive=ramp(f,b(2),b(2));
  const objects=[
    {name:'hero-hires',x:100,y:160,w:430,h:205,dx:-700,dy:-300,cue:0},
    {name:'die',x:1570,y:130,w:160,h:175,dx:650,dy:-400,cue:b(1)},
    {name:'bestiary-card',x:100,y:690,w:440,h:156,dx:-650,dy:450,cue:b(2)},
    {name:'portrait',x:1480,y:620,w:275,h:275,dx:600,dy:450,cue:b(2)},
  ];
  return <Backdrop>
    <Seal size={650} style={{position:'absolute',left:650,top:110,opacity:.11}}/>
    {objects.map((o,i)=>{
      const p=ramp(f,o.cue,b(4)-o.cue);
      return <div key={o.name} style={{position:'absolute',left:o.x,top:o.y,width:o.w,height:o.h,opacity:p*(1-.55*ramp(f,b(4),b(1))),transform:`translate(${o.dx*(1-p)}px,${o.dy*(1-p)}px) rotate(${(1-p)*(i%2?20:-20)}deg)`,filter:'drop-shadow(-12px 18px 25px #0008)'}}><Texture name={o.name} style={{width:'100%',height:'100%',objectFit:'contain'}}/></div>;
    })}
    <div style={{position:'absolute',left:350,top:350,width:1220,textAlign:'center',opacity:arrive,transform:`translateY(${(1-arrive)*90}px) scale(${1.06-.06*arrive})`}}>
      <Label>YOUR NEXT CAMPAIGN</Label><Head style={{fontSize:204,color:C.gold,marginTop:18}}>{headline}</Head>
      <div style={{fontSize:42,marginTop:35}}>ADK · Gemini · Firestore · A2UI</div>
    </div>
    <div style={{position:'absolute',left:100,right:100,bottom:130,textAlign:'center',fontSize:38,opacity:ramp(f,b(5),b(1))}}>github.com/mugnimaestra/realmforge-party-builder</div>
    <div style={{position:'absolute',bottom:55,left:0,right:0,textAlign:'center',opacity:ramp(f,b(5),b(1))}}><span style={{fontFamily:mono,fontSize:32,padding:'12px 20px',border:`1px solid ${C.gold}66`,color:C.muted}}>Build with Gemini · Gemini World Tour</span></div>
  </Backdrop>;
};

export const SCENES={chance:Chance,brand:Brand,table:Table,party:Party,dice:Dice,bestiary:Bestiary,combat:Combat,portrait:Portrait,outro:Outro};
