---
sidebar_position: 3
---

# Optimization Problem
ここでは、形状最適化における最適化問題の定義について紹介します。

## About Optimization Problem
EMOptSolutionでは、形状最適化における最適化問題を`opimization_problem.yaml`によって管理します。
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
$X$: $\boldsymbol{x}$の集合（EMOptSolutionにおいては、$x_i$の上下限値に対応）
:::info
各変数の上下限値は`optimization.yaml`にて設定可能です。  
その他、最適化イテレーション数など最適化そのものの設定に関しては[Guides > Optimization Configuration](../guides/optimization_config.md)ページを参照してください。
:::

各項目は`opimization_problem.yaml`ファイル内の以下のリストに対応しており、最適化中に参照されます。
- $f_i$: `objectives`
- $g_i$: `ineq_constraints`
- $h_i$: `eq_costraints`  
- 例外として、`other_metrics`リストは最適化計算には使われず、GUI表示やファイル出力に利用されます。

$f_i$, $g_i$, $h_i$はいずれも以下の設定項目を持ちます。
- `function_name: str` ... 関数名。実装本体は`core/opt_problem_functions.py`に記述されています。利用可能な関数名の一覧は`show_avl`コマンドでも確認できます。
- `case_name: str | null` ... `function_name`を評価する解析ケース名。`optimization_problem.yaml` > `case_names`から選択する。未設定（もしくは`null`を設定）の場合、`case_names`の一番上の解析ケースが自動的に使用される。
- `kwargs: dict` ... 関数に渡すpythonキーワード引数。省略可能。
    - なお、各関数の引数のうち`working_dir`は特殊なキーワードに位置付けられています。このキーワード引数はEMOptSolution内部にて自動的に設定されるため、yamlファイル内で設定は不要です（設定しても実行時には無視されます）。
- `coefficient: float` ... 重み係数。以下参照。デフォルト値は`1.0`。
- `baseline: float` ... バイアス項。以下参照。デフォルト値は`0.0`。

以上の設定項目から、各`Individual`において関数は以下の式によって計算されます。ここで、$\text{function\_name}$は`case_name`に設定された解析ケース結果に基づいて計算されます。
```math
\text{coefficient} \times (\text{function\_name}(\text{**kwargs}) - \text{baseline})
```

計算値は各`Individual`に`metrics`として保存され、optimizer内にて個体更新の処理に利用可能になります。この他に、`metrics`には特殊な値として`fitness`が設定されており、これは各$f_i$の和を計算したものと定義されます。この値は主に単目的最適化の計算に利用できます。

## Save / Load Optimization Problem as Template
`opimization_problem.yaml`の内容は最適化問題テンプレートとして`save_tpl`コマンドによって保存できます。テンプレートは`project/problem_template.yaml`に保存されます。
```sh
python emopt.py save_tpl NewDmodel NewProblem
```
保存した最適化問題は`load_tpl`によってプロジェクトにコピーできます。
```sh
python emopt.py load_tpl NewDmodel NewProblem
```
save, loadともyamlファイルの中身を複製しているに過ぎないため、これらの操作は手動で行っても構いません。

## Example 1: Dmodel
例として、単目的最適化を想定した`Dmodel`プロジェクト内の`optimization_problem.yaml`を見てみましょう。
```yaml
case_names:
  - transient

objectives:
  - function_name: average_torque
    kwargs:
      torque_scale: 4.0
    coefficient: -0.4762   # -1.0 / 2.1
  - function_name: torque_ripple_percentage
    kwargs:
      torque_scale: 4.0
    coefficient: 0.00185   # 0.1 / 54.0

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

また、それぞれの`coefficient`はその横にコメントで書かれた値を計算した結果です。これは、以下の式の定数部分$\frac{w}{T^\text{ref}}$に相当します。ここで$T^\text{ref}$は正規化定数であり、目的関数を無次元化するとともに目的関数間のスケールを合わせるために設定される値です。

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

最適化のプロセスにおいて形状評価が終わると、`Individual.metrics.fitness`に$F$の値が格納されます。これがoptimizer内の処理において`Individual`の更新に利用されることで最適化が進行します。

最後に、`other_metrics`には平均トルクとトルクリプル率（`coefficient`無の生データ）が登録されています。これにより、GUIからこれらの値を確認できるようになっています。

## Example 2: GL80
より発展的な例として、`GL80`プロジェクト内の`optimization_problem.yaml`を見てみましょう。
```yaml
case_names:
  - transient

objectives:
  - function_name: torque_ripple_percentage
    kwargs:
      torque_scale: 6.0

ineq_constraints:
  - function_name: average_torque
    kwargs:
      torque_scale: 6.0
    coefficient: -1.0
    baseline: 0.97

eq_constraints:
  - function_name: num_connected_components
    kwargs:
      phisical_tag: 20
    baseline: 1.0

other_metrics:
  - function_name: average_torque
    kwargs:
      torque_scale: 6.0
  - function_name: torque_ripple_percentage
    kwargs:
      torque_scale: 6.0
```

構成は先ほどの例と同じですが、ここでは制約条件付きのトルクリプル率最小化問題が定義されています。なお、プロジェクトに登録されているGL80モデルは6分の1モデルのため、トルク倍率は6となっています。

制約条件は2つあり、1つ目は`ineq_constraints`に記載の平均トルク制約です。`coefficient`が-1、`baseline`が0.97となっており、これは以下の不等式制約を表しています。
```math
g_1  = - (T_\text{avg}-0.97) \leq 0 \quad
```

すなわち、

```math
T_\text{avg} \geq 0.97 \quad
```

よって、平均トルクが0.97 Nm以上であることを制約に課しています。

次に、`eq_constraints`記載の連結制約です。ここでは、`phisical_tag`（材料番号）が`20`の領域の連結成分数が1となることを制約条件に課しています。

`GL80`プロジェクト内では`20`はロータコア領域を表しているため、この制約は「**ロータコアが一体となっており、浮いた領域が無いこと（＝ロータコアとして現実的な形状をしていること）**」を課しています。
