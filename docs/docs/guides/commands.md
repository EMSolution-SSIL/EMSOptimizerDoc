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

## プリ処理
### show_avl
#### Usage
```sh
python emsopt.py show_avl \[-n {オブジェクト名}\]
```
#### Description
このコマンドは`optimization.yaml`ファイル内に設定可能なEMSOptimizerコアオブジェクトの一覧を示します。また、`-n`オプションにオブジェクト名を指定することで、そのオブジェクトのドキュメントを表示します。

### cp_proj
#### Usage
```sh
python emsopt.py cp_proj {コピー元プロジェクト名} {コピー先プロジェクト名} [--project-root {プロジェクトルート}]
```
#### Description
このコマンドはプロジェクトをコピーします。コピー元のプロジェクトは`project`フォルダ内から選択します。コピー先のプロジェクトは`project`フォルダ内に自動的に作成されます。
#### --project-root \{プロジェクトルート\}
プロジェクトフォルダのルートパス。未指定の場合、実行元ディレクトリの`projects`フォルダが参照される。

### mk_study
#### Usage
```sh
python emsopt.py mk_study {プロジェクト名} {スタディ名} [--project-root {プロジェクトルート}]
```
#### Description
このコマンドはプロジェクトをコピーします。コピー元のプロジェクトは`project`フォルダ内から選択します。コピー先のプロジェクトは`project`フォルダ内に自動的に作成されます。
#### --project-root \{プロジェクトルート\}
プロジェクトフォルダのルートパス。未指定の場合、実行元ディレクトリの`projects`フォルダが参照される。

### cln_proj
#### Usage
```sh
python emsopt.py cln_proj {プロジェクト名} [--project-root {プロジェクトルート}] [--remove-summary] [--remove-studies] [--yes]
```
#### Description
このコマンドは指定したプロジェクトに格納された中間フォルダ（`resources`, `opt_progress`）を削除します。
#### --project-root \{プロジェクトルート\}
プロジェクトフォルダのルートパス。未指定の場合、実行元ディレクトリの`projects`フォルダが参照される。
#### --remove-summary
中間フォルダの削除に加え，最適化結果サマリーフォルダ（`summary`）を削除します。
#### --remove-studies
中間フォルダの削除に加え，プロジェクト内に存在するすべてのスタディを削除します。
#### --yes
確認メッセージをスキップし，即座に削除処理を行います。
:::warning
`cln_proj`を実行すると、**プロジェクトに格納された最適化経過・結果ファイルが削除されるためご注意ください**。削除されたファイルは元に戻せません。  
また、`check`コマンドによる最適化結果の表示は`summary`フォルダを読み込むことによって行います。そのため、`cln_proj --remove-summary`実行後は`check`コマンドによる最適化結果の確認ができません。  
:::

### rm_proj
#### Usage
```sh
python emsopt.py rm_proj {プロジェクト名} [--project-root {プロジェクトルート}] [--yes]
```
#### Description
このコマンドは`project`フォルダ内の指定したプロジェクトを削除します。
#### --project-root \{プロジェクトルート\}
プロジェクトフォルダのルートパス。未指定の場合、実行元ディレクトリの`projects`フォルダが参照される。
#### --yes
確認メッセージをスキップし，即座に削除処理を行います。
:::warning
**削除されたプロジェクトは元に戻せないため、ご注意ください**。  
:::

### save_tpl
#### Usage
```sh
python emsopt.py save_tpl {プロジェクト名} {テンプレート名} [--project-root {プロジェクトルート}] [--study-name {スタディ名}]
```
#### Description
このコマンドは指定したプロジェクトの`optimization_problem.yaml`の内容をテンプレートとして保存します。保存した設定は`project/template.yaml`ファイル内に格納され、`load_tpl`コマンドによって読み込み可能な状態になります。
#### --project-root \{プロジェクトルート\}
プロジェクトフォルダのルートパス。未指定の場合、実行元ディレクトリの`projects`フォルダが参照される。
#### --study-name \{スタディ名\}
参照するスタディ名。未指定の場合、プロジェクト直下のコンフィグファイルを元に`defaults`スタディが作成・参照される。

### load_tpl
#### Usage
```sh
python emsopt.py load_tpl {プロジェクト名} {テンプレート名} [--project-root {プロジェクトルート}] [--study-name {スタディ名}]
```
#### Description
このコマンドは指定したプロジェクトの`optimization_problem.yaml`にテンプレートの内容をコピーします。
#### --project-root \{プロジェクトルート\}
プロジェクトフォルダのルートパス。未指定の場合、実行元ディレクトリの`projects`フォルダが参照される。
#### --study-name \{スタディ名\}
参照するスタディ名。未指定の場合、プロジェクト直下のコンフィグファイルを元に`defaults`スタディが作成・参照される。

