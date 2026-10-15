"""
Preizkusi splošne kode na primerih, kjer odgovor poznamo.

Uporaba:   python testi.py
"""
import itertools, random
from fractions import Fraction as Fr
from tocke import Naloga
from konfiguracije import vse_konfiguracije, vrstni_red

random.seed(1)

def preveri(naloga, T=300):
    """Vrne (št. oglišč podatkov, št. rešljivih, št. točno preverjenih, št. rešljivih naključnih od T)."""
    X = naloga.oglisca_podatkov(); res = toc = 0
    for p in X:
        h = naloga.vektor_h(list(p)); v = naloga.resitev(h)
        if v is not None:
            res += 1; toc += naloga.tocno_zadosca(h, v)
    nak = sum(naloga.resitev(naloga.vektor_h(naloga.nakljucni_podatki())) is not None for _ in range(T))
    return len(X), res, toc, nak

print("1. Dve točki (znano: kopula vedno obstaja; pričakujemo 9, 27 in 81 oglišč podatkov)")
for ime, konf in [("2+0", ((1, 0), (1, 0))), ("1+1", ((1, 0), (0, 1))),
                  ("3+0", ((1, 0),) * 3), ("2+1", ((1, 0), (1, 0), (0, 1))),
                  ("4+0", ((1, 0),) * 4)]:
    N = Naloga(konf); o, r, t, nak = preveri(N)
    print(f"   {ime}: neznank {len(N.nedol)}, neenačb {N.G.shape[0]}; oglišča podatkov {o}, rešljivo v {r} "
          f"(točno {t}); naključni {nak}/300")

print("2. Tri točke v dveh dimenzijah (znano: kopula vedno obstaja)")
for t, konf in enumerate(vse_konfiguracije(d=2, n=3), 1):
    N = Naloga(konf); o, r, tc, nak = preveri(N)
    print(f"   {vrstni_red(konf)}: neznank {len(N.nedol)}; oglišča podatkov {o}, rešljivo v {r} (točno {tc}); "
          f"naključni {nak}/300")

print("3. Protiprimer v treh dimenzijah: točke (1/2,1/2,1), (1/2,1,1/2), (1,1/2,1/2), v vseh vrednost t")
print("   (znano: kopula obstaja natanko za t med 1/6 in 1/2)")
pol = Fr(1, 2)
for ime, konf in [(f"K{i + 1}", k) for i, k in enumerate(vse_konfiguracije()) if i + 1 in (8, 10)]:
    N = Naloga(konf)
    for t in [Fr(0), Fr(1, 10), Fr(1, 6) - Fr(1, 1000), Fr(1, 6), Fr(1, 3), Fr(1, 2)]:
        p = [pol, pol, Fr(1)] * 3 + [t, t, t]
        tocke = [N.koordinate(z, p) for z in N.tocke]
        h = N.vektor_h(p); v = N.resitev(h); y = None if v is not None else N.certifikat(h)
        odg = "rešitev obstaja" if v is not None else ("rešitve ni (dokaz točno preverjen)" if y else "rešitve ni")
        print(f"   {ime}, t = {str(t):>9}: {odg}")
    print(f"   {ime}: točke so {[tuple(str(c) for c in x) for x in tocke]}")
