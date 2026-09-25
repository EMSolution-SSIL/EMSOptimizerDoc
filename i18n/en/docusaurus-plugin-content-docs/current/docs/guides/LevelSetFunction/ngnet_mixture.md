---
sidebar_position: 4
---

# ngnet_mixture
An implementation example that combines [SimpleLevelSetRadius](ls_r.md) and [NGnet](ngnet.md) and applies the NGnet function within a specified radius.

## Overview
The following values are returned based on the dimensional parameter $\boldsymbol{w}$, the `boundary_r` configuration, and the radius $r$ at each point in the design region. When the `inversed` argument is `True`, the ranges are reversed.
- $r > \text{boundary\_r}$ → 1 (fix the material to `level 0`)
- $r \leq \text{boundary\_r}$ → NGnet output with the dimensional parameter $\boldsymbol{w}$ applied

:::info
This implementation can be used, for example, when you want to fix the material outside a specified rotor radius, or conversely when you want to apply the NGnet on/off method only to the rotor surface.  
See the [Showcase](../../../showcase/IPM8P48S/pto.md) for an example.
:::

## Configurable keyword arguments
- `coordinate: str` ... Coordinate system used to construct the NGnet: "Cartesian" or "Polar".
- `sigma: float` ... Standard deviation of the Gaussian basis functions in the NGnet. The default is `1`.
- `design_region: list[list[float, float], list[float, float]]` ... Region used to construct the NGnet (the design region). When `coordinate` is `Cartesian`, specify a rectangular region $[[x_1, x_2], [y_1, y_2]]$; when it is `Polar`, specify a sector region $[[r_1, r_2], [\theta_1, \theta_2]]$.
- `boundary_r: float` ... Radius defining the boundary for applying NGnet.
- `inversed: bool` ... Whether to reverse the range where NGnet is applied. The default is `False`.
- `distance_factor: float` ... Determines the spacing between Gaussian basis functions. Values below 1 place the functions so that they overlap more. The default is `0.8`.
- `dimension: str` ... Dimension in which to arrange the Gaussian basis functions: "2D" or "3D". The default is "2D".
- `eliminate_bases_on_edge: bool` ... Whether to remove Gaussian basis functions at the region boundaries. The default is `False`.
- `normalize_output: bool` ... Whether to normalize the NGnet output. When `False`,  
$y(\boldsymbol{w}, \boldsymbol{x}) = \sum_{i=1}^{N} w_i G_i(\boldsymbol{x}) \\$
is used. The default is `True`.
- `fixed_design_region: list[list[float, float], list[float, float]] | null` ... Force the output outside this range to 1. Specify it in the same way as `design_region`.
- `check_basis_GUI: bool` ... When True, launch a GUI at startup to inspect the arrangement of the Gaussian basis functions.
