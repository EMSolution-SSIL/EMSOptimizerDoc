---
sidebar_position: 3
---

# Machine Configuration (`machine.yaml`)
This page explains the available machine configuration options.

## Format
Notation: `{設定項目名}: {型名} = デフォルト値`  
Options without a default value are required.
```yaml
# Basic Settings
analysis_dimension: str ("2D" | "3D") = "2D"
design_target: str ("pre_geom" | "rotor") = "rotor"
coordinate: str ("Cartesian" | "Polar") = "Cartesian"
has_sym_region: bool = False
sym_deg: float = 0
num_rotate: int = 0

# Material Settings
target_ids_and_onoff: dict[int, list[int]] = []
physical_id_to_name: dict[int, str] = {}
mirror_id_map: dict[int, int] = {}
increment_info: dict[int, tuple[int, int, int, str]] = {}

# Output Settings
material_color_map: dict[int, str] = {}
image_export:
  resolution: float = 480
  view_mode: str ("cartesian_aspect_fit" | "cartesian_full" | "polar_full" | "polar_symmetry") = "cartesian_aspect_fit"
  image_target_region: tuple[tuple[float, float], tuple[float, float]] | null = null

# Implicit Domain Meshing Options
use_implicit_domain_meshing: bool = False
no_split_ids: list[int] = []
no_remesh_ids: list[int] = []
design_region_size: float = 0.0010
hausd_ratio: float = 0.0001
hmin_ratio: float  0.01
hgrad: float = 1.2
bad_mesh_threshold: float = 0.10

# neighbor judgement
neighbor_radius_ratio: float = 1.0
min_neighbors: float = 4

# levelset reinitialization
calc_levelset_init: bool = False
levelset_reinit_interval: int | null = null
levelset_reinit_weight: float = 0.2

# eMotorSolution Link Settings
ems_project_filepath: str | null = null
```

## Details
:::warning
The settings in `machine.yaml` must be consistent with the electrical-equipment base-model mesh and the pyemsol input JSON files in the analysis-case folders.  
See the [Showcase](../../showcase/intro.md) for practical configuration examples.
:::
### Basic settings
- `analysis_dimension: str ("2D" | "3D")` ... Dimension of the electrical-equipment base-model mesh.
:::warning
As of v0.7.0, 3D calculations have the following limitations.  
- When `level_set_function` is used, `use_implicit_domain_meshing` must be `True`.  
- `pyemsol_density` cannot be set for `level_set_function`.
:::
- `design_target: str ("pre_geom" | "rotor")` ... Target of shape optimization.
:::info
The EMSolution electromagnetic-field simulator (pyemsol) uses two separate input mesh files, so this configuration specifies which one to optimize.   
- `pre_geom`: Model mesh without motion
- `rotor`: Mesh for the sliding-motion component (provided only when the model has sliding motion)  

For example, in a synchronous motor, the stator corresponds to `pre_geom` and the rotor to `rotor`.
:::
- `coordinate: str ("Cartesian" | "Polar")` ... Coordinate system used for the calculation.
:::info
Specify `Cartesian` for shape optimization using a Cartesian `coordinate` system.  
For example, specify `Polar` for synchronous-motor shape optimization when the model is defined using polar coordinates (radius and angle).
:::
- `has_sym_region: bool` ... Whether a mirror-symmetric region exists. The design-region shape is mirrored into the mirror-symmetric region.
:::info
This option is currently effective only when `coordinate` is `Polar`.  
For example, rotor shapes in synchronous-motor models are often half-pole symmetric, so this option is set to `True`.
:::
- `sym_deg: float` ... Angle of the mirror-symmetry axis \[deg\] when `has_sym_region` is `True`.
- `num_rotate: int` ... Number of rotationally symmetric regions when `has_sym_region` is `True` and rotational symmetry exists. Set to `0` when no rotationally symmetric region exists.
:::info
Rotationally symmetric regions are assumed to exist every `2 × sym_deg`, and the combined design and mirror-symmetric region is copied by rotation.  
For example, set this option when the synchronous-motor model being analyzed contains multiple poles.
:::

### Material settings
- `target_ids_and_onoff: dict[int, list[int]]` ... Material IDs targeted for topology optimization. In regions assigned a `target_id`, the material ID at each position is set to `id for level 1`, `id for level 2`, and so on based on the level set function value.
  #### Format
  ```yaml
  target_ids_and_onoff:
    {target_id}:
      - {id for level 1}
      - {id for level 2}
      - ...
    ...
  ```
