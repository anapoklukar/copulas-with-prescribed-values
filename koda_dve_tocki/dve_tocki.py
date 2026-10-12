"""
Interpolacija dveh točk: sistem G v_n <= h in oglišča dualnega politopa P.

Uporaba:   python dve_tocki.py 3+0        (ali 2+1; v dveh dimenzijah 2+0, 1+1)

Konfiguracija "p+r" pomeni dimenzijo d = p + r, kjer je prva točka večja od
druge v prvih p koordinatah in manjša v zadnjih r koordinatah.

Koraki:
  1. incidenčna matrika H, določena in nedoločena vozlišča, razbitje H = [H_n | H_d]
  2. matrika G = [-H_n; I; -I]
  3. oglišča politopa P = {y >= 0, G^T y = 0, vsota y = 1}  (knjižnica cdd)
  4. preverjanje neenakosti h^T y >= 0 in kontrole
"""
import sys, time, itertools, random
from fractions import Fraction as Fr
from math import lcm
import numpy as np
import cdd
from scipy.optimize import linprog


# ---------- 1. mreža, incidenčna matrika, razbitje ----------

def incidencna_matrika(d):
    """H velikosti 3^d x 4^d: (H v)_B je volumen celice B. Vrstice so celice, stolpci vozlišča."""
    F = np.array([[-1, 1, 0, 0], [0, -1, 1, 0], [0, 0, -1, 1]])    # razlike po eni osi
    H = F
    for _ in range(d - 1):
        H = np.kron(H, F)
    return H

def vozlisca(d):
    """Vozlišča mreže kot d-terice indeksov 0..3 (0 -> 0, 1 -> manjša, 2 -> večja, 3 -> 1)."""
    return list(itertools.product(range(4), repeat=d))

def je_doloceno(z, tocki):
    return (0 in z                                   # katera koordinata je 0: vrednost 0
            or sum(1 for i in z if i != 3) <= 1      # vse razen ene so 1: vrednost je ta koordinata
            or z in tocki)                           # predpisana točka

def razbitje(d, tocki):
    H, Z = incidencna_matrika(d), vozlisca(d)
    nedol = [j for j, z in enumerate(Z) if not je_doloceno(z, tocki)]
    dol = [j for j, z in enumerate(Z) if je_doloceno(z, tocki)]
    return H, Z, nedol, dol


# ---------- 2. matrika G ----------

def matrika_G(H, nedol):
    Hn, k = H[:, nedol], len(nedol)
    return np.vstack([-Hn, np.eye(k, dtype=int), -np.eye(k, dtype=int)])


# ---------- 3. oglišča politopa P ----------

def oglisca_P(G):
    """Ekstremni žarki stožca {y >= 0, G^T y = 0}, vsak zapisan s celimi števili."""
    m, k = G.shape
    vrstice = [[0] + [int(i == j) for j in range(m)] for i in range(m)]         # y_i >= 0
    vrstice += [[0] + [int(G[i, s]) for i in range(m)] for s in range(k)]        # (G^T y)_s = 0
    mat = cdd.matrix_from_array(vrstice, rep_type=cdd.RepType.INEQUALITY,
                                lin_set=set(range(m, m + k)))
    generatorji = cdd.copy_generators(cdd.polyhedron_from_matrix(mat)).array
    oglisca = set()
    for g in generatorji:
        if g[0] != 0:                      # to je izhodišče, ne žarek
            continue
        y = np.array(g[1:])
        y = y / y[np.abs(y) > 1e-9].min()                        # najmanjša neničelna utež = 1
        ulomki = [Fr(float(t)).limit_denominator(1000) for t in y]
        skupni = lcm(*[u.denominator for u in ulomki])
        oglisca.add(tuple(int(u * skupni) for u in ulomki))
    # točno preverjanje vsakega oglišča
    for y in oglisca:
        assert all(t >= 0 for t in y)
        assert all(sum(int(G[i, s]) * y[i] for i in range(m)) == 0 for s in range(k))
        aktivne = np.vstack([np.eye(m)[[i for i in range(m) if y[i] == 0]], G.T])
        assert np.linalg.matrix_rank(aktivne) == m - 1           # res je ekstremni žarek
    return sorted(oglisca)

