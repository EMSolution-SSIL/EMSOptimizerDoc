---
sidebar_position: 1
---

# Command reference
This page lists the commands available in EMSOptimizer. Help for each command can also be displayed with the following command.

```sh
python emsopt.py -h
```
```sh
python emsopt.py {コマンド名} -h
```
:::info
When EMSOptFree is installed from a wheel, replace `python emsopt.py` with `emsopt`. In general, commands can be run from anywhere within the Python environment.  
:::
:::info
For details about the studies, runs, and jobs mentioned below, see [User Guide > Study control and result review](./study_control_and_results.md).
:::

## Preprocessing
### show_avl
#### Usage
```sh
python emsopt.py show_avl \[-n {オブジェクト名}\]
```
#### Description
This command lists the EMSOptimizer core objects that can be configured in `optimization.yaml`. Specify an object name with `-n` to display that object's documentation.

### cp_proj
#### Usage
```sh
python emsopt.py cp_proj {コピー元プロジェクト名} {コピー先プロジェクト名} [--project-root {プロジェクトルート}]
```
#### Description
This command copies a `project`. The source `project` is selected from the `project` folder, and the destination `project` is created there automatically.
#### --project-root \{project_root\}
Root path of the project folders. If omitted, the `projects` folder in the current directory is used.

### mk_study
#### Usage
```sh
python emsopt.py mk_study {プロジェクト名} {スタディ名} [--project-root {プロジェクトルート}]
```
#### Description
This command creates a study in a project. The study manages a set of optimization settings and results.
#### --project-root \{project_root\}
Root path of the project folders. If omitted, the `projects` folder in the current directory is used.

### cln_proj
#### Usage
```sh
python emsopt.py cln_proj {プロジェクト名} [--project-root {プロジェクトルート}] [--remove-summary] [--remove-studies] [--yes]
```
#### Description
This command deletes intermediate folders (`resources`, `opt_progress`) stored in the specified project.
#### --project-root \{project_root\}
Root path of the project folders. If omitted, the `projects` folder in the current directory is used.
#### --remove-`summary`
In addition to the intermediate folders, deletes the optimization-result `summary` folder (summary).
#### --remove-studies
In addition to the intermediate folders, deletes all studies in the project.
#### --yes
Skips the confirmation message and deletes immediately.
:::warning
Running `cln_proj` **deletes optimization-progress and result files stored in the project**. Deleted files cannot be restored.  
The `check` command displays results by reading the `summary` folder, so results cannot be reviewed with `check` after `cln_proj --remove-summary`.  
:::

### rm_proj
#### Usage
```sh
python emsopt.py rm_proj {プロジェクト名} [--project-root {プロジェクトルート}] [--yes]
```
#### Description
This command deletes the specified project in the `project` folder.
#### --project-root \{project_root\}
Root path of the project folders. If omitted, the `projects` folder in the current directory is used.
#### --yes
Skips the confirmation message and deletes immediately.
:::warning
**Deleted projects cannot be restored.**  
:::

### save_tpl
#### Usage
```sh
python emsopt.py save_tpl {プロジェクト名} {テンプレート名} [--project-root {プロジェクトルート}] [--study-name {スタディ名}]
```
#### Description
This command saves the specified project's `optimization_problem.yaml` as a template. The saved settings are stored in `project/template.yaml` and can be loaded with `load_tpl`.
#### --project-root \{project_root\}
Root path of the project folders. If omitted, the `projects` folder in the current directory is used.
#### --study-name \{study_name\}
Study name to reference. If omitted, a `defaults` study is created and referenced based on the configuration files directly under the project.

### load_tpl
#### Usage
```sh
python emsopt.py load_tpl {プロジェクト名} {テンプレート名} [--project-root {プロジェクトルート}] [--study-name {スタディ名}]
```
#### Description
This command copies the template contents into the specified project's `optimization_problem.yaml`.
#### --project-root \{project_root\}
Root path of the project folders. If omitted, the `projects` folder in the current directory is used.
#### --study-name \{study_name\}
Study name to reference. If omitted, a `defaults` study is created and referenced from the configuration files directly under the project.

### validate
#### Usage
```sh
python emsopt.py validate {プロジェクト名} [--project-root {プロジェクトルート}] [--study-name {スタディ名}]
```
#### Description
This command validates the optimization settings of the specified project.
#### --project-root \{project_root\}
Root path of the project folders. If omitted, the `projects` folder in the current directory is used.
#### --study-name \{study_name\}
Study name to reference. If omitted, a `defaults` study is created and referenced based on the configuration files directly under the project.

### inspect_mesh
#### Usage
```sh
python emsopt.py inspect_mesh {メッシュファイルパス} [--machine-config {machine.yamlパス}]
```
#### Description
This command analyzes the specified Gmsh mesh file and outputs material IDs and names from $PhysicalNames, element types by physical tag, node count, radius range, and angle range.
When `--machine-config` is specified, it also checks consistency between machine.yaml's target_ids_and_onoff / mirror_id_map / increment_info and the mesh physical IDs.
#### --machine-config \{machine_yaml_path\}
Optional path to machine.yaml used to check consistency with mesh physical IDs. If omitted, only mesh information is output.
:::info
The EMSOptAnalyzer package is required to run this command.
:::

