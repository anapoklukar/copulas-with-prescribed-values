# Existence of copulas with prescribed values using linear programming

This repository contains the code and supplementary materials for the master’s thesis titled 
**Existence of copulas with prescribed values using linear programming.**

The thesis investigates the existence problem for multivariate copulas with prescribed values at finitely many points, formulated and studied via linear programming techniques.

## Repository structure

The implementation is organized according to the dimension of the problem and the number of prescribed points:

- `dim3_one_point.wl` — experiments for one prescribed point in dimension 3,
- `dim3_two_points.wl` — experiments for two prescribed points in dimension 3,
- `dim4_three_points.wl` — experiments for three prescribed points in dimension 4,
- `run_all.wl` — script for running all experiments.

## Running the experiments

To run all experiments from the command line, use:

```bash
wolframscript -file run_all.wl