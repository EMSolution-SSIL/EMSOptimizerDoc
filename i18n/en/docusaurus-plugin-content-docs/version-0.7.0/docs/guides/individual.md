---
sidebar_position: 6
---

# Individual-related object API

## Overview

This page introduces the classes used to manage individuals throughout EMSOptimizer.
These classes are used particularly to exchange individual information between `optimizer` and `evaluator`.

## import

```python
from emsopt_engine.individual import (
    Individual,
    OptimizationProblemMetrics,
    Population,
)
```

## Quick reference

| API | Type | Main purpose | Main return value |
|---|---|---|---|
| `OptimizationProblemMetrics` | dataclass | Stores objective values, constraint values, and other metrics | `OptimizationProblemMetrics` |
| `Individual` | dataclass | Stores one candidate solution and its evaluation results | `Individual` |
| `Population` | class | Manages multiple `Individual` objects through a dictionary-like interface | `Population` |

## Common specifications

### Individuals and evaluation values

`Individual` represents one candidate solution and stores its design-variable vector in `solution`.
The evaluator writes objective values, constraint values, and other metrics to `Individual.metrics`.

During shape optimization, function values configured in `optimization_problem.yaml` are stored in `metrics` and `label_values`.

### Constraint violations

For inequality constraints, `v` is treated as the violation for each constraint value `max(0, v)`.
For equality constraints, the absolute value `abs(v)` is treated as the violation.

## API details

### `OptimizationProblemMetrics`

Dataclass that stores evaluation and constraint information for an optimization problem.

```python
@dataclass
class OptimizationProblemMetrics:
    objectives: list[float] = field(default_factory=list)
    ineq_constraints: list[float] = field(default_factory=list)
    eq_constraints: list[float] = field(default_factory=list)
    other_metrics: list[float] = field(default_factory=list)
    _fitness: float | None = None
```

#### Fields

| Name | Type | Default | Description |
|---|---|---:|---|
| `objectives` | `list[float]` | `[]` | List of objective values |
| `ineq_constraints` | `list[float]` | `[]` | List of inequality-constraint values |
| `eq_constraints` | `list[float]` | `[]` | List of equality-constraint values |
| `other_metrics` | `list[float]` | `[]` | Other metrics for visualization or analysis |
| `_fitness` | `float \| None` | `None` | Internally stored overall scalar fitness |

#### Properties

| Name | Type | Description |
|---|---|---|
| `fitness` | `float` | Returns the individual's scalar evaluation value (fitness) |
| `constraint_violation` | `float` | Returns the total violation of all constraints (inequality + equality) |
| `ineq_constraint_violation` | `float` | Returns the total inequality-constraint violation |
| `eq_constraint_violation` | `float` | Returns the total equality-constraint violation |

#### Notes

When `_fitness` is `None`, `fitness` returns the sum of `objectives` as the default fitness.
For custom scalarization, assign a value such as `metrics.fitness = scalar_value`; the value is stored in `_fitness` and returned as `fitness`.

### `Individual`

Dataclass representing one candidate solution.
In addition to the solution vector, it stores evaluation results, constraint violations, and visualization metrics in `metrics`.

```python
@dataclass
class Individual:
    solution: list[float]
    working_dir: str | None = None
    outcome_filepath: str | None = None
    metrics: OptimizationProblemMetrics = field(
        default_factory=OptimizationProblemMetrics
    )
    label_values: dict[str, float] = field(default_factory=dict)
    record_info: EvaluationRecord = field(default_factory=EvaluationRecord)
```

#### Fields

| Name | Type | Default | Description |
|---|---|---:|---|
| `solution` | `list[float]` | None | Design-variable (solution) vector $\boldsymbol{x}=\{x_1, x_2, ...\}$ |
| `working_dir` | `str \| None` | `None` | pyemsol working directory assigned to the individual |
| `outcome_filepath` | `str \| None` | `None` | Path to the shape file for this individual |
| `metrics` | `OptimizationProblemMetrics` | `OptimizationProblemMetrics()` | Stores evaluation values, constraint values, and other metrics |
| `label_values` | `dict[str, float]` | `{}` | Stores evaluation-function names and results during shape optimization |
| `record_info` | `EvaluationRecord` | `EvaluationRecord()` | Stores evaluation success/failure status and failure reason |

#### Related data

`record_info` stores the following evaluation-result record instance.

```python
@dataclass
class EvaluationRecord:
    status: Literal["success", "failure"] = "success"
    failure_reason: str | None = None
```

#### Notes

The key in `label_values` is composed of the evaluation-function name (`function_name`) and case name (`case_name`).
For example, it has a form such as `label__average_torque__case_transient`.

The value stores the raw function value configured in `optimization_problem.yaml` (the $A$ value on the [Getting Started > Optimization-problem settings](../getting-started/opt_problem.md) page).

:::warning
`label_values` identifies a function using only its function name and case name.
Therefore, values from functions with the same function and case names but different `kwargs` are not distinguished; only one is stored in `label_values`.

