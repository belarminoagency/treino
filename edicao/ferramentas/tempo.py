"""Conversão segundos <-> frames, num lugar só. Use a taxa real (fração) do vídeo."""
from fractions import Fraction

def fps_frac(fps):
    """Aceita '30000/1001', 29.97, 30, Fraction."""
    if isinstance(fps, Fraction):
        return fps
    if isinstance(fps, str) and "/" in fps:
        n, d = fps.split("/")
        return Fraction(int(n), int(d))
    f = float(fps)
    if abs(f - 29.97) < 0.01:
        return Fraction(30000, 1001)
    if abs(f - 23.976) < 0.01:
        return Fraction(24000, 1001)
    if abs(f - 59.94) < 0.01:
        return Fraction(60000, 1001)
    return Fraction(f).limit_denominator(1001)

def s2f(seg, fps):
    return int(round(Fraction(seg).limit_denominator(100000) * fps_frac(fps)))

def f2s(frame, fps):
    return float(Fraction(frame) / fps_frac(fps))

def tc(seg):
    m, s = divmod(max(seg, 0), 60)
    return f"{int(m):02d}:{s:05.2f}"
