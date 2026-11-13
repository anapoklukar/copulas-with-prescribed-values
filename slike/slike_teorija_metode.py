"""
Slike za poglavji Teoretično ozadje in Metode.

Nariše sedem slik v mapo, v kateri je ta datoteka:
  slika_kopula.pdf               vzorec vektorja z enakomernima komponentama in graf njegove kopule
  slika_pravokotnik.pdf          volumen pravokotnika iz štirih pravokotnikov z ogliščem v izhodišču
  slika_dopustna.pdf             dopustna množica sistema iz primera
  slika_shema.pdf                shema postopka
  slika_mreza2d.pdf              kanonična mreža za dve točki v dveh dimenzijah
  slika_konfiguracije_2tocki.pdf konfiguraciji 3+0 in 2+1 v kocki
  slika_primer2d.pdf             celice in vrednosti v vozliščih za konfiguracijo 2+0

Velikost slik je enaka velikosti v nalogi, zato so napisi v pravi velikosti.

Uporaba:   python slike_teorija_metode.py [mapa za predoglede png]
"""
import itertools, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D
import numpy as np
from scipy.stats import norm, multivariate_normal

MAPA = os.path.dirname(os.path.abspath(__file__))
PREDOGLED = sys.argv[1] if len(sys.argv) > 1 else None

CRNILO, SIVO, MREZA = "#0b0b0b", "#52514e", "#d9d8d4"
ZNANO, NEZNANO, TOCKA = "#9aa0a6", "#1f6feb", "#d1495b"     # enako kot na sliki slika_vozlisca
PLUS, MINUS, POLNILO = "#2a78d6", "#eb6834", "#e3edf9"
plt.rcParams.update({"font.size": 9, "font.family": "DejaVu Sans", "mathtext.fontset": "cm",
                     "axes.edgecolor": MREZA, "xtick.color": SIVO, "ytick.color": SIVO})

def shrani(fig, ime):
    # robove obrežemo; napise naštejemo posebej, ker obrezovanje napisov v 3D ne upošteva
    obrezi = dict(bbox_inches="tight", pad_inches=0.03,
                  bbox_extra_artists=[t for t in fig.findobj(matplotlib.text.Text) if t.get_text()])
    fig.savefig(os.path.join(MAPA, ime + ".pdf"), **obrezi)
    if PREDOGLED:
        fig.savefig(os.path.join(PREDOGLED, ime + ".png"), dpi=200, **obrezi)
    plt.close(fig)

def brez_okvirja(ax):
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)


def pravokotnik():
    # volumen pravokotnika B dobimo iz štirih pravokotnikov z ogliščem v izhodišču:
    # C(y1, y2) - C(x1, y2) - C(y1, x2) + C(x1, x2)
    a1, b1, a2, b2 = 0.34, 0.76, 0.30, 0.70
    ORANZNO = "#fbe1d3"
    deli = [((b1, b2), "+", "$C(y_1, y_2)$"), ((a1, b2), "-", "$C(x_1, y_2)$"),
            ((b1, a2), "-", "$C(y_1, x_2)$"), ((a1, a2), "+", "$C(x_1, x_2)$")]
    fig, osi = plt.subplots(1, 5, figsize=(5.3, 1.65))
    fig.subplots_adjust(left=0.01, right=0.99, bottom=0.3, top=0.97, wspace=0.42)
    for i, ax in enumerate(osi):
        ax.add_patch(Rectangle((0, 0), 1, 1, fill=False, ec=SIVO, lw=0.8))
        if i < 4:
            (x, y), znak, napis = deli[i]
            barva = PLUS if znak == "+" else MINUS
            ax.add_patch(Rectangle((0, 0), x, y, fc=POLNILO if znak == "+" else ORANZNO, ec=barva, lw=1.0))
            ax.add_patch(Rectangle((a1, a2), b1 - a1, b2 - a2, fill=False, ec=SIVO, lw=0.7, ls=(0, (2, 2))))
            ax.scatter([x], [y], s=14, color=barva, edgecolors="white", linewidths=0.8, zorder=4)
        else:
            barva, napis = CRNILO, "$V_C(B)$"
            ax.add_patch(Rectangle((a1, a2), b1 - a1, b2 - a2, fc=POLNILO, ec=PLUS, lw=1.0))
            ax.text((a1 + b1) / 2, (a2 + b2) / 2, "$B$", ha="center", va="center", fontsize=10, color=CRNILO)
            crta = dict(color=SIVO, lw=0.6, ls=(0, (2, 2)))
            for x in (a1, b1):
                ax.plot([x, x], [0, a2], **crta)
                ax.text(x, -0.04, f"${'x' if x == a1 else 'y'}_1$", ha="center", va="top", fontsize=7.5, color=SIVO)
            for y in (a2, b2):
                ax.plot([0, a1], [y, y], **crta)
                ax.text(-0.04, y, f"${'x' if y == a2 else 'y'}_2$", ha="right", va="center", fontsize=7.5, color=SIVO)
        ax.text(0.5, -0.2, napis, transform=ax.transAxes, ha="center", va="top", fontsize=8.5, color=barva)
        ax.set_xlim(-0.03, 1.03); ax.set_ylim(-0.03, 1.03); ax.set_aspect("equal"); ax.axis("off")
    for i, op in enumerate(["$-$", "$-$", "$+$", "$=$"]):
        levo, desno = osi[i].get_position(), osi[i + 1].get_position()
        fig.text((levo.x1 + desno.x0) / 2, (levo.y0 + levo.y1) / 2, op, ha="center", va="center", fontsize=12, color=CRNILO)
    shrani(fig, "slika_pravokotnik")


