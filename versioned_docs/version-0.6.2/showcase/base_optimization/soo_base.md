---
sidebar_position: 1
---

# soo_base紹介
ここでは、`soo_base`プロジェクトの内容について紹介します。  
本プロジェクトでは、単目的ベンチマーク関数Sphere\[11\]の最適化を行います。

## optimization.yaml（`soo_base`プロジェクト）
`optimization.yaml`の内容を確認します。  
評価関数`evaluator`はSphere関数実装`sphere`とし、その設計変数の数（最適化問題の次元）`dim`を`30`に設定しています。  
最適化手法`optimizer`は単目的最適化アルゴリズム`cmaes`（乱数シード固定）です。ここでは、設計変数の上下限値を\[-5.12, 5.12\] の範囲に制約します。これを`bounds`に設定しています。  
```yaml
evaluator:
  name: sphere
  kwargs:
    dim: 30
optimizer:
  name: cmaes
  kwargs:
    bounds: [-5.12, 5.12]
    seed: 42
```

今回は100イテレーションの最適化とします。  
```yaml
num_iteration: 100
```
（出力周りの設定は省略します）

## 最適化の実施例
100イテレーション最適化完了後のGUIを以下に示します。関数値が徐々に0に収束していく様子が分かります。  
![soo_base GUI](/img/soo_base_GUI.png)
