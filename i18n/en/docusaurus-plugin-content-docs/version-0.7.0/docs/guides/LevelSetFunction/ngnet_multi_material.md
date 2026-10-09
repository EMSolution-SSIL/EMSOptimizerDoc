---
sidebar_position: 5
---

# ngnet_multi_material
This is an NGnet implementation for three-material optimization. It is used for shape representation in the multi-material NGnet on/off method\[3\].  
In principle, it can represent arbitrary distributions consisting of three materials\[12\], \[17\].

## Overview
In the multi-material NGnet on/off method, at each position $\boldsymbol{x}$ in the design region, two weight vectors (design variables) $\boldsymbol{w}_{1}, \boldsymbol{w}_{2}$ are used to calculate $y_{1} = y(\boldsymbol{w}_{1}, \boldsymbol{x}), y_{2} = y(\boldsymbol{w}_{2}, \boldsymbol{x})$, where $y$ is the NGnet function.  
The material at each position is then determined by mapping $y_{1}, y_{2}$ to a material map.  
Following references \[12\] and \[17\], this implementation uses the material map below. Specifically, `level 1` through `level 3` are assigned according to $\theta^{\text{mat}}(\boldsymbol{x}) = \text{arctan2}(y_{2}, y_{1})$.

![NGnet multi-material map](/img/NGnet_multi_material_map.png)

:::info
This implementation assumes that `id for level 1` through `id for level 3` are configured in `machine.yaml` > `target_ids_and_onoff`.  
See [User Guide > Machine Configuration (machine.yaml)](../machine_config.md) for details.
:::
:::tip[Example of multi-material representation]
This type of multi-material representation is useful when the design target consists of multiple materials.  
An application to rotor topology optimization of a permanent magnet synchronous motor is presented in the [Showcase](../../../showcase/Dmodel/multi_material.md).
:::

## Configurable keyword arguments
- `coordinate: str` ... Coordinate system used to construct the NGnet: "Cartesian" or "Polar".
- `sigma: float` ... Standard deviation of the Gaussian basis functions in the NGnet. The default is `1`.
- `design_region: list[list[float, float], list[float, float]]` ... Region used to construct the NGnet (the design region). When `coordinate` is `Cartesian`, specify a rectangular region $[[x_1, x_2], [y_1, y_2]]$; when it is `Polar`, specify a sector region $[[r_1, r_2], [\theta_1, \theta_2]]$.
- `distance_factor: float` ... Determines the spacing between Gaussian basis functions. Values below 1 place the functions so that they overlap more. The default is `0.8`.
- `dimension: str` ... Dimension in which to arrange the Gaussian basis functions: "2D" or "3D". The default is "2D".
- `eliminate_bases_on_edge: bool` ... Whether to remove Gaussian basis functions at the region boundaries. The default is `False`.
- `normalize_output: bool` ... Whether to normalize the NGnet output. When `False`,  
$y(\boldsymbol{w}, \boldsymbol{x}) = \sum_{i=1}^{N} w_i G_i(\boldsymbol{x}) \\$
is used. The default is `True`.
- `check_basis_GUI: bool` ... When True, launch a GUI at startup to inspect the arrangement of the Gaussian basis functions.
- `angle_1: float` ... Material-map angle $\theta_{1}^{\text{mat}}$ assigned to Level 1 \[deg\]. The default is `120.0`.
- `angle_2: float` ... Material-map angle $\theta_{2}^{\text{mat}}$ assigned to Level 2 \[deg\]. The default is `120.0`.
:::info
The angle assigned to Level 3 is $\theta_{3}^{\text{mat}} = 360 - \theta_{1}^{\text{mat}} - \theta_{2}^{\text{mat}}$\[deg\].
:::
:::tip[Setting `angle_1` and `angle_2`]
`ngnet_multi_material` has the property that a material is more likely to appear in the design region when its material-map angle is larger\[12\].  
Therefore, setting a larger angle for a material expected to occupy a larger average proportion may improve optimization convergence.  
However, experience shows that depending on the optimization process, the material distribution may converge to one that reduces the objective function regardless of the material-map angles.
:::
- `insert_circle: bool` ... Add a circular region to the representation space formed by the two NGnet outputs, increasing the number of material states by one. The default is `false`.
- `circle_radius: float` ... Radius of the circular region used when `insert_circle=True`. The default is `0.5`.
- `insert_third_ngnet: bool` ... Add a third NGnet and a material state based on its sign. The default is `false`.
:::tip[Material representation for multi-material]
The combination of `insert_circle` and `insert_third_ngnet` changes the output levels and design-variable dimensionality \[36\], \[37\].
| Setting | Design-variable dimension | Representation |
|---|---:|---|
| Both `False` | `2K` | Conventional three-material representation |
| `insert_circle=True` | `2K` | Four-material representation with a circular region |
| `insert_third_ngnet=True` | `3K` | Four-material representation using a third NGnet |
| Both `True` | `3K` | Five-material representation using a circular region and a third NGnet |

*`K` ... Number of Gaussian basis functions.
:::
- `fixed_design_region: list[list[float, float], list[float, float]] | null` ... Force the output outside this range to 1. Specify it in the same way as `design_region`.
