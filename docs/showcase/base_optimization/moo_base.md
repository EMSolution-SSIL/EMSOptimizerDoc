---
sidebar_position: 2
---

# moo_base紹介
ここでは、`moo_base`プロジェクトの内容について紹介します。  
本プロジェクトでは、多目的ベンチマーク関数ZDT1\[9\]の最適化を行います。

## optimization.yaml（`moo_base`プロジェクト）
`optimization.yaml`の内容を確認します。  
評価関数`evaluator`はZDT1関数実装`zdt1`です（設計変数の数は30）。  
最適化手法`optimizer`は多目的最適化アルゴリズム`nsga2`（乱数シード固定）です。設計変数の上下限値は\[0, 1\] です。  
```yaml
evaluator:
  name: zdt1
optimizer:
  name: nsga2
  kwargs:
    seed: 42
    bounds: [0.0, 1.0]
```

今回は30イテレーションの最適化とします。  
```yaml
num_iteration: 30
```
（出力周りの設定は省略します）

## 最適化の実施例
30イテレーション最適化完了後のGUIを以下に示します。真のパレートフロントに近い解が得られていることが分かります。  
![moo_base GUI](/img/moo_base_GUI.png)
