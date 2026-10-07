---
sidebar_position: 6
---

# individual関連オブジェクト API

## 概要

このページでは、EMSOptimizer全体で使用される個体（individual）を管理するためのクラス群を紹介します。
これらのクラス群は、特に `optimizer` と `evaluator` の間で個体情報をやり取りするために利用されます。

## import

```python
from emsopt_engine.individual import (
    Individual,
    OptimizationProblemMetrics,
    Population,
)
```

## クイックリファレンス

| API | 種別 | 主な用途 | 主な戻り値 |
|---|---|---|---|
| `OptimizationProblemMetrics` | dataclass | 目的関数値、制約値、その他メトリクスを保持する | `OptimizationProblemMetrics` |
| `Individual` | dataclass | 1つの解候補と評価結果を保持する | `Individual` |
| `Population` | class | 複数の `Individual` を辞書に近いインターフェースで管理する | `Population` |

## 共通仕様

### 個体と評価値の関係

`Individual` は1つの解候補を表し、設計変数ベクトルを `solution` に保持します。
評価器（Evaluator）は、目的関数値、制約値、その他メトリクスを `Individual.metrics` に書き込みます。

形状最適化時は、`optimization_problem.yaml` に設定した関数値が `metrics` や `label_values` に格納されます。

### 制約違反量の扱い

不等式制約では、各制約値 `v` に対して `max(0, v)` を違反量として扱います。
等式制約では、各制約値の絶対値 `abs(v)` を違反量として扱います。

## API詳細

### `OptimizationProblemMetrics`

最適化問題における評価値と制約に関する情報を保持するデータクラスです。

```python
@dataclass
class OptimizationProblemMetrics:
    objectives: list[float] = field(default_factory=list)
    ineq_constraints: list[float] = field(default_factory=list)
    eq_constraints: list[float] = field(default_factory=list)
    other_metrics: list[float] = field(default_factory=list)
    _fitness: float | None = None
```

#### フィールド

| 名前 | 型 | デフォルト | 説明 |
|---|---|---:|---|
| `objectives` | `list[float]` | `[]` | 目的関数値（評価値）のリスト |
| `ineq_constraints` | `list[float]` | `[]` | 不等式制約の値のリスト |
| `eq_constraints` | `list[float]` | `[]` | 等式制約の値のリスト |
| `other_metrics` | `list[float]` | `[]` | 可視化や解析用のその他メトリクス |
| `_fitness` | `float \| None` | `None` | 内部的に保持している総合適合度（スカラー） |

#### プロパティ

| 名前 | 型 | 説明 |
|---|---|---|
| `fitness` | `float` | 個体のスカラー評価値（適合度）を返す |
| `constraint_violation` | `float` | 全制約（不等式 + 等式）の違反量の合計を返す |
| `ineq_constraint_violation` | `float` | 不等式制約の違反量の合計を返す |
| `eq_constraint_violation` | `float` | 等式制約の違反量の合計を返す |

#### 補足

`_fitness` が `None` の場合、`fitness` は `objectives` の総和をデフォルトの適合度として返します。
外部で任意のスカラー化を行った場合は、`metrics.fitness = scalar_value` のように代入すると `_fitness` に値がセットされ、その値が `fitness` として返されます。

### `Individual`

1つの解候補を表すデータクラスです。
解ベクトルに加えて、評価結果、制約違反量、可視化用メトリクスなどを `metrics` として保持します。

```python
@dataclass
class Individual:
    solution: list[float]
    working_dir: str | None = None
    outcome_filepath: str | None = None
    metrics: OptimizationProblemMetrics = field(
        default_factory=OptimizationProblemMetrics
    )
    label_values: dict[str, float] = field(default_factory=dict)
    record_info: EvaluationRecord = field(default_factory=EvaluationRecord)
```

#### フィールド

| 名前 | 型 | デフォルト | 説明 |
|---|---|---:|---|
| `solution` | `list[float]` | なし | 設計変数ベクトル（解ベクトル）$\boldsymbol{x}=\{x_1, x_2, ...\}$ |
| `working_dir` | `str \| None` | `None` | その個体に割り当てられたpyemsol用の作業ディレクトリ |
| `outcome_filepath` | `str \| None` | `None` | この個体に対応する形状ファイルパス |
| `metrics` | `OptimizationProblemMetrics` | `OptimizationProblemMetrics()` | 評価値、制約値、その他メトリクスを格納する |
| `label_values` | `dict[str, float]` | `{}` | 形状最適化時の評価関数名と評価結果を格納する |
| `record_info` | `EvaluationRecord` | `EvaluationRecord()` | 評価成功／失敗のステータスと失敗理由を保持する |

#### 関連データ

`record_info` には、以下の評価結果レコードインスタンスが格納されます。

```python
@dataclass
class EvaluationRecord:
    status: Literal["success", "failure"] = "success"
    failure_reason: str | None = None
```

#### 補足

`label_values` のkeyは、評価関数名（`function_name`）とケース名（`case_name`）によって構成された名称です。
たとえば、`label__average_torque__case_transient` のような形式になります。

valueには、`optimization_problem.yaml` に設定した関数値の生値（[基本の使い方 > 最適化問題の設定](../getting-started/opt_problem.md)ページの$A$値）が格納されます。

:::warning
`label_values`は関数名とケース名の2つによって関数を識別します。
したがって、同じ関数名・同じケース名に異なる `kwargs` を与えた関数値同士は区別されません（どちらか一方のみが `label_values` に保存されます）。

異なる `kwargs` を与えた関数値も個別に保存したい場合、たとえば処理内容は同じで `kwargs` を固定した関数を別の関数として作成し、`optimization_problem.yaml` にて指定する必要があります。
:::

