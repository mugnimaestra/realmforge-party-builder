"""Measure rendered AAC alignment against three original SFX waveforms.

uv run --with numpy --with scipy python demo/scripts/check_audio.py
"""

import json
import subprocess
from pathlib import Path

import numpy as np
from scipy.signal import correlate

ROOT = Path(__file__).resolve().parents[1]
SR = 48000
FPS = 60


def pcm(path):
    data = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(data, dtype="<f4")


def main():
    manifest = json.loads((ROOT / "src/audio-manifest.json").read_text())
    audio = pcm(ROOT.parent / "docs/demo-nobgm.mp4")
    rows = []
    for name, beat in [("impact", 8), ("paper", 31), ("impact", 90)]:
        source = next(s for s in manifest["sfx"] if s["name"] == name)
        original = pcm(ROOT / f"public/audio/{name}.wav")
        target = beat / 2
        intended_start = target - round(source["peakSeconds"] * FPS) / FPS
        start = int((intended_start - .25) * SR)
        stop = int((intended_start + len(original) / SR + .25) * SR)
        window = audio[start:stop]
        cross = correlate(window, original, mode="valid", method="fft")
        actual_start = (start + int(np.argmax(cross))) / SR
        peak_error = (actual_start + source["peakSeconds"] - target) * FPS
        offset = (actual_start - intended_start) * FPS
        rows.append({"sound": name, "beat": beat, "targetFrame": beat * 30, "outputOffsetFrames": round(offset, 4), "peakErrorFrames": round(peak_error, 4)})
    report = {"pipeline": "Remotion 4.0.484 PCM mix / FFmpeg 8.1.1 AAC 48kHz / H.264 MP4", "date": "2026-10-22", "method": "FFT cross-correlation of no-BGM rendered audio with original normalized SFX", "measurements": rows}
    score = pcm(ROOT / "public/audio/score.wav")[: SR * 10]
    mixed = pcm(ROOT.parent / "docs/demo.mp4")[: SR * 10]
    cross = correlate(mixed, score, mode="full", method="fft")
    center = len(score) - 1
    radius = SR // 10
    lag = int(np.argmax(cross[center - radius : center + radius + 1])) - radius
    report["scoreOffsetFrames"] = round(lag / SR * FPS, 4)
    (ROOT / "out/audio-alignment.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    assert all(abs(row["peakErrorFrames"]) <= 3 for row in rows)
    assert abs(report["scoreOffsetFrames"]) <= 3


if __name__ == "__main__":
    main()
