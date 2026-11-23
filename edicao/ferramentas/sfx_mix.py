#!/usr/bin/env python3
"""Efeitos sonoros num vídeo SEM voz (animação pura): posiciona os sons do plano e mixa.
Uso: sfx_mix.py <video.mp4> <plano.json> <saida.mp4> [--lufs -18]
plano: {"itens":[{"id","arquivo","t","alinha":"pico|inicio","db": pico em dBFS do som}]}. Normaliza o total (loudnorm 2 passadas)."""
import json, subprocess, sys
from pathlib import Path
import numpy as np, soundfile as sf
SR = 48000; SONS = Path(__file__).resolve().parent.parent / "sons"

def main(video, plano, saida, *a):
    alvo = float(a[a.index("--lufs") + 1]) if "--lufs" in a else -18.0
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video], capture_output=True, text=True).stdout)
    mix = np.zeros((int(dur * SR) + SR, 2), np.float32)
    idx = json.loads((SONS / "indice.json").read_text())
    for it in json.loads(Path(plano).read_text())["itens"]:
        x, sr = sf.read(SONS / it["arquivo"], dtype="float32")
        if x.ndim == 1: x = np.stack([x, x], 1)
        m = idx[it["arquivo"]]; x = x[int(m["inicio_util"] * sr):]
        ini = it["t"] - (m["pico"] if it.get("alinha") == "pico" else 0)
        x = x * (10 ** (it["db"] / 20) / (np.abs(x).max() + 1e-9))
        k = max(0, int(round(ini * SR))); x = x[max(0, -int(round(ini * SR))):]
        mix[k:k + len(x)] += x[:len(mix) - k]
    mix = mix[:int(dur * SR)]
    tmp = Path(saida).with_suffix(".mix.wav"); sf.write(tmp, mix, SR, subtype="FLOAT")
    j = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(tmp), "-af", f"loudnorm=I={alvo}:TP=-1:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    j = json.loads(j[j.rindex("{"):j.rindex("}") + 1])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", str(tmp), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
        "-af", f"loudnorm=I={alvo}:TP=-1:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true",
        "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-movflags", "+faststart", "-shortest", saida], check=True)
    tmp.unlink(); print(saida)

if __name__ == "__main__":
    main(*sys.argv[1:])
