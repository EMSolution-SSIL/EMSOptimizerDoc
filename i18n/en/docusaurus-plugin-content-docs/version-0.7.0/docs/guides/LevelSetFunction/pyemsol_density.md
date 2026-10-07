---
sidebar_position: 6
---

# `pyemsol_density`
This level set implementation handles density representations of material properties.

## Overview
pyemsol uses a density representation of material properties when calculating objective-function gradients\[26\],\[30\].  
To convert the level set value $\phi$ given as a design variable into a density value $\rho$ (a value in \[0,1\]), an S-shaped function symmetric about $\phi=0$ is applied.
:::info
Some features for gradient-based topology optimization are enabled by setting pyemsol_density for `level_set_function`. See [Showcase > Dmodel > Dmodel gradient-based optimization example (density method)](../../../showcase/Dmodel/gradient_density.md) for an example.
:::

## Configurable keyword arguments
- `proj_method: str` ... Method for converting level set values to density values: `heaviside5`\[26\] or `sigmoid`\[30\]. The default is `heaviside5`.
- `proj_half_width: float` ... Transition-width parameter for `heaviside5`. The default is `1.0`.
- `proj_beta: float` ... Transition-width parameter for `sigmoid`. The default is `1.0`.
- `proj_eta: float` ... Level set value regarded as the midpoint of the material transition. The default is `0`.
- `objective_type: str` ... Type of objective function for gradient calculation. `W1`: torque; `W2`: squared difference from the target torque\[26\]. The default is `W1`.
- `torque_scale: float` ... Torque scale. For a quarter model, set `4.0` to convert the torque to the full-model value. The default is `1.0`.
- `torque_target: float | null` ... Target torque when `objective_type` is `W2`.
- `design_region: list[list[float, float], list[float, float]] | null` ... Design region. Elements outside the design region specified by target in machine.yaml are fixed to on (1). When `coordinate` is `Cartesian`, specify a rectangular region $[[x_1, x_2], [y_1, y_2]]$; when it is `Polar`, specify a sector region $[[r_1, r_2], [\theta_1, \theta_2]]$.
