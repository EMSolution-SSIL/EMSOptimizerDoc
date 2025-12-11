---
sidebar_position: 4
---

# 計算ノード間分散処理
## 概要
EMSOptimizerは形状最適化において、形状評価の並列処理に加え、複数の計算ノードを利用した分散処理に対応しています。  
分散処理にはDask Distributedパッケージ\[18\]が提供するscheduler / worker / client間連携を利用しています。
:::info
分散処理機能を利用するには以下の2点が必要です。詳細は[インストールガイド](../intro.md)をご覧ください。
- 各ノードに`emsopt_engine`および`emsopt_analyzer`のCodeMeterプロテクト版がインストールされていること
- 各ノードにCodeMeter Runtimeが導入およびアクティベーションされていること
:::

## 計算ノード構成図
TBD

## 実行手順
1. ネットワーク内の任意の計算ノード上にschedulerを起動します。
2. ネットワーク内にある、実際に最適化計算を分散させたい計算ノード群上にworkerを起動します。
3. `optimization.yaml`に以下の設定を行います：  
- `enable_dask_distribution: True`
- `dask_scheduler_url: {tcp://{schedulerノードのIPアドレス}:{ポート番号}}`
- `num_chunks: {分散処理数}`または`null`
    - 形状評価タスクは`num_chunks`に分割され、アクティブなworker群に分配されます。
    - `null`のとき、`分散処理数＝workerノード数`に自動設定されます。
- `enable_parallelization: True`または`False`
    - `num_chunks`に分割された形状評価タスクをworkerノード内で並列処理するには、`True`に設定します。
- `num_processes: {並列処理数}`または`null`
    - workerノードでは、`num_processes`の数だけプロセス並列して形状評価タスクが処理されます。
    - したがって、総並列処理数は`num_chunks`×`num_processes`となります。
4. ネットワーク内の任意の計算ノードから、`run`コマンドによって最適化を実行します。
