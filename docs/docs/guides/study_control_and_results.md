---
sidebar_position: 5
---

# スタディコントロールと結果確認
## 全体像
EMSOptimizerでは、最適化の実行・結果は次の3階層で管理されます。
- `project`
  - 最適化対象そのものを切り分ける単位。メッシュファイル、解析条件フォルダはここに入れる。
- `study`
  - 最適化条件ごとの単位
  - `<project>/optimization_studies/`フォルダに作成される
  - `optimization.yaml`、`machine.yaml`、`optimization_problem.yaml` を持つ
- `run`
  - スタディの実行単位
  - `<project>/summary/optimization_studies/<study_name>/`フォルダに作成される
  - 同じスタディを複数回実行すると、ランが増えていく

## スタディの作成・管理
### スタディの作成
スタディは `mk_study` コマンドで作成します。
```bash
python emsopt.py mk_study <project_name> <study_name>
python emsopt.py mk_study <project_name> <study_name> --from-study <source_study>
```
コピー対象は以下です。
- `optimization.yaml`
- `machine.yaml`
- `optimization_problem.yaml`

既存スタディを上書きしないよう、同名スタディがある場合はエラーになります。

### `default`スタディの自動作成
`run`、`sample`、`check`、`analyze_runs` などで `--study-name` を省略した場合は、`default`スタディが対象になります。  
このとき `default` がなければ、プロジェクトルートのコンフィグファイル群をコピーして自動作成されます。
つまり、最初はスタディを明示的に作らなくても、`default`を起点に使い始められます。

## ランの作成・管理
### ランの作成
ランは主に次のコマンドを実行したとき，`summary`フォルダ内に自動的に作られます。
```bash
python emsopt.py run <project_name> --study-name <study>
python emsopt.py batch_run <project_name> <num_runs> --study-name <study>
python emsopt.py sample <project_name> <num_sample> --study-name <study>
```
- `run`
  - 最適化を1回実行し，1つのランとして保存
- `batch_run`
  - 同一スタディを複数回独立実行し，それぞれをランとして保存
- `sample`
  - LHSサンプルを評価して、1つのランとして保存

### ランIDの付け方
ランはスタディごとに連番で採番されます。
- `run_0001`
- `run_0002`
- `run_0003`

### 実行状態の管理
各ランに作成される`run_info.yaml`は，次の情報を有します：
- `run_id`
- `study_name`
- `status`（最適化の成功・失敗記録）
- `started_at`
- `finished_at`
- `failure_reason`
- `updated_at`

## 結果出力
結果は基本的に次に保存されます。
```text
<project>/summary/optimization_studies/<study_name>/
```
その下に主に以下があります。
```text
runs/
latest.yaml
resultant/
records/   ← `optimization.yaml` > `output_control` > `candidate` > `enabled` が `True` のとき
```
また，これとは別に，最新ランの実行結果のコピーが`summary`フォルダ直下に配置されます。最新の結果を確認したいときは`summary`フォルダ直下を参照できます。

### `runs/<run_id>/`
各ランの実行結果フォルダです。  
```text
summary/optimization_studies/<study>/runs/<run_id>/
```
ここには主に以下が入ります。
- `run_info.yaml`
  - 上述のランのメタ情報です。
- `summary.yaml`
  - ランの実施結果サマリーです。
- `resultant/`
  - 単目的なら収束履歴，多目的なら最終世代のパレートフロント情報を保存するフォルダです。
- `records/`
  - 解析した全個体の情報を保存するフォルダです。
  - `optimization.yaml` > `output_control` > `candidate` > `enabled` が `True` sのときに出力されます。

### `latest.yaml`
スタディの最新ランを指すメタ情報です。  
中には `latest_run_id` が入ります。
`check`コマンドはこの情報を使って、「そのスタディの最新ラン結果」を開きます。

### プロジェクト横断結果
プロジェクト全体では、スタディ横断の集約テーブル（全個体データ）も作られます。  
`optimization.yaml` > `output_control` > `candidate` > `enabled` が `True`のときに出力されます。
```text
<project>/summary/cross_study/cross_study_individuals.csv
```

### surrogate 用データ出力
`export_surrogate_data`コマンドを使うと、cross-study テーブルから条件付きで学習データを切り出せます。
```bash
python emsopt.py export_surrogate_data <project_name> --study-names <study1> <study2>
```
出力先は `summary/cross_study/` です。

## 複数ランの比較・分析
複数ランの比較・分析は `analyze_runs`コマンドによって実施できます。
```bash
python emsopt.py analyze_runs <project_name> --study-name <study>
python emsopt.py analyze_runs <project_name> --study-name <study> --run-ids run_0001 run_0002
```
出力先は以下です。
```text
summary/optimization_studies/<study>/analysis/
```

主な出力は次の通りです。

### 共通
- `run_status.csv`
  - run ごとの状態一覧
- `run_health.yaml`
  - 成功率、失敗率、失敗理由集計

例:
- `num_runs`
- `status_counts`
- `success_rate`
- `failure_rate`
- `failure_reason_counts`

### 単目的
複数ランの最良目的関数値の比較および統計が出力されます。
- `single_objective_run_comparison.csv`
- `single_objective_runs.png`
- `single_objective_stats.yaml`

### 多目的
複数ランのパレートフロントハイパーボリューム値の比較および統計が出力されます。
- `multi_objective_hypervolume.csv`
- `multi_objective_pareto.png`
- `multi_objective_stats.yaml`

## 使い分け
### 新しい条件で実験したい
- `mk_study` コマンドで新しい study を作る
- 派生条件なら `--from-study` を使う

### 同じ条件で複数回回したい
- 同じ study に対して `run` または `batch_run` コマンド
- run は `run_0001`, `run_0002` と増える
:::warning
`optimizer`の実装例にはオプショナル引数として`seed`が存在します。これは，最適化の乱数シードを指定し，再現性を担保する引数です。**ランごとに異なる結果を得たい場合，`seed`引数を未指定にする必要がある**ことに注意してください。  
特に，`batch_run`コマンドを実行した場合，`optimization.yaml`に記載された引数情報がすべてのランで使用されます。したがって，`seed`引数を指定していると，すべてのランで全く同じ最適化結果となることが期待されます。  
:::

### 最新結果だけすぐ見たい
- `check` コマンド
- または `summary/optimization_studies/<study>/resultant/`

### ランごとの差や成功率を見たい
- `analyze_runs` コマンド
- 出力は `analysis/` を見る

### スタディをまたいで再利用したい
- `summary/cross_study/cross_study_individuals.csv`
- 一部データのみ利用したいなら`export_surrogate_data`
