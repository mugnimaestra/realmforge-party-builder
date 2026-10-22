# Verification record — 2026-10-22

## Agent and frontend

- `uv run pytest tests/unit`: 18 passed. SDK experimental/deprecation warnings remain.
- Browser checks at 1440×1000 and 375×812: no horizontal overflow, visible focus,
  reduced motion, selected text contrast >=4.5:1, all supported A2UI components,
  real-roll rendering, safe text, HTTPS media, and empty-summary fallback passed.
- One production gate conversation passed all five real prompts before capture:
  party 14.0s, dice 6.4s, Goblin 6.9s, sandbox 13.8s, portrait 34.1s.
- A final run with the updated agent instructions passed all five again:
  party 260.6s, dice 8.5s, Goblin 10.0s, sandbox 20.9s, portrait 24.0s.
  Cloud latency remains variable. Waiting time in the reel is edited.
- Optional video generation succeeded; the actual 3.029s clip loaded in the
  frontend player. The renderer handles both MP4 text and a Video component.
- The movie freezes the original successful conversation: die 12 + 3 = 15;
  1000/1000 sandbox wins under the displayed simplified rules. Raw responses
  remain outside git. src/evidence.json contains the source hashes.

## Picture and timing

- 1920×1080, 60 fps, exactly 3000 frames / 50 seconds.
- Every scene boundary and impact target uses the 120 BPM whole-beat helper.
- Entrance/peak/hold stills were rendered, then frames were extracted from the
  encoded movie for inspection. Checks include actual portrait f2280 and video
  f2550, plus hero, bestiary, combat, title, and outro.
- Workbench parity: f150, f810, f1650, f2130, f2280, f2550, f2970 all matched.
  Reported difference pixels: 0.000%; worst individual channel difference: 1.
- Both deliveries use the same copied H.264 picture track. Its SHA-256 is
  `2f3f132aa480644fd80d6fb1b9c5abe2f446d54e163768c1acf6a4699c7d89ba`.
- README GIF: 12 seconds, 720×405, 12 fps, 2,131,451 bytes (<5 MB).

## Audio

Original deterministic score: 120 BPM, 48 kHz, beat zero at sample zero.
Normalized cinematic SFX retain exact source URLs and hashes in src/audio-manifest.json.
The two mixes come from the same Remotion composition, with `bgm:false` for the
SFX-only version. PCM is muxed to AAC with FFmpeg 8.1.1, including final silence
padding to 50 seconds. Native Remotion MP4 muxing showed a 2048-sample delay;
the delivered pipeline removes it without changing the source beat grid.

| Probe | Target frame | Measured output offset | Peak error |
| --- | ---: | ---: | ---: |
| Brand impact | 240 | 0.0000f | -0.2400f |
| Hero landing | 930 | 0.0000f | -0.3325f |
| Outro impact | 2700 | 0.0000f | -0.2400f |

The music's measured offset is 0.0000f. All probes are within the 3-frame limit.
Measurements use FFT cross-correlation against the original normalized sources.
Run `uv run --with numpy --with scipy python demo/scripts/check_audio.py` to repeat.
The mixed audio's peak is -5.5 dBFS; mean volume is -25.2 dBFS.

## Data and scope

- Public seeded heroes and real agent-generated media only.
- Visible capture text is checked for account, project, and cloud asset addresses.
- Credential scan found no student account, OAuth credential, access token, API
  key, or tracked environment file. Personal ADC still matches its backup.
- No deployment was performed. The deployed runtime is not revalidated by these
  local checks. Agent model and project IDs remain unchanged.
- Anonymous A2A chapters skip Memory Bank; stable playground users retain it.
- Gemini can return an empty final summary after a successful sandbox call.
  The frontend shows the verbatim verified result and discloses that case.

The [independent review](REVIEW.md) found no required fixes. It used rendered
frames and programmatic audio analysis; subjective listening and continuous
real-time playback were outside its capability.
