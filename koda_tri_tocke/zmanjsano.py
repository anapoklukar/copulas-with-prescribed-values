"""
Zmanjšana različica (predlog mentorja, 15. 10.): meje a_n <= v_n <= b_n izpustimo.

Ker so vrednosti v določenih vozliščih (robovi in predpisane točke) fiksne, je vsaka
rešitev sistema  H_n v_n >= -H_d v_d  že diskretna kopula s predpisanimi vrednostmi,
zato meje ovojnic ne dodajo ničesar. Dualni stožec je tedaj
    { lambda >= 0 : H_n^T lambda = 0 },
pogoj pa  lambda^T H_d v_d >= 0, ki je v podatkih LINEAREN.

Uporaba:   python zmanjsano.py 3+0        (dve točki, konfiguracija p+r)
           python zmanjsano.py dve        (dve točki, vse konfiguracije v dimenzijah 2 do 6)
"""
import sys, time, itertools, random
from fractions import Fraction as Fr
import numpy as np
from PyNormaliz import Cone
from tocke import Naloga

def konf_dve(p, r):
    return tuple([(1, 0)] * p + [(0, 1)] * r)

def zarki(N):
    """Ekstremni žarki stožca {lambda >= 0, H_n^T lambda = 0} (Normaliz, točno)."""
    Hn = N.H[:, N.nedol]; M = Hn.shape[0]
    C = Cone(equations=[[int(Hn[i, s]) for i in range(M)] for s in range(Hn.shape[1])],
             inequalities=np.eye(M, dtype=int).tolist())
    C.Compute("ExtremeRays")
    return np.array(C.ExtremeRays(), dtype=object)

def Hd_vd(N, p):
    """Prvi del vektorja h: volumni celic iz samih določenih vrednosti."""
    d, n = N.d, N.n
    def znana(z):
        if 0 in z: return Fr(0)
        if z in N.tocke: return p[d * n + N.tocke.index(z)]
        return min(N.koordinate(z, p))
    vd = {s: znana(N.Z[s]) for s in N.dol}
    return [sum(int(N.H[i, s]) * vd[s] for s in N.dol if N.H[i, s]) for i in range(N.H.shape[0])]

def obdelaj(ime, konf, nakljucnih=300):
    random.seed(1)
    N = Naloga(konf); t0 = time.time()
    L = zarki(N); t_z = time.time() - t0
    # vse neenakosti v vseh ogliščih politopa podatkov (točno)
    X = N.oglisca_podatkov()
    najmanj = min(min(sum(int(l) * c for l, c in zip(lam, Hd_vd(N, list(p)))) for lam in L) for p in X)
    # kontrola: zmanjšani sistem (brez mej) in polni sistem dajeta isti odgovor
    Hn = N.H[:, N.nedol].astype(float); ujemanje = 0
    from scipy.optimize import linprog
    for _ in range(nakljucnih):
        if random.random() < 0.5:
            p = N.nakljucni_podatki()                               # združljivi
        else:                                                       # ne nujno združljivi
            p = []
            for l in range(N.d):
                p += [Fr(t, 100) for t in sorted(random.sample(range(1, 100), N.n))]
            p += [Fr(random.randint(0, 100), 100) * min(p) for _ in range(N.n)]
        rhs = np.array([float(t) for t in Hd_vd(N, p)])
        zm = linprog(np.zeros(Hn.shape[1]), A_ub=-Hn, b_ub=rhs, bounds=[(None, None)] * Hn.shape[1],
                     method="highs").status == 0
        polni = N.resitev(N.vektor_h(p)) is not None
        ujemanje += zm == polni
    print(f"{ime}: celic {N.H.shape[0]}, neznank {len(N.nedol)} | žarki zmanjšanega stožca: {len(L)} "
          f"({t_z:.1f} s) | oglišča podatkov {len(X)}, najmanjša vrednost {najmanj} | "
          f"zmanjšani = polni sistem: {ujemanje}/{nakljucnih}", flush=True)

if __name__ == "__main__":
    if sys.argv[1] == "dve":
        for d in range(2, 7):
            for r in range(0, d // 2 + 1):
                obdelaj(f"{d - r}+{r}", konf_dve(d - r, r), nakljucnih=300 if d <= 4 else 60)
    else:
        p, r = map(int, sys.argv[1].split("+"))
        obdelaj(sys.argv[1], konf_dve(p, r))
