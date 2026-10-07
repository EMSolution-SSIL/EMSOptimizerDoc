---
sidebar_position: 5
---

# EMSOptimizer Python API

## 概要

v0.7.0以降、主要なコマンド（`run`コマンドなど）はCLIとPython APIの両方の方式で提供されています。
このページでは、`manager/emsopt_api.py`に定義されているPython APIを紹介します。
:::info
EMSOptimizerのEMSOptFree部は公開されているため、ユーザはAPIを利用せずに各種処理を直接呼び出すことも可能です。  
しかしながら、EMSOptimizer標準のワークフローはこのAPIを経由して駆動されることを期待しているため、安定した動作のためにはAPIを操作の窓口として利用することを推奨します。  
:::

`EMSOptimizerClient`クラスは、project / study / run のライフサイクルをPythonから扱うためのAPIです。
CLIはこのクライアントに処理を委譲しており、外部スクリプトからも同じ実行管理経路を利用できます。

## import

```python
from manager.emsopt_api import EMSOptimizerClient
```

## クイックリファレンス

| API | 種別 | 主な用途 | 戻り値 |
|---|---|---|---|
| `EMSOptimizerClient` | class | project / study / run を操作するクライアント | `EMSOptimizerClient` |
| `create_manager` | method | セットアップ済みmanagerを生成する | `ManagerHandle` |
| `check` | method | 保存済みrunを読み込み、確認用GUI処理を起動する | `OptimizationCommandResult` |
| `run` | method | 指定studyの最適化を実行する | `OptimizationCommandResult` |
| `batch_run` | method | 同一studyを複数回連続実行する | `list[OptimizationCommandResult]` |
| `sample` | method | LHSサンプル群を評価する | `OptimizationCommandResult` |
| `start_background_run` | method | `run`を別プロセスで開始する | `dict` |
| `start_background_batch_run` | method | `batch_run`を別プロセスで開始する | `dict` |
| `start_background_sample` | method | `sample`を別プロセスで開始する | `dict` |
| `background_job_status` | method | バックグラウンドジョブの状態を取得する | `dict` |
| `list_background_jobs` | method | バックグラウンドジョブ一覧を取得する | `list[dict]` |
| `pause_background_job` | method | 指定ジョブにpause要求を出す | `dict` |
| `resume_background_job` | method | 指定ジョブにresume要求を出す | `dict` |
| `stop_background_job` | method | 指定ジョブにstop要求を出す | `dict` |

## データモデル

### `ManagerHandle`

`create_manager()` が返す、生成済み `OptimizationManager` と解決済みコンテキストの入れ物です。

| フィールド | 型 | 説明 |
|---|---|---|
| `project_name` | `str` | 対象project名 |
| `study_name` | `str` | 解決済みstudy名 |
| `manager` | `OptimizationManager` | セットアップ済みmanager |
| `restart_target_study_name` | `str \| None` | restart先study名。未設定時は `None` |

### `OptimizationCommandResult`

`run` / `check` / `sample` / `batch_run` が返す実行結果です。

| フィールド | 型 | 説明 |
|---|---|---|
| `project_name` | `str` | 対象project名 |
| `study_name` | `str` | 実際に利用されたstudy名 |
| `status` | `str` | `completed` / `stopped` / `failed` などの状態 |
| `manager` | `OptimizationManager` | 実行に使われたmanager |
| `run_id` | `str \| None` | `run_0001` 形式のrun ID。該当しない場合は `None` |
| `run_summary_dir` | `Path \| None` | runの正本成果物ディレクトリ |
| `restart_selection` | `RestartSelection \| None` | GUIから返されたrestart選択 |
| `failure_reason` | `str \| None` | 失敗時の理由 |

## 共通仕様

### project / study の解決

`project_root` を指定した場合、projectは `project_root/project_name` として解決されます。
未指定の場合は既定の解決（実行時ディレクトリ直下`project`フォルダ）に従います。

`project_name` は識別子として扱われ、絶対パスやパス区切りを含む値は拒否されます。

### run summary ディレクトリ

通常run / sample / batch_runでは、runごとに次のsummaryディレクトリが作られます。

```text
<project_root>/<project_name>/summary/optimization_studies/<study_name>/runs/<run_id>/
```

