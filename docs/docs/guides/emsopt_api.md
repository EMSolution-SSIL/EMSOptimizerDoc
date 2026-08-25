---
sidebar_position: 5
---
# EMSOptimizer Python API
v0.7.0以降、主要なコマンド（`run`コマンドなど）はCLIとPython APIの両方の方式にて提供されています。  
ここでは、`manager/emsopt_api.py`に定義されているAPIを紹介します。  

## 位置づけ
`EMSOptimizerClient`クラスは project / study / run のライフサイクルをPythonから扱うためのAPIを提供します。
CLIはこのクライアントに処理を委譲し、外部スクリプトからも同じ実行管理経路を利用できます。

主な責務は次の通りです。
- project と study の解決
- `OptimizationManager` の生成
- run ID と run summary ディレクトリの割り当て
- `run_info.yaml` の状態更新
- study 直下の latest / resultant / records 成果物の更新
- GUIからの restart request の処理
- バックグラウンドジョブの開始、状態確認、pause / resume / stop 要求

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
run / check / sample / batch_run が返す実行結果です。
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

## `EMSOptimizerClient`
### 初期化
```python
from manager.emsopt_api import EMSOptimizerClient

client = EMSOptimizerClient(project_root="path/to/projects")
```

```python
EMSOptimizerClient(*, project_root: str | Path | None = None)
```

`project_root` を指定した場合、projectは `project_root/project_name` として解決されます。
未指定の場合は既定の `BaseConfig.PROJECT_DIR` 側の解決に従います。

`project_name` は識別子として扱われ、絶対パスやパス区切りを含む値は拒否されます。

## Manager生成API

### `create_manager`

```python
create_manager(
    project_name: str,
    study_name: str | None = None,
    *,
    restart_target_study_name: str | None = None,
) -> ManagerHandle
```

対象studyの `OptimizationManager` を生成し、外部スクリプトから直接操作できる形で返します。

- `study_name=None` の場合は default study が解決されます。
- `restart_target_study_name=None` の場合は、対象studyの `optimization.yaml` からrestart先を解決します。
- 内部では `setup_project_files()` で依存注入を構築し、`OptimizationManager` を取得します。
- 取得したmanagerには `set_run_context(project_name, study_name, restart_target_study_name)` が設定されます。

## 実行API

### `run`

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

指定studyの最適化を実行します。

処理の流れは次の通りです。

1. project / study / restart先studyを解決する
2. `OptimizationManager` を生成する
3. run ID と run summary ディレクトリを割り当てる
4. `run_info.yaml` に `running` を書き込む
5. `manager.run_optimization(str(run_summary_dir))` を実行する
6. 成果物をfinalizeし、`completed` または `stopped` を書き込む
7. GUIから `RestartSelection` が返された場合は、restart先studyへ切り替えて再実行する

例外が発生した場合は、`run_info.yaml` に `failed` と `failure_reason` を書いたうえで例外を再送出します。

`disable_progress_gui=True` の場合、`manager.config.enable_progress_gui` が `False` に設定されます。
バックグラウンド実行ではGUIを開かないために使われます。

### `check`

```python
check(
    project_name: str,
    study_name: str | None = None,
    run_id: str | None = None,
) -> OptimizationCommandResult
```

保存済みrunの結果を読み込み、確認用GUI処理を起動します。

- `run_id=None` の場合は `latest.yaml` が指す最新runを対象にします。
- `run_id` を指定した場合は、そのrun summaryディレクトリを直接読み込みます。
- 明示的に `run_id` を指定しても `latest.yaml` は更新されません。
- manager生成時は `setup_project_files(..., for_check=True)` を使います。
- 対象runが見つからない、または `run_id` が不正な場合は `RuntimeError` を送出します。
- GUIから `RestartSelection` が返された場合は、restart先studyを反映して通常の `run()` を開始します。

### `sample`

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

LHSサンプル群を評価し、通常runと同じ保存契約で永続化します。

- run ID を割り当てます。
- `run_info.yaml` に `running` を書き込みます。
- `manager.sample(num_sample, str(run_summary_dir), chunk_size=chunk_size)` を実行します。
- 成功時はfinalize後に `completed` または `stopped` を書き込みます。
- 失敗時は `failed` と `failure_reason` を書いたうえで例外を再送出します。

### `batch_run`

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