def dopustna():
    fig, ax = plt.subplots(figsize=(3.0, 3.5))
    ax.add_patch(Polygon([(1, 1), (2, 1), (2, 2), (1, 3)], fc=POLNILO, ec=PLUS, lw=1.4, zorder=2))
    crta = dict(color=SIVO, lw=0.9, zorder=1)
    ax.plot([1, 1], [0, 4.4], **crta); ax.plot([2, 2], [0, 4.4], **crta)
    ax.plot([0, 3.4], [1, 1], **crta); ax.plot([0, 3.4], [4, 0.6], **crta)
    ax.text(1.06, 4.3, "$x_1 = 1$", ha="left", va="top", fontsize=10, color=SIVO)
    ax.text(2.06, 4.3, "$x_1 = 2$", ha="left", va="top", fontsize=10, color=SIVO)
    ax.text(0.06, 1.06, "$x_2 = 1$", ha="left", va="bottom", fontsize=10, color=SIVO)
    ax.text(2.9, 1.48, "$x_1 + x_2 = 4$", ha="center", va="bottom", fontsize=10, color=SIVO,
            rotation=-45, rotation_mode="anchor", transform_rotates_text=True)
    for (x, y), (dx, dy, ha) in {(1, 1): (-0.08, -0.1, "right"), (2, 1): (0.08, -0.1, "left"),
                                 (2, 2): (0.1, 0.05, "left"), (1, 3): (-0.08, 0.08, "right")}.items():
        ax.scatter([x], [y], s=30, color=PLUS, edgecolors="white", linewidths=1.2, zorder=4)
        ax.text(x + dx, y + dy, f"$({x}, {y})$", ha=ha, va="center", fontsize=10, color=CRNILO)
    ax.set_xlim(0, 3.4); ax.set_ylim(0, 4.4); ax.set_aspect("equal")
    ax.set_xticks(range(4)); ax.set_yticks(range(5))
    ax.set_xlabel("$x_1$", fontsize=11, color=SIVO); ax.set_ylabel("$x_2$", fontsize=11, color=SIVO, rotation=0, labelpad=8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    fig.tight_layout()
    shrani(fig, "slika_dopustna")


def shema():
    fig, ax = plt.subplots(figsize=(5.4, 1.75))
    ax.set_xlim(-0.05, 10.05); ax.set_ylim(0, 3.1); ax.axis("off")
    skatle = [("Podatki", "točke $\\mathbf{x}_j$\nvrednosti $q_j$"),
              ("Mreža", "vozlišča\nin celice"),
              ("Sistem", "$H_{\\mathrm{n}} c_{\\mathrm{n}} \\geq -H_{\\mathrm{d}} c_{\\mathrm{d}}$"),
              ("Politop $\\Lambda$", "oglišča $\\lambda$"),
              ("Neenakosti", "$\\lambda^{\\mathsf{T}} H_{\\mathrm{d}} c_{\\mathrm{d}} \\geq 0$")]
    sirina, razmik, y0, visina = 1.72, 0.35, 1.25, 1.35
    srede = []
    for i, (naslov, vsebina) in enumerate(skatle):
        x0 = i * (sirina + razmik)
        ax.add_patch(FancyBboxPatch((x0, y0), sirina, visina, boxstyle="round,pad=0,rounding_size=0.12",
                                    fc=POLNILO if i in (2, 3) else "white", ec=PLUS if i in (2, 3) else SIVO, lw=1.0))
        ax.text(x0 + sirina / 2, y0 + visina - 0.22, naslov, ha="center", va="top", fontsize=8.5,
                fontweight="bold", color=CRNILO)
        ax.text(x0 + sirina / 2, y0 + 0.42, vsebina, ha="center", va="center", fontsize=8.5, color=CRNILO,
                linespacing=1.3)
        srede.append(x0 + sirina / 2)
        if i:
            ax.add_patch(FancyArrowPatch((x0 - razmik + 0.04, y0 + visina / 2), (x0 - 0.04, y0 + visina / 2),
                                         arrowstyle="-|>", mutation_scale=9, color=SIVO, lw=1.0))
    x_farkas = 3 * (sirina + razmik) - razmik / 2
    ax.text(x_farkas, y0 + visina + 0.08, "Farkasova lema", ha="center", va="bottom", fontsize=7.5, color=SIVO)
    # oklepaj pod sistemom in politopom
    xa, xb, yo = 2 * (sirina + razmik), 3 * (sirina + razmik) + sirina, y0 - 0.2
    ax.plot([xa, xa, xb, xb], [yo + 0.12, yo, yo, yo + 0.12], color=SIVO, lw=0.8)
    ax.text((xa + xb) / 2, yo - 0.12, "odvisno le od konfiguracije",
            ha="center", va="top", fontsize=7.5, color=SIVO)
    ax.text(srede[4], yo - 0.12, "linearne\nv podatkih", ha="center", va="top", fontsize=7.5, color=SIVO)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    shrani(fig, "slika_shema")


def mreza2d():
    t1, t2 = [0, 0.30, 0.65, 1], [0, 0.35, 0.70, 1]
    x1, x2 = (t1[2], t2[1]), (t1[1], t2[2])                    # konfiguracija 1+1
    fig, ax = plt.subplots(figsize=(2.6, 2.75))
    ax.add_patch(Rectangle((t1[2], t2[2]), t1[3] - t1[2], t2[3] - t2[2], fc=POLNILO, ec="none", zorder=0))
    ax.text((t1[2] + 1) / 2, (t2[2] + 1) / 2, "celica", ha="center", va="center", fontsize=8.5, color=PLUS)
    for t in t1:
        ax.plot([t, t], [0, 1], color=SIVO if t in (0, 1) else MREZA, lw=1.0, zorder=1)
    for t in t2:
        ax.plot([0, 1], [t, t], color=SIVO if t in (0, 1) else MREZA, lw=1.0, zorder=1)
    for z in itertools.product(t1, t2):
        if z not in (x1, x2):
            ax.scatter(*z, s=18, color=ZNANO, zorder=3)
    for (x, y), ime in ((x1, "$\\mathbf{x}_1$"), (x2, "$\\mathbf{x}_2$")):
        ax.scatter([x], [y], s=55, marker="s", color=TOCKA, zorder=4)
        ax.text(x + 0.03, y + 0.03, ime, ha="left", va="bottom", fontsize=11, color=CRNILO)
    ax.set_xticks(t1, ["$0$", "$t_{1,1}$", "$t_{1,2}$", "$1$"], fontsize=10)
    ax.set_yticks(t2, ["$0$", "$t_{2,1}$", "$t_{2,2}$", "$1$"], fontsize=10)
    ax.set_xlim(-0.03, 1.03); ax.set_ylim(-0.03, 1.03); ax.set_aspect("equal")
    brez_okvirja(ax)
    rocaji = [Line2D([], [], ls="", marker="o", ms=4.5, color=ZNANO, label="vozlišče"),
              Line2D([], [], ls="", marker="s", ms=6, color=TOCKA, label="dana točka")]
    fig.legend(handles=rocaji, loc="lower center", ncol=2, frameon=False, fontsize=8.5)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    shrani(fig, "slika_mreza2d")


def konfiguracije():
    s, l = (0.30, 0.35, 0.28), (0.72, 0.68, 0.74)
    primeri = [("3+0", (l, s), "$\\mathbf{x}_1$ je večja na vseh treh oseh"),
               ("2+1", ((l[0], l[1], s[2]), (s[0], s[1], l[2])), "$\\mathbf{x}_1$ je večja na oseh 1 in 2,\n$\\mathbf{x}_2$ na osi 3")]
    fig = plt.figure(figsize=(5.4, 2.95))
    osi = []
    for k, (ime, (p1, p2), opis) in enumerate(primeri):
        ax = fig.add_axes([0.08 + 0.5 * k, 0.13, 0.42, 0.80], projection="3d")
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_zlim(0, 1)
        ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=20, azim=-58)
        ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
        for os_ in (ax.xaxis, ax.yaxis, ax.zaxis):
            os_.set_pane_color((1, 1, 1, 0)); os_.line.set_color((1, 1, 1, 0))
        ax.grid(False)
        # ravnine skozi koordinate točk: narišemo, kje sekajo tri zadnje ploskve kocke
        for o in range(3):
            for v in (s[o], l[o]):
                for f, c in ((0, 0), (1, 1), (2, 0)):
                    if f == o:
                        continue
                    t = 3 - o - f
                    p, q = [0.0] * 3, [0.0] * 3
                    p[o] = q[o] = v; p[f] = q[f] = c; p[t], q[t] = 0, 1
                    ax.plot(*zip(p, q), color="#b5b4af", lw=0.8, zorder=1)
        for a, b in itertools.combinations(itertools.product([0, 1], repeat=3), 2):
            if sum(x != y for x, y in zip(a, b)) == 1:
                ax.plot(*zip(a, b), color=SIVO, lw=0.8, zorder=1)
        # kvader, ki ga napenjata točki
        for a, b in itertools.combinations(itertools.product([0, 1], repeat=3), 2):
            if sum(x != y for x, y in zip(a, b)) == 1:
                pa = [(p1, p2)[c][i] for i, c in enumerate(a)]
                pb = [(p1, p2)[c][i] for i, c in enumerate(b)]
                ax.plot(*zip(pa, pb), color=TOCKA, lw=0.8, ls=(0, (2, 2)), alpha=0.8, zorder=2)
        for p, oznaka in ((p1, "$\\mathbf{x}_1$"), (p2, "$\\mathbf{x}_2$")):
            ax.scatter(*([c] for c in p), s=40, marker="s", color=TOCKA, depthshade=False, zorder=5)
            ax.text(p[0], p[1], p[2] + 0.07, oznaka, ha="center", va="bottom", fontsize=10.5, color=CRNILO, zorder=6)
        osi.append(ax)
        fig.text(0.29 + 0.5 * k, 0.955, f"konfiguracija ${ime}$", ha="center", va="top", fontsize=9.5,
                 fontweight="bold", color=CRNILO)
        fig.text(0.29 + 0.5 * k, 0.15, opis, ha="center", va="top", fontsize=9, color=SIVO, linespacing=1.3)
    # oznake osi kot napise v ravnini, sicer jih obrezovanje robov odreže
    from mpl_toolkits.mplot3d import proj3d
    fig.canvas.draw()
    for ax in osi:
        for q, napis in (((0.5, -0.17, 0), "os 1"), ((1.17, 0.5, 0), "os 2"), ((-0.09, -0.09, 0.5), "os 3")):
            x2, y2 = proj3d.proj_transform(*q, ax.get_proj())[:2]
            ax.annotate(napis, xy=(x2, y2), ha="center", va="center", fontsize=7.5, color=SIVO)
    shrani(fig, "slika_konfiguracije_2tocki")


