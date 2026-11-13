# Obstoj kopul s predpisanimi vrednostmi z uporabo linearnega programiranja

*[English version below](#existence-of-copulas-with-prescribed-values-using-linear-programming)*

Repozitorij vsebuje kodo in dodatno gradivo k magistrskemu delu z naslovom
**Obstoj kopul s predpisanimi vrednostmi z uporabo linearnega programiranja.**

Magistrsko delo obravnava vprašanje, ali obstaja večrazsežna kopula s predpisanimi vrednostmi v končno mnogo točkah, ki ga z linearnim programiranjem prevedemo na končen seznam neenakosti v podatkih.

## Zgradba repozitorija

- `koda_dve_tocki/`: koda v jeziku Python za dve predpisani točki, z zmanjšano in prvotno različico dualnega problema. Glej `koda_dve_tocki/README.md`.
- `koda_tri_tocke/`: koda v jeziku Python za tri predpisane točke v dimenzijah od 3 do 5 (konfiguracije, zmanjšana različica, točna kontrola s programom Normaliz, naključno iskanje). Glej `koda_tri_tocke/README.md`.
- `slike/`: vse slike iz magistrskega dela. Slike za poglavji o teoretičnem ozadju in pristopu narišeta `slike/slike_teorija_metode.py` in `slike/slika_incidencna_3d.py`, ostale pa skripte v mapah `koda_dve_tocki/` in `koda_tri_tocke/`.
- `stari_poskusi/`: starejši poskusi v programu Mathematica z naključnimi primeri, ki jih hranimo za referenco, vendar jih ne uporabljamo več.

## Zagon kode

```bash
cd koda_dve_tocki
python3 -m venv venv
./venv/bin/pip install pycddlib-standalone numpy scipy matplotlib pynormaliz
./venv/bin/python dve_tocki.py 3+0
```

---

# Existence of copulas with prescribed values using linear programming

This repository contains the code and supplementary materials for the master’s thesis titled
**Existence of copulas with prescribed values using linear programming.**

The thesis investigates the existence problem for multivariate copulas with prescribed values at finitely many points, formulated and studied via linear programming techniques. The thesis, the code comments and the subfolder READMEs are in Slovene.

## Repository structure

- `koda_dve_tocki/`: Python code for two prescribed points, with and without the reduction of the dual problem. See `koda_dve_tocki/README.md`.
- `koda_tri_tocke/`: Python code for three prescribed points in dimensions 3 to 5 (configurations, the reduced version, exact checks with Normaliz, random search). See `koda_tri_tocke/README.md`.
- `slike/`: all figures in the thesis. Figures for the theory and method chapters are drawn by `slike/slike_teorija_metode.py` and `slike/slika_incidencna_3d.py`, the others by the scripts in `koda_dve_tocki/` and `koda_tri_tocke/`.
- `stari_poskusi/`: earlier Mathematica experiments with random instances. They are kept for reference and are no longer used.

## Running the code

```bash
cd koda_dve_tocki
python3 -m venv venv
./venv/bin/pip install pycddlib-standalone numpy scipy matplotlib pynormaliz
./venv/bin/python dve_tocki.py 3+0
```
