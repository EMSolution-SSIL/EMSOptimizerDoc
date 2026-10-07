---
sidebar_position: 7
---

# 評価用関数 API

## 概要

このページでは、形状最適化において `optimization_problem.yaml` に設定できる評価用関数群を紹介します。
これらの関数は、pyemsol解析結果の作業ディレクトリを参照し、目的関数、制約条件、その他メトリクスとして利用する値を計算します。

## import

評価用関数は、`optimization_problem.yaml` の `function_name` に関数名を指定して利用します。

```yaml
function_name: average_torque
kwargs:
  torque_scale: 4.0
```

## クイックリファレンス

| API | 種別 | 主な用途 | 戻り値 |
|---|---|---|---|
| `average_torque` | function | 平均トルクを計算する | `float` |
| `torque_density` | function | トルク密度を計算する | `float` |
| `torque_ripple` | function | トルクリップルを計算する | `float` |
| `torque_ripple_percentage` | function | トルクリップル率を計算する | `float` |
| `maximum_voltage` | function | 最大電圧値を抽出する | `float` |
| `magnetic_energy` | function | 指定材料の磁気エネルギーを抽出する | `float` |
| `num_connected_components` | function | 指定材料の連結成分数を数える | `int` |
| `boundary_length` | function | 指定材料の外周境界長さを計算する | `float` |
| `material_area` | function | 指定材料の総面積を計算する | `float` |
| `material_volume` | function | 指定材料の総体積を計算する | `float` |
| `magnet_cost` | function | 永久磁石の仮想コストを計算する | `float` |

## 共通仕様

### `working_dir`

すべての評価用関数は、pyemsol解析結果の作業ディレクトリ `working_dir` を引数として受け取ります。

:::info
`working_dir` は形状最適化実行時にEMSOptimizer内部で自動的に渡されます。
そのため、`optimization_problem.yaml` の `kwargs` には記載不要です。記載した場合も無視されます。
:::

### 入力ファイル

各関数内では、`working_dir` 内に保存された `output.json` やメッシュファイルを読み込んで評価値を計算します。
出力ファイルの詳細についてはEMSolutionのドキュメントを参照してください。

### YAML設定

評価用関数は、`optimization_problem.yaml` の `objectives`、`ineq_constraints`、`eq_constraints`、`other_metrics` の各リスト内で指定できます。
関数固有の引数は `kwargs` に指定します。

```yaml
objectives:
  - function_name: average_torque
    kwargs:
      torque_scale: 4.0
    normalization_const: 2.1
    coefficient: -1.0
```

設定項目の詳細は、[最適化問題の設定（optimization_problem.yaml）](./optimization_problem_config.md)をご覧ください。

## API詳細

### `average_torque`

解析結果 `output.json` からロータのトルク波形（`forceMZ`）を取得し、平均値を計算する関数です。

```python
average_torque(working_dir: str, torque_scale: float = 1.0) -> float
```

#### YAML設定例

```yaml
function_name: average_torque
kwargs:
  torque_scale: 4.0
```

#### 引数

| 名前 | 型 | デフォルト | YAML指定 | 説明 |
|---|---|---:|:---:|---|
| `working_dir` | `str` | なし | No | EMSOptimizerが自動で渡す作業ディレクトリ |
| `torque_scale` | `float` | `1.0` | Yes | トルク値に掛けるスケール係数 |

#### 戻り値

| 型 | 説明 |
|---|---|
| `float` | スケーリング後のトルク波形の平均値 |

#### 補足

同期モータの性能解析では部分モデルを使うことが多いため、トルクを `torque_scale` 倍することで全体モデル相当の値に換算します。

### `torque_density`

トルク密度（平均トルク値 ÷ 指定材料の総面積）を計算する関数です。
面積が極端に小さい場合は `0` を返します。

```python
torque_density(working_dir: str, physical_tag: int = 20) -> float
```

#### YAML設定例

```yaml
function_name: torque_density
kwargs:
  physical_tag: 20
```

#### 引数

