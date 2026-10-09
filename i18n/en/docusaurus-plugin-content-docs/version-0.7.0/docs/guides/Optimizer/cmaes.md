---
sidebar_position: 2
---

# cmaes
This is a Python implementation class for the CMA-ES single-objective optimization algorithm\[4\].  
The algorithm is implemented by calling the Python library `cmaes`\[5\], and this class functions as a wrapper for the `cmaes` library.

## Overview
CMA-ES samples multiple individuals $\boldsymbol{x}$ from a normal distribution as follows\[4\].
```math
\boldsymbol{x} \sim \boldsymbol{m} + \sigma \mathcal{N}(\boldsymbol{0}, \boldsymbol{C})
```
Unlike genetic algorithms, CMA-ES does not have an explicit solution population. Instead, it maintains distribution parameters such as $\boldsymbol{m}, \sigma, \boldsymbol{C}$.  
By updating the distribution parameters based on the relative quality of individuals, the sampled individuals evolve toward better solutions.

Individuals that violate constraints are evaluated as follows\[12\]. This prioritizes feasible solutions while accounting for the amount of constraint violation.
```math
f(\boldsymbol{x}) = f(\boldsymbol{x}_0) + r(\boldsymbol{x})
```
$f$: Objective function  
$f(\boldsymbol{x}_0)$: Worst objective-function value among the sampled individuals  
$r(\boldsymbol{x})$: Constraint violation

## Configurable keyword arguments
- `mean: np.ndarray` ... Initial value of $\boldsymbol{m}$ assigned to `mean`. The default is $\boldsymbol{m} = \boldsymbol{0}$.
:::info
If the length `len(mean)` differs from the number of dimensions `dim`, the following processing is applied.  
- `len(mean) < dim`: `mean` is stored from the beginning and the remaining entries are padded with zeros.
- `len(mean) > dim`: Error.
:::
- `sigma: float` ... Initial step size. The default is `1`.
- `bounds: tuple[float, float] | list[tuple[float, float]]` ... Lower and upper bounds for each variable.
:::tip[Behavior of `bounds`]
- Default (when not specified) ... No bounds.
- When `bounds: tuple[float, float]` ... The specified pair is used as the bounds for all variables.
- When `bounds: list[tuple[float, float]]` ... The specified list of pairs is used as the bounds for each variable. The list may end before all variables are covered; subsequent bounds are then automatically set to -1 to 1.
:::
- `seed: int | null` ... Random seed. The default is `null` (random seed not fixed).
- `population_size int` ... Number of individuals sampled per iteration. The default is the CMA-ES recommended value $4+\lfloor3\ln{n}\rfloor$.
- `scalarizer_type: str | null` ... Scalarization type. When `evaluator` is multi-objective (when `metrics.objectives` contains multiple values), this converts them to a single objective. Set this to one of `weighted_sum`, `tchebycheff`, or `pbi`. When `null`, [`metrics.fitness`](../individual.md#optimizationproblemmetrics) is used directly as the single objective. The default is `null`.
- `scalarizer_weights: list[float] | null` ... Scalarization weighting coefficients.
