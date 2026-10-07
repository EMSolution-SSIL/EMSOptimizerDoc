---
sidebar_position: 2
---

# EMSOptimizerのコンセプト
ここでは、EMSOptimizerを使う上でコアとなる概念について紹介します。

## 概要
以下の図は、EMSOptimizerの各機能（以下、コアオブジェクト）がどのように協働するかを示したものです。①→②→...→⑧が一連の処理（イテレーション）の流れとなっており、これを繰り返すことで最適化が進行します。  
:::info
②～⑦は形状最適化（＝`evaluator`が後述の`pyemsol_shape_evaluator`）の場合のみ実行されます。  
②～⑦の処理は`emsopt_analyzer`パッケージに含まれます。
:::
![Concepts Overview](/img/concepts_overview.drawio.png)

## コアオブジェクト実装例
EMSOptimizerではすぐに使用できるコアオブジェクトの実装例を提供しています。実装例はEMSOptimizerフォルダ内の`core` > `{コアオブジェクト名称}` > `examples`フォルダに存在します。  
ユーザは既存の実装例を利用するほか、ユーザ自身が修正あるいは新規に作成して自由に組み合わせることが可能です。どの実装を使うかは`optimization.yaml`内で設定します。
:::info[関連ページ]
- `optimization.yaml`の設定方法→[ユーザガイド > 最適化の設定](../guides/optimization_config.md)
- 各オブジェクト実装例の詳細や設定→ユーザガイド内の各セクション
- コアオブジェクトの自作方法→[発展的なトピック > コアオブジェクトの自作](../advanced/user_define.md)
:::

### Optimizer
最適化アルゴリズム（解候補の生成・更新）を担うオブジェクトです。`evaluator`によって評価された解候補を受け取り、新たな解候補を生成して`evaluator`に渡す役割を担います。

以下にEMSOptimizer既定の実装例の一部を示します。
- [`cmaes`](../guides/Optimizer/cmaes.md): 単目的最適化アルゴリズムCMA-ES\[4\], \[5\]。
- [`nsga2`](../guides/Optimizer/nsga2.md): 多目的最適化アルゴリズムNSGA-II\[6\]。
- [`decomposition_ensemble`](../guides/Optimizer/decomposition_ensemble.md): 多目的最適化アルゴリズムMOEA/D\[7\]ベースの実装例。多目的最適化を複数の単目的最適化に分解して解く。各単目的最適化問題はCMA-ESによって解く\[8\]。

### Evaluator
解候補の評価を担うオブジェクトです。`optimizer`によって生成された解候補を評価（目的関数値および制約関数値を計算）して`optimizer`に返す役割を担います。  

以下にEMSOptimizer既定の実装例の一部を示します。
- [`sphere`](../guides/Evaluator/sphere.md): 単目的最適化ベンチマークSphere関数\[11\]。
- [`rastrigin`](../guides/Evaluator/rastrigin.md): 単目的最適化ベンチマークRastrigin関数\[11\]。
- [`zdt1`](../guides/Evaluator/zdt1.md): 多目的最適化ベンチマークZDT1関数\[9\]。
- [`pyemsol_shape_evaluator`](../guides/Evaluator/pyemsol_shape_evaluator.md): **形状最適化用の評価実装**。`ls_function`や`ems_shape_builder`によって定義された形状を電磁界シミュレータパッケージpyemsolを用いて解析し、`optimization_problem.yaml`に定義された目的関数および制約条件を計算します（`optimizer_problem.yaml`については[最適化問題の設定](./opt_problem.md)ページを参照）。  
:::info
`pyemsol_shape_evaluator`は`emsopt_analyzer`パッケージにて定義されおり、`examples`フォルダ内に実装はありません。  
また、`pyemsol_shape_evaluator`による形状最適化の実行には`emsopt_analyzer`のインストールが必要です。
:::
なお、`sphere`, `rastrigin`, `zdt1`は最適化ベンチマーク関数であり、形状最適化を実行する前に`optimizer`の性能をチェックするために活用することができます。

:::tip[EMSOptimizerにおける形状最適化]
EMSOptimizerにおいては明確な「形状最適化モード」のようなものは存在しません。  
単に`evaluator`に`pyemsol_shape_evaluator`を設定することで、その内部で形状に対する諸々の計算が行われます。  
したがって、ベンチマーク関数の最適化と全く同じように形状最適化を実行することが可能です（ただし、形状最適化時には`machine.yaml`と`optimization_problem.yaml`の設定が必要です）。
:::