To store values with different `kwargs` separately, create separate functions with fixed `kwargs` (even if their processing is identical) and specify those functions in `optimization_problem.yaml`.
:::

### `Population`

Class for managing the population handled by an optimization algorithm.
It inherits `MutableMapping[int, Individual]`, so individuals can generally be manipulated through an interface similar to a dictionary (`dict`).

```python
class Population(MutableMapping[int, Individual]): ...
```

Instances of `optimizer` pass between `evaluator` and `Population`, carrying candidate solutions and their evaluation values.

#### Constructor

```python
Population(init_data: dict[int, Individual] | None = None)
```

| Name | Type | Default | Required | Description |
|---|---|---:|:---:|---|
| `init_data` | `dict[int, Individual] \| None` | `None` | No | Initial population dictionary; keys are individual indices and values are `Individual` instances |

#### Methods

| Method | Return value | Description |
|---|---|---|
| `add_individual(individual)` | `int` | Adds an individual and returns the smallest unused integer index |
| `merge(other)` | `None` | Merges this population with `other` |
| `overwrite(other)` | `None` | Replaces only individuals whose indices also exist in `other` |
| `reindex()` | `None` | Reindexes individuals as `0, 1, 2, ...` while preserving their current order |
| `split(indices)` | `tuple[Population, Population]` | Splits the population into the specified indices and the remaining individuals |
| `extract(indices)` | `Population` | Extracts only individuals at the specified indices |
| `from_design_matrix(design_matrix)` | `Population` | Creates a population from a design matrix |
| `to_design_matrix()` | `list[list[float]]` | Returns all `solution` values as a two-dimensional list |

#### `add_individual`

Adds an individual to the population and automatically assigns the smallest unused integer index.

```python
add_individual(individual: Individual) -> int
```

| Name | Type | Default | Required | Description |
|---|---|---:|:---:|---|
| `individual` | `Individual` | None | Yes | Individual to add |

| Return value | Description |
|---|---|
| `int` | Assigned index |

#### `merge`

Merges this population with the `other` population.
The original indices are discarded after merging and replaced with sequential indices `0, 1, 2, ...`.

```python
merge(other: Population) -> None
```

| Name | Type | Default | Required | Description |
|---|---|---:|:---:|---|
| `other` | `Population` | None | Yes | Population to merge |

#### `overwrite`

If `other` contains an individual with an index also present in this population, the individual at that index is replaced entirely.
Unlike Python dictionary `update`, new indices in `other` are ignored.

```python
overwrite(other: Population) -> None
```

| Name | Type | Default | Required | Description |
|---|---|---:|:---:|---|
| `other` | `Population` | None | Yes | Source population |

#### `reindex`

Reassigns indices as `0, 1, 2, ...` while preserving the current population order.
This is useful when indices become non-contiguous after deletion or merging.

```python
reindex() -> None
```

#### `split`

Splits the population into two populations.
The first contains individuals at indices in `indices`, and the second contains the remaining individuals.

```python
split(indices: list[int]) -> tuple[Population, Population]
```

| Name | Type | Default | Required | Description |
|---|---|---:|:---:|---|
| `indices` | `list[int]` | None | Yes | List of individual indices to include in the extracted population |

| Return value | Description |
|---|---|
| `tuple[Population, Population]` | Tuple containing the first and second populations |

#### `extract`

Extracts and returns a subpopulation containing only individuals at the specified indices `indices`.

```python
extract(indices: list[int]) -> Population
```

| Name | Type | Default | Required | Description |
|---|---|---:|:---:|---|
| `indices` | `list[int]` | None | Yes | List of individual indices to extract |

| Return value | Description |
|---|---|
| `Population` | Population containing only individuals at the specified indices |

#### `from_design_matrix`

Class method that creates a population from a design matrix.

```python
from_design_matrix(cls, design_matrix: list[list[float]]) -> Population
```

| Name | Type | Default | Required | Description |
|---|---|---:|:---:|---|
| `design_matrix` | `list[list[float]]` | None | Yes | Design matrix with dimensions number of individuals × number of variables |

| Return value | Description |
|---|---|
| `Population` | Population created from the design matrix |

#### `to_design_matrix`

Returns all individuals' `solution` values together as a two-dimensional list.
The format is a design matrix with dimensions number of individuals × number of variables.

```python
to_design_matrix() -> list[list[float]]
```

| Return value | Description |
|---|---|
| `list[list[float]]` | Design matrix containing all individuals' `solution` values |

## Examples

### Creating individuals and populations

```python
from emsopt_engine.individual import Individual, Population

# 個体の作成
ind = Individual(solution=[0.1, 0.5, 0.9])

# 評価値・制約をセット
ind.metrics.objectives = [1.23, 0.45]
ind.metrics.ineq_constraints = [0.0, 0.2]
ind.metrics.eq_constraints = [0.01]

print(ind.metrics.fitness)
print(ind.metrics.constraint_violation)

# 個体群の作成
pop = Population()
idx = pop.add_individual(ind)

# 設計行列の取得
X = pop.to_design_matrix()
```
