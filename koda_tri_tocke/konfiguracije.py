"""
Konfiguracije treh točk v treh dimenzijah.

Konfiguracija pove, kako so tri točke A, B, C razvrščene po velikosti na vsaki osi.
Dve konfiguraciji štejemo za enaki, če ju dobimo eno iz druge s preimenovanjem točk
ali z zamenjavo vrstnega reda osi.

Uporaba:   python konfiguracije.py          (izpiše seznam in nariše sliko)
"""
import itertools

TOCKE = "ABC"

def vse_konfiguracije(d=3, n=3):
    """Vsi razredi konfiguracij; vsak je podan z rangi točk na vsaki osi (0 = najmanjša)."""
    perm = list(itertools.permutations(range(n)))
    osi = list(itertools.permutations(range(d)))
    def predstavnik(k):
        return min(tuple(tuple(r[g[i]] for i in range(n)) for r in (k[a[j]] for j in range(d)))
                   for g in perm for a in osi)
    razredi = {}
    for k in itertools.product(perm, repeat=d):
        razredi.setdefault(predstavnik(k), []).append(k)
    def primerljivih(k):
        return sum(1 for i, j in itertools.combinations(range(n), 2)
                   if len({r[i] < r[j] for r in k}) == 1)
    return sorted(razredi, key=lambda k: (-primerljivih(k), k))

def vrstni_red(k):
    """Za vsako os niz točk od najmanjše do največje, npr. 'ACB'."""
    return ["".join(TOCKE[r.index(q)] for q in range(len(r))) for r in k]

def tipi_parov(k):
    """Za vsak par točk tip dvotočkovne konfiguracije: '3+0' ali '2+1'."""
    out = {}
    for i, j in itertools.combinations(range(len(k[0])), 2):
        manjsa = sum(1 for r in k if r[i] < r[j])
        out[TOCKE[i] + TOCKE[j]] = f"{max(manjsa, len(k) - manjsa)}+{min(manjsa, len(k) - manjsa)}"
    return out


