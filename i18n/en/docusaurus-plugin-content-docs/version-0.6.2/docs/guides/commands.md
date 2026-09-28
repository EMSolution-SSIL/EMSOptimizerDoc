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

## cp_proj
### Usage
```sh
python emsopt.py cp_proj {コピー元プロジェクト名} {コピー先プロジェクト名}
```
### Description
This command copies a project. The source project is selected from the `project` folder, and the destination project is created automatically in the `project` folder.

## cln_proj
### Usage
```sh
python emsopt.py cln_proj {プロジェクト名}
```
### Description
This command removes intermediate folders and similar data stored in the specified project under the `project` folder. Specifically, it removes the default intermediate folders (`resources`, `opt_progress`) and the optimization-result summary folder (`summary`).
:::warning
Running `cln_proj` **deletes optimization-progress and result files stored in the project**. Deleted files cannot be restored.  
The `check` command displays optimization results by reading the `summary` folder. Therefore, the results cannot be inspected after running `cln_proj`.  
:::

## rm_proj
### Usage
```sh
python emsopt.py rm_proj {プロジェクト名}
```
### Description
This command deletes the specified project in the `project` folder.
:::warning
**Deleted projects cannot be restored.**  
:::

## save_tpl
### Usage
```sh
python emsopt.py save_tpl {プロジェクト名} {テンプレート名}
```
### Description
This command saves the specified project's `optimization_problem.yaml` as a template. The saved settings are stored in `project/template.yaml` and can be loaded with `load_tpl`.

## load_tpl
### Usage
```sh
python emsopt.py load_tpl {プロジェクト名} {テンプレート名}
```
### Description
This command copies the template contents into the specified project's `optimization_problem.yaml`.

## run
### Usage
```sh
python emsopt.py run {プロジェクト名}
```
### Description
This command runs optimization for the specified project. When optimization finishes, an optimization summary `summary` folder is generated in the project folder and loaded by the `check` command.
:::warning
If intermediate files or a summary folder already exist in the project folder, their contents are overwritten.
:::

## check
### Usage
```sh
python emsopt.py check {プロジェクト名}
```
### Description
This command displays optimization progress for the specified project in the GUI. Specifically, it loads the `summary` folder generated after optimization with `run` and displays its contents in the GUI.

## show_avl
### Usage
```sh
python emsopt.py show_avl \[-n {オブジェクト名}\]
```
### Description
This command lists the EMSOptimizer core objects that can be configured in `optimization.yaml`. Specify an object name with the `-n` option to display its documentation.
