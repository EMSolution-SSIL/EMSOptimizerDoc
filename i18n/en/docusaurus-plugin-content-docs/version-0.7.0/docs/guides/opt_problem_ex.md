---
sidebar_position: 7
---

# Evaluation-function API

## Overview

This page introduces the evaluation functions that can be configured in `optimization_problem.yaml` for shape optimization.
These functions read the pyemsol analysis-result working directory and calculate values used as objectives, constraints, and other metrics.

## Usage

Use an evaluation function by specifying its name in `function_name` in `optimization_problem.yaml`.

```yaml
function_name: average_torque
kwargs:
  torque_scale: 4.0
```

## Quick reference

| API | Type | Main purpose | Return value |
|---|---|---|---|
| `average_torque` | function | Calculates average torque | `float` |
| `torque_density` | function | Calculates torque density | `float` |
| `torque_ripple` | function | Calculates torque ripple | `float` |
| `torque_ripple_percentage` | function | Calculates torque-ripple percentage | `float` |
| `maximum_voltage` | function | Extracts the maximum voltage | `float` |
| `magnetic_energy` | function | Extracts magnetic energy for a specified material | `float` |
| `num_connected_components` | function | Counts connected components of a specified material | `int` |
| `boundary_length` | function | Calculates the outer boundary length of a specified material | `float` |
| `material_area` | function | Calculates the total area of a specified material | `float` |
| `material_volume` | function | Calculates the total volume of a specified material | `float` |
| `magnet_cost` | function | Calculates a virtual permanent-magnet cost | `float` |

## Common specifications

### `working_dir`

All evaluation functions receive the pyemsol analysis-result working directory, `working_dir`, as an argument.

:::info
`working_dir` is passed automatically inside EMSOptimizer when shape optimization runs.
Therefore, it does not need to be listed in kwargs in `optimization_problem.yaml`; if listed, it is ignored.
:::

### Input files

Each function reads `kwargs` and mesh files stored in `working_dir` to calculate evaluation values.
See the EMSolution documentation for details about the output files.

### YAML configuration

Evaluation functions can be specified in the `objectives`, `ineq_constraints`, `eq_constraints`, and `other_metrics` lists in `optimization_problem.yaml`.
Function-specific arguments are specified in `kwargs`.

```yaml
objectives:
  - function_name: average_torque
    kwargs:
      torque_scale: 4.0
    normalization_const: 2.1
    coefficient: -1.0
```

For details about configuration items, see [Optimization-problem settings (optimization_problem.yaml)](./optimization_problem_config.md).

## API details

### `average_torque`

Function that obtains the rotor torque waveform (`forceMZ`) from the analysis result `output.json` and calculates its average. The input is read from `output.json`.

```python
average_torque(working_dir: str, torque_scale: float = 1.0) -> float
```

#### YAML example

```yaml
function_name: average_torque
kwargs:
  torque_scale: 4.0
```

#### Arguments

| Name | Type | Default | YAML | Description |
|---|---|---:|:---:|---|
| `working_dir` | `str` | None | No | Working directory passed automatically by EMSOptimizer |
| `torque_scale` | `float` | `1.0` | Yes | Scale factor applied to torque |

#### Return value

| Type | Description |
|---|---|
| `float` | Mean of the scaled torque waveform |

#### Notes

Because partial models are often used for synchronous-motor performance analysis, multiplying torque by `torque_scale` converts it to the full-model equivalent.

### `torque_density`

Function that calculates torque density (average torque ÷ total area of the specified material).
Returns `0` when the area is extremely small.

```python
torque_density(working_dir: str, physical_tag: int = 20) -> float
```

#### YAML example

```yaml
function_name: torque_density
kwargs:
  physical_tag: 20
```

#### Arguments

| Name | Type | Default | YAML | Description |
|---|---|---:|:---:|---|
| `working_dir` | `str` | None | No | Working directory passed automatically by EMSOptimizer |
| `physical_tag` | `int` | `20` | Yes | Gmsh physical tag ID of the target material |

#### Return value

| Type | Description |
|---|---|
| `float` | Torque density (average torque / material area) |

### `torque_ripple`

Function that calculates torque ripple (maximum value − minimum value) from the rotor torque waveform.

```python
torque_ripple(working_dir: str, torque_scale: float = 1.0) -> float
```

#### YAML example

```yaml
function_name: torque_ripple
kwargs:
  torque_scale: 4.0
```

#### Arguments

| Name | Type | Default | YAML | Description |
|---|---|---:|:---:|---|
| `working_dir` | `str` | None | No | Working directory passed automatically by EMSOptimizer |
| `torque_scale` | `float` | `1.0` | Yes | Scale factor applied to torque |

#### Return value

| Type | Description |
|---|---|
| `float` | Torque ripple (maximum − minimum of the scaled torque waveform) |

### `torque_ripple_percentage`

Function that calculates the torque ripple percentage.

```python
torque_ripple_percentage(working_dir: str, torque_scale: float = 1.0) -> float
```

#### YAML example

```yaml
function_name: torque_ripple_percentage
kwargs:
  torque_scale: 4.0
```

#### Arguments

| Name | Type | Default | YAML | Description |
|---|---|---:|:---:|---|
| `working_dir` | `str` | None | No | Working directory passed automatically by EMSOptimizer |
| `torque_scale` | `float` | `1.0` | Yes | Scale factor applied to torque |

#### Return value

| Type | Description |
|---|---|
| `float` | Torque ripple percentage [%] |

#### Definition

