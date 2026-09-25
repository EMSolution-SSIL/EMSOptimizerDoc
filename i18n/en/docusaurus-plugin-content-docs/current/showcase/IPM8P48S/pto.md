---
sidebar_position: 2
---

# IPM8P48S Simultaneous Shape and Topology Optimization
This page introduces the `IPM8P48S_pto` project.  
This project performs simultaneous shape and topology optimization of the IPM8P48S model.
:::info
The eMotorSolution API is required to run this project.
:::

## Optimization overview
In the `IPM8P48S_pto` project, the rotor component structure (permanent magnets and flux barriers) is represented by shape parameters, while the fine topology of the rotor surface is determined by the NGnet on/off method.  
Because the rotor-surface structure is known to contribute particularly to torque ripple, this optimization minimizes torque ripple while using simple shape parameters for the component structure and seeking a novel rotor-surface structure.  
![IPM8P48S PTO overview](/img/IPM8P48S_pto_ex.png)

## machine.yaml (`IPM8P48S_pto` project)
The basic `machine.yaml` settings are the same as those in the `IPM8P48S_moo` project, but `ems_project_filepath` is added to link with eMotorSolution for shape optimization.  
The `IPM8P48S_pto` project already includes the eMotorSolution project JSON file, so specify its path.  
```yaml
# ems functionality link
ems_project_filepath: "Path/To/EMSOptimizer/projects/IPM8P48S_pto/IPM8P48S.json"
```
:::info
Set the file path above according to your EMSOptimizer installation.
:::

### Implicit Domain Meshing option
As described above, only the rotor surface is finely modified by topology optimization.  
In this situation, Implicit Domain Meshing can make the mesh excessively fine, so it is disabled by default in the `IPM8P48S_pto` project.

## optimization.yaml (`IPM8P48S_pto` project)
First, we describe the core objects that determine the shape.  
Set `ngnet_mixture` as the level-set function to perform topology optimization with the NGnet on/off method only in the region from radius 78.2 mm to the rotor radius of 80.2 mm.  
At the same time, `ems_shape_builder` is set to `HoleMagnet55`, an object that defines the dimensions of the eMotorSolution Hole Magnet Type55 model used in the original IPM8P48S model (the rotor permanent-magnet and flux-barrier model) using 10 design variables.  
Setting `level_set_function` together with the shape builder determines the shape as follows:
- The rotor component structure is determined by `HoleMagnet55`.
- Fine topology modifications on the rotor surface are made by the NGnet on/off method.
```yaml
level_set_function:
  name: ngnet_mixture
  kwargs:
    sigma: 0.001
    design_region: [[0.0782, 0.0802], [0, 22.5]]
    coordinate: Polar
    boundary_r: 0.0782
    inversed: True
ems_shape_builder:
  name: HoleMagnet55
```

Because this is a single-objective shape optimization, `cmaes` is used as the optimization method.  
The `bounds` values are the lower and upper bounds for the `HoleMagnet55` shape parameters, set with reference to the original IPM8P48S model.
```yaml
evaluator:
  name: pyemsol_shape_evaluator
optimizer:
  name: cmaes
  kwargs:
    seed: 42
    bounds: [[40, 45], [1.5, 2.5], [1.0, 2.0], [11, 13], [20, 22],
             [16, 20], [1.0, 2.0], [0.5, 1.5], [4.0, 6.0], [0.0, 1.0]]
```
:::tip[Simultaneous optimization of analysis conditions, shape, and topology]
In this case, setting `ems_shape_builder` together with `ls_function` performs simultaneous shape and topology optimization \[10\]. The candidate-solution vector is constructed as follows.
```math
\boldsymbol{x} = [\boldsymbol{d}^\text{T}, \boldsymbol{w}^\text{T}]^\text{T}
```
$\boldsymbol{x}$: candidate-solution vector (`Individual.solution`)  
$\boldsymbol{d}$: shape-information vector passed to `ems_shape_builder`  
$\boldsymbol{w}$: level-set-function parameter vector passed to `ls_function`

`bounds` sets the bounds for the 10-dimensional $\boldsymbol{d}$ vector. Bounds for unspecified $\boldsymbol{w}$ components are automatically set to \[-1, 1\].
:::