### validate
#### Usage
```sh
python emsopt.py validate {プロジェクト名} [--project-root {プロジェクトルート}] [--study-name {スタディ名}]
```
#### Description
このコマンドは指定したプロジェクトの最適化設定を検証します。
#### --project-root \{プロジェクトルート\}
プロジェクトフォルダのルートパス。未指定の場合、実行元ディレクトリの`projects`フォルダが参照される。
#### --study-name \{スタディ名\}
参照するスタディ名。未指定の場合、プロジェクト直下のコンフィグファイルを元に`defaults`スタディが作成・参照される。

### inspect_mesh
#### Usage
```sh
python emsopt.py inspect_mesh {メッシュファイルパス} [--machine-config {machine.yamlパス}]
```
#### Description
このコマンドは指定したGmshメッシュファイルを解析し、$PhysicalNames の材料ID・名前、physical tagごとの要素種別、節点数、半径範囲、角度範囲を出力します。
`--machine-config`を指定した場合は、machine.yaml の target_ids_and_onoff / mirror_id_map / increment_info とメッシュ物理IDの整合性も確認します。
#### --machine-config \{machine.yamlパス\}
任意。メッシュ物理IDとの整合性確認に使う machine.yaml のパス。未指定の場合、メッシュ単体の情報のみを出力する。

### validate_mesh
#### Usage
```sh
python emsopt.py validate_mesh {プロジェクト名} [--project-root {プロジェクトルート}] [--study-name {スタディ名}] [--mesh {メッシュファイルパス}]
```
#### Description
このコマンドは指定したプロジェクトまたはスタディについて、メッシュとmachine.yamlとの整合性をチェックします。
machine.yaml を読み込み、設計対象メッシュを解析したうえで、target_ids_and_onoff / mirror_id_map / increment_info がメッシュ物理IDと整合しているか確認します。あわせて、設計対象領域の要素種類も出力します。
#### --project-root \{プロジェクトルート\}
プロジェクトフォルダのルートパス。未指定の場合、実行元ディレクトリの projects フォルダが参照される。
#### --study-name \{スタディ名\}
参照するスタディ名。未指定の場合、プロジェクト直下の machine.yaml を参照する。
#### --mesh \{メッシュファイルパス\}
検査対象メッシュを明示的に指定する。未指定の場合、machine.yaml の analysis_dimension と design_target から設計対象メッシュ名を解決し、プロジェクトまたはスタディ配下から探索する。

## 実行処理
### run
#### Usage
```sh
python emsopt.py run {プロジェクト名} [--project-root {プロジェクトルート}] [--study-name {スタディ名}] [--background]
```
#### Description
このコマンドは指定したプロジェクトの最適化計算を実行します。最適化が完了するとプロジェクトフォルダ内に最適化サマリー`summary`フォルダが自動生成され、これは`check`コマンドによって読み込まれます。
:::warning
プロジェクトフォルダ内に中間ファイルおよびサマリーフォルダが既に存在する場合、その内容は上書きされます。
:::
#### --project-root \{プロジェクトルート\}
プロジェクトフォルダのルートパス。未指定の場合、実行元ディレクトリの`projects`フォルダが参照される。
#### --study-name \{スタディ名\}
参照するスタディ名。未指定の場合、プロジェクト直下のコンフィグファイルを元に`defaults`スタディが作成・参照される。

### batch_run
#### Usage
```sh
python emsopt.py batch_run {プロジェクト名} {バッチサイズ（＝実行するランの数）} [--project-root {プロジェクトルート}] [--study-name {スタディ名}] [--stop-on-error] [--background]
```
#### Description
このコマンドは指定したプロジェクトの最適化計算をバッチ実行します。バッチ内の各実行結果はランとして`summary`フォルダ内に保存されます。
:::info
`batch_run`実行時，GUI表示は強制的にオフになります。
:::
#### --project-root \{プロジェクトルート\}
プロジェクトフォルダのルートパス。未指定の場合、実行元ディレクトリの`projects`フォルダが参照される。
#### --study-name \{スタディ名\}
参照するスタディ名。未指定の場合、プロジェクト直下のコンフィグファイルを元に`defaults`スタディが作成・参照される。
#### --stop-on-error
このオプションを指定した場合，エラー発生時にバッチ実行全体を中断する。未指定の場合，失敗ランは中断し，残りのランを続けて実行する。

