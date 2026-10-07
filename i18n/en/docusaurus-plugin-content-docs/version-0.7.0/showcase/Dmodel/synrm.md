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
