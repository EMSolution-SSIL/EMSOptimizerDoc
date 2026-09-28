---
sidebar_position: 2
---

# moo_base Overview
This page introduces the `moo_base` project.  
This project optimizes the multi-objective benchmark function ZDT1\[9\].

## optimization.yaml (`moo_base` project)
The contents of `optimization.yaml` are shown below.  
The `evaluator` is the `zdt1` implementation of the ZDT1 function, with 30 design variables.  
The `optimizer` is the multi-objective optimization algorithm `nsga2` with a fixed random seed. The design variables are bounded by \[0, 1\].  
```yaml
evaluator:
  name: zdt1
optimizer:
  name: nsga2
  kwargs:
    seed: 42
    bounds: [0.0, 1.0]
```

This example performs 30 optimization iterations.  
```yaml
num_iteration: 30
```
(Output-related settings are omitted.)

## Optimization Example
The GUI after completing 30 optimization iterations is shown below. A uniform Pareto front can be observed. According to the literature, this Pareto front is very close to the true Pareto front.  
![moo_base GUI](/img/moo_base_GUI.png)