### sample
```sh
python emsopt.py sample {プロジェクト名} {サンプル数} [--project-root {プロジェクトルート}] [--study-name {スタディ名}] [--chunk-size {チャンクサイズ}] [--background]
```
#### Description
このコマンドは指定したプロジェクトに設定された設計変数の範囲内でラテン超立方体サンプリング\[25\]を実行します。サンプリング結果は通常の最適化と同様に`summary`フォルダに格納されます。
#### --project-root \{プロジェクトルート\}
プロジェクトフォルダのルートパス。未指定の場合、実行元ディレクトリの`projects`フォルダが参照される。
#### --study-name \{スタディ名\}
参照するスタディ名。未指定の場合、プロジェクト直下のコンフィグファイルを元に`defaults`スタディが作成・参照される。
#### --chunk-size \{チャンクサイズ\}
チャンクサイズ。サンプル数を指定のチャンクサイズ（一度にまとめて評価されるサンプル数）に分割して評価します。未指定の場合，適切なチャンクサイズが自動的に設定されます。

## ジョブ管理
### job_list
#### Usage
```sh
python emsopt.py job_list {プロジェクト名} [--project-root {プロジェクトルート}] [--study-name {スタディ名}]
```
#### Description
指定したプロジェクト・スタディに紐づくバックグラウンドジョブ一覧を表示します。対象は`run --background`、`batch_run --background`、`sample --background`によって開始されたジョブです。
各ジョブの job_id、pid、状態、現在実行中のrun、関連run一覧などを確認できます。
#### --project-root \{プロジェクトルート\}
プロジェクトフォルダのルートパス。未指定の場合、実行元ディレクトリのprojectsフォルダが参照される。
#### --study-name \{スタディ名\}
参照するスタディ名。未指定の場合、プロジェクト直下のコンフィグファイルを元にdefaultスタディが作成・参照される。

### job_status
#### Usage
```sh
python emsopt.py job_status {プロジェクト名} --job-id {ジョブID} [--project-root {プロジェクトルート}] [--study-name {スタディ名}]
```
#### Description
指定したバックグラウンドジョブの現在状態を表示します。状態には running、pausing、paused、stopping、stopped、completed、failed、lostがあります。
lostはジョブ情報上は実行中だが、対応するプロセスが存在しない場合に表示されます。
#### --job-id \{ジョブID\}
操作対象のバックグラウンドジョブID。run --background、batch_run --background、sample --background 実行時の戻り値、または job_list で確認できる。
#### --project-root \{プロジェクトルート\}
プロジェクトフォルダのルートパス。未指定の場合、実行元ディレクトリのprojectsフォルダが参照される。
#### --study-name \{スタディ名\}
参照するスタディ名。未指定の場合、プロジェクト直下のコンフィグファイルを元にdefaultスタディが作成・参照される。

### job_pause
#### Usage
```sh
python emsopt.py job_pause {プロジェクト名} --job-id {ジョブID} [--project-root {プロジェクトルート}] [--study-name {スタディ名}]
```
#### Description
実行中のバックグラウンドジョブに一時停止要求を送ります。
:::warning
一時停止は即時割り込みではなく、最適化ループの安全な制御チェック点で反映されます。`run` / `batch_run`ではiteration境界、`sample`ではチャンク境界で停止します。
:::
#### --job-id \{ジョブID\}
一時停止対象のバックグラウンドジョブID。
#### --project-root \{プロジェクトルート\}
プロジェクトフォルダのルートパス。未指定の場合、実行元ディレクトリのprojectsフォルダが参照される。
#### --study-name \{スタディ名\}
参照するスタディ名。未指定の場合、プロジェクト直下のコンフィグファイルを元にdefaultスタディが作成・参照される。

### job_resume
#### Usage
```sh
python emsopt.py job_resume {プロジェクト名} --job-id {ジョブID} [--project-root {プロジェクトルート}] [--study-name {スタディ名}]
```
#### Description
一時停止中のバックグラウンドジョブに再開要求を送ります。job_pauseによりpausedになったジョブは、このコマンドによりrunningに戻ります。
#### --job-id \{ジョブID\}
再開対象のバックグラウンドジョブID。
#### --project-root \{プロジェクトルート\}
プロジェクトフォルダのルートパス。未指定の場合、実行元ディレクトリのprojectsフォルダが参照される。
#### --study-name \{スタディ名\}
参照するスタディ名。未指定の場合、プロジェクト直下のコンフィグファイルを元にdefaultスタディが作成・参照される。

