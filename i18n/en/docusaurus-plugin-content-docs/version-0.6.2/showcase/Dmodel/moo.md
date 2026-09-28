---
sidebar_position: 3
---

# Dmodel Multi-Objective Optimization Example
This page introduces the `Dmodel_moo` project.  
Compared with the `Dmodel` project, `Dmodel_moo` is configured for multi-objective optimization.

## optimization.yaml (`Dmodel_moo` project)
The contents of `optimization.yaml`, which configures the optimization, are shown below.  
For this multi-objective shape optimization, the `decomposition_ensemble` multi-objective optimization algorithm is selected. See the [corresponding documentation page](../../docs/guides/Optimizer/decomposition_ensemble.md) for details.
```yaml
evaluator:
  name: pyemsol_shape_evaluator
optimizer:
  name: decomposition_ensemble
  kwargs:
    num_decomposition: 5
    seed: 42
```

## optimization_problem.yaml (`Dmodel_moo` project)
The contents of `optimization_problem.yaml` are the same as in the `Dmodel` project. However, because the optimization algorithm handles a multi-objective problem, each entry in `objectives` is treated as an independent objective function.
```yaml
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
    coefficient: 1.0
```

Thus, the multi-objective optimization problem defined here is as follows.
```math
\begin{align*}
\text{minimize} \quad & f_1=-\frac{T_\text{avg}}{2.1} \\
                      & f_2=\frac{T_\text{rip}}{54.0} \\
\end{align*}
```
$T_\text{avg}$: Average torque [Nm]  
$T_\text{rip}$: Torque ripple percentage [%]

## Optimization Example
Optimization was performed with Implicit Domain Meshing enabled (`use_implicit_domain_meshing: True`). The GUI after 100 optimization iterations is shown below.  
Because the number of decompositions was set to 5, the Pareto front is sparse, but the solutions cover a broad range. The average torque reaches a plateau around $f_1=-1.05$ ($T_\text{avg}=2.2\text{Nm}$), suggesting that this is the limit of the average torque under these settings.  
The displayed shapes are the solutions labeled "Left" and "Right" in the Pareto-front plot. "Left" achieves both high average torque and low torque ripple and is close to the result of [Basic Optimization](./basic.md). "Right", on the other hand, focuses on reducing torque ripple; its value is very low at 2.42%, but the magnetic core has moved away from the rotor surface, resulting in a much lower average torque. A constraint requiring the average torque to remain above a certain value could prevent this (see the [IPM8P48S](../IPM8P48S/basic_moo.md) example).
![Dmodel Pareto front](/img/Dmodel_moo_check.png)
