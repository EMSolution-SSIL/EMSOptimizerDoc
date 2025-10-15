---
sidebar_position: 3
---

# 最適化問題の設定（optimization_problem.yaml）
ここでは、形状最適化における最適化問題の定義について紹介します。

## `case_names`について
EMSOptimizerにおいては、複数解析ケースに対して目的関数を設定することが可能です。これはモータ等において複数の運転点における性能を同時に最適化したい場合などに活用できます。  
解析ケース名の一覧は`optimization_problem.yaml` > `case_names`にリストとして設定します。また、同名の解析ケースフォルダ群をプロジェクトフォルダ内に格納します。  
:::info
実際に複数解析ケースを活用した最適化については[Dmodel_advanced](../../showcase/Dmodel/advanced.md)の例をご覧ください。
:::

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
- `function_name: str` ... 関数名。関数名に対応する実装内容は`core/opt_problem_functions.py`に記述されています。利用可能な関数名の一覧は`show_avl`コマンドでも確認できます。
- `case_name: str | null` ... `function_name`を評価する解析ケース名。冒頭で説明した`case_names`の中から選択する。未設定（もしくは`null`を設定）の場合、`case_names`の一番上の解析ケースが自動的に使用されます。
- `kwargs: dict` ... 関数に渡すpythonキーワード引数。省略可能。
    - なお、各関数の引数のうち`working_dir`は特殊なキーワードに位置付けられています。このキーワード引数はEMSOptimizer内部にて自動的に設定されるため、yamlファイル内では設定不要です（設定しても実行時には無視されます）。
- `coefficient: float` ... 重み係数。下式参照。デフォルト値は`1.0`。
- `baseline: float` ... バイアス項。下式参照。デフォルト値は`0.0`。

以上の設定項目から、各`Individual`において$f_i$, $g_i$, $h_i$は以下の式によって計算されます。
```math
\text{coefficient} \times (A - \text{baseline}) \\
```
$A$: `case_name`の解析結果に基づき、`function_name`に`kwargs`を与えて計算した結果値

計算値は各`Individual`に`metrics`として保存され、optimizer内にて個体更新の処理に利用可能になります。また、`metrics`には特殊な値として`fitness`が設定されており、これは各$f_i$の和を計算したものと定義されます。この値は主に単目的最適化の計算に利用できます。

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

最適化のプロセスにおいて形状評価が終わると、`Individual.metrics.objectives`に$f_1,f_2$の値が、`Individual.metrics.fitness`に$F$の値が、それぞれ格納されます。これらの値がoptimizer内の処理において`Individual`の更新に利用されることで最適化が進行します。

最後に、`other_metrics`には平均トルクとトルクリプル率（`coefficient`無の生データ）が登録されています。これにより、GUIからこれらの値を確認できるようになっています。
