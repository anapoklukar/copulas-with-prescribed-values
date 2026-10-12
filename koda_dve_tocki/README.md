# Dve točki: sistem G v_n ≤ h in oglišča dualnega politopa

Ena sama skripta, `dve_tocki.py`. Za izbrano konfiguracijo sestavi sistem, izračuna oglišča politopa P in preveri neenakosti.

## Namestitev (enkrat)

    python3 -m venv venv
    ./venv/bin/pip install pycddlib-standalone numpy scipy

## Uporaba

    ./venv/bin/python dve_tocki.py 3+0
    ./venv/bin/python dve_tocki.py 2+1

V dveh dimenzijah: `2+0` in `1+1` (nekaj sekund). V treh dimenzijah izračun oglišč traja približno pol minute, celoten zagon s preverjanji pa približno dve minuti.

Konfiguracija `p+r` pomeni: dimenzija je p + r, prva točka je večja od druge v prvih p koordinatah in manjša v zadnjih r.

## Kaj izpiše

| vrstica | pomen |
|---|---|
| `H: 27 x 64, določenih 46, nedoločenih 18` | velikost incidenčne matrike, razbitje vozlišč |
| `H_n: 27 x 18, G: 63 x 18` | velikost sistema G v_n ≤ h |
| `oglišča politopa P` | število oglišč, od tega trivialna (a_s ≤ b_s), čas izračuna |
| `oglišča do zamenjave koordinat` | število oglišč do simetrij konfiguracije |
| `(a)` | vse neenakosti h^T y ≥ 0 v vseh ogliščih politopa podatkov, točno |
| `(b)` | vse neenakosti na 2000 naključnih združljivih podatkih |
| `(c)` | kontrola seznama oglišč: odgovor po ogliščih se ujema z linearnim programom |

## Kje je kaj v kodi

| korak | funkcija |
|---|---|
| incidenčna matrika H | `incidencna_matrika` |
| določena in nedoločena vozlišča | `je_doloceno`, `razbitje` |
| matrika G | `matrika_G` |
| oglišča politopa P (knjižnica cdd) | `oglisca_P` |
| ovojnici a, b in vektor h | `ovojnici`, `vektor_h` |
| oglišča politopa podatkov | `oglisca_podatkov` |
