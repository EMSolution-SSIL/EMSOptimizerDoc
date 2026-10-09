---
sidebar_position: 3
---

# Implicit Domain Meshing
## Overview
In remeshing with Implicit Domain Meshing\[13\], the mesh in the region where the level set function is applied is deformed and regenerated along the zero level set of the function. Since the zero level set is often the material boundary in topology optimization, this can be broadly described as a method that **remeshes the region so that mesh nodes and edges are placed exactly on the material boundary**.

EMSOptimizer uses mmg (`mmg2d_O3`, `mmg3d_O3`) as the execution tool for Implicit Domain Meshing\[15\]. Remeshing is performed automatically when the `machine.yaml` > `use_implicit_domain_meshing` configuration is `True`. For detailed settings, see [User Guide > Machine Configuration (machine.yaml)](../guides/machine_config.md).

:::info
The mmg executables are stored directly under the EMSOptimizer folder.  
When running from outside the folder, set the paths to the mmg executables in the `MMG2D_EXE_PATH` (2D) and `MMG3D_EXE_PATH` (3D) environment variables.
:::

:::warning
When using Implicit Domain Meshing, **the mesh files stored in the project must consist only of triangular elements**.  
The accuracy with which boundaries are reproduced in the generated mesh also depends on the resolution (fineness) of the original mesh file. Consider increasing the mesh-file resolution if more accurate material boundaries are required.
:::

## Example using Implicit Domain Meshing
Example Dmodel shape from topology optimization (NGnet on/off method) **with** Implicit Domain Meshing. The material boundary is smooth. The mesh has approximately 3,000 nodes.
![Dmodel mesh example with IDM](/img/IDM_Dmodel.png)

For comparison, this is an example Dmodel shape using the same level set function **without** Implicit Domain Meshing. The material distribution is similar, but the material boundary is coarse and jagged because the calculation uses a fixed mesh. The mesh has approximately 4,000 nodes.
![Dmodel mesh example without IDM](/img/NonIDM_Dmodel.png)

## Detailed explanation
In topology optimization based on the on/off method, the material is normally switched on or off for each element of a fixed mesh. However, material boundaries do not necessarily coincide with mesh nodes and edges. As the mesh becomes coarser, the difference between the overall level set function and the resulting shape increases, and material boundaries are more likely to become jagged. One way to avoid this is to refine the mesh in the design region, but computation time increases as the mesh is refined.

In contrast, **Implicit Domain Meshing provides smooth material boundaries in principle**\[10\]. Because it eliminates the need to analyze with a mesh finer than the required accuracy, it can also reduce analysis time. However, remeshing is required for each shape, and EMSOptimizer has limitations such as allowing only two levels to be configured in `target_ids_and_onoff`.  
If the level set function contains a complex zero level set, the mesh may concentrate around it and become excessively fine. This can be partially mitigated by setting larger values for `machine.yaml` > `hausd_ratio` and `hmin_ratio`.