:::tip[Topology optimization behavior]
Topology optimization behavior depends on `target_ids_and_onoff`. Specifically, **the evenly divided values in the range -1 to 1 become the boundaries at which material IDs switch.**  
Let the level set function value be $y$. For example, when `id for level 1` and `id for level 2` are configured, the material ID at each position is set as follows.
```math
y > 0 \rightarrow \text{id for level 1} \\
y \leq 0  \rightarrow \text{id for level 2}
```
This is extended as follows when `id for level 3` is also configured.
```math
y > 0.33  \rightarrow \text{id for level 1}  \\
-0.33 < y \leq 0.33 \rightarrow \text{id for level 2} \\
y \leq -0.33 \rightarrow \text{id for level 3} \\
```
  
Multiple `target_id` values can also be configured. In that case, material settings are applied independently for each `target_id`.
:::

- `physical_id_to_name: dict[int, str]` ... Mapping from material IDs to material names.
  #### Format
  ```yaml
  physical_id_to_name:
    {id}: {name}
    ...
  ```

- `mirror_id_map: dict[int, int]` ... When `has_sym_region` is `True`, mapping from source material IDs to material IDs in the mirrored copy. For example, if material ID `50000` becomes `50001` in the copy across the mirror-symmetry axis, set `50000: 50001`.
  #### Format
  ```yaml
  mirror_id_map:
    {original_id}: {mirrored_id}
    ...
  ```
:::info
Include materials whose IDs do not change during mirroring as well (for example, `20: 20`).  
Because changes in material IDs during rotational copying are configured by `increment_info` below, `mirror_id_map` should specify **material-ID changes during mirroring within each rotationally symmetric region**.
:::

- `increment_info: dict[int, tuple[int, int, int, str]]` ... Information about materials in rotational copies when `num_rotate > 0`.
  #### Format
  ```yaml
  increment_info:
    {original_id}:  # 回転コピー時に変化させる材料ID
      - {first rotated material id}  # 変化先IDの先頭番号
      - {incremental of id per rotate}  # 回転ごとのID増分
      - {num of rotate (should be equal to num_rotate)}  # 回転数（`num_rotate`と同じ値に設定する）
      - {prefix name}  # 材料名の接頭辞
    ...
  ```
:::tip[Behavior of `increment_info`]
For example, when `num_rotate: 6`, suppose `increment_info` is configured as follows.   
```yaml
increment_info:
  50000:
    - 51000
    - 1000
    - 6
    - "magnet_0_0"
```
In this case, material IDs are created for each rotational region as follows.
```yaml
51000: "magnet_0_0_1"
52000: "magnet_0_0_2"
53000: "magnet_0_0_3"
54000: "magnet_0_0_4"
55000: "magnet_0_0_5"
56000: "magnet_0_0_6"
```
:::

### Image output settings
:::info
These settings are used when output is enabled in `optimization.yaml`.
:::
- `image_export` ... General image-output settings.
- `resolution: float` ... Image resolution.
- `view_mode: str ("cartesian_aspect_fit" | "cartesian_full" | "polar_full" | "polar_symmetry")` ... Image-rendering mode.
    - `cartesian_aspect_fit` ... Render the Cartesian coordinate system as a square image while preserving the mesh aspect ratio.
    - `cartesian_full` ... Render the Cartesian coordinate system as a square image, expanding it to fill the image in both directions.
    - `polar_full` ... Render the polar coordinate system as a square image, expanding it to fill the image in both directions.
    - `polar_symmetry` ... Render the polar coordinate system as a square image, expanding it to fill the image in both directions. The $\theta$ range is automatically set from 0° to `sym_deg`°.
  - `image_target_region: tuple[tuple[float, float], tuple[float, float]] | null` ... Region to render. For `Cartesian`, specify a rectangular region $[[x_1, x_2], [y_1, y_2]]$; for `Polar`, specify a sector region $[[r_1, r_2], [\theta_1, \theta_2]]$.
:::info
When `view_mode` is `polar_symmetry` and `image_target_region` is set, the `image_target_region` setting takes precedence (automatic setting of the $\theta$ range is ignored).
:::
- `material_color_map: dict[int, str]` ... Mapping from material IDs to image colors. A default color is applied to IDs that are not specified.
  #### Format
  ```yaml
  material_color_map:
    {id}: {color_name or code}
    ...
  ```
