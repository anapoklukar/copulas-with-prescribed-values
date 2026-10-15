"""
Rast števila vmesnih kombinacij pri izračunu oglišč v štirih dimenzijah (Normaliz, konfiguracija 4+0).
Bere dnevnik normaliz_4+0.txt in nariše sliko ../slike/slika_rast_4d.pdf.

Uporaba:   python rast_4d.py
"""
import re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

vrstice = re.findall(r"^gen=(\d+), (\d+) hyp", open("normaliz_4+0.txt", encoding="utf-8").read(), flags=re.M)
korak = [int(a) for a, b in vrstice]; stevilo = [int(b) for a, b in vrstice]
print("korak  kombinacije")
for a, b in zip(korak, stevilo):
    print(f"{a:5d}  {b:>12,}".replace(",", " "))

MODRA, CRNILO, SIVO, MREZA = "#2a78d6", "#0b0b0b", "#52514e", "#e3e2de"
plt.rcParams.update({"font.size": 10, "font.family": "DejaVu Sans"})
fig, ax = plt.subplots(figsize=(7.2, 4.3))
ax.plot(korak, stevilo, color=MODRA, lw=2, solid_capstyle="round", solid_joinstyle="round", zorder=3)
ax.scatter([korak[-1]], [stevilo[-1]], s=60, color=MODRA, edgecolors="white", linewidths=1.6, zorder=4)
ax.set_yscale("log")
ax.axhline(26966, color=SIVO, lw=1, zorder=2)
ax.text(korak[0], 26966 * 1.35, "vsa oglišča v treh dimenzijah (26 966)", color=SIVO, fontsize=9, va="bottom")
ax.annotate("12,9 milijona\n(dosežena omejitev\n30 GB pomnilnika)", xy=(korak[-1], stevilo[-1]), xytext=(10, 0),
            textcoords="offset points", ha="left", va="center", fontsize=9, color=CRNILO)
ax.set_xlabel("korak izračuna (od 221)", color=SIVO)
ax.set_ylabel("število vmesnih kombinacij", color=SIVO)
ax.set_title("Štiri dimenzije, konfiguracija 4+0: rast med izračunom oglišč", fontsize=11, color=CRNILO, loc="left")
ax.set_xlim(korak[0] - 1, korak[-1] + 11)
ax.grid(axis="y", color=MREZA, lw=0.8); ax.set_axisbelow(True)
for s in ("top", "right"): ax.spines[s].set_visible(False)
for s in ("left", "bottom"): ax.spines[s].set_color(MREZA)
ax.tick_params(colors=SIVO, length=0)
fig.tight_layout()
fig.savefig("../slike/slika_rast_4d.pdf"); fig.savefig("../slike/slika_rast_4d.png", dpi=150)
