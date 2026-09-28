---
sidebar_position: 1
---

# Introduction
This page provides an introduction to optimization with EMSOptimizer.

## Try mathematical optimization with benchmark functions
To try the optimization functionality of EMSOptimizer, run the following command in the `EMSOptimizer` folder.
```sh
python emsopt.py run soo_base
```
This runs single-objective optimization of a benchmark function.
:::info
See the [Showcase](../../showcase/base_optimization/soo_base.md) for an example result from this optimization.
:::

## Try shape optimization
To try the shape optimization sample, run the following command in the root of the `EMSOptimizer` folder.
```sh
python emsopt.py run Dmodel
```
This runs single-objective topology optimization of the permanent magnet synchronous motor benchmark model, “Dmodel”\[1\].
:::info
See the [Showcase](../../showcase/Dmodel/basic.md) for an example result from this optimization.
:::
:::info
Running shape optimization requires the related packages.  
For details, see the [Installation Guide](../intro.md).
:::

## EMSOptimizer overview
### EMSOptimizer projects
EMSOptimizer manages each optimization case as a **project**. A project is represented by a folder under `project`. Project folders contain the following files.
- **Mesh files used as the base model for shape optimization** (`pre_geom2D.msh`, `rotor_mesh2D.msh` when a sliding-motion region is included)
- **Shape-optimization analysis-case folders**
    - Place a JSON file with the same name in each analysis-case folder (the JSON file is an input file for the `pyemsol` electromagnetic simulator package).
- **Optimization configuration (YAML files)**
    - `mahcine.yaml`: Configuration related to the machine being optimized during shape optimization
    - `optimization_problem.yaml`: Configuration defining the shape optimization problem, including objectives and constraints
    - `optimization.yaml`: Configuration related to optimization execution, such as the number of optimization iterations

Several example projects are already included in the `project` folder. The `Dmodel` project used in the introductory example is one of them.

The figure below shows the actual structure of the `Dmodel` project. `pre_geom2D.msh` and `rotor_mesh2D.msh` are the stator and rotor mesh files, respectively. The project also contains the `transient` analysis case.

![Project folder example](/img/project_folder.png)

To optimize a project, execute the `run` command as follows.  
```sh
python emsopt.py run {プロジェクト名}
```

### Basic optimization workflow
**The basic workflow for optimization with EMSOptimizer is as follows.**
1. Create a new project folder under `project`, or clone an existing project from the CLI with the `cp_proj` command.
2. For shape optimization, place the mesh files and analysis-case folders in the project folder.
3. For shape optimization, configure `machine.yaml` according to the mesh files and analysis cases.
4. For shape optimization, define the optimization problem to solve (for example, maximizing average torque) in `optimization_problem.yaml`.
5. Configure the optimization method and other settings in `optimization.yaml`.
6. Run the optimization from the CLI with the `run` command.
7. After optimization is complete, use the `check` command to inspect the results if necessary.

### Try it yourself
We begin by cloning a project with the `cp_proj` command.
For example, to run Dmodel optimization as a separate project, clone the `Dmodel` project with the following command.
```sh
python emsopt.py cp_proj Dmodel NewDmodel
```

The copied project is created automatically in the `project` folder.  
Edit the files in the NewDmodel project folder to configure it.

For example, change `optimization.yaml` > `level_set_function` > `kwargs` > `sigma` from `0.0013` to `0.0010` as follows.  
This produces more complex changes in the resulting motor shape.
```yaml
level_set_function:
  name: ngnet
  kwargs:
    sigma: 0.0010
    design_region: [[0.008, 0.0275], [0, 45.0]]
    coordinate: Polar
```
:::tip NGnet settings
The `sigma` value corresponds to the standard deviation of each Gaussian basis function composing the NGnet \[3\] that defines the rotor shape.  
By default, basis functions are placed automatically to fill `design_region`. 
See [User Guide > LevelSetFunction > NGnet](../guides/LevelSetFunction/ngnet.md) for details.
:::

Run the optimization with the `run` command.
```sh
python emsopt.py run NewDmodel
```

When the `run` command starts the optimization, the GUI launches by default so that you can monitor progress.  
![GUI example](/img/GUI_ex.png)  
:::info
To disable the GUI, set `enable_progress_gui` in `optimization.yaml` to `False`.  
For details about other optimization settings, see [User Guide > Optimization settings](../guides/optimization_config.md).
:::

Optimization completes after the configured number of iterations or when stopped from the GUI. The GUI remains available after completion; close it or enter `Ctrl+C` in the CUI (command line) to terminate the process completely.

The GUI can also be launched after the process ends with the `check` command. This is mainly useful for reviewing completed optimization runs.
```sh
python emsopt.py check NewDmodel
```

### GUI
![GUI (single-objective optimization)](/img/GUI_soo.png)

① Optimization control panel.
- `Stop`: Stop optimization
- `Pause / Resume`: Pause or resume optimization

:::info
Stopping and pausing take effect when the current optimization iteration finishes. To interrupt the calculation immediately, enter `Ctrl+C` in the CLI, although this may damage the working directory and related files.
:::

② Optimization-progress graph. For single-objective optimization, it shows objective value versus optimization iteration; for multi-objective optimization, it shows the Pareto front. Clicking the graph displays the corresponding shape image in ③.

:::info
For multi-objective optimization, the Pareto front is plotted using two objective values as the vertical and horizontal axes. Use the combo boxes above the graph to switch the displayed axes.
:::

③ Shape-image window. The shape of the individual clicked in ② is displayed in the left window together with the function values registered in `optimization_problem.yaml` > `other_metrics`. For single-objective optimization, the best shape in each iteration is displayed automatically.
- `Save outcome`: Saves the displayed image and individual information in the `project` folder.
- `Pin to right`: Pins the image in the left window to the right window.
- `Remove pinned`: Removes the image from the right window.

④ Comparison-metrics graph. The `other_metrics` values for the shape shown in ③ are displayed as a bar graph. The graph shows ratios relative to the function values of the shape in the right window, which are set to 1. If no shape is in the right window, all metrics are displayed as 1.
