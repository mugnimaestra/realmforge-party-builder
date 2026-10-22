# RealmForge — Your next move

Mode: video-shotcraft autonomous free creation. One Remotion engine. The
hyperframes-motion-reel reference supplies the showreel direction, kinetic
type, and whole-beat grid; no HyperFrames segment is needed.

## Product brief and evidence

An RPG companion for game masters: persistent hero sheets, real dice, live
bestiary lookup, sandbox encounter trials, and generated portraits. The audience
is a hackathon reviewer who needs to see the agent perform useful work.

Production gate passed on 2026-10-22: all five prompts in one frontend
conversation. Party 14.0s; dice 6.4s; Goblin 6.9s; combat 13.8s; portrait 34.1s.
Each used its actual tool. Combat returned successful sandbox output but an empty
model summary; the frontend shows the verbatim verified result and says so.
The movie edits waiting time and uses frozen responses from that conversation.
It is a feature reel, not a claim about response speed.

The four heroes are the public example records in scripts/seed_firestore.py.
No personal or customer data is used. Only frontend content is captured: no
browser chrome, account, project ID, bucket URL, lab page, or console.

## Requirements to execution

| Requirement | Decision |
| --- | --- |
| Working agent | Gate before capture; real results frozen, never invented |
| Dark fantasy | Ink, moss, parchment, gold; native frontend typography |
| Shotcraft + motion reel | Tactile screenshot camera work plus bold masked type |
| 45–60 seconds | 50 seconds, 100 beats, 3000 frames |
| 120 BPM / 60 fps / 1080p | b(n) = n × 30; boundaries and impacts on whole beats |
| Cold open | Actual d20 result; no forced natural 20 |
| Memory | Omitted; anonymous A2A contexts cannot recall across chapters |
| Combat | Actual trials and percentage, with simplified assumptions visible |
| Portrait | Actual generated portrait, fully loaded before capture |
| Optional clip | Generation succeeded; real Valen animation follows the portrait |
| Audio | Original deterministic electronic score at exactly 120 BPM; cinematic SFX |
| Editable source | One timeline table, props, workbench manifest, pinned dependencies |
| Honest limitations | Empty post-sandbox model summary disclosed; no memory or identity-consistency claim |

## Visual direction

Considered: a parchment manuscript film, a tavern tabletop film, and a dark
product launch. Selected the dark tabletop launch: it retains the frontend's
field-guide identity while giving screenshots depth and clear reading holds.
Manuscript-only would hide the product; tavern props would compete with the UI.

Tokens from frontend/static/index.html:

- Background #161914; surface #20271f; gold #d7b775; parchment #eee2c4;
  ink #302b23; body #eee6d5; secondary #bcb5a2.
- Display Cormorant Garamond 600/700; body Source Sans 3; labels IBM Plex Mono.
- Square paper edges, 3–5px UI radii, thin gold rules. No purple gradient.
- Frame margins 100px, 12-column alignment, generous negative space.
- Narrative type 64–100px; supporting type 32–40px, with a 32px minimum. UI microtext is texture;
  the important claim is repeated at readable size as an editorial annotation.
- Motion: deliberate, weighted, decisive. Ease(.35,0,.2,1) for camera;
  rise(.2,1.25,.3,1); no shake; locked camera after the main move.
- Brand holds exceed one second. At most two full-frame impact moments, more
  than 16 beats apart. Other beat accents affect individual elements only.

Styleframe: styleframe.html, three static frames, checked before implementation.
Screen captures follow this final storyboard. No recreated product UI.

## Function to shot mapping

| Function | Motion | Source / reference |
| --- | --- | --- |
| Dice cold open | One tactile die drops, rotates, settles | Real .die cutout; original motion |
| Brand | Serif wordmark revealed through letter masks | Motion-reel kinetic typography |
| Product context | Real table pulls into view | Welcome screenshot; original camera |
| Party | Spotlight, lift, two contour laps, reseat | spotlight-hero-card, exact same style key |
| Dice arithmetic | Die cutout resolves into the real roll panel | Real screenshot; original match cut |
| Bestiary | Rows drop into their original screenshot slots | row-embed, exact same style key |
| Encounter | Verified output beside a percentage counter | Actual sandbox result; original motion |
| Portrait | Framed image with a restrained lateral reveal | Actual generated image and frontend frame |
| Outro | Feature cutouts assemble around kinetic wordmark | Original launch composition |

Gallery index: video-shotcraft/gallery/api/library.json.
Exact demos read: demos/opening/spotlight-hero-card/SpotlightHeroCard.tsx and
demos/ui-entrance/row-embed/RowEmbed.tsx. Gallery references are the matching
gallery/media/<style-key>.mp4. Adaptation keeps the action arcs and easing;
timings scale to 60fps and land on beats. Large UI crops require a smaller
camera zoom than the reference's small cards. Row impacts use decreasing
whole-beat intervals. PageCam's layout zoom math is retained for sharp text.

## Final storyboard and frame budget

| # | Time / beats | Shot | Main action / copy / transition / sound |
| --- | --- | --- | --- |
| 1 | 0–3s / b0–6 | Chance | Real die tumbles then holds; “Your next move.”; physical impact at b2 |
| 2 | 3–6s / b6–12 | RealmForge | Kinetic serif brand reveal, >1s hold; cinematic hit at b8 |
| 3 | 6–10s / b12–20 | One table | “Heroes. Dice. Encounters.”; welcome screenshot enters and holds; soft sweep |
| 4 | 10–17s / b20–34 | Party ledger | Spotlight finds one real hero region, lifts, scans twice, reseats; “Meet your party.”; restrained whoosh/contour/landing |
| 5 | 17–22s / b34–44 | Roll initiative | Real die and modifier resolve into actual result panel; “Every modifier counts.”; paper movement |
| 6 | 22–28s / b44–56 | Bestiary | Real Goblin rows land in real slots; “Know what you face.”; one page-turn sound |
| 7 | 28–36s / b56–72 | Test encounter | Actual output + counter reaches actual percentage; “Test the encounter.”; 1000 trials / simplified rules, not a forecast; low impact |
| 8 | 36–43s / b72–86 | Forge | Actual portrait in its frontend frame; “Give your hero a face.”; warm reveal and hold; at b79 cut to real generated video, “Then set them in motion.” |
| 9 | 43–50s / b86–100 | Launch | Features assemble around RealmForge; ADK · Gemini · Firestore · A2UI; repository URL and small Build with Gemini / Gemini World Tour badge; rise → impact b90 → shimmer; >1s hold |

No simulated clicking or sped-up typing. Capture scripts replay the verified
responses through the actual renderer. All displayed numbers come from the
gate manifest. The final compositor is frame-driven and deterministic.

Storyboard revision: the separate optional video tool check succeeded after the
five-turn gate. Its actual clip and inline playback check are added within the
existing forge shot budget. No generation-speed or portrait-to-video identity
consistency claim is made. The clip has its own source hash in evidence.json.

Review note: the roll metadata, sandbox-summary note, and event badge use 32px
type. This is the Q11 supporting-text minimum and keeps the event badge small;
the 480px preview check found these readable. Other supporting lines use 34–42px.

## QA plan

Two stills per shot plus entrance/peak/hold contact sheets; 480px preview check;
full render with music and a same-timeline no-music version retaining SFX.
Measure output peaks and audio offsets; whole-beat cut errors <=3 frames.
Independent clean-context review uses final-review.md and aesthetic-rules.md.
Report any unverifiable reference or audio issue rather than marking it passed.
