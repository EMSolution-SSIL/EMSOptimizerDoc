---
sidebar_position: 2
---

# cmaes
単目的最適化アルゴリズムCMA-ES\[4\]のpython実装クラスです。  
アルゴリズム部分はpythonライブラリ`cmaes`\[5\]を呼び出す形で実装しており、このクラスは`cmaes`ライブラリのラッパーとして機能します。

## 概要
CMA-ESでは、下記のように正規分布から個体$\boldsymbol{x}$を複数サンプリングします\[4\]。
```math
\boldsymbol{x} \sim \boldsymbol{m} + \sigma \mathcal{N}(\boldsymbol{0}, \boldsymbol{C})
```
CMA-ESでは遺伝的アルゴリズム等とは異なり、明示的な解集団はありません。その代わり、分布パラメータ$\boldsymbol{m}, \sigma, \boldsymbol{C}$等を保持します。  
個体の優劣関係に基づいて分布パラメータを更新することで、サンプリングされる個体を優れた方向に進化させます。

また、制約違反した個体は以下のように評価します\[12\]。これにより、実行可能解を優先的に評価しつつ、制約違反量を考慮した評価が可能になります。
```math
f(\boldsymbol{x}) = f(\boldsymbol{x}_0) + r(\boldsymbol{x})
```
$f$: 目的関数  
$f(\boldsymbol{x}_0)$: サンプリング個体中の目的関数の最悪値  
$r(\boldsymbol{x})$: 制約違反量

## 設定可能なキーワード引数一覧
- `mean: np.ndarray` ... $\boldsymbol{m}$初期値。デフォルト値は$\boldsymbol{m} = \boldsymbol{0}$。
- `sigma: float` ...ステップサイズ初期値。デフォルト値は`1`。
- `bounds: tuple[float, float] | list[tuple[float, float]]` ... 各変数の上下限値。
:::tip[`bounds`の挙動]
- デフォルト値（設定無の場合） ... 上下限無し。
- `bounds: tuple[float, float]`の場合 ... 与えた数値の組がすべての変数の上下限値に設定される。
- `bounds: list[tuple[float, float]]`の場合 ... 与えた数値の組のリストが各変数の上下限値に設定される。上下限値の設定は途中までで打ち切ることが可能（この場合、打ち切り以降の上下限値は-1~1に自動設定される）。
:::
- `seed: int | null` ... 乱数シード値。デフォルト値は`null`（乱数シード非固定）。
- `population_size int` ... 1イテレーションあたりサンプリング個体数。デフォルト値はCMA-ES推奨の $4+\lfloor3\ln{n}\rfloor$。
- `scalarizer_type: str | None` ... スカラー化タイプ。`evaluator`が多目的の場合（`metrics.objectives`に複数の値が入る場合）に，それらを単目的に変換します。`weighted_sum`, `tchebycheff`, `pbi`のいずれかに設定します。`None`の場合，`metrics.fitness`をそのまま単目的に使用します。デフォルト値は`None`。
- `scalarizer_weights: list[float] | None` ... スカラー化重み係数。