`run_id` は `run_0001` 形式で連番割り当てされます。

### run状態

実行中、完了、停止、失敗の状態は `run_info.yaml` に書き込まれます。

| 状態 | 書き込まれるタイミング |
|---|---|
| `running` | run ID割り当て直後 |
| `completed` | manager処理とfinalizeが正常終了したとき |
| `stopped` | 協調停止要求により終了したとき |
| `failed` | 例外が発生したとき |

### コールバック

`run_started_callback` は、run ID と run summaryディレクトリが確定した直後に呼ばれます。
バックグラウンドジョブでは、現在実行中のrun IDを `job_info.yaml` に反映する用途で使われます。

```python
def on_started(run_id: str, run_summary_dir: Path) -> None: ...
```

### 制御プロバイダ

`control_provider` は、`OptimizationManager` へ渡される外部制御用オブジェクトです。
バックグラウンドジョブでは `FileJobControl` が使われ、pause / stop要求をファイル経由でmanagerへ伝えます。

`batch_run()` では、新しいrunを開始する前に `control_provider.stop_requested()` を確認します。

## API詳細

### `EMSOptimizerClient`

project / study / run の実行管理を行うクライアントです。

```python
EMSOptimizerClient(*, project_root: str | Path | None = None)
```

#### 引数

| 名前 | 型 | デフォルト | 必須 | 説明 |
|---|---|---:|:---:|---|
| `project_root` | `str \| Path \| None` | `None` | No | projectを探索するルートディレクトリ |

#### 戻り値

| 型 | 説明 |
|---|---|
| `EMSOptimizerClient` | project / study / run を操作するクライアント |

#### 使用例

```python
client = EMSOptimizerClient(project_root="projects")
```

### `create_manager`

対象studyの `OptimizationManager` を生成し、外部スクリプトから直接操作できる形で返します。

```python
create_manager(
    project_name: str,
    study_name: str | None = None,
    *,
    restart_target_study_name: str | None = None,
) -> ManagerHandle
```

#### 引数

| 名前 | 型 | デフォルト | 必須 | 説明 |
|---|---|---:|:---:|---|
| `project_name` | `str` | なし | Yes | 対象project名 |
| `study_name` | `str \| None` | `None` | No | 対象study名。`None` の場合は default study が解決される |
| `restart_target_study_name` | `str \| None` | `None` | No | restart先study名。`None` の場合は `optimization.yaml` から解決される |

#### 戻り値

| 型 | 説明 |
|---|---|
| `ManagerHandle` | 生成済みmanagerと解決済みコンテキスト |

#### 副作用

- `setup_project_files()` で依存注入を構築します。
- 取得したmanagerに `set_run_context(project_name, study_name, restart_target_study_name)` を設定します。

### `run`

指定studyの最適化を実行します。

```python
run(
    project_name: str,
    study_name: str | None = None,
    *,
    control_provider: object | None = None,
    disable_progress_gui: bool = False,
    run_started_callback: Callable[[str, Path], None] | None = None,
) -> OptimizationCommandResult
```

#### 引数

| 名前 | 型 | デフォルト | 必須 | 説明 |
|---|---|---:|:---:|---|
| `project_name` | `str` | なし | Yes | 対象project名 |
| `study_name` | `str \| None` | `None` | No | 対象study名。`None` の場合は default study が解決される |
| `control_provider` | `object \| None` | `None` | No | pause / stop などの外部制御をmanagerへ渡すためのオブジェクト |
| `disable_progress_gui` | `bool` | `False` | No | `True` の場合、progress GUIを無効化する |
| `run_started_callback` | `Callable[[str, Path], None] \| None` | `None` | No | run ID とsummaryディレクトリ確定直後に呼ばれるコールバック |

#### 戻り値

| 型 | 説明 |
|---|---|
| `OptimizationCommandResult` | 実行状態、manager、run ID、成果物ディレクトリなどを含む結果 |

#### 例外

| 例外 | 条件 |
|---|---|
| `Exception` | 実行中に例外が発生した場合。`run_info.yaml` に `failed` と `failure_reason` を書いたうえで再送出される |

#### 処理の流れ

