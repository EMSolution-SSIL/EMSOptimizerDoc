---
sidebar_position: 7
---

# Dmodel勾配ベース最適化例（レベルセット法）
ここでは，`Dmodel_SynRM_gradient_ls`プロジェクトの内容について紹介します。  
`Dmodel_SynRM_gradient_ls`では同期リラクタンスモータ（SynRM）を想定し，勾配ベースのトポロジー最適化手法（レベルセット法）によって最適化を行います。

## ベースメッシュについて
`Dmodel_SynRM_gradient_ls`では，下図のように2層フラックスバリアを有するロータを初期形状として，その材料境界を平滑化ヘビサイド関数に基づくレベルセット法\[27\]によって最適化します。

![Dmodel SynRM example](/img/Dmodel_SynRM_gradient_ls_ex.png)

## machine.yaml（`Dmodel_SynRM_gradient_ls`プロジェクト）
`machine.yaml`では，初期形状の各位置におけるレベルセット関数値（符号付距離関数）を計算するため，`calc_levelset_init`を`True`に設定します。これは設計変数の初期値として用いられます。  
また，レベルセット法においては，各設計変数を適切に再初期化する必要があることが知られています。本プロジェクトでは5世代ごとに再初期化を行います。これらのコンフィグの詳細については[機器設定ページ](../../docs/guides/machine_config.md)をご覧ください。
```yaml
calc_levelset_init: True
levelset_reinit_interval: 5
levelset_reinit_weight: 0.2
```

なお，レベルセット法においてもImplicit Domain Meshingが適用可能です\[29\],\[30\]。これにより，レベルセット値の零等位面に沿った明瞭な材料境界を有するメッシュが得られます。  
Implicit Domain Meshingを有効化するには[`Dmodel`プロジェクトの例](./basic.md)と同様に`use_implicit_domain_meshing`を`True`に変更します。

## optimization.yaml（`Dmodel_SynRM_gradient_ls`プロジェクト）
`optimization.yaml`では，レベルセット関数`level_set_function`に`pyemsol_density`を指定します。これにより，目的関数`W1`（トルク）に関する勾配計算がEMSOptimizer内部で行われます。  
計算した勾配は`optimizer`の`gradient_update`の中で設計変数（ここでは，設計領域内の各要素におけるレベルセット関数値）の更新に利用されます。  
また，今回は初期形状における符号付距離関数値を設計変数の初期値に採用するため，`init_value_filepath`に初期値csvファイルへのパスを格納します。符号付距離関数値はmmオーダーのため，`move_limit`は`0.0001`とします。また，境界近傍の変化のみ許容するため，`pyemsol_density` > `proj_half_width`は`0.0005`としています。これにより，最適化の各時点における材料境界（＝零等位面）から+-0.5mmの範囲内のみが変化します。  
:::info
`level_set_function`が`pyemsol_density`のとき，最適化実行前にdry run（設計領域情報の取得等のための空解析）が実行されます。レベルセット関数値の初期計算もdry runによって行われます。  
dry runの結果は`resource_dir`内の`dry_run`フォルダに格納されています。
:::

```yaml
evaluator:
  name: pyemsol_shape_evaluator
optimizer:
  name: gradient_update
  kwargs:
    init_value_filepath: "path/to/EMSOptimizer/projects/Dmodel_SynRM_gradient_ls/optimization_studies/default/resources/dry_run/transient/design_ls_parameters.csv"
    diffusion_coef: 0.0  # 拡散無し
    move_limit: 0.0001
level_set_function:
  name: pyemsol_density
  kwargs:
    proj_method: heaviside5
    proj_half_width: 0.0005
    objective_type: W1
    torque_scale: 4.0
```

以下は，初期形状の符号付距離関数値に`heaviside5`を適用して得られた材料密度値を可視化した図です（赤：磁性体コア，青：空気）。密度値が中間になっている材料境界近辺で変化が発生し得ます。  
なお，最適化中に再初期化が何度か発生するため，そのタイミングで材料境界が再計算され，その境界に合わせて材料境界近辺も再計算されます。  
![Levelset values example](/img/levelset_values_ex.png)

## optimization_problem.yaml（`Dmodel_SynRM_gradient_ls`プロジェクト）
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
今回は50イテレーションの最適化としました。  
下図は50イテレーションの形状の進化過程です（各イテレーションの最良形状をアニメーション化）。グレー部分は物性値が中間的な値を取る部分（グレースケール），黒は磁性体コアであり，回転子表面が徐々に変化する様子が分かります。
![Dmodel勾配LS最適化履歴](/img/ls_best_individuals.gif)

50イテレーション最適化完了後のGUIを以下に示します。23イテレーション目に最良値を記録しました。
初期形状と比較すると，平均トルクが0.5583Nm → 0.6808Nmと向上していることが分かります。  

![Dmodel勾配LS最適化履歴](/img/ls_GUI.png)