def primer2d():
    x, y = [0, 0.30, 0.65, 1], [0, 0.35, 0.70, 1]
    imx, imy = ["0", "s_1", "l_1", "1"], ["0", "s_2", "l_2", "1"]
    fig, ax = plt.subplots(figsize=(3.8, 3.9))
    for t in x:
        ax.plot([t, t], [0, 1], color=SIVO if t in (0, 1) else MREZA, lw=1.0, zorder=1)
    for t in y:
        ax.plot([0, 1], [t, t], color=SIVO if t in (0, 1) else MREZA, lw=1.0, zorder=1)
    for i, j in itertools.product(range(1, 4), repeat=2):
        ax.text((x[i - 1] + x[i]) / 2, (y[j - 1] + y[j]) / 2, f"$B_{{{i}{j}}}$", ha="center", va="center",
                fontsize=11, color=SIVO)
    notranje = {(1, 1): ("q_2", TOCKA, "s"), (2, 2): ("q_1", TOCKA, "s"), (1, 2): ("u", NEZNANO, "o"),
                (2, 1): ("w", NEZNANO, "o")}
    for i, j in itertools.product(range(4), repeat=2):
        if (i, j) in notranje:
            ime, barva, oblika = notranje[(i, j)]
            ax.scatter([x[i]], [y[j]], s=50 if oblika == "s" else 45, marker=oblika, color=barva, zorder=4)
            ax.text(x[i] + 0.025, y[j] + 0.025, f"${ime}$", ha="left", va="bottom", fontsize=11, color=barva,
                    fontweight="bold", zorder=5)
            continue
        ax.scatter([x[i]], [y[j]], s=16, color=ZNANO, zorder=3)
        if i == 0 or j == 0:                                  # na levem in spodnjem robu je vrednost 0
            continue
        vrednost = imx[i] if j == 3 else imy[j]
        ax.text(x[i] + 0.02, y[j] + 0.02, f"${vrednost}$", ha="left", va="bottom", fontsize=10, color=ZNANO, zorder=5)
    ax.set_xticks(x, [f"${v}$" for v in imx], fontsize=10)
    ax.set_yticks(y, [f"${v}$" for v in imy], fontsize=10)
    ax.set_xlim(-0.03, 1.08); ax.set_ylim(-0.03, 1.08); ax.set_aspect("equal")
    brez_okvirja(ax)
    rocaji = [Line2D([], [], ls="", marker="o", ms=4.5, color=ZNANO, label="določena"),
              Line2D([], [], ls="", marker="s", ms=6, color=TOCKA, label="predpisana"),
              Line2D([], [], ls="", marker="o", ms=6, color=NEZNANO, label="neznanka")]
    fig.legend(handles=rocaji, loc="lower center", ncol=3, frameon=False, fontsize=8.5)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    shrani(fig, "slika_primer2d")


