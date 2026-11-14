#!/usr/bin/env python3
"""Monta os segmentos do corte num MP4 leve para revisão no celular.
Uso: render_rascunho.py <pasta_do_video> [largura=720]
Saída: Renders/<projeto>_cortes_vNN.mp4 (H.264/AAC, +faststart). Fade de áudio de ~1 frame em cada borda (sem estalo)."""
import subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import estado

def main(pasta, largura="720"):
    pasta = Path(pasta); d = estado.ler(pasta); c = d["cortes"]; fps = c["fps"]
    trab = {i["arquivo"]: str(pasta / i["trabalho"]) for i in d["midia"]["itens"]}
    arqs = sorted({s["arquivo"] for s in c["segmentos"]}, key=lambda a: a)
    idx = {a: k for k, a in enumerate(arqs)}
    cmd = ["ffmpeg", "-v", "error", "-y"]
    for a in arqs: cmd += ["-i", trab[a]]
    fade = 1.0/fps; fil, cat = [], ""
    for n, s in enumerate(c["segmentos"]):
        k = idx[s["arquivo"]]; dur = s["fim"]-s["ini"]
        fil.append(f"[{k}:v]trim=start_frame={s['frame_ini']}:end_frame={s['frame_fim']},setpts=PTS-STARTPTS,scale={largura}:-2[v{n}]")
        fil.append(f"[{k}:a]atrim=start={s['ini']}:end={s['fim']},asetpts=PTS-STARTPTS,"
                   f"afade=t=in:d={fade:.4f},afade=t=out:st={max(0,dur-fade):.4f}:d={fade:.4f}[a{n}]")
        cat += f"[v{n}][a{n}]"
    fil.append(f"{cat}concat=n={len(c['segmentos'])}:v=1:a=1[v][a]")
    out = pasta / "Renders" / f"{d['projeto']}_cortes_v{c['versao']:02d}.mp4"
    cmd += ["-filter_complex", ";".join(fil), "-map", "[v]", "-map", "[a]", "-r", str(fps),
            "-c:v", "libx264", "-crf", "23", "-preset", "veryfast", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)
    print(out)

if __name__ == "__main__":
    main(*sys.argv[1:])
