---
sidebar_position: 1
---

# コマンドリスト
ここでは、EMSOptimizerで利用可能なコマンド一覧を紹介します。なお、各コマンドのヘルプは以下のコマンドでも確認できます。

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
このコマンドはプロジェクトをコピーします。コピー元のプロジェクトは`project`フォルダ内から選択します。コピー先のプロジェクトは`project`フォルダ内に自動的に作成されます。

## cln_proj
### Usage
```sh
python emsopt.py cln_proj {プロジェクト名}
```
### Description
このコマンドは`project`フォルダ内の指定したプロジェクトに格納された中間フォルダ等を削除します。具体的には、デフォルトの中間フォルダ（`resources`, `opt_progress`）および最適化結果サマリーフォルダ（`summary`）を削除します。
:::warning
`cln_proj`を実行すると、**プロジェクトに格納された最適化経過・結果ファイルが削除されるためご注意ください**。削除されたファイルは元に戻せません。  
また、`check`コマンドによる最適化結果の表示は`summary`フォルダを読み込むことによって行います。そのため、`cln_proj`実行後は最適化結果の確認ができません。  
:::

## rm_proj
### Usage
```sh
python emsopt.py rm_proj {プロジェクト名}
```
### Description
このコマンドは`project`フォルダ内の指定したプロジェクトを削除します。
:::warning
**削除されたプロジェクトは元に戻せないため、ご注意ください**。  
:::

## save_tpl
### Usage
```sh
python emsopt.py save_tpl {プロジェクト名} {テンプレート名}
```
### Description
このコマンドは指定したプロジェクトの`optimization_problem.yaml`の内容をテンプレートとして保存します。保存した設定は`project/template.yaml`ファイル内に格納され、`load_tpl`コマンドによって読み込み可能な状態になります。

## load_tpl
### Usage
```sh
python emsopt.py load_tpl {プロジェクト名} {テンプレート名}
```
### Description
このコマンドは指定したプロジェクトの`optimization_problem.yaml`にテンプレートの内容をコピーします。

## run
### Usage
```sh
python emsopt.py run {プロジェクト名}
```
### Description
このコマンドは指定したプロジェクトの最適化計算を実行します。最適化が完了するとプロジェクトフォルダ内に最適化サマリー`summary`フォルダが自動生成され、これは`check`コマンドによって読み込まれます。
:::warning
プロジェクトフォルダ内に中間ファイルおよびサマリーフォルダが既に存在する場合、その内容は上書きされます。
:::

## check
### Usage
```sh
python emsopt.py check {プロジェクト名}
```
### Description
このコマンドは指定したプロジェクトの最適化経過をGUI上に表示します。具体的には、`run`コマンドによる最適化が完了した後に生成される`summary`フォルダを読み込み、その内容をGUI上に表示します。

## show_avl
### Usage
```sh
python emsopt.py show_avl \[-n {オブジェクト名}\]
```
### Description
このコマンドは`optimization.yaml`ファイル内に設定可能なEMSOptimizerコアオブジェクトの一覧を示します。また、`-n`オプションにオブジェクト名を指定することで、そのオブジェクトのドキュメントを表示します。
