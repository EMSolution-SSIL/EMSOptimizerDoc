---
sidebar_position: 5
---

# EMSOptimizer Python API

## Overview

Since v0.7.0, major commands such as `run` are available through both the CLI and Python API.
This page introduces the Python API defined in `manager/emsopt_api.py`.
:::info
The EMSOptFree portion of EMSOptimizer is public, so users can also call operations directly without this API.  
However, the standard EMSOptimizer workflow is designed to run through this API, so using the API as the operation interface is recommended for stable behavior.  
:::

The `EMSOptimizerClient` class provides an API for managing the project / study / run lifecycle from Python.
The CLI delegates operations to this client, so external scripts can use the same execution-management path.

## import

```python
from manager.emsopt_api import EMSOptimizerClient
```

## Quick reference

| API | Type | Main purpose | Return value |
|---|---|---|---|
| `EMSOptimizerClient` | class | Client for project / study / run operations | `EMSOptimizerClient` |
| `create_manager` | method | Creates a configured manager | `ManagerHandle` |
| `check` | method | Loads a saved run and starts the review GUI | `OptimizationCommandResult` |
| `run` | method | Runs optimization for a study | `OptimizationCommandResult` |
| `batch_run` | method | Runs the same study repeatedly | `list[OptimizationCommandResult]` |
| `sample` | method | Evaluates an LHS sample set | `OptimizationCommandResult` |
| `start_background_run` | method | Starts `run` in another process | `dict` |
| `start_background_batch_run` | method | Starts `batch_run` in another process | `dict` |
| `start_background_sample` | method | Starts `sample` in another process | `dict` |
| `background_job_status` | method | Gets background-job status | `dict` |
| `list_background_jobs` | method | Lists background jobs | `list[dict]` |
| `pause_background_job` | method | Sends a pause request to a job | `dict` |
| `resume_background_job` | method | Sends a resume request to a job | `dict` |
| `stop_background_job` | method | Sends a stop request to a job | `dict` |

## Data models

### `ManagerHandle`

Container for the created `OptimizationManager` and resolved context returned by `create_manager()`.

| Field | Type | Description |
|---|---|---|
| `project_name` | `str` | Target project name |
| `study_name` | `str` | Resolved study name |
| `manager` | `OptimizationManager` | Configured manager |
| `restart_target_study_name` | `str \| None` | Study name used for restart; `None` when unset |

### `OptimizationCommandResult`

Execution result returned by `run` / `check` / `sample` / `batch_run`.

| Field | Type | Description |
|---|---|---|
| `project_name` | `str` | Target project name |
| `study_name` | `str` | Study name actually used |
| `status` | `str` | Status such as `completed`, `stopped`, or `failed` |
| `manager` | `OptimizationManager` | Manager used for execution |
| `run_id` | `str \| None` | Run ID in the form `run_0001`; `None` when not applicable |
| `run_summary_dir` | `Path \| None` | Canonical artifact directory for the run |
| `restart_selection` | `RestartSelection \| None` | Restart selection returned by the GUI |
| `failure_reason` | `str \| None` | Reason for failure |

## Common specifications

### Resolving project / study

When `project_root` is specified, the project is resolved as `project_root/project_name`.
When omitted, the default resolution is used: the `project` folder directly under the execution directory.

`project_name` is treated as an identifier; absolute paths and values containing path separators are rejected.

### Run-summary directory

For ordinary run / sample / batch_run operations, the following summary directory is created for each run.

```text
<project_root>/<project_name>/summary/optimization_studies/<study_name>/runs/<run_id>/
```

`run_id` values are assigned sequentially in the form `run_0001`.

### Run states

Running, `completed`, `stopped`, and failed states are written to `run_info.yaml`.

| State | When it is written |
|---|---|
| `running` | Immediately after assigning the run ID |
| `completed` | When manager processing and finalization finish successfully |
| `stopped` | When execution ends due to a cooperative stop request |
| `failed` | When an exception occurs |

### Callbacks

`run_started_callback` is called immediately after the run ID and run-summary directory are determined.
For background jobs, it is used to record the currently `running` run ID in `job_info.yaml`.

```python
def on_started(run_id: str, run_summary_dir: Path) -> None: ...
```

### Control provider

`control_provider` is an object for external control passed to `OptimizationManager`.
Background jobs use `FileJobControl` to communicate pause / stop requests to the manager through files.

`batch_run()` checks `control_provider.stop_requested()` before starting each new run.

