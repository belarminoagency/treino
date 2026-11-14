#!/usr/bin/env python3
"""Palavras → tempo da sequência → blocos de legenda (1–3 palavras).
Uso: legendas_blocos.py <pasta_do_video>            gera _CLAUDE/legendas/blocos.json + blocos.txt (proposta)
     legendas_blocos.py <pasta_do_video> --gravar   grava blocos.json (já revisado) no bloco `legendas` do estado
No blocos.json revisado, cada bloco pode ter "destaque": <índice da palavra-chave> e "enfase": true (serifada itálica),
e cada palavra um "t" (texto exibido, ex.: "R$ 500") diferente do falado."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import estado
from tempo import tc

FUNCAO = set("a o as os um uma uns umas de da do das dos em na no nas nos por pra pro para com sem e ou mas que se ao à".split())

def palavras_seq(d, pal):
    out, off = [], 0.0
    for s in d["cortes"]["segmentos"]:
        for p in pal[s["arquivo"]]:
            meio = (p["ini"] + p["fim"]) / 2
            if s["ini"] <= meio <= s["fim"]:
                out.append({"w": p["w"], "ini": round(off + max(p["ini"], s["ini"]) - s["ini"], 3),
                            "fim": round(off + min(p["fim"], s["fim"]) - s["ini"], 3), "seg": s["id"]})
        off += s["fim"] - s["ini"]
    return out, off

def limpa(w):
    return re.sub(r"[.,;:]+$", "", w)

def propor(ws):
    blocos, cur = [], []
    for i, p in enumerate(ws):
        cur.append(p)
        prox = ws[i+1] if i+1 < len(ws) else None
        quebra = (not prox or len(cur) == 3 or re.search(r"[.,?!;:]$", p["w"])
                  or (prox and prox["ini"] - p["fim"] > 0.25) or (prox and prox["seg"] != p["seg"]))
        if quebra and prox and limpa(p["w"]).lower() in FUNCAO and len(cur) > 1:
            cur.pop(); blocos.append(cur); cur = [p]; continue
        if quebra:
            blocos.append(cur); cur = []
    if cur: blocos.append(cur)
    return [{"id": f"lg{k:02d}", "palavras": [{"w": p["w"], "t": limpa(p["w"]), "ini": p["ini"], "fim": p["fim"]} for p in b]}
            for k, b in enumerate(blocos, 1)]

def main(pasta, *args):
    pasta = Path(pasta); d = estado.ler(pasta); out = pasta / "_CLAUDE" / "legendas"; out.mkdir(parents=True, exist_ok=True)
    if "--gravar" in args:
        b = json.loads((out / "blocos.json").read_text(encoding="utf-8"))
        d["legendas"] = {"versao": d.get("legendas", {}).get("versao", 0) + 1, "cortes_versao": d["cortes"]["versao"],
                         "blocos": b["blocos"], "duracao": b["duracao"]}
        estado.gravar(pasta, d); print(f"legendas v{d['legendas']['versao']}: {len(b['blocos'])} blocos"); return
    pal = json.loads((pasta / d["transcricao"]["palavras"]).read_text(encoding="utf-8"))
    ws, dur = palavras_seq(d, pal)
    blocos = propor(ws)
    (out / "blocos.json").write_text(json.dumps({"duracao": round(dur, 3), "blocos": blocos}, ensure_ascii=False, indent=1), encoding="utf-8")
    txt = [f"{b['id']} [{tc(b['palavras'][0]['ini'])}] " + " | ".join(p["t"] for p in b["palavras"]) for b in blocos]
    (out / "blocos.txt").write_text("\n".join(txt) + "\n", encoding="utf-8"); print("\n".join(txt))

if __name__ == "__main__":
    main(*sys.argv[1:])
