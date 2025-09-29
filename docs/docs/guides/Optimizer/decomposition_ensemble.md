---
sidebar_position: 4
---

# decomposition_ensemble
多目的最適化アルゴリズムMOEA/D\[7\]ベースのpython実装クラスです。多目的最適化を複数の単目的最適化に分解し、CMA-ESによって解きます\[8\]。  
ただし、原著論文で行われている近傍問題間での情報共有などは行わず、分解後の単目的最適化をCMA-ESによって独立して解きます。

## 概要
MOEA/Dとは、多目的最適化を適切なアプローチによって複数の単目的最適化に分解し、各単目的問題を解く手法です。分解アプローチとして原著論文\[7\]では単純重み付き和（Weighted Sum）、Tchebycheffのアプローチ、Penalty-based Boundary Intersection (PBI) が紹介されています。

本実装では分解後の単目的最適化問題をCMA-ESによって独立に解きます。最適化過程で得られた解集団は非優越ソート\[6\]され、その結果ランク1となった個体群はパレート解候補としてアーカイブされます。
:::info
単目的最適化へ分解したとき、目的関数間のスケールに大きな違いがあると探索が偏ってしまいます。  
`decomposition_ensemble`を使用する際は`coefficient`によって目的関数を正規化することを推奨します。具体例は[Dmodel多目的最適化の例](../../../showcase/Dmodel/moo.md)をご覧ください。
:::

## 設定可能なキーワード引数一覧
- `dim: int` ... 最適化問題の次元数$n$。
:::info
evaluatorが`pyemsol_shape_evaluator`の場合、`dim`はlevel set functionなどのコンフィグから自動的に設定されます。
:::
- `num_obj: int` ... 最適化問題の目的関数の数。
:::info
evaluatorが`pyemsol_shape_evaluator`の場合、`num_obj`は`optimization_problem.yaml`から自動的に設定されます。
:::
- `num_decomposition: int` ... 多目的最適化の分解数。デフォルト値は`10`。
:::tip `num_decomposition`による計算時間・パレート解密度のトレードオフ
`num_decomposition`を大きく設定するほど多目的最適化が「細かく」分解されるため、より密なパレート解が得られるようになります。  
一方、計算時間は`num_decomposition`に比例して増加します。
:::
- `decomposition_type: str` ... 分解アプローチ。 `weighted_sum`, `tchebycheff`, `pbi`のいずれかに設定します。デフォルト値は"tchebycheff"。
- `seed: int` ... 乱数シード値。デフォルト値は`null`（乱数シード非固定）。
- `mean: np.ndarray` ... CMA-ESの$\boldsymbol{m}$初期値。デフォルト値は$\boldsymbol{m} = \boldsymbol{0}$。
- `sigma: float` ... CMA-ESの$\boldsymbol{C}$の標準偏差初期値。デフォルト値は`1`。
- `bounds: tuple[float, float] | list[tuple[float, float]]` ... CMA-ESの各変数の上下限値。
:::tip `bounds`の挙動
- デフォルト値（設定無の場合） ... 上下限無し。
- `bounds: tuple[float, float]`の場合 ... 与えた数値の組がすべての変数の上下限値に設定される。
- `bounds: list[tuple[float, float]]`の場合 ... 与えた数値の組のリストが各変数の上下限値に設定される。上下限値の設定は途中までで打ち切ることが可能（この場合、打ち切り以降の上下限値は-1~1に自動設定される）。
:::
- `population_size int` ... CMA-ESの1イテレーションあたりサンプリング個体数。デフォルト値はCMA-ES推奨の $4+\lfloor3\ln{n}\rfloor$。