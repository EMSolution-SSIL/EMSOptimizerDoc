---
sidebar_position: 2
---

# Dmodel発展的な最適化例
ここでは、`Dmodel_advanced`プロジェクトの内容について紹介します。  
`Dmodel`プロジェクトと比較して、`Dmodel_advanced`では`optimization_problem.yaml`の中身が大きく異なっています。具体的には、最適化時に2つの電流条件を与え、それぞれの条件下におけるトルク特性を同時に考慮した最適化を行います。

## optimization_problem.yaml（`Dmodel_advanced`プロジェクト）
では、`optimization_problem.yaml`の中身を確認します。

### 解析ケース
まず、`case_names`が2つ存在します。1つ目は`transient`で、これは`Dmodel`プロジェクトのものと同様の条件（電流3.0Arms, 電流位相角20deg）を与える解析ケースです。  
2つ目は`transient_high_current`で、電流値が3.0Armsから9.0Armsに、電流位相角が20degから30degに、それぞれ変更されています。  
これらと同名の解析ケースフォルダが`Dmodel_advanced`プロジェクトフォルダ内にあり、電流条件（およびその他の解析条件）は各解析ケースフォルダ内の同名jsonファイルに記載されています。jsonファイルのフォーマットについてはEMSolutionのドキュメントをご覧ください。
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
\text{minimize} \quad F=f_1+f_2=-1.0\frac{T_\text{avg}^\text{3.0Arms}}{2.1} - 1.0\frac{T_\text{avg}^\text{9.0Arms}}{6.3} \\
```
$T_\text{avg}^\text{3.0Arms}$：平均トルク@3.0Arms [Nm]  
$T_\text{avg}^\text{9.0Arms}$：平均トルク@9.0Arms [Nm]  
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

### 等式制約
次に、等式制約（`eq_constraints`）です。ここでは、[基本の最適化](./basic.md)ページの最後に説明があるように、ロータコアに結合制約をかけています。
```yaml
eq_constraints:
  - function_name: num_connected_components
    kwargs:
      physical_tag: 20
      element_type: triangle
    baseline: 1
```

最後に、`other_metrics`では関連する生値をGUI用に出力するよう設定してあります。

## 最適化の実施例
