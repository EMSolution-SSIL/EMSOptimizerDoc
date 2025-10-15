---
sidebar_position: 2
---

# EMSOptimizerのコンセプト
ここでは、EMSOptimizerを使う上でコアとなる概念について紹介します。

## 概要
以下の図は、EMSOptimizerの各機能（オブジェクト）がどのように協働するかを示したものです。①→②→...→⑧が一連の処理（イテレーション）の流れとなっており、これを繰り返すことで最適化が進行します。  

![Concepts Overview](/img/concepts_overview.drawio.png)

## Individual, Population
`Individual`は、EMSOptimizer内において個体を表すオブジェクトです。**ここでいう個体は、「最適化過程において生成される解候補およびそれに対する評価値を保有したオブジェクト」のこと**を指します。また、**`Population`は複数の`Individual`をひとまとめにしたオブジェクトです**。  
EMSOptimizerでは`Individual`ないし`Population`がオブジェクト間を行き来し、それぞれのオブジェクトが各`Individual`に対して形状定義・形状の電磁界解析と評価・評価に基づく解候補ベクトル更新などの操作を行うことで最適化を進行します。

`Individual`は以下の情報（メンバ変数）を保持します。
- `solution`: 解候補ベクトル。
- `metrics`: 目的関数および制約関数の値をまとめたオブジェクト。詳細は[最適化問題の設定](./opt_problem.md)ページを参照。
- `outcome_filepath`: 形状最適化における結果形状のメッシュファイルへのパス。形状最適化実行時、EMSOptimizer内で自動的に設定されます。


## コアオブジェクト
ここでは、EMSOptimizerのコアとなるオブジェクト群とその実装例を簡単に紹介します。冒頭で示したオブジェクト群の実装方法は様々ですが、EMSOptimizerではすぐに使用できるいくつかの実装例を提供しています。  
ユーザは既存の実装例を利用するほか、ユーザ自身が修正あるいは新規に作成して自由に組み合わせることが可能です。どの実装を使うかは`optimization.yaml`内で設定します。
:::info 関連ページ
- `optimization.yaml`の設定方法→[ユーザガイド > 最適化の設定](../guides/optimization_config.md)
- 各オブジェクト実装例の詳細や設定→ユーザガイド内の各セクション
- コアオブジェクトの自作方法→[ユーザガイド > コアオブジェクトの自作](../guides/user_define.md)
:::

### Optimizer (core/optimizer)
最適化アルゴリズム（`Individual`の生成・更新）を担うオブジェクトです。`evaluator`によって評価された`Individual`を受け取り、新たな`Individual`を生成して`evaluator`に渡す役割を担います。

以下の実装例（`examples`フォルダ内）がデフォルトで利用可能です。
- `cmaes`: 単目的最適化アルゴリズムCMA-ES\[4\], \[5\]。
- `nsga2`: 多目的最適化アルゴリズムNSGA-II\[6\]。
- `decomposition_ensemble`: 多目的最適化アルゴリズムMOEA/D\[7\]に基づく実装。多目的最適化を複数の単目的最適化に分解して解く。各単目的最適化問題はCMA-ESによって解く\[8\]。

### Evaluator (core/evaluator)
`Indvidual`の評価を担うオブジェクトです。`optimizer`によって生成された`Individual`を評価し、`Individual.metrics`に目的関数値および制約条件値を格納して`optimizer`に返す役割を担います。また、形状最適化においては他のオブジェクトおよび電磁界シミュレータパッケージpyemsolと連携し、形状定義から`metrics`の計算までの一連の処理を担います。

以下の実装例（`examples`フォルダ内）がデフォルトで利用可能です。
- `rastrigin`: 単目的最適化ベンチマークRastrigin関数\[11\]。
- `zdt1`: 多目的最適化ベンチマークZDT1関数\[9\]。
- `pyemsol_shape_evaluator`: **形状最適化用の評価実装**。`ls_function`や`ems_shape_builder`によって定義された形状を電磁界シミュレータパッケージpyemsolを用いて解析し、`optimization_problem.yaml`に定義された目的関数および制約条件を計算します（`optimizer_problem.yaml`については[最適化問題の設定](./opt_problem.md)ページを参照）。
`pyemsol_shape_evaluator`は例外的にEMSOptimizer内部にて定義されおり、`examples`フォルダ内に実装はありません。

