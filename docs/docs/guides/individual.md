---
sidebar_position: 4
---

# individual関連オブジェクト API
ここでは、EMSOptimizer全体で使用される個体（individual）を管理するためのクラス群を紹介します。  
`emsopt_engine.individual`からimport可能です。  
これらのクラス群は特に`optimizer`, `evaluator`間における個体情報のやり取りに利用されます。

## `OptimizationProblemMetrics`
```python
@dataclass
class OptimizationProblemMetrics:
    objectives: list[float] = field(default_factory=list)
    ineq_constraints: list[float] = field(default_factory=list)
    eq_constraints: list[float] = field(default_factory=list)
    other_metrics: list[float] = field(default_factory=list)
    _fitness: float | None = None
```
最適化問題における評価値と制約に関する情報を保持するデータクラスです。

### 属性
#### `objectives: list[float]`
- 目的関数値（評価値）のリスト

#### `ineq_constraints: list[float]`
- 不等式制約の値のリスト

#### `eq_constraints: list[float]`
- 等式制約の値のリスト

#### `other_metrics: list[float]`
- その他のメトリクス（可視化や解析用）

#### `_fitness: float | None`
- 内部的に保持している総合適合度（スカラー）
- 通常は外部から直接参照せず、`fitness` プロパティ経由で利用します

### プロパティ
#### `fitness: float`
- 個体のスカラー評価値（適合度）を返します。
- `_fitness` が `None` の場合は、`objectives` の総和をデフォルトの適合度として返します。
    - 単目的最適化における単純加重和として利用可能
- 外部で任意のスカラー化を行った場合、`metrics.fitness = スカラー値` のように代入すると`_fitness`に値がセットされ、その値が`fitness`として返されるようになります。

#### `constraint_violation: float`
- 全制約（不等式＋等式）の違反量の合計を返します。

#### `ineq_constraint_violation: float`
- 不等式制約の違反量の合計を返します。
- 各制約値 `v` に対して `max(0, v)` をとり、正の部分のみを違反量として加算します。
  - `v ≤ 0` なら違反なし（0）
  - `v > 0` ならその分だけ違反量としてカウント

#### `eq_constraint_violation: float`
- 等式制約の違反量の合計を返します。
- 各制約値の絶対値 `abs(v)` を違反量として加算します。

## `Individual`
```python
@dataclass
class Individual:
    solution: list[float]
    outcome_filepath: str | None = None
    metrics: OptimizationProblemMetrics = field(default_factory=OptimizationProblemMetrics)
    label_values: dict[str, float] = field(default_factory=dict)
    record_info: EvaluationRecord = field(default_factory=EvaluationRecord)
```
個体（1つの解候補）を表すデータクラスです。
解ベクトルに加えて、その評価結果・制約違反量・可視化用メトリクスなどを`metrics`として保持します。  
また，構造最適化時の評価関数を`label_values`に，評価ステータスを`record_info`として保持します。

### 属性
#### `solution: list[float]`
- 設計変数ベクトル（解ベクトル）$\boldsymbol{x}=\{x_1, x_2, ...\}$

#### `outcome_filepath: str | None`
- この個体に対応する形状ファイルパス
- 形状最適化時、EMSOptimizer内部で自動的に設定

#### `metrics: OptimizationProblemMetrics`
- 評価値・制約値・その他メトリクスを格納する `OptimizationProblemMetrics`インスタンス
- 評価器（Evaluator）がこのフィールドに値をセットする想定
- 形状最適化時は`optimization_problem.yaml`に設定した関数値がこのフィールドに格納される

#### `label_values: dict[str, float]`
- `metrics`に含まれる評価関数と，その評価結果を格納する辞書型変数
    - key (str): 評価関数名（`function_name`）とケース名（`case_name`）によって構成された名称（例：`label__average_torque__case_transient`）
    - value (float): `optimization_proble.yaml`に設定した関数値の生値（[基本の使い方 > 最適化問題の設定](../getting-started/opt_problem.md)ページの$A$値）
