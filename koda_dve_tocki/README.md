# Dve točki: sistem neenačb in oglišča dualnega politopa

Glavna skripta je `dve_tocki.py`. Za izbrano konfiguracijo sestavi sistem, izračuna oglišča dualnega politopa in preveri dobljene neenakosti. Ima dve različici.

- **Zmanjšana različica (privzeto).** Meje ovojnic v nedoločenih vozliščih so odveč: ko so vrednosti na robovih in v obeh točkah določene, je vsaka rešitev z nenegativnimi masami celic že kopula in zato leži med ovojnicama. Ostanejo le uteži celic, iščemo oglišča stožca {λ ≥ 0, H_n^T λ = 0}. Vsako oglišče da linearno neenakost v podatkih.
- **Prvotna različica (`--brez-redukcije`).** Sistem G v_n ≤ h z mejami, kot v članku Omladiča, Vuka in Zalarja. Daje enak odgovor, vendar z bistveno več oglišči.

## Namestitev (enkrat)

    python3 -m venv venv
    ./venv/bin/pip install pycddlib-standalone numpy scipy matplotlib pynormaliz

## Uporaba

    ./venv/bin/python dve_tocki.py 3+0                    # zmanjšana različica
    ./venv/bin/python dve_tocki.py 3+0 --brez-redukcije   # prvotna različica

Konfiguracija `p+r` pomeni: dimenzija je p + r, prva točka je večja od druge v prvih p koordinatah in manjša v zadnjih r. V dveh dimenzijah sta konfiguraciji `2+0` in `1+1`, v treh `3+0` in `2+1`, v štirih `4+0`, `3+1` in `2+2`.

## Rezultati

| dimenzija | konfiguracija | prvotna različica | zmanjšana različica | do zamenjave koordinat |
|---|---|---|---|---|
| 2 | 2+0 | 23 | 10 | 7 |
| 2 | 1+1 | 23 | 10 | 10 |
| 3 | 3+0 | 26 966 | 16 | 8 |
| 3 | 2+1 | 32 224 | 17 | 13 |
| 4 | 4+0 | ni končano | 20 | 8 |
| 4 | 3+1 | ni končano | 21 | 13 |
| 4 | 2+2 | ni končano | 22 | 14 |
| 5 | 5+0 | – | 24 | 8 |
| 5 | 4+1 | – | 25 | 13 |
| 5 | 3+2 | – | 26 | 14 |
| 6 | 6+0 | – | 28 | 8 |
| 6 | 5+1 | – | 29 | 13 |
| 6 | 4+2 | – | 30 | 14 |
| 6 | 3+3 | – | 30 | 14 |

V zmanjšani različici je vsaka dobljena neenakost en sam pogoj združljivosti podatkov (pogoja (3.2) in (3.3) iz članka) ali urejenost koordinat, in sicer v vseh konfiguracijah do dimenzije 6. Izpisi so v datotekah `izhod_zmanjsano_*.txt`, izpisa prvotne različice v treh dimenzijah pa v `izhod_brez_redukcije_*.txt`. Zagon v šestih dimenzijah traja približno minuto in pol.

## Zahtevnost (zmanjšana različica)

Čas in največji porabljeni pomnilnik za izračun oglišč, MacBook Pro (M1 Pro, 16 GB). Algoritem je determinističen, zato navajamo mediano in razpon (najmanj do največ) čez ponovitve: 5 ponovitev do dimenzije 5, 3 v dimenziji 6, 1 v dimenziji 7. Izračun ustavimo, ko traja več kot 30 minut.

| dimenzija | neznanke | oglišča | Normaliz: čas | Normaliz: pomnilnik | cdd: čas | cdd: pomnilnik |
|---|---|---|---|---|---|---|
| 2 | 2 | 10 | 0,2 s | 49 MB | 0,2 s | 45 MB |
| 3 | 18 | 16–17 | 0,2 s | 49 MB | 0,2 s | 45 MB |
| 4 | 70 | 20–22 | 0,2 s | 53 MB | 0,2 s | 45 MB |
| 5 | 230 | 24–26 | 1,0–1,2 s | 76–79 MB | 1,2 s | 53 MB |
| 6 | 714 | 28–30 | 23–25 s | 295 MB | 29 s | 124 MB |
| 7 | 2170 | 32–34 | 20 min | 1,6–1,7 GB | 14 min | 0,61–0,69 GB |
| 8 | 6542 | – | več kot 30 min | – | – | – |

V dimenziji 7 je število oglišč v vseh štirih konfiguracijah enako 4d + 4 + min(r, 2). Podrobni podatki po konfiguracijah so v `zahtevnost_normaliz.csv` in `zahtevnost_cdd.csv`, slika v `slike/slika_zahtevnost.pdf`. Meritve poženemo z `meri_zahtevnost.py`.

## Kaj izpiše zmanjšana različica

| vrstica | pomen |
|---|---|
| `oglišča` | število oglišč stožca {λ ≥ 0, H_n^T λ = 0} |
| `oglišča do zamenjave koordinat` | število oglišč do simetrij konfiguracije |
| `neenakosti` | vsako oglišče, zapisano kot pogoj na podatke |
| `(a)` | vse neenakosti v vseh ogliščih politopa podatkov, točno |
| `(b)` | kontrola: oglišča, zmanjšani sistem in polni sistem dajo enak odgovor na naključnih podatkih |

## Druge datoteke

| datoteka | kaj je |
|---|---|
| `neposredno.py` | neposredno preverjanje z linearnim programom, brez oglišč (izpisi `neposredno_*.txt`) |
| `oglisca_normaliz.py` | oglišča prvotne različice s programom Normaliz |
| `normaliz_4+0.txt` | dnevnik izračuna v 4D (prvotna različica), ustavljen pri 30 GB pomnilnika |
| `rast_4d.py` | slika rasti števila vmesnih kombinacij v 4D (`slike/slika_rast_4d.pdf`) |