def kopula():
    # vzorec dobimo iz dvorazsežne normalne porazdelitve s korelacijo RHO, ki ga preoblikujemo z robnima
    # porazdelitvenima funkcijama; desno je graf pripadajoče kopule C(u1, u2) = P(U1 <= u1, U2 <= u2)
    RHO, u1, u2 = 0.7, 0.55, 0.62
    rng = np.random.default_rng(3)
    X = rng.multivariate_normal([0, 0], [[1, RHO], [RHO, 1]], size=1000)
    U = norm.cdf(X)
    znotraj = (U[:, 0] <= u1) & (U[:, 1] <= u2)

    fig = plt.figure(figsize=(5.3, 2.75))
    mreza = fig.add_gridspec(2, 3, width_ratios=(4, 0.7, 4.6), height_ratios=(0.7, 4),
                             left=0.06, right=0.99, bottom=0.11, top=0.97, wspace=0.05, hspace=0.05)
    ax = fig.add_subplot(mreza[1, 0])
    zgoraj = fig.add_subplot(mreza[0, 0], sharex=ax)
    desno = fig.add_subplot(mreza[1, 1], sharey=ax)
    ax.add_patch(Rectangle((0, 0), u1, u2, fc=POLNILO, ec=PLUS, lw=1.1, zorder=1))
    ax.scatter(U[~znotraj, 0], U[~znotraj, 1], s=1.6, color=SIVO, alpha=0.55, lw=0, zorder=2)
    ax.scatter(U[znotraj, 0], U[znotraj, 1], s=1.6, color=PLUS, alpha=0.9, lw=0, zorder=2)
    ax.scatter([u1], [u2], s=22, color=PLUS, edgecolors="white", linewidths=1.0, zorder=4)
    ax.add_patch(Rectangle((0, 0), 1, 1, fill=False, ec=SIVO, lw=0.8, zorder=3))
    ax.set_xticks([0, u1, 1], ["$0$", "$u_1$", "$1$"], fontsize=9)
    ax.set_yticks([0, u2, 1], ["$0$", "$u_2$", "$1$"], fontsize=9)
    ax.set_xlim(-0.01, 1.01); ax.set_ylim(-0.01, 1.01)
    brez_okvirja(ax)
    stolpci = np.linspace(0, 1, 11)
    zgoraj.hist(U[:, 0], bins=stolpci, color=MREZA, ec="white", lw=0.6)
    desno.hist(U[:, 1], bins=stolpci, orientation="horizontal", color=MREZA, ec="white", lw=0.6)
    for a in (zgoraj, desno):
        a.axis("off")
    zgoraj.text(-0.03, 0.35, "$U_1$", transform=zgoraj.transAxes, ha="right", va="center", fontsize=9, color=SIVO)
    desno.text(0.35, 1.03, "$U_2$", transform=desno.transAxes, ha="center", va="bottom", fontsize=9, color=SIVO)

    ax3 = fig.add_subplot(mreza[:, 2], projection="3d")
    t = np.linspace(0, 1, 31)
    A, B = np.meshgrid(t, t)
    eps = 1e-9
    tocke = np.column_stack([norm.ppf(np.clip(A.ravel(), eps, 1 - eps)), norm.ppf(np.clip(B.ravel(), eps, 1 - eps))])
    Z = multivariate_normal([0, 0], [[1, RHO], [RHO, 1]]).cdf(tocke).reshape(A.shape)
    Z[:, 0] = 0; Z[0, :] = 0; Z[:, -1] = t; Z[-1, :] = t          # robni pogoji točno
    # vseh 12 robov kocke narišemo sami; robovi na treh zadnjih ploskvah (x = 0, y = 1, z = 0) so za ploskvijo
    ax3.computed_zorder = False
    zadaj = (0, 1, 0)
    for k in range(3):
        for f in itertools.product((0, 1), repeat=2):
            fiks = [i for i in range(3) if i != k]
            konca = [[0, 0, 0], [0, 0, 0]]
            for i, v in zip(fiks, f):
                konca[0][i] = konca[1][i] = v
            konca[1][k] = 1
            skrit = all(v == zadaj[i] for i, v in zip(fiks, f))
            ax3.plot(*zip(*konca), color=MREZA, lw=0.8, zorder=1 if skrit else 3)
    ax3.plot_surface(A, B, Z, color=POLNILO, edgecolor=PLUS, lw=0.25, alpha=0.9, rstride=3, cstride=3, shade=False,
                     zorder=2)
    ax3.plot(t, np.zeros_like(t), 0 * t, color=MINUS, lw=1.6, zorder=4)
    ax3.plot(np.zeros_like(t), t, 0 * t, color=MINUS, lw=1.6, zorder=4)
    ax3.plot(t, np.ones_like(t), t, color=CRNILO, lw=1.6, zorder=4)
    ax3.plot(np.ones_like(t), t, t, color=CRNILO, lw=1.6, zorder=4)
    ax3.view_init(elev=22, azim=-58)
    ax3.set_xlim(0, 1); ax3.set_ylim(0, 1); ax3.set_zlim(0, 1)
    ax3.set_xticks([0, 1]); ax3.set_yticks([1]); ax3.set_zticks([0, 1])      # 0 na osi u2 bi prekril 1 na osi u1
    ax3.tick_params(labelsize=8, pad=-2, colors=SIVO)
    ax3.set_xlabel("$u_1$", fontsize=9, labelpad=-9, color=SIVO)
    ax3.set_ylabel("$u_2$", fontsize=9, labelpad=-9, color=SIVO)
    ax3.text2D(0.5, 0.97, "$C(u_1, u_2)$", transform=ax3.transAxes, fontsize=9.5, color=CRNILO, ha="center", va="top")
    ax3.grid(False)
    for os3 in (ax3.xaxis, ax3.yaxis, ax3.zaxis):
        os3.set_pane_color((1, 1, 1, 0)); os3.pane.set_edgecolor((1, 1, 1, 0)); os3.line.set_color((1, 1, 1, 0))
    ax3.set_box_aspect((1, 1, 0.8), zoom=0.92)
    shrani(fig, "slika_kopula")

if __name__ == "__main__":
    kopula(); pravokotnik(); dopustna(); shema(); mreza2d(); konfiguracije(); primer2d()
