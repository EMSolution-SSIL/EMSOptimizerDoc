---
sidebar_position: 2
---

# Dmodel発展的な最適化例
ここでは、`Dmodel_advanced`プロジェクトの内容について紹介します。  
`Dmodel`プロジェクトと比較して、`Dmodel_advanced`では`optimization_problem.yaml`の中身が大きく異なっています。具体的には、最適化時に2つの電流条件を与え、それぞれの条件下におけるトルク特性を同時に考慮した最適化を行います。

## optimization_problem.yaml（`Dmodel_advanced`プロジェクト）
では、`optimization_problem.yaml`の中身を確認します。

### 解析ケース
一番の変更点として、`case_names`が2つ存在します。1つ目は`transient`で、これは`Dmodel`プロジェクトのものと同様の条件（電流3.0Arms, 電流位相角20deg）を与える解析ケースです。  
2つ目は`transient_high_current`で、電流値が3.0Armsから9.0Armsに、電流位相角が20degから30degに、それぞれ変更されています。  
これらと同名の解析ケースフォルダが`Dmodel_advanced`プロジェクトフォルダ内にあり、電流条件（およびその他の解析条件）は各解析ケースフォルダ内の同名jsonファイルに記載されています。jsonファイルのフォーマットについては電磁界シミュレータEMSolution(pyemsol)のドキュメントをご覧ください。
```yaml
case_names:
  - transient
  - transient_high_current
```

### 目的関数
次に、目的関数（`objectives`）です。ここでは、それぞれの解析条件下における平均トルクの重み付き和を最大化する最適化問題を定義しています。
```yaml
objectives:
  - function_name: average_torque
    case_name: transient
    kwargs:
      torque_scale: 4.0
    coefficient: -0.4762   # -1.0 / 2.1
  - function_name: average_torque
    case_name: transient_high_current
    kwargs:
      torque_scale: 4.0
    coefficient: -0.1587   # -1.0 / 6.3
```
これを単目的問題として式で書くと（今回も`optmization.yaml`では単目的最適化アルゴリズム`cmaes`を設定）、以下の通りです。
```math
\text{minimize} \quad F=f_1+f_2=-1.0\frac{T_\text{avg}^\text{3.0Arms20deg}}{2.1} - 1.0\frac{T_\text{avg}^\text{9.0Arms30deg}}{6.3} \\
```
$T_\text{avg}^\text{3.0Arms20deg}$：平均トルク@3.0Arms,20deg [Nm]  
$T_\text{avg}^\text{9.0Arms30deg}$：平均トルク@9.0Arms,30deg [Nm]  
なお、各項の分母の値（正規化定数）は同条件下におけるオリジナルのDmodelの平均トルクです。

### 不等式制約
次に、不等式制約（`ineq_constraints`）です。ここでは、それぞれの解析条件下におけるトルクリプルの値に制約をかけています。  
それぞれ30%以下となるよう制約します。
```yaml
  - function_name: torque_ripple_percentage
    case_name: transient
    kwargs:
      torque_scale: 4.0
    baseline: 30.0
  - function_name: torque_ripple_percentage
    case_name: transient_high_current
    kwargs:
      torque_scale: 4.0
    baseline: 30.0
```
式で書くと以下の通りです。
```math
\begin{align*}
\text{subject to} \quad & g_1(\boldsymbol{x}) = T_\text{rip}^\text{3.0Arms20deg} - 30.0 \leq 0 \\
                        & g_2(\boldsymbol{x}) = T_\text{rip}^\text{9.0Arms30deg} - 30.0 \leq 0
\end{align*}
```
$T_\text{rip}^\text{3.0Arms20deg}$：トルクリプル率@3.0Arms,20deg [%]  
$T_\text{rip}^\text{9.0Arms30deg}$：トルクリプル率@9.0Arms,30deg [%]  

### 等式制約
次に、等式制約（`eq_constraints`）です。ここでは、[基本の最適化](./basic.md)ページの最後に説明があるように、ロータコアが一体となる（分離した箇所や浮島を生じない）ように制約をかけています。
```yaml
eq_constraints:
  - function_name: num_connected_components
    kwargs:
      physical_tag: 20
    baseline: 1
```

最後に、`other_metrics`では関連する値をGUI用に出力するよう設定してあります。

## 最適化の実施例
Implicit Domain Meshing有（`use_implicit_domain_meshing: True`）として最適化を実施しました。100イテレーション最適化完了後のGUIを以下に示します。  
10イテレーション目まではトルクリプル制約を満たさない解も見られますが、最終的には制約違反値は0となり、トルクリプル制約を満たす解が得られたことが分かります。  
GUIの図に示しているのが最良形状（93イテレーション目）です（$T_\text{avg}^\text{3.0Arms20deg}$=2.13Nm, $T_\text{avg}^\text{9.0Arms30deg}$=6.91Nm, $T_\text{rip}^\text{3.0Arms20deg}$=26.8%, $T_\text{rip}^\text{9.0Arms30deg}$=16.4%）。[基本の最適化](./basic.md)とは違ったフラックスバリア形状となっていることが分かります。  
また、磁石両端にわずかではありますが磁性体コアの層が存在しており、結合制約を満たす形状となっています。
![Dmodel最適化履歴](/img/Dmodel_advanced_check.png)