---
sidebar_position: 7
---

# 評価用関数 API
ここでは、形状最適化において`optimization_problem.yaml`に設定できる評価用関数群を紹介します。  
これらの関数は、pyemsol解析結果の作業ディレクトリを参照し、目的関数・制約条件・その他メトリクスとして利用する値を計算します。

## 共通事項
すべての評価用関数は、pyemsol解析結果の作業ディレクトリ `working_dir` を引数として受け取ります。

:::info
`working_dir`は形状最適化実行時にEMSOptimizer内部で自動的に渡されます。  
そのため、`optimization_problem.yaml`の`kwargs`には記載不要です。記載した場合も無視されます。
:::

各関数内では、`working_dir`内に保存された`output.json`やメッシュファイルを読み込んで評価値を計算します。出力ファイルの詳細についてはEMSolutionのドキュメントを参照してください。

## `average_torque`
```python
average_torque(working_dir: str, torque_scale: float = 1.0) -> float
```
解析結果`output.json`からロータのトルク波形（`forceMZ`）を取得し、平均値を計算する関数です。

### 引数
#### `torque_scale: float`
- トルク値に掛けるスケール係数

:::info
同期モータの性能解析では部分モデルを使うことが多いため、トルクを`torque_scale`倍することで全体モデル相当の値に換算します。
:::

### 戻り値
#### `float`
- スケーリング後のトルク波形の平均値

## `torque_density`
```python
torque_density(working_dir: str, physical_tag: int = 20) -> float
```
トルク密度（平均トルク値 ÷ 指定材料の総面積）を計算する関数です。  
面積が極端に小さい場合は`0`を返します。

### 引数
#### `physical_tag: int`
- 対象材料のgmsh物理タグID

### 戻り値
#### `float`
- トルク密度（平均トルク / 材料面積）

## `torque_ripple`
```python
torque_ripple(working_dir: str, torque_scale: float = 1.0) -> float
```
ロータのトルク波形から、トルクリップル（最大値 - 最小値）を計算する関数です。

### 引数
#### `torque_scale: float`
- トルク値に掛けるスケール係数

### 戻り値
#### `float`
- トルクリップル（スケーリング後のトルク波形の最大値 - 最小値）

## `torque_ripple_percentage`
```python
torque_ripple_percentage(working_dir: str, torque_scale: float = 1.0) -> float
```
トルク波形のリップル率をパーセントで計算する関数です。  
定義は以下の通りです。

```math
\frac{\text{最大値} - \text{最小値}}{\text{平均トルク}} \times 100
```

平均トルクがごく小さい場合は、大きなペナルティ値を返します。

### 引数
#### `torque_scale: float`
- トルク値に掛けるスケール係数

### 戻り値
#### `float`
- トルクリップル率 [%]

## `maximum_voltage`
```python
maximum_voltage(working_dir: str) -> float
```
電圧波形から最大値を抽出する関数です。

### 引数
なし（`working_dir`のみ）

### 戻り値
#### `float`
- 最大電圧値 [V]

## `magnetic_energy`
```python
magnetic_energy(working_dir: str, physical_tag: int) -> float
```
指定した材料の磁気エネルギーを抽出する関数です。

### 引数
#### `physical_tag: int`
- 対象材料の物理タグID

### 戻り値
#### `float`
- 磁気エネルギー値 [J]

## `num_connected_components`
```python
num_connected_components(working_dir: str, physical_tag: int = 20) -> int
```
指定された物理タグ（材料番号）を持つ要素（triangle / quad）について、辺共有による連結成分数をカウントする関数です。  
要素間で一つでも辺を共有していれば同じ連結成分と見なします。

:::info
この評価関数は主にトポロジー最適化において、指定した材料が複数の領域に分離することを防ぐ目的で使用します。  
実際の使用例は[Showcase](../../showcase/Dmodel/advanced.md)をご覧ください。
:::

### 引数
#### `physical_tag: int`
- 対象材料の物理タグID

:::info
なお、デフォルト値の`20`は既存プロジェクト群においてロータコアを指すIDです。  
詳細は[Showcase](../../showcase/Dmodel/basic.md)をご覧ください。
:::

### 戻り値
#### `int`
- 連結成分の数
- `0`の場合はメッシュもしくは対象要素が存在しないことを表します

## `boundary_length`
```python
boundary_length(working_dir: str, physical_tag: int = 20) -> float
```
指定された物理タグを持つ要素群に対して、外周境界長さを計算する関数です。  

### 引数
#### `physical_tag: int`
- 対象材料の物理タグID

### 戻り値
#### `float`
- 外周境界長さ

## `material_area`
```python
material_area(working_dir: str, physical_tag: int = 20) -> float
```
指定された物理タグを持つセル（材料）が占める面積の総和を計算する関数です。

### 引数
#### `physical_tag: int`
- 対象材料の物理タグID

### 戻り値
#### `float`
- 指定材料の総面積 [m^2]

## `material_volume`
```python
material_volume(working_dir: str, physical_tag: int = 20) -> float
```
指定された物理タグを持つセル（材料）が占める体積の総和を計算する関数です。

### 引数
#### `physical_tag: int`
- 対象材料の物理タグID

### 戻り値
#### `float`
- 指定材料の総体積 [m^3]

## `magnet_cost`
```python
magnet_cost(working_dir: str,
            physical_tag: int = 50000,
            ferrite_coef: float = 0.2) -> float
```
指定された物理タグが表す永久磁石の仮想コストを計算する関数です。  
計算式は`係数 × 総面積`です。eMotorSolution連携時に有効です。

### 引数
#### `physical_tag: int`
- 対象材料の物理タグID

#### `ferrite_coef: float`
- フェライト磁石にかかる係数

:::info
この関数内では、永久磁石材料として`NdFeB`または`FerriteMagnet`のいずれかのキーワードを期待します。  
対象の`working_dir`において永久磁石材料が`FerriteMagnet`の場合は`ferrite_coef`を係数として使用し、それ以外の場合は`1.0`を係数として使用します。
:::

### 戻り値
#### `float`
- 仮想コスト [m^2]
