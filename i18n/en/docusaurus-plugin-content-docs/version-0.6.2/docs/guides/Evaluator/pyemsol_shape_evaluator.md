---
sidebar_position: 5
---

# pyemsol_shape_evaluator
Evaluation implementation for shape optimization using pyemsol.

## Overview
Shape evaluation is performed under the following conditions. If `ls_function`, `ems_shape_builder`, or `analysis_conditioner` is not configured, the corresponding processing is skipped.
- The shape is determined by passing the candidate-solution vector to `ls_function` and `ems_shape_builder`.
- The analysis conditions are determined by passing the candidate-solution vector to `analysis_conditioner`.
- The objective and constraint functions defined in `optimization_problem.yaml` are calculated.
- Shape analysis is performed independently for each analysis case defined in `optimization_problem.yaml` > `case_names`. Each analysis-case folder in the project folder is assumed to contain a pyemsol input JSON file with the same name.

## Configurable keyword arguments
None
