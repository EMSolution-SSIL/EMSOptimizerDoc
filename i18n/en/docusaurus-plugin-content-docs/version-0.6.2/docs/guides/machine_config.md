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

# Implicit Domain Meshing Options
use_implicit_domain_meshing: bool = False
no_split_ids: list[int] = []
no_remesh_ids: list[int] = []
design_region_size: float = 0.0010
hausd_ratio: float = 0.0001
hmin_ratio: float  0.01
bad_mesh_threshold: float = 0.10

# eMotorSolution Link Settings
ems_project_filepath: str | null = null
```

## Details
:::warning
The settings in `machine.yaml` must be consistent with the electrical-equipment base-model mesh and the pyemsol input JSON files in the analysis-case folders.  
See the [Showcase](../../showcase/intro.md) for practical configuration examples.
:::
### Basic settings
- `design_target: str ("pre_geom" | "rotor")` ... Target of shape optimization.
:::info
The EMSolution electromagnetic-field simulator (pyemsol) uses two separate input mesh files, so this configuration specifies which one to optimize.   
- `pre_geom`: Model mesh without motion
- `rotor`: Mesh for the sliding-motion component (provided only when the model has sliding motion)  

For example, in a synchronous motor, the stator corresponds to `pre_geom` and the rotor to `rotor`.
:::
- `coordinate: str ("Cartesian" | "Polar")` ... Coordinate system used for the calculation.
:::info
Specify `Cartesian` for shape optimization using a Cartesian coordinate system.  
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
:::tip Topology optimization behavior
Topology optimization behavior depends on `target_ids_and_onoff`. Specifically, **the evenly divided values in the range -1 to 1 become the boundaries at which material IDs switch.**  
Let the level set function value be $y$. For example, when `id for level 1` and `id for level 2` are configured, the material ID at each position is set as follows.
```math
y > 0 \rightarrow \text{id for level 1} \\
y \leq 0  \rightarrow \text{id for level 2}
```
is assigned.  
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

- `mirror_id_map: dict[int, int]` ... Material-ID map from the source to the destination of a mirror copy when `has_sym_region` is `True`. For example, if material ID `50000` becomes `50001` in the mirrored region, specify `50000: 50001`.
  #### Format
  ```yaml
  mirror_id_map:
    {original_id}: {mirrored_id}
    ...
  ```
:::info
Include materials whose IDs do not change during mirror copying in this configuration as well (for example, `20: 20`).
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
:::tip Behavior of `increment_info`
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

### Implicit Domain Meshing options
:::info
See the [Implicit Domain Meshing](../advanced/implicit_domain_meshing.md) page for details about the method.
:::
- `use_implicit_domain_meshing: bool` ... Enable or disable Implicit Domain Meshing.
:::warning Limitations
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
- `bad_mesh_threshold: float` ... If the mesh-quality metric (0 to 1, where 1 is best) falls below this value during remeshing, evaluation of the shape is skipped. A large penalty is assigned to skipped shapes, so the optimization algorithm eliminates them.
:::tip Recommended settings
- `hausd_ratio` ... Approximately 0.001. Smaller values more faithfully reproduce the material boundary of the level set function, but increase the number of mesh elements and analysis time (the number of elements is limited by `hmin_ratio`).
- `hmin_ratio` ... Approximately 0.05 to 0.01. Smaller values make the entire mesh finer.
- `bad_mesh_threshold:` ... Approximately 0.05 to 0.10. Smaller values allow lower-quality meshes, increasing the shape-analysis rate but reducing result reliability.
:::

### eMotorSolution Link Settings
`ems_project_filepath: str` ... File path to the eMotorSolution project file (.json) to integrate with EMSOptimizer.
:::info
See [Advanced Topics > Integration with eMotorSolution](../advanced/link_ems.md) for details about eMotorSolution integration.
:::
