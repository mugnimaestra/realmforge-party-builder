export const FPS = 60;
export const BPM = 120;
export const b = (n: number) => Math.round(n * FPS * 60 / BPM);
export const TOTAL = b(100);
export const SHOTS = [
  {id:'chance',label:'Your next move',from:b(0),duration:b(6)},
  {id:'brand',label:'RealmForge',from:b(6),duration:b(6)},
  {id:'table',label:'One table',from:b(12),duration:b(8)},
  {id:'party',label:'The party ledger',from:b(20),duration:b(14)},
  {id:'dice',label:'Roll initiative',from:b(34),duration:b(10)},
  {id:'bestiary',label:'Know what you face',from:b(44),duration:b(12)},
  {id:'combat',label:'Test the encounter',from:b(56),duration:b(16)},
  {id:'portrait',label:'Forge a portrait',from:b(72),duration:b(14)},
  {id:'outro',label:'Build with Gemini',from:b(86),duration:b(14)},
] as const;
export const SFX = [
  {from:b(2),src:'impact',volume:.42,duration:b(4),action:'die lands'},
  {from:b(8),src:'impact',volume:.55,duration:b(4),action:'wordmark lands'},
  {from:b(12),src:'sweep',volume:.25,duration:b(2),action:'table reveal'},
  {from:b(24),src:'sweep',volume:.24,duration:b(2),action:'hero lifts'},
  {from:b(25),src:'shimmer',volume:.18,duration:b(3),action:'hero contour lap'},
  {from:b(31),src:'paper',volume:.35,duration:b(2),action:'hero reseats'},
  {from:b(36),src:'paper',volume:.3,duration:b(2),action:'roll panel resolves'},
  {from:b(44),src:'paper',volume:.3,duration:b(2),action:'bestiary page'},
  {from:b(60),src:'impact',volume:.25,duration:b(3),action:'verified win percentage'},
  {from:b(74),src:'shimmer',volume:.26,duration:b(4),action:'portrait reveal'},
  {from:b(79),src:'paper',volume:.24,duration:b(2),action:'generated video cut'},
  {from:b(90),src:'impact',volume:.65,duration:b(4),action:'launch wordmark'},
  {from:b(92),src:'shimmer',volume:.23,duration:b(4),action:'launch afterglow'},
];
