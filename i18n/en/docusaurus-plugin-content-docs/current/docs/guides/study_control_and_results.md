---
sidebar_position: 1
---

# Study Control and Results
## Overview
In EMSOptimizer, optimization execution and results are managed in the following three-level hierarchy.
- `project`
  - Unit that separates the optimization target itself. Mesh files and analysis-condition folders are stored here.
- `study`
  - Unit for a set of optimization conditions
  - Created in the `<project>/optimization_studies/` folder
  - Contains `optimization.yaml`, `machine.yaml`, and `optimization_problem.yaml`
- `run`
  - Unit of study execution
  - Created in `<project>/summary/optimization_studies/<study_name>/`
  - Additional runs are created when the same study is executed repeatedly
  - Runs submitted in the background are also managed as jobs. Job information is created in the same `<project>/summary/optimization_studies/<study_name>/` folder.

## Creating and managing studies
### Creating a study
Create a study with the `mk_study` command.
```bash
python emsopt.py mk_study <project_name> <study_name>
python emsopt.py mk_study <project_name> <study_name> --from-study <source_study>
```
The following files are copied.
- `optimization.yaml`
- `machine.yaml`
- `optimization_problem.yaml`

An error is raised if a study with the same name already exists, preventing an existing study from being overwritten.

### Automatic creation of the `default` study
When `--study-name` is omitted for commands such as `run`, `sample`, `check`, or `analyze_runs`, the `default` study is used.  
In this case, the `default` study is created automatically by copying the configuration files in the project root.

## Creating and managing runs
### Creating a run
Runs are automatically created in the `summary` folder, primarily when one of the following commands is executed.
```bash
python emsopt.py run <project_name> --study-name <study>
python emsopt.py batch_run <project_name> <num_runs> --study-name <study>
python emsopt.py sample <project_name> <num_sample> --study-name <study>
```
- `run`
  - Run optimization once and save it as one run
- `batch_run`
  - Execute the same study independently multiple times and save each execution as a run
- `sample`
  - Evaluate LHS samples and save them as one run

### Run ID assignment
Runs are numbered sequentially for each study.
- `run_0001`
- `run_0002`
- `run_0003`

### Managing execution status
The `run_info.yaml` created for each run contains the following information:
- `run_id`
- `study_name`
- `status` (record of optimization success or failure)
- `started_at`
- `finished_at`
- `failure_reason`
- `updated_at`

### Job management
When a target command is run in the background (`run --background`, `batch_run --background`, or `sample --background`), information about the execution as a job is saved along with the run information.  
- job IDs use the format `job_YYYYMMDD_HHMMSS_xxxxxxxx`, based on UTC time and a short UUID.
- `job_info.yaml` is the authoritative job metadata and stores the target project/study, command, PID, status, and run list.
- `control.yaml` is the control-request file and stores `pause_requested` and `stop_requested`.
- `stdout.log` and `stderr.log` store the standard output and standard error of the background worker.

## Result output
Results are generally saved in the following location.
```text
<project>/summary/optimization_studies/<study_name>/
```
The main contents are as follows.
```text
runs/
latest.yaml
resultant/
records/   ← `optimization.yaml` > `output_control` > `candidate` > `enabled` が `True` のとき
```
In addition, a copy of the latest run's results is placed directly under the `summary` folder. Refer directly to the `summary` folder when you want to check the latest results.

### `runs/<run_id>/`
This is the result folder for each run.  
```text
summary/optimization_studies/<study>/runs/<run_id>/
```
It mainly contains the following.
- `run_info.yaml`
  - Metadata for the run described above.
- `summary.yaml`
  - Summary of the run results.
- `resultant/`
  - Folder storing the convergence history for single-objective optimization or the final-generation Pareto-front information for multi-objective optimization.
- `records/`
  - Folder storing information about all evaluated individuals.
  - Output when `optimization.yaml` > `output_control` > `candidate` > `enabled` is `True`.

### `latest.yaml`
Metadata identifying the latest run of a study.  
It contains `latest_run_id`.
The `check` command uses this information to open the latest run results for the study.

### Cross-study results
An aggregate table across studies (containing all individual data) is also created for the project.  
It is output when `optimization.yaml` > `output_control` > `candidate` > `enabled` is `True`.
```text
<project>/summary/cross_study/cross_study_individuals.csv
```

### Exporting data for a surrogate model
The `export_surrogate_data` command extracts training data conditionally from the cross-study table.
```bash
python emsopt.py export_surrogate_data <project_name> --study-names <study1> <study2>
```
The output directory is `summary/cross_study/`.

## Comparing and analyzing multiple runs
Compare and analyze multiple runs with the `analyze_runs` command.
```bash
python emsopt.py analyze_runs <project_name> --study-name <study>
python emsopt.py analyze_runs <project_name> --study-name <study> --run-ids run_0001 run_0002
```
The output directory is as follows.
```text
summary/optimization_studies/<study>/analysis/
```

The main outputs are as follows.

### Common
- `run_status.csv`
  - Status list for each run
- `run_health.yaml`
  - Aggregated success rate, failure rate, and failure reasons

Example:
- `num_runs`
- `status_counts`
- `success_rate`
- `failure_rate`
- `failure_reason_counts`

### Single-objective
The best objective values from multiple runs are compared and statistics are output.
- `single_objective_run_comparison.csv`
- `single_objective_runs.png`
- `single_objective_stats.yaml`

### Multi-objective
The Pareto-front hypervolume values from multiple runs are compared and statistics are output.
- `multi_objective_hypervolume.csv`
- `multi_objective_pareto.png`
- `multi_objective_stats.yaml`

## Choosing an approach
### To experiment with new conditions
- Create a new study with the `mk_study` command.
- For derived conditions, use `--from-study`.

### To run the same conditions multiple times
- Use the `run` or `batch_run` command for the same study.
- Runs increase as `run_0001`, `run_0002`, and so on.
:::warning
The `optimizer` implementation examples have an optional `seed` argument. This specifies the random seed for optimization and ensures reproducibility. **To obtain different results for each run, leave the `seed` argument unspecified.**  
In particular, when `batch_run` is executed, the arguments in `optimization.yaml` are used for every run. Therefore, specifying `seed` is expected to produce exactly the same optimization results for all runs.  
:::

### To quickly view only the latest results
- Use the `check` command.
- Or refer to `summary/optimization_studies/<study>/resultant/`.

### To view differences or success rates between runs
- Use the `analyze_runs` command.
- Check the output in `analysis/`.

### To reuse data across studies
- `summary/cross_study/cross_study_individuals.csv`
- Use `export_surrogate_data` when only a subset of the data is needed.
