---
sidebar_position: 5
---

# NGnetMultiMaterial
3材料最適化用のNGnet実装です。多材料表現型のNGnet on/off法\[3\]において形状表現に用いられます。  
原理的には3材料からなる任意の分布を表現可能です\[12\], \[17\]。

## 概要
多材料表現型のNGnet on/off法においては設計領域内の各位置$\boldsymbol{x}$において、2通りの重み係数（＝設計変数）$\boldsymbol{w}_{1}, \boldsymbol{w}_{2}$から、$y_{1} = y(\boldsymbol{w}_{1}, \boldsymbol{x}), y_{2} = y(\boldsymbol{w}_{2}, \boldsymbol{x})$を計算します（$y$はNGnet関数）。  
そして、$y_{1}, y_{2}$の値を材料マップに当てはめることで、各位置における材料種を決定します。  
本実装例では文献\[12\], \[17\]に倣い、下図の材料マップを用いて材料種を決定します。すなわち、$\theta^{\text{mat}}(\boldsymbol{x}) = \text{arctan2}(y_{2}, y_{1})$の値によって`level 1` ~ `level 3`の各材料種を割り当てます。

![ガウス基底関数の配置](/img/NGnet_multi_material_map.png)

:::info
本実装例は`machine.yaml` > `target_ids_and_onoff`に`id for level 1`~`id for level 3`が設定されていることを前提としています。  
詳細は[ユーザガイド > 機器設定（machine.yaml）](../machine_config.md)を参照してください。
:::
:::tip 多材料表現の活用例
このような多材料表現は設計対象が複数の材料種から構成される場合に活用できます。  
例えば、永久磁石同期モータのロータトポロジー最適化への応用例は[Showcase](../../../showcase/Dmodel/multi_material.md)にて紹介されています。
:::

## 設定可能なキーワード引数一覧
- `coordinate: str` ... NGnetの構築に用いる座標系。 "Cartesian"または"Polar"。
- `sigma: float` ... NGnetを構成するガウス基底関数の標準偏差。デフォルト値は`1`。
- `design_region: list[list[float, float], list[float, float]]` ... NGnetを構築する範囲（＝設計領域）。`coordinate`が`Cartesian`の場合は矩形領域$[[x_1, x_2], [y_1, y_2]]$、`Polar`の場合は扇状領域$[[r_1, r_2], [\theta_1, \theta_2]]$を設定します。
- `distance_factor: float` ... ガウス基底関数同士をどの程度の間隔で配置するかを決める値。1より小さいほど、ガウス基底関数同士が重なるように配置される。デフォルト値は`0.8`。
- `eliminate_bases_on_edge: bool` ... 領域端のガウス基底関数を排除するかどうか。デフォルト値は`False`。
- `normalize_output: bool` ... NGnet出力を正規化するかどうか。`False`にすると、  
$y(\boldsymbol{w}, \boldsymbol{x}) = \sum_{i=1}^{N} w_i G_i(\boldsymbol{x}) \\$
となります。デフォルト値は`True`。
- `angle_1: float` ... Level 1 に割り当てられる材料マップ上角度$\theta_{1}^{\text{mat}}$\[deg\]。デフォルト値は`120.0`。
- `angle_2: float` ... Level 2 に割り当てられる材料マップ上角度$\theta_{2}^{\text{mat}}$\[deg\]。デフォルト値は`120.0`。
:::info
Level 3に割り当てられる角度は$\theta_{3}^{\text{mat}} = 360 - \theta_{1}^{\text{mat}} - \theta_{2}^{\text{mat}}$\[deg\]となります。
:::
:::tip `angle_1`, `angle_2`の設定
`ngnet_multi_material`には「材料マップ上角度の割り当てが大きいほど設計領域上にその材料が出現しやすくなる」という特徴があります\[12\]。  
したがって、平均的に多くの割合を占める材料に対応する角度は大き目に設定することで、最適化の収束性が良くなる可能性があります。  
ただし、最適化の経過によっては材料マップ上角度に係わらず、目的関数を低減するよう材料分布に収束することが経験的に知られています。
:::