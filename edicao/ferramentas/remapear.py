#!/usr/bin/env python3
"""Leva tempos da sequência de um corte antigo para o corte novo (pelo tempo do arquivo de origem).
Uso: remapear.py <pasta_do_video> <cortes_antigos.json>
Atualiza: legendas (palavras), motions.itens (ini/fim/gatilhos), motion/eventos.json, motion/base/template.html (tempos no script),
camera/movimentos.json (t) e o plano de sfx mais recente (t). Grava as cópias antigas com sufixo _cortes_vN."""
import json, re, shutil, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import estado

def tabela(cortes):
    fps, off, out = cortes["fps"], 0, []
    for s in cortes["segmentos"]:
        n = s["frame_fim"] - s["frame_ini"]
        out.append((s["id"], s["arquivo"], off / fps, (off + n) / fps, s["frame_ini"] / fps, s["frame_fim"] / fps)); off += n
    return out, off / fps

def main(pasta, antigo):
    pasta = Path(pasta); d = estado.ler(pasta)
    velho, dv = tabela(json.loads(Path(antigo).read_text(encoding="utf-8")))
    novo, dn = tabela(d["cortes"])
    def R(t):
        if t >= dv: return dn - (dv - t) if t - dv < 2 else dn
        for (sid, arq, a, b, si, sf) in velho:
            if a <= t < b:
                src = si + (t - a)
                n = next(x for x in novo if x[0] == sid)
                return round(n[2] + min(max(src, n[4]), n[5]) - n[4], 3)
        return t
    vc = json.loads(Path(antigo).read_text())["versao"]
    # legendas
    for b in d["legendas"]["blocos"]:
        for p in b["palavras"]: p["ini"], p["fim"] = R(p["ini"]), R(p["fim"])
    d["legendas"]["duracao"] = round(dn, 3); d["legendas"]["cortes_versao"] = d["cortes"]["versao"]
    # motions
    for it in d["motions"]["itens"]:
        it["ini"], it["fim"] = R(it["ini"]), R(it["fim"])
        it["gatilhos"] = {k: R(v) for k, v in it.get("gatilhos", {}).items()}
    d["motions"]["cortes_versao"] = d["cortes"]["versao"]
    for e in ["legendas", "motion_mapa", "motion_render", "camera", "sfx"]:
        d.setdefault("versoes_usadas", {})[e] = {"cortes": d["cortes"]["versao"]}
    estado.gravar(pasta, d)
    # eventos
    ev = pasta / "_CLAUDE/motion/eventos.json"
    if ev.exists():
        e = json.loads(ev.read_text()); shutil.copy(ev, ev.with_name(f"eventos_cortes_v{vc:02d}.json"))
        for x in e["eventos"]: x["t"] = R(x["t"])
        ev.write_text(json.dumps(e, ensure_ascii=False, indent=1))
    # template: só números com 2 casas no <script>, que não sejam valor de propriedade ("chave: 0.45") e >= 0,3 s
    tp = pasta / "_CLAUDE/motion/base/template.html"
    if tp.exists():
        h = tp.read_text(); shutil.copy(tp, tp.with_name(f"template_cortes_v{vc:02d}.html"))
        i = h.index("<script>\n  window.__timelines")
        head, scr = h[:i], h[i:]
        def sub(m):
            v = float(m.group(1)); return f"{R(v):.2f}" if v >= 0.3 else m.group(1)
        scr = re.sub(r"(?<![\w]: )(?<![\w.])(\d{1,2}\.\d{2})(?![\d])", sub, scr)
        # posição com 1 casa logo depois de um tween ("…}), 20.6);")
        scr = re.sub(r"(?<=\}\), )(\d{1,2}\.\d)(?=\);)", sub, scr)
        N = round(dn * d["cortes"]["fps"]); dur = (N - 0.5) / d["cortes"]["fps"]
        scr = re.sub(r"FIM = [\d.]+", f"FIM = {dur:.4f}", scr)
        head = re.sub(r'data-duration="[\d.]+"', f'data-duration="{dur:.4f}"', head)
        tp.write_text(head + scr)
    # câmera
    cm = pasta / "_CLAUDE/camera/movimentos.json"
    if cm.exists():
        m = json.loads(cm.read_text()); shutil.copy(cm, cm.with_name(f"movimentos_cortes_v{vc:02d}.json"))
        for mv in m["movimentos"]: mv["t"] = R(mv["t"])
        cm.write_text(json.dumps(m, ensure_ascii=False, indent=1))
    # sfx (o plano mais recente)
    planos = sorted((pasta / "_CLAUDE/sfx").glob("plano_v*.json"))
    if planos:
        p = json.loads(planos[-1].read_text()); n = int(planos[-1].stem[-2:]) + 1
        for x in p["itens"]: x["t"] = R(x["t"])
        p["obs"] = p.get("obs", "") + f" · remapeado para cortes v{d['cortes']['versao']}"
        (planos[-1].parent / f"plano_v{n:02d}.json").write_text(json.dumps(p, ensure_ascii=False, indent=1))
    print(f"duração {dv:.2f} → {dn:.2f} s")
    for t in [0.40, 3.37, 9.43, 12.68, 20.93, 28.38, 33.90]: print(f"  {t:.2f} → {R(t):.2f}")

if __name__ == "__main__":
    main(*sys.argv[1:])
