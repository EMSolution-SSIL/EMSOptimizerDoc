---
sidebar_position: 6
---

# gradient_update
勾配ベースの更新アルゴリズム実装です。`level_set_function`が`pyemsol_desity`であることを想定しています。

## 概要
勾配ベース手法では，目的関数$f$の設計変数（多くの場合，設計領域中の各セルの密度値やレベルセット値）に関する勾配情報を元に，以下のように設計変数$\boldsymbol{x}$を更新します（最小化問題を想定）\[12\], \[26\], \[27\], \[31\]。  
```math
\boldsymbol{x} \leftarrow \boldsymbol{x} - \alpha \frac{\partial f}{\partial \boldsymbol{x}}
```
ここで$\alpha$はステップサイズを表します。  
また，フェーズフィールド法の拡散反応方程式に基づいた手法では拡散項（設計変数のラプラシアン）が加わります。拡散項は結果形状の複雑さに影響することが知られています\[28\]-\[30\]。
```math
\boldsymbol{x} \leftarrow \boldsymbol{x} + \alpha \left(-M \frac{\partial f}{\partial \boldsymbol{x}} + \tau \nabla^2 \boldsymbol{x}\right)
```

## 設定可能なキーワード引数一覧
- `init_uniform_value: float` ... 設計変数の初期値。全設計変数にこの値が初期値として与えられる。
- `init_value_filepath: str | null` ... 設計変数の初期値を格納したファイルパス。この引数を指定した場合，`init_uniform_value`より優先される。
- `bounds: tuple[float, float] | null` ... 設計変数の上下限値。`null`の場合，自動的に\[-1,1\]が設定される。
- `step_size: float` ... ステップサイズ$\alpha$。デフォルトは`1.0`。
- `reaction_coef: float` ... 反応項係数$M$\[28\]-\[30\]。デフォルトは`1.0`。
- `diffusion_coef: float` ... 拡散項係数$\tau$\[28\]-\[30\]。デフォルトは`1.0`。
- `move_limit: float` ... ムーブリミット\[31\]。一回の更新で設計変数が変化する範囲を\[-move_limit, +move_limit\]に制限する。デフォルトは`0.2`。
- `damping_factor: float` ... ムーブリミットの減衰係数\[31\]。目的関数値が悪化したとき，ムーブリミットを減衰係数倍することで目的関数の振動（改善と悪化を繰り返し，収束しない現象）を抑制する。デフォルトは`0.99`。
- `scaling_mode: str` ... 勾配のスケーリングモード。`none`: 解析から得られる勾配値をそのまま使用する。 `max`: 勾配値を上下限値と最大値によってスケーリングする。 `sign`: 勾配値の符号のみ参照し，+なら上限値，-なら下限値を勾配として設定する。ただし，いずれのモードでも設計変数の変化量は`move_limit`により制約される。
- `constraint_mode: str` ... 制約モード。`none`: 制約無。 `volume_penalty`: 体積制約。
- `volume_frac_ulim: float` ... 体積制約の上限値（割合）。`0.5`であれば，材料密度の積分値が設計領域全域の50%以下となるよう制約する。
- `volume_penalty_coef: float` ... 制約モード`volume_penalty`時，制約違反量に対するペナルティ係数。制約違反量×ペナルティ係数の分，全体の密度値が下がるよう勾配を調整する。
