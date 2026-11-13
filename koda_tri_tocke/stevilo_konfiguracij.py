"""
Število različnih konfiguracij treh točk v dimenzijah od 3 do 7.

Konfiguracija je izbira vrstnega reda treh točk na vsaki osi (6 možnosti na os, skupaj 6^d).
Dve konfiguraciji štejemo za enaki, če ju dobimo eno iz druge s preimenovanjem točk
ali s preureditvijo osi (6 * d! zamenjav). Razrede preštejemo neposredno: vsako še
neobiskano konfiguracijo razširimo na ves njen razred z generatorji teh zamenjav.

Uporaba:   python stevilo_konfiguracij.py          (izpis v izhod_stevilo_konfiguracij.txt)
"""
import itertools, math

PERM = list(itertools.permutations(range(3)))          # vrstni red na osi = rangi točk A, B, C
INDEKS = {p: i for i, p in enumerate(PERM)}

def preimenuj(s, i):
    """Preimenovanje točk s permutacijo s, uporabljeno na vrstnem redu PERM[i]."""
    return INDEKS[tuple(PERM[i][s[t]] for t in range(3))]

def stevilo_razredov(d):
    obiskane, razredi = set(), 0
    for k in itertools.product(range(6), repeat=d):
        if k in obiskane:
            continue
        razredi += 1
        sklad = [k]; obiskane.add(k)
        while sklad:
            c = sklad.pop()
            sosedi = [c[1:] + c[:1], (c[1], c[0]) + c[2:]]               # generatorja preureditev osi
            for s in [(1, 0, 2), (1, 2, 0)]:                             # generatorja preimenovanj točk
                sosedi.append(tuple(preimenuj(s, i) for i in c))
            for n in sosedi:
                if n not in obiskane:
                    obiskane.add(n); sklad.append(n)
    return razredi

if __name__ == "__main__":
    vrstice = ["d   vseh 6^d   zamenjav 6*d!   razredov"]
    for d in range(3, 8):
        vrstice.append(f"{d}   {6 ** d:8d}   {6 * math.factorial(d):13d}   {stevilo_razredov(d):8d}")
        print(vrstice[-1], flush=True)
    open("izhod_stevilo_konfiguracij.txt", "w").write("\n".join(vrstice) + "\n")
