---
sidebar_position: 6
---

# Dmodel勾配ベース最適化例（密度法ライク）
ここでは，`Dmodel_SynRM_gradient`プロジェクトの内容について紹介します。  
`Dmodel_SynRM_gradient`では同期リラクタンスモータ（SynRM）を想定し，勾配ベースのトポロジー最適化手法（密度法ライク）によって最適化を行います。

## ベースメッシュについて
`Dmodel_SynRM_gradient`では[多材料最適化例](./multi_material.md)と同様に，ベースメッシュとしてロータ部が永久磁石を含まず材料番号`20`（磁性体コア）のみからなるメッシュを使用し，ロータ部全域について空気／磁性体コア分布を最適化します。

## optimization.yaml（`Dmodel_SynRM_gradient`プロジェクト）
`optimization.yaml`では，レベルセット関数`level_set_function`に`pyemsol_density`を指定します。これにより，目的関数`W1`（トルク）に関する勾配計算がEMSOptimizer内部で行われます。  
計算した勾配は`optimizer`の`gradient_update`の中で設計変数（ここでは，設計領域内の各要素の物性値を表現する[-1,1]の値）の更新に利用されます。`scaling_mode: sign`と設定することで，勾配方向に大きく降下する最適化を行います。  
さらに，ここでは体積制約（`constraint_mode: volume_penalty`）を考慮し，磁性体コア面積が全体の50%以下となるよう制約を加えます。  
```yaml
optimizer:
  name: gradient_update
  kwargs:
    constraint_mode: volume_penalty
    volume_frac_ulim: 0.5
    scaling_mode: sign
level_set_function:
  name: pyemsol_density
  kwargs:
    proj_method: heaviside5
    objective_type: W1
    torque_scale: 4.0
```

## optimization_problem.yaml（`Dmodel_SynRM_gradient`プロジェクト）
`pyemsol_density`を用いる場合，そちらの引数に設定した目的関数が内部的に計算されます。`optimization_problem.yaml`は`case_names`の設定，および`gradient_update`のムーブリミット減衰判定に利用されます。  
```yaml
case_names:
  - transient

objectives:
  - function_name: average_torque
    kwargs:
      torque_scale: 4.0
    coefficient: -1.0

ineq_constraints: []

eq_constraints: []

other_metrics:
  - function_name: average_torque
    kwargs:
      torque_scale: 4.0
```

## 最適化の実施例
今回は200イテレーションの最適化としました。  
下図は200イテレーションの形状の進化過程です（各イテレーションの最良形状をアニメーション化）。グレー部分は物性値が中間的な値を取る部分（グレースケール），黒は磁性体コアであり，回転子表面に磁性体コアが生成されていく様子が確認できます。
![Dmodel勾配最適化履歴](/img/Dmodel_SynRM_gradient_best_individuals.gif)

200イテレーション最適化完了後のGUIを以下に示します。  
94イテレーション目に最良値を記録し，以降はほぼ横ばいとなっており，十分に収束したと判断できます。  

![Dmodel勾配最適化履歴](/img/Dmodel_SynRM_gradient_check.png)