### job_stop
#### Usage
```sh
python emsopt.py job_stop {プロジェクト名} --job-id {ジョブID} [--project-root {プロジェクトルート}] [--study-name {スタディ名}]
```
#### Description
実行中または一時停止中のバックグラウンドジョブに停止要求を送ります。停止要求を受けたジョブは、安全な制御チェック点で終了し、該当runのrun_info.yamlにはstoppedとして記録されます。  
:::warning
このコマンドはプロセスを強制終了するものではありません。CAE解析や並列評価の途中で破壊的に中断せず、EMSOptimizer側の制御チェック点で協調的に停止します。
:::
#### --job-id \{ジョブID\}
停止対象のバックグラウンドジョブID。
#### --project-root \{プロジェクトルート\}
プロジェクトフォルダのルートパス。未指定の場合、実行元ディレクトリのprojectsフォルダが参照される。
#### --study-name \{スタディ名\}
参照するスタディ名。未指定の場合、プロジェクト直下のコンフィグファイルを元にdefaultスタディが作成・参照される。

## ポスト処理
### check
#### Usage
```sh
python emsopt.py check {プロジェクト名} [--project-root {プロジェクトルート}] [--study-name {スタディ名}] [--run-id {ランID}]
```
#### Description
このコマンドは指定したプロジェクトの最適化経過をGUI上に表示します。具体的には、`run`コマンドによる最適化が完了した後に生成される`summary`フォルダを読み込み、その内容をGUI上に表示します。
#### --project-root \{プロジェクトルート\}
プロジェクトフォルダのルートパス。未指定の場合、実行元ディレクトリの`projects`フォルダが参照される。
#### --study-name \{スタディ名\}
参照するスタディ名。未指定の場合、プロジェクト直下のコンフィグファイルを元に`defaults`スタディが作成・参照される。
#### --run-id \{ランID\}
参照するランID。未指定の場合、最新ランが参照される。

### export_data
#### Usage
```sh
python emsopt.py export_data {プロジェクト名} [--project-root {プロジェクトルート}] [--study-names {スタディ名1} {スタディ名2} ...] [--statuses {ステータス名1} {ステータス名2} ...]
```
#### Description
このコマンドはプロジェクト内で実行された全スタディの最適化結果CSVから，指定したスタディ・ステータスのデータを抽出してエクスポートします。
#### --project-root \{プロジェクトルート\}
プロジェクトフォルダのルートパス。未指定の場合、実行元ディレクトリの`projects`フォルダが参照される。
#### --study-names \{スタディ名1\} \{スタディ名2\} ...
抽出対象スタディ名。未指定の場合，全スタディからデータを抽出。
#### --statuses \{ステータス名1\} \{ステータス名2\} ...
抽出対象ステータス名。未指定の場合，解析に成功したデータのみを抽出します。
:::info
このコマンドで対象とするCSVは`optimization.yaml` > `output_control` > `candidate` > `enabled`が`True`の時に出力されます。
:::

### analyze_runs
#### Usage
```sh
python emsopt.py analyze_runs {プロジェクト名} [--project-root {プロジェクトルート}] [--study-name {スタディ名}] [--reference-point {HV参照点}] [--run-ids {ランID}] [--gui]
```
#### Description
このコマンドは指定したプロジェクトに存在するラン全体を読み込み，統計情報（単目的なら最良目的関数値，多目的ならハイパーボリューム（HV）の平均・標準偏差）を計算します。計算結果は`summary/analysis`フォルダに出力されます。
#### --project-root \{プロジェクトルート\}
プロジェクトフォルダのルートパス。未指定の場合、実行元ディレクトリの`projects`フォルダが参照される。
#### --study-name \{スタディ名\}
参照するスタディ名。未指定の場合、プロジェクト直下のコンフィグファイルを元に`defaults`スタディが作成・参照される。
#### --reference-point \{HV参照点\}
多目的最適化結果の分析時，HV計算に用いる参照点。  
例：2目的，参照点(1.0, 1.0)の場合，`--reference-point 1.0 1.0`と指定する。
:::warning
参照点はパレートフロントに含まれるどの点よりも悪い（目的関数値が大きい）側に存在する必要がある。
:::
#### --run-ids \{ランID\}
参照するランID。複数指定する（例：`--run-ids run_0001 run_0002 run_0003`）。未指定の場合，スタディ内に存在する全てのランが参照される。
#### --gui
このオプションを指定した場合，複数ランの結果確認用GUIが表示される。
