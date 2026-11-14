#!/usr/bin/env python3
"""Vídeo final: cortes + câmera (por quadro) + animações + legenda + voz + efeitos, -14 LUFS.
Uso: final_render.py <pasta_do_video> --motion <mov> --legenda <mov> --sfx <plano.json> [--segura 1.0] [--largura 1080] [--saida <mp4>]
- Imagem: cada cópia de trabalho é escalada para 1080 de largura (1080x2400 no bruto 864x1920) e a câmera
  (keyframes.json) escolhe a janela 1080x1920. Overlays RGBA por cima (legenda some onde há tela cheia).
- Segura o último quadro por --segura segundos (a última legenda precisa de tempo de leitura).
- Áudio: voz com fade de 1 quadro nas junções + efeitos nivelados pelo pico da voz; loudnorm 2 passadas."""
import argparse, json, subprocess, sys, tempfile
from pathlib import Path
import numpy as np, soundfile as sf, cv2
sys.path.insert(0, str(Path(__file__).parent)); import estado
SR = 48000
SONS = Path(__file__).resolve().parent.parent / "sons"

def le_frames(cmd, w, h, ch):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL); n = w*h*ch
    while True:
        b = p.stdout.read(n)
        if len(b) < n: break
        yield np.frombuffer(b, np.uint8).reshape(h, w, ch)
    p.wait()

def rgba(mov):
    return le_frames(["ffmpeg", "-v", "error", "-i", str(mov), "-f", "rawvideo", "-pix_fmt", "rgba", "-"], 1080, 1920, 4)

def blend(base, ov):
    a = ov[:, :, 3:4].astype(np.float32) / 255.0
    if a.max() == 0: return base
    return (base.astype(np.float32) * (1 - a) + ov[:, :, :3].astype(np.float32) * a).astype(np.uint8)

