---
sidebar_position: 2
---

# SimpleLevelSetRadius
半径ごとにレベルを設定するシンプルなLevelSetFunction実装です。

## 概要
例として、コンフィグ`num_level`が`3`のときは、寸法パラメータ$\boldsymbol{w}$と設計領域の各点の半径$r$に基づき以下の値を返します。
- $r < w_0$ → 1
- $w_0 < r < w_0 + w_1$ → 0
- $w_0 + w_1 < r$ → -1

これにより、$r < w_0$の領域では`level 0`、$w_0 < r < w_0 + w_1$の領域では`level 1`, $w_0 + w_1 < r2$の領域では`level 2`の材料がそれぞれ割り当てられます。

## 設定可能なキーワード引数一覧
- `num_level: int` ... 設定するレベルの数。
- `scale: float` ... 寸法パラメータ$\boldsymbol{w}$に乗じるスケール。デフォルト値は`1.0`。