1. project / study / restart先studyを解決します。
2. `OptimizationManager` を生成します。
3. run ID と run summary ディレクトリを割り当てます。
4. `run_info.yaml` に `running` を書き込みます。
5. `manager.run_optimization(str(run_summary_dir))` を実行します。
6. 成果物をfinalizeし、`completed` または `stopped` を書き込みます。
7. GUIから `RestartSelection` が返された場合は、restart先studyへ切り替えて再実行します。

#### 補足

`disable_progress_gui=True` の場合、`manager.config.enable_progress_gui` が `False` に設定されます。
バックグラウンド実行では、GUIを開かないためにこの設定が使われます。

### `check`

保存済みrunの結果を読み込み、確認用GUI処理を起動します。

```python
check(
    project_name: str,
    study_name: str | None = None,
    run_id: str | None = None,
) -> OptimizationCommandResult
```

#### 引数

| 名前 | 型 | デフォルト | 必須 | 説明 |
|---|---|---:|:---:|---|
| `project_name` | `str` | なし | Yes | 対象project名 |
| `study_name` | `str \| None` | `None` | No | 対象study名。`None` の場合は default study が解決される |
| `run_id` | `str \| None` | `None` | No | 対象run ID。`None` の場合は `latest.yaml` が指す最新runを使う |

#### 戻り値

| 型 | 説明 |
|---|---|
| `OptimizationCommandResult` | 確認対象のrun情報とmanagerを含む結果 |

#### 例外

| 例外 | 条件 |
|---|---|
| `RuntimeError` | 対象runが見つからない、または `run_id` が不正な場合 |

#### 副作用

- manager生成時は `setup_project_files(..., for_check=True)` を使います。
- GUIから `RestartSelection` が返された場合は、restart先studyを反映して通常の `run()` を開始します。

#### 補足

明示的に `run_id` を指定しても `latest.yaml` は更新されません。

### `sample`

LHSサンプル群を評価し、通常runと同じ保存契約で永続化します。

```python
sample(
    project_name: str,
    num_sample: int,
    study_name: str | None = None,
    *,
    chunk_size: int | None = None,
    control_provider: object | None = None,
    run_started_callback: Callable[[str, Path], None] | None = None,
) -> OptimizationCommandResult
```

#### 引数

| 名前 | 型 | デフォルト | 必須 | 説明 |
|---|---|---:|:---:|---|
| `project_name` | `str` | なし | Yes | 対象project名 |
| `num_sample` | `int` | なし | Yes | 評価するLHSサンプル数 |
| `study_name` | `str \| None` | `None` | No | 対象study名。`None` の場合は default study が解決される |
| `chunk_size` | `int \| None` | `None` | No | サンプル評価時のchunkサイズ |
| `control_provider` | `object \| None` | `None` | No | pause / stop などの外部制御をmanagerへ渡すためのオブジェクト |
| `run_started_callback` | `Callable[[str, Path], None] \| None` | `None` | No | run ID とsummaryディレクトリ確定直後に呼ばれるコールバック |

#### 戻り値

| 型 | 説明 |
|---|---|
| `OptimizationCommandResult` | サンプル評価の状態、manager、run ID、成果物ディレクトリなどを含む結果 |

#### 例外

| 例外 | 条件 |
|---|---|
| `Exception` | 評価中に例外が発生した場合。`run_info.yaml` に `failed` と `failure_reason` を書いたうえで再送出される |

#### 副作用

- run ID を割り当てます。
- `run_info.yaml` に `running` を書き込みます。
- `manager.sample(num_sample, str(run_summary_dir), chunk_size=chunk_size)` を実行します。
- 成功時はfinalize後に `completed` または `stopped` を書き込みます。

### `batch_run`

同一studyを複数回、独立したrunとして連続実行します。

```python
batch_run(
    project_name: str,
    num_runs: int,
    study_name: str | None = None,
    *,
    stop_on_error: bool = False,
    control_provider: object | None = None,
    run_started_callback: Callable[[str, Path], None] | None = None,
) -> list[OptimizationCommandResult]
```

#### 引数