def audio(pasta, d, plano, segura, tmp):
    fps = d["midia"]["fps"]; partes = []
    for s in d["cortes"]["segmentos"]:
        trab = next(i["trabalho"] for i in d["midia"]["itens"] if i["arquivo"] == s["arquivo"])
        a0, a1 = s["frame_ini"]/fps, s["frame_fim"]/fps
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(pasta/trab), "-ss", f"{a0:.5f}", "-t", f"{a1-a0:.5f}",
                              "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
        x = np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
        n = int(round((s["frame_fim"]-s["frame_ini"]) / fps * SR)); x = np.pad(x, ((0, max(0, n-len(x))), (0, 0)))[:n]
        f = int(SR/fps); r = np.linspace(0, 1, f)[:, None]; x[:f] *= r; x[-f:] *= r[::-1]
        partes.append(x)
    voz = np.concatenate(partes); total = len(voz) + int(segura*SR)
    mix = np.zeros((total, 2), np.float32); mix[:len(voz)] += voz
    pico_voz = np.abs(voz).max()
    idx = json.loads((SONS/"indice.json").read_text(encoding="utf-8"))
    log = []
    for it in plano["itens"]:
        x, sr = sf.read(SONS/it["arquivo"], dtype="float32")
        if x.ndim == 1: x = np.stack([x, x], 1)
        meta = idx[it["arquivo"]]; x = x[int(meta["inicio_util"]*sr):]
        ini = it["t"] - (meta["pico"] if it.get("alinha") == "pico" else 0.0)
        g = pico_voz * 10**(it["db"]/20) / (np.abs(x).max() + 1e-9)
        a = int(round(ini*SR))
        if a < 0: x = x[-a:]; a = 0
        b = min(total, a+len(x)); mix[a:b] += x[:b-a]*g
        log.append(f"{it['id']} {it['arquivo']} em {ini:.3f}s")
    w = Path(tmp)/"mix.wav"; sf.write(w, mix, SR, subtype="FLOAT")
    # loudnorm em 2 passadas
    m = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(w), "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    j = json.loads(m[m.rindex("{"):m.rindex("}")+1])
    out = Path(tmp)/"mix_norm.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(w), "-af",
        f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true",
        "-ar", str(SR), str(out)], check=True)
    return out, log

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("pasta"); ap.add_argument("--motion"); ap.add_argument("--legenda")
    ap.add_argument("--tras", help="animações ATRÁS da pessoa (RGBA)"); ap.add_argument("--frente", help="animações na frente da pessoa (RGBA)")
    ap.add_argument("--pessoa", help="recorte da pessoa na sequência (MOV com alfa, resolução da cópia de trabalho)")
    ap.add_argument("--sfx"); ap.add_argument("--segura", type=float, default=1.0); ap.add_argument("--largura", type=int, default=1080)
    ap.add_argument("--saida"); a = ap.parse_args()
    pasta = Path(a.pasta); d = estado.ler(pasta); fps = d["midia"]["fps"]
    cam = json.loads((pasta / d["camera"]["keyframes"]).read_text()); Q = cam["quadros"]; ax, ay = cam["ancora"]
    esconde = [(round(i["ini"]*fps), round(i["fim"]*fps)) for i in d["motions"]["itens"]
               if i["formato"] == "tela cheia" or str(i.get("legenda", "")).startswith("some")]
    tmp = tempfile.mkdtemp()
    wav, log = audio(pasta, d, json.loads(Path(a.sfx).read_text(encoding="utf-8")), a.segura, tmp)
    vers = d.get("final", {}).get("versao", 0) + 1
    out = Path(a.saida) if a.saida else pasta / "Renders" / f"{d['projeto']}_final_v{vers:02d}.mp4"
    W, H = 1080, 1920
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
        "-i", str(wav), "-map", "0:v", "-map", "1:a", "-vf", f"scale={a.largura}:-2:flags=lanczos",
        "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-profile:v", "high",
        "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-movflags", "+faststart", "-shortest", str(out)], stdin=subprocess.PIPE)
    mo = rgba(a.motion) if a.motion else None; lg = rgba(a.legenda) if a.legenda else None
    tr = rgba(a.tras) if a.tras else None; fr_ = rgba(a.frente) if a.frente else None
    pe = None
    if a.pessoa:
        pw, ph = d["midia"]["largura"], d["midia"]["altura"]; psh = int(round(ph * 1080 / pw / 2) * 2)
        pe = le_frames(["ffmpeg", "-v", "error", "-i", str(a.pessoa), "-vf", f"scale=1080:{psh}:flags=lanczos",
                        "-f", "rawvideo", "-pix_fmt", "rgba", "-"], 1080, psh, 4)
    f = 0; ultimo = None
    for s in d["cortes"]["segmentos"]:
        trab = next(i for i in d["midia"]["itens"] if i["arquivo"] == s["arquivo"])
        sh = int(round(trab.get("altura", 1920) * 1080 / trab.get("largura", 1080) / 2) * 2)
        cmd = ["ffmpeg", "-v", "error", "-i", str(pasta/trab["trabalho"]), "-vf",
               f"trim=start_frame={s['frame_ini']}:end_frame={s['frame_fim']},setpts=PTS-STARTPTS,scale=1080:{sh}:flags=lanczos",
               "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
        off = (sh - H) / 2
        for fr in le_frames(cmd, 1080, sh, 3):
            sc, tx, ty = Q[min(f, len(Q)-1)]
            M = np.float32([[sc, 0, ax - sc*ax + tx], [0, sc, ay - sc*(ay + off) + ty]])
            img = cv2.warpAffine(fr, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
            cam_img = img.copy()  # a imagem da câmera (a pessoa volta por cima com os pixels originais + alfa do recorte)
            m_ = next(mo, None) if mo else None
            l_ = next(lg, None) if lg else None
            t_ = next(tr, None) if tr else None
            f_ = next(fr_, None) if fr_ else None
            p_ = next(pe, None) if pe else None
            if t_ is not None: img = blend(img, t_)
            if p_ is not None and t_ is not None and t_[:, :, 3].any():
                # a pessoa só precisa voltar por cima quando há algo atrás dela neste quadro
                pw_ = cv2.warpAffine(p_, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
                img = blend(img, np.dstack([cam_img, pw_[:, :, 3]]))
            if f_ is not None: img = blend(img, f_)
            if m_ is not None: img = blend(img, m_)
            if l_ is not None and not any(i0 <= f < i1 for i0, i1 in esconde): img = blend(img, l_)
            enc.stdin.write(img.tobytes()); ultimo = img; f += 1
    for _ in range(int(round(a.segura*fps))): enc.stdin.write(ultimo.tobytes())
    enc.stdin.close(); enc.wait()
    d = estado.ler(pasta)
    d["final"] = {"versao": vers, "arquivo": str(out.relative_to(pasta)), "quadros": f, "segura": a.segura}
    estado.gravar(pasta, d)
    print(out, f, "quadros"); print("\n".join(log[:3]), "…")

if __name__ == "__main__":
    main()
