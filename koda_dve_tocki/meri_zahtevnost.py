"""
Meritve časa in pomnilnika za zmanjšano različico, dve točki, dimenzije od 2 naprej.

Vsak zagon teče kot ločen proces, merimo ga z /usr/bin/time -l (skupni čas in največji
porabljeni pomnilnik). Vsako konfiguracijo poženemo večkrat in poročamo mediano in razpon.
Ko en zagon traja več kot MEJA sekund, višjih dimenzij s tem programom ne poganjamo več.

Uporaba:   python meri_zahtevnost.py normaliz [najvisja_dimenzija]
Rezultati: zahtevnost_<program>.csv
"""
import sys, json, re, subprocess, statistics, time, csv

program = sys.argv[1]; dmax = int(sys.argv[2]) if len(sys.argv) > 2 else 10
MEJA = 30 * 60
PY = sys.executable
vrstice = []
konec = False
for d in range(2, dmax + 1):
    for r in range(0, d // 2 + 1):
        ponovitve = 5 if d <= 5 else (3 if d <= 6 else 1)
        casi, pomnilniki, rez = [], [], None
        for _ in range(ponovitve):
            t0 = time.perf_counter()
            try:
                out = subprocess.run(["/usr/bin/time", "-l", PY, "zahtevnost.py", str(d), str(r), program],
                                     capture_output=True, text=True, timeout=MEJA + 60)
            except subprocess.TimeoutExpired:
                print(f"{d - r}+{r}: prekinjeno po {MEJA // 60} minutah", flush=True); konec = True; break
            skupaj = time.perf_counter() - t0
            if out.returncode != 0:
                print(f"{d - r}+{r}: napaka\n{out.stderr[-800:]}", flush=True); konec = True; break
            rez = json.loads(out.stdout.strip().splitlines()[-1])
            pom = int(re.search(r"(\d+)\s+maximum resident set size", out.stderr).group(1))
            casi.append(skupaj); pomnilniki.append(pom / 2**20)
        if rez is None:
            break
        vr = dict(rez, ponovitve=len(casi),
                  cas_mediana_s=round(statistics.median(casi), 2), cas_min_s=round(min(casi), 2),
                  cas_max_s=round(max(casi), 2), pomnilnik_mediana_MB=round(statistics.median(pomnilniki), 1))
        vrstice.append(vr)
        print(f"{vr['konfiguracija']:>5}  d={d}  oglišč {vr['oglisca']:>4} (pričakovano {vr['pricakovano']})  "
              f"čas {vr['cas_mediana_s']:>8} s [{vr['cas_min_s']}, {vr['cas_max_s']}]  "
              f"od tega oglišča {vr['cas_oglisca_s']} s  pomnilnik {vr['pomnilnik_mediana_MB']} MB", flush=True)
        if konec or max(casi) > MEJA:
            konec = True; break
    with open(f"zahtevnost_{program}.csv", "w", newline="") as f:
        if vrstice:
            w = csv.DictWriter(f, fieldnames=list(vrstice[0].keys())); w.writeheader(); w.writerows(vrstice)
    if konec:
        print("ustavljeno: zagon je presegel mejo", flush=True); break
