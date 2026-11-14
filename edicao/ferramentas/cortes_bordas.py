#!/usr/bin/env python3
"""Ajusta as bordas dos segmentos pela energia do áudio + folga do perfil, arredonda para frames.
Uso: cortes_bordas.py <pasta_do_video> <rascunho.json>
rascunho.json: {"segmentos":[{"arquivo":"bruto01.mp4","de":"Seu","ate":"mais.","de_i":0,"ate_i":12,"obs":""}],
                "marcadores":[{"arquivo":..., "tempo":..., "tipo":"duvida_take|hesitacao|nota|sugestao|alerta", "texto":...}],
                "folga_ini":0.06, "folga_fim":0.10}
de_i/ate_i: índices das palavras de borda em palavras.json (o "de"/"ate" é só para conferência).
Grava o bloco `cortes` (versão +1) e `marcadores` no estado. Tempos no tempo da cópia de trabalho."""
import json, sys
from pathlib import Path
import numpy as np, soundfile as sf
sys.path.insert(0, str(Path(__file__).parent)); import estado
from tempo import s2f, f2s, tc

def energia_db(wav, sr, j=0.01):
    n = int(sr*j); k = len(wav)//n
    return 20*np.log10(np.sqrt((wav[:k*n].reshape(k, n)**2).mean(1)+1e-12)), j

def main(pasta, rascunho):
    pasta = Path(pasta); d = estado.ler(pasta); r = json.loads(Path(rascunho).read_text(encoding="utf-8"))
    fps = d["midia"]["fps"]; pal = json.loads((pasta / d["transcricao"]["palavras"]).read_text(encoding="utf-8"))
    fi, ff = r.get("folga_ini", 0.06), r.get("folga_fim", 0.10)
    cache, segs, avisos = {}, [], []
    durs = {i["arquivo"]: i["duracao_trab"] for i in d["midia"]["itens"]}
    for n, s in enumerate(r["segmentos"], 1):
        arq = s["arquivo"]; ps = pal[arq]; w0, w1 = ps[s["de_i"]], ps[s["ate_i"]]
        for chk, w in (("de", w0), ("ate", w1)):
            if s.get(chk) and s[chk].strip(".,?!").lower() not in w["w"].strip(".,?!").lower():
                avisos.append(f"s{n:03d}: '{s[chk]}' não bate com a palavra '{w['w']}'")
        if arq not in cache:
            wav, sr = sf.read(str(pasta / "_CLAUDE" / "midia" / arq.replace(".mp4", "_16k.wav")))
            cache[arq] = energia_db(wav, sr)
        db, j = cache[arq]; piso = np.percentile(db, 10); lim = piso + 0.35*(np.percentile(db, 95)-piso)
        # início: recua da palavra enquanto houver energia (até 0,25 s); fim: avança idem
        a = int(w0["ini"]/j); lim_a = max(0, a-int(0.25/j))
        while a > lim_a and db[a-1] > lim: a -= 1
        b = min(int(w1["fim"]/j), len(db)-1); lim_b = min(len(db)-1, b+int(0.25/j))
        while b < lim_b and db[b+1] > lim: b += 1
        ini = max(0.0, a*j - fi); fim = min(durs[arq], (b+1)*j + ff)
        # não invadir a palavra anterior/seguinte que ficou fora do segmento
        if s["de_i"] > 0: ini = max(ini, ps[s["de_i"]-1]["fim"] + 0.02)
        if s["ate_i"]+1 < len(ps): fim = min(fim, ps[s["ate_i"]+1]["ini"] - 0.02)
        F0, F1 = s2f(ini, fps), s2f(fim, fps)
        segs.append({"id": f"s{n:03d}", "arquivo": arq, "ini": round(f2s(F0, fps), 4), "fim": round(f2s(F1, fps), 4),
                     "frame_ini": F0, "frame_fim": F1,
                     "texto": " ".join(p["w"] for p in ps[s["de_i"]:s["ate_i"]+1]), "obs": s.get("obs", "")})
    vers = d.get("cortes", {}).get("versao", 0) + 1
    d["cortes"] = {"versao": vers, "fps": fps, "segmentos": segs,
                   "duracao": round(sum(x["fim"]-x["ini"] for x in segs), 3)}
    d["marcadores"] = [dict(m, id=f"m{i:03d}") for i, m in enumerate(r.get("marcadores", []), 1)]
    estado.gravar(pasta, d)
    print(f"cortes v{vers}: {len(segs)} segmentos, {tc(d['cortes']['duracao'])}")
    for x in segs: print(f"  {x['id']} {x['arquivo']} {tc(x['ini'])}–{tc(x['fim'])} {x['texto'][:60]}")
    for a in avisos: print("AVISO:", a)

if __name__ == "__main__":
    main(*sys.argv[1:])
