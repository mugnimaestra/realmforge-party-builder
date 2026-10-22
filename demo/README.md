# RealmForge demo source

50 seconds · 1920 × 1080 · 60 fps · 120 BPM. Remotion is the only video engine.
The cut combines video-shotcraft screenshot camera work with the motion-reel
reference's whole-beat timing and kinetic typography.

## Rebuild

Requires Node 22+, FFmpeg, and network access for the first asset preparation.

```bash
cd demo
npm ci
npm run audio
npm run check
npm run render
npm run render:nobgm
```

The main render goes to `docs/demo.mp4`. The same timeline with `bgm:false`
goes to `docs/demo-nobgm.mp4`; it retains the sound effects. Both use the
original score and licensed SFX prepared from the source/provenance manifest.
The generated Valen clip is a real source asset, not an edited render of this reel.

The render script produces a shared picture track and separate Remotion PCM
mixes, then muxes AAC with FFmpeg. This keeps both versions' pictures identical
and avoids the native MP4 mux's measured 2048-sample audio priming offset.

`npm run studio` opens the Remotion editor. `src/workbench.ts` exposes the same
shot and audio tables to video-shotcraft's visual workbench. Headline props are
editable; camera timings and the beat grid stay fixed.

## Evidence and capture

`src/evidence.json` records real tool calls, actual dice and sandbox output, inline
video playback, and image/video hashes. The raw responses contain public cloud
asset URLs and remain in ignored `.local-demo/`; they are not committed.

To collect new real responses, first run the agent and frontend as described in
the repository README, then:

```bash
uv run --with patchright python scripts/check_live_agent.py
uv run --with patchright python demo/capture.py
```

The optional video response must exist at `.local-demo/video-result.json` to
recapture that segment. Capture replays frozen real responses through the actual
renderer, waits for fonts/images/video, and rejects sensitive visible text.
It captures 2× page textures, a 4× hero region, an 8× die, element coordinates,
and before/after screenshots. It does not generate fixture product data.

`DESIGN.md` contains the brief, visual tokens, decisions, shot-card mapping,
storyboard, and limits. `ATTRIBUTION.md` lists source licenses. `scripts/stills.mjs`
renders the planned entrance, peak, and hold frames for visual review.

The 100% encounter result means 1,000 wins in the printed simplified simulation,
not a universal game balance claim. Gemini returned no final summary after the
successful code execution; the frontend and reel show the verified output and
disclose that limitation. Waiting time is edited. Anonymous A2A cross-session
memory is not shown or claimed.
