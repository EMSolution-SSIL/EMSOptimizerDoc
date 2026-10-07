---
sidebar_position: 5
---

# Dmodel混合変数最適化例
ここでは、`Dmodel_mixed_variables`プロジェクトの内容について紹介します。  
`Dmodel`プロジェクトと比較して、`Dmodel_mixed_variables`では`ga`optimizerとeMotorSolution連携を利用し，モータ構成を決定するカテゴリ変数・離散変数をNGnet on/off法の連続変数と同時に最適化します。

## machine.yaml（`Dmodel_mixed_variables`プロジェクト）
`machine.yaml`の基本設定は`Dmodel`プロジェクトと同じですが、eMotorSolutionと連携して最適化を行うため、`ems_project_filepath`コンフィグを追加します。  
`Dmodel_mixed_variables`プロジェクトにはすでにeMotorSolutionプロジェクトjsonファイルが含まれているため、そのファイルパスを指定します。  
```yaml
# ems functionality link
ems_project_filepath: "Path/To/EMSOptimizer/projects/Dmodel_mixed_variables/Dmodel.json"
```
:::info
上記のファイルパスはご使用のEMSOptimizerのインストール先に合わせて設定してください。
:::

## optimization.yaml（`Dmodel_mixed_variables`プロジェクト）
`optimization.yaml`の中身を確認します。  
ems_shape_builderは`Dmodel_mixed_builder`であり，これは1つのカテゴリ変数（永久磁石材料定義），1つの離散変数（コイル巻数），3つの連続変数（永久磁石寸法）を受け取り，eMotorSolution連携によって設定を行う実装例です。  
加えて，`Dmodel`プロジェクトと同様にNGnet on/off法の設定を行います。
```yaml
ems_shape_builder:
  name: Dmodel_mixed_builder
level_set_function:
  name: ngnet
  kwargs:
    sigma: 0.0020
    design_region: [[0.008, 0.0275], [0, 45.0]]
    coordinate: Polar
```

optimizerに`ga`を設定し，カテゴリ変数1，離散変数1を設定します。カテゴリ変数（永久磁石材料定義）は0（NdFeB, $B_r=1.25\text{T}$） or 1（FerriteMagnet，$B_r=0.40\text{T}$），離散変数（コイル巻数）は20~35の範囲を設定します。  
`bounds`には連続変数の範囲を指定します。ここでは，永久磁石寸法の上下限値を指定しています。
```yaml
optimizer:
  name: ga
  kwargs:
    seed: 42
    population_size: 30
    variable_type_counts:
      categorical: 1
      discrete: 1
    categorical_choices: [[0, 1]]
    discrete_values: [[20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]]
    bounds: [[10.0, 20.0], [3.0, 13.0], [1.5, 3.5]]
```

## optimization_problem.yaml（`Dmodel_mixed_variables`プロジェクト）
`optimization_problem.yaml`では，平均トルク最大化に加え，仮想的な永久磁石材料コスト（永久磁石面積×コスト係数）の最小化を設定しています。  
永久磁石材料として`FerriteMagnet`が指定されたときはコストに係数0.2を乗じます（`NdFeB`よりも低コストであることを反映するため）。  
また，制約条件には最大電圧値80.0V以下を設定しています。ロータ構造および巻数の最適化により，トルクとコストのバランスを取りつつ，電圧は想定する値を超えないようにします。
```yaml
objectives:
  - function_name: average_torque
    kwargs:
      torque_scale: 4.0
    normalization_const: 2.1
    coefficient: -0.8
  - function_name: magnet_cost
    kwargs:
      physical_tag: 50000
      ferrite_coef: 0.2
    normalization_const: 4.9975e-05
    coefficient: 0.2

ineq_constraints:
  - function_name: maximum_voltage
    normalization_const: 80.0
    baseline: 80.0
```

## 最適化の実施例
今回は50世代の最適化としました。最適化結果を以下に示します。平均トルク2.12Nm，永久磁石コスト33.4($\text{mm}^2$) ，最大電圧値76.9V。永久磁石材料にはNdFeBが選ばれ，巻数は最大値である35となりました。  
元々のDmodelよりも少ない永久磁石量で同等のトルクが発揮されています。ロータ構造に着目すると，永久磁石がDmodelよりも回転子表面に近づいており，主にマグネットトルクを活用するような形状になっていると推察されます。  
![Dmodel_mixed_variables最適化結果](/img/Dmodel_mixed_usual_best.png)

ここで，目的関数の設定を以下の通りに変更してみます。この設定下では`magnet_cost`の重みが大きいため，より永久磁石コストを低減する解が得られることが期待されます。
```yaml
objectives:
  - function_name: average_torque
    kwargs:
      torque_scale: 4.0
    normalization_const: 2.1
    coefficient: -0.5
  - function_name: magnet_cost
    kwargs:
      physical_tag: 50000
      ferrite_coef: 0.2
    normalization_const: 4.9975e-05
    coefficient: 0.5
```

設定変更後の結果を以下に示します。平均トルク0.87Nm，永久磁石コスト5.85($\text{mm}^2$) ，最大電圧値69.0V。永久磁石材料にはFerriteMagnetが選ばれ，巻数は最大値である35となりました。  
先ほどの結果と比較して，永久磁石材料にFerriteMagnetが選ばれたのが特徴として挙げられます。ロータ構造もそれに合わせて変化しており，リラクタンストルクの割合が大きいと推察されます。  
![Dmodel_mixed_variables最適化結果lowercost](/img/Dmodel_mixed_lowercost_best.png)
