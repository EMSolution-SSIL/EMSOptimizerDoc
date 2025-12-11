---
sidebar_position: 2
---

# 最適化の設定（optimization.yaml）
ここでは、`optimization.yaml`の内容を説明します。

## Format
凡例：`{設定項目名}: {型名} = デフォルト値`  
デフォルト値の無いものは設定必須項目。
```yaml
# Core Objects
evaluator:
  name: str
  kwargs: dict[str, Any] = {}
optimizer:
  name: str
  kwargs: dict[str, Any] = {}
analysis_conditioner: = None
  name: str
  kwargs: dict[str, Any] = {}
level_set_function: = None
  name: str
  kwargs: dict[str, Any] = {}
ems_shape_builder: = None
  name: str
  kwargs: dict[str, Any] = {}

# Optimization Settings
num_iteration: int
enable_parallelization: bool = False
num_processes: int | null = null
enable_dask_distribution: bool = False
dask_scheduler_url: str | null = null
num_chunks: int | null = null

# Output
resource_dir: str | null = null
output_dir: str
output_interval: int = 1
output_control:
  best_individual:
    filename_base: str
    enabled: bool = True
    output_interval: int = 1
  candidate:
    filename_base: str
    enabled: bool = True
    output_interval: int = 1
  candidate_plot:
    filename_base: str
    enabled: bool = True
    output_interval: int = 1
enable_progress_gui: bool = True
```

## Details
:::info
コアオブジェクトの実装例についてはユーザガイド内の各セクションを参照してください。  
また、`name`と`kwargs`の仕組みについては[発展的なトピック > コアオブジェクトの自作ページ](../advanced/user_define.md)を参照してください。
:::

### コアオブジェクト
- `evaluator` ... 最適化で使用するEvaluator実装。
    - `name: str` ... 実装名
    - `kwargs: dict[str, Any]` ... キーワード引数
- `optimizer` ... 最適化で使用するEvaluator実装。
    - `name: str` ... 実装名
    - `kwargs: dict[str, Any]` ... キーワード引数
- `analysis_conditioner` ... 最適化で使用するAnalysisConditioner実装。省略可能。
    - `name: str` ... 実装名
    - `kwargs: dict[str, Any]` ... キーワード引数
- `level_set_function` ... 最適化で使用するLevel set function実装。省略可能。
    - `name: str` ... 実装名
    - `kwargs: dict[str, Any]` ... キーワード引数
- `ems_shape_builder` ... 最適化で使用するeMotorSolution Shape Builder実装。省略可能。
    - `name: str` ... 実装名
    - `kwargs: dict[str, Any]` ... キーワード引数
:::info
後半3つのコアオブジェクト設定は省略可能です。使用したいもののみ設定してください。  
特に、`evaluator`にベンチマーク関数を使用した場合は3つすべて使用しないため省略可能です。
:::

### 最適化設定
- `num_iteration: int` ... 最適化イテレーション数。
:::info
ここでは、「イテレーション」＝「`optimizer`が`Population`を`evaluator`に渡し、`evaluator`が評価し、`optimizer`が`Population`の更新処理をする一連のプロセス」と定義しています。
:::
- `enable_parallelization: bool`... 並列処理の有効化／無効化。有効化時、形状最適化における形状評価を並列化する。
- `num_processes: int | null` ... 並列処理の有効化時、並列処理プロセス数。`null`の場合、PCのCPU数から自動的に設定される。
- `enable_dask_distribution: bool` ... pythonパッケージdask distributedによる分散処理の有効化／無効化。有効化時、形状最適化における形状評価を別途立ち上げたworkerノード群に分散する。
- `dask_scheduler_url: str | null` ... 分散処理の有効化時、workerノード群が接続されたschedulerノードへのURL。
- `num_chunks: int | null` ... 分散処理の有効化時、分散処理数。形状評価タスクは`num_chunks`に分割され、アクティブなworker群に分配される。さらに`enable_parallelization`が`True`ならば、worker内では`num_processes`の数だけプロセス並列して形状評価タスクを処理する。
:::info
分散処理の詳細については[発展的なトピック > 計算ノード間分散処理](../advanced/distribution.md)をご覧ください。
:::

### 出力設定
- `resource_dir: str | null` ... 形状最適化における作業用フォルダ名。中間ファイル等の出力先であり、eMotorSolution APIやpyemsolの計算結果が格納される。（形状最適化以外では設定不要）
:::info
分散処理時、`resource_dir`には最適化実行ノードおよびworkerノード群からアクセス可能な共有フォルダを指定します。
:::
- `output_dir: str` ... 最適化経過の出力先フォルダ名。
- `output_interval: int` ... GUIを含む出力全体のインターバル。1なら毎イテレーション、2なら2イテレーションに1回、...と出力します。
- `output_control` ... 各出力ファイルの設定。
  - `best_individual` ... エリート解（多目的最適化においては、パレート解）の情報。
    - `filename_base: str` ... ファイル名
    - `enabled: bool` ... 出力の有効化／無効化
    - `output_interval: int` ... 個別の出力インターバル
  - `candidate` ... 解析した全個体の情報。
    - `filename_base: str` ... ファイル名
    - `enabled: bool` ... 出力の有効化／無効化
    - `output_interval: int` ... 個別の出力インターバル
  - `candidate_plot` ... 各世代で生成された解候補ベクトルの分布プロット。
    - `filename_base: str` ... ファイル名
    - `enabled: bool` ... 出力の有効化／無効化
    - `output_interval: int` ... 個別の出力インターバル
- `enable_progress_gui: bool` ... GUIの有効化／無効化。