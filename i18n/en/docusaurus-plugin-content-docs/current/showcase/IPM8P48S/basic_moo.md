---
sidebar_position: 1
---

# IPM8P48S Description and Basic Optimization Example
This page describes IPM8P48S and introduces the contents of the `IPM8P48S_moo` project.

## Model description
IPM8P48S is an eight-pole, 48-slot (distributed-winding) interior permanent magnet synchronous motor (IPMSM) virtual model. It is one of the motor models proposed in reference \[16\] and is based on a motor for automotive drive systems.    
The mesh included with the `IPM8P48S_moo` project is an eighth model, and material information (material ID: material name) is assigned to each region.  
The figure below shows the rotor model and material information. For topology optimization, the air holes (flux barriers) in the original model have been filled with rotor core.

![IPM8P48S example](/img/IPM8P48S_ex.png)

## machine.yaml (`IPM8P48S_moo` project)
First, examine `machine.yaml`, which configures the machine information.
### Basic settings
IPM8P48S is defined by radius and angle in the `Polar` coordinate system.
```yaml
coordinate: Polar
```

IPM8P48S is a half-pole-symmetric model.
```yaml
has_sym_region: True
```

The symmetry axis is at 22.5° from the x-axis.
```yaml
sym_deg: 22.5
```

There is no rotationally symmetric region in the eighth model.
```yaml
num_rotate: 0
```

### Material settings
Here, the design target is the rotor core (material ID 20), with the following settings.
- ON-state material → rotor core (material ID 20)
- OFF-state material → air hole (material ID 600000)
```yaml
target_ids_and_onoff:
  20:
    - 20
    - 600000
```

The material IDs and names are assigned as follows.
```yaml
physical_id_to_name:
  20: rotor
  30: shaft
  40: airgap
  50000: magnet_0_0_0
  50001: magnet_1_0_0
  600000: hole_0
```

This is the material-ID map for the symmetric region. **Permanent magnet `50000` becomes `50001` across the symmetry axis, so this mapping is configured here.** The other materials do not change across the symmetry axis and are mapped to the same IDs.
```yaml
mirror_id_map:
  20: 20
  30: 30
  40: 40
  50000: 50001
  600000: 600000
```

Because there is no rotationally symmetric region, `increment_info` is empty.
```yaml
increment_info: {}
```

### Implicit Domain Meshing options
Implicit Domain Meshing is enabled by default.
```yaml
use_implicit_domain_meshing: True
```

Regions other than the design target (`20: rotor`) are not split.
```yaml
no_split_ids:
  - 30
  - 40
  - 50000
  - 50001
```

The sliding-mesh region (`40: air`) is also placed in `no_remesh_ids` because it must not be remeshed.  
Remeshing this region would make the mesh inconsistent with the stator side.
```yaml
no_remesh_ids:
  - 40
```

The mesh-quality-related settings are assigned appropriate values.
```yaml
design_region_size: 0.04
hausd_ratio: 0.0001
hmin_ratio: 0.02
```

Finally, the evaluation-skip threshold is set to 0.02. Compared with Dmodel, IPM8P48S is more likely to generate flattened elements during optimization, so a somewhat lower threshold is used here to prioritize optimization performance.
```yaml
bad_mesh_threshold: 0.02
```

## optimization.yaml (`IPM8P48S_moo` project)
Next, examine `optimization.yaml`, which configures the optimization.  
Because this is a multi-objective shape optimization, the multi-objective `decomposition_ensemble` algorithm is selected. See the [corresponding documentation page](../../docs/guides/Optimizer/decomposition_ensemble.md) for details.
```yaml
evaluator:
  name: pyemsol_shape_evaluator
optimizer:
  name: decomposition_ensemble
  kwargs:
    num_decomposition: 5
    seed: 42
```

The `ngnet` level-set function is used to perform topology optimization with the NGnet on/off method.
```yaml
level_set_function:
  name: ngnet
  kwargs:
    sigma: 0.003
    design_region: [[0.040, 0.0802], [0, 22.5]]
    coordinate: Polar
```

This example uses 100 optimization iterations.  
Parallel processing is enabled by default.
```yaml
num_iteration: 100
enable_parallelization: True
num_processes: Null  # if Null, automatically set from cpu counts
```
(Output-related settings are omitted.)

## optimization_problem.yaml (`IPM8P48S_moo` project)
```yaml
case_names:
  - transient

objectives:
  - function_name: average_torque
    kwargs:
      torque_scale: 8.0
    normalization_const: 14.62
    coefficient: -1.0
  - function_name: torque_ripple_percentage
    kwargs:
      torque_scale: 8.0
    normalization_const: 35.34
    coefficient: 1.0

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
The multi-objective optimization problem is defined below. It considers both average torque and torque ripple, while constraining average torque not to fall below the original-model value of 14.62 Nm. The rotor-core connectivity constraint is also considered.
```math
\begin{align*}
\text{minimize} \quad & f_1=-\frac{T_\text{avg}}{14.62} \\
                      & f_2=\frac{T_\text{rip}}{35.34} \\
\text{subject to} \quad & g_1=-(T_\text{avg}-14.62) \leq 0 \\
                        & h_1=N-1 = 0 \\
\end{align*}
```
$T_\text{avg}$: average torque [Nm]  
$T_\text{rip}$: torque ripple [%]  
$N$: number of connected components

## Optimization example
The GUI after 100 optimization iterations is shown below. A relatively broad and uniform Pareto front is obtained.  
The example shapes shown are the solutions labeled "Left" and "Right" in the Pareto-front plot. Their flux-barrier arrangements are similar, but the rotor-surface-side flux barriers differ. The "Right" solution has elongated flux barriers and offers a relatively good balance between average torque and torque ripple. In contrast, the "Left" solution has semicircular flux barriers arranged to confine the magnetic flux, suggesting a high-torque motor.
![IPM8P48S Pareto front](/img/IPM8P48S_moo_check.png)
