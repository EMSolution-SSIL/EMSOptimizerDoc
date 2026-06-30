---
sidebar_position: 4
---

# Dmodel多材料最適化例
ここでは、`Dmodel_multi_material`プロジェクトの内容について紹介します。  
`Dmodel`プロジェクトと比較して、`Dmodel_multi_material`では多材料トポロジー最適化を行います。ここでは、ロータコアにおける空気・磁性体コア・永久磁石の3材料の分布を最適化します。

## ベースメッシュについて
`Dmodel_multi_material`プロジェクトではベースメッシュとして、ロータ部が永久磁石を含まず材料番号`20`（磁性体コア）のみからなるメッシュを使用します。  
後述の設計対象の設定において材料番号`20`を設定することで、ロータ部全域について多材料分布を最適化します。

![Dmodel multimaterial example](/img/Dmodel_multi_material_ex.png)

## machine.yaml（`Dmodel_multi_material`プロジェクト）
多材料最適化を設定するために、`machine.yaml` > `target_ids_and_onoff`に材料番号`20`, `50000`, `600000`の3材料を設定します。  
これにより、レベルセット関数`level_set_function`から3つの材料を設定することが可能となります。  
```yaml
target_ids_and_onoff:
  20:
    - 20
    - 50000
    - 600000
```

:::info
なお、3材料以上を指定時はImplicit Domain Meshing機能は使用不可です。
:::

## optimization.yaml（`Dmodel_multi_material`プロジェクト）
`optimization.yaml`では、レベルセット関数`level_set_function`に`ngnet_multi_material`を指定します。  
`ngnet_multi_material`は設計変数をもとに、設計領域内の各位置に3つのレベルを設定する実装例です。引数の詳細については[Docs > ユーザガイド > ngnet_multi_material](../../docs/guides/LevelSetFunction/ngnet_multi_material.md)をご参照ください。  
```yaml
level_set_function:
  name: ngnet_multi_material
  kwargs:
    sigma: 0.0020
    design_region: [[0.008, 0.0275], [0, 45.0]]
    coordinate: Polar
    angle_1: 240
    angle_2: 60
```
:::tip[`angle_1`, `angle_2`の設定]
`angle_1`, `angle_2`は磁性体コア、永久磁石に割り当てられる材料マップ上角度を表します。また、空気に割り当てられる角度は$360-240-60=60$\[deg\]です。  
`ngnet_multi_material`には「材料マップ上角度の割り当てが大きいほど設計領域上にその材料が出現しやすくなる」という特徴があります\[12\]。一般に永久磁石同期モータのロータは大部分が磁性体コアによって構成されるため、ここでは磁性体コアに対応する`angle_1`の角度を意図的に大きく設定しています。
:::

## optimization_problem.yaml（`Dmodel_multi_material`プロジェクト）
目的関数については`Dmodel`プロジェクトと変わらず、平均トルク最大化・トルクリプル最小化の設定となっています。  
変更点として、`ineq_constraint`に`material_area`（指定材料の面積）が追加されています。指定材料（`physical_tag`）には`50000`（永久磁石）を設定します。  
本最適化においては、永久磁石面積をオリジナルのDmodelの値（$4.9975\times10^{-5}\text{m}^2$）以下に制約することで、使用する永久磁石量が同等以下という条件下で最適な材料分布を得ることを目指します。
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
    coefficient: 0.1

ineq_constraints:
  - function_name: material_area
    kwargs:
      physical_tag: 50000
    baseline: 4.9975e-05
```

## 最適化の実施例
今回は200イテレーションの最適化としました。  
下図は200イテレーションの形状の進化過程です（各イテレーションの最良形状をアニメーション化）。空気／磁性体コア／永久磁石からなる分布が変化しつつ、単層の永久磁石＋フラックスバリア形状に収束していく様子が分かります。  
![Dmodelマルマテ最適化履歴](/img/Dmodel_multi_material_best_individuals.gif)

200イテレーション最適化完了後のGUIを以下に示します。  
他の最適化事例より収束が遅いものの、130イテレーション以降は目的関数値がほぼ横ばいとなっており、最適化が収束したと判断できます。  
GUIの図に示しているのが最良形状です（$T_\text{avg}$=2.5183Nm, $T_\text{rip}$=24.318%, 永久磁石面積$S=4.7543\times10^{-5}\text{m}^2$）。[基本の最適化](./basic.md)と比較して、特に平均トルクに大きな向上が見られます。永久磁石モータの多材料最適化では永久磁石の修正が可能なため、特に平均トルクの改善に寄与しやすいことが経験的に知られています。また、本事例とは反対に、平均トルク一定以上の制約を与えて永久磁石面積を最小化する最適化計算も可能です。
![Dmodelマルマテ最適化履歴](/img/Dmodel_multi_material_check.png)