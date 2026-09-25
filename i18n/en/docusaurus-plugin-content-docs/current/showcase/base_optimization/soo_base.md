---
sidebar_position: 1
---

# soo_base Overview
This page introduces the `soo_base` project.  
This project optimizes the single-objective benchmark function Sphere\[11\].

## optimization.yaml (`soo_base` project)
The contents of `optimization.yaml` are shown below.  
The `evaluator` is the `sphere` implementation of the Sphere function, with `dim`, the number of design variables (the dimension of the optimization problem), set to `30`.  
The `optimizer` is the single-objective optimization algorithm `cmaes` with a fixed random seed. The design variables are constrained to the range \[-5.12, 5.12\] by setting `bounds`.  
```yaml
evaluator:
  name: sphere
  kwargs:
    dim: 30
optimizer:
  name: cmaes
  kwargs:
    bounds: [-5.12, 5.12]
    seed: 42
```

This example performs 100 optimization iterations.  
```yaml
num_iteration: 100
```
(Output-related settings are omitted.)

## Optimization Example
The GUI after completing 100 optimization iterations is shown below. The function value gradually converges to 0.  
![soo_base GUI](/img/soo_base_GUI.png)
