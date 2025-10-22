---
sidebar_position: 1
---

# IPM8P48S説明＆基本の最適化例
ここでは、IPM8P48Sの説明、および`IPM8P48S_moo`プロジェクトの内容について紹介します。

## モデル説明
IPM8P48Sは8極48スロット（分布巻）の埋め込み型永久磁石同期モータ（IPMSM）バーチャルモデルです。文献\[16\]にて提案されたモータモデル群の一つで、自動車駆動用のモータが元となっています。    
`IPM8P48S_moo`プロジェクト同梱のメッシュは1/8部分モデルで、各領域には材料情報（材料番号：材料名）が割り当てられています。  
下図はロータ部分のモデルと材料情報です。トポロジー最適化のため、元のモデルにあった空気穴（フラックスバリア）はロータコアで埋めてあります。

![IPM8P48S example](/img/IPM8P48S_ex.png)

## machine.yaml（`IPM8P48S_moo`プロジェクト）
まず、機器情報を設定する`machine.yaml`の内容を確認します。
### 基本設定
IPM8P48Sは半径と角度（`Polar`座標系）によって定義します。
```yaml
coordinate: Polar
```

IPM8P48Sは半極対称のモデルです。
```yaml
has_sym_region: True
```

対称軸はx軸から22.5°方向です。
```yaml
sym_deg: 22.5
```

1/8部分モデル中には回転対称の領域は存在しません。
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
  50001: magnet_1_0_0
  600000: hole_0
```

対称領域への材料IDマップです。**永久磁石`50000`は対称軸を跨いで`50001`に変化するため、そのマッピングをここで行います**。それ以外の材料は対称軸を跨いで変化しないため、同じ番号にマッピングします。
```yaml
mirror_id_map:
  20: 20
  30: 30
  40: 40
  50000: 50001
  600000: 600000
```

回転対称領域は無いため、`increment_info`は空です。
```yaml
increment_info: {}
```

### Implicit Domain Meshing オプション
Implicit Domain Meshingはデフォルトで有効としています。
```yaml
use_implicit_domain_meshing: True
```

設計対象（`20: rotor`）以外は領域分割を行いません。
```yaml
no_split_ids:
  - 30
  - 40
  - 50000
  - 50001
```

また、スライドメッシュ領域（`40: air`）はリメッシュさせたくないため、`no_remesh_ids`に設定します。  
スライドメッシュ領域をリメッシュするとステータ側とのメッシュの整合が取れなくなるためです。
```yaml
no_remesh_ids:
  - 40
```

メッシュの質にかかわる箇所は適当な値に設定します。
```yaml
design_region_size: 0.04
hausd_ratio: 0.0001
hmin_ratio: 0.02
```

最後に、評価スキップ基準値は0.02とします。IPM8P48Sの場合はDmodelと比較して最適化過程で扁平な要素が生成されやすいため、今回は最適化の性能を優先してやや低い基準値としています。
```yaml
bad_mesh_threshold: 0.02
```

## optimization.yaml（`IPM8P48S_moo`プロジェクト）
次に、最適化を設定する`optimization.yaml`の内容を確認します。  
今回は多目的形状最適化のため、最適化手法に多目的最適化アルゴリズム`decomposition_ensemble`を設定しています。本アルゴリズムの詳細については[docsの該当ページ](../../docs/guides/Optimizer/decomposition_ensemble.md)をご覧ください。  
```yaml
evaluator:
  name: pyemsol_shape_evaluator
optimizer:
  name: decomposition_ensemble
  kwargs:
    num_decomposition: 5
    seed: 42
```

レベルセット関数に`ngnet`を設定し、NGnet on/off法によるトポロジー最適化を実施します。
```yaml
level_set_function:
  name: ngnet
  kwargs:
    sigma: 0.003
    design_region: [[0.040, 0.0802], [0, 22.5]]
    coordinate: Polar
```

今回は100イテレーションの最適化とします。  
並列処理はデフォルトで有効としています。
```yaml
num_iteration: 100
enable_parallelization: True
num_processes: Null  # if Null, automatically set from cpu counts
```
（出力周りの設定は省略します）

## optimization_problem.yaml（`IPM8P48S_moo`プロジェクト）
最適化問題（多目的）は以下の通りです。ここでは、平均トルクとトルクリプル率の両方を考慮しつつ、平均トルクについてはオリジナルモデルの値14.62Nmを超えるよう制約をかけています。また、ロータコアの結合制約も考慮しています。
```math
\begin{align*}
\text{minimize} \quad & f_1=-\frac{T_\text{avg}}{14.62} \\
                      & f_2=\frac{T_\text{rip}}{35.34} \\
\text{subject to} \quad & g_1=-(T_\text{avg}-14.62) \leq 0 \\
                        & h_1=N-1 = 0 \\
\end{align*}
```
$T_\text{avg}$：平均トルク [Nm]  
$T_\text{rip}$：トルクリプル率 [%]  
$N$: 連結成分数

## 最適化の実施例
100イテレーション最適化完了後のGUIを以下に示します。比較的広範囲に均一なパレートフロントが得られました。  
表示している形状例はそれぞれパレートフロント図の"Left", "Right"の解形状です。フラックスバリアの配置は似ていますが、回転子表面側のフラックスバリアに特徴がみられます。"Right"では細長いフラックスバリアが得られており、平均トルクとトルクリプル率のバランスが比較的良いと言えます。一方で、"Left"では半円状のフラックスバリアが磁束を閉じ込めるように配置されており、高トルクなモータとなっていると推察されます。
![IPM8P48Sパレートフロント](/img/IPM8P48S_moo_check.png)