### validate_mesh
#### Usage
```sh
python emsopt.py validate_mesh {プロジェクト名} [--project-root {プロジェクトルート}] [--study-name {スタディ名}] [--mesh {メッシュファイルパス}]
```
#### Description
This command checks consistency between the mesh and machine.yaml for the specified project or study.
It loads machine.yaml, analyzes the design-target mesh, checks whether target_ids_and_onoff / mirror_id_map / increment_info are consistent with the mesh physical IDs, and outputs the element types in the design region.
#### --project-root \{project_root\}
Root path of the project folders. If omitted, the projects folder in the current directory is used.
#### --study-name \{study_name\}
Study name to reference. If omitted, machine.yaml directly under the project is used.
#### --mesh \{mesh_path\}
Explicitly specifies the mesh to inspect. If omitted, the design-target mesh name is resolved from analysis_dimension and design_target in machine.yaml and searched for in the project or study folder.
:::info
The EMSOptAnalyzer package is required to run this command.
:::

## Execution
### run
#### Usage
```sh
python emsopt.py run {プロジェクト名} [--project-root {プロジェクトルート}] [--study-name {スタディ名}] [--background]
```
#### Description
This command runs optimization for the specified project. When optimization finishes, an optimization summary `summary` folder is generated in the project folder and loaded by the `check` command.
:::warning
If intermediate files or a summary folder already exist in the project folder, their contents are overwritten.
:::
#### --project-root \{project_root\}
Root path of the project folders. If omitted, the `projects` folder in the current directory is used.
#### --study-name \{study_name\}
Study name to reference. If omitted, a `defaults` study is created and referenced based on the configuration files directly under the project.

### batch_run
#### Usage
```sh
python emsopt.py batch_run {プロジェクト名} {バッチサイズ（＝実行するランの数）} [--project-root {プロジェクトルート}] [--study-name {スタディ名}] [--stop-on-error] [--background]
```
#### Description
This command runs optimization for the specified project as a batch. Each result in the batch is saved as a run in the `summary` folder.
:::info
The GUI is forcibly disabled when `batch_run` runs.
:::
#### --project-root \{project_root\}
Root path of the project folders. If omitted, the `projects` folder in the current directory is used.
#### --study-name \{study_name\}
Study name to reference. If omitted, a `defaults` study is created and referenced from the configuration files directly under the project.
#### --stop-on-error
When specified, aborts the entire batch if an error occurs. When omitted, the failed run is stopped and the remaining runs continue.

### sample
```sh
python emsopt.py sample {プロジェクト名} {サンプル数} [--project-root {プロジェクトルート}] [--study-name {スタディ名}] [--chunk-size {チャンクサイズ}] [--background]
```
#### Description
This command performs Latin hypercube sampling \[25\] within the design-variable ranges configured for the specified project. Sampling results are stored in the `summary` folder, like ordinary optimization results.
#### --project-root \{project_root\}
Root path of the project folders. If omitted, the `projects` folder in the current directory is used.
#### --study-name \{study_name\}
Study name to reference. If omitted, a `defaults` study is created and referenced from the configuration files directly under the project.
#### --chunk-size \{chunk_size\}
Chunk size. Samples are divided into chunks of this size for evaluation. If omitted, an appropriate chunk size is set automatically.

## Job management
### job_list
#### Usage
```sh
python emsopt.py job_list {プロジェクト名} [--project-root {プロジェクトルート}] [--study-name {スタディ名}]
```
#### Description
Displays background jobs associated with the specified project and study. This includes jobs started by `run --background`, `batch_run --background`, and `sample --background`.
You can inspect each job's job_id, pid, status, currently running run, and related runs.
#### --project-root \{project_root\}
Root path of the project folders. If omitted, the projects folder in the current directory is used.
#### --study-name \{study_name\}
Study name to reference. If omitted, a default study is created and referenced based on the configuration files directly under the project.

### job_status
#### Usage
```sh
python emsopt.py job_status {プロジェクト名} --job-id {ジョブID} [--project-root {プロジェクトルート}] [--study-name {スタディ名}]
```
#### Description
Displays the current status of the specified background job. Statuses include running, pausing, paused, stopping, stopped, completed, failed, and lost.
lost is shown when the job is marked as running but its corresponding process does not exist.
#### --job-id \{job_id\}
ID of the background job to operate on. It is returned by run --background, batch_run --background, or sample --background, and can also be found with job_list.
#### --project-root \{project_root\}
Root path of the project folders. If omitted, the projects folder in the current directory is used.
#### --study-name \{study_name\}
Study name to reference. If omitted, a default study is created and referenced from the configuration files directly under the project.

