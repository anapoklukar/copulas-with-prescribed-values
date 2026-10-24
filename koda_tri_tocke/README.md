# Tri točke v treh dimenzijah

Koda za točko 3: za vsako konfiguracijo treh točk preverimo, ali kopula s predpisanimi vrednostmi vedno obstaja.

## Datoteke

| datoteka | kaj naredi |
|---|---|
| `konfiguracije.py` | našteje konfiguracije (K1 do K10) in nariše sliko `slike/slika_konfiguracije_3tocke.pdf` |
| `tocke.py` | sistem G v_n ≤ h za poljubno število točk in poljubno dimenzijo |
| `testi.py` | preizkusi na primerih, kjer odgovor poznamo |
| `tri_tocke.py` | preverjanje za eno ali vse konfiguracije |
| `zmanjsano_tri.py` | zmanjšana različica: oglišča stožca {λ ≥ 0, H_n^T λ = 0} za vse konfiguracije v dimenziji 3, 4 ali 5 (izpisi `izhod_zmanjsano_tri.txt`, `izhod_zmanjsano_tri_4d.txt`, `izhod_zmanjsano_tri_5d.txt`) |
| `zmanjsano.py` | pomožne funkcije za zmanjšano različico |

## Uporaba

Iz te mape, z okoljem, v katerem so nameščeni `pycddlib-standalone`, `numpy`, `scipy` in `matplotlib`:

    python testi.py              # približno 10 sekund
    python tri_tocke.py K8       # ena konfiguracija
    python tri_tocke.py vse      # vseh deset, približno minuto
    python zmanjsano_tri.py      # zmanjšana različica v 3D, nekaj sekund (potrebuje še pynormaliz)
    python zmanjsano_tri.py 4    # 4D, 24 konfiguracij, približno pol minute
    python zmanjsano_tri.py 5    # 5D, 42 konfiguracij, približno 70 minut

## Kaj preverja `testi.py`

1. Dve točki v dimenzijah 2, 3 in 4: kopula mora vedno obstajati.
2. Tri točke v dveh dimenzijah: kopula mora vedno obstajati.
3. Protiprimer v treh dimenzijah, točke (1/2, 1/2, 1), (1/2, 1, 1/2), (1, 1/2, 1/2) z isto vrednostjo t: rešitev mora obstajati natanko za t med 1/6 in 1/2.

## Kaj izpiše `tri_tocke.py`

Za vsako konfiguracijo:

- število neznank in neenačb sistema,
- število oglišč politopa združljivih podatkov,
- v koliko ogliščih ima sistem rešitev (in koliko rešitev je točno preverjenih),
- v koliko ogliščih rešitve ni (in za koliko je dokaz točno preverjen),
- koliko od 1000 naključnih združljivih podatkov ima rešitev,
- do tri primere podatkov brez rešitve.

Dokaz, da rešitve ni, je vsota neenačb sistema z nenegativnimi utežmi, v kateri se neznanke pokrajšajo, na desni pa ostane negativno število.

Če ima sistem rešitev v vseh ogliščih politopa podatkov, ima rešitev za vse združljive podatke te konfiguracije. Če je v katerem oglišču nima, obstajajo združljivi podatki, za katere kopula ne obstaja.

## Zmanjšana različica (`zmanjsano_tri.py`)

Vsako oglišče stožca da linearno neenakost v podatkih. Neenakost je bodisi pogoj združljivosti (faseta politopa združljivih podatkov) bodisi dodaten pogoj.

| konfiguracija | oglišč | pogojev združljivosti | dodatnih |
|---|---|---|---|
| K1 | 24 | 24 | 0 |
| K2 | 28 | 26 | 2 |
| K3 | 26 | 26 | 0 |
| K4 | 28 | 26 | 2 |
| K5 | 29 | 27 | 2 |
| K6 | 28 | 26 | 2 |
| K7 | 28 | 26 | 2 |
| K8 | 32 | 28 | 4 |
| K9 | 29 | 27 | 2 |
| K10 | 31 | 27 | 4 |

V vseh konfiguracijah so vsi pogoji združljivosti med oglišči. Vsak dodaten pogoj je kršen v kakšnem oglišču politopa združljivih podatkov, zato v K1 in K3 kopula vedno obstaja, v ostalih osmih pa ne. To se ujema z izpisom `tri_tocke.py`.

## Štiri in pet dimenzij

Konfiguracij je 24 v štirih in 42 v petih dimenzijah (preverjeno tudi z Burnsidovo lemo: 3456 / 144 in 30240 / 720). Kot v treh dimenzijah so vsi pogoji združljivosti med oglišči in vsak dodaten pogoj je kršen v kakšnem oglišču politopa združljivih podatkov.

| dimenzija | konfiguracij | oglišč | pogojev združljivosti | število dodatnih pogojev (koliko konfiguracij) | čas na konfiguracijo |
|---|---|---|---|---|---|
| 3 | 10 | 24–32 | 24–28 | 0 (2), 2 (6), 4 (2) | manj kot 1 s |
| 4 | 24 | 30–45 | 30–36 | 0 (3), 3 (8), 4 (6), 9 (7) | približno 1,5 s |
| 5 | 42 | 36–56 | 36–42 | 0 (3), 4 (10), 5 (12), 12 (8), 14 (9) | približno 100 s |

Brez dodatnih pogojev so v vseh treh dimenzijah natanko konfiguracije, v katerih je ena od točk na vseh oseh največja (v 3D K1 in K3, v 4D in 5D K1, K3 in K5). Če je ena točka na vseh oseh najmanjša, to ne zadošča (npr. K2).

