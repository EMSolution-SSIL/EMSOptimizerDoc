---
sidebar_position: 3
---

# Optimization Problem Configuration (optimization_problem.yaml)
This page introduces the definition of an optimization problem for shape optimization.

## Configuring the Optimization Problem
In EMSOptimizer, the optimization problem for shape optimization is managed with `opimization_problem.yaml`.
The following optimization problem is defined through `opimization_problem.yaml`.
```math
\begin{align*}
\text{minimize} \quad & f_i(\boldsymbol{x}) \quad (i = 1, \ldots, n) \\
\text{subject to} \quad & g_j(\boldsymbol{x}) \leq 0 \quad (j = 1, \ldots, m) \\
                         & h_k(\boldsymbol{x}) = 0 \quad (k = 1, \ldots, p) \\
                         & \boldsymbol{x} \in X
\end{align*}
```
$\boldsymbol{x} = \{x_i\}^\text{T}$: candidate-solution vector  
$X$: the set of $\boldsymbol{x}$ (in EMSOptimizer, this corresponds to the lower and upper bounds of $x_i$)
:::info
Variable bounds can be configured in `optimization.yaml`.  
For optimization settings such as the number of iterations, see [User Guide > Optimization settings](../guides/optimization_config.md).
:::

$f_i$, $g_i$, and $h_i$ correspond to the following lists in `opimization_problem.yaml` and are referenced during optimization.
- $f_i$: `objectives`
- $g_i$: `ineq_constraints`
- $h_i$: `eq_costraints`  
- As an exception, the `other_metrics` list is not used in optimization calculations; it is used for GUI display and file output.

Each item in these lists has the following settings:
- `function_name: str` ... Evaluation-function name (see below), such as `average_torque` or `torque_ripple`.
- `case_name: str | null` ... Name of the analysis case used to evaluate `function_name` (see below).
- `kwargs: dict` ... Python keyword arguments passed to the evaluation function. Optional.
- `normalization_const: float` ... Normalization constant; see the equation below. The default is `1.0`.
- `coefficient: float` ... Weight coefficient; see the equation below. The default is `1.0`.
- `baseline: float` ... Bias term; see the equation below. The default is `0.0`.
:::info
For the evaluation functions that can be specified for `function_name` and their `kwargs` arguments, see [User Guide > Evaluation Function Examples](../guides/opt_problem_ex.md).
:::
:::tip About `case_names`
EMSOptimizer can define objectives for multiple analysis cases. This is useful, for example, when optimizing performance at multiple operating points of a motor simultaneously.  
Set the list of analysis-case names in `optimization_problem.yaml` > `case_names`, and store folders with the same names in the project folder.  
See the [Showcase](../../showcase/Dmodel/advanced.md) example for optimization using multiple analysis cases.
:::

Using these settings, $f_i$, $g_i$, and $h_i$ are calculated for each individual as follows.
```math
\text{coefficient} \times (A - \text{baseline}) / \text{normalization\_const} \\
```
$A$: Result calculated by the evaluation function with `case_name`, based on the analysis results for `kwargs`.

The calculated values are stored with each individual and used by the optimizer when updating individuals.
:::info
For technical details on managing individuals and calculated values, see [User Guide > Individual-related object API](../guides/individual.md).
:::

## Saving and loading optimization-problem templates
The contents of `opimization_problem.yaml` can be saved as an optimization-problem template with the `save_tpl` command. The template is saved to `project/problem_template.yaml`.
```sh
python emsopt.py save_tpl Dmodel NewProblem
```
The saved optimization problem can be copied to another project with `load_tpl`.
```sh
python emsopt.py load_tpl NewDmodel NewProblem
```

## Example: Dmodel
As an example, consider the `Dmodel` in the `optimization_problem.yaml` project, which is configured for single-objective optimization.
```yaml
case_names:
  - transient

objectives:
  - function_name: average_torque
    kwargs:
      torque_scale: 4.0
    normalization_const: 2.1
    coefficient: -1.0
  - function_name: torque_ripple_percentage
    kwargs:
      torque_scale: 4.0
    normalization_const: 54.0
    coefficient: 0.1

ineq_constraints: []

eq_constraints: []

other_metrics:
  - function_name: average_torque
    kwargs:
      torque_scale: 4.0
  - function_name: torque_ripple_percentage
    kwargs:
      torque_scale: 4.0
```

First, the only analysis case is `transient` (a multi-case analysis while varying the electrical and mechanical angles). No constraints are imposed here, so `ineq_constraints` and `eq_constraints` are empty arrays. Omitting these settings is treated in the same way.

Next, two $f_i$ objectives are configured in `objectives`. The first calculates the motor's average torque, and the second calculates torque ripple (the peak-to-peak amplitude of the torque waveform divided by average torque).

`kwargs` contains a torque scale factor. Because the `Dmodel` project analyzes a quarter model of the motor, the factor is set to 4 to convert torque to the full-model equivalent.

The `normalization_const` and `coefficient` values correspond to $T^\text{ref}$ and $w$ in the equation below. $T^\text{ref}$ is the normalization constant, which makes the objective dimensionless and aligns the scales between objectives.

```math
w \frac{f_i}{T^\text{ref}}
```

The original performance of the model before optimization is often used as the normalization constant. The values configured here are also the original Dmodel performance at a current of 3.0 Arms and a current phase angle of 20°.

Thus, this project minimizes the weighted sum of negative average torque and torque ripple. Because maximizing negative average torque is equivalent to maximizing (positive) average torque, this is ultimately a problem that maximizes average torque and minimizes torque ripple.

```math
\text{minimize} \quad F=f_1+f_2=-1.0\frac{T_\text{avg}}{2.1} + 0.1\frac{T_\text{rip}}{54.0} \\
```
$T_\text{avg}$: average torque [Nm]  
$T_\text{rip}$: torque ripple [%]

Finally, `other_metrics` contains average torque and torque ripple as raw values without `normalization_const` or `coefficient`. This makes these values available in the GUI.