### job_pause
#### Usage
```sh
python emsopt.py job_pause {プロジェクト名} --job-id {ジョブID} [--project-root {プロジェクトルート}] [--study-name {スタディ名}]
```
#### Description
Sends a pause request to a running background job.
:::warning
Pausing is not an immediate interrupt; it takes effect at a safe control checkpoint in the optimization loop. For `run` / `batch_run`, this is at an iteration boundary; for `sample`, it is at a chunk boundary.
:::
#### --job-id \{job_id\}
ID of the background job to pause.
#### --project-root \{project_root\}
Root path of the project folders. If omitted, the projects folder in the current directory is used.
#### --study-name \{study_name\}
Study name to reference. If omitted, a default study is created and referenced from the configuration files directly under the project.

### job_resume
#### Usage
```sh
python emsopt.py job_resume {プロジェクト名} --job-id {ジョブID} [--project-root {プロジェクトルート}] [--study-name {スタディ名}]
```
#### Description
Sends a resume request to a paused background job. A job paused by job_pause returns to running with this command.
#### --job-id \{job_id\}
ID of the background job to resume.
#### --project-root \{project_root\}
Root path of the project folders. If omitted, the projects folder in the current directory is used.
#### --study-name \{study_name\}
Study name to reference. If omitted, a default study is created and referenced from the configuration files directly under the project.

### job_stop
#### Usage
```sh
python emsopt.py job_stop {プロジェクト名} --job-id {ジョブID} [--project-root {プロジェクトルート}] [--study-name {スタディ名}]
```
#### Description
Sends a stop request to a running or paused background job. The job terminates at a safe control checkpoint, and stopped is recorded in the corresponding run's run_info.yaml.  
:::warning
This command does not forcibly terminate the process. It stops cooperatively at an EMSOptimizer control checkpoint rather than destructively interrupting a CAE analysis or parallel evaluation.
:::
#### --job-id \{job_id\}
ID of the background job to stop.
#### --project-root \{project_root\}
Root path of the project folders. If omitted, the projects folder in the current directory is used.
#### --study-name \{study_name\}
Study name to reference. If omitted, a default study is created and referenced from the configuration files directly under the project.

## Postprocessing
### check
#### Usage
```sh
python emsopt.py check {プロジェクト名} [--project-root {プロジェクトルート}] [--study-name {スタディ名}] [--run-id {ランID}]
```
#### Description
This command displays optimization progress for the specified project in the GUI. Specifically, it loads the summary folder generated after optimization with `run` and displays its contents in the GUI.
#### --project-root \{project_root\}
Root path of the project folders. If omitted, the `projects` folder in the current directory is used.
#### --study-name \{study_name\}
Study name to reference. If omitted, a `defaults` study is created and referenced from the configuration files directly under the project.
#### --run-id \{run_id\}
Run ID to reference. If omitted, the latest run is used.

### export_data
#### Usage
```sh
python emsopt.py export_data {プロジェクト名} [--project-root {プロジェクトルート}] [--study-names {スタディ名1} {スタディ名2} ...] [--statuses {ステータス名1} {ステータス名2} ...]
```
#### Description
This command extracts and exports data for the specified studies and statuses from optimization-result CSV files for all studies run in the project.
#### --project-root \{project_root\}
Root path of the project folders. If omitted, the `projects` folder in the current directory is used.
#### --study-names \{study_name_1\} \{study_name_2\} ...
Study names to extract. If omitted, data is extracted from all studies.
#### --statuses \{status_name_1\} \{status_name_2\} ...
Statuses to extract. If omitted, only data from successful analyses is extracted.
:::info
The CSV files used by this command are generated when `optimization.yaml` > `output_control` > `candidate` > `enabled` is `True`.
:::

### analyze_runs
#### Usage
```sh
python emsopt.py analyze_runs {プロジェクト名} [--project-root {プロジェクトルート}] [--study-name {スタディ名}] [--reference-point {HV参照点}] [--run-ids {ランID}] [--gui]
```
#### Description
This command loads all runs in the specified project and calculates statistics: the best objective value for single-objective optimization, or the mean and standard deviation of hypervolume (HV) for multi-objective optimization. Results are written to the `summary/analysis` folder.
#### --project-root \{project_root\}
Root path of the project folders. If omitted, the `projects` folder in the current directory is used.
#### --study-name \{study_name\}
Study name to reference. If omitted, a `defaults` study is created and referenced from the configuration files directly under the project.
#### --reference-point \{HV_reference_point\}
Reference point used to calculate HV when analyzing multi-objective results.  
For example, for two objectives with reference point (1.0, 1.0), specify `--reference-point 1.0 1.0`.
:::warning
The reference point must be on the worse side (with larger objective values) than every point on the Pareto front.
:::
#### --run-ids \{run_ids\}
Run IDs to reference. Multiple IDs can be specified (for example, `--run-ids run_0001 run_0002 run_0003`). If omitted, all runs in the study are used.
#### --gui
When specified, displays a GUI for reviewing results from multiple runs.
