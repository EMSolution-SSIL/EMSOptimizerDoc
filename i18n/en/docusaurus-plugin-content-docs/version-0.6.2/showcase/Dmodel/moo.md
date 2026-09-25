---
sidebar_position: 3
---

# Dmodel多目的最適化例
ここでは、`Dmodel_moo`プロジェクトの内容について紹介します。  
`Dmodel`プロジェクトと比較して、`Dmodel_moo`では多目的最適化を実施する設定になっています。

## optimization.yaml（`Dmodel_moo`プロジェクト）
最適化を設定する`optimization.yaml`の内容を確認します。  
今回は多目的形状最適化のため、最適化手法に多目的最適化アルゴリズム`decomposition_ensemble`を設定しています。本アルゴリズムの詳細については[docsの該当ページ](../../docs/guides/Optimizer/decomposition_ensemble.md)をご覧ください。  
```yaml
evaluator:
  name: pyemsol_shape_evaluator
optimizer:
  name: decomposition_ensemble
  kwargs:
    num_decomposition: 5
    seed: 42
```

## optimization_problem.yaml（`Dmodel_moo`プロジェクト）
`optimization_problem.yaml`の中身は`Dmodel`プロジェクトと変わりませんが、今回は最適化アルゴリズムが多目的問題用のため、`objectives`はそれぞれが独立した目的関数として認識されます。
```yaml
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
    coefficient: 1.0
```

すなわち、ここで定義された多目的最適化問題は以下の通りです。
```math
\begin{align*}
\text{minimize} \quad & f_1=-\frac{T_\text{avg}}{2.1} \\
                      & f_2=\frac{T_\text{rip}}{54.0} \\
\end{align*}
```
$T_\text{avg}$：平均トルク [Nm]  
$T_\text{rip}$：トルクリプル率 [%]

## 最適化の実施例
Implicit Domain Meshing有（`use_implicit_domain_meshing: True`）として最適化を実施しました。100イテレーション最適化完了後のGUIを以下に示します。  
今回は多目的問題の分解数を5としたためパレートフロントはまばらですが、解の分布する範囲自体は広く得られています。$f_1=-1.05$ ($T_\text{avg}=2.2\text{Nm}$) 付近で平均トルクが頭打ちとなっており、今回の設定下ではここが平均トルクの限界だということが推察されます。  
表示している形状例はそれぞれパレートフロント図の"Left", "Right"の解形状です。"Left"は高い平均トルクと低いトルクリプル率を両立した形状となっており、[基本の最適化](./basic.md)結果に近しい解であることがわかります。一方、"Right"はトルクリプル率の低減に特化した解であり、その値は2.42%と非常に低い反面、磁性体コアがロータ表面から離れてしまっており、結果として平均トルクもかなり低い値となっています。これを防ぐには、平均トルクが一定以上の値となるよう制約条件を課すことが考えられます（[IPM8P48S](../IPM8P48S/basic_moo.md)の例もご覧ください）。
![Dmodelパレートフロント](/img/Dmodel_moo_check.png)