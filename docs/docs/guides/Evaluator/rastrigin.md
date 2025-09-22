---
sidebar_position: 2
---

# rastrigin
単目的最適化ベンチマーク関数Rastrigin\[11\]。

## 概要
Rastrigin関数の定義は以下の通りです。
```math
f(\boldsymbol{x}) = 10n + \sum_{i=1}^{n} [x_{i}^{2}-10 \cos (2 \pi x_i)] \\
-5.12 \leq x_i \leq 5.12
```

## 設定可能なキーワード引数一覧
- `dim: int` ... 最適化問題の次元数$n$。
