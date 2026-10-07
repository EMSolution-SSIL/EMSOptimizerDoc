---
sidebar_position: 4
---

# Dmodel Multi-Material Optimization Example
This page introduces the `Dmodel_multi_material` project.  
Unlike the `Dmodel` project, `Dmodel_multi_material` performs multi-material topology optimization. It optimizes the distribution of three materials in the rotor core: air, magnetic core, and permanent magnet.

## Base mesh
The `Dmodel_multi_material` project uses a base mesh whose rotor contains only material ID `20` (magnetic core), without permanent magnets.  
By setting material ID `20` as the design target, the multi-material distribution is optimized throughout the rotor.

![Dmodel multimaterial example](/img/Dmodel_multi_material_ex.png)

## machine.yaml (`Dmodel_multi_material` project)
To configure multi-material optimization, set the three material IDs `machine.yaml`, `target_ids_and_onoff`, and `20` in `50000` > `600000`.  
This enables the `level_set_function` to configure the three materials.  
```yaml
target_ids_and_onoff:
  20:
    - 20
    - 50000
    - 600000
```

:::info
Implicit Domain Meshing cannot be used when three or more materials are specified.
:::

## optimization.yaml (`Dmodel_multi_material` project)
In `optimization.yaml`, specify `level_set_function` as the `ngnet_multi_material`.  
`ngnet_multi_material` is an implementation example that sets three levels at each location in the design region based on the design variables. See [Docs > User Guide > ngnet_multi_material](../../docs/guides/LevelSetFunction/ngnet_multi_material.md) for details about its arguments.  
```yaml
level_set_function:
  name: ngnet_multi_material
  kwargs:
    sigma: 0.0020
    design_region: [[0.008, 0.0275], [0, 45.0]]
    coordinate: Polar
    angle_1: 240
    angle_2: 60
```
:::tip[Setting `angle_1` and `angle_2`]
`angle_1` and `angle_2` represent the angles assigned to the magnetic core and permanent magnet on the material map. The angle assigned to air is $360-240-60=60$\[deg\].  
`ngnet_multi_material` makes a material more likely to appear in the design region when it is assigned a larger angle on the material map \[12\]. Because the rotor of a permanent-magnet synchronous motor generally consists mostly of magnetic core, `angle_1`, corresponding to the magnetic core, is intentionally set to a large value here.
:::

## optimization_problem.yaml (`Dmodel_multi_material` project)
The objectives are unchanged from the `Dmodel` project: maximize average torque and minimize torque ripple.  
The change is the addition of `ineq_constraint` (the area of a specified material) to `material_area`. Set `physical_tag` (permanent magnet) as `50000`.  
This optimization constrains the permanent-magnet area to no more than the original Dmodel value ($4.9975\times10^{-5}\text{m}^2$), seeking an optimal material distribution while using no more permanent magnet than the original.
```yaml
objectives:
  - function_name: average_torque
    kwargs:
      torque_scale: 4.0
    normalization_const: 2.1
    coefficient: -1.0
  - function_name: torque_ripple_percentage
    kwargs:
      torque_scale: 4.0
    normalization_const: 54.0
    coefficient: 0.1

ineq_constraints:
  - function_name: material_area
    kwargs:
      physical_tag: 50000
    baseline: 4.9975e-05
```

## Optimization example
This example runs for 200 optimization iterations.  
The figure below shows the shape evolution over 200 iterations, with the best shape at each iteration animated. The air/magnetic-core/permanent-magnet distribution changes and converges toward a single-layer permanent-magnet and flux-barrier shape.  
![Dmodel multi-material optimization history](/img/Dmodel_multi_material_best_individuals.gif)

The GUI after 200 iterations is shown below.  
Although convergence is slower than in the other examples, the objective values are nearly flat after iteration 130, indicating convergence.  
The best shape shown in the GUI has $T_\text{avg}$=2.5183 Nm, $T_\text{rip}$=24.318%, and permanent-magnet area $S=4.7543\times10^{-5}\text{m}^2$. Compared with the [basic optimization](./basic.md), average torque improves substantially. In multi-material optimization of permanent-magnet motors, the permanent magnets can be reshaped, which is known empirically to make improvements in average torque easier to achieve. Conversely, it is also possible to minimize permanent-magnet area while constraining average torque to remain above a specified level.
![Dmodel multi-material optimization history](/img/Dmodel_multi_material_check.png)
