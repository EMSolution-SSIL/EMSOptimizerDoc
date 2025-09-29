---
sidebar_position: 3
---

# Dmodel多目的最適化例
ここでは、`Dmodel_moo`プロジェクトの内容について紹介します。  
`Dmodel`プロジェクトと比較して、`Dmodel_moo`では多目的最適化を実施する設定になっています。

## optimization.yaml（`Dmodel`プロジェクト）
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

## optimization_problem.yaml（`Dmodel_advanced`プロジェクト）
`optimization_problem.yaml`の中身は`Dmodel`プロジェクトと変わりませんが、今回は最適化アルゴリズムが多目的問題用のため、`objectives`はそれぞれが独立した目的関数として認識されます。
```yaml
objectives:
  - function_name: average_torque
    kwargs:
      torque_scale: 4.0
    coefficient: -0.476  # -1 / 2.1
  - function_name: torque_ripple_percentage
    kwargs:
      torque_scale: 4.0
    coefficient: 0.0185  # 1 / 54.0
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
