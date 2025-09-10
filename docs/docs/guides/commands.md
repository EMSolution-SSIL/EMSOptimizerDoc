---
sidebar_position: 1
---

# Available Commands
ここでは、EMOptSolutionで利用可能なコマンド一覧を紹介します。なお、各コマンドのヘルプは以下のコマンドでも確認できます。

```sh
python emopt.py -h
```
```sh
python emopt.py {コマンド名} -h
```

## cp_proj
### Usage
```sh
python emopt.py cp_proj {コピー元プロジェクト名} {コピー先プロジェクト名}
```
### Description
このコマンドはプロジェクトをコピーします。コピー元のプロジェクトは`project`フォルダ内から選択します。コピー先のプロジェクトは`project`フォルダ内に自動的に作成されます。

## rm_proj
### Usage
```sh
python emopt.py rm_proj {プロジェクト名}
```
### Description
このコマンドは`project`フォルダ内の指定したプロジェクトを削除します。

## save_tpl
### Usage
```sh
python emopt.py save_tpl {プロジェクト名} {テンプレート名}
```
### Description
このコマンドは指定したプロジェクトの`optimization_problem.yaml`の内容をテンプレートとして保存します。保存した設定は`project/template.yaml`ファイル内に格納され、`load_tpl`コマンドによって読み込み可能な状態になります。

## load_tpl
### Usage
```sh
python emopt.py load_tpl {プロジェクト名} {テンプレート名}
```
### Description
このコマンドは指定したプロジェクトの`optimization_problem.yaml`にテンプレートの内容をコピーします。

## run
### Usage
```sh
python emopt.py run {プロジェクト名}
```
### Description
このコマンドは指定したプロジェクトの最適化計算を実行します。最適化が完了するとプロジェクトフォルダ内に`summary`フォルダが自動生成され、これは`check`コマンドによって読み込まれます。

## check
### Usage
```sh
python emopt.py check {プロジェクト名}
```
### Description
このコマンドは指定したプロジェクトの最適化経過をGUI上に表示します。具体的には、`run`コマンドによる最適化が完了した後に生成される`summary`フォルダを読み込み、その内容をGUI上に表示します。

## show_avl
### Usage
```sh
python emopt.py show_avl \[-n {オブジェクト名}\]
```
### Description
このコマンドは`optimization.yaml`ファイル内に設定可能なEMOptSolutionコアオブジェクトの一覧を示します。また、`-n`オプションにオブジェクト名を指定することで、そのオブジェクトのドキュメントを表示します。
