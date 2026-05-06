(* ====================================== *)
(* 4D COPULA: THREE PRESCRIBED POINTS     *)
(* ====================================== *)

ClearAll[LogMsg, FHBounds4, GridFrom3, HyperVol4, IndexInGrid,
  Dim4ThreePointsTestOneInstanceFast, Dim4ThreePointsTestManyFast];

LogMsg[msg__] := Print[DateString[{"Hour", ":", "Minute", ":", "Second"}], "  ", Row[{msg}]];

(* 4D Frechet-Hoeffding bounds *)
FHBounds4[p_List] := {Max[0., Total[p] - 3.], Min @@ p};

(* Build grid for one coordinate from 3 points *)
GridFrom3[a_, b_, c_] := Module[{inner = Sort@DeleteDuplicates@N@{a, b, c}}, Join[{0.}, inner, {1.}]];

(* 4D hypervolume on one elementary cell *)
HyperVol4[c_, i_, j_, k_, l_] :=
  Sum[(-1.)^(4 - Total[{e1, e2, e3, e4}])*
    c[i + e1, j + e2, k + e3, l + e4],
    {e1, 0, 1}, {e2, 0, 1}, {e3, 0, 1}, {e4, 0, 1}];

(* Locate index of a value in a grid *)
IndexInGrid[grid_List, val_?NumericQ] := First@First@Position[grid, _?(# == val &)];

Dim4ThreePointsTestOneInstanceFast[
   opts : OptionsPattern[{
      "Verbose" -> True,
      "LogEvery" -> 5,
      "MaxTries" -> 30,
      "LPTimeLimit" -> 20,
      "Method" -> "InteriorPoint"}]] :=
  Module[{verbose, logEvery, maxTries, lpLimit, method, u, v, t, q1,
    q2, q3, xs, ys, zs, ws, nx, ny, nz, nw, iu, ju, ku, lu, iv, jv,
    kv, lv, it, jt, kt, lt, vars, boundaryConstraints,
    monotoneConstraints, volumeConstraints, boundsConstraints,
    constraints, prescribedConstraints, q1min, q1max, q2min, q2max,
    q3min, q3max, tries = 0, sol = $Failed, buildT, consCount, solveT},
   
   verbose = OptionValue["Verbose"];
   logEvery = OptionValue["LogEvery"];
   maxTries = OptionValue["MaxTries"];
   lpLimit = OptionValue["LPTimeLimit"];
   method = OptionValue["Method"];
   
   (* Random points in (0,1)^4, force machine reals *)
   u = N@RandomReal[{0, 1}, 4];
   v = N@RandomReal[{0, 1}, 4];
   t = N@RandomReal[{0, 1}, 4];
   
   (* Build grids *)
   xs = GridFrom3[u[[1]], v[[1]], t[[1]]];
   ys = GridFrom3[u[[2]], v[[2]], t[[2]]];
   zs = GridFrom3[u[[3]], v[[3]], t[[3]]];
   ws = GridFrom3[u[[4]], v[[4]], t[[4]]];
   
   nx = Length[xs];
   ny = Length[ys];
   nz = Length[zs];
   nw = Length[ws];
   
   If[verbose, LogMsg["Build start | grid=", {nx, ny, nz, nw}]];
   
   buildT = AbsoluteTiming[
      vars = Flatten@Table[c[i, j, k, l], {i, nx}, {j, ny}, {k, nz}, {l, nw}];
      
      boundaryConstraints = Flatten@{
         Table[c[1, j, k, l] == 0., {j, ny}, {k, nz}, {l, nw}],
         Table[c[i, 1, k, l] == 0., {i, nx}, {k, nz}, {l, nw}],
         Table[c[i, j, 1, l] == 0., {i, nx}, {j, ny}, {l, nw}],
         Table[c[i, j, k, 1] == 0., {i, nx}, {j, ny}, {k, nz}],
         Table[c[i, ny, nz, nw] == xs[[i]], {i, nx}],
         Table[c[nx, j, nz, nw] == ys[[j]], {j, ny}],
         Table[c[nx, ny, k, nw] == zs[[k]], {k, nz}],
         Table[c[nx, ny, nz, l] == ws[[l]], {l, nw}]};
      
      monotoneConstraints = Flatten@{
         Table[c[i, j, k, l] <= c[i + 1, j, k, l], {i, 1, nx - 1}, {j, 1, ny}, {k, 1, nz}, {l, 1, nw}],
         Table[c[i, j, k, l] <= c[i, j + 1, k, l], {i, 1, nx}, {j, 1, ny - 1}, {k, 1, nz}, {l, 1, nw}],
         Table[c[i, j, k, l] <= c[i, j, k + 1, l], {i, 1, nx}, {j, 1, ny}, {k, 1, nz - 1}, {l, 1, nw}],
         Table[c[i, j, k, l] <= c[i, j, k, l + 1], {i, 1, nx}, {j, 1, ny}, {k, 1, nz}, {l, 1, nw - 1}]};
      
      volumeConstraints = Flatten@Table[
         HyperVol4[c, i, j, k, l] >= 0.,
         {i, 1, nx - 1}, {j, 1, ny - 1}, {k, 1, nz - 1}, {l, 1, nw - 1}];
      
      boundsConstraints = Thread[0. <= vars <= 1.];
      
      iu = IndexInGrid[xs, u[[1]]]; ju = IndexInGrid[ys, u[[2]]];
      ku = IndexInGrid[zs, u[[3]]]; lu = IndexInGrid[ws, u[[4]]];
      iv = IndexInGrid[xs, v[[1]]]; jv = IndexInGrid[ys, v[[2]]];
      kv = IndexInGrid[zs, v[[3]]]; lv = IndexInGrid[ws, v[[4]]];
      it = IndexInGrid[xs, t[[1]]]; jt = IndexInGrid[ys, t[[2]]];
      kt = IndexInGrid[zs, t[[3]]]; lt = IndexInGrid[ws, t[[4]]];
      
      constraints = Join[boundaryConstraints, monotoneConstraints, volumeConstraints, boundsConstraints];
      consCount = Length[constraints];
      
      {q1min, q1max} = FHBounds4[u];
      {q2min, q2max} = FHBounds4[v];
      {q3min, q3max} = FHBounds4[t];
   ][[1]];
   
   If[verbose,
    LogMsg["Build done | vars=", Length[vars], " constraints=", consCount,
      " buildTime(s)=", NumberForm[buildT, {6, 2}],
      " method=", method, " lpLimit(s)=", lpLimit]];
   
   While[tries < maxTries && sol === $Failed,
    q1 = RandomReal[{q1min, q1max}];
    q2 = RandomReal[{q2min, q2max}];
    q3 = RandomReal[{q3min, q3max}];
    
    prescribedConstraints = {c[iu, ju, ku, lu] == q1,
      c[iv, jv, kv, lv] == q2,
      c[it, jt, kt, lt] == q3};
    
    If[verbose && Mod[tries, logEvery] == 0,
     LogMsg["Try ", tries, "/", maxTries, " q=",
       NumberForm[{q1, q2, q3}, {4, 3}], " (solving...)"]];
    
    solveT = AbsoluteTiming[
       sol = TimeConstrained[
          Quiet@Check[
            LinearOptimization[0., Join[constraints, prescribedConstraints], vars,
             "PrimalMinimizer", Method -> method],
            $Failed],
          lpLimit, $Failed];
    ][[1]];
    
    If[verbose && sol =!= $Failed && Mod[tries, logEvery] == 0,
     LogMsg["  solved in ", NumberForm[solveT, {6, 2}], " s  -> FEASIBLE"]];
    
    tries++;
   ];
   
   If[sol === $Failed,
    If[verbose, LogMsg["FAIL after ", maxTries, " tries."]];
    Return[<|"FeasibleQ" -> False,
      "triesUsed" -> tries,
      "gridsizes" -> {nx, ny, nz, nw},
      "vars" -> Length[vars],
      "constraints" -> consCount,
      "u" -> u,
      "v" -> v,
      "t" -> t|>]
   ];
   
   If[verbose, LogMsg["SUCCESS | triesUsed=", tries, " grid=", {nx, ny, nz, nw}]];
   
   <|"FeasibleQ" -> True,
    "triesUsed" -> tries,
    "gridsizes" -> {nx, ny, nz, nw},
    "vars" -> Length[vars],
    "constraints" -> consCount,
    "u" -> u,
    "v" -> v,
    "t" -> t,
    "q1" -> q1,
    "q2" -> q2,
    "q3" -> q3|>
];

Dim4ThreePointsTestManyFast[
   n_Integer : 30,
   opts : OptionsPattern[Dim4ThreePointsTestOneInstanceFast]
] := Module[
  {success = 0, fail = 0, t0, elapsed, r, i},

  t0 = AbsoluteTime[];

  Do[
    r = Dim4ThreePointsTestOneInstanceFast[
      opts,
      "Verbose" -> False
    ];

    If[TrueQ[r["FeasibleQ"]],
      success++,
      fail++
    ];

   , {i, 1, n}];

  elapsed = AbsoluteTime[] - t0;

  <|
    "TotalRuns" -> n,
    "Successes" -> success,
    "Failures" -> fail,
    "FeasiblePercent" -> N[100. success/n],
    "ElapsedSeconds" -> elapsed,
    "AverageSecondsPerRun" -> elapsed/n
  |>
]
