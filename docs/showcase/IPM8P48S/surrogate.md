---
sidebar_position: 3
---

# IPM8P48Sサロゲート利用例
ここでは`IPM8P48S_surrogate`プロジェクトの内容について紹介します。  
このプロジェクトでは、IPM8P48Sモデルの寸法最適化を実施し、その結果を応答曲面（ランダムフォレスト利用）として可視化します。
:::info
本プロジェクトの最適化の実施にはeMotorSolution APIが必要です。
:::

## optimization.yaml（`IPM8P48S_surrogate`プロジェクト）
[IPM8P48S寸法およびトポロジー同時最適化](./pto.md)と同様に、`ems_shape_builder`に`HoleMagnet55`を指定することで、永久磁石＋フラックスバリアの寸法最適化を行います。ここでは簡単のためにトポロジー最適化用の設定は無しとし、純粋な寸法最適化をeMotorSolution連携にて行います。  
また、最適化問題（optimization_problem.yaml）は[IPM8P48S説明＆基本の最適化例](./basic_moo.md)と同様に、平均トルク最大化・トルクリプル最小化の多目的最適化です。`optimizer`には`nsga2`を選択しました。
```yaml
evaluator:
  name: pyemsol_shape_evaluator
ems_shape_builder:
  name: HoleMagnet55
optimizer:
  name: nsga2
  kwargs:
    population_size: 20
    seed: 42
    bounds: [[40, 45], [1.5, 2.5], [1.0, 2.0], [11, 13], [20, 22],
             [16, 20], [1.0, 2.0], [0.5, 1.5], [4.0, 6.0], [0.0, 1.0]]
```

ここでは、最適化中の全解析データを応答曲面の構築に利用するため、`candidate`の出力を有効（`enabled: True`）としています。  
さらに、`check`コマンド起動時に応答曲面を構築するオプションを`response_surface`に設定しています。
```yaml
# output functionality
output_interval: 1
output_control:
  best_individual:
    filename_base: best_individual
    enabled: True
    output_interval: 1
  candidate:
    filename_base: candidate
    enabled: True
    output_interval: 1
  candidate_plot:
    filename_base: candidate_plot
    enabled: True
    output_interval: 10
enable_progress_gui: True
response_surface:
  enabled: True
  grid_size: 50
  min_samples: 5
  n_estimators: 200
  random_state: 0
```

## 最適化の実施例
50イテレーション最適化完了後のGUIを以下に示します。平均トルク・トルクリプルについて、幅広いパレートフロントが得られたことが分かります。  
![IPM8P48S surrogate結果](/img/IPM8P48S_surrogate_check.png)

また、`Responce Surface`タブ（応答曲面による可視化）について、平均トルクに関する可視化結果を以下に示します。上は応答曲面、下はランダムフォレストから導かれた各設計変数（寸法パラメータ）の重要度です。  
これらの図から、例えば10番目の設計変数（回転子表面リブ厚さ）は特に平均トルクへの影響が大きく、この値を小さくするほど平均トルクが向上することが分かります。実際の設計時には様々な要因を考慮して変数を決める必要がありますが、少なくとも最適化において評価した性能値と設計変数との関係性については、この応答曲面からヒントを得ることができます。  
![IPM8P48S surrogate結果（応答曲面）](/img/IPM8P48S_surrogate_check_rs.png)

## サロゲートモデルを利用した最適化
さらに、上記の最適化で集めたデータを用いて、応答曲面（サロゲートモデル）上を探索する最適化を実施することが可能です。  
例として、以下のように`sa_nsga2`（[サロゲートモデル補助付NSGA-II](../../docs/guides/Optimizer/sa_nsga2.md)）optimizerを使用した最適化を実施します。ここでは、元のパレートフロントにおいて解のバリエーションが薄かった平均トルク16.5Nm、トルクリプル40.0%を集中的に探索するR-NSGA-IIを実行します。  
`data_csv_path`には、前述の最適化で得られたcsvファイルへのパスを指定します。そのほか、各種引数やアルゴリズムの詳細は上記optimizerページおよび原著論文をご覧ください。  
```yaml
optimizer:
  name: sa_nsga2
  kwargs:
    population_size: 20
    reference_points: [[-16.5, 40.0]]
    seed: 42
    bounds: [[40, 45], [1.5, 2.5], [1.0, 2.0], [11, 13], [20, 22],
             [16, 20], [1.0, 2.0], [0.5, 1.5], [4.0, 6.0], [0.0, 1.0]]
    surrogate_mode: full_loop
    eval_init_population_truly: False
    data_csv_path: "Path/To/EMSOptimizer/projects/IPM8P48S_surrogate/summary/cross_study/cross_study_individuals.csv"
ems_shape_builder:
  name: HoleMagnet55

# optimization settings
num_iteration: 1  # サロゲート補助の最適化を1回実行する設定
enable_parallelization: True
num_processes: Null  # if Null, automatically set from cpu counts
```

下図に実行結果を示します。サロゲートモデルを利用した最適化により、少ない追加計算量にて参照点[-16.5Nm, 40.0%]に近い範囲に新たなパレートフロントが得られました。
![IPM8P48S surrogate sa結果](/img/IPM8P48S_surrogate_sa_check.png)
