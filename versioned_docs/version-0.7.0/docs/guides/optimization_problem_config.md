---
sidebar_position: 4
---

# 最適化問題の設定（optimization_problem.yaml）
ここでは、`optimization_problem.yaml`の内容を説明します。  
:::info
各コンフィグの詳細や具体例については[基本の使い方 > 最適化問題の設定](../getting-started/opt_problem.md)をご覧ください。
:::

## Format
凡例：`{設定項目名}: {型名} = デフォルト値`  
デフォルト値の無いものは設定必須項目。
```yaml
case_names: list[str]
objectives: list[OptimizationProblemFunction] = []
ineq_constraints: list[OptimizationProblemFunction] = []
eq_constraints: list[OptimizationProblemFunction] = []
other_metrics: list[OptimizationProblemFunction] = []
```

`OptimizationProblemFunction`は以下の項目を有するコンフィグです。  
```yaml
function_name: str
case_name: str | Null = Null
kwargs: dict[str, Any] = {}
coefficient: float = 1.0
normalization_const: float = 1.0
baseline: float = 0.0
```

## Details
- `case_names: list[str]` ... 解析ケース名リスト。
- `objectives: list[OptimizationProblemFunction]` ... 目的関数リスト。
- `ineq_constraints: list[OptimizationProblemFunction]` ... 不等式制約リスト。
- `eq_constraints: list[OptimizationProblemFunction]` ... 等式制約リスト。
- `other_metrics: list[OptimizationProblemFunction]` ... メトリクスリスト。

### OptimizationProblemFunction
:::info
評価用関数実装例については[評価用関数実装例ページ](./opt_problem_ex.md)をご覧ください。  
各コンフィグの詳細や具体例については[基本の使い方 > 最適化問題の設定](../getting-started/opt_problem.md)をご覧ください。
:::

- `function_name: str` ... 評価用関数名。
- `kwargs: dict[str, Any]` ... 評価用関数への引数。
- `case_name: str | Null` ... 評価用関数の計算に用いる解析ケース名。
- `coefficient: float = 1.0` ... 結果値にかかる係数。
- `normalization_const: float = 1.0` ... 結果値にかかる正規化定数。
- `baseline: float = 0.0` ... 結果値にバイアスするベースライン値。
