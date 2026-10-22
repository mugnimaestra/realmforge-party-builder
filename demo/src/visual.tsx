import React,{useEffect,useState} from 'react';
import {AbsoluteFill,Easing,Img,cancelRender,continueRender,delayRender,interpolate,staticFile,useCurrentFrame} from 'remotion';
import fontData from '../public/fonts/font-data.json';

let fontsReady:Promise<FontFace[]>|undefined;
function useTypography(){
  const [handle]=useState(()=>delayRender('RealmForge bundled typography'));
  useEffect(()=>{
    fontsReady??=Promise.all([
      ['Cormorant Garamond',fontData.CormorantGaramond,'500 700'],
      ['Source Sans 3',fontData.SourceSans3,'400 700'],
      ['IBM Plex Mono',fontData.IBMPlexMono,'400'],
    ].map(([family,data,weight])=>new FontFace(family,Uint8Array.from(atob(data),c=>c.charCodeAt(0)),{weight}).load()));
    fontsReady.then(fonts=>{fonts.forEach(font=>document.fonts.add(font));continueRender(handle)}).catch(cancelRender);
  },[handle]);
}
export const C={bg:'#161914',surface:'#20271f',gold:'#d7b775',paper:'#eee2c4',ink:'#302b23',text:'#eee6d5',muted:'#bcb5a2'};
export const serif='Cormorant Garamond, Georgia, serif';
export const sans='Source Sans 3, sans-serif';
export const mono='IBM Plex Mono, monospace';
export const clamp={extrapolateLeft:'clamp',extrapolateRight:'clamp'} as const;
export const ease=Easing.bezier(.35,0,.2,1);
export const ramp=(f:number,start:number,duration:number)=>interpolate(f,[start,start+duration],[0,1],{...clamp,easing:ease});
export const Texture:React.FC<{name:string;style?:React.CSSProperties}>=({name,style})=><Img src={staticFile(`textures/${name}.png`)} style={{display:'block',...(name==='die'?{clipPath:'polygon(50% 0,96% 25%,96% 75%,50% 100%,4% 75%,4% 25%)'}:{}),...style}}/>;
export const Backdrop:React.FC<{children?:React.ReactNode}>=({children})=>{useTypography();return <AbsoluteFill style={{background:`radial-gradient(ellipse at 70% 25%,#34422c,${C.bg} 67%)`,color:C.text,fontFamily:sans,overflow:'hidden'}}>
  <AbsoluteFill style={{opacity:.045,backgroundImage:'url("data:image/svg+xml,%3Csvg viewBox=\'0 0 180 180\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cfilter id=\'n\'%3E%3CfeTurbulence type=\'fractalNoise\' baseFrequency=\'.8\' numOctaves=\'3\' seed=\'7\'/%3E%3C/filter%3E%3Crect width=\'100%25\' height=\'100%25\' opacity=\'.8\' filter=\'url(%23n)\'/%3E%3C/svg%3E")'}}/>
  {children}
</AbsoluteFill>};
export const Label:React.FC<{children:React.ReactNode;style?:React.CSSProperties}>=({children,style})=><div style={{fontFamily:mono,fontSize:34,letterSpacing:4,color:C.gold,textTransform:'uppercase',...style}}>{children}</div>;
export const Head:React.FC<{children:React.ReactNode;style?:React.CSSProperties}>=({children,style})=><div style={{fontFamily:serif,fontSize:112,fontWeight:600,lineHeight:.97,letterSpacing:-3,...style}}>{children}</div>;
export const Seal:React.FC<{size?:number;style?:React.CSSProperties}>=({size=400,style})=><svg width={size} height={size*1.1} viewBox="0 0 100 110" fill="none" stroke="currentColor" strokeWidth=".6" style={{color:C.gold,...style}}><path d="M50 3 96 28 96 82 50 107 4 82 4 28Z M50 3 25 68 75 68Z M4 28 25 68 4 82 M96 28 75 68 96 82 M25 68 50 107 75 68 M4 28 96 28"/></svg>;

export type Key={frame:number;cx:number;cy:number;zoom:number;rx?:number;ry?:number;rz?:number};
// Adapted from video-shotcraft PageCam. Layout-level zoom avoids blurry GPU upscaling.
export const Camera:React.FC<{src:string;keys:Key[];children?:React.ReactNode;frame?:number}>=({src,keys,children,frame:override})=>{
  const own=useCurrentFrame(),f=override??own;
  let a=keys[0],z=keys[keys.length-1];
  for(let i=0;i<keys.length-1;i++)if(f>=keys[i].frame&&f<=keys[i+1].frame){a=keys[i];z=keys[i+1];break;}
  const t=ramp(f,a.frame,Math.max(1,z.frame-a.frame));
  const mix=(x:number|undefined,y:number|undefined)=>(x??0)+((y??0)-(x??0))*t;
  const cx=mix(a.cx,z.cx),cy=mix(a.cy,z.cy),zoom=mix(a.zoom,z.zoom);
  return <AbsoluteFill style={{overflow:'hidden',background:C.bg,perspective:1200*zoom,perspectiveOrigin:'960px 540px'}}>
    <div style={{position:'absolute',width:1920,height:1080,zoom,transformOrigin:`${cx}px ${cy}px`,transformStyle:'preserve-3d',transform:`translate(${960/zoom-cx}px,${540/zoom-cy}px) rotateY(${mix(a.ry,z.ry)}deg) rotateX(${mix(a.rx,z.rx)}deg) rotateZ(${mix(a.rz,z.rz)}deg)`}}>
      <Texture name={src} style={{position:'absolute',width:1920,height:1080}}/>{children}
    </div>
  </AbsoluteFill>;
};
