"""
Slika časa izračuna oglišč politopa Lambda (zmanjšana različica) v odvisnosti od števila celic M.
Dve točki: zahtevnost_normaliz.csv in zahtevnost_cdd.csv (mediana ponovitev, vključno z zagonom programa).
Tri točke: izpisi ../koda_tri_tocke/izhod_zmanjsano_tri*.txt (čas za celotno obdelavo konfiguracije).
Nariše ../slike/slika_zahtevnost.pdf.
"""
import csv, re, statistics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def dve_tocki(datoteka):
    vr = list(csv.DictReader(open(datoteka)))
    d = sorted({int(v["d"]) for v in vr})
    return d, [3 ** x for x in d], [statistics.median(float(v["cas_mediana_s"]) for v in vr if int(v["d"]) == x) for x in d]

def tri_tocke():
    d, cas = [3, 4, 5], []
    for f in ["izhod_zmanjsano_tri.txt", "izhod_zmanjsano_tri_4d.txt", "izhod_zmanjsano_tri_5d.txt"]:
        cas.append(statistics.median(float(t) for t in re.findall(r"čas ([0-9.]+) s", open("../koda_tri_tocke/" + f).read())))
    return d, [4 ** x for x in d], cas

BARVE = {"dve točki, Normaliz": "#2a78d6", "dve točki, cddlib": "#eb6834", "tri točke, Normaliz": "#1baf7a"}
OZNAKE = {"dve točki, Normaliz": "o", "dve točki, cddlib": "s", "tri točke, Normaliz": "^"}
CRNILO, SIVO, MREZA = "#0b0b0b", "#52514e", "#e3e2de"
# velikost ustreza širini besedila (390 pt), zato se pisava v nalogi ne pomanjša
plt.rcParams.update({"font.size": 9, "font.family": "DejaVu Sans"})
fig, ax = plt.subplots(figsize=(5.4, 3.5))
podatki = {"dve točki, Normaliz": dve_tocki("zahtevnost_normaliz.csv"),
           "dve točki, cddlib": dve_tocki("zahtevnost_cdd.csv"),
           "tri točke, Normaliz": tri_tocke()}
for ime, (d, M, t) in podatki.items():
    print(ime, list(zip(d, M, [round(x, 3) for x in t])))
    ax.plot(M, t, color=BARVE[ime], lw=1.8, marker=OZNAKE[ime], ms=6, mec="white", mew=1.2, label=ime, zorder=3)
# oznake dimenzij ob točkah
d, M, t = podatki["dve točki, cddlib"]
for x, m, y in zip(d, M, t):
    if x >= 4: ax.annotate(f"$d = {x}$", xy=(m, y), xytext=(8, -10), textcoords="offset points", fontsize=8, color=SIVO)
d, M, t = podatki["tri točke, Normaliz"]
for x, m, y in zip(d, M, t):
    ax.annotate(f"$d = {x}$", xy=(m, y), xytext=(-8, 9), textcoords="offset points", fontsize=8, color=SIVO, ha="right")
# primerjalna premica, sorazmerna z M^3, skozi točko cddlib v dimenziji 7
d, M, t = podatki["dve točki, cddlib"]
c = t[-1] / M[-1] ** 3
xs = [130, 6561]
ax.plot(xs, [c * x ** 3 for x in xs], color=SIVO, lw=1.2, ls="--", zorder=2)
ax.annotate("sorazmerno z $M^3$", xy=(6561, c * 6561 ** 3), xytext=(-8, 0), textcoords="offset points",
            ha="right", va="center", color=SIVO, fontsize=9)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(6, 9000); ax.set_ylim(0.05, 5e4)
ax.set_xlabel("število celic $M$", color=CRNILO); ax.set_ylabel("čas izračuna [s]", color=CRNILO)
ax.legend(frameon=False, loc="upper left", fontsize=8.5)
ax.grid(axis="y", color=MREZA, lw=0.8); ax.set_axisbelow(True)
for s in ("top", "right"): ax.spines[s].set_visible(False)
for s in ("left", "bottom"): ax.spines[s].set_color(MREZA)
ax.tick_params(which="both", colors=CRNILO, length=0, labelsize=8.5)
fig.tight_layout(); fig.savefig("../slike/slika_zahtevnost.pdf"); fig.savefig("../slike/slika_zahtevnost.png", dpi=150)