:::warning
`label_values`は関数名とケース名の2つによって関数を識別します。したがって，同じ関数名・同じケース名に異なる`kwargs`を与えた関数値同士は区別されません（どちらか一方のみが`label_values`に保存されます）。  
異なる`kwargs`を与えた関数値も個別に保存したい場合，たとえば処理内容は同じで`kwargs`を固定した関数を別の関数として作成し，`optimization_problem.yaml`にて指定する必要があります。
:::

#### `record_info: EvaluationRecord`
- 以下に示す評価結果レコードインスタンス。評価成功／失敗を`status`に，失敗時の理由（メッシュ生成エラー，解析エラーなど）を`failure_reason`に保存します。
```python
@dataclass
class EvaluationRecord:
    status: Literal["success", "failure"] = "success"
    failure_reason: str | None = None
```

## `Population`
```python
class Population(MutableMapping[int, Individual]):
    ...
```
最適化アルゴリズムで扱う個体群（Population）を管理するクラスです。
`MutableMapping[int, Individual]` を継承しており、基本的に**辞書 (`dict`) とほぼ同じインターフェース**で個体を操作できます。  
`optimizer`, `evaluator`間ではPopulationのインスタンスが行き来することによって解候補群とそれらに対する評価値がやりとりされます。

### コンストラクタ（__init__）
- 引数：`init_data: dict[int, Individual] | None`
    - 初期状態の個体群辞書（キー：個体インデックス、値：`Individual` インスタンス）
    - `None` の場合は空の個体群が生成されます。

### メソッド
#### `add_individual(individual: Individual) -> int`
- 個体を個体群に追加し、未使用の最小の整数インデックスを自動で割り当てます。
- 戻り値：割り当てられたインデックス（`int`）

#### `merge(other: Population) -> None`
- 自身の個体群と `other` 個体群を結合します。
- マージ後は元のインデックスは失われ、`0, 1, 2, ...` の連番になります。

#### `overwrite(other: Population) -> None`
- `other` の中で、自身と同じインデックスを持つ個体が存在する場合、そのインデックスに対応する個体を丸ごと置き換えます。
    - python辞書型の`update`とは異なり、`other`に新規のインデックスがあっても無視されます。
- 典型的な用途
    - 既存個体群に対して、一部インデックスの個体だけを更新する
    - 評価済み個体のみを差し替える
    など

#### `reindex() -> None`
- 現在の個体群の順序を維持したまま、インデックスを `0, 1, 2, ...` と連番に振り直します。
- 削除やマージの後でインデックスが飛び飛びになった場合にリセットしたいときに便利です。

#### `split(indices: list[int]) -> tuple[Population, Population]`
- 個体群を2つに分割します。
    - 第1個体群：`indices` に含まれるインデックスの個体
    - 第2個体群：残りの個体
- 戻り値：（第1個体群、第2個体群）のタプル

#### `extract(indices: list[int]) -> Population`
- 指定したインデックス `indices` を持つ個体だけからなる部分個体群を抽出して返します。
- 例
    - エリート個体だけを取り出して別途保存・可視化したい場合
    - 特定のインデックス群に対してのみ再評価を行いたい場合

#### `to_design_matrix() -> list[list[float]]`
- 全個体の `solution` をまとめて 2 次元リストとして返します。
- 形式は「個体数 × 次元数」の設計行列（デザインマトリクス）に相当します。
- 例：機械学習の入力行列や統計解析の入力として利用可能。

## 使用例
```python
# 個体の作成
ind = Individual(solution=[0.1, 0.5, 0.9])

# 評価値・制約をセット
ind.metrics.objectives = [1.23, 0.45]         # 2目的
ind.metrics.ineq_constraints = [0.0, 0.2]     # 2つ目だけ違反
ind.metrics.eq_constraints = [0.01]           # 0に近ければ近いほど良い

print(ind.metrics.fitness)                    # _fitness 未設定なので objectives の和 = 1.68
print(ind.metrics.constraint_violation)       # ineq + eq

# 個体群の作成
pop = Population()
idx = pop.add_individual(ind)             # 自動で index=0 が割り当てられる

# 設計行列の取得
X = pop.to_design_matrix()                # [[0.1, 0.5, 0.9]]
```
