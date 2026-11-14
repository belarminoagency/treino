#!/usr/bin/env python3
"""Transcreve cada cópia de trabalho (faster-whisper, CPU), tempo por palavra.
Uso: <venv>/python transcrever.py <pasta_do_video> [modelo=large-v3-turbo] [contexto="termos, nomes"]
Saídas: _CLAUDE/transcricao/palavras.json, frases.txt; bloco `transcricao` e `silencios` no estado.
Confere buracos (trecho com som e sem palavra) e retranscreve sem contexto."""
import json, sys, time
from pathlib import Path
import numpy as np, soundfile as sf
sys.path.insert(0, str(Path(__file__).parent))
import estado
from tempo import tc
import whisperx

PAUSA_MIN = 0.3

def rms_ativo(wav, sr, janela=0.02, limiar_db=-38):
    n = int(sr * janela); k = len(wav) // n
    r = np.sqrt((wav[:k*n].reshape(k, n) ** 2).mean(1) + 1e-12)
    db = 20 * np.log10(r)
    return db > max(limiar_db, np.percentile(db, 95) - 30), janela

def buracos(palavras, wav, sr, minimo=0.45):
    ativo, j = rms_ativo(wav, sr)
    cobre = np.zeros_like(ativo)
    for p in palavras:
        cobre[int(p["ini"]/j):int(p["fim"]/j)+1] = True
    falta = ativo & ~cobre
    res, i = [], 0
    while i < len(falta):
        if falta[i]:
            k = i
            while k < len(falta) and falta[k]: k += 1
            if (k - i) * j >= minimo: res.append((i*j, k*j))
            i = k
        else: i += 1
    return res

def palavras_de(seg_result, offset=0.0):
    out = []
    for s in seg_result["segments"]:
        for w in s.get("words", []):
            if "start" in w:
                out.append({"w": w["word"].strip(), "ini": round(w["start"]+offset, 3), "fim": round(w["end"]+offset, 3), "score": round(w.get("score", 0), 2)})
    return out

def main(pasta, modelo="large-v3-turbo", contexto=None):
    # ASR: faster-whisper (VAD Silero embutido no pacote, sem download extra).
    # Tempo por palavra: word_timestamps do faster-whisper (precisão ~0,05–0,1 s; as bordas de corte
    # são refinadas pela energia do áudio). O WhisperX (VAD pyannote/torch.hub e alinhamento com dados
    # do nltk) não carrega neste ambiente: usamos só o load_audio dele.
    from faster_whisper import WhisperModel
    import os
    pasta = Path(pasta); d = estado.ler(pasta)
    out = pasta / "_CLAUDE" / "transcricao"; out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    fw = WhisperModel(modelo, device="cpu", compute_type="int8", cpu_threads=os.cpu_count())
    def asr(audio, com_contexto=True):
        segs, _ = fw.transcribe(audio, language="pt", beam_size=5, vad_filter=True, word_timestamps=True,
                                initial_prompt=contexto if com_contexto else None,
                                condition_on_previous_text=False)
        return {"segments": [{"words": [{"word": w.word, "start": w.start, "end": w.end, "score": w.probability}
                                        for w in x.words]} for x in segs]}
    todas, sil, avisos = {}, {}, []
    for it in d["midia"]["itens"]:
        stem = Path(it["arquivo"]).stem
        wpath = pasta / "_CLAUDE" / "midia" / f"{stem}_16k.wav"
        audio = whisperx.load_audio(str(wpath))
        ps = palavras_de(asr(audio))
        wav, sr = sf.read(str(wpath))
        for a, b in buracos(ps, wav, sr):
            trecho = audio[int(max(0, a-0.2)*16000):int((b+0.2)*16000)]
            r2 = asr(trecho, com_contexto=False)
            if r2["segments"]:
                novas = [p for p in palavras_de(r2, max(0, a-0.2)) if not any(abs(p["ini"]-q["ini"]) < 0.1 for q in ps)]
                if novas:
                    ps = sorted(ps + novas, key=lambda p: p["ini"])
                    avisos.append(f"{it['arquivo']} {tc(a)}–{tc(b)}: recuperado '{' '.join(p['w'] for p in novas)}'")
            else:
                avisos.append(f"{it['arquivo']} {tc(a)}–{tc(b)}: som sem palavra (respiração/ruído?)")
        todas[it["arquivo"]] = ps
        dur = it["duracao_trab"]; s, ant = [], 0.0
        for p in ps:
            if p["ini"] - ant >= PAUSA_MIN: s.append([round(ant, 3), p["ini"]])
            ant = p["fim"]
        if dur - ant >= PAUSA_MIN: s.append([round(ant, 3), round(dur, 3)])
        sil[it["arquivo"]] = s
    (out / "palavras.json").write_text(json.dumps(todas, ensure_ascii=False, indent=1), encoding="utf-8")
    linhas = []
    for arq, ps in todas.items():
        linhas.append(f"## {arq}")
        frase, ini = [], None
        for i, p in enumerate(ps):
            if ini is None: ini = p["ini"]
            frase.append(p["w"])
            prox = ps[i+1] if i+1 < len(ps) else None
            gap = (prox["ini"] - p["fim"]) if prox else 0
            if not prox or gap >= 0.5 or p["w"][-1:] in ".?!":
                linhas.append(f"[{tc(ini)}–{tc(p['fim'])}] {' '.join(frase)}" + (f"  (pausa {gap:.1f} s)" if prox and gap >= 0.5 else ""))
                frase, ini = [], None
    (out / "frases.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    d = estado.ler(pasta)
    d["transcricao"] = {"modelo": f"faster-whisper {modelo} cpu int8 word_timestamps", "palavras": "_CLAUDE/transcricao/palavras.json",
                        "frases": "_CLAUDE/transcricao/frases.txt", "avisos": avisos, "segundos_gastos": round(time.time()-t0)}
    d["silencios"] = sil
    estado.gravar(pasta, d)
    print(f"ok em {round(time.time()-t0)} s; avisos: {len(avisos)}")
    for a in avisos: print(" -", a)

if __name__ == "__main__":
    main(*sys.argv[1:])