同一studyを複数回、独立したrunとして連続実行します。

- `num_runs < 1` は `ValueError` になります。
- 各runで新しい `OptimizationManager`、run ID、run summaryディレクトリを作成します。
- progress GUI は常に無効化されます。
- `control_provider.stop_requested()` が `True` の場合、新しいrunの開始前に中断します。
- 途中runが失敗しても `stop_on_error=False` なら失敗結果を `results` に追加し、次runへ進みます。
- `stop_on_error=True` の場合、失敗時に例外を再送出します。

## バックグラウンドジョブAPI

### `start_background_run`

```python
start_background_run(
    project_name: str,
    study_name: str | None = None,
) -> dict
```

`run` を別プロセスで開始し、ジョブ情報を辞書で返します。

### `start_background_batch_run`

```python
start_background_batch_run(
    project_name: str,
    num_runs: int,
    study_name: str | None = None,
    *,
    stop_on_error: bool = False,
) -> dict
```

`batch_run` を別プロセスで開始します。
`num_runs < 1` は `ValueError` になります。

### `start_background_sample`

```python
start_background_sample(
    project_name: str,
    num_sample: int,
    study_name: str | None = None,
    *,
    chunk_size: int | None = None,
) -> dict
```

`sample` を別プロセスで開始します。
`num_sample < 1` または `chunk_size < 1` は `ValueError` になります。

### `background_job_status`

```python
background_job_status(
    project_name: str,
    study_name: str | None,
    job_id: str,
) -> dict
```

指定ジョブの永続化済み状態を返します。

### `list_background_jobs`

```python
list_background_jobs(
    project_name: str,
    study_name: str | None = None,
) -> list[dict]
```

対象project / study配下のジョブ状態一覧を返します。

### `pause_background_job`

```python
pause_background_job(
    project_name: str,
    study_name: str | None,
    job_id: str,
) -> dict
```

指定ジョブにpause要求を出し、更新後の状態を返します。

### `resume_background_job`

```python
resume_background_job(
    project_name: str,
    study_name: str | None,
    job_id: str,
) -> dict
```

指定ジョブにresume要求を出し、更新後の状態を返します。

### `stop_background_job`

```python
stop_background_job(
    project_name: str,
    study_name: str | None,
    job_id: str,
) -> dict
```

指定ジョブに協調停止要求を出し、更新後の状態を返します。

## 状態と保存先

通常run / sample / batch_runでは、runごとに次のようなsummaryディレクトリが作られます。

```text
<project_root>/<project_name>/summary/optimization_studies/<study_name>/runs/<run_id>/
```

`run_id` は `run_0001` 形式で連番割り当てされます。

実行中、完了、停止、失敗の状態は `run_info.yaml` に書き込まれます。

| 状態 | 書き込まれるタイミング |
|---|---|
| `running` | run ID割り当て直後 |
| `completed` | manager処理とfinalizeが正常終了したとき |
| `stopped` | 協調停止要求により終了したとき |
| `failed` | 例外が発生したとき |

## コールバックと制御プロバイダ

### `run_started_callback`

`run_started_callback` は、run ID と run summaryディレクトリが確定した直後に呼ばれます。
バックグラウンドジョブでは、現在実行中のrun IDを `job_info.yaml` に反映する用途で使われます。

```python
def on_started(run_id: str, run_summary_dir: Path) -> None: ...
```

### `control_provider`

`control_provider` は、`OptimizationManager` へ渡される外部制御用オブジェクトです。
バックグラウンドジョブでは `FileJobControl` が使われ、pause / stop要求をファイル経由でmanagerへ伝えます。

`batch_run()` では、新しいrunを開始する前に `control_provider.stop_requested()` を確認します。

## 内部ヘルパー

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

## 最小利用例

```python
from manager.emsopt_api import EMSOptimizerClient

client = EMSOptimizerClient(project_root="projects")

result = client.run("motor_project", "study_a", disable_progress_gui=True)
print(result.status, result.run_id, result.run_summary_dir)
```

```python
client = EMSOptimizerClient(project_root="projects")

result = client.check("motor_project", "study_a", run_id="run_0001")
print(result.status)
```

```python
client = EMSOptimizerClient(project_root="projects")

job = client.start_background_run("motor_project", "study_a")
status = client.background_job_status("motor_project", "study_a", str(job["job_id"]))
```
