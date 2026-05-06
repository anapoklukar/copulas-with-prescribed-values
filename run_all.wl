(* ====================================== *)
(* RUN ALL EXPERIMENTS                    *)
(* ====================================== *)

SetDirectory[DirectoryName[$InputFileName]];

Get["dim3_one_point.wl"];
Get["dim3_two_points.wl"];
Get["dim4_three_points.wl"];

Print["==== 3D: one prescribed point ===="];
Print[Dim3OnePointTestMany[100]];

Print["==== 3D: two prescribed points ===="];
Print[Dim3TwoPointsTestMany[100]];

Print["==== 4D: three prescribed points ===="];
Print[Dim4ThreePointsTestManyFast[100, "LPTimeLimit" -> 15, "MaxTries" -> 20]];