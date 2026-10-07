---
sidebar_position: 4
---

# Optimization Problem Configuration (`optimization_problem.yaml`)
This page explains the available optimization-problem configuration options.  
:::info
See [Getting Started > Defining the Optimization Problem](../getting-started/opt_problem.md) for details and examples of each configuration.
:::

## Format
Notation: `{設定項目名}: {型名} = デフォルト値`  
Options without a default value are required.
```yaml
case_names: list[str]
objectives: list[OptimizationProblemFunction] = []
ineq_constraints: list[OptimizationProblemFunction] = []
eq_constraints: list[OptimizationProblemFunction] = []
other_metrics: list[OptimizationProblemFunction] = []
```

`OptimizationProblemFunction` is a configuration with the following fields.  
```yaml
function_name: str
case_name: str | Null = Null
kwargs: dict[str, Any] = {}
coefficient: float = 1.0
normalization_const: float = 1.0
baseline: float = 0.0
```

## Details
- `case_names: list[str]` ... List of analysis case names.
- `objectives: list[OptimizationProblemFunction]` ... List of objective functions.
- `ineq_constraints: list[OptimizationProblemFunction]` ... List of inequality constraints.
- `eq_constraints: list[OptimizationProblemFunction]` ... List of equality constraints.
- `other_metrics: list[OptimizationProblemFunction]` ... List of metrics.

### OptimizationProblemFunction
:::info
See the [Evaluation Function Examples](./opt_problem_ex.md) page for implementation examples.  
See [Getting Started > Defining the Optimization Problem](../getting-started/opt_problem.md) for details and examples of each configuration.
:::

- `function_name: str` ... Name of the evaluation function.
- `kwargs: dict[str, Any]` ... Arguments passed to the evaluation function.
- `case_name: str | Null` ... Analysis case name used to calculate the evaluation function.
- `coefficient: float = 1.0` ... Coefficient applied to the result.
- `normalization_const: float = 1.0` ... Normalization constant applied to the result.
- `baseline: float = 0.0` ... Baseline value used to bias the result.
