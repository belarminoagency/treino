#!/usr/bin/env python3
"""Câmera: base (zoom alternado por corte + aproximação lenta) + movimentos desenhados → transformação por quadro.
Uso: camera_calc.py <pasta_do_video> <movimentos.json>
movimentos.json: {"fechado":1.15,"lenta":0.04,"ancora":[540,800],
  "planos":{"s002":"fechado",...},            # opcional: força o plano de um corte (senão alterna)
  "movimentos":[{"id":"cam01","tipo":"punch","t":3.37,"de":1.0,"mais":0.07,"dur":0.3},
                {"id":"cam02","tipo":"zoom","t":9.43,"mais":0.06,"dur":1.0,"curva":"sine.inOut"},
                {"id":"cam03","tipo":"desloca","t":20.8,"ate":23.43,"dx":60,"dy":0,"dur":0.6},
                {"id":"cam04","tipo":"acelera","t":27.95,"mais":0.10,"dur":0.2},
                {"id":"cam05","tipo":"chega","t":29.23,"dy":90,"dx":0,"dur":0.5}]}
Saída: _CLAUDE/camera/keyframes.json  ({"fps":30,"ancora":[x,y],"quadros":[[s,tx,ty],...]} no quadro final 1080x1920)
Avisos: borda à mostra, corte com mudança < 5%."""
import json, math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import estado
from tempo import s2f

def ease(nome, x):
    x = min(max(x, 0.0), 1.0)
    if nome == "power2.out": return 1 - (1 - x) ** 3
    if nome == "power4.in": return x ** 5
    if nome == "expo.out": return 1 if x == 1 else 1 - 2 ** (-10 * x)
    if nome == "sine.inOut": return -(math.cos(math.pi * x) - 1) / 2
    if nome == "power2.inOut": return 4*x**3 if x < .5 else 1 - (-2*x + 2)**3 / 2
    return x

def main(pasta, mov):
    pasta = Path(pasta); d = estado.ler(pasta); m = json.loads(Path(mov).read_text(encoding="utf-8"))
    fps = d["midia"]["fps"]; segs = d["cortes"]["segmentos"]
    # tempos de corte na sequência
    # cortes em QUADROS inteiros (como o render final monta), para câmera e imagem baterem no mesmo quadro
    cortes, fo = [], 0
    for s in segs:
        n = s["frame_fim"] - s["frame_ini"]
        cortes.append((s["id"], fo / fps, (fo + n) / fps)); fo += n
    N = fo; fe = m.get("fechado", 1.15); lenta = m.get("lenta", 0.04)
    # o plano de cada corte é escolhido por onde a câmera TERMINOU no take anterior (o corte sempre muda de plano)
    planos, quadros, avisos = {}, [], []
    ult_s = None
    for f in range(N):
        t = f / fps
        sid, a, b = next((c for c in cortes if round(c[1]*fps) <= f < round(c[2]*fps)), cortes[-1])
        if sid not in planos:
            forcado = m.get("planos", {}).get(sid)
            if forcado: planos[sid] = forcado
            elif ult_s is None: planos[sid] = "aberto"
            else: planos[sid] = "aberto" if ult_s >= (1 + fe) / 2 else "fechado"
        base = fe if planos[sid] == "fechado" else 1.0
        s = base * (1 + lenta * (t - a) / max(b - a, 0.01))
        tx = ty = 0.0
        for mv in m["movimentos"]:
            t0, dur = mv["t"], mv.get("dur", 0.3)
            if t < t0: continue
            # movimentos valem até o fim do segmento em que começam (salvo "ate")
            fim_mv = mv.get("ate") or next(c[2] for c in cortes if c[1] <= t0 < c[2])
            if t >= fim_mv: continue
            x = (t - t0) / dur
            if mv["tipo"] in ("punch", "zoom", "acelera"):
                cur = {"punch": "power2.out", "zoom": mv.get("curva", "sine.inOut"), "acelera": "power4.in"}[mv["tipo"]]
                s *= 1 + mv["mais"] * ease(cur, x)
            elif mv["tipo"] == "desloca":
                e = ease("power2.inOut", x); tx += mv.get("dx", 0) * e; ty += mv.get("dy", 0) * e
            elif mv["tipo"] == "chega":
                e = 1 - ease("expo.out", x); tx += mv.get("dx", 0) * e; ty += mv.get("dy", 0) * e
        # limite da borda: o quadro-fonte é 1080x2400 (sobra 240 px em cima e embaixo)
        ax, ay = m.get("ancora", [540, 800])
        maxx = (s - 1) * 1080 / 2 + 0.0
        if abs(tx) > maxx + (s - 1) * 0 and s >= 1:
            lim = (s - 1) * 1080 / 2
            if abs(tx) > lim + 0.5:
                avisos.append(f"{t:.2f}s: deslocamento x {tx:.0f} > margem {lim:.0f} (limitado)")
                tx = math.copysign(lim, tx)
        quadros.append([round(s, 5), round(tx, 2), round(ty, 2)])
        ult_s = s
    # avisos de corte sem mudança de plano
    for (sid1, a1, b1), (sid2, a2, b2) in zip(cortes, cortes[1:]):
        f2 = round(a2 * fps); f1 = f2 - 1
        if f2 < N and abs(quadros[f2][0] / quadros[f1][0] - 1) < 0.05:
            avisos.append(f"corte {sid2} ({a2:.2f}s): mudança de plano < 5%")
    out = pasta / "_CLAUDE" / "camera"; out.mkdir(parents=True, exist_ok=True)
    (out / "keyframes.json").write_text(json.dumps({"fps": fps, "ancora": m.get("ancora", [540, 800]), "quadros": quadros}), encoding="utf-8")
    d = estado.ler(pasta)
    d["camera"].update({"planos": planos, "movimentos": m["movimentos"], "fechado": fe, "lenta": lenta, "keyframes": "_CLAUDE/camera/keyframes.json"})
    estado.gravar(pasta, d)
    print(f"{N} quadros; planos: " + " ".join(f"{k}:{v[0]}" for k, v in planos.items()))
    for a in avisos: print("AVISO:", a)

if __name__ == "__main__":
    main(*sys.argv[1:])
