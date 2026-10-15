# Existence of copulas with prescribed values using linear programming

This repository contains the code and supplementary materials for the master’s thesis titled 
**Existence of copulas with prescribed values using linear programming.**

The thesis investigates the existence problem for multivariate copulas with prescribed values at finitely many points, formulated and studied via linear programming techniques.

## Repository structure

- `porocilo/`: report on two prescribed points in dimension 3 (`dve_tocki_3d.pdf`, source `dve_tocki_3d.tex`).
- `koda_dve_tocki/`: Python code for two prescribed points, with and without the reduction of the dual problem. See `koda_dve_tocki/README.md`.
- `koda_tri_tocke/`: Python code for three prescribed points in dimension 3 (configurations, tests, direct check). See `koda_tri_tocke/README.md`.
- `slike/`: figures produced by the code.
- `stari_poskusi/`: earlier Mathematica experiments with random instances. They are kept for reference and are no longer used.

## Running the code

```bash
cd koda_dve_tocki
python3 -m venv venv
./venv/bin/pip install pycddlib-standalone numpy scipy matplotlib pynormaliz
./venv/bin/python dve_tocki.py 3+0
```
