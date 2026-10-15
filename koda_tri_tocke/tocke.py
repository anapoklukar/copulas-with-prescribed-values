"""
Splošna različica sistema G v_n <= h za n točk v d dimenzijah.

Konfiguracijo podamo z rangi točk na vsaki osi: konf[os][tocka] je mesto točke
po velikosti na tej osi (0 = najmanjša). Primer za dve točki v treh dimenzijah,
konfiguracija 2+1:  ((1, 0), (1, 0), (0, 1)).

Podatki so vektor  p = (t_11..t_1n, ..., t_d1..t_dn, q_1..q_n),
kjer so t_l1 <= ... <= t_ln po velikosti urejene koordinate točk na osi l,
q_j pa predpisana vrednost v točki j.
"""
import itertools, random
from fractions import Fraction as Fr
from math import lcm
import numpy as np
import cdd
from scipy.optimize import linprog


class Naloga:
    def __init__(self, konf):
        self.konf = tuple(tuple(r) for r in konf)
        self.d, self.n = len(self.konf), len(self.konf[0])
        d, n = self.d, self.n
        # mreža: na vsaki osi indeksi 0..n+1 (0 -> 0, 1..n -> koordinate točk, n+1 -> 1)
        self.tocke = [tuple(self.konf[l][j] + 1 for l in range(d)) for j in range(n)]
        self.Z = list(itertools.product(range(n + 2), repeat=d))
        F = np.zeros((n + 1, n + 2), dtype=int)
        for i in range(n + 1):
            F[i, i], F[i, i + 1] = -1, 1
        H = F
        for _ in range(d - 1):
            H = np.kron(H, F)
        self.H = H                                              # (n+1)^d x (n+2)^d
        vrh = n + 1
        def doloceno(z):
            return 0 in z or sum(1 for i in z if i != vrh) <= 1 or z in self.tocke
        self.dol = [s for s, z in enumerate(self.Z) if doloceno(z)]
        self.nedol = [s for s, z in enumerate(self.Z) if not doloceno(z)]
        k = len(self.nedol)
        self.G = np.vstack([-H[:, self.nedol], np.eye(k, dtype=int), -np.eye(k, dtype=int)])

    # ---------- podatki ----------
    def koordinate(self, z, p):
        d, n = self.d, self.n
        return [Fr(0) if z[l] == 0 else Fr(1) if z[l] == n + 1 else p[l * n + z[l] - 1] for l in range(d)]

    @staticmethod
    def d_plus(u, v):
        return sum(max(a - b, Fr(0)) for a, b in zip(u, v))

    def ovojnici(self, z, p):
        """Spodnja in zgornja ovojnica v vozlišču z."""
        d, n = self.d, self.n
        u = self.koordinate(z, p); q = p[d * n:]
        T = [self.koordinate(t, p) for t in self.tocke]
        a = max([Fr(0), sum(u) - (d - 1)] + [q[j] - self.d_plus(T[j], u) for j in range(n)])
        b = min(u + [q[j] + self.d_plus(u, T[j]) for j in range(n)])
        return a, b

    def vektor_h(self, p):
        """h = [H_d v_d; b_n; -a_n]."""
        d, n = self.d, self.n
        def znana(z):
            if 0 in z: return Fr(0)
            if z in self.tocke: return p[d * n + self.tocke.index(z)]
            return min(self.koordinate(z, p))
        vd = [znana(self.Z[s]) for s in self.dol]
        Hd_vd = [sum(int(self.H[i, s]) * vd[ss] for ss, s in enumerate(self.dol) if self.H[i, s])
                 for i in range(self.H.shape[0])]
        ab = [self.ovojnici(self.Z[s], p) for s in self.nedol]
        return Hd_vd + [b for a, b in ab] + [-a for a, b in ab]

    def neenacbe_podatkov(self):
        """Pogoji za združljive podatke kot vrstice (c0, c) s pomenom c0 + c . p >= 0."""
        d, n = self.d, self.n; N = d * n + n
        def e(i):
            v = np.zeros(N + 1, dtype=int); v[i + 1] = 1; return v
        ena = np.zeros(N + 1, dtype=int); ena[0] = 1
        koord = lambda j, l: e(l * n + self.konf[l][j])
        vr = []
        for l in range(d):                                       # 0 <= t_l1 <= ... <= t_ln <= 1
            vr.append(e(l * n))
            vr += [e(l * n + i + 1) - e(l * n + i) for i in range(n - 1)]
            vr.append(ena - e(l * n + n - 1))
        for j in range(n):
            qj = e(d * n + j)
            vr += [qj, qj - sum(koord(j, l) for l in range(d)) + (d - 1) * ena]      # q_j >= W(x_j)
            vr += [koord(j, l) - qj for l in range(d)]                               # q_j <= M(x_j)
        for i, j in itertools.permutations(range(n), 2):                              # q_i - q_j <= d_+(x_i, x_j)
            dp = sum((koord(i, l) - koord(j, l) for l in range(d) if self.konf[l][i] > self.konf[l][j]), 0 * ena)
            vr.append(dp - e(d * n + i) + e(d * n + j))
        return np.array(vr)

    def oglisca_podatkov(self):
        """Oglišča politopa združljivih podatkov (cdd), vsako točno preverjeno."""
        vr = self.neenacbe_podatkov(); N = vr.shape[1] - 1
        mat = cdd.matrix_from_array([[int(t) for t in r] for r in vr], rep_type=cdd.RepType.INEQUALITY)
        gen = cdd.copy_generators(cdd.polyhedron_from_matrix(mat)).array
        assert all(g[0] == 1 for g in gen), "politop podatkov mora biti omejen"
        najdena = set()
        for g in gen:
            p = [Fr(float(t)).limit_denominator(1000) for t in g[1:]]
            vred = [int(r[0]) + sum(int(c) * t for c, t in zip(r[1:], p)) for r in vr]
            assert all(v >= 0 for v in vred)
            tesne = vr[[i for i, v in enumerate(vred) if v == 0], 1:]
            assert np.linalg.matrix_rank(tesne) == N              # res je oglišče
            najdena.add(tuple(p))
        return sorted(najdena)

    def nakljucni_podatki(self):
        """Naključni združljivi podatki v splošni legi; vrednosti tudi na robu dovoljenega intervala."""
        d, n = self.d, self.n
        def izberi(lo, hi):
            r = random.random()
            return lo if r < 0.25 else hi if r < 0.5 else lo + Fr(random.randint(0, 100), 100) * (hi - lo)
        p = []
        for l in range(d):
            p += [Fr(t, 100) for t in sorted(random.sample(range(1, 100), n))]
        T = [self.koordinate(t, p + [Fr(0)] * n) for t in self.tocke]
        q = []
        for j in range(n):
            lo = max([Fr(0), sum(T[j]) - (d - 1)] + [q[i] - self.d_plus(T[i], T[j]) for i in range(j)])
            hi = min(T[j] + [q[i] + self.d_plus(T[j], T[i]) for i in range(j)])
            assert lo <= hi
            q.append(izberi(lo, hi))
        return p + q

    # ---------- neposredno preverjanje ----------
    def resitev(self, h):
        """Rešitev sistema G v_n <= h ali None."""
        k = self.G.shape[1]
        r = linprog(np.zeros(k), A_ub=self.G.astype(float), b_ub=np.array([float(t) for t in h]),
                    bounds=[(None, None)] * k, method="highs")
        return r.x if r.status == 0 else None

    def tocno_zadosca(self, h, v):
        vf = [Fr(float(t)).limit_denominator(1000) for t in v]
        G = self.G
        return all(sum(int(G[i, s]) * vf[s] for s in range(G.shape[1]) if G[i, s]) <= h[i] for i in range(G.shape[0]))

    def certifikat(self, h):
        """Dokaz, da sistem nima rešitve: y >= 0, G^T y = 0, h^T y < 0 (točno preverjen) ali None."""
        m, k = self.G.shape
        r = linprog(np.array([float(t) for t in h]), A_eq=np.vstack([self.G.T.astype(float), np.ones((1, m))]),
                    b_eq=np.r_[np.zeros(k), 1.0], bounds=[(0, None)] * m, method="highs-ds")
        if r.status != 0 or r.fun > -1e-9:
            return None
        y = r.x / r.x[r.x > 1e-9].min()
        yf = [Fr(float(t)).limit_denominator(1000) for t in y]
        im = lcm(*[t.denominator for t in yf]); y = [int(t * im) for t in yf]
        ok = (all(t >= 0 for t in y)
              and all(sum(int(self.G[i, s]) * y[i] for i in range(m)) == 0 for s in range(k))
              and sum(hi * yi for hi, yi in zip(h, y)) < 0)
        return y if ok else None
