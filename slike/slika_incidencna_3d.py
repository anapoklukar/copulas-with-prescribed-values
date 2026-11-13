"""Slika: incidenčna matrika H_E = F_2 ⊗ F_2 ⊗ F_2 za dve točki v treh dimenzijah (27 × 64)."""
import os
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

MAPA = os.path.dirname(os.path.abspath(__file__))
F = np.array([[-1, 1, 0, 0], [0, -1, 1, 0], [0, 0, -1, 1]])   # F_2: zgornje krajišče +1
H = np.kron(np.kron(F, F), F)                                   # vozlišča in celice leksikografsko

# velikost ustreza širini besedila (390 pt), zato se pisava v nalogi ne pomanjša
plt.rcParams.update({"font.size": 9, "font.family": "DejaVu Sans"})
fig, ax = plt.subplots(figsize=(5.4, 3.2))
ax.imshow(H, cmap=ListedColormap(["#c0392b", "white", "#2e86c1"]), vmin=-1, vmax=1,
          aspect="auto", interpolation="nearest")
ax.set_xticks(np.arange(-.5, 64, 1), minor=True); ax.set_yticks(np.arange(-.5, 27, 1), minor=True)
ax.grid(which="minor", color="#ddd", lw=0.3); ax.tick_params(which="minor", length=0)
ax.set_xticks(range(0, 64, 4)); ax.set_yticks(range(0, 27, 3))
ax.tick_params(which="major", labelsize=8)
ax.set_xlabel("vozlišča mreže 4×4×4 (64)"); ax.set_ylabel("celice 3×3×3 (27)")
fig.tight_layout()
fig.savefig(os.path.join(MAPA, "incidencna_matrika_3d.pdf"))
fig.savefig(os.path.join(MAPA, "incidencna_matrika_3d.png"), dpi=150)
