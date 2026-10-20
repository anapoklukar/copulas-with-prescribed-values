"""
En meritveni zagon: oglišča zmanjšanega stožca {lambda >= 0, H_n^T lambda = 0} za dve točki.

Uporaba:   python zahtevnost.py 7 0 normaliz      (dimenzija, r, program: normaliz ali cdd)

Matriko H_n sestavimo redko (scipy.sparse), samo na vozliščih brez ničelne koordinate,
saj so vozlišča z ničelno koordinato vedno določena. Izpiše eno vrstico JSON.
"""
import sys, json, time, itertools
import numpy as np
import scipy.sparse as sp

def Hn_redka(d, p, r):
    F1 = sp.csr_matrix(np.array([[1, 0, 0], [-1, 1, 0], [0, -1, 1]]))   # stolpci vozlišč 1, 2, 3
    H = F1
    for _ in range(d - 1):
        H = sp.kron(H, F1, format="csr")
    tocki = [tuple([1] * p + [0] * r), tuple([0] * p + [1] * r)]       # indeksi 0, 1, 2 = vozlišča 1, 2, 3
    nedol = [j for j, t in enumerate(itertools.product(range(3), repeat=d))
             if sum(1 for x in t if x != 2) > 1 and t not in tocki]
    return H[:, nedol]

if __name__ == "__main__":
    d, r, program = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]; p = d - r
    t0 = time.perf_counter()
    Hn = Hn_redka(d, p, r); M, k = Hn.shape
    enacbe = Hn.T.toarray().astype(int).tolist()
    t_sestava = time.perf_counter() - t0
    t1 = time.perf_counter()
    if program == "normaliz":
        from PyNormaliz import Cone
        C = Cone(equations=enacbe, inequalities=np.eye(M, dtype=int).tolist())
        C.Compute("ExtremeRays")
        st = len(C.ExtremeRays())
    else:
        import cdd
        vrstice = [[0] + [int(i == j) for j in range(M)] for i in range(M)] + [[0] + e for e in enacbe]
        mat = cdd.matrix_from_array(vrstice, rep_type=cdd.RepType.INEQUALITY, lin_set=set(range(M, M + k)))
        st = sum(1 for g in cdd.copy_generators(cdd.polyhedron_from_matrix(mat)).array if g[0] == 0)
    t_oglisca = time.perf_counter() - t1
    print(json.dumps({"d": d, "konfiguracija": f"{p}+{r}", "program": program, "celice": M, "neznanke": k,
                      "oglisca": st, "pricakovano": 4 * d + 4 + min(r, 2) if d >= 3 else None,
                      "cas_sestava_s": round(t_sestava, 3), "cas_oglisca_s": round(t_oglisca, 3)}), flush=True)