| 名前 | 型 | デフォルト | YAML指定 | 説明 |
|---|---|---:|:---:|---|
| `working_dir` | `str` | なし | No | EMSOptimizerが自動で渡す作業ディレクトリ |
| `physical_tag` | `int` | `20` | Yes | 対象材料のgmsh物理タグID |

#### 戻り値

| 型 | 説明 |
|---|---|
| `float` | トルク密度（平均トルク / 材料面積） |

### `torque_ripple`

ロータのトルク波形から、トルクリップル（最大値 - 最小値）を計算する関数です。

```python
torque_ripple(working_dir: str, torque_scale: float = 1.0) -> float
```

#### YAML設定例

```yaml
function_name: torque_ripple
kwargs:
  torque_scale: 4.0
```

#### 引数

| 名前 | 型 | デフォルト | YAML指定 | 説明 |
|---|---|---:|:---:|---|
| `working_dir` | `str` | なし | No | EMSOptimizerが自動で渡す作業ディレクトリ |
| `torque_scale` | `float` | `1.0` | Yes | トルク値に掛けるスケール係数 |

#### 戻り値

| 型 | 説明 |
|---|---|
| `float` | トルクリップル（スケーリング後のトルク波形の最大値 - 最小値） |

### `torque_ripple_percentage`

トルク波形のリップル率をパーセントで計算する関数です。

```python
torque_ripple_percentage(working_dir: str, torque_scale: float = 1.0) -> float
```

#### YAML設定例

```yaml
function_name: torque_ripple_percentage
kwargs:
  torque_scale: 4.0
```

#### 引数

| 名前 | 型 | デフォルト | YAML指定 | 説明 |
|---|---|---:|:---:|---|
| `working_dir` | `str` | なし | No | EMSOptimizerが自動で渡す作業ディレクトリ |
| `torque_scale` | `float` | `1.0` | Yes | トルク値に掛けるスケール係数 |

#### 戻り値

| 型 | 説明 |
|---|---|
| `float` | トルクリップル率 [%] |

#### 定義

```math
\frac{\text{最大値} - \text{最小値}}{\text{平均トルク}} \times 100
```

#### 補足

平均トルクがごく小さい場合は、大きなペナルティ値を返します。

### `maximum_voltage`

電圧波形から最大値を抽出する関数です。

```python
maximum_voltage(working_dir: str) -> float
```

#### YAML設定例

```yaml
function_name: maximum_voltage
kwargs: {}
```

#### 引数

| 名前 | 型 | デフォルト | YAML指定 | 説明 |
|---|---|---:|:---:|---|
| `working_dir` | `str` | なし | No | EMSOptimizerが自動で渡す作業ディレクトリ |

#### 戻り値

| 型 | 説明 |
|---|---|
| `float` | 最大電圧値 [V] |

### `magnetic_energy`

指定した材料の磁気エネルギーを抽出する関数です。

```python
magnetic_energy(working_dir: str, physical_tag: int) -> float
```

#### YAML設定例

```yaml
function_name: magnetic_energy
kwargs:
  physical_tag: 20
```

#### 引数

| 名前 | 型 | デフォルト | YAML指定 | 説明 |
|---|---|---:|:---:|---|
| `working_dir` | `str` | なし | No | EMSOptimizerが自動で渡す作業ディレクトリ |
| `physical_tag` | `int` | なし | Yes | 対象材料の物理タグID |

#### 戻り値

| 型 | 説明 |
|---|---|
| `float` | 磁気エネルギー値 [J] |

### `num_connected_components`

指定された物理タグ（材料番号）を持つ要素（triangle / quad）について、辺共有による連結成分数をカウントする関数です。
要素間で一つでも辺を共有していれば同じ連結成分と見なします。

```python
num_connected_components(working_dir: str, physical_tag: int = 20) -> int
```

#### YAML設定例

```yaml
function_name: num_connected_components
kwargs:
  physical_tag: 20
```

#### 引数

| 名前 | 型 | デフォルト | YAML指定 | 説明 |
|---|---|---:|:---:|---|
| `working_dir` | `str` | なし | No | EMSOptimizerが自動で渡す作業ディレクトリ |
| `physical_tag` | `int` | `20` | Yes | 対象材料の物理タグID |

