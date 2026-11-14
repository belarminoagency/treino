#!/usr/bin/env python3
"""Extrai o quadro da câmera num tempo da SEQUÊNCIA (pelos segmentos do corte), já no quadro final 9:16.
Uso: quadro_seq.py <pasta_do_video> <tempo_seq> <saida.png> [sobreposicao.png]
O bruto do celular pode não ser 9:16 (ex.: 864x1920): escala pela largura para 1080 e corta o excesso no centro.
Com sobreposição (PNG transparente 1080x1920), compõe por cima."""
import subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import estado

def local(d, t):
    off = 0.0
    for s in d["cortes"]["segmentos"]:
        dur = s["fim"] - s["ini"]
        if t < off + dur: return s["arquivo"], s["ini"] + (t - off)
        off += dur
    s = d["cortes"]["segmentos"][-1]; return s["arquivo"], s["fim"] - 0.04

def main(pasta, t, out, sob=None):
    pasta = Path(pasta); d = estado.ler(pasta); arq, tl = local(d, float(t))
    trab = next(i["trabalho"] for i in d["midia"]["itens"] if i["arquivo"] == arq)
    vf = "scale=1080:-2,crop=1080:1920"
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{tl:.3f}", "-i", str(pasta / trab)]
    if sob:
        cmd += ["-i", sob, "-filter_complex", f"[0:v]{vf}[b];[1:v]scale=1080:1920[o];[b][o]overlay=0:0", "-frames:v", "1", out]
    else:
        cmd += ["-vf", vf, "-frames:v", "1", out]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    main(*sys.argv[1:])