### Level Set Function
トポロジー最適化におけるレベルセット関数です。解候補ベクトル内の対応する変数を元にレベルセット関数の出力を計算する役割を担います。  
`evaluator`に`pyemsol_shape_evaluator`を設定したときに参照され、`machine.yaml`にて定義された設計対象の各位置における関数値を計算します。材料種の割り当ては関数値を元に`pyemsol_shape_evaluator`内で行われます。
:::info
EMSOptimizerでは「設計領域内の各位置（正確には、設計領域内の各要素の中心座標）で正負の値を返す関数」全体をレベルセット関数と呼称しています。  
一般的には「レベルセット法（トポロジー最適化手法の一種）に用いられる、材料境界を表現する関数」を特に指すことが多いです。
:::

以下にEMSOptimizer既定の実装例の一部を示します。
- [`ls_r`](../guides/LevelSetFunction/ls_r.md): 半径ごとにレベルをセットするシンプルな実装例。
- [`ngnet`](../guides/LevelSetFunction/ngnet.md): NGnet関数\[3\]。
- [`ngnet_mixture`](../guides/LevelSetFunction/ngnet_mixture.md): `ls_r`と`ngnet`を組み合わせ、ある半径以内（または以外）の領域についてNGnet関数を適用する実装例。
- [`ngnet_multi_material`](../guides/LevelSetFunction/ngnet_multi_material.md): 多材料表現型のNGnet関数\[3\]。

### AnalysisConditioner
形状最適化における解析条件（電流位相角、磁化方向など）の動的な設定を担います。`evaluator`に`pyemsol_shape_evaluator`を設定したときに参照され、解候補ベクトル内の対応する変数を元に解析条件に関するパラメータを変更します。  
すなわち、このオブジェクトを設定することで解析条件を最適化対象に含めることが可能です。

以下にEMSOptimizer既定の実装例の一部を示します。
- [`phase_conditioner`](../guides/AnalysisConditioner/phase_conditioner.md): 電流位相角を変更します。

### eMotorSolution Shape Builder
寸法最適化における形状定義を担います。`evaluator`が`pyemsol_shape_evaluator`、かつeMotorSolution連携時に使用可能で、解候補ベクトル内の対応する変数を元にモータの部品寸法を設定する役割を担います。
:::info
eMotorSolution連携については[発展的なトピック > eMotorSolutionとの連携](../advanced/link_ems.md)をご覧ください。
:::

以下にEMSOptimizer既定の実装例の一部を示します。
- [`HoleMagnet55`](../guides/EMSShapeBuilder/holemagnet55.md): eMotorSolution HoleMagnet Type 55 永久磁石定義。`IPM8P48S_pto`プロジェクト内で使用されています。

:::tip[解析条件・寸法・トポロジーの同時最適化]
EMSOptimizerでは`analysis_conditioner`、`ls_function`、`ems_shape_builder`はすべて独立に・同時に設定可能です。特に、`ems_shape_builder`を`ls_function`と同時に設定することで、寸法・トポロジーの同時最適化\[10\]が実行可能です。  
より詳細には、解候補ベクトルは以下のように解釈されます。
```math
\boldsymbol{x} = [\boldsymbol{p}^\text{T}, \boldsymbol{d}^\text{T}, \boldsymbol{w}^\text{T}]^\text{T}
```
$\boldsymbol{x}$: 解候補ベクトル  
$\boldsymbol{p}$: `analysis_conditioner`に与えられる解析条件情報ベクトル  
$\boldsymbol{d}$: `ems_shape_builder`に与えられる寸法情報ベクトル  
$\boldsymbol{w}$: `ls_function`に与えられるレベルセット関数パラメータベクトル  
$\boldsymbol{p}$, $\boldsymbol{d}$, $\boldsymbol{w}$ のうち、未設定のオブジェクトに対応するベクトルはゼロベクトルと見なされます。
:::

:::tip[最適化コントロール]
`evaluator`と`optimizer`とを協働させる役割は`manager/optimization_manager.py`が担っています。
`manager`フォルダ内にはほかにもCLI定義、GUI出力、ファイル出力を行うクラスが定義されています。
:::