#### 戻り値

| 型 | 説明 |
|---|---|
| `int` | 連結成分の数。`0` の場合はメッシュもしくは対象要素が存在しないことを表す |

#### 補足

この評価関数は主にトポロジー最適化において、指定した材料が複数の領域に分離することを防ぐ目的で使用します。
実際の使用例は[Showcase](../../showcase/Dmodel/advanced.md)をご覧ください。

なお、デフォルト値の `20` は既存プロジェクト群においてロータコアを指すIDです。
詳細は[Showcase](../../showcase/Dmodel/basic.md)をご覧ください。

### `boundary_length`

指定された物理タグを持つ要素群に対して、外周境界長さを計算する関数です。

```python
boundary_length(working_dir: str, physical_tag: int = 20) -> float
```

#### YAML設定例

```yaml
function_name: boundary_length
kwargs:
  physical_tag: 20
```

#### 引数

| 名前 | 型 | デフォルト | YAML指定 | 説明 |
|---|---|---:|:---:|---|
| `working_dir` | `str` | なし | No | EMSOptimizerが自動で渡す作業ディレクトリ |
| `physical_tag` | `int` | `20` | Yes | 対象材料の物理タグID |

#### 戻り値

| 型 | 説明 |
|---|---|
| `float` | 外周境界長さ |

### `material_area`

指定された物理タグを持つセル（材料）が占める面積の総和を計算する関数です。

```python
material_area(working_dir: str, physical_tag: int = 20) -> float
```

#### YAML設定例

```yaml
function_name: material_area
kwargs:
  physical_tag: 20
```

#### 引数

| 名前 | 型 | デフォルト | YAML指定 | 説明 |
|---|---|---:|:---:|---|
| `working_dir` | `str` | なし | No | EMSOptimizerが自動で渡す作業ディレクトリ |
| `physical_tag` | `int` | `20` | Yes | 対象材料の物理タグID |

#### 戻り値

| 型 | 説明 |
|---|---|
| `float` | 指定材料の総面積 [m^2] |

### `material_volume`

指定された物理タグを持つセル（材料）が占める体積の総和を計算する関数です。

```python
material_volume(working_dir: str, physical_tag: int = 20) -> float
```

#### YAML設定例

```yaml
function_name: material_volume
kwargs:
  physical_tag: 20
```

#### 引数

| 名前 | 型 | デフォルト | YAML指定 | 説明 |
|---|---|---:|:---:|---|
| `working_dir` | `str` | なし | No | EMSOptimizerが自動で渡す作業ディレクトリ |
| `physical_tag` | `int` | `20` | Yes | 対象材料の物理タグID |

#### 戻り値

| 型 | 説明 |
|---|---|
| `float` | 指定材料の総体積 [m^3] |

### `magnet_cost`

指定された物理タグが表す永久磁石の仮想コストを計算する関数です。
計算式は `係数 x 総面積` です。eMotorSolution連携時に有効です。

```python
magnet_cost(
    working_dir: str,
    physical_tag: int = 50000,
    ferrite_coef: float = 0.2,
) -> float
```

#### YAML設定例

```yaml
function_name: magnet_cost
kwargs:
  physical_tag: 50000
  ferrite_coef: 0.2
```

#### 引数

| 名前 | 型 | デフォルト | YAML指定 | 説明 |
|---|---|---:|:---:|---|
| `working_dir` | `str` | なし | No | EMSOptimizerが自動で渡す作業ディレクトリ |
| `physical_tag` | `int` | `50000` | Yes | 対象材料の物理タグID |
| `ferrite_coef` | `float` | `0.2` | Yes | フェライト磁石にかかる係数 |

#### 戻り値

| 型 | 説明 |
|---|---|
| `float` | 仮想コスト [m^2] |

#### 補足

この関数内では、永久磁石材料として `NdFeB` または `FerriteMagnet` のいずれかのキーワードを期待します。
対象の `working_dir` において永久磁石材料が `FerriteMagnet` の場合は `ferrite_coef` を係数として使用し、それ以外の場合は `1.0` を係数として使用します。
