---
sidebar_position: 3
---

# 最適化問題の設定（optimization_problem.yaml）
ここでは、形状最適化における最適化問題の定義について紹介します。

## 最適化問題の設定
EMSOptimizerでは、形状最適化における最適化問題を`opimization_problem.yaml`によって管理します。
`opimization_problem.yaml`を通じて、以下の最適化問題を定義します。
```math
\begin{align*}
\text{minimize} \quad & f_i(\boldsymbol{x}) \quad (i = 1, \ldots, n) \\
\text{subject to} \quad & g_j(\boldsymbol{x}) \leq 0 \quad (j = 1, \ldots, m) \\
                         & h_k(\boldsymbol{x}) = 0 \quad (k = 1, \ldots, p) \\
                         & \boldsymbol{x} \in X
\end{align*}
```
$\boldsymbol{x} = \{x_i\}^\text{T}$: 解候補ベクトル  
$X$: $\boldsymbol{x}$の集合（EMSOptimizerにおいては、$x_i$の上下限値に対応）
:::info
各変数の上下限値は`optimization.yaml`にて設定可能です。  
その他、最適化イテレーション数など最適化そのものの設定に関しては[ユーザガイド > 最適化の設定](../guides/optimization_config.md)ページを参照してください。
:::

$f_i$, $g_i$, $h_i$は`opimization_problem.yaml`ファイル内の以下のリストに対応しており、最適化中に参照されます。
- $f_i$: `objectives`
- $g_i$: `ineq_constraints`
- $h_i$: `eq_costraints`  
- 例外として、`other_metrics`リストは最適化計算には使われず、GUI表示やファイル出力に利用されます。

リスト内の各項目はいずれも以下の設定を持ちます。
- `function_name: str` ... 評価用関数名（下記参照）。
- `case_name: str | null` ... `function_name`を評価する解析ケース名（下記参照）。
- `kwargs: dict` ... 評価用関数に渡すpythonキーワード引数。省略可能。
- `normalization_const: float` ... 正規化定数。下式参照。デフォルト値は`1.0`。
- `coefficient: float` ... 重み係数。下式参照。デフォルト値は`1.0`。
- `baseline: float` ... バイアス項。下式参照。デフォルト値は`0.0`。
:::info
`function_name`に指定可能な評価用関数群、およびそれらの引数`kwargs`の一覧は[ユーザガイド > 評価用関数実装例](../guides/opt_problem_ex.md)をご覧ください。
:::
:::tip `case_names`について
EMSOptimizerにおいては、複数解析ケースに対して目的関数を設定することが可能です。これはモータ等において複数の運転点における性能を同時に最適化したい場合などに活用できます。  
解析ケース名の一覧は`optimization_problem.yaml` > `case_names`にリストとして設定します。また、同名の解析ケースフォルダ群をプロジェクトフォルダ内に格納します。  
実際に複数解析ケースを活用した最適化については[Dmodel_advanced](../../showcase/Dmodel/advanced.md)の例をご覧ください。
:::

以上の設定項目から、各個体に対して$f_i$, $g_i$, $h_i$は以下の式によって計算されます。
```math
\text{coefficient} \times (A - \text{baseline}) / \text{normalization\_const} \\
```
$A$: `case_name`の解析結果に基づき、評価用関数に`kwargs`を与えて計算した結果値

計算値は各個体に紐づけて保存され、optimizer内にて個体更新の処理に利用されます。
:::info
個体や計算値の管理方法の技術的詳細については[ユーザガイド > individual関連オブジェクト API](../guides/individual.md)をご覧ください。
:::

## 最適化問題テンプレートの保存・読込
`opimization_problem.yaml`の内容は最適化問題テンプレートとして`save_tpl`コマンドによって保存できます。テンプレートは`project/problem_template.yaml`に保存されます。
```sh
python emsopt.py save_tpl Dmodel NewProblem
```
保存した最適化問題は`load_tpl`によって他のプロジェクトにコピーできます。
```sh
python emsopt.py load_tpl NewDmodel NewProblem
```

## Example: Dmodel
例として、単目的最適化を想定した`Dmodel`プロジェクト内の`optimization_problem.yaml`を見てみましょう。
```yaml
case_names:
  - transient

objectives:
  - function_name: average_torque
    kwargs:
      torque_scale: 4.0
    normalization_const: 2.1
    coefficient: -1.0
  - function_name: torque_ripple_percentage
    kwargs:
      torque_scale: 4.0
    normalization_const: 54.0
    coefficient: 0.1

ineq_constraints: []

eq_constraints: []

other_metrics:
  - function_name: average_torque
    kwargs:
      torque_scale: 4.0
  - function_name: torque_ripple_percentage
    kwargs:
      torque_scale: 4.0
```

まず、解析ケース名は`transient`（電気角／機械角を動かしながらの多ケース解析）のみです。また、ここでは制約条件を課していないため、`ineq_constraints`および`eq_constraints`は空配列となっています（なお、設定の記載を省略した場合も空配列と同じ扱いになります）。

次に、`objectives`には2つの$f_i$が設定されています。1つ目はモータの平均トルク、2つ目はトルクリプル率（トルク波形のpeak-to-peak振幅を平均トルクによって除した値）を計算する関数です。

`kwargs`にはトルクに乗じる倍率が登録されています。`Dmodel`プロジェクトではモータの4分の1モデルを解析対象としているため、トルクの値をフルモデル相当に変換するために倍率を4としています。

また、それぞれの`normalization_const`, `coefficient`はそれぞれ下式$T^\text{ref}, w$を表しています。ここで$T^\text{ref}$は正規化定数であり、目的関数を無次元化するとともに目的関数間のスケールを合わせるために設定される値です。

```math
w \frac{f_i}{T^\text{ref}}
```

なお、正規化定数としては最適化対象モデルの元々の（最適化前の）性能値がよく用いられます。ここで設定されている値もDmodelの元々の性能値（@電流値3.0 Arms、電流位相角20°）です。

以上を踏まえると本プロジェクトでは以下の通り、負の平均トルクとトルクリプル率の重み付き和を最小化する設定になっています。「負の平均トルクの最大化」＝「（正の）平均トルクの最大化」なので、結果としてこれは平均トルク最大化・トルクリプル率最小化問題となります。

```math
\text{minimize} \quad F=f_1+f_2=-1.0\frac{T_\text{avg}}{2.1} + 0.1\frac{T_\text{rip}}{54.0} \\
```
$T_\text{avg}$：平均トルク [Nm]  
$T_\text{rip}$：トルクリプル率 [%]

最後に、`other_metrics`には平均トルクとトルクリプル率（`coefficient`無の生データ）が登録されています。これにより、GUIからこれらの値を確認できるようになっています。
