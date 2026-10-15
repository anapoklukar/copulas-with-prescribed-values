"""
Oglišča politopa P s programom Normaliz (točna aritmetika, več jeder, sproten izpis).

Uporaba:   python oglisca_normaliz.py 3+0 [stevilo_niti]

Izpiše število ekstremnih žarkov stožca {y >= 0, G^T y = 0}, torej število oglišč politopa P.
"""
import sys, time
import numpy as np
import PyNormaliz
from PyNormaliz import Cone
from dve_tocki import razbitje, matrika_G

ime = sys.argv[1]; p, r = map(int, ime.split("+")); d = p + r
if len(sys.argv) > 2:
    PyNormaliz.NmzSetNumberOfNormalizThreads(int(sys.argv[2]))
tocki = [tuple([2] * p + [1] * r), tuple([1] * p + [2] * r)]
H, Z, nedol, dol = razbitje(d, tocki); G = matrika_G(H, nedol); m, k = G.shape
print(f"konfiguracija {ime}: {k} neznank, {m} neenačb", flush=True)
t0 = time.time()
C = Cone(equations=[[int(G[i, s]) for i in range(m)] for s in range(k)],
         inequalities=np.eye(m, dtype=int).tolist())
C.SetVerbose(True)
C.Compute("ExtremeRays")
print(f"oglišča politopa P (Normaliz): {len(C.ExtremeRays())},  čas {time.time() - t0:.0f} s", flush=True)
