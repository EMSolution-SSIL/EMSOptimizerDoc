---
sidebar_position: 1
---

# Dmodel説明＆基本の最適化例
ここでは、Dmodelの説明、および`Dmodel`プロジェクトの内容について紹介します。

## モデル説明
Dmodelは4極24スロット（分布巻）の埋め込み型永久磁石同期モータ（IPMSM）モデルです。IPMSMの標準モデルとして広く使用されています。  
`Dmodel`プロジェクト同梱のメッシュは1/4部分モデルで、各領域には材料情報（材料番号：材料名）が割り当てられています。  
下図はロータ部分のモデルと材料情報です。トポロジー最適化のため、元のモデルにあった空気穴（フラックスバリア）はロータコアで埋めてあります。特筆すべき点として、`40: "air"`はスライドメッシュ領域であり、この領域のみ均一な四角形メッシュによって要素分割してあります。

![Dmodel example](/img/Dmodel_ex.png)

## machine.yaml（`Dmodel`プロジェクト）
まず、機器情報を設定する`machine.yaml`の内容を確認します。
### 基本設定
Dmodelは半径と角度（`Polar`座標系）によって定義します。
```yaml
coordinate: Polar
```

Dmodelは半極対称のモデルです。
```yaml
has_sym_region: True
```

対称軸はx軸から45°方向です。
```yaml
sym_deg: 45.0
```

1/4部分モデル中には回転対称の領域は存在しません。
```yaml
num_rotate: 0
```

### 材料設定
今回、設計対象はロータコア（材料番号20）とし、
- オン材料→ロータコア（材料番号20）
- オフ材料→空気穴（材料番号600000）
と設定しました。
```yaml
target_ids_and_onoff:
  20:
    - 20
    - 600000
```

材料番号と材料名の割り当てです。
```yaml
physical_id_to_name:
  20: rotor
  30: shaft
  40: airgap
  50000: magnet_0_0_0
  600000: hole_0
```

対称領域への材料IDマップですが、今回対称軸を跨いで変化する材料は無いため、すべて同じ番号にマッピングしています。
```yaml
mirror_id_map:
  20: 20
  30: 30
  40: 40
  50000: 50000
  600000: 600000
```

回転対称領域は無いため、`increment_info`は空です。
```yaml
increment_info: {}
```

### Implicit Domain Meshing オプション
デフォルトではImplicit Domain Meshingは無効化されていますが、`True`にすることで有効化できます。
```yaml
use_implicit_domain_meshing: False
```

設計対象（`20: rotor`）以外は領域分割を行いません。
```yaml
no_split_ids:
  - 30
  - 40
  - 50000
```

また、スライドメッシュ領域（`40: air`）はリメッシュさせたくないため、`no_remesh_ids`に設定します。  
スライドメッシュ領域をリメッシュするとステータ側とのメッシュの整合が取れなくなるためです。
```yaml
no_remesh_ids:
  - 40
```

メッシュの質にかかわる箇所は適当な値に設定します。
```yaml
design_region_size: 0.02
hausd_ratio: 0.0001
hmin_ratio: 0.02
```

最後に、評価スキップ基準値は0.05とします。
```yaml
bad_mesh_threshold: 0.05
```

## optimization.yaml（`Dmodel`プロジェクト）
次に、最適化を設定する`optimization.yaml`の内容を確認します。  
今回は単目的形状最適化のため、`evaluator`は`pyemsol_shape_evaluator`で固定、最適化手法には単目的最適化アルゴリズム`cmaes`（乱数シード固定）を設定しています。  
```yaml
evaluator:
  name: pyemsol_shape_evaluator
optimizer:
  name: cmaes
  kwargs:
    seed: 42
```

レベルセット関数に`ngnet`を設定し、NGnet on/off法によるトポロジー最適化を実施します。`kwargs`は適当な値に設定します。特に、`design_region`にはロータの内径～外径と0°～対称軸の範囲を設定します。
```yaml
level_set_function:
  name: ngnet
  kwargs:
    sigma: 0.0013
    design_region: [[0.008, 0.0275], [0, 45.0]]
                 # [[inner, outer],  [0, sym_deg]]
    coordinate: Polar
```

今回は100イテレーションの最適化とします。  
並列処理はデフォルトでは無効化されていますが、`True`にすることで有効化されます。
```yaml
num_iteration: 100
enable_parallelization: False
num_processes: Null  # if Null, automatically set from cpu counts
```
（出力周りの設定は省略します）

## optimization_problem.yaml（`Dmodel`プロジェクト）
最適化問題の設定（`optimization_problem.yaml`）については[基本の使い方 > 最適化問題の設定](../../docs/getting-started/opt_problem.md)ページに解説があります。  
ここで定義された最適化問題（単目的）は以下の通りです。
```math
\text{minimize} \quad F=f_1+f_2=-1.0\frac{T_\text{avg}}{2.1} + 0.1\frac{T_\text{rip}}{54.0} \\
```
$T_\text{avg}$：平均トルク [Nm]  
$T_\text{rip}$：トルクリプル率 [%]

## 最適化の実施例
Implicit Domain Meshing有（`use_implicit_domain_meshing: True`）として最適化を実施しました。  
下図は100イテレーションの形状の進化過程です（各イテレーションの最良形状をアニメーション化）。序盤はランダムな形状ですが、徐々に一定の特徴を持った形状に収束していく様子が分かります。Implicit Domain Meshingを使用しているため、材料境界は滑らかです。
![Dmodel最適化履歴](/img/Dmodel_best_individuals.gif)

横軸にイテレーション、縦軸に各イテレーションの最良評価値をプロットしたグラフを下図に示します。10イテレーションほどでオリジナルのDmodel（図中黒破線）を凌駕する解が得られていることがわかります。  
また、最終イテレーション付近では評価値の変動がほとんど見られないため、最適化は100世代で十分収束したと判断できます。  
最良の評価値を記録したのは80イテレーション目（図中星印）でした。
![Dmodel最適化収束履歴](/img/convergence.png)

また、進化過程はGUIからも確認できます。（GUIを有効化して`run`コマンド、もしくは最適化完了後に`check`コマンド）
![Dmodel最適化GUI](/img/Dmodel_ex_GUI.gif)

下図が最適化によって得られた最良形状（80イテレーション目）です。平均トルク: 2.2 Nm、トルクリプル率: 10.4 %（Dmodel参照値...平均トルク: 2.1 Nm、トルクリプル率: 54.0 %）  
永久磁石両端に大きなフラックスバリアが生じており、永久磁石磁束が活用される形状になっていることがわかります。
![Dmodel最適形状例](/img/Dmodel_best_ex.png)

:::tip ロータコアの結合制約
なお、今回の最適化ではロータコアに制約を課していないため、最良形状は分離したロータコアを有しています。  
これを分離しないよう制約するには、以下の設定を`optimization_problem.yaml`に追加します。
```yaml
eq_constraints:
  - function_name: num_connected_components
    kwargs:
      physical_tag: 20
    baseline: 1.0
```
`num_connected_components`は指定した材料の連結成分数（＝ひと繋がりになっている領域の数）を計算する関数です。これを`baseline: 1.0`として`eq_constraints`（等式制約リスト）に追加することで、以下の制約条件が最適化に課されます。
```math
N - 1.0 = 0
```
$N$: 連結成分数
:::