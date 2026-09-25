---
sidebar_position: 4
---

# sa_nsga2
This is a Python implementation class that accelerates the NSGA-II multi-objective optimization algorithm\[6\] using a surrogate model.

## Overview
Multi-objective structural optimization of electrical equipment can be computationally expensive because many shapes must be analyzed and evaluated. One widely used approach is to replace the analysis with a surrogate model, a fast model for approximate evaluation.  
This implementation integrates a surrogate model into NSGA-II.  
For details, see [Advanced Topics > Surrogate Model Usage](../../advanced/surrogate_model_usage.md).

## Configurable keyword arguments
Only options added to `nsga2` are listed.  
- `func_manager` ... Objective-function and constraint manager automatically injected when `evaluator` is `pyemsol_shape_evaluator`.
:::info
When func_manager is set as an argument of the `optimizer` factory function, the manager object is automatically injected, regardless of whether `func_manager` is used. See [Advanced Topics > Surrogate Model Usage](../../advanced/surrogate_model_usage.md) for details.
:::
- `surrogate_model: str` ... Name of the surrogate model to use. The default is `"mlp"`.
:::info
As of v0.7.0, only `mlp` (a multilayer perceptron model) is implemented. Users can define and use their own surrogate models in `core/optimizer/surrogate_models`.
:::
- `data_csv_path: str | null` ... CSV file used to train the surrogate model when one is specified. The default is `null` (no initial data).
- `enable_adaptive_training: bool` ... Whether to update the surrogate model during optimization. The default is `True`.
- `surrogate_mode: Literal["full", "full_loop", "assist", "assist_strict"]` ... Acceleration mode using the surrogate model. The default is `"assist_strict"`.  
:::tip[Acceleration modes]
- "full" ... Replace the analysis of all individuals with the surrogate model.
- "full_loop" ... Repeat optimization using the surrogate model, true evaluation of the resulting population, and so on\[22\].
- "assist" ... In each generation, truly evaluate only individuals whose surrogate-model evaluation is good (high rank in non-dominated sorting)\[23\].
- "assist_strict" ... In each generation, truly evaluate only individuals whose surrogate-model evaluation is good. Individuals not truly evaluated are forcibly eliminated\[24\].
:::
- `eval_init_population_truly: bool` ... Whether to truly evaluate the initial population with `evaluator` instead of the surrogate model. The default is `True`.
