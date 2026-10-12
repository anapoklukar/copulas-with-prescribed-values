(* ====================================== *)
(* 3D COPULA: ONE PRESCRIBED POINT        *)
(* ====================================== *)

ClearAll[Dim3OnePointTestOneInstance, Dim3OnePointTestMany];

Dim3OnePointTestOneInstance[] := Module[{
   u1, u2, u3, q,
   xs, ys, zs,
   vars,
   boundaryConstraints,
   monotoneConstraints,
   volumeConstraints,
   boundsConstraints,
   prescribedConstraint,
   constraints,
   sol},
  
  (* Nakljucni parametri v (0,1) *)
  u1 = RandomReal[];
  u2 = RandomReal[];
  u3 = RandomReal[];
  q = RandomReal[{Max[u1 + u2 + u3 - 2, 0], Min[u1, u2, u3]}];
  
  xs = {0, u1, 1};
  ys = {0, u2, 1};
  zs = {0, u3, 1};
  
  (* Spremenljivke c_{ijk}=C(x_i,y_j,z_k) *)
  vars = Flatten@Table[c[i, j, k], {i, 3}, {j, 3}, {k, 3}];
  
  (* (1) Robni pogoji *)
  boundaryConstraints = Flatten@{
     (* C=0, ko je katera koli koordinata 0 *)
     Table[c[1, j, k] == 0, {j, 3}, {k, 3}],
     Table[c[i, 1, k] == 0, {i, 3}, {k, 3}],
     Table[c[i, j, 1] == 0, {i, 3}, {j, 3}],
     
     (* Margine: C(x,1,1)=x, C(1,y,1)=y, C(1,1,z)=z *)
     Table[c[i, 3, 3] == xs[[i]], {i, 3}],
     Table[c[3, j, 3] == ys[[j]], {j, 3}],
     Table[c[3, 3, k] == zs[[k]], {k, 3}]};
  
  (* (2) Monotonost v vsaki koordinati *)
  monotoneConstraints = Flatten@{
     Table[c[i, j, k] <= c[i + 1, j, k], {i, 1, 2}, {j, 1, 3}, {k, 1, 3}],
     Table[c[i, j, k] <= c[i, j + 1, k], {i, 1, 3}, {j, 1, 2}, {k, 1, 3}],
     Table[c[i, j, k] <= c[i, j, k + 1], {i, 1, 3}, {j, 1, 3}, {k, 1, 2}]};
  
  (* (3) 3-narascanje: C-volumen vsake male kocke je >= 0 *)
  volumeConstraints = Flatten@Table[
     c[i + 1, j + 1, k + 1]
       - c[i + 1, j + 1, k]
       - c[i + 1, j, k + 1]
       - c[i, j + 1, k + 1]
       + c[i + 1, j, k]
       + c[i, j + 1, k]
       + c[i, j, k + 1]
       - c[i, j, k] >= 0,
     {i, 1, 2}, {j, 1, 2}, {k, 1, 2}];
  
  (* (4) Dodatna naravna omejitev za kopulo *)
  boundsConstraints = Thread[0 <= vars <= 1];
  
  (* (5) Predpisana vrednost v tocki (u1,u2,u3) *)
  prescribedConstraint = (c[2, 2, 2] == q);
  
  constraints = Join[
    boundaryConstraints,
    monotoneConstraints,
    volumeConstraints,
    boundsConstraints,
    {prescribedConstraint}];
  
  sol = Quiet@Check[
     LinearOptimization[0, constraints, vars, "PrimalMinimizer", Method -> "Simplex"],
     $Failed];
  
  <|"u" -> {u1, u2, u3},
    "q" -> q,
    "FeasibleQ" -> (sol =!= $Failed),
    "Solution" -> sol|>
];

Dim3OnePointTestMany[n_Integer : 100] := Module[{results, successCount, failCount},
  results = Table[Dim3OnePointTestOneInstance[], n];
  successCount = Count[results, assoc_ /; assoc["FeasibleQ"]];
  failCount = n - successCount;
  <|"TotalRuns" -> n, "Successes" -> successCount, "Failures" -> failCount|>
];
