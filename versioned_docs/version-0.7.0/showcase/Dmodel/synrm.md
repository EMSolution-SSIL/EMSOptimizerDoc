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
