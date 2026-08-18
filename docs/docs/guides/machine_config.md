---
sidebar_position: 3
---

# 機器設定（machine.yaml）
ここでは、`machine.yaml`の内容を説明します。

## Format
凡例：`{設定項目名}: {型名} = デフォルト値`  
デフォルト値の無いものは設定必須項目。
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
material_color_map: dict[int, str] = {}
mirror_id_map: dict[int, int] = {}
increment_info: dict[int, tuple[int, int, int, str]] = {}

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
`machine.yaml`の各種設定は使用する電気機器ベースモデルメッシュおよび各解析ケースフォルダ内のpyemsol入力jsonファイルと整合するように設定する必要があります。  
実際の設定例は[Showcase](../../showcase/intro.md)をご覧ください。
:::
### 基本設定
- `analysis_dimension: str ("2D" | "3D")` ... 取り扱う電気機器ベースモデルメッシュの次元。
:::warning
現在（v0.7.0）時点では，3Dの計算に以下の制約があります。  
- `level_set_function`を使用する場合，`use_implicit_domain_meshing`は`True`でなければならない  
- `level_set_function`に`pyemsol_density`は設定できない
:::
- `design_target: str ("pre_geom" | "rotor")` ... 形状最適化のターゲット。
:::info
電磁界シミュレータEMSolution(pyemsol)では入力メッシュファイルが以下の2つに分かれるため、このコンフィグによってどちらを形状最適化するか指定します。   
- `pre_geom`: 運動を伴わないモデルメッシュ
- `rotor`: スライド運動部モデルメッシュ（モデルがスライド運動を伴う場合のみ入力）  

例えば、同期モータ等ではステータが`pre_geom`、ロータが`rotor`に当たります。
:::
- `coordinate: str ("Cartesian" | "Polar")` ... 計算に用いる座標系。
:::info
直交座標系を用いる形状最適化では`Cartesian`を指定します。  
一方、例えば同期モータの形状最適化の場合は極座標系（半径と角度）を用いてモデル定義を行うため、`Polar`を指定します。
:::
- `has_sym_region: bool` ... 鏡面対称領域の有無。鏡面対称領域には設計領域の形状が鏡面コピーされます。
:::info
現在、このオプションは`coordinate`が`Polar`の場合のみ有効です。  
例えば、同期モータモデルのロータ形状は半極対称であることが多いため、このオプションを`True`に設定します。
:::
- `sym_deg: float` ... `has_sym_region`が`True`のとき、その鏡面対称軸角度 \[deg\]。
- `num_rotate: int` ... `has_sym_region`が`True`かつ、回転対称領域がある場合、その領域数。回転対称領域が無い場合は`0`に設定します。
:::info
回転対称領域は`2 × sym_deg`ごとに存在すると仮定し、設計領域と鏡面対称領域を合わせた領域を回転コピーします。  
例えば、解析対象となる同期モータモデルが複数極を含む場合にこのオプションを設定します。
:::

### 材料設定
- `target_ids_and_onoff: dict[int, list[int]]` ... トポロジー最適化において設計対象とする材料ID。`target_id`が割り当てられた領域について、各位置の材料IDをレベルセット関数の値に基づいて`id for level 1`, `id for level 2`, ...に設定します。
  #### Format
  ```yaml
  target_ids_and_onoff:
    {target_id}:
      - {id for level 1}
      - {id for level 2}
      - ...
    ...
  ```
:::tip[トポロジー最適化の挙動]
トポロジー最適化の挙動は`target_ids_and_onoff`の設定によって変化します。すなわち、**-1~1の範囲を等分割した値が材料IDの切り替わる境界値となります。**  
レベルセット関数の値を$y$とします。例えば、`id for level 1`および`id for level 2`が設定されているとき、各位置の材料IDは
```math
y > 0 \rightarrow \text{id for level 1} \\
y \leq 0  \rightarrow \text{id for level 2}
```
と設定されます。  
これに加えて`id for level 3`が設定されているときは、
```math
y > 0.33  \rightarrow \text{id for level 1}  \\
-0.33 < y \leq 0.33 \rightarrow \text{id for level 2} \\
y \leq -0.33 \rightarrow \text{id for level 3} \\
```
と設定されます。  

