---
sidebar_position: 3
---

# IPM8P48S Surrogate-Model Example
This page introduces the `IPM8P48S_surrogate` project.  
This project performs shape optimization of the IPM8P48S model and visualizes the results as response surfaces using a random forest.
:::info
The eMotorSolution API is required to run this project.
:::

## optimization.yaml (`IPM8P48S_surrogate` project)
As in [IPM8P48S simultaneous shape and topology optimization](./pto.md), setting `ems_shape_builder` to `HoleMagnet55` performs shape optimization of the permanent magnets and flux barriers. For simplicity, topology-optimization settings are omitted here, and pure shape optimization is performed through the eMotorSolution link.  
The optimization problem (`optimizer`) is also a multi-objective optimization that maximizes average torque and minimizes torque ripple, as in the [IPM8P48S description and basic optimization example](./basic_moo.md). `nsga2` is selected as the optimizer.
```yaml
evaluator:
  name: pyemsol_shape_evaluator
ems_shape_builder:
  name: HoleMagnet55
optimizer:
  name: nsga2
  kwargs:
    population_size: 20
    seed: 42
    bounds: [[40, 45], [1.5, 2.5], [1.0, 2.0], [11, 13], [20, 22],
             [16, 20], [1.0, 2.0], [0.5, 1.5], [4.0, 6.0], [0.0, 1.0]]
```

The `candidate` output is enabled (`enabled: True`) so that all analysis data generated during optimization can be used to build the response surface.  
The `check` option also configures a response surface to be built when the `response_surface` command starts.
```yaml
# output functionality
output_interval: 1
output_control:
  best_individual:
    filename_base: best_individual
    enabled: True
    output_interval: 1
  candidate:
    filename_base: candidate
    enabled: True
    output_interval: 1
  candidate_plot:
    filename_base: candidate_plot
    enabled: True
    output_interval: 10
enable_progress_gui: True
response_surface:
  enabled: True
  grid_size: 50
  min_samples: 5
  n_estimators: 200
  random_state: 0
```

## Optimization example
The GUI after 50 optimization iterations is shown below. A broad Pareto front is obtained for average torque and torque ripple.  
![IPM8P48S surrogate result](/img/IPM8P48S_surrogate_check.png)

The `Responce Surface` tab (response-surface visualization) shows the results for average torque below. The upper plot is the response surface, and the lower plot shows the importance of each design variable (shape parameter) derived from the random forest.  
For example, these plots show that the tenth design variable (rotor-surface rib thickness) has a particularly large effect on average torque, and that reducing this value improves average torque. Actual design decisions require consideration of many factors, but this response surface can provide insight into the relationship between performance values evaluated during optimization and design variables.  
![IPM8P48S surrogate result (response surface)](/img/IPM8P48S_surrogate_check_rs.png)

## Optimization using a surrogate model
The data collected in the optimization above can be used to perform an optimization that searches on the response surface (surrogate model).  
For example, the following configuration uses the `sa_nsga2` optimizer ([NSGA-II with surrogate-model assistance](../../docs/guides/Optimizer/sa_nsga2.md)). It runs R-NSGA-II to focus on average torque of 16.5 Nm and torque ripple of 40.0%, where the original Pareto front had relatively few solutions.  
Set `data_csv_path` to the path of the CSV file obtained from the preceding optimization. See the optimizer page above and the original paper for other arguments and algorithm details.  
```yaml
optimizer:
  name: sa_nsga2
  kwargs:
    population_size: 20
    reference_points: [[-16.5, 40.0]]
    seed: 42
    bounds: [[40, 45], [1.5, 2.5], [1.0, 2.0], [11, 13], [20, 22],
             [16, 20], [1.0, 2.0], [0.5, 1.5], [4.0, 6.0], [0.0, 1.0]]
    surrogate_mode: full_loop
    eval_init_population_truly: False
    data_csv_path: "Path/To/EMSOptimizer/projects/IPM8P48S_surrogate/summary/cross_study/cross_study_individuals.csv"
ems_shape_builder:
  name: HoleMagnet55

# optimization settings
num_iteration: 1  # サロゲート補助の最適化を1回実行する設定
enable_parallelization: True
num_processes: Null  # if Null, automatically set from cpu counts
```

The result is shown below. Surrogate-model optimization obtains a new Pareto front near the reference point [-16.5 Nm, 40.0%] with little additional computation.
![IPM8P48S surrogate-assisted result](/img/IPM8P48S_surrogate_sa_check.png)
