---
sidebar_position: 5
---
# Introduction to surrogate models
Since v0.7.0, EMSOptimizer has provided an implementation example for accelerating optimization with surrogate models.  
This page explains how to use surrogate models with EMSOptimizer.
:::info
For a practical example, see [IPM8P48S surrogate-model example](../../showcase/IPM8P48S/surrogate.md).
:::

## Surrogate-model overview
A surrogate model (also called a proxy or substitute model) is built to replace computationally expensive numerical calculations such as electrical-device analysis.  
The finite element method (FEM) is widely used for electrical-device analysis, but its high computational cost can become a design bottleneck. This is especially significant in optimization, which repeatedly performs FEM analyses.  
A surrogate model is built as a lightweight, fast replacement for FEM that reproduces analysis results. Existing data is used to train a machine-learning or deep-learning model so that it can accurately predict analysis results, replacing FEM analyses in parameter surveys and optimization.

## Usage flow
### Collecting training data in advance
A surrogate model requires training data. In EMSOptimizer, set `optimization.yaml` > `output_control` > `candidate` > `enabled` to `True` to accumulate data for every individual analyzed during optimization.  
After each study finishes, project results are consolidated into CSV files in the project `summary` folder > `cross_study` folder. Individual results are saved in `summary` > `optimization_studies`.  
:::tip[Offline and online training]
Training data is generally collected before building a surrogate model.  
When a surrogate model is used for optimization, however, it can be trained and updated using data obtained during optimization. In general, the surrogate model becomes more accurate as optimization progresses.  
Here, the former is called offline training and the latter online training (or adaptive training).

Offline training requires collecting training data in advance as described above.  
Online training can run without pre-collected data. However, providing pre-collected training data initially allows analysis results to be predicted with a high-accuracy surrogate model from the beginning of optimization.
:::

### Integrating surrogate models into optimization
EMSOptimizer provides surrogate-model implementations in `core.optimizer.surrogate_models` and utilities for using surrogate models in `core.optimizer.surrogate_utils`.  
`sa_nsga2` is an implementation example using these components. Passing the path to pre-collected training data through `data_csv_path` makes `sa_nsga2` train the surrogate model automatically before optimization. Setting `enable_adaptive_training` to `True` enables online training, updating the surrogate model after every optimization generation.  
:::tip[Aggregating evaluation functions and design variables]
CSV files saved in the `summary` folder contain information about `Indivisual` from the [User Guide > Individual-related object API](../guides/individual.md).  
The values of `label_values` (a dictionary) represent raw evaluation-function values. Training a surrogate model on these values makes it possible to flexibly reuse its predictions as objectives or constraints. For example, after optimizing average torque as an objective, its raw values can be used to train a surrogate model and the predictions can then be reused in an optimization problem that constrains average torque.  
The utilities in `core.optimizer.surrogate_utils` automatically store surrogate predictions where the corresponding `label_values` keys match; `sa_nsga2` also uses this feature.  

Design variables, on the other hand, are saved with naïve column names such as `solution_1`, `solution_2`, and so on. If the design-variable definition changes between studies, the design-variable columns in the `cross_study` table become inconsistent. Therefore, when using `cross_study` data, keeping the design-variable definition consistent across studies is recommended.  
:::

## Displaying response surfaces in the GUI
Since v0.7.0, EMSOptimizer has provided a simple GUI display for response surfaces in a broad sense. Response surfaces show which design variables affect performance.  
:::info
For a practical configuration example, see [IPM8P48S surrogate-model example](../../showcase/IPM8P48S/surrogate.md).
:::
1. Set `optimization.yaml` > `output_control` > `candidate` > `enabled` to `True` and run the optimization. The response surface uses the resulting `run_records.csv` for training.
2. Set `optimization.yaml` > `response_surface` > `enabled` to `True` and configure the related settings. See [User Guide > Optimization settings](../guides/optimization_config.md) for details.
3. Display the GUI with the `check` command and select the `Response Sruface` tab.

An example is shown below. The upper graph shows the response surface, and the lower graph shows approximate design-variable importance. As of v0.7.0, importance is calculated as random-forest feature importance (feature_importance) \[35\].  
- `Samples` shows the number of samples used for training.
- `Anchor` specifies the reference for the response-surface display. The surface is displayed along two axes; when there are three or more design variables, hidden-axis values are fixed to the reference values.
    - `selected_individual`: Design-variable values of the individual selected in the GUI. When an individual is selected, this anchor mode is used automatically.
    - `median_record`: Mean values in the training data. This is used as a fallback when no individual is selected.
- The combo boxes at the top of the screen select the displayed value (performance value) and the horizontal and vertical axes of the response surface.

![Response-surface GUI](/img/response_surface_gui.png)
