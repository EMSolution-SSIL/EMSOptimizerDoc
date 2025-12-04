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

# Output
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
- `enable_parallelization: bool`... 並列処理の有効化／無効化。
- `num_processes: int | null` ... 並列処理プロセス数。`null`の場合、PCのCPU数から自動的に設定される。

### 出力設定
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