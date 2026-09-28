---
sidebar_position: 4
---

# Individual-related object API
This page introduces the classes used to manage individuals throughout EMSOptimizer.  
They can be imported from `emsopt_engine.individual`.  
These classes are used primarily to exchange individual information between `optimizer` and `evaluator`.

## `OptimizationProblemMetrics`
```python
@dataclass
class OptimizationProblemMetrics:
    objectives: list[float] = field(default_factory=list)
    ineq_constraints: list[float] = field(default_factory=list)
    eq_constraints: list[float] = field(default_factory=list)
    other_metrics: list[float] = field(default_factory=list)
    _fitness: float | None = None
```
A data class that stores objective values and constraint information for an optimization problem.

### Attributes
#### `objectives: list[float]`
- List of objective values

#### `ineq_constraints: list[float]`
- List of inequality-constraint values

#### `eq_constraints: list[float]`
- List of equality-constraint values

#### `other_metrics: list[float]`
- Other metrics used for visualization and analysis

#### `_fitness: float | None`
- Internally stored aggregate fitness (scalar)
- Normally accessed through the `fitness` property rather than directly

### Properties
#### `fitness: float`
- Returns the scalar objective value (fitness) of the individual.
- If `_fitness` is `None`, returns the sum of `objectives` as the default fitness.
    - Can be used as a simple weighted sum in single-objective optimization
- If arbitrary scalarization is performed externally, assign the result as in `metrics.fitness = スカラー値`; that value will then be returned as `fitness`.

#### `constraint_violation: float`
- Returns the total violation of all constraints (inequality and equality constraints).

#### `ineq_constraint_violation: float`
- Returns the total inequality-constraint violation.
- Applies `max(0, v)` to each constraint value `v` and adds only the positive parts as violations.
  - If `v ≤ 0`, there is no violation (0)
  - If `v > 0`, that amount is counted as a violation

#### `eq_constraint_violation: float`
- Returns the total equality-constraint violation.
- Adds the absolute value `abs(v)` of each constraint value as the violation.

## `Individual`
```python
@dataclass
class Individual:
    solution: list[float]
    outcome_filepath: str | None = None
    metrics: OptimizationProblemMetrics = field(default_factory=OptimizationProblemMetrics)
```
A data class representing an individual (one candidate solution).
In addition to its solution vector, it stores evaluation results, constraint violations, visualization metrics, and related data in `metrics`.

### Attributes
#### `solution: list[float]`
- Design-variable vector (solution vector) $\boldsymbol{x}=\{x_1, x_2, ...\}$

#### `outcome_filepath: str | None`
- Path to the shape file corresponding to this individual
- Set automatically within EMSOptimizer during shape optimization

#### `metrics: OptimizationProblemMetrics`
- `OptimizationProblemMetrics` instance storing objective values, constraint values, and other metrics
- The Evaluator is expected to set values in this field
- During shape optimization, this field stores the function values configured in `optimization_problem.yaml`

## `Population`
```python
class Population(MutableMapping[int, Individual]):
    ...
```
Class for managing the population handled by an optimization algorithm.
It inherits from `MutableMapping[int, Individual]`, allowing individuals to be manipulated through essentially **the same interface as a dictionary (`dict`)**.  
Population instances pass between `optimizer` and `evaluator`, exchanging candidate solutions and their objective values.

### Constructor (__init__)
- Argument: `init_data: dict[int, Individual] | None`
    - Initial population dictionary (key: individual index; value: `Individual` instance)
    - If `None`, an empty population is created.

### Methods
#### `add_individual(individual: Individual) -> int`
- Adds an individual to the population and automatically assigns the smallest unused integer index.
- Return value: assigned index (`int`)

#### `merge(other: Population) -> None`
- Merges this population with the `other` population.
- After merging, the original indices are discarded and reassigned sequentially as `0, 1, 2, ...`.

#### `overwrite(other: Population) -> None`
- If `other` contains an individual with an index that also exists in this population, replaces the entire individual at that index.
    - Unlike the Python dictionary `update`, new indices in `other` are ignored.
- Typical uses include:
    - Updating only selected indices in an existing population
    - Replacing only evaluated individuals

#### `reindex() -> None`
- Reassigns indices sequentially as `0, 1, 2, ...` while preserving the current population order.
- Useful for resetting noncontiguous indices after deletion or merging.

#### `split(indices: list[int]) -> tuple[Population, Population]`
- Splits the population into two populations.
    - First population: individuals whose indices are included in `indices`
    - Second population: the remaining individuals
- Return value: tuple of the first and second populations

#### `extract(indices: list[int]) -> Population`
- Extracts and returns a subpopulation containing only individuals with the specified `indices`.
- Examples:
    - Extracting only elite individuals for separate storage or visualization
    - Reevaluating only a specific group of indices

#### `to_design_matrix() -> list[list[float]]`
- Returns the `solution` values of all individuals as a two-dimensional list.
- The result is a design matrix with the form “number of individuals × number of dimensions.”
- It can be used, for example, as an input matrix for machine learning or statistical analysis.

## Examples
```python
# 個体の作成
ind = Individual(solution=[0.1, 0.5, 0.9])

# 評価値・制約をセット
ind.metrics.objectives = [1.23, 0.45]         # 2目的
ind.metrics.ineq_constraints = [0.0, 0.2]     # 2つ目だけ違反
ind.metrics.eq_constraints = [0.01]           # 0に近ければ近いほど良い

print(ind.metrics.fitness)                    # _fitness 未設定なので objectives の和 = 1.68
print(ind.metrics.constraint_violation)       # ineq + eq

# 個体群の作成
pop = Population()
idx = pop.add_individual(ind)             # 自動で index=0 が割り当てられる

# 設計行列の取得
X = pop.to_design_matrix()                # [[0.1, 0.5, 0.9]]
```