### `Population`

最適化アルゴリズムで扱う個体群（Population）を管理するクラスです。
`MutableMapping[int, Individual]` を継承しており、基本的に辞書（`dict`）とほぼ同じインターフェースで個体を操作できます。

```python
class Population(MutableMapping[int, Individual]): ...
```

`optimizer` と `evaluator` の間では、`Population` のインスタンスが行き来することで、解候補群とそれらに対する評価値がやり取りされます。

#### コンストラクタ

```python
Population(init_data: dict[int, Individual] | None = None)
```

| 名前 | 型 | デフォルト | 必須 | 説明 |
|---|---|---:|:---:|---|
| `init_data` | `dict[int, Individual] \| None` | `None` | No | 初期状態の個体群辞書。キーは個体インデックス、値は `Individual` インスタンス |

#### メソッド

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `add_individual(individual)` | `int` | 個体を追加し、未使用の最小整数インデックスを返す |
| `merge(other)` | `None` | 自身と `other` の個体群を結合する |
| `overwrite(other)` | `None` | 自身と同じインデックスを持つ個体のみ、`other` の個体で置き換える |
| `reindex()` | `None` | 現在の順序を維持したまま、インデックスを `0, 1, 2, ...` に振り直す |
| `split(indices)` | `tuple[Population, Population]` | 指定インデックス群と残りの個体群に分割する |
| `extract(indices)` | `Population` | 指定インデックスの個体だけを抽出する |
| `from_design_matrix(design_matrix)` | `Population` | 設計行列から個体群を生成する |
| `to_design_matrix()` | `list[list[float]]` | 全個体の `solution` を2次元リストとして返す |

#### `add_individual`

個体を個体群に追加し、未使用の最小の整数インデックスを自動で割り当てます。

```python
add_individual(individual: Individual) -> int
```

| 名前 | 型 | デフォルト | 必須 | 説明 |
|---|---|---:|:---:|---|
| `individual` | `Individual` | なし | Yes | 追加する個体 |

| 戻り値 | 説明 |
|---|---|
| `int` | 割り当てられたインデックス |

#### `merge`

自身の個体群と `other` 個体群を結合します。
マージ後は元のインデックスは失われ、`0, 1, 2, ...` の連番になります。

```python
merge(other: Population) -> None
```

| 名前 | 型 | デフォルト | 必須 | 説明 |
|---|---|---:|:---:|---|
| `other` | `Population` | なし | Yes | 結合する個体群 |

#### `overwrite`

`other` の中で、自身と同じインデックスを持つ個体が存在する場合、そのインデックスに対応する個体を丸ごと置き換えます。
Python辞書型の `update` とは異なり、`other` に新規のインデックスがあっても無視されます。

```python
overwrite(other: Population) -> None
```

| 名前 | 型 | デフォルト | 必須 | 説明 |
|---|---|---:|:---:|---|
| `other` | `Population` | なし | Yes | 置き換え元の個体群 |

#### `reindex`

現在の個体群の順序を維持したまま、インデックスを `0, 1, 2, ...` と連番に振り直します。
削除やマージの後でインデックスが飛び飛びになった場合に便利です。

```python
reindex() -> None
```

#### `split`

個体群を2つに分割します。
第1個体群には `indices` に含まれるインデックスの個体が入り、第2個体群には残りの個体が入ります。

```python
split(indices: list[int]) -> tuple[Population, Population]
```

| 名前 | 型 | デフォルト | 必須 | 説明 |
|---|---|---:|:---:|---|
| `indices` | `list[int]` | なし | Yes | 抽出側に含める個体インデックスのリスト |

| 戻り値 | 説明 |
|---|---|
| `tuple[Population, Population]` | 第1個体群と第2個体群のタプル |

#### `extract`

指定したインデックス `indices` を持つ個体だけからなる部分個体群を抽出して返します。

```python
extract(indices: list[int]) -> Population
```

| 名前 | 型 | デフォルト | 必須 | 説明 |
|---|---|---:|:---:|---|
| `indices` | `list[int]` | なし | Yes | 抽出する個体インデックスのリスト |

| 戻り値 | 説明 |
|---|---|
| `Population` | 指定インデックスの個体だけを含む個体群 |

#### `from_design_matrix`

設計行列から個体群を生成するクラスメソッドです。

```python
from_design_matrix(cls, design_matrix: list[list[float]]) -> Population
```

| 名前 | 型 | デフォルト | 必須 | 説明 |
|---|---|---:|:---:|---|
| `design_matrix` | `list[list[float]]` | なし | Yes | 個体数 x 次元数の設計行列 |

| 戻り値 | 説明 |
|---|---|
| `Population` | 設計行列から生成された個体群 |

#### `to_design_matrix`

全個体の `solution` をまとめて2次元リストとして返します。
形式は「個体数 x 次元数」の設計行列（デザインマトリクス）に相当します。

```python
to_design_matrix() -> list[list[float]]
```

| 戻り値 | 説明 |
|---|---|
| `list[list[float]]` | 全個体の `solution` をまとめた設計行列 |

## 使用例

### 個体と個体群を作成する

```python
from emsopt_engine.individual import Individual, Population

# 個体の作成
ind = Individual(solution=[0.1, 0.5, 0.9])

# 評価値・制約をセット
ind.metrics.objectives = [1.23, 0.45]
ind.metrics.ineq_constraints = [0.0, 0.2]
ind.metrics.eq_constraints = [0.01]

print(ind.metrics.fitness)
print(ind.metrics.constraint_violation)

# 個体群の作成
pop = Population()
idx = pop.add_individual(ind)

# 設計行列の取得
X = pop.to_design_matrix()
```
