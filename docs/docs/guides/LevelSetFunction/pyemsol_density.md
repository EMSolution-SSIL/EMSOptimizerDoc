---
sidebar_position: 6
---

# pyemsol_density
物性値の密度表現を取り扱うためのレベルセット実装です。

## 概要
pyemsolでは，目的関数の勾配を計算する際に物性値の密度表現を採用しています\[26\],\[30\]。  
設計変数として与えられたレベルセット値$\phi$を密度値$\rho$（\[0,1\]の値）に変換するため，$\phi=0$に関して対称なS字状の関数を適用します。
:::info
勾配ベーストポロジー最適化用のいくつかの機能は，`level_set_function`に`pyemsol_density`を設定することで有効になります。実際の使用例は[showcase > Dmodel > Dmodel勾配ベース最適化例（密度法）](../../../showcase/Dmodel/gradient_density.md)
:::

## 設定可能なキーワード引数一覧
- `proj_method: str` ... レベルセット値を密度値に変換する手法。`heaviside5`\[26\]または`sigmoid`\[30\]。デフォルトは`heaviside5`。
- `proj_half_width: float` ... `heaviside5`における遷移幅パラメータ値。デフォルトは`1.0`。
- `proj_beta: float` ... `sigmoid`における遷移幅パラメータ値。デフォルトは`1.0`。
- `proj_eta: float` ... 材料遷移の中間と見なすレベルセット値。デフォルトは`0`。
- `objective_type: str` ... 勾配を計算する目的関数の種類。`W1`: トルク，`W2`：トルク目標値からの二乗差\[26\]。デフォルトは`W1`。
- `torque_scale: float` ... トルクのスケール値。1/4モデルなら`4.0`を設定することでトルクの値をフルモデル換算する。デフォルトは`1.0`。
- `torque_target: float | null` ...`objective_type`が`W2`のとき，トルク目標値。