def stevilo_do_simetrij(oglisca, d, p, Z, nedol):
    """Število oglišč do zamenjav koordinat, ki ohranjajo konfiguracijo."""
    celice = list(itertools.product(range(3), repeat=d))
    M, k = len(celice), len(nedol)
    ind_cel = {c: i for i, c in enumerate(celice)}
    ind_ned = {Z[j]: i for i, j in enumerate(nedol)}
    perm = [a + tuple(p + t for t in b) for a in itertools.permutations(range(p))
            for b in itertools.permutations(range(d - p))]
    vsa, videna, razredov = set(oglisca), set(), 0
    for y in oglisca:
        if y in videna:
            continue
        razredov += 1
        for s in perm:
            t = [0] * len(y)
            for c, i in ind_cel.items():
                t[ind_cel[tuple(c[s[a]] for a in range(d))]] = y[i]
            for z, i in ind_ned.items():
                j = ind_ned[tuple(z[s[a]] for a in range(d))]
                t[M + j], t[M + k + j] = y[M + i], y[M + k + i]
            assert tuple(t) in vsa
            videna.add(tuple(t))
    return razredov


# ---------- 4. podatki, vektor h, preverjanje ----------
# Podatki: x = (s_1..s_d, l_1..l_d, q_1, q_2); s_k < l_k sta koordinati točk na osi k.

def koordinate(z, x, d):
    return [[Fr(0), x[k], x[d + k], Fr(1)][z[k]] for k in range(d)]

def d_plus(u, v):
    return sum(max(a - b, Fr(0)) for a, b in zip(u, v))

def ovojnici(z, x, d, tocki):
    """Spodnja in zgornja ovojnica (3.4), (3.5) v vozlišču z."""
    u = koordinate(z, x, d)
    T = [koordinate(t, x, d) for t in tocki]
    q = x[2 * d:]
    a = max([Fr(0), sum(u) - (d - 1)] + [q[j] - d_plus(T[j], u) for j in range(2)])
    b = min(u + [q[j] + d_plus(u, T[j]) for j in range(2)])
    return a, b

def vektor_h(x, d, tocki, H, Z, nedol, dol):
    """h = [H_d v_d; b_n; -a_n]."""
    def znana_vrednost(z):
        if 0 in z: return Fr(0)
        if z == tocki[0]: return x[2 * d]
        if z == tocki[1]: return x[2 * d + 1]
        return min(koordinate(z, x, d))
    vd = [znana_vrednost(Z[j]) for j in dol]
    Hd_vd = [sum(int(H[i, j]) * vd[jj] for jj, j in enumerate(dol)) for i in range(H.shape[0])]
    ab = [ovojnici(Z[j], x, d, tocki) for j in nedol]
    return Hd_vd + [b for a, b in ab] + [-a for a, b in ab]

def neenacbe_podatkov(d, tocki):
    """Pogoji za združljive podatke kot vrstice (c0, c) s pomenom c0 + c . x >= 0."""
    n = 2 * d + 2
    def e(i, t=1):
        v = [0] * (n + 1); v[i + 1] = t; return np.array(v)
    koord = lambda j, k: e(k) if tocki[j][k] == 1 else e(d + k)
    ena = np.array([1] + [0] * n)
    vr = []
    for k in range(d):
        vr += [e(k), e(d + k) - e(k), ena - e(d + k)]                    # 0 <= s_k <= l_k <= 1
    for j in range(2):
        qj = e(2 * d + j)
        vr += [qj, qj - sum(koord(j, k) for k in range(d)) + (d - 1) * ena]   # q_j >= W(x_j)
        vr += [koord(j, k) - qj for k in range(d)]                            # q_j <= M(x_j)
    for i, j in [(0, 1), (1, 0)]:                                             # (3.3)
        dp = sum((e(d + k) - e(k) for k in range(d) if tocki[i][k] > tocki[j][k]), 0 * ena)
        vr.append(dp - e(2 * d + i) + e(2 * d + j))
    return np.array(vr)

def oglisca_podatkov(d, tocki):
    """Oglišča politopa združljivih podatkov: izčrpen pregled, vsako točno preverjeno."""
    vr = neenacbe_podatkov(d, tocki); n = 2 * d + 2
    najdena = set()
    for izbor in itertools.combinations(range(len(vr)), n):
        A = vr[list(izbor), 1:].astype(float)
        if abs(np.linalg.det(A)) < 1e-9:
            continue
        x = np.linalg.solve(A, -vr[list(izbor), 0].astype(float))
        xf = [Fr(float(t)).limit_denominator(10**6) for t in x]
        vrednosti = [int(r[0]) + sum(int(c) * t for c, t in zip(r[1:], xf)) for r in vr]
        assert all(vrednosti[i] == 0 for i in izbor)
        if all(v >= 0 for v in vrednosti):
            najdena.add(tuple(xf))
    return sorted(najdena)

