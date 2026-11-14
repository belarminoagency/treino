#!/usr/bin/env python3
"""Acha as notas de edição faladas ("nota de edição" … "fim da nota"), tolerando variações.
Uso: notas.py <pasta_do_video>  → grava o bloco `notas_edicao` no estado."""
import json, re, sys, unicodedata
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import estado

def norm(t):
    t = unicodedata.normalize("NFD", t.lower()); t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z ]", "", t)

ABRE = re.compile(r"\bnota (de|da|do)? ?edica[oa]\b")
FECHA = re.compile(r"\bfi[mn] (da|de|do)? ?nota\b")

def main(pasta):
    pasta = Path(pasta); d = estado.ler(pasta)
    pal = json.loads((pasta / d["transcricao"]["palavras"]).read_text(encoding="utf-8"))
    notas = []
    for arq, ps in pal.items():
        txt, idx = "", []
        for i, p in enumerate(ps):
            w = norm(p["w"]); idx.append((len(txt), i)); txt += w + " "
        def pal_em(pos): return max(i for c, i in idx if c <= pos)
        for m in ABRE.finditer(txt):
            i0 = pal_em(m.start()); f = FECHA.search(txt, m.end())
            if f:
                i1 = pal_em(f.end() - 1); conf = "alta"
            else:
                i1 = i0
                while i1 + 1 < len(ps) and ps[i1+1]["ini"] - ps[i1]["fim"] < 1.0: i1 += 1
                conf = "baixa"
            notas.append({"id": f"n{len(notas)+1:02d}", "arquivo": arq, "ini": ps[i0]["ini"], "fim": ps[i1]["fim"],
                          "texto": " ".join(p["w"] for p in ps[i0:i1+1]), "confianca": conf,
                          "interpretacao": "", "etapa": ""})
    d["notas_edicao"] = notas; estado.gravar(pasta, d)
    print(f"{len(notas)} notas"); [print(" ", n["id"], n["arquivo"], n["texto"]) for n in notas]

if __name__ == "__main__":
    main(sys.argv[1])
