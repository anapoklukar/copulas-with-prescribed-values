"""
Interpolacija dveh točk: sistem G v_n <= h in oglišča dualnega politopa P.

Uporaba:   python dve_tocki.py 3+0                     zmanjšana različica (privzeto)
           python dve_tocki.py 3+0 --brez-redukcije    prvotna različica z mejami

Zmanjšana različica (predlog mentorja, 15. 10. 2026): meje a_n <= v_n <= b_n so odveč.
Ko so vrednosti v določenih vozliščih fiksne, je vsaka rešitev sistema H_n v_n >= -H_d v_d
že diskretna kopula s predpisanimi vrednostmi in zato samodejno leži med ovojnicama.
Ostanejo le uteži celic lambda: oglišča stožca {lambda >= 0, H_n^T lambda = 0}, pogoji pa
so lambda^T H_d v_d >= 0, kar je linearno v podatkih.

Konfiguracija "p+r" pomeni dimenzijo d = p + r, kjer je prva točka večja od
druge v prvih p koordinatah in manjša v zadnjih r koordinatah.

Koraki:
  1. incidenčna matrika H, določena in nedoločena vozlišča, razbitje H = [H_n | H_d]
  2. matrika G = [-H_n; I; -I]
  3. oglišča politopa P = {y >= 0, G^T y = 0, vsota y = 1}  (knjižnica cdd)
     oziroma v zmanjšani različici {lambda >= 0, H_n^T lambda = 0, vsota lambda = 1}
  4. preverjanje neenakosti in kontrole
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
    print(f"  cdd je končal: {sum(1 for g in generatorji if g[0] == 0)} žarkov, sledi točno preverjanje", flush=True)
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
            if len(y) > M:                     # uteži mej (samo v prvotni različici)
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

def vektor_Hd_vd(x, d, tocki, H, Z, dol):
    """H_d v_d: volumni celic, izračunani le iz določenih vrednosti."""
    def znana_vrednost(z):
        if 0 in z: return Fr(0)
        if z == tocki[0]: return x[2 * d]
        if z == tocki[1]: return x[2 * d + 1]
        return min(koordinate(z, x, d))
    vd = [znana_vrednost(Z[j]) for j in dol]
    return [sum(int(H[i, j]) * vd[jj] for jj, j in enumerate(dol) if H[i, j]) for i in range(H.shape[0])]

def vektor_h(x, d, tocki, H, Z, nedol, dol):
    """h = [H_d v_d; b_n; -a_n]."""
    ab = [ovojnici(Z[j], x, d, tocki) for j in nedol]
    return vektor_Hd_vd(x, d, tocki, H, Z, dol) + [b for a, b in ab] + [-a for a, b in ab]

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

def imena_pogojev(d, tocki):
    """Imena vrstic iz neenacbe_podatkov, v istem vrstnem redu."""
    koord = lambda j, k: f"l{k + 1}" if tocki[j][k] == 2 else f"s{k + 1}"
    im = []
    for k in range(d):
        im += [f"s{k + 1} >= 0", f"s{k + 1} <= l{k + 1}", f"l{k + 1} <= 1"]
    for j in range(2):
        vsota = " + ".join(koord(j, k) for k in range(d))
        im += [f"q{j + 1} >= 0   (3.2)", f"q{j + 1} >= {vsota} - {d - 1}   (3.2)"]
        im += [f"q{j + 1} <= {koord(j, k)}   (3.2)" for k in range(d)]
    for i, j in [(0, 1), (1, 0)]:
        im.append(f"q{i + 1} - q{j + 1} <= d_+(x{i + 1}, x{j + 1})   (3.3)")
    return im

def linearna_oblika(f, n):
    """Koeficienti (c0, c1, ..., cn) linearnega izraza f v n spremenljivkah."""
    c0 = f([Fr(0)] * n)
    return [c0] + [f([Fr(int(i == j)) for j in range(n)]) - c0 for i in range(n)]

def ime_neenakosti(oblika, vr, imena):
    """Ime pogoja združljivosti, katerega pozitivni večkratnik je dana neenakost, ali None."""
    for vrstica, ime in zip(vr, imena):
        r = [Fr(int(c)) for c in vrstica]
        i = next(i for i, c in enumerate(r) if c != 0)
        if oblika[i] != 0 and oblika[i] / r[i] > 0 and all(o * r[i] == c * oblika[i] for o, c in zip(oblika, r)):
            return ime
    return None

def oglisca_podatkov(d, tocki):
    """Oglišča politopa združljivih podatkov (cdd), vsako točno preverjeno."""
    vr = neenacbe_podatkov(d, tocki); n = 2 * d + 2
    mat = cdd.matrix_from_array([[int(c) for c in r] for r in vr], rep_type=cdd.RepType.INEQUALITY)
    najdena = set()
    for g in cdd.copy_generators(cdd.polyhedron_from_matrix(mat)).array:
        assert g[0] == 1, "politop podatkov mora biti omejen"
        xf = [Fr(float(t)).limit_denominator(10**6) for t in g[1:]]
        vrednosti = [int(r[0]) + sum(int(c) * t for c, t in zip(r[1:], xf)) for r in vr]
        assert all(v >= 0 for v in vrednosti)
        tesne = vr[[i for i, v in enumerate(vrednosti) if v == 0], 1:]
        assert np.linalg.matrix_rank(tesne) == n                  # res je oglišče
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


def zmanjsana_razlicica(ime, d, p, tocki, H, Z, nedol, dol, rng):
    Hn = H[:, nedol]; k = len(nedol)
    print(f"zmanjšana različica: neznanke le uteži celic, H_n^T: {k} x {H.shape[0]}")
    t0 = time.time()
    L = oglisca_P(-Hn)                                   # {lambda >= 0, H_n^T lambda = 0}
    print(f"oglišča: {len(L)},  čas {time.time() - t0:.1f} s")
    print(f"oglišča do zamenjave koordinat: {stevilo_do_simetrij(L, d, p, Z, nedol)}")

    # vsako oglišče da linearno neenakost v podatkih; poiščemo, kateri pogoj je
    vr, imena = neenacbe_podatkov(d, tocki), imena_pogojev(d, tocki); n = 2 * d + 2
    neimenovanih = 0
    print("neenakosti (vsaka je pogoj združljivosti ali urejenost koordinat):")
    for lam in L:
        f = lambda x: sum(l * c for l, c in zip(lam, vektor_Hd_vd(x, d, tocki, H, Z, dol)) if l)
        im = ime_neenakosti(linearna_oblika(f, n), vr, imena)
        neimenovanih += im is None
        print(f"   {im if im else 'NI ENEGA SAMEGA POGOJA: ' + str(linearna_oblika(f, n))}"
              f"   [{sum(1 for l in lam if l)} celic]")
    print(f"neenakosti, ki niso en sam pogoj združljivosti: {neimenovanih}")

    Lc = np.array(L, dtype=np.int64)
    # (a) v vseh ogliščih politopa podatkov, točno
    X = oglisca_podatkov(d, tocki)
    najmanj = min(int((Lc @ np.array([int(t) for t in vektor_Hd_vd(list(x), d, tocki, H, Z, dol)],
                                       dtype=np.int64)).min()) for x in X)
    print(f"(a) oglišča politopa podatkov: {len(X)};  najmanjša vrednost = {najmanj}")

    # (b) kontrola: zmanjšani sistem, polni sistem in odgovor po ogliščih se ujemajo,
    #     na naključnih podatkih, ki niso nujno združljivi
    G = matrika_G(H, nedol); ujemanj, brez, T = 0, 0, 300
    for _ in range(T):
        pari = [sorted(rng.choice(range(1, 100), 2, replace=False)) for _ in range(d)]
        x = [Fr(int(a), 100) for a, b in pari] + [Fr(int(b), 100) for a, b in pari]
        x += [Fr(int(rng.integers(0, 101)), 100) * min(x) for _ in range(2)]
        hd = np.array([float(t) for t in vektor_Hd_vd(x, d, tocki, H, Z, dol)])
        po_ogliscih = bool((Lc @ hd).min() >= -1e-12)
        zmanjsani = linprog(np.zeros(k), A_ub=-Hn.astype(float), b_ub=hd,
                            bounds=[(None, None)] * k, method="highs").status == 0
        h = np.array([float(t) for t in vektor_h(x, d, tocki, H, Z, nedol, dol)])
        polni = linprog(np.zeros(k), A_ub=G.astype(float), b_ub=h,
                        bounds=[(None, None)] * k, method="highs").status == 0
        ujemanj += po_ogliscih == zmanjsani == polni; brez += not polni
    print(f"(b) kontrola: oglišča = zmanjšani sistem = polni sistem v {ujemanj}/{T} primerih "
          f"(od tega brez rešitve: {brez})")


if __name__ == "__main__":
    brez_redukcije = "--brez-redukcije" in sys.argv
    ime = [a for a in sys.argv[1:] if not a.startswith("--")][0]; p, r = map(int, ime.split("+")); d = p + r
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
    if not brez_redukcije:
        zmanjsana_razlicica(ime, d, p, tocki, H, Z, nedol, dol, rng)
        sys.exit()

    print("prvotna različica: z mejami a_n <= v_n <= b_n")
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