また、`target_id`は複数設定することが可能です。この場合、各`target_id`ごとに独立した材料設定が行われます。
:::

- `physical_id_to_name: dict[int, str]` ... 材料ID→材料名称マップ。
  #### Format
  ```yaml
  physical_id_to_name:
    {id}: {name}
    ...
  ```

- `material_color_map: dict[int, str]` ... 材料ID→画像色マップ。`optimization.yaml`にて画像出力を有効にしたときに参照される。未指定のIDに対してはデフォルト色が適用される。
  #### Format
  ```yaml
  material_color_map:
    {id}: {color_name or code}
    ...
  ```
:::info
value値にはライブラリ（pyvista）にて利用可能な色名、およびカラーコード(#+6桁の16進数)が使用できます。
:::

- `mirror_id_map: dict[int, int]` ... `has_sym_region`が`True`のとき、鏡映コピー元→鏡映コピー先材料IDマップ。例えば、材料ID`50000`の材料が鏡面対称軸を跨いだ鏡映コピー先では`50001`になる場合、`50000: 50001`と設定する。
  #### Format
  ```yaml
  mirror_id_map:
    {original_id}: {mirrored_id}
    ...
  ```
:::info
鏡映コピー時に材料IDが変化しない場合もこのコンフィグに記載してください（例：`20: 20`）。  
また、回転コピー時の材料IDの変化は下記の`increment_info`によって設定するため、`mirror_id_map`には**各回転対称領域内における鏡映コピー時の材料IDの変化**を設定します。
:::

- `increment_info: dict[int, tuple[int, int, int, str]]` ... `num_rotate > 0`のとき、回転コピー先材料情報。
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
:::tip[`increment_info`の挙動]
例えば、`num_rotate: 6`のとき、以下のように`increment_info`を設定したとします。   
```yaml
increment_info:
  50000:
    - 51000
    - 1000
    - 6
    - "magnet_0_0"
```
この場合、材料IDは回転領域ごとに以下のように作成されます。
```yaml
51000: "magnet_0_0_1"
52000: "magnet_0_0_2"
53000: "magnet_0_0_3"
54000: "magnet_0_0_4"
55000: "magnet_0_0_5"
56000: "magnet_0_0_6"
```
:::

### Implicit Domain Meshing オプション
:::info
Implicit Domain Meshingの手法については[Implicit Domain Meshing](../advanced/implicit_domain_meshing.md)ページを参照してください。
:::
- `use_implicit_domain_meshing: bool` ... Implicit Domain Meshingの有効化／無効化。
:::warning[制限事項]
Implicit Domain Meshingの有効化時は以下の点を確認してください。
- プロジェクトに格納するメッシュファイルは三角形メッシュのみで構成されていること。四角形メッシュ等のImplicit Domain Meshingは実行不可です。
- `target_ids_and_onoff`に`id for level 1`, `id for level 2`のみ設定されていること。Implicit Domain Meshing時は3材料以上のレベルセットは不可です。
:::
- `no_split_ids: list[int]` ... Implicit Domain Meshing適用時、領域変形の対象外とする材料IDのリスト（ただし、領域内のリメッシュは許容）。
- `no_remesh_ids: list[int]` ... Implicit Domain Meshing適用時、リメッシュの対象外とする材料IDのリスト。
:::info
`no_split_ids`には通常、「モデルには含まれるが`target_ids_and_onoff`に指定しなかった材料ID（＝設計対象外の材料ID）」を列挙します。  
**その中でも特にメッシュを維持したいもの（例：モータにおけるスライドメッシュ領域）については`no_remesh_ids`に指定します。**
:::
- `design_region_size: float` ... 設計領域の（大まかな）大きさ \[m\]。以下の`hausd_ratio`および`hmin_ratio`と併せて、リメッシュ時の材料境界の精度に影響します。
- `hausd_ratio: float` ... リメッシュ時の材料境界の許容誤差率。具体的には、`hausd_raito`×`design_region_size`の値がリメッシュ時に許容誤差として参照されます。
- `hmin_ratio: float` ... リメッシュ時の要素エッジ長の最小値率。具体的には、`hmin_ratio`×`design_region_size`の値がリメッシュ時に最小エッジ長として参照されます。
- `hgrad: float` ... リメッシュ時の要素エッジ長勾配。1より大きい値を指定する。この値が大きいほど境界からのメッシュサイズの変化が大きくなり，小さいほど一様なメッシュに近づく。
- `bad_mesh_threshold: float` ... リメッシュ時にメッシュの質を表す指標（0~1, 1が最良）がこの値を下回った場合、その形状は評価をスキップする。評価がスキップされた形状には大きなペナルティが与えられるため、最適化アルゴリズムにより淘汰されます。
:::tip[推奨設定値]
- `hausd_ratio` ... 0.001程度。値が小さいほどレベルセット関数に対する材料境界の忠実度が高くなる代わりにメッシュ要素数が増加し、解析に要する時間が増加します（ただし、メッシュ要素数は`hmin_ratio`によって制限されます）。
- `hmin_ratio` ... 0.05~0.01程度。値が小さいほどメッシュ全体が細かくなります。
- `hgrad` ... 1.05~1.3程度。値が小さいほど一様なメッシュに近づきます。
- `bad_mesh_threshold:` ... 0.05~0.10程度。値が小さいほど質の悪いメッシュも許容されるようになり、形状の解析率が上がる代わりに結果の信頼度が低下します。
:::

### 近傍判定
近傍判定は，`ls_function`を設定した場合に行われ，解析フォルダ内に`design_neighbors.csv`という名前で出力されます。
- `neighbor_radius_ratio: float` ... ある要素の近傍と判定される規格化半径。具体的には，（その要素の最近傍要素中心との距離）× neighbor_radius_ratio の距離内にある要素が近傍と判定される。
- `min_neighbors: int` ... 最小近傍要素数。近傍判定の結果要素数がこの値に満たない場合，非近傍要素のうち最も近い要素が順に近傍要素に加えられる。

### レベルセット再初期化
レベルセット再初期化は，`ls_function`に`pyemsol_density`を設定した場合に有効なオプションです。
- `calc_levelset_init: bool` ... 最適化実行前にメッシュを読み取り，各要素における境界からの符号付距離関数値を計算する。計算結果は解析フォルダ内に`design_ls_parameters.csv`という名前で出力される。
- `levelset_reinit_interval: int | null` ... レベルセット再初期化頻度。`null`のとき，最適化中に再初期化は行わない。
- `levelset_reinit_weight: float` ... レベルセット再初期化時の重み係数$w$。再初期化前の設計変数の値（レベルセット関数値）を$\boldsymbol{\phi}^\text{old}$，再初期化後の値を$\boldsymbol{\phi}^\text{new}$とし，以下の式によって再初期化を反映します。
  ```math
  \boldsymbol{\phi} = (1 - w) \boldsymbol{\phi}^\text{old} + w \boldsymbol{\phi}^\text{new}
  ```
  この値が大きいほど再初期化が確実に反映されますが，既存の設計変数の情報が崩れる可能性があります。

### eMotorSolution Link Settings
`ems_project_filepath: str` ... EMSOptimizerと連携したいeMotorSolutionプロジェクトファイル（.json）へのファイルパス。
:::info
eMotorSlution連携については[発展的なトピック > eMotorSolutionとの連携](../advanced/link_ems.md)をご覧ください。
:::
