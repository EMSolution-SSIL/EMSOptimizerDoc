---
sidebar_position: 2
---

# ga
単目的最適化用の遺伝的アルゴリズムのpython実装クラスです。  
実数変数をベースとしつつ\[32\]，カテゴリ変数（順序情報無し整数変数）・整数変数を扱える構成になっています\[33\]。

## 概要
各世代の集団＋子個体から，高い評価値を持つ個体を次世代の集団として選択することで，集団の進化を促します。  
各変数は種類ごとに以下の通り処理します：  
- 実数変数：SBX + polynomial mutation \[6\]
- 整数変数：実数変数と同様。ただし，結果値を最も近い整数変数に丸める
- カテゴリ変数：一様交叉＋カテゴリ内のランダムな値への突然変異

また、制約違反した個体は以下のように評価します\[12\]。これにより、実行可能解を優先的に評価しつつ、制約違反量を考慮した評価が可能になります。
```math
f(\boldsymbol{x}) = f(\boldsymbol{x}_0) + r(\boldsymbol{x})
```
$f$: 目的関数  
$f(\boldsymbol{x}_0)$: 対象個体群中の目的関数の最悪値  
$r(\boldsymbol{x})$: 制約違反量

## 設定可能なキーワード引数一覧
- `population_size: int | null` ... 集団サイズ。デフォルト（設定無の場合）は`10*dim`。
- `num_parents: int | null` ... 親個体数。デフォルト（設定無の場合）は`population_size`。
- `num_children: int | null` ... 子個体。デフォルト（設定無の場合）は`2*num_parents`。
- `variable_type_counts: dict | null` ... 変数タイプごとの次元数。
    - `categorical: int` ... カテゴリ変数の次元数。
    - `discrete: int` ... 整数変数の次元数。
    - `continuous: int | null` ... 実数変数の次元数。未設定の場合，自動的に`dim - categorical - discrete`が値として計算される。
- `categorical_choice list[list[float | int]] | null` ... カテゴリ変数の候補値（整数値）。各変数ごとにリストで与える。
- `discrete_values list[list[float | int]] | null` ... 整数変数の候補値（整数値）。各変数ごとにリストで与える。
- `bounds: tuple[float, float] | list[tuple[float, float]]` ... 実数変数の上下限値。
:::tip[`bounds`の挙動]
- デフォルト値（設定無の場合） ... \[-1, 1\]がすべての変数の上下限値に適用。
- `bounds: tuple[float, float]`の場合 ... 与えた数値の組がすべての変数の上下限値に設定される。
- `bounds: list[tuple[float, float]]`の場合 ... 与えた数値の組のリストが各変数の上下限値に設定される。上下限値の設定は途中までで打ち切ることが可能（この場合、打ち切り以降の上下限値は-1~1に自動設定される）。
:::
- `seed: int | null` ... 乱数シード値。デフォルト値は`null`（乱数シード非固定）。
- `scalarizer_type: str | null` ... スカラー化タイプ。`evaluator`が多目的の場合（`metrics.objectives`に複数の値が入る場合）に，それらを単目的に変換します。`weighted_sum`, `tchebycheff`, `pbi`のいずれかに設定します。`null`の場合，[`metrics.fitness`](../individual.md#optimizationproblemmetrics)をそのまま単目的に使用します。デフォルト値は`null`。
- `scalarizer_weights: list[float] | null` ... スカラー化重み係数。