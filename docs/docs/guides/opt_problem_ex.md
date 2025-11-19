---
sidebar_position: 9
---
# 評価用関数実装例
ここでは、形状最適化において`optimization_problem.yaml`に設定できる評価関数の実装例を紹介します。  

## 共通事項
すべての関数はpyemsol解析結果の作業ディレクトリ (`working_dir`) を入力として受け取ります。ただし、**`working_dir`は形状最適化実行時にEMSOptimizer内部で自動的に渡されるため、`optimization_problem.yaml`内`kwargs`への記載は不要です**（記載しても無視されます）。以下の説明では`working_dir`は省略しています。  
`working_dir`の中に保存された`output.json`やメッシュファイルを読み込んで評価値を計算します。

## `average_torque`
```python
average_torque(working_dir: str, torque_scale: float = 1.0) -> float
```
解析結果 `output.json` からロータのトルク波形（`forceMZ`）を取得し、平均値を計算して返します。
### 引数
- `torque_scale` (`float`, デフォルト `1.0`): トルク値に掛けるスケール係数。
:::info
同期モータの性能解析には部分モデルを使うことが多いため、トルクを`torque_scale`倍することで全体モデル相当の値に換算します。
:::
### 戻り値
- `float`: スケーリング後のトルク波形の平均値。

## `torque_density`
```python
torque_density(working_dir: str, physical_tag: int = 20) -> float
```
トルク密度（平均トルク値 ÷ 指定材料の総面積）を計算します。面積が極端に小さい場合は0を返します。
### 引数
- `physical_tag` (`int`, デフォルト `20`): 対象材料の gmsh 物理タグ ID。
### 戻り値
- `float`: トルク密度（平均トルク / 材料面積）。

## `torque_ripple`
```python
torque_ripple(working_dir: str, torque_scale: float = 1.0) -> float
```
ロータのトルク波形から、トルクリップル（最大値 - 最小値）を計算します。
### 引数
- `torque_scale` (`float`, デフォルト `1.0`): トルク値に掛けるスケール係数。
### 戻り値
- `float`: トルクリップル（スケーリング後のトルク波形の最大値 - 最小値）。

## `torque_ripple_percentage`
```python
torque_ripple_percentage(working_dir: str, torque_scale: float = 1.0) -> float
```
トルク波形のリップル率をパーセントで計算します。定義：$\frac{\text{最大値} - \text{最小値}}{\text{平均トルク}} \times 100$  
平均トルクがごく小さい場合は、大きなペナルティ値を返します。
### 引数
- `torque_scale` (`float`, デフォルト `1.0`): トルク値に掛けるスケール係数。
### 戻り値
- `float`: トルクリップル率 [%]。

## `num_connected_components`
```python
num_connected_components(working_dir: str, physical_tag: int = 20) -> int
```
指定された物理タグ（材料番号）を持つ要素（triangle / quad）について、**辺共有による連結成分数**をカウントします。  
要素間で一つでも辺を共有していれば同じ連結成分と見なします。
:::info
この評価関数は主にトポロジー最適化において、指定した材料が複数の領域に分離することを防ぐ目的で使用します。  
実際の使用例は[Showcase](../../showcase/Dmodel/advanced.md)をご覧ください。
:::
### 引数
- `physical_tag` (`int`, デフォルト `20`): 対象材料の物理タグID。
:::info
なお、デフォルト値の`20`は既存プロジェクト群においてロータコアを指すIDです。  
詳細は[Showcase](../../showcase/Dmodel/basic.md)をご覧ください。
:::
### 戻り値
- `int`: 連結成分の数（0 の場合はメッシュもしくは対象要素が存在しない）。

## `boundary_length`
```python
boundary_length(working_dir: str, physical_tag: int = 20) -> float
```
指定された物理タグを持つ要素群に対して、**外周境界長さ**を計算します。  
### 引数
- `physical_tag` (`int`, デフォルト `20`): 対象材料の物理タグID。
### 戻り値
- `float`: 外周境界長さ。

## `material_area`
```python
material_area(working_dir: str, physical_tag: int = 20) -> float
```
指定された物理タグを持つセル（材料）が占める面積の総和を計算します。
### 引数
- `physical_tag` (`int`, デフォルト `20`): 対象材料の物理タグID。
### 戻り値
- `float`: 指定材料の総面積。
