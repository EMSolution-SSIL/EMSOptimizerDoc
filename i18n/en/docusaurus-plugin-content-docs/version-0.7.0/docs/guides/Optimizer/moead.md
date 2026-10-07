---
sidebar_position: 5
---

# moead
This is a Python implementation class of the MOEA/D multi-objective optimization algorithm\[7\].

## Overview
MOEA/D decomposes a multi-objective optimization problem into multiple single-objective problems using an appropriate approach and solves each subproblem. The original paper\[7\] introduces the weighted-sum, Tchebycheff, and Penalty-based Boundary Intersection (PBI) approaches.

In this implementation, one individual is assigned to each decomposed single-objective problem, and the population evolves through SBX crossover between neighboring individuals. The solutions obtained during optimization are non-dominated sorted\[6\], and the rank-1 individuals are archived as Pareto-solution candidates.
:::info
When the problem is decomposed into single-objective problems, large differences in objective-function scales can bias the search.  
When using `moead`, normalizing the objective functions with `coefficient` is recommended.
:::

## Configurable keyword arguments
- `num_grid_division: int` ... Number of grid divisions for multi-objective optimization. The default is `10`.
:::tip[About grid decomposition]
The `moead` implementation decomposes a multi-objective optimization problem into single-objective subproblems on an evenly spaced grid. For example, when there are two objectives, the number of decomposed subproblems is `num_grid_division + 1`.  
Larger values produce a denser Pareto front, but increase computation time.
:::
- `neighborhood_size: int` ... Number of neighboring subproblems, used for operations and decisions such as crossover. The default is `10`.
- `decomposition_type: str` ... Decomposition approach. Set to one of `weighted_sum`, `tchebycheff`, or `pbi`. The default is "tchebycheff".
- `bounds: tuple[float, float] | list[tuple[float, float]]` ... Lower and upper bounds for each CMA-ES variable.
:::tip[Behavior of `bounds`]
- Default (when omitted) ... [-1, 1] is applied as the bounds for every variable.
- With `bounds: tuple[float, float]` ... The specified pair is used as the bounds for every variable.
- With `bounds: list[tuple[float, float]]` ... The specified pairs are used as the bounds for each variable. The list may be truncated; bounds after the truncation point are automatically set to -1 to 1.
:::
- `seed: int | null` ... Random seed. The default is `null` (the random seed is not fixed).