| 名前 | 型 | デフォルト | 必須 | 説明 |
|---|---|---:|:---:|---|
| `project_name` | `str` | なし | Yes | 対象project名 |
| `num_runs` | `int` | なし | Yes | 連続実行するrun数 |
| `study_name` | `str \| None` | `None` | No | 対象study名。`None` の場合は default study が解決される |
| `stop_on_error` | `bool` | `False` | No | `True` の場合、途中runの失敗時に例外を再送出して停止する |
| `control_provider` | `object \| None` | `None` | No | pause / stop などの外部制御をmanagerへ渡すためのオブジェクト |
| `run_started_callback` | `Callable[[str, Path], None] \| None` | `None` | No | run ID とsummaryディレクトリ確定直後に呼ばれるコールバック |

#### 戻り値

| 型 | 説明 |
|---|---|
| `list[OptimizationCommandResult]` | 各runの実行結果 |

#### 例外

| 例外 | 条件 |
|---|---|
| `ValueError` | `num_runs < 1` の場合 |
| `Exception` | `stop_on_error=True` で途中runが失敗した場合 |

#### 副作用

- 各runで新しい `OptimizationManager`、run ID、run summaryディレクトリを作成します。
- progress GUI は常に無効化されます。
- `control_provider.stop_requested()` が `True` の場合、新しいrunの開始前に中断します。

#### 補足

途中runが失敗しても `stop_on_error=False` なら失敗結果を `results` に追加し、次runへ進みます。

## バックグラウンドジョブAPI

### `start_background_run`

`run` を別プロセスで開始し、ジョブ情報を辞書で返します。

```python
start_background_run(
    project_name: str,
    study_name: str | None = None,
) -> dict
```

#### 引数

| 名前 | 型 | デフォルト | 必須 | 説明 |
|---|---|---:|:---:|---|
| `project_name` | `str` | なし | Yes | 対象project名 |
| `study_name` | `str \| None` | `None` | No | 対象study名 |

#### 戻り値

| 型 | 説明 |
|---|---|
| `dict` | 開始したバックグラウンドジョブの情報 |

### `start_background_batch_run`

`batch_run` を別プロセスで開始します。

```python
start_background_batch_run(
    project_name: str,
    num_runs: int,
    study_name: str | None = None,
    *,
    stop_on_error: bool = False,
) -> dict
```

#### 引数

| 名前 | 型 | デフォルト | 必須 | 説明 |
|---|---|---:|:---:|---|
| `project_name` | `str` | なし | Yes | 対象project名 |
| `num_runs` | `int` | なし | Yes | 連続実行するrun数 |
| `study_name` | `str \| None` | `None` | No | 対象study名 |
| `stop_on_error` | `bool` | `False` | No | `True` の場合、途中runの失敗時に停止する |

#### 戻り値

| 型 | 説明 |
|---|---|
| `dict` | 開始したバックグラウンドジョブの情報 |

#### 例外

| 例外 | 条件 |
|---|---|
| `ValueError` | `num_runs < 1` の場合 |

### `start_background_sample`

`sample` を別プロセスで開始します。

```python
start_background_sample(
    project_name: str,
    num_sample: int,
    study_name: str | None = None,
    *,
    chunk_size: int | None = None,
) -> dict
```

#### 引数

| 名前 | 型 | デフォルト | 必須 | 説明 |
|---|---|---:|:---:|---|
| `project_name` | `str` | なし | Yes | 対象project名 |
| `num_sample` | `int` | なし | Yes | 評価するLHSサンプル数 |
| `study_name` | `str \| None` | `None` | No | 対象study名 |
| `chunk_size` | `int \| None` | `None` | No | サンプル評価時のchunkサイズ |

#### 戻り値

| 型 | 説明 |
|---|---|
| `dict` | 開始したバックグラウンドジョブの情報 |

#### 例外

| 例外 | 条件 |
|---|---|
| `ValueError` | `num_sample < 1` または `chunk_size < 1` の場合 |

### `background_job_status`

指定ジョブの永続化済み状態を返します。

```python
background_job_status(
    project_name: str,
    study_name: str | None,
    job_id: str,
) -> dict
```

#### 引数

| 名前 | 型 | デフォルト | 必須 | 説明 |
|---|---|---:|:---:|---|
| `project_name` | `str` | なし | Yes | 対象project名 |
| `study_name` | `str \| None` | なし | Yes | 対象study名 |
| `job_id` | `str` | なし | Yes | 対象ジョブID |

#### 戻り値

| 型 | 説明 |
|---|---|
| `dict` | 指定ジョブの状態 |

