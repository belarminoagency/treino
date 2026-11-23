#!/usr/bin/env python3
"""Gera a biblioteca inicial de efeitos sonoros por síntese (sem problema de licença) em edicao/sons/<categoria>/.
Uso: sons_sintetizar.py   (semente fixa: sai igual toda vez). WAV 48 kHz estéreo, 24 bits, pico -1 dBFS."""
import numpy as np, soundfile as sf
from pathlib import Path
SR = 48000; RAIZ = Path(__file__).resolve().parent.parent / "sons"
rng = np.random.default_rng(7)

def t(d): return np.arange(int(SR*d)) / SR
def norm(x, pico_db=-1.0): return x / (np.abs(x).max() + 1e-9) * 10**(pico_db/20)
def env_ad(n, ataque, queda=4.0):
    a = int(n*ataque); e = np.ones(n)
    e[:a] = np.linspace(0, 1, a)**2 if a else 1
    r = np.linspace(0, 1, n-a); e[a:] = np.exp(-queda*r) * (1 - r)
    return e
def passa_banda_varrido(x, f0, f1, q=2.0):
    # filtro de estado variável com frequência variando no tempo
    n = len(x); f = np.geomspace(f0, f1, n); y = np.zeros(n); lp = bp = 0.0
    for i in range(n):
        g = 2*np.sin(np.pi*f[i]/SR); hp = x[i] - lp - bp/q; bp += g*hp; lp += g*bp; y[i] = bp
    return y
def estereo(x, larg=0.15):
    d = int(SR*0.0007); r = np.concatenate([np.zeros(d), x[:-d]]) if d else x
    return np.stack([x*(1-larg)+r*larg, r*(1-larg)+x*larg], 1)
def grava(cat, nome, x):
    p = RAIZ / cat; p.mkdir(parents=True, exist_ok=True)
    sf.write(p / f"{nome}.wav", estereo(norm(x)), SR, subtype="PCM_24")

def whoosh(d, f0, f1, pico=0.6):
    n = int(SR*d); x = rng.standard_normal(n)
    y = passa_banda_varrido(x, f0, f1, q=1.6)
    k = int(n*pico); e = np.concatenate([np.linspace(0, 1, k)**2.5, np.linspace(1, 0, n-k)**1.8])
    return y*e
def pop(f0, f1, d=0.09):
    tt = t(d); f = np.geomspace(f0, f1, len(tt)); ph = 2*np.pi*np.cumsum(f)/SR
    return np.sin(ph) * env_ad(len(tt), 0.04, 5)
def clique(f=3500, d=0.025):
    tt = t(d); x = rng.standard_normal(len(tt))*0.6 + np.sin(2*np.pi*f*tt)
    return x * np.exp(-tt*220)
def impacto(f=55, d=0.9, brilho=0.4):
    tt = t(d); corpo = np.sin(2*np.pi*f*tt*(1+0.6*np.exp(-tt*18))) * np.exp(-tt*5)
    trans = rng.standard_normal(len(tt)) * np.exp(-tt*60) * brilho
    return corpo + trans
def ding(f=1320, d=0.6):
    tt = t(d); return (np.sin(2*np.pi*f*tt) + 0.5*np.sin(2*np.pi*f*2.01*tt) + 0.25*np.sin(2*np.pi*f*3.02*tt)) * np.exp(-tt*7) * (1-np.exp(-tt*900))
def tic(f=1800, d=0.05):
    tt = t(d); return np.sin(2*np.pi*f*tt) * np.exp(-tt*120) + rng.standard_normal(len(tt))*np.exp(-tt*400)*0.3
def riser(d=0.9):
    n = int(SR*d); y = passa_banda_varrido(rng.standard_normal(n), 300, 6000, q=2.5)
    return y * np.linspace(0, 1, n)**3
def tecla():
    tt = t(0.04); return (rng.standard_normal(len(tt))*np.exp(-tt*300) + 0.5*np.sin(2*np.pi*2400*tt)*np.exp(-tt*200))
def digitacao(n=12, intervalo=0.045):
    out = np.zeros(int(SR*(n*intervalo+0.1)))
    for i in range(n):
        k = tecla() * (0.6 + 0.4*rng.random()); a = int(SR*(i*intervalo + rng.random()*0.012)); out[a:a+len(k)] += k
    return out
def carimbo():
    return impacto(f=90, d=0.35, brilho=1.2) * 0.8 + np.pad(clique(1200, 0.03), (0, int(SR*0.32)))

def main():
    for i, (d, f0, f1) in enumerate([(0.35, 500, 5000), (0.5, 300, 3500), (0.7, 150, 2200), (0.45, 800, 7000)], 1):
        grava("whoosh", f"whoosh_{i:02d}", whoosh(d, f0, f1))
    for i, (f0, f1) in enumerate([(900, 420), (700, 300), (1200, 600)], 1):
        grava("pop", f"pop_{i:02d}", pop(f0, f1))
    for i, f in enumerate([3500, 2600, 4500], 1):
        grava("clique", f"clique_{i:02d}", clique(f))
    for i, (f, d, b) in enumerate([(50, 1.0, 0.5), (65, 0.7, 0.8)], 1):
        grava("impacto", f"impacto_{i:02d}", impacto(f, d, b))
    grava("grave", "sub_01", impacto(42, 1.2, 0.0))
    for i, f in enumerate([1320, 1760], 1):
        grava("ding", f"ding_{i:02d}", ding(f))
    for i, f in enumerate([1800, 2200, 1500], 1):
        grava("interface", f"tic_{i:02d}", tic(f))
    grava("interface", "digitacao_01", digitacao())
    grava("interface", "carimbo_01", carimbo())
    grava("riser", "riser_01", riser())
    # subida curta: varredura ascendente que termina no pico (barra/elemento que sobe rápido)
    for i, (d, f0, f1) in enumerate([(0.45, 250, 6000), (0.35, 400, 8000)], 1):
        grava("whoosh", f"subida_{i:02d}", whoosh(d, f0, f1, pico=0.85))
    # descida: varredura do agudo pro grave (algo que cai/despenca)
    for i, (d, f0, f1) in enumerate([(0.5, 5000, 180), (0.4, 7000, 300)], 1):
        grava("whoosh", f"descida_{i:02d}", whoosh(d, f0, f1, pico=0.2))
    print("ok:", RAIZ)

if __name__ == "__main__":
    main()
