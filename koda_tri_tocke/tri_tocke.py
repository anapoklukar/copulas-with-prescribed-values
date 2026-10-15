"""
Tri točke v treh dimenzijah: neposredno preverjanje za izbrano konfiguracijo.

Uporaba:   python tri_tocke.py K1          (ali K2, ..., K10; "vse" za vseh deset)

Za konfiguracijo poišče oglišča politopa združljivih podatkov in v vsakem preveri,
ali ima sistem G v_n <= h rešitev. Kjer je nima, poišče dokaz (vsoto neenačb,
ki vodi v protislovje) in ga točno preveri. Za primerjavo preveri še naključne
združljive podatke.
"""
import sys, time, random
from tocke import Naloga
from konfiguracije import vse_konfiguracije, vrstni_red, tipi_parov

def obdelaj(ime, konf, T=1000):
    random.seed(1); t0 = time.time()
    N = Naloga(konf)
    X = N.oglisca_podatkov()
    resljivo = tocno = brez = dokazano = 0; slabi = []
    for p in X:
        h = N.vektor_h(list(p)); v = N.resitev(h)
        if v is not None:
            resljivo += 1; tocno += N.tocno_zadosca(h, v)
        else:
            brez += 1; y = N.certifikat(h); dokazano += y is not None; slabi.append(p)
    nak = sum(N.resitev(N.vektor_h(N.nakljucni_podatki())) is not None for _ in range(T))
    print(f"{ime}  osi {vrstni_red(konf)}:  neznank {len(N.nedol)}, neenačb {N.G.shape[0]}")
    print(f"   oglišča politopa podatkov: {len(X)};  rešitev obstaja v {resljivo} (točno preverjeno {tocno}), "
          f"rešitve ni v {brez} (dokaz točno preverjen {dokazano})")
    print(f"   naključni združljivi podatki: rešitev obstaja v {nak}/{T};  čas {time.time() - t0:.0f} s")
    for p in slabi[:3]:
        d, n = N.d, N.n
        tocke = [tuple(str(c) for c in N.koordinate(z, list(p))) for z in N.tocke]
        print(f"   primer brez rešitve: točke {tocke}, vrednosti {[str(q) for q in p[d * n:]]}")
    return {"ime": ime, "pari": tipi_parov(konf), "oglisca": len(X), "resljivo": resljivo, "brez": brez, "nakljucni": nak, "T": T}

if __name__ == "__main__":
    K = vse_konfiguracije()
    izbor = range(1, len(K) + 1) if sys.argv[1] == "vse" else [int(sys.argv[1].lstrip("Kk"))]
    rezultati = [obdelaj(f"K{i}", K[i - 1]) for i in izbor]
    if len(rezultati) > 1:
        print("\nPovzetek")
        print(f"{'konf.':6} {'pari tipa 3+0':>13} {'oglišča podatkov':>17} {'rešitev obstaja':>16} {'rešitve ni':>11} {'naključni':>11}")
        for r in rezultati:
            primerljivi = sum(1 for v in r["pari"].values() if v == "3+0")
            print(f"{r['ime']:6} {primerljivi:>13} {r['oglisca']:>17} {r['resljivo']:>16} {r['brez']:>11} "
                  f"{str(r['nakljucni']) + '/' + str(r['T']):>11}")
