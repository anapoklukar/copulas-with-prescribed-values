"""
Slika časa izračuna oglišč (zmanjšana različica, dve točki) v odvisnosti od dimenzije.
Bere zahtevnost_normaliz.csv in zahtevnost_cdd.csv, nariše ../slike/slika_zahtevnost.pdf.
"""
import csv, statistics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def po_dimenzijah(datoteka):
    vr = list(csv.DictReader(open(datoteka)))
    d = sorted({int(v["d"]) for v in vr})
    return d, [statistics.median(float(v["cas_mediana_s"]) for v in vr if int(v["d"]) == x) for x in d]

BARVE = {"Normaliz": "#2a78d6", "cdd": "#eb6834"}
CRNILO, SIVO, MREZA = "#0b0b0b", "#52514e", "#e3e2de"
plt.rcParams.update({"font.size": 10, "font.family": "DejaVu Sans"})
fig, ax = plt.subplots(figsize=(7.0, 4.2))
for ime, dat in [("Normaliz", "zahtevnost_normaliz.csv"), ("cdd", "zahtevnost_cdd.csv")]:
    d, t = po_dimenzijah(dat)
    ax.plot(d, t, color=BARVE[ime], lw=2, marker="o", ms=6, mec="white", mew=1.5, label=ime, zorder=3)
    ax.annotate(ime, xy=(d[-1], t[-1]), xytext=(8, 7 if ime == "Normaliz" else -7), textcoords="offset points", va="center",
                fontsize=9, color=CRNILO)
ax.axhline(30 * 60, color=SIVO, lw=1, zorder=2)
ax.text(2, 30 * 60 * 1.3, "meja 30 minut (8D se v njej ne konča)", color=SIVO, fontsize=9, va="bottom")
ax.set_yscale("log"); ax.set_xticks(range(2, 9)); ax.set_xlim(1.7, 8.3); ax.set_ylim(0.1, 2e4)
ax.set_xlabel("dimenzija $d$", color=SIVO); ax.set_ylabel("čas izračuna [s]", color=SIVO)
ax.set_title("Dve točki, zmanjšana različica: čas izračuna oglišč", fontsize=11, color=CRNILO, loc="left")
ax.legend(frameon=False, loc="lower right")
ax.grid(axis="y", color=MREZA, lw=0.8); ax.set_axisbelow(True)
for s in ("top", "right"): ax.spines[s].set_visible(False)
for s in ("left", "bottom"): ax.spines[s].set_color(MREZA)
ax.tick_params(colors=SIVO, length=0)
fig.tight_layout(); fig.savefig("../slike/slika_zahtevnost.pdf"); fig.savefig("../slike/slika_zahtevnost.png", dpi=150)
