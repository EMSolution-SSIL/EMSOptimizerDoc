---
sidebar_position: 1
---

# `MagneticShield_3D`最適化
ここでは，`MagneticShield_3D`プロジェクトの内容について紹介します。

## モデル説明
MagneticShield3Dは3次元の磁気シールド構造を模擬したモデルです（元モデル：参考文献\[34\]）。  
保護対象領域`3: "Target"`に磁場が侵入しないよう，磁性体材料を表す`2: "design"`（線形・比透磁率200）によってその領域を囲う構造となっています。  
本プロジェクトでは，この磁性体材料の構造をNGnet on/off法によって最適化します。

![MagneticShield3D example](/img/MagneticShield3D_ex.png)

## machine.yaml（`MagneticShield3D`プロジェクト）
まず、機器情報を設定する`machine.yaml`の内容を確認します。
### 基本設定
今回，解析の次元は3次元であり，最適化ターゲットは`pre_geom.msh`です（モータとは異なりスライド運動部を含まないため，これが唯一の入力メッシュ）。また，座標系は直交座標系（xyz）で定義されています。
```yaml
# analysis dimension
analysis_dimension: 3D

# design target: "pre_geom" or "rotor"
design_target: pre_geom

# coordinate system: 'Cartesian' or 'Polar'
coordinate: Cartesian
```

解析領域内に線対称・回転対称な領域は含みません。
```yaml
# whether design region includes symmetric region
has_sym_region: False
```

### 材料設定
今回、設計対象は磁気シールドとなる磁性体材料（材料番号2）とし、
- オン材料→磁性体材料（材料番号2）
- オフ材料→空気穴（材料番号600000）
と設定しました。
```yaml
# on/off material information
target_ids_and_onoff:
  2:
    - 2
    - 600000
```

材料番号と材料名の割り当てです。このうち，`6`-`9`番はpyemsol側で電流ソースを定義するために，コイルの各面に割り当てられた番号です。  
また，4番は後述するImplicit Domain Meshing実行のために，`2: Design`と`4: Air`（雰囲気）との間に設けられた空気薄層です。
```yaml
physical_id_to_name:
  1: Coil
  2: Design
  3: Target
  4: Air
  5: layer
  6: Coil_top
  7: Coil_outer
  8: Coil_bottom
  9: Coil_inner
  600000: Hole
```

### Implicit Domain Meshing オプション
Implicit Domain Meshingはデフォルトで有効としています。
```yaml
use_implicit_domain_meshing: True
```

設計対象（`20: rotor`）以外は領域分割を行いません。
```yaml
# material boundaries of no_split_ids will be preserved after remeshing
no_split_ids:
  - 1
  - 3
  - 4
  - 5
  - 6
  - 7
  - 8
  - 9
```

また、コイル周りおよび雰囲気はリメッシュしたくないため、`no_remesh_ids`に設定します。  
```yaml
# mesh of no_remesh_ids will be preserved after remeshing
no_remesh_ids:
  - 1
  - 4
  - 6
  - 7
  - 8
  - 9
```
:::tip[3D最適化におけるリメッシュ]
今回の設定では`2: Design`がリメッシュ対象となっており，この領域は`3: Target`および`4: Air`と接触しています。  
このうち，`4: Air`は`1: Coil`の定義の関係上，リメッシュしないように設定しています。  
このとき，`2: Design`のリメッシュ結果と`4: Air`の固定メッシュとの接合を取るため，間にリメッシュを許容する空気薄層（`5: layer`）を設けています。
:::

メッシュの質にかかわる箇所は適当な値に設定します。
```yaml
# approximate design region size
design_region_size: 1.0

# hausd option ratio to design region size
# stands for maximum Hausdorff distance (approximation error) for level set boundaries
hausd_ratio: 0.001

# hmin option (minimum size of mesh) ratio to design region size
hmin_ratio: 0.01
```

最後に、評価スキップ基準値は0.001とします。
```yaml
# if mesh quality (>= 0, <= 1) is less than bad_mesh_threshold after remeshing, the individual will be skipped
bad_mesh_threshold: 0.001
```

## optimization.yaml（`MagneticShield3D`プロジェクト）
次に、最適化を設定する`optimization.yaml`の内容を確認します。  
今回は単目的形状最適化のため，`optimizer`に`cmaes`を指定しています。  
また，`level_set_function`は`ngnet`とし，設計領域を含む`[[0, 0.140], [0, 0.140], [0, 0.140]]`の範囲にガウス基底関数を配置する設定です。
```yaml
# optimization dependencies
evaluator:
  name: pyemsol_shape_evaluator
optimizer:
  name: cmaes
  kwargs:
    seed: 42
level_set_function:
  name: ngnet
  kwargs:
    sigma: 0.04
    design_region: [[0, 0.140], [0, 0.140], [0, 0.140]]
    dimension: 3D
    coordinate: Cartesian
```

今回は100イテレーションの最適化とします。  
並列処理はデフォルトで有効としています。
```yaml
num_iteration: 100
enable_parallelization: True
num_processes: Null  # if Null, automatically set from cpu counts
```
（出力周りの設定は省略します）

## optimization_problem.yaml（`MagneticShield3D`プロジェクト）
```yaml
case_names:
  - static

objectives:
  - function_name: magnetic_energy
    kwargs:
      physical_tag: 3
    normalization_const: 1.0e-14
    coefficient: 0.5
  - function_name: material_volume
    kwargs:
      physical_tag: 2
    normalization_const: 0.002744
    coefficient: 0.5

ineq_constraints: []

eq_constraints: []

other_metrics:
  - function_name: magnetic_energy
    kwargs:
      physical_tag: 3
  - function_name: material_volume
    kwargs:
      physical_tag: 2
```
最適化問題は`magnetic_energy`（保護対象領域`3`の磁気エネルギー）の最小化，および`material_volume`（磁性体材料の使用量）の最小化です。

## 最適化の実施例
最適化の経過を以下に示します。おおむね2層の磁性体構造が得られました。  
磁性体は軸対称ではなく三次元的な構造を有しており，磁性体材料の使用量を最小化する方向に最適化が進んでいることが分かります。
![磁気シールド最適化経過](/img/magshield3d_best_individuals.gif)

最適構造における磁束密度分布を以下に示します（pyemsiによって可視化）。磁束のほとんどは外側の層を通過しており，対象領域が保護されている様子が分かります。  
![磁気シールド磁束密度分布](/img/magshield3d_countor.png)