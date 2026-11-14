#!/usr/bin/env python3
"""Lê e muda o _CLAUDE/projeto.json sem abrir inteiro.

Uso:
  estado.py <pasta> status
  estado.py <pasta> <bloco> [--json]
  estado.py <pasta> --item <id>
  estado.py <pasta> --set <caminho.com.pontos> <valor-json-ou-texto>
  estado.py <pasta> --etapa <etapa>=<status>
  estado.py <pasta> --pendencia <etapa> "<texto>"
  estado.py <pasta> --resolver <id>
"""
import json, os, sys, tempfile
from pathlib import Path

ORDEM = ["iniciar", "preparar", "cortes", "legendas", "motion_mapa", "motion_render", "camera", "sfx", "final"]
# bloco -> etapas que dependem da versão dele
DEPENDE = {"cortes": ["legendas", "motion_mapa", "motion_render", "camera", "sfx", "final"]}

def caminho(pasta):
    return Path(pasta) / "_CLAUDE" / "projeto.json"

def ler(pasta):
    return json.loads(caminho(pasta).read_text(encoding="utf-8"))

def gravar(pasta, dados):
    p = caminho(pasta)
    fd, tmp = tempfile.mkstemp(dir=p.parent, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=1)
    os.replace(tmp, p)

def status(pasta, d):
    print(f"Projeto: {d.get('projeto')} · perfil {d.get('perfil')} · {d.get('tipo')} · {d.get('formato')}"
          + (" · espelhado" if d.get("espelhar") else ""))
    et = d.get("etapas", {})
    print("Etapas: " + " → ".join(f"{e}[{et.get(e,'pendente')}]" for e in ORDEM))
    prox = next((e for e in ORDEM if et.get(e, "pendente") not in ("concluido", "nao_precisa")), None)
    print(f"Próxima: {prox or 'nenhuma (vídeo concluído)'}")
    alertas = []
    falt = [b["arquivo"] for b in d.get("brutos", []) if not (Path(pasta) / "Brutos" / b["arquivo"]).exists()]
    if falt:
        alertas.append(f"brutos ausentes nesta sessão (pedir reenvio): {', '.join(falt)}")
    vc = d.get("cortes", {}).get("versao")
    for e in DEPENDE["cortes"]:
        usada = d.get("versoes_usadas", {}).get(e, {}).get("cortes")
        if vc and usada and usada != vc and et.get(e) in ("concluido", "aguardando_aprovacao"):
            alertas.append(f"{e} feito com cortes v{usada}, cortes agora é v{vc}: recalcular")
    for a in alertas:
        print("ALERTA: " + a)
    pend = [p for p in d.get("pendencias", []) if not p.get("resolvida")]
    for p in pend:
        print(f"Pendência {p['id']} ({p['etapa']}): {p['texto']}")
    ap = Path(pasta) / "_CLAUDE" / "aprendizados.md"
    if ap.exists():
        n = sum(1 for l in ap.read_text(encoding="utf-8").splitlines() if l.startswith("- [ ]"))
        print(f"Aprendizados anotados (não aplicados): {n}")

def resumo_bloco(nome, v):
    if isinstance(v, dict):
        for k, x in v.items():
            if isinstance(x, list):
                print(f"{k}: {len(x)} itens")
                for it in x[:60]:
                    if isinstance(it, dict):
                        print("  " + " · ".join(f"{a}={str(b)[:50]}" for a, b in it.items() if not isinstance(b, (dict, list))))
            elif isinstance(x, dict):
                print(f"{k}: {{{', '.join(list(x)[:12])}}}")
            else:
                print(f"{k}: {x}")
    elif isinstance(v, list):
        print(f"{len(v)} itens")
        for it in v[:60]:
            print("  " + (json.dumps(it, ensure_ascii=False)[:160]))
    else:
        print(v)

def achar_item(o, iid):
    if isinstance(o, dict):
        if o.get("id") == iid:
            return o
        for x in o.values():
            r = achar_item(x, iid)
            if r: return r
    elif isinstance(o, list):
        for x in o:
            r = achar_item(x, iid)
            if r: return r

def main(a):
    if len(a) < 2:
        print(__doc__); return 1
    pasta, cmd = a[0], a[1]
    d = ler(pasta)
    if cmd == "status":
        status(pasta, d)
    elif cmd == "--item":
        print(json.dumps(achar_item(d, a[2]), ensure_ascii=False, indent=1))
    elif cmd == "--set":
        chaves, valor = a[2].split("."), a[3]
        try: valor = json.loads(valor)
        except Exception: pass
        o = d
        for k in chaves[:-1]:
            o = o.setdefault(k, {})
        o[chaves[-1]] = valor
        gravar(pasta, d); print("ok")
    elif cmd == "--etapa":
        e, s = a[2].split("=")
        d.setdefault("etapas", {})[e] = s
        if s in ("concluido", "aguardando_aprovacao") and "cortes" in d and e in DEPENDE["cortes"]:
            d.setdefault("versoes_usadas", {}).setdefault(e, {})["cortes"] = d["cortes"].get("versao")
        gravar(pasta, d); print(f"{e} = {s}")
    elif cmd == "--pendencia":
        ps = d.setdefault("pendencias", [])
        pid = f"p{len(ps)+1:02d}"
        ps.append({"id": pid, "etapa": a[2], "texto": a[3]})
        gravar(pasta, d); print(pid)
    elif cmd == "--resolver":
        for p in d.get("pendencias", []):
            if p["id"] == a[2]: p["resolvida"] = True
        gravar(pasta, d); print("ok")
    else:
        v = d.get(cmd)
        if "--json" in a: print(json.dumps(v, ensure_ascii=False, indent=1))
        else: resumo_bloco(cmd, v)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
