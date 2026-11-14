#!/usr/bin/env python3
"""Recorte da pessoa (fundo transparente) na sequência do corte, para animações ATRÁS da pessoa.
Uso: recorte_pessoa.py <pasta_do_video>
1) monta a sequência do corte sem câmera, na resolução da cópia de trabalho (_CLAUDE/midia/sequencia.mp4)
2) hyperframes remove-background (modelo local, CPU ~1,6 quadro/s) → _CLAUDE/midia/pessoa.mov (ProRes 4444 com alfa)
O final_render aplica a mesma câmera ao recorte e compõe: vídeo → animação de trás → pessoa → animação da frente → legenda."""
import subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import estado

def main(pasta):
    pasta = Path(pasta); d = estado.ler(pasta); c = d["cortes"]
    arqs = sorted({s["arquivo"] for s in c["segmentos"]}); idx = {a: k for k, a in enumerate(arqs)}
    trab = {i["arquivo"]: str(pasta / i["trabalho"]) for i in d["midia"]["itens"]}
    cmd = ["ffmpeg", "-v", "error", "-y"]
    for a in arqs: cmd += ["-i", trab[a]]
    fil, cat = [], ""
    for n, s in enumerate(c["segmentos"]):
        fil.append(f"[{idx[s['arquivo']]}:v]trim=start_frame={s['frame_ini']}:end_frame={s['frame_fim']},setpts=PTS-STARTPTS[v{n}]"); cat += f"[v{n}]"
    fil.append(f"{cat}concat=n={len(c['segmentos'])}:v=1:a=0[v]")
    seq = pasta / "_CLAUDE" / "midia" / "sequencia.mp4"
    subprocess.run(cmd + ["-filter_complex", ";".join(fil), "-map", "[v]", "-r", str(c["fps"]), "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", str(seq)], check=True)
    if "--so-sequencia" in sys.argv: print(seq); return
    out = pasta / "_CLAUDE" / "midia" / "pessoa.mov"
    subprocess.run(["npx", "--yes", f"hyperframes@{d['ferramentas']['hyperframes']}", "remove-background", str(seq), "-o", str(out)], check=True)
    d = estado.ler(pasta); d.setdefault("midia", {})["pessoa"] = str(out.relative_to(pasta)); estado.gravar(pasta, d)
    print(out)

if __name__ == "__main__":
    main(sys.argv[1])
