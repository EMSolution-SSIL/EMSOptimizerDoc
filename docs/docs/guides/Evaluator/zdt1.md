---
sidebar_position: 2
---

# zdt1
多目的最適化ベンチマーク関数ZDT1\[9\]。

## 概要
ZDT1関数の定義は以下の通りです。
```math
f_1(\boldsymbol{x}) = x_1 \\
f_2(\boldsymbol{x}) = g(\boldsymbol{x}) h(\boldsymbol{x}) \\
g(\boldsymbol{x}) = 1 + 9 \sum_{i=2}^{n} x_i \\
h(\boldsymbol{x}) = 1 - \sqrt{f_1 / g} \\
n=30, 0 \leq x_i \leq 1
```

## 設定可能なキーワード引数一覧
なし
