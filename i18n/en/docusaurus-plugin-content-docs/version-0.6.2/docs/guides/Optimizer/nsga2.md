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
- `population_size: int` ... Population size. The default is $n \times 10$.
- `num_children int` ... Number of offspring generated per iteration. The default is the same as `population_size`.
- `bounds: tuple[float, float] | list[tuple[float, float]]` ... Lower and upper bounds for each variable.
:::tip Behavior of `bounds`
- Default (when not specified) ... \[-1, 1\] is applied as the bounds for all variables.
- When `bounds: tuple[float, float]` ... The specified pair is used as the bounds for all variables.
- When `bounds: list[tuple[float, float]]` ... The specified list of pairs is used as the bounds for each variable. The list may end early; subsequent bounds are automatically set to -1 to 1.
:::
- `seed: int` ... Random seed. The default is `null` (random seed not fixed).
