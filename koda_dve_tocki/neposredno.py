"""
Neposredno preverjanje brez oglišč politopa P: ali ima sistem G v_n <= h rešitev?

Uporaba:   python neposredno.py 4+0        (ali 3+1, 2+2; deluje tudi za 3+0, 2+1, 2+0, 1+1)

Za dane podatke je to en linearni program. Preverimo ga
  (a) v vseh ogliščih politopa združljivih podatkov,
  (b) na 2000 naključnih združljivih podatkih,
  (c) za kontrolo še na naključnih podatkih, ki niso nujno združljivi
      (tam mora program včasih odgovoriti, da rešitve ni).
V (a) najdeno rešitev zaokrožimo na ulomke in točno preverimo, da res zadošča sistemu.
"""
import sys, time, random
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from dve_tocki import (razbitje, matrika_G, vektor_h, oglisca_podatkov,
                       nakljucni_zdruzljivi_podatki)

def resitev(G, h):
    """Rešitev sistema G v <= h z linearnim programom ali None, če je ni."""
    k = G.shape[1]
    r = linprog(np.zeros(k), A_ub=G.astype(float), b_ub=np.array([float(t) for t in h]),
                bounds=[(None, None)] * k, method="highs")
    return r.x if r.status == 0 else None

def tocno_zadosca(G, h, v):
    """Zaokroži v na ulomke in točno preveri G v <= h."""
    vf = [Fr(float(t)).limit_denominator(1000) for t in v]
    return all(sum(int(G[i, s]) * vf[s] for s in range(G.shape[1])) <= h[i] for i in range(G.shape[0]))

if __name__ == "__main__":
    ime = sys.argv[1]; p, r = map(int, ime.split("+")); d = p + r
    tocki = [tuple([2] * p + [1] * r), tuple([1] * p + [2] * r)]
    random.seed(1); rng = np.random.default_rng(1)
    H, Z, nedol, dol = razbitje(d, tocki); G = matrika_G(H, nedol)
    print(f"konfiguracija {ime}: {len(nedol)} neznank, {G.shape[0]} neenačb", flush=True)

    t0 = time.time(); X = oglisca_podatkov(d, tocki)
    resljivih = tocnih = 0
    for x in X:
        h = vektor_h(list(x), d, tocki, H, Z, nedol, dol)
        v = resitev(G, h)
        if v is not None:
            resljivih += 1; tocnih += tocno_zadosca(G, h, v)
    print(f"(a) oglišča politopa podatkov: {len(X)};  sistem ima rešitev v {resljivih}, "
          f"točno preverjenih {tocnih}  ({time.time() - t0:.0f} s)", flush=True)

    T = 2000; resljivih = 0
    for _ in range(T):
        h = vektor_h(nakljucni_zdruzljivi_podatki(d, tocki), d, tocki, H, Z, nedol, dol)
        resljivih += resitev(G, h) is not None
    print(f"(b) naključni združljivi podatki: sistem ima rešitev v {resljivih}/{T}", flush=True)

    T = 300; brez = 0
    for _ in range(T):
        pari = [sorted(rng.choice(range(1, 100), 2, replace=False)) for _ in range(d)]
        x = [Fr(int(a), 100) for a, b in pari] + [Fr(int(b), 100) for a, b in pari]
        x += [Fr(int(rng.integers(0, 101)), 100) * min(x) for _ in range(2)]
        brez += resitev(G, vektor_h(x, d, tocki, H, Z, nedol, dol)) is None
    print(f"(c) kontrola, podatki niso nujno združljivi: brez rešitve {brez}/{T}", flush=True)
