---
sidebar_position: 3
---

# NGnet
This is an NGnet implementation. It is used for shape representation in the NGnet on/off method\[3\].

## Overview
NGnet $y(\boldsymbol{w}, \boldsymbol{x})$ is defined as follows (for a two-dimensional `coordinate` space).
```math
y(\boldsymbol{w}, \boldsymbol{x}) = \sum_{i=1}^{N} w_i b_i(\boldsymbol{x}) \\
b_i(\boldsymbol{x}) = \frac{G_i(\boldsymbol{x})}{\sum_{j=1}^N G_j(\boldsymbol{x})} \\
G_i(\boldsymbol{x}) = \frac{1}{2\pi \sigma_i^2}\exp(-\frac{\|\boldsymbol{x}-\boldsymbol{\mu_i}\|^2}{2\sigma_i^2}) \\
\boldsymbol{w} = \{w_i\}, \boldsymbol{x} = \{x, y\}
```
$\boldsymbol{w}$: Weight vector  
$\boldsymbol{x}$: Coordinate vector  
$N$: Number of Gaussian basis functions in the NGnet  
$\mu_i$: Center vector of the $i$th Gaussian basis function $G_i(\boldsymbol{x})$  
$\sigma_i$: Standard deviation of the $i$th Gaussian basis function $G_i(\boldsymbol{x})$

In the NGnet on/off method, optimizing the weight vector $\boldsymbol{w}$ changes the distribution of $y(\boldsymbol{w}, \boldsymbol{x})$, and the material at each position $\boldsymbol{x}$ in the design region is determined from its value.  
The original paper defines locations where $y(\boldsymbol{w}, \boldsymbol{x})$ is greater than 0 as the ON-state material (magnetic core), and locations where it is 0 or less as the OFF-state material (air).

## Configurable keyword arguments
- `coordinate: str` ... Coordinate system used to construct the NGnet: "Cartesian" or "Polar".
- `sigma: float` ... Standard deviation of the Gaussian basis functions in the NGnet. The default is `1`.
- `design_region: list[list[float, float], list[float, float]]` ... Region used to construct the NGnet (the design region). For `Cartesian`, specify a rectangular region $[[x_1, x_2], [y_1, y_2]]$; for `Polar`, specify a sector region $[[r_1, r_2], [\theta_1, \theta_2]]$.
:::tip Placement of Gaussian basis functions
By default, the Gaussian basis functions that make up the NGnet are automatically arranged to fill `design_region`, as shown below.  
Each circle in the figure represents the placement of a Gaussian basis function, and its radius represents the standard deviation. The figure is output as `gaussian.png` directly under the EMSOptimizer folder when shape optimization is run.  
![Gaussian basis-function arrangement](/img/gaussian_arrangement.png)
:::
- `distance_factor: float` ... Determines the spacing between Gaussian basis functions. Values below 1 place the functions so that they overlap more. The default is `0.8`.
- `eliminate_bases_on_edge: bool` ... Whether to remove Gaussian basis functions at the region boundaries. The default is `False`.
- `normalize_output: bool` ... Whether to normalize the NGnet output. When `False`,  
$y(\boldsymbol{w}, \boldsymbol{x}) = \sum_{i=1}^{N} w_i G_i(\boldsymbol{x}) \\$
is used. The default is `True`.
