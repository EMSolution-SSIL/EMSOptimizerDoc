---
sidebar_position: 2
---

# Optimization Configuration (`optimization.yaml`)
This page explains the available optimization configuration options.

## Format
Notation: `{設定項目名}: {型名} = デフォルト値`  
Options without a default value are required.
```yaml
# Core Objects
evaluator:
  name: str
  kwargs: dict[str, Any] = {}
optimizer:
  name: str
  kwargs: dict[str, Any] = {}
analysis_conditioner: = None
  name: str
  kwargs: dict[str, Any] = {}
level_set_function: = None
  name: str
  kwargs: dict[str, Any] = {}
ems_shape_builder: = None
  name: str
  kwargs: dict[str, Any] = {}

# Optimization Settings
num_iteration: int
enable_parallelization: bool = False
num_processes: int | null = null
enable_dask_distribution: bool = False
dask_scheduler_url: str | null = null
num_chunks: int | null = null

# Output
resource_dir: str | null = null
output_dir: str | null = null
output_interval: int = 1
output_control:
  best_individual:
    filename_base: str
    enabled: bool = True
    output_interval: int = 1
  candidate:
    filename_base: str
    enabled: bool = True
    output_interval: int = 1
  candidate_plot:
    filename_base: str
    enabled: bool = True
    output_interval: int = 1
enable_progress_gui: bool = True
```

## Details
:::info
See the relevant User Guide sections for core-object implementation examples and configurable keyword arguments.  
:::

### Core objects
- `evaluator` ... Evaluator implementation used for optimization.
    - `name: str` ... Implementation name
    - `kwargs: dict[str, Any]` ... Keyword arguments
- `optimizer` ... Optimizer implementation used for optimization.
    - `name: str` ... Implementation name
    - `kwargs: dict[str, Any]` ... Keyword arguments
- `analysis_conditioner` ... Analysis Conditioner implementation used for optimization. Optional.
    - `name: str` ... Implementation name
    - `kwargs: dict[str, Any]` ... Keyword arguments
- `level_set_function` ... Level Set Function implementation used for optimization. Optional.
    - `name: str` ... Implementation name
    - `kwargs: dict[str, Any]` ... Keyword arguments
- `ems_shape_builder` ... eMotorSolution Shape Builder implementation used for optimization. Optional.
    - `name: str` ... Implementation name
    - `kwargs: dict[str, Any]` ... Keyword arguments
:::info
The last three core object settings are optional. Configure only the objects you want to use.  
In particular, when a benchmark function is used for `evaluator`, all three are irrelevant and can be omitted (any configured values are ignored).
:::

### Optimization settings
- `num_iteration: int` ... Number of optimization iterations.
:::info
Here, an iteration is defined as follows:  
“The sequence in which `optimizer` passes a candidate to `evaluator`, `evaluator` evaluates it, and `optimizer` performs an update.”
:::
- `enable_parallelization: bool` ... Enable or disable parallel processing. When enabled, shape evaluation in shape optimization is parallelized.
- `num_processes: int | null` ... Number of parallel processes when parallel processing is enabled. When `null`, it is set automatically from the number of CPUs on the PC.
- `enable_dask_distribution: bool` ... Enable or disable distributed processing. When enabled, shape evaluation in shape optimization is distributed among separately started worker nodes.
- `dask_scheduler_url: str | null` ... Address of the scheduler node to which worker nodes connect when distributed processing is enabled.
- `num_chunks: int | null` ... Number of distributed chunks when distributed processing is enabled. Shape-evaluation tasks are divided into `num_chunks` and distributed among active workers. If `enable_parallelization` is `True`, each worker processes them with `num_processes` processes in parallel.
:::info
See [Advanced Topics > Distributed Processing Across Compute Nodes](../advanced/distribution.md) for details.
:::

### Output settings
- `resource_dir: str | null` ... Working-directory name for shape optimization. Intermediate files and results from the eMotorSolution API and pyemsol are stored here. When `null`, a `resources` directory is automatically created in the project folder and used as the working directory (only for shape optimization).
- `output_dir: str | null` ... Output-directory name for optimization progress. When `null`, an `opt_progress` directory is automatically created in the project folder and used as the output directory.
- `output_interval: int` ... Interval for all output, including the GUI. With 1, output is produced every iteration; with 2, every two iterations; and so on.
- `output_control` ... Settings for each output file.
  - `best_individual` ... Information about the elite solution (Pareto solutions in multi-objective optimization).
    - `filename_base: str` ... File name
    - `enabled: bool` ... Enable or disable output
    - `output_interval: int` ... Individual output interval
  - `candidate` ... Information about all evaluated individuals.
    - `filename_base: str` ... File name
    - `enabled: bool` ... Enable or disable output
    - `output_interval: int` ... Individual output interval
  - `candidate_plot` ... Distribution plot of candidate-solution vectors generated in each generation.
    - `filename_base: str` ... File name
    - `enabled: bool` ... Enable or disable output
    - `output_interval: int` ... Individual output interval
- `enable_progress_gui: bool` ... Enables or disables the GUI.