if __name__ == "__main__":
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    K = vse_konfiguracije()
    print(f"število konfiguracij: {len(K)}")
    for t, k in enumerate(K, 1):
        print(f"K{t}:  osi {vrstni_red(k)}   pari {tipi_parov(k)}")

    BARVA = {"A": "#2a78d6", "B": "#eb6834", "C": "#1baf7a"}     # preverjeno za barvno slepoto
    CRNILO, SIVO, MREZA = "#0b0b0b", "#52514e", "#d9d8d4"
    plt.rcParams.update({"font.size": 9, "font.family": "DejaVu Sans"})
    fig = plt.figure(figsize=(13.5, 8.6))
    gs = fig.add_gridspec(4, 5, height_ratios=[3.0, 1.75, 3.0, 1.75], hspace=0.12, wspace=0.10,
                          left=0.035, right=0.985, top=0.93, bottom=0.085)
    lega = [0.2, 0.5, 0.8]                                        # položaj rangov 0, 1, 2

    oznake = []
    for t, k in enumerate(K):
        vr, st = divmod(t, 5)
        # --- zgoraj: točke v kocki ---
        ax = fig.add_subplot(gs[2 * vr, st], projection="3d")
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_zlim(0, 1)
        ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=20, azim=-58)
        ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
        for os_ in (ax.xaxis, ax.yaxis, ax.zaxis):
            os_.set_pane_color((1, 1, 1, 0)); os_.line.set_color(MREZA)
        ax.grid(False)
        for a, b in itertools.combinations(itertools.product([0, 1], repeat=3), 2):
            if sum(x != y for x, y in zip(a, b)) == 1:
                ax.plot(*zip(a, b), color=MREZA, lw=0.8, zorder=1)
        ax.text(0.5, -0.16, 0, "os 1", color=SIVO, fontsize=7, ha="center")
        ax.text(1.16, 0.5, 0, "os 2", color=SIVO, fontsize=7, ha="center")
        ax.text(-0.08, -0.08, 0.5, "os 3", color=SIVO, fontsize=7, ha="center")
        for i, ime in enumerate(TOCKE):
            x, y, z = (lega[k[o][i]] for o in range(3))
            ax.plot([x, x], [y, y], [0, z], color=BARVA[ime], lw=1.0, alpha=0.55, zorder=2)   # navpičnica do tal
            ax.scatter([x], [y], [0], s=10, color=BARVA[ime], alpha=0.55, zorder=2)
            ax.scatter([x], [y], [z], s=95, color=BARVA[ime], edgecolors="white", linewidths=1.6,
                       depthshade=False, zorder=5)
        oznake.append((ax, [tuple(lega[k[o][i]] for o in range(3)) for i in range(3)]))
        pari = tipi_parov(k)
        ax.set_title(f"K{t + 1}", fontsize=11, fontweight="bold", color=CRNILO, pad=-2)
        ax.text2D(0.5, 0.955, "   ".join(f"{p}: {v}" for p, v in pari.items()), transform=ax.transAxes,
                  ha="center", va="top", fontsize=7.5, color=SIVO)

        # --- spodaj: vrstni red točk na vsaki osi ---
        bx = fig.add_subplot(gs[2 * vr + 1, st])
        bx.set_xlim(-0.12, 1.06); bx.set_ylim(-0.75, 2.9); bx.axis("off")
        for o in range(3):
            yy = 2 - o
            bx.plot([0.08, 0.92], [yy, yy], color=MREZA, lw=1.0, solid_capstyle="round", zorder=1)
            bx.text(-0.02, yy, f"os {o + 1}", ha="right", va="center", fontsize=7.5, color=SIVO)
            for i, ime in enumerate(TOCKE):
                xx = lega[k[o][i]]
                bx.scatter([xx], [yy], s=70, color=BARVA[ime], edgecolors="white", linewidths=1.6, zorder=3)
                bx.text(xx, yy + 0.30, ime, ha="center", va="bottom", fontsize=7.5, color=CRNILO)

    # črke ob točkah v kocki: izberemo stran, na kateri ne prekrijejo druge točke
    from mpl_toolkits.mplot3d import proj3d
    fig.canvas.draw()
    for ax, tocke in oznake:
        zaslon = [ax.transData.transform(proj3d.proj_transform(*q, ax.get_proj())[:2]) for q in tocke]
        for i, ime in enumerate(TOCKE):
            drugi = [zaslon[j] for j in range(3) if j != i]
            def prosto(odmik):
                cilj = zaslon[i] + [c * fig.dpi / 72 for c in odmik]
                return min(((cilj[0] - d[0]) ** 2 + (cilj[1] - d[1]) ** 2) ** 0.5 for d in drugi)
            odmik = max([(0, 11), (-12, 0), (12, 0), (0, -13)], key=lambda o: (prosto(o) > 16 * fig.dpi / 72, -[(0, 11), (-12, 0), (12, 0), (0, -13)].index(o)))
            x2, y2 = proj3d.proj_transform(*tocke[i], ax.get_proj())[:2]
            ax.annotate(ime, xy=(x2, y2), xytext=odmik, textcoords="offset points", ha="center", va="center",
                        fontsize=9, fontweight="bold", color=CRNILO, zorder=6)

    fig.suptitle("Konfiguracije treh točk v treh dimenzijah", fontsize=13, fontweight="bold", color=CRNILO, y=0.985)
    rocaji = [Line2D([], [], marker="o", ls="", ms=8, mfc=BARVA[i], mec="white", mew=1.4, label=f"točka {i}") for i in TOCKE]
    fig.legend(handles=rocaji, loc="lower left", bbox_to_anchor=(0.03, 0.012), ncol=3, frameon=False, fontsize=9)
    fig.text(0.985, 0.03, "Na vsaki osi so točke razvrščene od najmanjše (levo) do največje (desno).   "
             "Pod oznako konfiguracije je tip vsakega para točk.",
             ha="right", va="center", fontsize=8.5, color=SIVO)
    fig.savefig("../slike/slika_konfiguracije_3tocke.pdf"); fig.savefig("../slike/slika_konfiguracije_3tocke.png", dpi=150)