## optimization_problem.yaml (`IPM8P48S_pto` project)
```yaml
case_names:
  - transient

objectives:
  - function_name: torque_ripple_percentage
    kwargs:
      torque_scale: 8.0

ineq_constraints:
  - function_name: average_torque
    kwargs:
      torque_scale: 8.0
    coefficient: -1
    baseline: 14.62

eq_constraints:
  - function_name: num_connected_components
    kwargs:
      physical_tag: 20
    baseline: 1

other_metrics:
  - function_name: average_torque
    kwargs:
      torque_scale: 8.0
  - function_name: torque_ripple_percentage
    kwargs:
      torque_scale: 8.0
```
The optimization problem is defined below. It minimizes torque ripple while constraining average torque not to fall below the original-model value of 14.62 Nm. The rotor-core connectivity constraint is also considered.
```math
\begin{align*}
\text{minimize} \quad & f_1=T_\text{rip} \\
\text{subject to} \quad & g_1=-(T_\text{avg}-14.62) \leq 0 \\
                        & h_1=N-1 = 0 \\
\end{align*}
```
$T_\text{avg}$: average torque [Nm]  
$T_\text{rip}$: torque ripple [%]  
$N$: number of connected components

## Optimization example
The shape evolution is shown below. The rotor component and surface structures change simultaneously and gradually converge to a stable structure.    
![IPM8P48S PTO evolution history](/img/IPM8P48S_pto_best_individuals.gif)

The GUI after 100 optimization iterations is shown below. The objective value is nearly flat after approximately 80 iterations, indicating convergence.  
The best shape (iteration 81) has a permanent-magnet and flux-barrier structure similar to the original model, while topology optimization produces a distinctive rotor-surface structure. Average torque is 15.597 Nm and torque ripple is 12.578%.  
Since the minimum torque ripple in the [multi-objective topology optimization](./basic_moo.md) example was approximately 20%, this rotor-surface structure may reduce torque ripple.  
![IPM8P48S PTO result](/img/IPM8P48S_pto_check.png)

## Considering a stress constraint
Since v0.7.0, EMSOptimizer can be linked with the auxiliary analysis tool eMachineSim.  
The `IPM8P48S_pto_structural` project is an optimization example that adds a maximum von Mises stress constraint of 250 MPa at 15,000 rpm to `IPM8P48S_pto`.  

The `IPM8P48S_pto_structural` project has the following structure.  
As with the pyemsol electromagnetic-analysis input files, eMachineSim input files are stored in same-named folders under the project. Rotational speed and constraints are defined in the input files; see the eMachineSim documentation for details.  
```txt
IPM8P48S_pto_structural/
├── structural/
│    └── structural.json  # eMachineSim用入力ファイル
├── transient/
│    └── transient.json  # pyemsol用入力ファイル
├── IPM8P48S.json  # eMotorSolutionプロジェクトファイル
├── machine.yaml
├── optimization_problem.yaml
└── optimization.yaml
```

In `optimization_problem.yaml`, list the analysis-case names in `case_names` and specify the case used by each evaluation function, regardless of whether it is a pyemsol or eMachineSim case.  
Here, the `von_mises_stress` evaluation function is configured to use the `structural` analysis case.  
```yaml
case_names:
  - transient
  - structural

objectives:
  - function_name: torque_ripple_percentage
    kwargs:
      torque_scale: 8.0

ineq_constraints:
  - function_name: average_torque
    kwargs:
      torque_scale: 8.0
    coefficient: -1
    baseline: 14.62
  - function_name: von_mises_stress
    case_name: structural
    kwargs:
      prohibit_seperated: True
    normalization_const: 250e6
    baseline: 250e6

eq_constraints:
  - function_name: num_connected_components
    kwargs:
      physical_tag: 20
    baseline: 1

other_metrics:
  - function_name: average_torque
    kwargs:
      torque_scale: 8.0
  - function_name: torque_ripple_percentage
    kwargs:
      torque_scale: 8.0
  - function_name: von_mises_stress
    case_name: structural
    kwargs:
      prohibit_seperated: True
```

The GUI after 100 optimization iterations is shown below.  
The maximum von Mises stress of the best shape is 214 MPa, below the 250 MPa limit.  

![IPM8P48S PTO structural result](/img/IPM8P48S_pto_structural_check.png)

The figure below visualizes the von Mises stress of the best shape. Stress is concentrated in the ribs between the permanent magnets.  
This method provides a simple way to prevent excessive stress during optimization, but note that analysis accuracy depends on the mesh.  
![IPM8P48S PTO structural stress](/img/IPM8P48S_pto_structural_stress.png)