def nakljucni_zdruzljivi_podatki(d, tocki):
    def izberi(lo, hi):                        # 1/4 spodnji rob, 1/4 zgornji rob, 1/2 vmes
        r = random.random()
        return lo if r < 0.25 else hi if r < 0.5 else lo + Fr(random.randint(0, 100), 100) * (hi - lo)
    pari = [sorted(random.sample(range(1, 100), 2)) for _ in range(d)]
    s, l = [Fr(p[0], 100) for p in pari], [Fr(p[1], 100) for p in pari]
    T = [koordinate(t, s + l, d) for t in tocki]
    W = [max(Fr(0), sum(t) - (d - 1)) for t in T]; Mm = [min(t) for t in T]
    q1 = izberi(W[0], Mm[0])
    q2 = izberi(max(W[1], q1 - d_plus(T[0], T[1])), min(Mm[1], q1 + d_plus(T[1], T[0])))
    return s + l + [q1, q2]


if __name__ == "__main__":
    ime = sys.argv[1]; p, r = map(int, ime.split("+")); d = p + r
    tocki = [tuple([2] * p + [1] * r), tuple([1] * p + [2] * r)]       # indeksi točk na mreži
    random.seed(1); rng = np.random.default_rng(1)

    H, Z, nedol, dol = razbitje(d, tocki)
    # preizkus predznakov v H: za produktno kopulo so volumni celic produkti stranic
    x0 = [Fr(1, 3)] * d + [Fr(2, 3)] * d
    assert all(v == Fr(1, 3) ** d for v in
               (sum(int(H[i, j]) * np.prod(koordinate(z, x0, d)) for j, z in enumerate(Z)) for i in range(len(H))))
    G = matrika_G(H, nedol)
    print(f"konfiguracija {ime}: dimenzija {d}, točki na mreži {tocki}")
    print(f"H: {H.shape[0]} x {H.shape[1]},  določenih vozlišč {len(dol)}, nedoločenih {len(nedol)}")
    print(f"H_n: {H.shape[0]} x {len(nedol)},  G: {G.shape[0]} x {G.shape[1]}")

    t0 = time.time()
    Y = oglisca_P(G)
    trivialna = sum(1 for y in Y if not any(y[:H.shape[0]]))
    print(f"oglišča politopa P: {len(Y)}  (od tega trivialnih a_s <= b_s: {trivialna}),  "
          f"čas {time.time() - t0:.0f} s")
    print(f"oglišča do zamenjave koordinat: {stevilo_do_simetrij(Y, d, p, Z, nedol)}")
    Yc = np.array(Y, dtype=np.int64)

    # (a) vse neenakosti v vseh ogliščih politopa podatkov, točno (cela števila)
    X = oglisca_podatkov(d, tocki)
    najmanj = None
    for x in X:
        h = vektor_h(list(x), d, tocki, H, Z, nedol, dol)
        im = lcm(*[t.denominator for t in h])
        v = int((Yc @ np.array([int(t * im) for t in h], dtype=np.int64)).min())
        najmanj = Fr(v, im) if najmanj is None else min(najmanj, Fr(v, im))
    print(f"(a) oglišča politopa podatkov: {len(X)};  {len(Y)} neenakosti v vsakem, "
          f"najmanjša vrednost h^T y = {najmanj}")

    # (b) vse neenakosti na naključnih združljivih podatkih
    T = 2000
    hs = np.array([[float(t) for t in vektor_h(nakljucni_zdruzljivi_podatki(d, tocki), d, tocki, H, Z, nedol, dol)]
                   for _ in range(T)])
    print(f"(b) {T} naključnih združljivih podatkov: najmanjša vrednost h^T y = "
          f"{min((hs[i:i + 200] @ Yc.T).min() for i in range(0, T, 200)):.1e}")

    # (c) kontrola seznama oglišč: odgovor po ogliščih = odgovor linearnega programa,
    #     na naključnih podatkih, ki niso nujno združljivi
    ujemanj, brez_resitve, T = 0, 0, 300
    for _ in range(T):
        pari = [sorted(rng.choice(range(1, 100), 2, replace=False)) for _ in range(d)]
        x = [Fr(int(a), 100) for a, b in pari] + [Fr(int(b), 100) for a, b in pari]
        x += [Fr(int(rng.integers(0, 101)), 100) * min(x) for _ in range(2)]
        h = np.array([float(t) for t in vektor_h(x, d, tocki, H, Z, nedol, dol)])
        po_ogliscih = bool((Yc @ h).min() >= -1e-12)
        lp = linprog(np.zeros(G.shape[1]), A_ub=G.astype(float), b_ub=h,
                     bounds=[(None, None)] * G.shape[1], method="highs").status == 0
        ujemanj += po_ogliscih == lp; brez_resitve += not lp
    print(f"(c) kontrola z linearnim programom: ujemanje {ujemanj}/{T} "
          f"(od tega brez rešitve: {brez_resitve})")
