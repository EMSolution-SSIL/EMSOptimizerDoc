---
sidebar_position: 4
---

# 計算ノード間分散処理
## 概要
EMSOptimizerは形状最適化において、形状評価の並列処理に加え、複数の計算ノードを利用した分散処理に対応しています。  
分散処理にはDask Distributedパッケージ\[18\]が提供するclient / scheduler / worker間連携を利用しています。分散処理機能を有効化するには、`optimization.yaml` > `enable_dask_distribution`を`True`に設定します。
:::info
分散処理機能を利用するには以下の2点が必要です。
- 各ノードにEMSOptimizerの実行環境が導入されていること
- CodeMeter Runtimeによるライセンス設定が各ノードに行われていること
:::

## 計算ノード構成図
![dask分散_計算ノード構成図](/img/dask_distributed.png)
- EMSOptimizerでは、`run`コマンドによって形状最適化を実行した計算ノードがclientノードとなります。
- schedulerノードとworkerノードは別途配置します。workerノード群はschedulerノードに接続します。
- 分散処理有効化時、
    - clientノードが形状最適化を実行すると、schedulerノードに形状評価タスクが渡されます。
    - schedulerノードは渡されたタスクを分割してworkerノードに分配します。
    - 各workerノード内ではmultiprocessingによってタスクをさらに分割して並列処理します。
        - したがって、総並列処理数は`（workerノードの数）×（各workerノード内での並列処理数）`となります。
:::info
各ノードは同一の計算機上の個別のプロセスであっても構いません。例えば、clientノードとschedulerノードは同一計算機上で別プロセスとして立ち上げることができます。
:::

## 分散処理の実行
### 環境設定
- schedulerノードに以下の環境変数を設定します。  
    - 環境変数名：`PYTHONPATH`
    - 設定値：`{ノードに配置したEMSOptimizerフォルダへのパス}`
        - pythonが`EMSOptimizer`のスクリプト群を検索するのに必要です。
- workerノードに以下の環境変数を設定します。
    - 環境変数名：`PYTHONPATH`
    - 設定値：`{ノードに配置したEMSOptimizerフォルダへのパス}`
        - pythonが`EMSOptimizer`のスクリプト群を検索するのに必要です。
    - 環境変数名：`DASK_DISTRIBUTED__WORKER__DAEMON`
    - 設定値：`False`
        - Dask Distributedによって起動されるworkerプロセスを非デーモン化します。workerノード内で並列処理を行うのに必要です。

### 実行フロー
1. schedulerノードにて以下のコマンドを実行し、schedulerを起動します。
```sh
dask scheduler
```
- scheduler起動時、以下のログが表示されるので{}内の情報を記録しておきます（2.以降の手順にて使用します）。
```sh
Scheduler at: tcp://{schedulerノードのIPアドレス}:{ポート番号}
```
2. workerノードにて以下のコマンドを実行し、workerを起動します。
```sh
dask worker tcp://{schedulerノードのIPアドレス}:{ポート番号} --nworkers 1 --nthreads 1
```
3. clientノード上の実行したいプロジェクトにおいて、`optimization.yaml`に以下の設定を行います。  
- `enable_dask_distribution: True`
- `dask_scheduler_url: tcp://{schedulerノードのIPアドレス}:{ポート番号}`
- `num_chunks: {タスク分割数}`または`null`
    - 形状評価タスクは`num_chunks`に分割され、アクティブなworkerノード群に分配されます。
    - `null`のとき、`タスク分割数＝アクティブなworkerノード数`に自動設定されます。
- `enable_parallelization: True`または`False`
    - `num_chunks`に分割された形状評価タスクをworkerノード内で並列処理するには、`True`に設定します。
- `num_processes: {並列処理数}`または`null`
    - workerノードでは、`num_processes`の数だけプロセス並列して形状評価タスクが処理されます。
    - したがって、総並列処理数は`num_chunks`×`num_processes`となります。
- `resource_dir: {共有フォルダへのパス}`
    - 最適化の中間ファイル等は`resource_dir`に集約されるため、`resource_dir`にはclient, schedulerおよびworkerノード群の全てからアクセス可能な共有フォルダを指定します。
4. clientノードから、`run`コマンドによって最適化を実行します。
    - 形状最適化中、形状評価タスクが自動的にworkerノード群に分配されます。
