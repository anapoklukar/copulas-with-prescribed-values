"""
Naključno iskanje protiprimerov za tri točke v treh dimenzijah: kako pogosto naključni
združljivi podatki nimajo kopule.

Ker so dodatni pogoji linearni (zmanjsano_tri.py), lahko za vsak vzorec točno povemo, ali
kopula obstaja: obstaja natanko tedaj, ko so vsi dodatni pogoji njegove konfiguracije nenegativni.

1. Enakomerna porazdelitev na politopu podatkov D, za vsako od desetih konfiguracij.
2. Naključno iskanje v celi kocki: tri točke enakomerno v [0,1]^3, vrednosti zaporedoma
   a) enakomerno med mejama, ki ju dopuščata pogoja združljivosti,
   b) s verjetnostjo 1/4 na spodnji meji, 1/4 na zgornji, sicer enakomerno vmes.
3. Kontrola: na 40 vzorcih brez kopule in 40 vzorcih s kopulo (po dodatnih pogojih) odgovor
   primerjamo z linearnim programom za prvotni sistem.

Uporaba:   python nakljucno.py
"""
import time
from functools import lru_cache
import numpy as np
from fractions import Fraction as Fr
from tocke import Naloga
from konfiguracije import vse_konfiguracije, vrstni_red
from zmanjsano import zarki
from zmanjsano_tri import fasete, linearni_del, oblika

RNG = np.random.default_rng(1)
D, N = 3, 3

@lru_cache(maxsize=None)
def dodatni(konf):
    """Dodatni pogoji konfiguracije kot matrika vrstic (c0, c)."""
    Nl = Naloga(konf); F = fasete(Nl); B = linearni_del(Nl)
    oblike = {oblika(B, lam) for lam in zarki(Nl)}
    return np.array(sorted(oblike - F), dtype=float).reshape(-1, 1 + D * N + N), Nl

def podatkovni_vektor(tocke, q):
    """Vektor p (na osi l koordinate po velikosti, nato q) in konfiguracija (rang točke na vsaki osi)."""
    n = len(tocke); rangi = np.argsort(np.argsort(tocke, axis=1), axis=1)       # (vzorci, točke, osi)
    urejene = np.sort(tocke, axis=1)                                              # (vzorci, točke, osi)
    p = np.concatenate([urejene.transpose(0, 2, 1).reshape(n, -1), q], axis=1)
    return p, rangi

def enakomerno_na_D(konf, M=400_000):
    """Delež podatkov brez kopule pri enakomerni porazdelitvi na D (zavrnitveno vzorčenje)."""
    E, Nl = dodatni(konf)
    pogoji = np.array(Nl.neenacbe_podatkov(), dtype=float)
    sprejeti = brez = 0
    for _ in range(10):
        # na vsaki osi tri enakomerne vrednosti po velikosti, vrednosti q enakomerno v [0,1]
        p = np.concatenate([np.sort(RNG.random((M, N)), axis=1) for _ in range(D)] + [RNG.random((M, N))], axis=1)
        ok = (pogoji[:, :1].T + p @ pogoji[:, 1:].T >= 0).all(axis=1)
        p = p[ok]; sprejeti += len(p)
        if len(E):
            brez += ((E[:, :1].T + p @ E[:, 1:].T) < -1e-12).any(axis=1).sum()
    return sprejeti, brez

def d_plus(u, v):
    return np.maximum(u - v, 0).sum(axis=-1)

def vzorci_v_kocki(nacin, M, rng):
    """Tri točke enakomerno v kocki, vrednosti zaporedoma med mejami združljivosti.
    Vrne podatkovne vektorje, konfiguracije in to, ali kopula ne obstaja."""
    tocke = rng.random((M, N, D))
    q = np.zeros((M, N))
    for j in range(N):
        lo = np.maximum(0, tocke[:, j].sum(axis=1) - (D - 1))
        hi = tocke[:, j].min(axis=1)
        for i in range(j):
            lo = np.maximum(lo, q[:, i] - d_plus(tocke[:, i], tocke[:, j]))
            hi = np.minimum(hi, q[:, i] + d_plus(tocke[:, j], tocke[:, i]))
        u = rng.random(M)
        if nacin == "enakomerno":
            q[:, j] = lo + u * (hi - lo)
        else:
            v = rng.random(M)
            q[:, j] = np.where(v < 0.25, lo, np.where(v < 0.5, hi, lo + u * (hi - lo)))
    p, rangi = podatkovni_vektor(tocke, q)
    brez = np.zeros(M, dtype=bool)
    # vzorce razdelimo po konfiguracijah (vrstni red točk na vsaki osi)
    kljuci = [tuple(tuple(int(rangi[s, j, l]) for j in range(N)) for l in range(D)) for s in range(M)]
    skupine = {}
    for s, k in enumerate(kljuci):
        skupine.setdefault(k, []).append(s)
    for k, idx in skupine.items():
        E, _ = dodatni(k)
        if len(E):
            idx = np.array(idx)
            brez[idx] = ((E[:, :1].T + p[idx] @ E[:, 1:].T) < -1e-12).any(axis=1)
    return p, kljuci, brez

def iskanje_v_kocki(nacin, M=200_000):
    _, _, brez = vzorci_v_kocki(nacin, M, RNG)
    return M, int(brez.sum())

def kontrola_lp(K=40, M=20_000):
    """Odgovor po dodatnih pogojih primerjamo z linearnim programom (prvotni sistem z mejami)."""
    p, kljuci, brez = vzorci_v_kocki("z robovi", M, np.random.default_rng(7))
    izbrani = list(np.flatnonzero(brez)[:K]) + list(np.flatnonzero(~brez)[:K])
    neujemanj = 0
    for s in izbrani:
        Nl = Naloga(kljuci[s])
        podatki = [Fr(float(x)).limit_denominator(10**9) for x in p[s]]
        ima = Nl.resitev(Nl.vektor_h(podatki)) is not None
        neujemanj += ima == bool(brez[s])
    return len(izbrani), neujemanj

if __name__ == "__main__":
    t0 = time.time()
    print("1. Enakomerna porazdelitev na politopu podatkov D")
    for i, konf in enumerate(vse_konfiguracije(), 1):
        sprejeti, brez = enakomerno_na_D(konf)
        print(f"   K{i:<3} osi {vrstni_red(konf)}:  vzorcev {sprejeti:>7},  brez kopule {brez:>5}"
              f"  ({100 * brez / sprejeti:.3f} %)", flush=True)
    print("2. Tri točke enakomerno v kocki, vrednosti zaporedoma med mejami združljivosti")
    for nacin in ("enakomerno", "z robovi"):
        M, brez = iskanje_v_kocki(nacin)
        print(f"   vrednosti {nacin:<11}: vzorcev {M},  brez kopule {brez}  ({100 * brez / M:.3f} %)", flush=True)
    stevilo, neujemanj = kontrola_lp()
    print(f"3. Kontrola z linearnim programom: preverjenih {stevilo} vzorcev, neujemanj {neujemanj}", flush=True)
    print(f"čas {time.time() - t0:.0f} s")
