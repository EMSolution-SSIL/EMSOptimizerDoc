---
sidebar_position: 5
---

# Dmodel Synchronous Reluctance Motor Optimization Example
This page introduces the `Dmodel_SynRM` project.  
`Dmodel_SynRM` assumes a synchronous reluctance motor (SynRM) and optimizes the air/magnetic-core distribution in a rotor region without permanent magnets.  
In addition to optimizing torque characteristics, this example incorporates stress evaluation through eMachineSim integration.  

## Base mesh
As in the [multi-material optimization example](./multi_material.md), `Dmodel_SynRM` uses a base mesh whose rotor contains no permanent magnets and consists only of material ID `20` (magnetic core). The air/magnetic-core distribution is optimized throughout the rotor.

## optimization.yaml (`Dmodel_SynRM` project)
In `optimization.yaml`, `level_set_function` is set to `ngnet_mixture` to fix the outermost 0.2 mm of the rotor as magnetic core and arrange Gaussian basis functions in the range \[0.008, 0.0273\], excluding the outer 0.2 mm.  
```yaml
level_set_function:
  name: ngnet_mixture
  kwargs:
    boundary_r: 0.0273
    sigma: 0.0010
    design_region: [[0.008, 0.0273], [0, 45.0]]
    coordinate: Polar
```

## Optimization Example
This example performs 200 iterations of single-objective optimization to maximize average torque.  
The GUI after completing 200 iterations is shown below.  
The objective value continues to improve until late in the optimization, eventually converging to a shape with two large layers of flux barriers.  

![Dmodel SynRM optimization history](/img/Dmodel_SynRM_check.png)

## Additional optimization with stress evaluation
The optimized shape is supported by a 0.2-mm bridge at the surface.  
Such a thin section may fracture during high-speed rotation, so practical optimization should account for the stress distribution.  
Here, the optimized shape is used as the initial shape, and optimization is performed with the maximum stress during high-speed rotation (15,000 rpm) as a constraint.  

The optimization problem (optimization_problem.yaml) is configured as follows.  
```yaml
case_names:
  - transient
  - structural

objectives:
  - function_name: average_torque
    kwargs:
      torque_scale: 4.0
    normalization_const: 2.1
    coefficient: -1.0

ineq_constraints:
  - function_name: von_mises_stress
    case_name: structural
    kwargs:
      prohibit_seperated: True
    normalization_const: 200e6
    baseline: 200e6

eq_constraints:
  - function_name: num_connected_components
    case_name: transient
    kwargs:
      physical_tag: 20
    baseline: 1
```
First, `structural` has been added to `case_names`. The `Dmodel_SynRM` project already contains a `structural` folder and input file. This input file is for eMachineSim and describes the analysis conditions.  
`von_mises_stress` is specified in `ineq_constraints`, constraining the maximum von Mises stress to 200 MPa or less. In `eq_constraints`, `num_connected_commponents` is constrained to `1` so that the rotor core remains connected.  

The GUI after completing the additional 200-iteration optimization is shown below.  
At the initial stage (right image), the maximum stress (Metrics 2) is approximately 254 MPa and violates the constraint. After optimization (left image), the maximum stress is reduced to approximately 199 MPa. Although the average torque decreases, the optimization accounts for mechanical strength during high-speed rotation.

![Dmodel SynRM additional optimization history](/img/Dmodel_SynRM_additional_check.png)
