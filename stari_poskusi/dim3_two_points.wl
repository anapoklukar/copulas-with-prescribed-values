(* ====================================== *)
(* 3D COPULA: TWO PRESCRIBED POINTS       *)
(* ====================================== *)

ClearAll[FHBounds3, Q2BoundsGivenQ1, Dim3TwoPointsTestOneInstance, Dim3TwoPointsTestMany];

(* Frechet-Hoeffding bounds for a 3-copula at point {x,y,z} *)
FHBounds3[p_List] := {Max[0, Total[p] - 2], Min @@ p};

(* Fast bounds for q2=C(v), given q1=C(u) *)
Q2BoundsGivenQ1[u_List, v_List, q1_?NumericQ] := Module[
  {delta, lbList, ubList, fhV, q2min, q2max},
  
  delta = v - u;
  fhV = FHBounds3[v];
   
  (* Lower bounds for q2 *)
  lbList = {0, fhV[[1]]};
  lbList = Join[lbList, q1 + Select[delta, # < 0 &]];
  If[And @@ Thread[u <= v], lbList = Append[lbList, q1]];
   
  (* Upper bounds for q2 *)
  ubList = {1, fhV[[2]]};
  ubList = Join[ubList, q1 + Select[delta, # > 0 &]];
  If[And @@ Thread[v <= u], ubList = Append[ubList, q1]];
   
  q2min = Max[lbList];
  q2max = Min[ubList];
   
  (* Numeric safety *)
  q2min = Max[0, q2min];
  q2max = Min[1, q2max];
  
  {q2min, q2max}
];

Dim3TwoPointsTestOneInstance[] := Module[{
    u1, u2, u3, v1, v2, v3,
    q1, q2,
    xs, ys, zs,
    iu, ju, ku, iv, jv, kv,
    vars,
    boundaryConstraints,
    monotoneConstraints,
    volumeConstraints,
    boundsConstraints,
    prescribedConstraints,
    constraints,
    sol,
    q1min, q1max, q2min, q2max,
    tries, maxTries},
   
   u1 = RandomReal[];
   u2 = RandomReal[];
   u3 = RandomReal[];
   v1 = RandomReal[];
   v2 = RandomReal[];
   v3 = RandomReal[];
   
   (* V vsaki koordinati zgradimo mrezo {0,min,max,1} *)
   xs = {0, Min[u1, v1], Max[u1, v1], 1};
   ys = {0, Min[u2, v2], Max[u2, v2], 1};
   zs = {0, Min[u3, v3], Max[u3, v3], 1};
   
   (* Spremenljivke c_{ijk}=C(x_i,y_j,z_k) *)
   vars = Flatten@Table[c[i, j, k], {i, 4}, {j, 4}, {k, 4}];
   
   (* (1) Robni pogoji kopule in robne funkcije *)
   boundaryConstraints = Flatten@{
      Table[c[1, j, k] == 0, {j, 4}, {k, 4}],
      Table[c[i, 1, k] == 0, {i, 4}, {k, 4}],
      Table[c[i, j, 1] == 0, {i, 4}, {j, 4}],
      Table[c[i, 4, 4] == xs[[i]], {i, 4}],
      Table[c[4, j, 4] == ys[[j]], {j, 4}],
      Table[c[4, 4, k] == zs[[k]], {k, 4}]};
   
   (* (2) Monotonost po vsaki koordinati *)
   monotoneConstraints = Flatten@{
      Table[c[i, j, k] <= c[i + 1, j, k], {i, 1, 3}, {j, 1, 4}, {k, 1, 4}],
      Table[c[i, j, k] <= c[i, j + 1, k], {i, 1, 4}, {j, 1, 3}, {k, 1, 4}],
      Table[c[i, j, k] <= c[i, j, k + 1], {i, 1, 4}, {j, 1, 4}, {k, 1, 3}]};
   
   (* (3) 3-narascanje: C-prostornine vseh 27 majhnih kock *)
   volumeConstraints = Flatten@Table[
      c[i + 1, j + 1, k + 1]
        - c[i + 1, j + 1, k]
        - c[i + 1, j, k + 1]
        - c[i, j + 1, k + 1]
        + c[i + 1, j, k]
        + c[i, j + 1, k]
        + c[i, j, k + 1]
        - c[i, j, k] >= 0,
      {i, 1, 3}, {j, 1, 3}, {k, 1, 3}];
   
   (* (4) Naravne omejitve kopule *)
   boundsConstraints = Thread[0 <= vars <= 1];
   
   (* Dolocimo indekse tock u in v v mrezi *)
   iu = If[u1 <= v1, 2, 3]; iv = If[u1 <= v1, 3, 2];
   ju = If[u2 <= v2, 2, 3]; jv = If[u2 <= v2, 3, 2];
   ku = If[u3 <= v3, 2, 3]; kv = If[u3 <= v3, 3, 2];
   
   (* Osnovne omejitve brez predpisanih vrednosti *)
   constraints = Join[boundaryConstraints, monotoneConstraints, volumeConstraints, boundsConstraints];
   
   {q1min, q1max} = FHBounds3[{u1, u2, u3}];
   
   tries = 0;
   maxTries = 50;
   sol = $Failed;
   
   While[tries < maxTries && sol === $Failed,
    q1 = RandomReal[{q1min, q1max}];
    {q2min, q2max} = Q2BoundsGivenQ1[{u1, u2, u3}, {v1, v2, v3}, q1];
    
    If[q2min > q2max, tries++; Continue[]];
    
    q2 = RandomReal[{q2min, q2max}];
    prescribedConstraints = {c[iu, ju, ku] == q1, c[iv, jv, kv] == q2};
    
    sol = Quiet@Check[
       LinearOptimization[0, Join[constraints, prescribedConstraints],
         vars, "PrimalMinimizer", Method -> "Simplex"],
       $Failed];
    tries++;
   ];
   
   If[sol === $Failed,
    Print["[FAIL-after-retries] u=", {u1, u2, u3}, " v=", {v1, v2, v3}];
    Return[<|"Status" -> "No feasible (q1,q2) found after retries",
      "u" -> {u1, u2, u3},
      "v" -> {v1, v2, v3},
      "Interval q1" -> {q1min, q1max},
      "Dopustno?" -> False|>]
   ];
   
   <|"u" -> {u1, u2, u3},
    "v" -> {v1, v2, v3},
    "Indeksi u" -> {iu, ju, ku},
    "Indeksi v" -> {iv, jv, kv},
    "Interval q1" -> {q1min, q1max},
    "Interval q2" -> {q2min, q2max},
    "q1" -> q1,
    "q2" -> q2,
    "Dopustno?" -> (sol =!= $Failed)|>
];

Dim3TwoPointsTestMany[n_Integer : 50] := Module[{rezultati},
  rezultati = Table[Dim3TwoPointsTestOneInstance[], n];
  <|"Skupaj" -> n,
    "Uspehi" -> Count[rezultati, a_ /; TrueQ[a["Dopustno?"]]],
    "Neuspehi" -> Count[rezultati, a_ /; KeyExistsQ[a, "Dopustno?"] && ! TrueQ[a["Dopustno?"]]]|>
];
