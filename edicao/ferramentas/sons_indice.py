#!/usr/bin/env python3
"""Índice da biblioteca de sons: duração útil (sem silêncio inicial), tempo até o pico, forma.
Uso: sons_indice.py → edicao/sons/indice.json"""
import json, numpy as np, soundfile as sf
from pathlib import Path
RAIZ = Path(__file__).resolve().parent.parent / "sons"
def main():
    idx = {}
    for f in sorted(RAIZ.rglob("*.wav")):
        if "entrada" in f.parts: continue
        x, sr = sf.read(f); m = np.abs(x).max(1) if x.ndim > 1 else np.abs(x)
        lim = m.max() * 10**(-40/20); ini = int(np.argmax(m > lim))
        env = np.convolve(m, np.ones(int(sr*0.005))/int(sr*0.005), "same")
        pk = int(np.argmax(env))
        forma = "ataque_seco" if (pk - ini)/sr < 0.03 else "crescendo"
        idx[str(f.relative_to(RAIZ))] = {"categoria": f.parent.name, "inicio_util": round(ini/sr, 4),
            "duracao_util": round((len(m)-ini)/sr, 3), "pico": round((pk-ini)/sr, 4), "forma": forma}
    (RAIZ / "indice.json").write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in idx.items(): print(k, v)
if __name__ == "__main__":
    main()
