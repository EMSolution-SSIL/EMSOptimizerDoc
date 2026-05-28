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

## mk_study
### Usage
```sh
python emsopt.py mk_study {プロジェクト名} {スタディ名}
```
### Description
このコマンドはプロジェクトをコピーします。コピー元のプロジェクトは`project`フォルダ内から選択します。コピー先のプロジェクトは`project`フォルダ内に自動的に作成されます。

## cln_proj
### Usage
```sh
python emsopt.py cln_proj {プロジェクト名} [--remove-summary] [--remove-studies] [--yes]
```
### Description
このコマンドは指定したプロジェクトに格納された中間フォルダ（`resources`, `opt_progress`）を削除します。
### --remove-summary
中間フォルダの削除に加え，最適化結果サマリーフォルダ（`summary`）を削除します。
### --remove-studies
中間フォルダの削除に加え，プロジェクト内に存在するすべてのスタディを削除します。
### --yes
確認メッセージをスキップし，即座に削除処理を行います。
:::warning
`cln_proj`を実行すると、**プロジェクトに格納された最適化経過・結果ファイルが削除されるためご注意ください**。削除されたファイルは元に戻せません。  
また、`check`コマンドによる最適化結果の表示は`summary`フォルダを読み込むことによって行います。そのため、`cln_proj --remove-summary`実行後は`check`コマンドによる最適化結果の確認ができません。  
:::

## rm_proj
### Usage
```sh
python emsopt.py rm_proj {プロジェクト名} [--yes]
```
### Description
このコマンドは`project`フォルダ内の指定したプロジェクトを削除します。
### --yes
確認メッセージをスキップし，即座に削除処理を行います。
:::warning
**削除されたプロジェクトは元に戻せないため、ご注意ください**。  
:::

## save_tpl
### Usage
```sh
python emsopt.py save_tpl {プロジェクト名} {テンプレート名} [--study-name {スタディ名}]
```
### Description
このコマンドは指定したプロジェクトの`optimization_problem.yaml`の内容をテンプレートとして保存します。保存した設定は`project/template.yaml`ファイル内に格納され、`load_tpl`コマンドによって読み込み可能な状態になります。
### --study-name {スタディ名}
参照するスタディ名。

## load_tpl
### Usage
```sh
python emsopt.py load_tpl {プロジェクト名} {テンプレート名} [--study-name {スタディ名}]
```
### Description
このコマンドは指定したプロジェクトの`optimization_problem.yaml`にテンプレートの内容をコピーします。
### --study-name {スタディ名}
参照するスタディ名。

## run
### Usage
```sh
python emsopt.py run {プロジェクト名} [--study-name {スタディ名}]
```
### Description
このコマンドは指定したプロジェクトの最適化計算を実行します。最適化が完了するとプロジェクトフォルダ内に最適化サマリー`summary`フォルダが自動生成され、これは`check`コマンドによって読み込まれます。
:::warning
プロジェクトフォルダ内に中間ファイルおよびサマリーフォルダが既に存在する場合、その内容は上書きされます。
:::
### --study-name {スタディ名}
参照するスタディ名。

## check
### Usage
```sh
python emsopt.py check {プロジェクト名} [--study-name {スタディ名}]
```
### Description
このコマンドは指定したプロジェクトの最適化経過をGUI上に表示します。具体的には、`run`コマンドによる最適化が完了した後に生成される`summary`フォルダを読み込み、その内容をGUI上に表示します。
### --study-name {スタディ名}
参照するスタディ名。

## sample
```sh
python emsopt.py sample {プロジェクト名} {サンプル数} [--study-name {スタディ名}] [--chunk-size {チャンクサイズ}]
```
### Description
このコマンドは指定したプロジェクトに設定された設計変数の範囲内でラテン超立方体サンプリング\[25\]を実行します。サンプリング結果は通常の最適化と同様に`summary`フォルダに格納されます。
### --study-name {スタディ名}
参照するスタディ名。
### --chunk-size {チャンクサイズ}
チャンクサイズ。サンプル数を指定のチャンクサイズ（一度にまとめて評価されるサンプル数）に分割して評価します。未指定の場合，適切なチャンクサイズが自動的に設定されます。

## export_surrogate_data
### Usage
```sh
python emsopt.py export_surrogate_data {プロジェクト名} [--study-names {スタディ名1} {スタディ名2} ...] [--statuses {ステータス名1} {ステータス名2} ...]
```
### Description
このコマンドはプロジェクト内で実行された全スタディの最適化結果CSVから，指定したスタディ・ステータスのデータを抽出してエクスポートします。主にサロゲートモデル構築に使用する想定。
### --study-names {スタディ名1} {スタディ名2} ...
抽出対象スタディ名。未指定の場合，全スタディからデータを抽出。
### --statuses {ステータス名1} {ステータス名2} ...
抽出対象ステータス名。未指定の場合，解析に成功したデータのみを抽出します。
:::info
このコマンドで対象とするCSVは`optimization.yaml` > `output_control` > `candidate` > `enabled`が`True`の時に出力されます。
:::

## batch_run
### Usage
```sh
python emsopt.py batch_run {プロジェクト名} {バッチサイズ（＝実行するランの数）} [--study-name {スタディ名}] [--stop-on-error]
```
### Description
このコマンドは指定したプロジェクトの最適化計算をバッチ実行します。バッチ内の各実行結果はランとして`summary`フォルダ内に保存されます。
:::info
`batch_run`実行時，GUI表示は強制的にオフになります。
:::
### --study-name {スタディ名}
参照するスタディ名。
### --stop-on-error
このオプションを指定した場合，エラー発生時にバッチ実行全体を中断する。未指定の場合，失敗ランは中断し，残りのランを続けて実行する。

## analyze_runs
### Usage
```sh
python emsopt.py analyze_runs {プロジェクト名} [--study-name {スタディ名}] [--reference-point {HV参照点}] [--run-ids {ランID}] [--gui]
```
### Description
このコマンドは指定したプロジェクトに存在するラン全体を読み込み，統計情報（単目的なら最良目的関数値，多目的ならハイパーボリューム（HV）の平均・標準偏差）を計算します。計算結果は`summary/analysis`フォルダに出力されます。
### --study-name {スタディ名}
参照するスタディ名。
### --reference-point {HV参照点}
多目的最適化結果の分析時，HV計算に用いる参照点。  
例：2目的，参照点(1.0, 1.0)の場合，`--reference-point 1.0 1.0`と指定する。
:::warning
参照点はパレートフロントに含まれるどの点よりも悪い（目的関数値が大きい）側に存在する必要がある。
:::
### --run-ids {ランID}
参照するランID。複数指定する（例：`--run-ids run_0001 run_0002 run_0003`）。未指定の場合，スタディ内に存在する全てのランが参照される。
### --gui
このオプションを指定した場合，複数ランの結果確認用GUIが表示される。

## show_avl
### Usage
```sh
python emsopt.py show_avl \[-n {オブジェクト名}\]
```
### Description
このコマンドは`optimization.yaml`ファイル内に設定可能なEMSOptimizerコアオブジェクトの一覧を示します。また、`-n`オプションにオブジェクト名を指定することで、そのオブジェクトのドキュメントを表示します。
