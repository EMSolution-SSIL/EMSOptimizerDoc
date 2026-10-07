---
sidebar_position: 2
---

# ga
This is a Python implementation class of a genetic algorithm for single-objective optimization.  
It is based on real-valued variables\[32\] and can also handle categorical variables (unordered integer variables) and integer variables\[33\].

## Overview
The population evolves by selecting high-quality individuals from the population and offspring of each generation to form the next-generation population.  
Each variable type is processed as follows:  
- Real-valued variables: SBX + polynomial mutation \[6\]
- Integer variables: same as real-valued variables, except that the result is rounded to the nearest integer
- Categorical variables: uniform crossover and mutation to a random value within the category

Individuals that violate constraints are evaluated as follows\[12\]. This prioritizes feasible solutions while accounting for the amount of constraint violation.
```math
f(\boldsymbol{x}) = f(\boldsymbol{x}_0) + r(\boldsymbol{x})
```
$f$: Objective function  
$f(\boldsymbol{x}_0)$: Worst objective-function value in the target population  
$r(\boldsymbol{x})$: Constraint violation

## Configurable keyword arguments
- `population_size: int | null` ... Population size. The default (when not specified) is `10*dim`.
- `num_parents: int | null` ... Number of parents. The default is `population_size`.
- `num_children: int | null` ... Number of offspring. The default is `2*num_parents`.
- `variable_type_counts: dict | null` ... Number of dimensions for each variable type.
    - `categorical: int` ... Number of categorical-variable dimensions.
    - `discrete: int` ... Number of integer-variable dimensions.
    - `continuous: int | null` ... Number of real-valued-variable dimensions. If not specified, it is automatically calculated as `dim - categorical - discrete`.
- `categorical_choice list[list[float | int]] | null` ... Candidate values (integers) for categorical variables, provided as a list for each variable.
- `discrete_values list[list[float | int]] | null` ... Candidate values (integers) for integer variables, provided as a list for each variable.
- `bounds: tuple[float, float] | list[tuple[float, float]]` ... Lower and upper bounds for real-valued variables.
:::tip[Behavior of `bounds`]
- Default (when not specified) ... \[-1, 1\] is applied as the bounds for all variables.
- When `bounds: tuple[float, float]` ... The specified pair is used as the bounds for all variables.
- When `bounds: list[tuple[float, float]]` ... The specified list of pairs is used as the bounds for each variable. The list may end early; subsequent bounds are automatically set to -1 to 1.
:::
- `seed: int | null` ... Random seed. The default is `null` (random seed not fixed).
- `scalarizer_type: str | null` ... Scalarization type. When `evaluator` is multi-objective (when `metrics.objectives` contains multiple values), this converts its objectives to a single objective. Set one of `weighted_sum`, `tchebycheff`, or `pbi`. When `null`, [`metrics.fitness`](../individual.md#optimizationproblemmetrics) is used directly as the single objective. The default is `null`.
- `scalarizer_weights: list[float] | null` ... Scalarization weighting coefficients.
