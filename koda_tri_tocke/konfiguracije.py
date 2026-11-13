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
    plt.rcParams.update({"font.size": 8, "font.family": "DejaVu Sans"})
    # mreža 3 x 4: deset kock, v zadnjih dveh poljih legenda; vrstni red na oseh je v tabeli v nalogi
    fig = plt.figure(figsize=(6.3, 5.2))
    gs = fig.add_gridspec(3, 4, hspace=0.28, wspace=0.02, left=0.03, right=0.99, top=0.95, bottom=0.02)
    lega = [0.2, 0.5, 0.8]                                        # položaj rangov 0, 1, 2

    oznake = []
    for t, k in enumerate(K):
        vr, st = divmod(t, 4)
        ax = fig.add_subplot(gs[vr, st], projection="3d")
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_zlim(0, 1)
        ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=20, azim=-58)
        ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
        for os_ in (ax.xaxis, ax.yaxis, ax.zaxis):
            os_.set_pane_color((1, 1, 1, 0)); os_.line.set_color(MREZA)
        ax.grid(False)
        for a, b in itertools.combinations(itertools.product([0, 1], repeat=3), 2):
            if sum(x != y for x, y in zip(a, b)) == 1:
                ax.plot(*zip(a, b), color=MREZA, lw=0.8, zorder=1)
        ax.text(0.5, -0.18, 0, "os 1", color=SIVO, fontsize=6.5, ha="center")
        ax.text(1.18, 0.5, 0, "os 2", color=SIVO, fontsize=6.5, ha="center")
        ax.text(-0.1, -0.1, 0.5, "os 3", color=SIVO, fontsize=6.5, ha="center")
        for i, ime in enumerate(TOCKE):
            x, y, z = (lega[k[o][i]] for o in range(3))
            ax.plot([x, x], [y, y], [0, z], color=BARVA[ime], lw=1.0, alpha=0.55, zorder=2)   # navpičnica do tal
            ax.scatter([x], [y], [0], s=8, color=BARVA[ime], alpha=0.55, zorder=2)
            ax.scatter([x], [y], [z], s=60, color=BARVA[ime], edgecolors="white", linewidths=1.2,
                       depthshade=False, zorder=5)
        oznake.append((ax, [tuple(lega[k[o][i]] for o in range(3)) for i in range(3)]))
        pari = tipi_parov(k)
        ax.set_title(f"K{t + 1}", fontsize=10, fontweight="bold", color=CRNILO, pad=8)
        ax.text2D(0.5, 1.0, "  ".join(f"{p} {v}" for p, v in pari.items()), transform=ax.transAxes,
                  ha="center", va="top", fontsize=6.5, color=SIVO)

    # črke ob točkah v kocki: izberemo stran, na kateri ne prekrijejo druge točke
    from mpl_toolkits.mplot3d import proj3d
    fig.canvas.draw()
    smeri = [(0, 9), (-10, 0), (10, 0), (0, -10)]
    for ax, tocke in oznake:
        zaslon = [ax.transData.transform(proj3d.proj_transform(*q, ax.get_proj())[:2]) for q in tocke]
        for i, ime in enumerate(TOCKE):
            drugi = [zaslon[j] for j in range(3) if j != i]
            def prosto(odmik):
                cilj = zaslon[i] + [c * fig.dpi / 72 for c in odmik]
                return min(((cilj[0] - d[0]) ** 2 + (cilj[1] - d[1]) ** 2) ** 0.5 for d in drugi)
            odmik = max(smeri, key=lambda o: (prosto(o) > 13 * fig.dpi / 72, -smeri.index(o)))
            x2, y2 = proj3d.proj_transform(*tocke[i], ax.get_proj())[:2]
            ax.annotate(ime, xy=(x2, y2), xytext=odmik, textcoords="offset points", ha="center", va="center",
                        fontsize=8, fontweight="bold", color=CRNILO, zorder=6)

    lx = fig.add_subplot(gs[2, 2:]); lx.axis("off")
    rocaji = [Line2D([], [], marker="o", ls="", ms=8, mfc=BARVA[i], mec="white", mew=1.4, label=f"točka {i}") for i in TOCKE]
    lx.legend(handles=rocaji, loc="center", frameon=False, fontsize=9)
    fig.savefig("../slike/slika_konfiguracije_3tocke.pdf"); fig.savefig("../slike/slika_konfiguracije_3tocke.png", dpi=150)
