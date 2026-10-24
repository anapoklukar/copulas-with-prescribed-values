"""
Tri točke v dimenziji d (privzeto 3), zmanjšana različica: oglišča stožca {lambda >= 0, H_n^T lambda = 0}.

Vsako oglišče da linearno neenakost v podatkih. Za vsako konfiguracijo preverimo,
katere od teh neenakosti so pogoji združljivosti (fasete politopa združljivih podatkov)
in katere so dodatni pogoji. Dodatne izpišemo.

Uporaba:   python zmanjsano_tri.py        (tri dimenzije)
           python zmanjsano_tri.py 4      (štiri dimenzije)
"""
import sys, time, math
import numpy as np
from fractions import Fraction as Fr
import cdd
from tocke import Naloga
from konfiguracije import vse_konfiguracije, vrstni_red
from zmanjsano import zarki

def okrajsaj(v):
    g = 0
    for t in v: g = math.gcd(g, int(t))
    return tuple(int(t) // g for t in v) if g else tuple(v)

def linearni_del(N):
    """Matrika B, za katero je H_d v_d = B (1, p): vrednosti v določenih vozliščih so linearne v podatkih."""
    d, n = N.d, N.n; m = d * n + n
    A = np.zeros((len(N.dol), m + 1), dtype=np.int64)
    for i, s in enumerate(N.dol):
        z = N.Z[s]
        if 0 in z:
            continue                                             # vrednost 0
        if z in N.tocke:
            A[i, 1 + d * n + N.tocke.index(z)] = 1               # predpisana vrednost
            continue
        ostale = [l for l in range(d) if z[l] != n + 1]
        if ostale:
            l = ostale[0]; A[i, 1 + l * n + z[l] - 1] = 1        # edina koordinata, ki ni 1
        else:
            A[i, 0] = 1                                          # vozlišče (1, ..., 1)
    return N.H[:, N.dol].astype(np.int64) @ A

def oblika(B, lam):
    """Neenakost lambda^T H_d v_d >= 0 kot (c0, c) s pomenom c0 + c . p >= 0."""
    return okrajsaj(np.array([int(t) for t in lam], dtype=np.int64) @ B)

def fasete(N):
    """Potrebni pogoji združljivosti (cdd odstrani odvečne)."""
    mat = cdd.matrix_from_array([[int(t) for t in r] for r in N.neenacbe_podatkov()],
                                rep_type=cdd.RepType.INEQUALITY)
    cdd.matrix_canonicalize(mat)
    return {okrajsaj(r) for r in mat.array}

def zapis(N, o):
    ime = {}
    for l in range(N.d):
        for j in range(N.n):
            ime[l * N.n + N.konf[l][j]] = f"{'xyzwv'[l]}_{'ABC'[j]}"
    for j in range(N.n):
        ime[N.d * N.n + j] = f"q_{'ABC'[j]}"
    clen = lambda c, i: f"{'+' if c > 0 else '-'} {abs(c) if abs(c) != 1 else ''}{ime[i]}"
    return " ".join(clen(c, i) for i, c in enumerate(o[1:]) if c) + (f" + {o[0]}" if o[0] else "") + " >= 0"

if __name__ == "__main__":
    d = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    vrstice = []
    for i, konf in enumerate(vse_konfiguracije(d=d, n=3), 1):
        t0 = time.time(); N = Naloga(konf)
        L = zarki(N); F = fasete(N); X = N.oglisca_podatkov(); B = linearni_del(N)
        oblike = {oblika(B, lam): lam for lam in L}
        dodatni = [o for o in oblike if o not in F]
        # dodatni pogoj je res nov, če je kršen v kakšnem oglišču politopa podatkov
        nov = lambda o: min(o[0] + sum(c * t for c, t in zip(o[1:], p)) for p in X) < 0
        print(f"K{i}  osi {vrstni_red(konf)}:  oglišč {len(L)}, pogojev združljivosti {len(F)} "
              f"(vsi med oglišči: {F <= set(oblike)}), dodatnih {len(dodatni)}, "
              f"od teh res novih {sum(map(nov, dodatni))};  čas {time.time() - t0:.1f} s", flush=True)
        for o in dodatni:
            lam = oblike[o]
            print(f"   {zapis(N, o)}   (celic {sum(1 for t in lam if t)}, uteži {sorted({int(t) for t in lam if t})})")
        vrstice.append((f"K{i}", len(L), len(F), len(dodatni), len(X)))
    print(f"\nPovzetek (dimenzija {d})\nkonf.  oglišč  pogojev združljivosti  dodatnih  oglišč politopa podatkov")
    for v in vrstice:
        print(f"{v[0]:<5} {v[1]:>7} {v[2]:>22} {v[3]:>9} {v[4]:>25}")
