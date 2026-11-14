#!/usr/bin/env python3
"""Atualiza o recorte da pessoa para um corte novo, reaproveitando o recorte do corte antigo.
Uso: recorte_atualizar.py <pasta_do_video> <cortes_antigos.json>
Quadros que já existiam (mesmo arquivo e mesmo quadro de origem) vêm do pessoa.mov antigo; só os novos passam pelo modelo.
Saída: _CLAUDE/midia/pessoa.mov (o antigo vira pessoa_cortes_vNN.mov) e sequencia.mp4 do corte novo."""
import json, shutil, subprocess, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent)); import estado

def frames(cmd, w, h, ch):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL); n = w*h*ch
    while True:
        b = p.stdout.read(n)
        if len(b) < n: break
        yield np.frombuffer(b, np.uint8).reshape(h, w, ch)

def lista(c):
    return [(s["arquivo"], f) for s in c["segmentos"] for f in range(s["frame_ini"], s["frame_fim"])]

def main(pasta, antigo):
    pasta = Path(pasta); d = estado.ler(pasta); m = pasta / "_CLAUDE/midia"
    velho = json.loads(Path(antigo).read_text()); vc = velho["versao"]
    lv, ln = lista(velho), lista(d["cortes"])
    idx_velho = {k: i for i, k in enumerate(lv)}
    faltam = [k for k in ln if k not in idx_velho]
    W, H = d["midia"]["largura"], d["midia"]["altura"]
    trab = {i["arquivo"]: str(pasta / i["trabalho"]) for i in d["midia"]["itens"]}
    # sequência nova (sem câmera)
    sv = m / f"sequencia_cortes_v{vc:02d}.mp4"
    if not sv.exists(): shutil.move(str(m / "sequencia.mp4"), sv)
    pv = m / f"pessoa_cortes_v{vc:02d}.mov"
    if not pv.exists(): shutil.move(str(m / "pessoa.mov"), pv)
    subprocess.run([sys.executable, str(Path(__file__).parent / "recorte_pessoa.py"), str(pasta), "--so-sequencia"], check=True)
    # quadros que faltam → vídeo curto → modelo
    tmp = m / "faltam"; tmp.mkdir(exist_ok=True)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                            "-c:v", "libx264", "-crf", "10", "-pix_fmt", "yuv420p", str(tmp / "faltam.mp4")], stdin=subprocess.PIPE)
    por_arq = {}
    for a, f in faltam: por_arq.setdefault(a, set()).add(f)
    for a in sorted(por_arq):
        for f, q in enumerate(frames(["ffmpeg", "-v", "error", "-i", trab[a], "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], W, H, 3)):
            if f in por_arq[a]: enc.stdin.write(q.tobytes())
    enc.stdin.close(); enc.wait()
    ordem_faltam = [(a, f) for a in sorted(por_arq) for f in sorted(por_arq[a])]
    subprocess.run(["npx", "--yes", f"hyperframes@{d['ferramentas']['hyperframes']}", "remove-background", str(tmp / "faltam.mp4"), "-o", str(tmp / "faltam.mov")], check=True)
    novos = {k: q.copy() for k, q in zip(ordem_faltam, frames(["ffmpeg", "-v", "error", "-i", str(tmp / "faltam.mov"), "-f", "rawvideo", "-pix_fmt", "rgba", "-"], W, H, 4))}
    # monta o pessoa.mov novo: percorre o antigo em ordem (os quadros reaproveitados aparecem na mesma ordem)
    out = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                            "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", str(m / "pessoa.mov")], stdin=subprocess.PIPE)
    velho_it = enumerate(frames(["ffmpeg", "-v", "error", "-i", str(pv), "-f", "rawvideo", "-pix_fmt", "rgba", "-"], W, H, 4))
    atual = next(velho_it, (None, None))
    for k in ln:
        if k in novos: out.stdin.write(novos[k].tobytes()); continue
        alvo = idx_velho[k]
        while atual[0] is not None and atual[0] < alvo: atual = next(velho_it, (None, None))
        out.stdin.write(atual[1].tobytes())
    out.stdin.close(); out.wait()
    shutil.rmtree(tmp)
    print(f"{len(ln)} quadros; reaproveitados {len(ln)-len(faltam)}, recortados agora {len(faltam)}")

if __name__ == "__main__":
    main(*sys.argv[1:])