## API details

### `EMSOptimizerClient`

Client for managing project / study / run execution.

```python
EMSOptimizerClient(*, project_root: str | Path | None = None)
```

#### Arguments

| Name | Type | Default | Required | Description |
|---|---|---:|:---:|---|
| `project_root` | `str \| Path \| None` | `None` | No | Root directory in which to search for projects |

#### Return value

| Type | Description |
|---|---|
| `EMSOptimizerClient` | Client for project / study / run operations |

#### Example

```python
client = EMSOptimizerClient(project_root="projects")
```

### `create_manager`

Creates the `OptimizationManager` for the target study and returns it in a form that can be operated directly from an external script.

```python
create_manager(
    project_name: str,
    study_name: str | None = None,
    *,
    restart_target_study_name: str | None = None,
) -> ManagerHandle
```

#### Arguments

| Name | Type | Default | Required | Description |
|---|---|---:|:---:|---|
| `project_name` | `str` | None | Yes | Target project name |
| `study_name` | `str \| None` | `None` | No | Target study name; the default study is resolved when `None` |
| `restart_target_study_name` | `str \| None` | `None` | No | Study name for restart; resolved from `optimization.yaml` when `None` |

#### Return value

| Type | Description |
|---|---|
| `ManagerHandle` | Created manager and resolved context |

#### Side effects

- Builds dependency injection with `setup_project_files()`.
- Sets `set_run_context(project_name, study_name, restart_target_study_name)` on the returned manager.

### `run`

Runs optimization for the specified study.

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

#### Arguments

| Name | Type | Default | Required | Description |
|---|---|---:|:---:|---|
| `project_name` | `str` | None | Yes | Target project name |
| `study_name` | `str \| None` | `None` | No | Target study name; the default study is resolved when `None` |
| `control_provider` | `object \| None` | `None` | No | Object passed to the manager for external control such as pause / stop |
| `disable_progress_gui` | `bool` | `False` | No | Disables the progress GUI when `True` |
| `run_started_callback` | `Callable[[str, Path], None] \| None` | `None` | No | Callback invoked immediately after the run ID and summary directory are determined |

#### Return value

| Type | Description |
|---|---|
| `OptimizationCommandResult` | Result containing execution status, manager, run ID, and artifact directory |

#### Exceptions

| Exception | Condition |
|---|---|
| `Exception` | If an exception occurs during execution. It is re-raised after `failed` and `failure_reason` are written to `run_info.yaml` |

#### Processing flow

1. Resolves the project, study, and restart-target study.
2. Creates an `OptimizationManager`.
3. Assigns a run ID and run-summary directory.
4. Writes running to `run_info.yaml`.
5. Executes `manager.run_optimization(str(run_summary_dir))`.
6. Finalizes artifacts and writes `completed` or `stopped`.
7. If the GUI returns a `RestartSelection`, switches to the restart-target study and runs again.

#### Notes

When `disable_progress_gui=True`, `manager.config.enable_progress_gui` is set to `False`.
Background execution uses this setting to prevent the GUI from opening.

### `check`

Loads the results of a saved run and starts the review GUI.

```python
check(
    project_name: str,
    study_name: str | None = None,
    run_id: str | None = None,
) -> OptimizationCommandResult
```

#### Arguments

| Name | Type | Default | Required | Description |
|---|---|---:|:---:|---|
| `project_name` | `str` | None | Yes | Target project name |
| `study_name` | `str \| None` | `None` | No | Target study name; the default study is resolved when `None` |
| `run_id` | `str \| None` | `None` | No | Target run ID; when `None`, the latest run referenced by `latest.yaml` is used |

#### Return value

| Type | Description |
|---|---|
| `OptimizationCommandResult` | Result containing the target run information and manager |

#### Exceptions

| Exception | Condition |
|---|---|
| `RuntimeError` | When the target run cannot be found or `run_id` is invalid |

#### Side effects

- Manager creation uses `setup_project_files(..., for_check=True)`.
- If the GUI returns a `RestartSelection`, starts a normal `run()` using the restart-target study.

#### Notes

Specifying `run_id` explicitly does not update `latest.yaml`.

### `sample`

Evaluates an LHS sample set and persists it using the same storage contract as a normal run.

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

#### Arguments

