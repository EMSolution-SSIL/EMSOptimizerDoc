---
sidebar_position: 2
---

# Optimization Configuration
ここでは、`optimization.yaml`の内容を説明します。

## Format
```yaml
# Core Objects
evaluator:
  name: str
  kwargs: dict[str, Any]
optimizer:
  name: str
  kwargs: dict[str, Any]
level_set_function:
  name: str
  kwargs: dict[str, Any]
ems_shape_builder:
  name: str
  kwargs: dict[str, Any]
use_implicit_domain_meshing: bool

# Optimization Settings
num_iteration: int
enable_parallelization: bool
num_processes: int | null

# Output
output_dir: str
output_interval: int
output_control:
  best_individual:
    filename_base: str
    enabled: bool
    output_interval: int
  candidate:
    filename_base: str
    enabled: bool
    output_interval: int
  candidate_plot:
    filename_base: str
    enabled: bool
    output_interval: int
enable_progress_gui: bool
```

## Details
:::info
`evaluator`, `optimizer`, `level_set_function`, `ems_shape_builder`の実装例については各セクションを参照してください。  
また、`name`と`kwargs`の仕組みについては[How to Define Core Object](./user_define.md)を参照してください。
:::

### Core Objects
- `evaluator` ... 最適化で使用するEvaluator実装。
    - `name: str` ... 実装名
    - `kwargs: dict[str, Any]` ... キーワード引数
- `optimizer` ... 最適化で使用するEvaluator実装。
    - `name: str` ... 実装名
    - `kwargs: dict[str, Any]` ... キーワード引数
- `level_set_function` ... 最適化で使用するLevel set function実装。
    - `name: str` ... 実装名
    - `kwargs: dict[str, Any]` ... キーワード引数
- `ems_shape_builder` ... 最適化で使用するeMotorSolution Shape Builder実装。
    - `name: str` ... 実装名
    - `kwargs: dict[str, Any]` ... キーワード引数

### Optimization Settings
- `num_iteration: int` ... 最適化イテレーション数。
:::info
ここでは、「イテレーション」＝「`optimizer`が`Population`を`evaluator`に渡し、`evaluator`が評価し、`optimizer`が`Population`の更新処理をする一連のプロセス」と定義しています。
:::
- `enable_parallelization: bool`... 並列処理の有効化／無効化。
- `num_processes: int | null` ... 並列処理プロセス数。`null`の場合、PCのCPU数から自動的に設定される。

### Output
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