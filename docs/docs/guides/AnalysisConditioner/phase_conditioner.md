---
sidebar_position: 1
---

# phase_conditioner
電流位相角の動的設定を行う実装例。

## 概要
パラメータ$\boldsymbol{p}=\{p_0\}$から電流位相角を定義します。内部的にはpyemsolの入力jsonデータおよび解析ケース名を受け取り、解析ケース名が`transient`のときにjsonデータの位相角に当たる箇所に`scale`$ \times p_0$を加算します（`scale`はキーワード引数に受け取る位相角スケール）。

$p_0$: 電流位相角 \[deg\]。  

## 設定可能なキーワード引数一覧
`scale`: 電流位相角スケール。デフォルト値は`1.0`。
