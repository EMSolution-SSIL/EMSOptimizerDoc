---
slug: pre-release-v0.7.0
title: Pre-Release V0.7.0
authors: [SSIL]
tags: [change_log]
---

This post provides pre-release information for v0.7.0.

{/* truncate */}

## v0.7.0 pre-release information
The documentation has been updated in preparation for the v0.7.0 release.  
The major updates are listed below. The official release is coming soon.  

### New features
- Integration with eMachineSim
    - Added support for integration with eMachineSim, a tool for analyzing electrical equipment and its surroundings.
    - As with pyemsol, analyses can be run by placing an analysis case folder and specifying it in `optimization_problem.yaml`.
- [Study control and results](/docs/next/docs/guides/study_control_and_results)
    - Added functionality for creating studies. This makes it possible to maintain multiple optimization configurations for a single design target.
    - The results of each study are now saved as runs and can be reviewed later.
- Gradient-based method examples ([gradient-based optimizer](/docs/next/docs/guides/Optimizer/gradient_update), [density-based level_set_function](/docs/next/docs/guides/LevelSetFunction/pyemsol_density))
    - The gradient-based optimizer updates the design variables (the density or level set value of each cell in the design elements) based on gradient information.
    - The density-based level_set_function is a special object defined for pyemsol that triggers gradient computation within pyemsol.
- Added optimizer examples ([moead](/docs/next/docs/guides/Optimizer/moead), [ga](/docs/next/docs/guides/Optimizer/ga), [sa-nsga2](/docs/next/docs/guides/Optimizer/sa_nsga2))
- Added an ems_shape_builder example ([Dmodel_mixed_builder](/docs/next/docs/guides/EMSShapeBuilder/Dmodel_mixed))
- Updated [Commands](/docs/next/docs/guides/commands)
- Updated [Optimization configuration](/docs/next/docs/guides/optimization_config)
    - Added output settings
    - Restart functionality
- Updated [Machine configuration](/docs/next/docs/guides/machine_config)
    - Image output settings
    - Three-dimensional optimization analysis
    - Level set function computation settings
- Updated [Objective and constraint function examples](/docs/next/docs/guides/opt_problem_ex)
- Added [Using surrogate models](/docs/next/docs/advanced/surrogate_model_usage)
- Added [AI-assisted configuration](/docs/next/docs/advanced/ai_usage)

### Major updates and additions
- Updated the [Introduction](/docs/next/docs/getting-started/Introduction)
    - Added information about studies and related concepts.
    - Updated the GUI.
- Added [Optimization problem configuration](/docs/next/docs/guides/optimization_problem_config)
    - Formally documented the content of the [Defining an optimization problem](/docs/next/docs/getting-started/opt_problem) page as a configuration schema.
- Added the [EMSOptimizer Python API](/docs/next/docs/guides/emsopt_api)
    - Starting with v0.7.0, the optimization execution modules (classes) are also provided as an API.
- [Multi-material optimization example](/docs/next/docs/guides/LevelSetFunction/ngnet_multi_material)
    - Added representations for four and five materials

### Showcase updates
- Added [Dmodel mixed-variable optimization](/docs/next/showcase/Dmodel/mixed_variables)
    - This example optimizes mixed variables including permanent magnet material, the number of coil turns, permanent magnet dimensional parameters, and magnetic core topology.
- Added Dmodel synchronous reluctance motor optimization
    - [Density-based optimization](/docs/next/showcase/Dmodel/gradient_density)
    - [Level set-based optimization](/docs/next/showcase/Dmodel/gradient_levelset)
- [IPM8P48S optimization example with stress constraints](/docs/next/showcase/IPM8P48S/pto)
- [IPM8P48S surrogate model example](/docs/next/showcase/IPM8P48S/surrogate)
