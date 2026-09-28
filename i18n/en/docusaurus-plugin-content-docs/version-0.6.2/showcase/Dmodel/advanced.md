---
sidebar_position: 2
---

# Dmodel Advanced Optimization Example
This page introduces the `Dmodel_advanced` project.  
Compared with the `Dmodel` project, `Dmodel_advanced` has a substantially different `optimization_problem.yaml`. Specifically, the optimization considers torque characteristics under two current conditions simultaneously.

## optimization_problem.yaml (`Dmodel_advanced` project)
Let us examine the contents of `optimization_problem.yaml`.

### Analysis cases
The main change is that `case_names` contains two cases. The first is `transient`, which uses the same conditions as the `Dmodel` project (current 3.0 Arms and current phase angle 20 deg).  
The second is `transient_high_current`, where the current changes from 3.0 Arms to 9.0 Arms and the current phase angle changes from 20 deg to 30 deg.  
Folders with these case names are included in the `Dmodel_advanced` project. The current conditions and other analysis settings are specified in same-named JSON files in each case folder. See the EMSolution (pyemsol) electromagnetic-field simulator documentation for the JSON format.
```yaml
case_names:
  - transient
  - transient_high_current
```

### Objective function
The `objectives` section defines an optimization problem that maximizes the weighted sum of average torque under the two analysis conditions.
```yaml
objectives:
  - function_name: average_torque
    case_name: transient
    kwargs:
      torque_scale: 4.0
    normalization_const: 2.1
    coefficient: -1.0
  - function_name: average_torque
    case_name: transient_high_current
    kwargs:
      torque_scale: 4.0
    normalization_const: 6.3
    coefficient: -1.0
```
Written as a single-objective problem (the single-objective `optmization.yaml` algorithm is configured in `cmaes`), this becomes:
```math
\text{minimize} \quad F=f_1+f_2=-1.0\frac{T_\text{avg}^\text{3.0Arms20deg}}{2.1} - 1.0\frac{T_\text{avg}^\text{9.0Arms30deg}}{6.3} \\
```
$T_\text{avg}^\text{3.0Arms20deg}$: average torque at 3.0 Arms and 20 deg [Nm]  
$T_\text{avg}^\text{9.0Arms30deg}$: average torque at 9.0 Arms and 30 deg [Nm]  
The denominator of each term (the normalization constant) is the average torque of the original Dmodel under the corresponding condition.

### Inequality constraints
The `ineq_constraints` section constrains torque ripple under each analysis condition.  
Each torque-ripple value is constrained to be no greater than 30%.
```yaml
  - function_name: torque_ripple_percentage
    case_name: transient
    kwargs:
      torque_scale: 4.0
    baseline: 30.0
  - function_name: torque_ripple_percentage
    case_name: transient_high_current
    kwargs:
      torque_scale: 4.0
    baseline: 30.0
```
In equation form:
```math
\begin{align*}
\text{subject to} \quad & g_1(\boldsymbol{x}) = T_\text{rip}^\text{3.0Arms20deg} - 30.0 \leq 0 \\
                        & g_2(\boldsymbol{x}) = T_\text{rip}^\text{9.0Arms30deg} - 30.0 \leq 0
\end{align*}
```
$T_\text{rip}^\text{3.0Arms20deg}$: torque ripple at 3.0 Arms and 20 deg [%]  
$T_\text{rip}^\text{9.0Arms30deg}$: torque ripple at 9.0 Arms and 30 deg [%]  

### Equality constraints
The `eq_constraints` section constrains the rotor core to remain connected, as described at the end of the [basic optimization](./basic.md) page.
```yaml
eq_constraints:
  - function_name: num_connected_components
    kwargs:
      physical_tag: 20
    baseline: 1
```

Finally, `other_metrics` is configured to output the related values for the GUI.

## Optimization example
The optimization was run with Implicit Domain Meshing enabled (`use_implicit_domain_meshing: True`). The GUI after 100 iterations is shown below.  
Some solutions violate the torque-ripple constraints through iteration 10, but the final constraint-violation values are zero, showing that feasible solutions were obtained.  
The best shape shown in the GUI has $T_\text{avg}^\text{3.0Arms20deg}$=2.13 Nm, $T_\text{avg}^\text{9.0Arms30deg}$=6.91 Nm, $T_\text{rip}^\text{3.0Arms20deg}$=26.8%, and $T_\text{rip}^\text{9.0Arms30deg}$=16.4%. Its flux-barrier shape differs from that in the [basic optimization](./basic.md) example.  
A thin layer of magnetic-core material remains at both ends of the magnets, satisfying the connectivity constraint.
![Dmodel optimization history](/img/Dmodel_advanced_check.png)
