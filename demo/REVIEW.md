# Independent review — 2026-10-22

A separate clean-context DevSpace reviewer inspected the brief, tokens,
storyboard, Gallery index, exact shot-card demo sources, reference clips,
source code, captured assets, rendered frames, and both final MP4s.

The review found no required fixes. It used frame extraction and programmatic
audio analysis. It did not hear playback or watch continuous 60fps playback;
subjective sound balance and real-time viewing remain outside that review's
capability. Those limits qualify the results below.

| Area | Evidence and result |
| --- | --- |
| Product goals P1–P4 | Actual party, dice, bestiary, sandbox, portrait, and video capabilities match the brief. No memory recall or forced critical-roll claim. |
| Features F1–F3 | Distinct shots show each required operation; metadata and UI states explain the functions. |
| Visual direction V1–V4 | Frontend palette, serif/body/mono families, parchment edges, and weighted motion remain consistent. |
| Shot references S1–S6 | Spotlight/lift/two contour laps/reseat and row-slot landings retain the selected Gallery motion grammar. High-resolution real cutouts and layout zoom preserve detail. |
| Storyboard B1–B4 | Nine shots span 100 beats / 3000 frames. Brand holds exceed one second, and feature arrivals leave reading time. |
| Data D1–D5 | Public seed data and verified generated media; hashes match. No credentials, project identifiers, storage URLs, or personal accounts were found in the inspected frames. |
| Visual quality Q | Entrance, peak, and hold frames were inspected, including 480px previews. Headlines and supporting labels remain readable. No required composition or masking defect was reported. |
| Audio direction A1/A7 | Original 120-BPM score and attributed cinematic SFX were verified from sources and waveforms. Subjective tonal quality was not assessed by listening. |
| Sync A2/A3/A9 | Current PCM-to-AAC pipeline measures zero output/music offset. Impact peak errors are -0.2400f, -0.3325f, and -0.2400f, below the 3-frame limit. |
| Ending A4 | Riser, impact at f2700, and shimmer at f2760 follow the planned sequence. |
| Sample management A5 | Explicit clip durations; source SFX are under five seconds and end within the film. |
| Signal A6 | Full mix sample peak -5.5 dBFS; SFX-only peak -7.0 dBFS. Nonzero SFX signal and no sample clipping were confirmed. Perceptual audibility was not established through listening. |
| Dual delivery A8 | Both files are 50.000000 seconds, 3000 frames at 60fps. Video bitstreams have identical MD5 `5e0002462999338cb2a2f2c1a0cd1803`. |

The reviewer ran ffprobe, FFmpeg bitstream and volume checks, the FFT alignment
script, and TypeScript validation, and inspected workbench parity evidence.
Seven checked workbench frames matched at the parity threshold (0.000%
different pixels, maximum individual channel difference 1).

Review follow-ups:

- The initial native-MP4 audio offset was corrected by the delivered PCM/AAC mux
  pipeline. The source beat grid stays unchanged.
- The three 32px metadata lines meet Q11's supporting-text minimum. DESIGN.md
  explicitly records that range and the 480px readability check.
- `Video.objectFit` is passed directly to the media component. A still at f2550
  is pixel-identical before and after this API cleanup.
- All source and duration-padding changes are included in the branch.

Checked hold intervals, corrected from the reviewer's shot-duration shorthand:
the opening wordmark is settled for at least f240–359 (2 seconds), and the
closing wordmark for f2700–2999 (5 seconds). The full shot durations are 3 and
7 seconds respectively. The volume figures above are sample peaks, not a
separate oversampled true-peak measurement.
