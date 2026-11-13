"""
Slika incidenčne matrike H pred razbitjem in po razbitju stolpcev na nedoločeni (H_n)
in določeni del (H_d), konfiguracija 3+0. Nariše ../slike/slika_razbitje_H.pdf.
"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from dve_tocki import razbitje

H, Z, nedol, dol = razbitje(3, [(2, 2, 2), (1, 1, 1)])
cmap = ListedColormap(["#c0392b", "white", "#2e86c1"])
# velikost ustreza širini besedila (390 pt), zato se pisava v nalogi ne pomanjša
plt.rcParams.update({"font.size": 9, "font.family": "DejaVu Sans", "mathtext.fontset": "cm"})
fig, axs = plt.subplots(2, 1, figsize=(5.4, 4.6))
for ax, M in [(axs[0], H), (axs[1], H[:, nedol + dol])]:
    ax.imshow(M, cmap=cmap, vmin=-1, vmax=1, aspect="auto", interpolation="nearest")
    ax.set_xticks(np.arange(-.5, 64, 1), minor=True); ax.set_yticks(np.arange(-.5, 27, 1), minor=True)
    ax.grid(which="minor", color="#ddd", lw=0.3); ax.tick_params(which="both", length=0)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_ylabel("celice (27)")
for j in nedol:                                                   # nedoločeni stolpci v naravnem vrstnem redu
    axs[0].add_patch(plt.Rectangle((j - .5, -.5), 1, 27, fill=False, ec="#f2a900", lw=0.9))
    axs[0].text(j, -1.0, "▼", ha="center", va="bottom", color="#f2a900", fontsize=5)
axs[0].set_xlabel("vozlišča (64), nedoločena so označena")
axs[1].axvline(17.5, color="black", lw=1.5)
axs[1].text(8.5, 27.6, "$H_{\\mathrm{n}}$ (18 stolpcev)", ha="center", va="top")
axs[1].text(40.5, 27.6, "$H_{\\mathrm{d}}$ (46 stolpcev)", ha="center", va="top")
plt.tight_layout(h_pad=2.2); plt.savefig("../slike/slika_razbitje_H.pdf"); plt.savefig("../slike/slika_razbitje_H.png", dpi=150)
