"""
Tri točke v treh dimenzijah, zmanjšana različica: oglišča stožca {lambda >= 0, H_n^T lambda = 0}.

Vsako oglišče da linearno neenakost v podatkih. Za vsako konfiguracijo preverimo,
katere od teh neenakosti so pogoji združljivosti (fasete politopa združljivih podatkov)
in katere so dodatni pogoji. Dodatne izpišemo.

Uporaba:   python zmanjsano_tri.py
"""
import time, math
from fractions import Fraction as Fr
import cdd
from tocke import Naloga
from konfiguracije import vse_konfiguracije, vrstni_red
from zmanjsano import zarki, Hd_vd

def okrajsaj(v):
    g = 0
    for t in v: g = math.gcd(g, int(t))
    return tuple(int(t) // g for t in v) if g else tuple(v)

def oblika(N, lam):
    """Neenakost lambda^T H_d v_d >= 0 kot (c0, c) s pomenom c0 + c . p >= 0."""
    m = N.d * N.n + N.n
    f = lambda p: sum(int(l) * c for l, c in zip(lam, Hd_vd(N, p)) if l)
    c0 = f([Fr(0)] * m)
    return okrajsaj([c0] + [f([Fr(int(i == j)) for i in range(m)]) - c0 for j in range(m)])

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
            ime[l * N.n + N.konf[l][j]] = f"{'xyz'[l]}_{'ABC'[j]}"
    for j in range(N.n):
        ime[N.d * N.n + j] = f"q_{'ABC'[j]}"
    clen = lambda c, i: f"{'+' if c > 0 else '-'} {abs(c) if abs(c) != 1 else ''}{ime[i]}"
    return " ".join(clen(c, i) for i, c in enumerate(o[1:]) if c) + (f" + {o[0]}" if o[0] else "") + " >= 0"

if __name__ == "__main__":
    vrstice = []
    for i, konf in enumerate(vse_konfiguracije(), 1):
        t0 = time.time(); N = Naloga(konf)
        L = zarki(N); F = fasete(N); X = N.oglisca_podatkov()
        oblike = {oblika(N, lam): lam for lam in L}
        dodatni = [o for o in oblike if o not in F]
        # dodatni pogoj je res nov, če je kršen v kakšnem oglišču politopa podatkov
        nov = lambda o: min(o[0] + sum(c * t for c, t in zip(o[1:], p)) for p in X) < 0
        print(f"K{i}  osi {vrstni_red(konf)}:  oglišč {len(L)}, pogojev združljivosti {len(F)} "
              f"(vsi med oglišči: {F <= set(oblike)}), dodatnih {len(dodatni)}, "
              f"od teh res novih {sum(map(nov, dodatni))};  čas {time.time() - t0:.1f} s")
        for o in dodatni:
            lam = oblike[o]
            print(f"   {zapis(N, o)}   (celic {sum(1 for t in lam if t)}, uteži {sorted({int(t) for t in lam if t})})")
        vrstice.append((f"K{i}", len(L), len(F), len(dodatni)))
    print("\nPovzetek\nkonf.  oglišč  pogojev združljivosti  dodatnih")
    for v in vrstice:
        print(f"{v[0]:<5} {v[1]:>7} {v[2]:>22} {v[3]:>9}")
