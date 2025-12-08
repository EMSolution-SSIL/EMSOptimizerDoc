---
sidebar_position: 4
---

# 計算ノード間分散処理
## 概要
EMSOptimizerは並列処理に加え、複数の計算ノードを利用した分散処理に対応しています。  
分散処理にはDask Distributedパッケージ\[18\]が提供するscheduler / worker / client間連携を利用しています。
:::info
分散処理機能を利用するには以下の2点が必要です。詳細は[インストールガイド](../intro.md)をご覧ください。
- 各ノードに`emsopt_engine`および`emsopt_analyzer`のCodeMeterプロテクト版がインストールされていること
- 各ノードにCodeMeter Runtimeが導入およびアクティベーションされていること
:::
