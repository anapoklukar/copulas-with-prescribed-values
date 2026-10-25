"""
Točna kontrola izračunov s plavajočo vejico (cddlib) s programom Normaliz, ki računa točno.

1. Politop podatkov D, vse konfiguracije (dve točki v dimenzijah 2 do 6, tri točke v 3 do 5):
   ali se oglišča in fasete, ki jih da cddlib, natanko ujemajo s točnim izračunom.
2. Dve točki: ali se oglišča politopa Lambda iz cddlib natanko ujemajo z Normaliz.
3. Glavne trditve s točnimi fasetami: dve točki (vsako oglišče je natanko ena faseta politopa D)
   in tri točke v 3D in 4D (število dodatnih pogojev).

Uporaba:   python preveri_tocno.py
"""
import sys, io, time, math, contextlib, os
from fractions import Fraction as Fr
from PyNormaliz import Cone
from tocke import Naloga
from konfiguracije import vse_konfiguracije
from zmanjsano import zarki, konf_dve
from zmanjsano_tri import fasete, linearni_del, oblika, okrajsaj

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "koda_dve_tocki"))
import dve_tocki as dt

def politop_tocno(vrstice):
    """Oglišča in fasete politopa {p : c0 + c . p >= 0} s programom Normaliz (točno)."""
    C = Cone(inhom_inequalities=[[int(t) for t in r[1:]] + [int(r[0])] for r in vrstice])
    C.Compute("VerticesOfPolyhedron", "SupportHyperplanes")
    assert not C.ExtremeRays(), "politop mora biti omejen"
    assert not C.Equations(), "politop mora biti polne dimenzije"
    oglisca = {tuple(Fr(int(x), int(v[-1])) for x in v[:-1]) for v in C.VerticesOfPolyhedron()}
    ploskve = {okrajsaj([h[-1]] + list(h[:-1])) for h in C.SupportHyperplanes()}
    return oglisca, ploskve

def lam_okrajsan(lam):
    g = 0
    for t in lam: g = math.gcd(g, int(t))
    return tuple(int(t) // g for t in lam)

def preveri(ime, N, polni_lambda):
    t0 = time.time()
    X_cdd = set(N.oglisca_podatkov()); F_cdd = fasete(N)
    X_toc, F_toc = politop_tocno(N.neenacbe_podatkov())
    vrstica = (f"{ime}: D oglišča {len(X_toc)} (cdd = točno: {X_cdd == X_toc}), "
               f"fasete {len(F_toc)} (cdd = točno: {F_cdd == F_toc})")
    if polni_lambda:
        L = zarki(N); B = linearni_del(N)
        oblike = {oblika(B, lam) for lam in L}
        dodatnih = len(oblike - F_toc)
        vrstica += (f" | Lambda {len(L)}, vse fasete med oglišči: {F_toc <= oblike}, dodatnih {dodatnih}")
    return vrstica + f"  ({time.time() - t0:.1f} s)", locals()

if __name__ == "__main__":
    vse_ok = True
    print("Dve točki", flush=True)
    for d in range(2, 7):
        for r in range(0, d // 2 + 1):
            p = d - r
            N = Naloga(konf_dve(p, r))
            vr, lok = preveri(f"  {p}+{r}", N, polni_lambda=True)
            # oglišča politopa D tudi iz dve_tocki.py (druga razporeditev spremenljivk)
            tocki = [tuple([2] * p + [1] * r), tuple([1] * p + [2] * r)]
            X2_toc, _ = politop_tocno(dt.neenacbe_podatkov(d, tocki))
            ok_dt = set(dt.oglisca_podatkov(d, tocki)) == X2_toc
            # oglišča Lambda iz cddlib (dve_tocki.py) proti Normaliz
            H, Z, nedol, dol = dt.razbitje(d, tocki)
            with contextlib.redirect_stdout(io.StringIO()):
                L_cdd = {lam_okrajsan(l) for l in dt.oglisca_P(-H[:, nedol])}
            L_toc = {lam_okrajsan(l) for l in zarki(N)}
            # vsako oglišče da natanko eno faseto in vsaka faseta pride od natanko enega oglišča
            bijekcija = len(L_toc) == len(lok["F_toc"]) and lok["dodatnih"] == 0 and lok["F_toc"] <= lok["oblike"]
            vr += f" | dve_tocki.py D: {ok_dt}, Lambda cdd = Normaliz: {L_cdd == L_toc}, oglišča = fasete: {bijekcija}"
            vse_ok &= "False" not in vr
            print(vr, flush=True)

    print("Tri točke", flush=True)
    for d in (3, 4, 5):
        for i, konf in enumerate(vse_konfiguracije(d=d, n=3), 1):
            vr, _ = preveri(f"  {d}D K{i}", Naloga(konf), polni_lambda=(d <= 4))
            vse_ok &= "False" not in vr
            print(vr, flush=True)

    print("\nVSE SE UJEMA" if vse_ok else "\nNEKAJ SE NE UJEMA", flush=True)