なお、前半2つは最適化ベンチマーク関数であり、形状最適化を実行する前に`optimizer`の性能をチェックするために活用することができます。

:::tip EMSOptimizerにおける形状最適化
EMSOptimizerにおいては明確な「形状最適化モード」のようなものは存在しません。  
単に`evaluator`に`pyemsol_shape_evaluator`を設定することで、その内部で形状に対する諸々の計算が行われます。  
したがって、ベンチマーク関数の最適化と全く同じように形状最適化を実行することが可能です（ただし、形状最適化時には`machine.yaml`と`optimization_problem.yaml`の設定が必要です）。
:::

### Level Set Function (core/ls_function)
トポロジー最適化におけるレベルセット関数です。`Individual`の解候補ベクトルからレベルセット関数の出力を計算する役割を担います。  
`evaluator`に`pyemsol_shape_evaluator`を設定したときに参照され、`machine.yaml`にて定義された設計対象の各位置における関数値を計算します。実際の材料種の割り当ては関数値を元に`pyemsol_shape_evaluator`内で行われます。
:::info
EMSOptimizerでは「設計領域内の各位置で正負の値を返す関数」全体をレベルセット関数と呼称しています。  
一般的には「レベルセット法（トポロジー最適化手法の一種）に用いられる、材料境界を表現する関数」を特に指すことが多いです。
:::

以下の実装例（`examples`フォルダ内）がデフォルトで利用可能です。
- `ls_r`: 半径ごとにレベルをセットするシンプルな実装例。
- `ngnet`: NGnet関数\[3\]。
- `ngnet_mixture`: `ls_r`と`ngnet`を組み合わせ、ある半径以内の領域についてNGnet関数を適用する実装例。

### AnalysisConditioner (core/analysis_conditioner)
形状最適化における解析条件（電流位相角、磁化方向など）の動的な設定を担います。`evaluator`に`pyemsol_shape_evaluator`を設定したときに参照され、`Individual`の解候補ベクトルから解析条件に関するパラメータを変更します。  
すなわち、このオブジェクトによって解析条件を最適化対象に含めることが可能となります。

以下の実装例（`examples`フォルダ内）がデフォルトで利用可能です。
- `phase_conditioner`: 電流位相角を変更します。

### eMotorSolution Shape Builder (core/ems_shape_builder)
寸法最適化における形状定義を担います。`evaluator`が`pyemsol_shape_evaluator`、かつeMotorSolution連携時に使用可能で、`Individual`の解候補ベクトルからモータの部品寸法を設定する役割を担います。

:::info
eMotorSolution連携については[ユーザガイド > eMotorSolutionとの連携](../guides/link_ems.md)をご覧ください。
:::

以下の実装例（`examples`フォルダ内）がデフォルトで利用可能です。
- `HoleMagnet55`: eMotorSolution HoleMagnet Type 55 永久磁石定義。`IPM8P48S_pto`プロジェクト内で使用されています。

:::tip 解析条件・寸法・トポロジーの同時最適化
EMSOptimizerでは`analysis_conditioner`、`ls_function`、`ems_shape_builder`はすべて独立に・同時に設定可能です。特に、`ems_shape_builder`を`ls_function`と同時に設定することで、寸法・トポロジーの同時最適化\[10\]が実行可能です。  
より詳細には、`Individual.solution`は以下のように解釈されます。
```math
\boldsymbol{x} = [\boldsymbol{p}^\text{T}, \boldsymbol{d}^\text{T}, \boldsymbol{w}^\text{T}]^\text{T}
```
$\boldsymbol{x}$: 解候補ベクトル（`Individual.solution`）  
$\boldsymbol{p}$: `analysis_conditioner`に与えられる解析条件情報ベクトル  
$\boldsymbol{d}$: `ems_shape_builder`に与えられる寸法情報ベクトル  
$\boldsymbol{w}$: `ls_function`に与えられるレベルセット関数パラメータベクトル  
$\boldsymbol{p}$, $\boldsymbol{d}$, $\boldsymbol{w}$ のうち、未設定のオブジェクトに対応するベクトルはゼロベクトルと見なされます。
:::

:::tip 最適化コントロール
`evaluator`と`optimizer`とを協働させる役割は`manager/optimization_manager.py`が担っています。  
`manager`フォルダ内にはほかにもGUIやファイル出力を担当するクラスが定義されていますが、ここでは割愛します。
:::
