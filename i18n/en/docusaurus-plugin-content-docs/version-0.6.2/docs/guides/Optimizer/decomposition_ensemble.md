---
sidebar_position: 4
---

# decomposition_ensemble
This is a Python implementation class based on the MOEA/D multi-objective optimization algorithm\[7\]. It decomposes multi-objective optimization into multiple single-objective problems and solves them with CMA-ES\[8\].  
Unlike the original paper, it does not share information between neighboring problems; each decomposed single-objective problem is solved independently with CMA-ES.

## Overview
MOEA/D decomposes a multi-objective optimization problem into multiple single-objective problems using an appropriate approach and solves each subproblem. The original paper\[7\] introduces the weighted-sum, Tchebycheff, and Penalty-based Boundary Intersection (PBI) approaches.

In this implementation, the decomposed single-objective problems are solved independently with CMA-ES. The solutions obtained during optimization are non-dominated sorted\[6\], and the rank-1 individuals are archived as Pareto-solution candidates.
:::info
When the problem is decomposed into single-objective problems, large differences in objective-function scales can bias the search.  
When using `decomposition_ensemble`, normalizing the objective functions with `coefficient` is recommended. See the [Dmodel multi-objective optimization example](../../../showcase/Dmodel/moo.md) for a specific example.
:::

## Configurable keyword arguments
- `num_decomposition: int` ... Number of decompositions for multi-objective optimization. The default is `10`.
:::tip Tradeoff between computation time and Pareto-solution density with `num_decomposition`
Increasing `num_decomposition` creates a finer decomposition of the multi-objective problem and produces a denser set of Pareto solutions.  
However, computation time increases in proportion to `num_decomposition`.
:::
- `decomposition_type: str` ... Decomposition approach. Set to one of `weighted_sum`, `tchebycheff`, or `pbi`. The default is "tchebycheff".
- `seed: int` ... Random seed. The default is `null` (random seed not fixed).
- `mean: np.ndarray` ... Initial value of CMA-ES $\boldsymbol{m}$. The default is $\boldsymbol{m} = \boldsymbol{0}$.
- `sigma: float` ... Initial standard deviation of CMA-ES $\boldsymbol{C}$. The default is `1`.
- `bounds: tuple[float, float] | list[tuple[float, float]]` ... Lower and upper bounds for each CMA-ES variable.
:::tip Behavior of `bounds`
- Default (when omitted) ... No bounds.
- With `bounds: tuple[float, float]` ... The specified pair is used as the bounds for every variable.
- With `bounds: list[tuple[float, float]]` ... The specified pairs are used as the bounds for each variable. The list may be truncated; bounds after the truncation point are automatically set to -1 to 1.
:::
- `population_size int` ... Number of samples per CMA-ES iteration. The default is the CMA-ES recommendation, $4+\lfloor3\ln{n}\rfloor$.
:::info
The number of samples per optimization iteration is `population_size` × `num_decomposition`.
:::