| Name | Type | Default | Required | Description |
|---|---|---:|:---:|---|
| `project_name` | `str` | None | Yes | Target project name |
| `num_sample` | `int` | None | Yes | Number of LHS samples to evaluate |
| `study_name` | `str \| None` | `None` | No | Target study name; the default study is resolved when `None` |
| `chunk_size` | `int \| None` | `None` | No | Chunk size for sample evaluation |
| `control_provider` | `object \| None` | `None` | No | Object passed to the manager for external control such as pause / stop |
| `run_started_callback` | `Callable[[str, Path], None] \| None` | `None` | No | Callback invoked immediately after the run ID and summary directory are determined |

#### Return value

| Type | Description |
|---|---|
| `OptimizationCommandResult` | Result containing sample-evaluation status, manager, run ID, and artifact directory |

#### Exceptions

| Exception | Condition |
|---|---|
| `Exception` | If an exception occurs during evaluation. It is re-raised after `failed` and `failure_reason` are written to `run_info.yaml` |

#### Side effects

- Assigns a run ID.
- Writes `running` to `run_info.yaml`.
- Executes `manager.sample(num_sample, str(run_summary_dir), chunk_size=chunk_size)`.
- On success, writes `completed` or `stopped` after finalization.

### `batch_run`

Runs the same study repeatedly as independent runs.

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

#### Arguments

| Name | Type | Default | Required | Description |
|---|---|---:|:---:|---|
| `project_name` | `str` | None | Yes | Target project name |
| `num_runs` | `int` | None | Yes | Number of runs to execute sequentially |
| `study_name` | `str \| None` | `None` | No | Target study name; the default study is resolved when `None` |
| `stop_on_error` | `bool` | `False` | No | When `True`, re-raises an exception and stops if an intermediate run fails |
| `control_provider` | `object \| None` | `None` | No | Object passed to the manager for external control such as pause / stop |
| `run_started_callback` | `Callable[[str, Path], None] \| None` | `None` | No | Callback invoked immediately after the run ID and summary directory are determined |

#### Return value

| Type | Description |
|---|---|
| `list[OptimizationCommandResult]` | Result for each run |

#### Exceptions

| Exception | Condition |
|---|---|
| `ValueError` | When `num_runs < 1` |
| `Exception` | When an intermediate run fails with `stop_on_error=True` |

#### Side effects

- Creates a new `OptimizationManager`, run ID, and run-summary directory for each run.
- The progress GUI is always disabled.
- If `control_provider.stop_requested()` is `True`, stops before starting a new run.

#### Notes

If an intermediate run fails while `stop_on_error=False`, its failure result is added to `results` and execution proceeds to the next run.

## Background-job API

### `start_background_run`

Starts `run` in another process and returns job information as a dictionary.

```python
start_background_run(
    project_name: str,
    study_name: str | None = None,
) -> dict
```

#### Arguments

| Name | Type | Default | Required | Description |
|---|---|---:|:---:|---|
| `project_name` | `str` | None | Yes | Target project name |
| `study_name` | `str \| None` | `None` | No | Target study name |

#### Return value

| Type | Description |
|---|---|
| `dict` | Information about the started background job |

### `start_background_batch_run`

Starts `batch_run` in another process.

```python
start_background_batch_run(
    project_name: str,
    num_runs: int,
    study_name: str | None = None,
    *,
    stop_on_error: bool = False,
) -> dict
```

#### Arguments

| Name | Type | Default | Required | Description |
|---|---|---:|:---:|---|
| `project_name` | `str` | None | Yes | Target project name |
| `num_runs` | `int` | None | Yes | Number of runs to execute sequentially |
| `study_name` | `str \| None` | `None` | No | Target study name |
| `stop_on_error` | `bool` | `False` | No | When `True`, stop if an intermediate run fails |

#### Return value

| Type | Description |
|---|---|
| `dict` | Information about the started background job |

#### Exceptions

| Exception | Condition |
|---|---|
| `ValueError` | When `num_runs < 1` |

### `start_background_sample`

Starts `sample` in another process.

```python
start_background_sample(
    project_name: str,
    num_sample: int,
    study_name: str | None = None,
    *,
    chunk_size: int | None = None,
) -> dict
```

#### Arguments

| Name | Type | Default | Required | Description |
|---|---|---:|:---:|---|
| `project_name` | `str` | None | Yes | Target project name |
| `num_sample` | `int` | None | Yes | Number of LHS samples to evaluate |
| `study_name` | `str \| None` | `None` | No | Target study name |
| `chunk_size` | `int \| None` | `None` | No | Chunk size for sample evaluation |

#### Return value

