---
sidebar_position: 2
---

# Integration with eMotorSolution
This page describes integration with the motor design and simulation tool eMotorSolution.

## Enabling integration
To enable integration with eMotorSolution, **set up the eMotorSolution API in the Python environment and configure the following settings**.
- Set the path to the eMotorSolution project file (JSON) to integrate in `machine.yaml` > `ems_project_filepath`.
- Set the path to the executable of the mesh-generation tool gmsh\[14\] in the `GMSH_EXE_PATH` environment variable.
:::info
See the [Installation Guide](../intro.md) for setting up the eMotorSolution API.
:::
:::info
The eMotorSolution API calls gmsh externally as its default mesh-generation tool. When integrating, download the gmsh executable and set its path in the `GMSH_EXE_PATH` environment variable.
:::

## Features
### Dimensional optimization
When integrated with eMotorSolution, **dimensional optimization can be performed with the `ems_shape_builder` core object**. Meshes are generated dynamically through the eMotorSolution API, so mesh files are not required in the EMSOptimizer project folder.
:::info
For configuring dimensional optimization, see [Getting Started > EMSOptimizer Concepts](../getting-started/core_concepts.md), [User Guide > Optimization Configuration](../guides/optimization_config.md), and the eMotorSolution Shape Builder section of the User Guide.  
See the [Showcase](../../showcase/IPM8P48S/pto.md) for an example.
:::

### Analysis Case Control
When integrated with eMotorSolution, shape analysis uses the analysis-case folders in the integrated project. Therefore, analysis-case folders are not required in the EMSOptimizer project folder.
:::info
When integrating, analysis cases must be configured correctly in the eMotorSolution project.  
As when running without integration, configure the analysis-case names correctly in `optimization_problem.yaml` > `case_names`.
:::
