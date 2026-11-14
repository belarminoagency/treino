#!/usr/bin/env python3
"""Gera o projeto HyperFrames da legenda a partir do bloco `legendas` do estado e (opcional) renderiza.
Uso: legendas_render.py <pasta_do_video> [--check] [--snapshot 1,5,9] [--render]
Projeto em _CLAUDE/legendas/hf/ (copia a peça-base legendas_render/). Render: Renders/<projeto>_legendas_vNN.mov
(ProRes 4444 com transparência, 1080x1920, fps do vídeo). Composição sempre 1080 de largura."""
import json, shutil, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import estado
from tempo import s2f
BASE = Path(__file__).parent / "legendas_render"

def hf(d):
    return ["npx", "--yes", f"hyperframes@{d['ferramentas']['hyperframes']}"]

def main(pasta, *args):
    pasta = Path(pasta); d = estado.ler(pasta)
    if "hyperframes" not in d.get("ferramentas", {}):
        v = subprocess.run(["npm", "view", "hyperframes", "version"], capture_output=True, text=True).stdout.strip()
        d.setdefault("ferramentas", {})["hyperframes"] = v; estado.gravar(pasta, d)
    lg, fps = d["legendas"], d["midia"]["fps"]
    proj = pasta / "_CLAUDE" / "legendas" / "hf"
    if proj.exists(): shutil.rmtree(proj)
    shutil.copytree(BASE, proj, ignore=shutil.ignore_patterns("template.html"))
    N = s2f(lg["duracao"], fps); dur = (N - 0.5) / fps
    vertical = d.get("formato", "vertical") == "vertical"
    html = (BASE / "template.html").read_text(encoding="utf-8")
    html = (html.replace("__DADOS__", json.dumps({"duracao": dur, "blocos": lg["blocos"]}, ensure_ascii=False))
                .replace("__DUR__", f"{dur:.4f}").replace("__Y__", "1460" if vertical else "1500")
                .replace("__APOIO__", "62").replace("__CHAVE__", "116").replace("__ENFASE__", "104"))
    (proj / "index.html").write_text(html, encoding="utf-8")
    (proj / "meta.json").write_text(json.dumps({"id": "legendas", "name": "legendas"}), encoding="utf-8")
    print(f"projeto: {proj} · {N} frames · {dur:.4f} s")
    if "--check" in args:
        subprocess.run(hf(d) + ["check"], cwd=proj)
    if "--snapshot" in args:
        at = args[args.index("--snapshot") + 1]
        subprocess.run(hf(d) + ["snapshot", "--at", at], cwd=proj)
    if "--render" in args:
        out = pasta / "Renders" / f"{d['projeto']}_legendas_v{lg['versao']:02d}.mov"
        subprocess.run(hf(d) + ["render", "--format", "mov", "--fps", str(fps), "-o", str(out), "--quiet"], cwd=proj, check=True)
        print(out)

if __name__ == "__main__":
    main(*sys.argv[1:])