### `list_background_jobs`

対象project / study配下のジョブ状態一覧を返します。

```python
list_background_jobs(
    project_name: str,
    study_name: str | None = None,
) -> list[dict]
```

#### 引数

| 名前 | 型 | デフォルト | 必須 | 説明 |
|---|---|---:|:---:|---|
| `project_name` | `str` | なし | Yes | 対象project名 |
| `study_name` | `str \| None` | `None` | No | 対象study名 |

#### 戻り値

| 型 | 説明 |
|---|---|
| `list[dict]` | ジョブ状態の一覧 |

### `pause_background_job`

指定ジョブにpause要求を出し、更新後の状態を返します。

```python
pause_background_job(
    project_name: str,
    study_name: str | None,
    job_id: str,
) -> dict
```

#### 引数

| 名前 | 型 | デフォルト | 必須 | 説明 |
|---|---|---:|:---:|---|
| `project_name` | `str` | なし | Yes | 対象project名 |
| `study_name` | `str \| None` | なし | Yes | 対象study名 |
| `job_id` | `str` | なし | Yes | 対象ジョブID |

#### 戻り値

| 型 | 説明 |
|---|---|
| `dict` | 更新後のジョブ状態 |

### `resume_background_job`

指定ジョブにresume要求を出し、更新後の状態を返します。

```python
resume_background_job(
    project_name: str,
    study_name: str | None,
    job_id: str,
) -> dict
```

#### 引数

| 名前 | 型 | デフォルト | 必須 | 説明 |
|---|---|---:|:---:|---|
| `project_name` | `str` | なし | Yes | 対象project名 |
| `study_name` | `str \| None` | なし | Yes | 対象study名 |
| `job_id` | `str` | なし | Yes | 対象ジョブID |

#### 戻り値

| 型 | 説明 |
|---|---|
| `dict` | 更新後のジョブ状態 |

### `stop_background_job`

指定ジョブに協調停止要求を出し、更新後の状態を返します。

```python
stop_background_job(
    project_name: str,
    study_name: str | None,
    job_id: str,
) -> dict
```

#### 引数

| 名前 | 型 | デフォルト | 必須 | 説明 |
|---|---|---:|:---:|---|
| `project_name` | `str` | なし | Yes | 対象project名 |
| `study_name` | `str \| None` | なし | Yes | 対象study名 |
| `job_id` | `str` | なし | Yes | 対象ジョブID |

#### 戻り値

| 型 | 説明 |
|---|---|
| `dict` | 更新後のジョブ状態 |

## 内部向けAPI

以下は `EMSOptimizerClient` 内部用の補助メソッドです。
通常の利用者が直接呼ぶ想定ではありません。

| メソッド | 役割 |
|---|---|
| `_build_manager()` | `setup_project_files()` から `OptimizationManager` を取得し、run contextを設定する |
| `_start_run()` | run IDを割り当て、summaryディレクトリを作り、`running` の `run_info.yaml` を書く |
| `_finalize()` | study-level成果物を更新する |
| `_write_run_completed()` | `completed` のrun情報を書く |
| `_write_run_failed()` | `failed` と失敗理由を書く |
| `_write_run_stopped()` | `stopped` のrun情報を書く |
| `_infer_run_id()` | summaryディレクトリ名が `run_` 始まりならrun IDとして返す |
| `_control_stop_requested()` | 任意のcontrol providerからstop要求を読み取る |

## 使用例

### 最適化を実行する

```python
from manager.emsopt_api import EMSOptimizerClient

client = EMSOptimizerClient(project_root="projects")

result = client.run("motor_project", "study_a", disable_progress_gui=True)
print(result.status, result.run_id, result.run_summary_dir)
```

### 保存済みrunを確認する

```python
from manager.emsopt_api import EMSOptimizerClient

client = EMSOptimizerClient(project_root="projects")

result = client.check("motor_project", "study_a", run_id="run_0001")
print(result.status)
```

### バックグラウンド実行を開始する

```python
from manager.emsopt_api import EMSOptimizerClient

client = EMSOptimizerClient(project_root="projects")

job = client.start_background_run("motor_project", "study_a")
status = client.background_job_status("motor_project", "study_a", str(job["job_id"]))
```
