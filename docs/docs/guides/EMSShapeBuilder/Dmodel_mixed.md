---
sidebar_position: 3
---

# Dmodel_mixed_builder
`Dmodel_mixed_variabls`プロジェクト用の，Dmodelモータ構成を編集する実装例です。

## 概要
カテゴリ変数から永久磁石材料（`NdFeB` / `FerriteMagnet`）を，離散変数からコイル巻数を定義します。  
同時に，3次元の寸法パラメータから永久磁石形状を定義します。
:::info
本実装例を適用するためには、使用するeMotorSolutionプロジェクトにHoleMagnet Type 51が設定されている必要があります。  
寸法パラメータ情報についてはeMotorSolutionのドキュメントをご覧ください。
:::

## 設定可能なキーワード引数一覧
なし