```math
\frac{\text{最大値} - \text{最小値}}{\text{平均トルク}} \times 100
```

#### Notes

Returns a large penalty value when average torque is extremely small.

### `maximum_voltage`

Function that extracts the maximum value from the voltage waveform.

```python
maximum_voltage(working_dir: str) -> float
```

#### YAML example

```yaml
function_name: maximum_voltage
kwargs: {}
```

#### Arguments

| Name | Type | Default | YAML | Description |
|---|---|---:|:---:|---|
| `working_dir` | `str` | None | No | Working directory passed automatically by EMSOptimizer |

#### Return value

| Type | Description |
|---|---|
| `float` | Maximum voltage [V] |

### `magnetic_energy`

Function that extracts the magnetic energy of a specified material.

```python
magnetic_energy(working_dir: str, physical_tag: int) -> float
```

#### YAML example

```yaml
function_name: magnetic_energy
kwargs:
  physical_tag: 20
```

#### Arguments

| Name | Type | Default | YAML | Description |
|---|---|---:|:---:|---|
| `working_dir` | `str` | None | No | Working directory passed automatically by EMSOptimizer |
| `physical_tag` | `int` | None | Yes | Physical tag ID of the target material |

#### Return value

| Type | Description |
|---|---|
| `float` | Magnetic energy [J] |

### `num_connected_components`

Function that counts connected components among elements (triangle / quad) with the specified physical tag (material ID), using shared edges.
Elements are considered part of the same component if they share at least one edge.

```python
num_connected_components(working_dir: str, physical_tag: int = 20) -> int
```

#### YAML example

```yaml
function_name: num_connected_components
kwargs:
  physical_tag: 20
```

#### Arguments

| Name | Type | Default | YAML | Description |
|---|---|---:|:---:|---|
| `working_dir` | `str` | None | No | Working directory passed automatically by EMSOptimizer |
| `physical_tag` | `int` | `20` | Yes | Physical tag ID of the target material |

#### Return value

| Type | Description |
|---|---|
| `int` | Number of connected components. `0` means that the mesh or target elements do not exist |

#### Notes

This evaluation function is mainly used in topology optimization to prevent the specified material from separating into multiple regions.
See the [Showcase](../../showcase/Dmodel/advanced.md) for a practical example.

The default value `20` refers to the rotor core in the existing projects.
See the [Showcase](../../showcase/Dmodel/basic.md) for details.

### `boundary_length`

Function that calculates the outer boundary length of elements with the specified physical tag.

```python
boundary_length(working_dir: str, physical_tag: int = 20) -> float
```

#### YAML example

```yaml
function_name: boundary_length
kwargs:
  physical_tag: 20
```

#### Arguments

| Name | Type | Default | YAML | Description |
|---|---|---:|:---:|---|
| `working_dir` | `str` | None | No | Working directory passed automatically by EMSOptimizer |
| `physical_tag` | `int` | `20` | Yes | Physical tag ID of the target material |

#### Return value

| Type | Description |
|---|---|
| `float` | Outer boundary length |

### `material_area`

Function that calculates the total area occupied by cells (material) with the specified physical tag.

```python
material_area(working_dir: str, physical_tag: int = 20) -> float
```

#### YAML example

```yaml
function_name: material_area
kwargs:
  physical_tag: 20
```

#### Arguments

| Name | Type | Default | YAML | Description |
|---|---|---:|:---:|---|
| `working_dir` | `str` | None | No | Working directory passed automatically by EMSOptimizer |
| `physical_tag` | `int` | `20` | Yes | Physical tag ID of the target material |

#### Return value

| Type | Description |
|---|---|
| `float` | Total area of the specified material [m^2] |

### `material_volume`

Function that calculates the total volume occupied by cells (material) with the specified physical tag.

```python
material_volume(working_dir: str, physical_tag: int = 20) -> float
```

#### YAML example

```yaml
function_name: material_volume
kwargs:
  physical_tag: 20
```

#### Arguments

| Name | Type | Default | YAML | Description |
|---|---|---:|:---:|---|
| `working_dir` | `str` | None | No | Working directory passed automatically by EMSOptimizer |
| `physical_tag` | `int` | `20` | Yes | Physical tag ID of the target material |

#### Return value

| Type | Description |
|---|---|
| `float` | Total volume of the specified material [m^3] |

### `magnet_cost`

Function that calculates a virtual cost for the permanent magnet represented by the specified physical tag.
The formula is `係数 x 総面積`. It is useful when integrating with eMotorSolution.

```python
magnet_cost(
    working_dir: str,
    physical_tag: int = 50000,
    ferrite_coef: float = 0.2,
) -> float
```

#### YAML example

```yaml
function_name: magnet_cost
kwargs:
  physical_tag: 50000
  ferrite_coef: 0.2
```

#### Arguments

| Name | Type | Default | YAML | Description |
|---|---|---:|:---:|---|
| `working_dir` | `str` | None | No | Working directory passed automatically by EMSOptimizer |
| `physical_tag` | `int` | `50000` | Yes | Physical tag ID of the target material |
| `ferrite_coef` | `float` | `0.2` | Yes | Coefficient applied to ferrite magnets |

#### Return value

| Type | Description |
|---|---|
| `float` | Virtual cost [m^2] |

#### Notes

This function expects either `NdFeB` or `FerriteMagnet` as a keyword for the permanent-magnet material.
If the permanent-magnet material in the target `working_dir` is `FerriteMagnet`, `ferrite_coef` is used as the coefficient; otherwise, the coefficient is `1.0`.
