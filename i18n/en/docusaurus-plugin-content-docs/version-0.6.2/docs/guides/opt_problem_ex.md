---
sidebar_position: 9
---
# Evaluation Function Examples
This page introduces examples of evaluation functions that can be configured in `optimization_problem.yaml` for shape optimization.  

## Common behavior
Every function receives the working directory containing the pyemsol analysis results (`working_dir`) as an argument. However, **EMSOptimizer passes `working_dir` automatically during shape optimization, so it does not need to be included in the argument list (`kwargs` in `optimization_problem.yaml`)**; it is ignored if specified. The descriptions below omit `working_dir`.  
Each function calculates its metric by reading `output.json` or mesh files stored in `working_dir`. See the EMSolution documentation for details about the output files.

## `average_torque`
```python
average_torque(working_dir: str, torque_scale: float = 1.0) -> float
```
Obtains the rotor torque waveform (`forceMZ`) from the analysis result `output.json` and returns its average.
### Arguments
- `torque_scale` (`float`, default: `1.0`): Scaling coefficient applied to torque values.
:::info
Because partial models are commonly used to analyze synchronous-motor performance, the torque is multiplied by `torque_scale` to convert it to the equivalent full-model value.
:::
### Return value
- `float`: Average of the scaled torque waveform.

## `torque_density`
```python
torque_density(working_dir: str, physical_tag: int = 20) -> float
```
Calculates torque density (average torque divided by the total area of the specified material). Returns 0 when the area is extremely small.
### Arguments
- `physical_tag` (`int`, default: `20`): gmsh physical-tag ID of the target material.
### Return value
- `float`: Torque density (average torque / material area).

## `torque_ripple`
```python
torque_ripple(working_dir: str, torque_scale: float = 1.0) -> float
```
Calculates torque ripple (maximum minus minimum) from the rotor torque waveform.
### Arguments
- `torque_scale` (`float`, default: `1.0`): Scaling coefficient applied to torque values.
### Return value
- `float`: Torque ripple (maximum minus minimum of the scaled torque waveform).

## `torque_ripple_percentage`
```python
torque_ripple_percentage(working_dir: str, torque_scale: float = 1.0) -> float
```
Calculates the torque-waveform ripple percentage. It is defined as $\frac{\text{maximum} - \text{minimum}}{\text{average torque}} \times 100$.  
Returns a large penalty value when average torque is extremely small.
### Arguments
- `torque_scale` (`float`, default: `1.0`): Scaling coefficient applied to torque values.
### Return value
- `float`: Torque ripple percentage [%].

## `num_connected_components`
```python
num_connected_components(working_dir: str, physical_tag: int = 20) -> int
```
Counts the **edge-connected components** of elements (triangles/quads) with the specified physical tag (material ID).  
Elements sharing at least one edge are considered part of the same connected component.
:::info
This evaluation function is used primarily in topology optimization to prevent the specified material from separating into multiple regions.  
See the [Showcase](../../showcase/Dmodel/advanced.md) for a practical example.
:::
### Arguments
- `physical_tag` (`int`, default: `20`): Physical-tag ID of the target material.
:::info
The default value `20` is the rotor-core ID in the existing projects.  
See the [Showcase](../../showcase/Dmodel/basic.md) for details.
:::
### Return value
- `int`: Number of connected components (0 if the mesh or target elements do not exist).

## `boundary_length`
```python
boundary_length(working_dir: str, physical_tag: int = 20) -> float
```
Calculates the **outer-boundary length** of elements with the specified physical tag.  
### Arguments
- `physical_tag` (`int`, default: `20`): Physical-tag ID of the target material.
### Return value
- `float`: Outer-boundary length.

## `material_area`
```python
material_area(working_dir: str, physical_tag: int = 20) -> float
```
Calculates the total area occupied by cells (material) with the specified physical tag.
### Arguments
- `physical_tag` (`int`, default: `20`): Physical-tag ID of the target material.
### Return value
- `float`: Total area of the specified material.
