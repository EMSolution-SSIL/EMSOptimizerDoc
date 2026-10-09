---
sidebar_position: 1
---

# `MagneticShield_3D` Optimization
This page introduces the `MagneticShield_3D` project.

## Model description
MagneticShield3D is a model of a three-dimensional magnetic-shield structure (original model: reference \[34\]).  
The protected region, `3: "Target"`, is surrounded by `2: "design"`, a magnetic material with a linear relative permeability of 200, to prevent magnetic fields from entering it.  
This project optimizes the magnetic-material structure using the NGnet on/off method.

![MagneticShield3D example](/img/MagneticShield3D_ex.png)

## machine.yaml (`MagneticShield3D` project)
First, examine `machine.yaml`, which configures the machine information.
### Basic settings
This is a three-dimensional analysis, and the optimization target is `pre_geom.msh`. Unlike the motor examples, the model has no sliding-motion region, so this is the only input mesh. The coordinate system is Cartesian (xyz).
```yaml
# analysis dimension
analysis_dimension: 3D

# design target: "pre_geom" or "rotor"
design_target: pre_geom

# coordinate system: 'Cartesian' or 'Polar'
coordinate: Cartesian
```

The analysis region contains no line-symmetric or rotationally symmetric region.
```yaml
# whether design region includes symmetric region
has_sym_region: False
```

### Material settings
The design target is the magnetic shielding material (material ID 2):
- On-state material → magnetic material (material ID 2)
- Off-state material → air hole (material ID 600000)
```yaml
# on/off material information
target_ids_and_onoff:
  2:
    - 2
    - 600000
```

The following assigns material IDs to names. IDs `6`–`9` are assigned to the coil surfaces for defining current sources in pyemsol.  
ID 4 is a thin air layer placed between `2: Design` and `4: Air` for the Implicit Domain Meshing operation described below.
```yaml
physical_id_to_name:
  1: Coil
  2: Design
  3: Target
  4: Air
  5: layer
  6: Coil_top
  7: Coil_outer
  8: Coil_bottom
  9: Coil_inner
  600000: Hole
```

### Implicit Domain Meshing option
Implicit Domain Meshing is enabled by default.
```yaml
use_implicit_domain_meshing: True
```

Regions other than the design target (`2: Design`) are not split.
```yaml
# material boundaries of no_split_ids will be preserved after remeshing
no_split_ids:
  - 1
  - 3
  - 4
  - 5
  - 6
  - 7
  - 8
  - 9
```

The coil and surrounding air should not be remeshed, so they are listed in `no_remesh_ids`.  
```yaml
# mesh of no_remesh_ids will be preserved after remeshing
no_remesh_ids:
  - 1
  - 4
  - 6
  - 7
  - 8
  - 9
```
:::tip[Remeshing in 3D optimization]
In this configuration, `2: Design` is remeshed and contacts `3: Target` and `4: Air`.  
Because `4: Air` contacts `1: Coil`, it is configured not to be remeshed.  
To connect the remeshed `2: Design` result to the fixed mesh of `4: Air`, a thin air layer (`5: layer`) that permits remeshing is placed between them.
:::

Mesh-quality-related settings are assigned appropriate values.
```yaml
# approximate design region size
design_region_size: 1.0

# hausd option ratio to design region size
# stands for maximum Hausdorff distance (approximation error) for level set boundaries
hausd_ratio: 0.001

# hmin option (minimum size of mesh) ratio to design region size
hmin_ratio: 0.01
```

Finally, the evaluation-skip threshold is set to 0.001.
```yaml
# if mesh quality (>= 0, <= 1) is less than bad_mesh_threshold after remeshing, the individual will be skipped
bad_mesh_threshold: 0.001
```

## optimization.yaml (`MagneticShield3D` project)
Next, examine `optimization.yaml`, which configures the optimization.  
Because this is a single-objective shape optimization, `cmaes` is specified as the `optimizer`.  
The `level_set_function` is set to `ngnet`, which places Gaussian basis functions over `[[0, 0.140], [0, 0.140], [0, 0.140]]`, which contains the design region.
```yaml
# optimization dependencies
evaluator:
  name: pyemsol_shape_evaluator
optimizer:
  name: cmaes
  kwargs:
    seed: 42
level_set_function:
  name: ngnet
  kwargs:
    sigma: 0.04
    design_region: [[0, 0.140], [0, 0.140], [0, 0.140]]
    dimension: 3D
    coordinate: Cartesian
```

This example uses 100 optimization iterations.  
Parallel processing is enabled by default.
```yaml
num_iteration: 100
enable_parallelization: True
num_processes: Null  # if Null, automatically set from cpu counts
```
(Output-related settings are omitted.)

## optimization_problem.yaml (`MagneticShield3D` project)
```yaml
case_names:
  - static

objectives:
  - function_name: magnetic_energy
    kwargs:
      physical_tag: 3
    normalization_const: 1.0e-14
    coefficient: 0.5
  - function_name: material_volume
    kwargs:
      physical_tag: 2
    normalization_const: 0.002744
    coefficient: 0.5

ineq_constraints: []

eq_constraints: []

other_metrics:
  - function_name: magnetic_energy
    kwargs:
      physical_tag: 3
  - function_name: material_volume
    kwargs:
      physical_tag: 2
```
The optimization problem minimizes `magnetic_energy` (the magnetic energy in protected region `3`) and `material_volume` (the amount of magnetic material used).

## Optimization example
The optimization progress is shown below. An approximately two-layer magnetic-material structure is obtained.  
The magnetic material has a three-dimensional rather than axisymmetric structure, showing that the optimization reduces the amount of magnetic material used.
![Magnetic-shield optimization progress](/img/magshield3d_best_individuals.gif)

The magnetic-flux-density distribution in the optimized structure is shown below, visualized with pyemsi. Most of the flux passes through the outer layers, protecting the target region.  
![Magnetic-shield magnetic flux density](/img/magshield3d_countor.png)
