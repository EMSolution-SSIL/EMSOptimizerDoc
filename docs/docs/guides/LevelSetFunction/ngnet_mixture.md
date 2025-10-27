---
sidebar_position: 4
---

# NGnetMixture
[SimpleLevelSetRadius](ls_r.md)と[NGnet](ngnet.md)を組み合わせ、ある半径以内の領域についてNGnet関数を適用する実装例。

## 概要
寸法パラメータ$\boldsymbol{w}$、コンフィグ`boundary_r`と設計領域の各点の半径$r$に基づき、以下の値を返します。ただし、引数`inversed`が`True`のときは範囲が逆転します。
- $r > \text{boundary\_r}$ → 1（材料を`level 0`に固定）
- $r \leq \text{boundary\_r}$ → 寸法パラメータ$\boldsymbol{w}$を適用したNGnetの出力値

:::info
この実装例は例えば、「ロータのある半径から外側は材料を固定したい」場合、あるいは逆に「ロータの表面だけをNGnet on/off法の対象にしたい」場合などに利用することができます。  
実際の活用例は[Showcase](../../../showcase/IPM8P48S/pto.md)をご覧ください。
:::

## 設定可能なキーワード引数一覧
- `coordinate: str` ... NGnetの構築に用いる座標系。 "Cartesian"または"Polar"。
- `sigma: float` ... NGnetを構成するガウス基底関数の標準偏差。デフォルト値は`1`。
- `design_region: list[list[float, float], list[float, float]]` ... NGnetを構築する範囲（＝設計領域）。`coordinate`が`Cartesian`の場合は矩形領域$[[x_1, x_2], [y_1, y_2]]$、`Polar`の場合は扇状領域$[[r_1, r_2], [\theta_1, \theta_2]]$を設定します。
- `boundary_r: float` ... NGnet適用の境界となる半径。
- `inversed: bool`... NGnet適用範囲を逆転するかどうか。デフォルト値は`False`。
- `normalize_output: bool` ... NGnet出力を正規化するかどうか。`False`にすると、  
$y(\boldsymbol{w}, \boldsymbol{x}) = \sum_{i=1}^{N} w_i G_i(\boldsymbol{x}) \\$
となります。デフォルト値は`True`。