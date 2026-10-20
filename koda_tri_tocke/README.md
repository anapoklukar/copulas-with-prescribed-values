# Tri točke v treh dimenzijah

Koda za točko 3: za vsako konfiguracijo treh točk preverimo, ali kopula s predpisanimi vrednostmi vedno obstaja.

## Datoteke

| datoteka | kaj naredi |
|---|---|
| `konfiguracije.py` | našteje konfiguracije (K1 do K10) in nariše sliko `slike/slika_konfiguracije_3tocke.pdf` |
| `tocke.py` | sistem G v_n ≤ h za poljubno število točk in poljubno dimenzijo |
| `testi.py` | preizkusi na primerih, kjer odgovor poznamo |
| `tri_tocke.py` | preverjanje za eno ali vse konfiguracije |
| `zmanjsano_tri.py` | zmanjšana različica: oglišča stožca {λ ≥ 0, H_n^T λ = 0} za vseh deset konfiguracij (izpis `izhod_zmanjsano_tri.txt`) |
| `zmanjsano.py` | pomožne funkcije za zmanjšano različico |

## Uporaba

Iz te mape, z okoljem, v katerem so nameščeni `pycddlib-standalone`, `numpy`, `scipy` in `matplotlib`:

    python testi.py              # približno 10 sekund
    python tri_tocke.py K8       # ena konfiguracija
    python tri_tocke.py vse      # vseh deset, približno minuto
    python zmanjsano_tri.py      # zmanjšana različica, nekaj sekund (potrebuje še pynormaliz)

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
