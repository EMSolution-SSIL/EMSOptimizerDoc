---
sidebar_position: 3
---

# nsga2
This is a Python implementation class of the NSGA-II multi-objective optimization algorithm\[6\]. The crossover algorithm and other details follow the original paper\[6\].

## Overview
NSGA-II ranks individuals by non-dominated sorting. The population evolves by preferentially retaining individuals with higher ranks. Diversity is maintained by prioritizing individuals of the same rank according to crowding distance (approximately, similarity in objective-function space).

In NSGA-II with constraints, individual $i$ is defined to dominate $j$ in the following cases.
- $i$ is feasible (no constraint violation) and $j$ is infeasible (has a constraint violation).
- Both $i$ and $j$ are infeasible, and $i$ has a smaller constraint violation.
- Both $i$ and $j$ are feasible, and $i$ dominates $j$ in objective-function space.

This dominance relation is applied between all individuals. The individuals with zero dominators are assigned rank 1; after removing rank-1 individuals, those with zero dominators are assigned rank 2, and so on.

## Configurable keyword arguments
- `population_size: int` ... Population size. The default is (number of objectives) $\times 100$.
- `num_children int` ... Number of offspring generated per iteration. The default is the same as `population_size`.
- `bounds: tuple[float, float] | list[tuple[float, float]]` ... Lower and upper bounds for each variable.
:::tip[Behavior of `bounds`]
- Default (when not specified) ... \[-1, 1\] is applied as the bounds for all variables.
- When `bounds: tuple[float, float]` ... The specified pair is used as the bounds for all variables.
- When `bounds: list[tuple[float, float]]` ... The specified list of pairs is used as the bounds for each variable. The list may end early; subsequent bounds are automatically set to -1 to 1.
:::
- `seed: int` ... Random seed. The default is `null` (random seed not fixed).
- `mean: np.ndarray | null` ... Base solution for the initial population. The default is `null` (random initialization).
:::tip[Seeding the initial population]
`mean` is used for seeding the initial population\[19\],\[20\].  
When `mean` is set, optimization starts with a population obtained by mutating `mean`. This is useful when focusing on a single-objective solution or Pareto solutions around an existing design.
:::
:::info
If the length `len(mean)` differs from the number of dimensions `dim`, the following processing is applied.  
- `len(mean) < dim`: `mean` is stored from the beginning and the remaining entries are padded with zeros.
- `len(mean) > dim`: Error.
:::
- `reference_points: np.ndarray | null` ... Reference points for R-NSGA-II. The default is `null` (R-NSGA-II disabled).
:::tip[R-NSGA-II]
R-NSGA-II is a multi-objective optimization algorithm proposed in reference \[21\]. When selecting individuals, it uses the distance to reference points instead of crowding distance, causing solutions close to the reference points to survive preferentially.  
It is useful when ideal objective-function values are known and Pareto solutions around them are of particular interest.
:::
- `reference_weights: np.ndarray | null` ... Objective-weight parameters for R-NSGA-II. The default is `null` (equal weighting).
- `epsilon: float` ... ε parameter representing the solution-thinning distance in R-NSGA-II. The default is `1e-3`.
