---
sidebar_position: 6
---

# Dmodel Gradient-Based Optimization Example (Density Method)
This page introduces the `Dmodel_SynRM_gradient` project.  
The `Dmodel_SynRM_gradient` project assumes a synchronous reluctance motor (SynRM) and performs optimization using a gradient-based topology optimization method (density method).

## Base mesh
As in the [multi-material optimization example](./multi_material.md), `Dmodel_SynRM_gradient` uses a base mesh whose rotor contains no permanent magnets and consists only of material ID `20` (magnetic core). The air/magnetic-core distribution is optimized throughout the rotor.

## optimization.yaml (`Dmodel_SynRM_gradient` project)
In `optimization.yaml`, `level_set_function` is set to `pyemsol_density`. This causes EMSOptimizer to calculate the gradient of objective `W2` (the squared difference from the target torque) internally. Here, the target torque is set to 0.5 Nm. The design region is also set slightly smaller than the rotor region so that a rib remains around the outer circumference.  
The calculated gradient is used by `optimizer` > `gradient_update` to update the design variables (here, values in [-1,1] representing the material properties of each element in the design region).  
This example also applies a volume constraint (`constraint_mode: volume_penalty`) so that the magnetic-core area is at most 50% of the total area.  
```yaml
optimizer:
  name: gradient_update
  kwargs:
    constraint_mode: volume_penalty
    volume_frac_ulim: 0.5
level_set_function:
  name: pyemsol_density
  kwargs:
    proj_method: heaviside5
    objective_type: W2
    torque_scale: 4.0
    torque_target: 0.5
    coordinate: Polar
    design_region: [[0.0100, 0.0273], [5.0, 45.0]]
```

## optimization_problem.yaml (`Dmodel_SynRM_gradient` project)
When `pyemsol_density` is used, the objective function specified in its arguments is calculated internally. `optimization_problem.yaml` is used to configure `case_names` and to determine move-limit damping in `gradient_update`.  
```yaml
case_names:
  - transient

objectives:
  - function_name: torque_squared_error
    kwargs:
      torque_target: 0.5
      torque_scale: 4.0

ineq_constraints: []

eq_constraints: []

other_metrics:
  - function_name: average_torque
    kwargs:
      torque_scale: 4.0
  - function_name: torque_ripple
    kwargs:
      torque_scale: 4.0
  - function_name: torque_squared_error
    kwargs:
      torque_target: 0.5
      torque_scale: 4.0
```

## Optimization Example
This example performs 200 optimization iterations.  
The following animation shows the shape evolution over 200 iterations (the best shape from each iteration). Gray areas have intermediate material-property values (grayscale), while black areas are magnetic core; the magnetic core can be seen forming on the rotor surface.
![Dmodel gradient optimization history](/img/Dmodel_SynRM_gradient_best_individuals.gif)

The GUI after completing 200 optimization iterations is shown below.  
The best value was recorded at iteration 40 and remained almost flat thereafter, indicating sufficient convergence.  
The magnetic-core area slightly exceeds the constraint value, but this can be mitigated by adjusting the penalty coefficient and related settings.  

![Dmodel gradient optimization history](/img/Dmodel_SynRM_gradient_check.png)
