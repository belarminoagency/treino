#!/usr/bin/env python3
"""Inventário dos brutos + cópia de trabalho CFR (e espelhada, se pedido) + WAVs.
Uso: inventario.py <pasta_do_video>
Grava o bloco `midia` no estado. Cópias em _CLAUDE/midia/ (fora do git)."""
import json, subprocess, sys
from fractions import Fraction
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import estado

def probe(f):
    o = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=index,codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate,sample_rate,channels:stream_side_data=rotation",
        "-of", "json", str(f)], capture_output=True, text=True, check=True)
    return json.loads(o.stdout)

def main(pasta):
    pasta = Path(pasta); d = estado.ler(pasta)
    out = pasta / "_CLAUDE" / "midia"; out.mkdir(parents=True, exist_ok=True)
    itens, alertas, taxas = [], [], []
    for b in d["brutos"]:
        f = pasta / "Brutos" / b["arquivo"]; p = probe(f)
        v = next(s for s in p["streams"] if s["codec_type"] == "video")
        a = next((s for s in p["streams"] if s["codec_type"] == "audio"), None)
        rot = 0
        for sd in v.get("side_data_list", []) or []:
            rot = int(sd.get("rotation", 0) or 0)
        avg = Fraction(v["avg_frame_rate"]); r = Fraction(v["r_frame_rate"])
        vfr = abs(float(avg) - float(r)) > 0.5
        taxas.append(float(avg))
        if not a: alertas.append(f"{b['arquivo']} sem áudio")
        itens.append({"arquivo": b["arquivo"], "duracao": float(p["format"]["duration"]),
                      "largura": v["width"], "altura": v["height"], "rotacao": rot,
                      "fps_medio": round(float(avg), 3), "vfr": vfr, "audio": bool(a)})
    # taxa alvo: a padrão mais próxima da média
    media = sum(taxas) / len(taxas)
    alvo = min([24, 25, 30, 60], key=lambda x: abs(x - media))
    vf = f"fps={alvo}" + (",hflip" if d.get("espelhar") else "")
    for it in itens:
        src = pasta / "Brutos" / it["arquivo"]; stem = Path(it["arquivo"]).stem
        trab = out / f"{stem}_trab.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", vf, "-fps_mode", "cfr",
                        "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "256k", "-ar", "48000", str(trab)], check=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(trab), "-vn", "-ac", "1", "-ar", "16000", str(out / f"{stem}_16k.wav")], check=True)
        it["trabalho"] = str(trab.relative_to(pasta))
        it["duracao_trab"] = float(probe(trab)["format"]["duration"])
    d["midia"] = {"fps": alvo, "largura": itens[0]["largura"], "altura": itens[0]["altura"],
                  "espelhado": bool(d.get("espelhar")), "itens": itens, "alertas": alertas,
                  "obs": f"VFR convertido para {alvo} fps CFR" if any(i["vfr"] for i in itens) else "CFR"}
    estado.gravar(pasta, d)
    print(json.dumps({k: v for k, v in d["midia"].items() if k != "itens"}, ensure_ascii=False))
    for i in itens: print(i["arquivo"], round(i["duracao"], 2), "→", round(i["duracao_trab"], 2), "vfr" if i["vfr"] else "")

if __name__ == "__main__":
    main(sys.argv[1])
