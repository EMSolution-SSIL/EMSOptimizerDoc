---
sidebar_position: 5
---

# Dmodel同期リラクタンスモータ最適化例
ここでは，`Dmodel_SynRM`プロジェクトの内容について紹介します。  
`Dmodel_SynRM`では同期リラクタンスモータ（SynRM）を想定し，永久磁石を含まないロータ領域の空気／磁性体コア分布の最適化を行います。  
通常のトルク特性改善の最適化に加え、eMachineSim連携による応力評価を組み込んだ最適化を紹介します。  

## ベースメッシュについて
`Dmodel_SynRM`では[多材料最適化例](./multi_material.md)と同様に，ベースメッシュとしてロータ部が永久磁石を含まず材料番号`20`（磁性体コア）のみからなるメッシュを使用し，ロータ部全域について空気／磁性体コア分布を最適化します。

## optimization.yaml（`Dmodel_SynRM`プロジェクト）
`optimization.yaml`では，回転子表面0.2mmを磁性体コアに固定するため，`level_set_function`に`ngnet_mixture`を指定し，表面0.2mmを除いた\[0.008, 0.0273\]の範囲にガウス基底関数を配置する設定とします。  
```yaml
level_set_function:
  name: ngnet_mixture
  kwargs:
    boundary_r: 0.0273
    sigma: 0.0010
    design_region: [[0.008, 0.0273], [0, 45.0]]
    coordinate: Polar
```

## 最適化の実施例
今回は200イテレーションの最適化としました（平均トルク最大化の単目的最適化）。  
200イテレーション最適化完了後のGUIを以下に示します。  
最適化の終盤まで目的関数値が改善し続けており，最終的に2層の大きなフラックスバリアを有する形状に収束しました。  

![DmodelSynRM最適化履歴](/img/Dmodel_SynRM_check.png)

## 応力評価を組み込んだ追加最適化
得られた最適形状は表面0.2mmのブリッジによって支持されています。  
このような薄い箇所は高速回転時に破断する恐れがあるため、実用上は応力分布を加味した最適化が望ましいと考えられます。  
ここでは、最適形状を初期形状とし、高速回転時（15000rpm）の最大応力値を制約条件とした最適化を行います。  

最適化問題（optimization_problem.yaml）は以下の通り設定します。  
```yaml
case_names:
  - transient
  - structural

objectives:
  - function_name: average_torque
    kwargs:
      torque_scale: 4.0
    normalization_const: 2.1
    coefficient: -1.0

ineq_constraints:
  - function_name: von_mises_stress
    case_name: structural
    kwargs:
      prohibit_seperated: True
    normalization_const: 200e6
    baseline: 200e6

eq_constraints:
  - function_name: num_connected_components
    case_name: transient
    kwargs:
      physical_tag: 20
    baseline: 1
```
まず、`case_names`に`structural`が追加されています。`Dmodel_SynRM`のプロジェクトにはすでに`structural`フォルダおよび入力ファイルが用意されています。この入力ファイルはeMachineSim用のファイルであり、解析条件が記述されています。  
`ineq_constraints`に`von_mises_stress`が指定されており、ここでは最大ミーゼス応力値が200MPa以下を制約条件としています。また、`eq_constraints`にはロータコアが一体となるよう、`num_connected_commponents`に`1`を制約しています。  

200イテレーションの追加最適化完了後のGUIを以下に示します。  
初期段階（右画像）では最大応力値（Metrics 2）が約254MPaであり制約を違反していますが、最適化後（左画像）は最大応力値が約199MPaに抑えられています。代わりに平均トルクが減少したものの、高速回転時の機械的な耐性を考慮しながら最適化ができました。

![DmodelSynRM追加最適化履歴](/img/Dmodel_SynRM_additional_check.png)