"""
Slika določenih in nedoločenih vozlišč mreže za dve točki (2D in 3D, konfiguracije s p >= r).
Nariše ../slike/slika_vozlisca.pdf.
"""
import itertools, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from dve_tocki import je_doloceno

# indeksi točk na mreži (0 -> 0, 1 -> manjša, 2 -> večja, 3 -> 1)
KONF = {"2+0": [(2, 2), (1, 1)], "1+1": [(2, 1), (1, 2)],
        "3+0": [(2, 2, 2), (1, 1, 1)], "2+1": [(2, 2, 1), (1, 1, 2)]}

ZNANO, NEZNANO, TOCKA, MREZA = "#9aa0a6", "#1f6feb", "#d1495b", "#d9d8d4"
plt.rcParams.update({"font.size": 9, "font.family": "DejaVu Sans", "mathtext.fontset": "cm"})

def slog(z, tocki):
    if z in tocki: return TOCKA, "s", 60
    return (ZNANO, "o", 14) if je_doloceno(z, tocki) else (NEZNANO, "o", 45)

fig = plt.figure(figsize=(6.2, 6.3))
for k, ime in enumerate(["2+0", "1+1", "3+0", "2+1"]):
    tocki = KONF[ime]; d = len(tocki[0])
    ax = fig.add_subplot(2, 2, k + 1, projection="3d" if d == 3 else None)
    for z in itertools.product(range(4), repeat=d):
        c, m, s = slog(z, tocki)
        if d == 3:
            ax.scatter(*z, color=c, marker=m, s=s, depthshade=False)
        else:
            ax.scatter(*z, color=c, marker=m, s=s, zorder=3)
    oznake = [["$0$", f"$s_{i}$", f"$l_{i}$", "$1$"] for i in (1, 2, 3)]
    if d == 2:
        for t in range(4):
            ax.plot([0, 3], [t, t], color=MREZA, lw=0.8, zorder=1); ax.plot([t, t], [0, 3], color=MREZA, lw=0.8, zorder=1)
        ax.set_aspect("equal")
        for s_ in ax.spines.values(): s_.set_visible(False)
        ax.tick_params(length=0)
    else:
        ax.view_init(elev=22, azim=-60)
        ax.set_zticks(range(4)); ax.set_zticklabels(oznake[2])
    ax.set_xticks(range(4)); ax.set_xticklabels(oznake[0])
    ax.set_yticks(range(4)); ax.set_yticklabels(oznake[1])
    ax.set_title(f"$d = {d}$, konfiguracija ${ime}$", fontsize=9.5)
h = [plt.Line2D([], [], ls="", marker="o", ms=4, color=ZNANO, label="določeno vozlišče"),
     plt.Line2D([], [], ls="", marker="s", ms=6, color=TOCKA, label="dana točka"),
     plt.Line2D([], [], ls="", marker="o", ms=6, color=NEZNANO, label="nedoločeno vozlišče")]
fig.legend(handles=h, loc="lower center", ncol=3, frameon=False)
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig("../slike/slika_vozlisca.pdf", bbox_inches="tight", pad_inches=0.03)
fig.savefig("../slike/slika_vozlisca.png", dpi=130, bbox_inches="tight")