:::info
The value field accepts color names supported by the pyvista library and color codes (# followed by six hexadecimal digits). Enclose color-code values in double quotes.
Example:
50000: red
600000: "#0000ff"
:::


### Implicit Domain Meshing options
:::info
See the [Implicit Domain Meshing](../advanced/implicit_domain_meshing.md) page for details about the method.
:::
- `use_implicit_domain_meshing: bool` ... Enable or disable Implicit Domain Meshing.
:::warning[Limitations]
When enabling Implicit Domain Meshing, check the following.
- Mesh files stored in the project must consist only of triangular elements. Implicit Domain Meshing cannot be run with quadrilateral or other non-triangular meshes.
- Only `id for level 1` and `id for level 2` may be configured in `target_ids_and_onoff`. Three or more material levels cannot be used with Implicit Domain Meshing.
:::
- `no_split_ids: list[int]` ... List of material IDs excluded from region deformation when Implicit Domain Meshing is applied (remeshing within the region is still allowed).
- `no_remesh_ids: list[int]` ... List of material IDs excluded from remeshing when Implicit Domain Meshing is applied.
:::info
Normally, `no_split_ids` lists material IDs that are included in the model but not specified in `target_ids_and_onoff` (that is, IDs outside the design target).  
**Among these, specify materials whose mesh must be preserved, such as a motor's sliding-mesh region, in `no_remesh_ids`.**
:::
- `design_region_size: float` ... Approximate size of the design region \[m\]. Together with `hausd_ratio` and `hmin_ratio`, this affects material-boundary accuracy during remeshing.
- `hausd_ratio: float` ... Tolerance ratio for material boundaries during remeshing. Specifically, `hausd_raito` × `design_region_size` is used as the tolerance during remeshing.
- `hmin_ratio: float` ... Minimum element-edge-length ratio during remeshing. Specifically, `hmin_ratio` × `design_region_size` is used as the minimum edge length during remeshing.
- `hgrad: float` ... Element-edge-length gradient during remeshing. Specify a value greater than 1. Larger values produce greater changes in mesh size away from the boundary; smaller values produce a more uniform mesh.
- `bad_mesh_threshold: float` ... If the mesh-quality metric (0 to 1, where 1 is best) falls below this value during remeshing, evaluation of the shape is skipped. A large penalty is assigned to skipped shapes, so the optimization algorithm eliminates them.
:::tip[Recommended settings]
- `hausd_ratio` ... Approximately 0.001. Smaller values more faithfully reproduce the material boundary of the level set function, but increase the number of mesh elements and analysis time (the number of elements is limited by `hmin_ratio`).
- `hmin_ratio` ... Approximately 0.05 to 0.01. Smaller values make the entire mesh finer.
- `hgrad` ... Approximately 1.05 to 1.3. Smaller values produce a more uniform mesh.
- `bad_mesh_threshold:` ... Approximately 0.05 to 0.10. Smaller values allow lower-quality meshes, increasing the shape-analysis rate but reducing result reliability.
:::

### Neighbor judgment
Neighbor judgment is performed when `ls_function` is configured, and the result is output as `design_neighbors.csv` in the analysis folder.
- `neighbor_radius_ratio: float` ... Normalized radius used to identify neighboring elements. An element is considered a neighbor when it is within (the distance to the nearest element center) × neighbor_radius_ratio.
- `min_neighbors: int` ... Minimum number of neighboring elements. If fewer elements than this value are identified, the nearest non-neighboring elements are added in order.

### Level set reinitialization
Level set reinitialization is available when `pyemsol_density` is configured for `ls_function`.
- `calc_levelset_init: bool` ... Read the mesh before optimization and calculate the signed distance from the boundary for each element. The result is output as `design_ls_parameters.csv` in the analysis folder.
- `levelset_reinit_interval: int | null` ... Level set reinitialization interval. When `null`, no reinitialization is performed during optimization.
- `levelset_reinit_weight: float` ... Weight $w$ used during level set reinitialization. If the design variables (level set values) before and after reinitialization are $\boldsymbol{\phi}^\text{old}$ and $\boldsymbol{\phi}^\text{new}$, respectively, reinitialization is applied as follows.
  ```math
  \boldsymbol{\phi} = (1 - w) \boldsymbol{\phi}^\text{old} + w \boldsymbol{\phi}^\text{new}
  ```
  Larger values apply reinitialization more strongly, but may disrupt information in the existing design variables.

### eMotorSolution Link Settings
`ems_project_filepath: str` ... File path to the eMotorSolution project file (.json) to integrate with EMSOptimizer.
:::info
See [Advanced Topics > Integration with eMotorSolution](../advanced/link_ems.md) for details about eMotorSolution integration.
:::