| Type | Description |
|---|---|
| `dict` | Information about the started background job |

#### Exceptions

| Exception | Condition |
|---|---|
| `ValueError` | When `num_sample < 1` or `chunk_size < 1` |

### `background_job_status`

Returns the persisted state of the specified job.

```python
background_job_status(
    project_name: str,
    study_name: str | None,
    job_id: str,
) -> dict
```

#### Arguments

| Name | Type | Default | Required | Description |
|---|---|---:|:---:|---|
| `project_name` | `str` | None | Yes | Target project name |
| `study_name` | `str \| None` | None | Yes | Target study name |
| `job_id` | `str` | None | Yes | Target job ID |

#### Return value

| Type | Description |
|---|---|
| `dict` | State of the specified job |

### `list_background_jobs`

Returns a list of job states under the target project / study.

```python
list_background_jobs(
    project_name: str,
    study_name: str | None = None,
) -> list[dict]
```

#### Arguments

| Name | Type | Default | Required | Description |
|---|---|---:|:---:|---|
| `project_name` | `str` | None | Yes | Target project name |
| `study_name` | `str \| None` | `None` | No | Target study name |

#### Return value

| Type | Description |
|---|---|
| `list[dict]` | List of job states |

### `pause_background_job`

Sends a pause request to the specified job and returns its updated state.

```python
pause_background_job(
    project_name: str,
    study_name: str | None,
    job_id: str,
) -> dict
```

#### Arguments

| Name | Type | Default | Required | Description |
|---|---|---:|:---:|---|
| `project_name` | `str` | None | Yes | Target project name |
| `study_name` | `str \| None` | None | Yes | Target study name |
| `job_id` | `str` | None | Yes | Target job ID |

#### Return value

| Type | Description |
|---|---|
| `dict` | Updated job state |

### `resume_background_job`

Sends a resume request to the specified job and returns its updated state.

```python
resume_background_job(
    project_name: str,
    study_name: str | None,
    job_id: str,
) -> dict
```

#### Arguments

| Name | Type | Default | Required | Description |
|---|---|---:|:---:|---|
| `project_name` | `str` | None | Yes | Target project name |
| `study_name` | `str \| None` | None | Yes | Target study name |
| `job_id` | `str` | None | Yes | Target job ID |

#### Return value

| Type | Description |
|---|---|
| `dict` | Updated job state |

### `stop_background_job`

Sends a cooperative stop request to the specified job and returns its updated state.

```python
stop_background_job(
    project_name: str,
    study_name: str | None,
    job_id: str,
) -> dict
```

#### Arguments

| Name | Type | Default | Required | Description |
|---|---|---:|:---:|---|
| `project_name` | `str` | None | Yes | Target project name |
| `study_name` | `str \| None` | None | Yes | Target study name |
| `job_id` | `str` | None | Yes | Target job ID |

#### Return value

| Type | Description |
|---|---|
| `dict` | Updated job state |

## Internal API

The following helper methods are for internal use by `EMSOptimizerClient`.
They are not intended to be called directly by ordinary users.

| Method | Role |
|---|---|
| `_build_manager()` | Gets `OptimizationManager` from `setup_project_files()` and sets the run context |
| `_start_run()` | Assigns a run ID, creates the summary directory, and writes `running` to `run_info.yaml` |
| `_finalize()` | Updates study-level artifacts |
| `_write_run_completed()` | Writes completed-run information |
| `_write_run_failed()` | Writes `failed` and the failure reason |
| `_write_run_stopped()` | Writes stopped-run information |
| `_infer_run_id()` | Returns the summary-directory name as a run ID when it starts with `run_` |
| `_control_stop_requested()` | Reads a stop request from an arbitrary control provider |

## Examples

### Run optimization

```python
from manager.emsopt_api import EMSOptimizerClient

client = EMSOptimizerClient(project_root="projects")

result = client.run("motor_project", "study_a", disable_progress_gui=True)
print(result.status, result.run_id, result.run_summary_dir)
```

### Review a saved run

```python
from manager.emsopt_api import EMSOptimizerClient

client = EMSOptimizerClient(project_root="projects")

result = client.check("motor_project", "study_a", run_id="run_0001")
print(result.status)
```

### Starting background execution

```python
from manager.emsopt_api import EMSOptimizerClient

client = EMSOptimizerClient(project_root="projects")

job = client.start_background_run("motor_project", "study_a")
status = client.background_job_status("motor_project", "study_a", str(job["job_id"]))
```
